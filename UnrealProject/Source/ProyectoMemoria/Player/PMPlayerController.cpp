#include "PMPlayerController.h"

#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "UserSettings/EnhancedInputUserSettings.h"
#include "Engine/LocalPlayer.h"
#include "InputCoreTypes.h"
#include "InputAction.h"
#include "InputActionValue.h"
#include "PMCameraModeComponent.h"
#include "PMGameUserSettings.h"
#include "PMPlayerCharacter.h"
#include "PMInteractableInterface.h"
#include "PMInteractableDoor.h"
#include "PMMemoryPickup.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Engine/PointLight.h"
#include "Components/LightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Engine/GameViewportClient.h"
#include "Engine/Engine.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SOverlay.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SCheckBox.h"
#include "Widgets/Input/SSlider.h"
#include "Widgets/Text/STextBlock.h"
#include "Styling/CoreStyle.h"

DEFINE_LOG_CATEGORY_STATIC(LogPMPlayerController, Log, All);

APMPlayerController::APMPlayerController()
{
	LookSensitivityX = 1.0f;
	LookSensitivityY = 1.0f;
	bInvertLookY = false;
	MappingPriority = 0;
	CrouchHoldThreshold = 0.25f;
	bCrouchInputActive = false;
	bWasCrouchedWhenInputStarted = false;
	bMappingContextAdded = false;
	PreferredCameraMode = EPMCameraMode::FirstPerson;
	bCameraPreferenceLoaded = false;
	bMenuOpen = false;
	bMainMenuOpen = false;
	bSettingsOpen = false;
	bControllerTab = false;
	MemoryFragmentsCollected = 0;
}

void APMPlayerController::BeginPlay()
{
	Super::BeginPlay();
	if (UPMGameUserSettings* Settings = UPMGameUserSettings::GetPMGameUserSettings())
	{
		LookSensitivityX = Settings->GetLookSensitivityX();
		LookSensitivityY = Settings->GetLookSensitivityY();
		bInvertLookY = Settings->GetInvertLookY();
	}

	ApplyPreferredCameraModeToPawn();
	EnsureTestInteractableDoor();
	EnsureTestMemoryPickup();
	if (GetWorld())
	{
		if (ADirectionalLight* Sun = GetWorld()->SpawnActor<ADirectionalLight>(FVector::ZeroVector, FRotator(-45.0f, -35.0f, 0.0f)))
		{
			Sun->GetLightComponent()->SetIntensity(10.0f);
		}
		if (ASkyLight* Sky = GetWorld()->SpawnActor<ASkyLight>(FVector(0.0f, 0.0f, 800.0f), FRotator::ZeroRotator))
		{
			Sky->GetLightComponent()->SetIntensity(4.0f);
		}
		if (APointLight* Fill = GetWorld()->SpawnActor<APointLight>(FVector(0.0f, 0.0f, 300.0f), FRotator::ZeroRotator))
		{
			Fill->PointLightComponent->SetIntensity(2500.0f);
			Fill->PointLightComponent->SetAttenuationRadius(1800.0f);
		}
	}

	ULocalPlayer* LocalPlayer = GetLocalPlayer();
	if (!LocalPlayer)
	{
		return;
	}

	if (!PlayerMappingContext)
	{
		UE_LOG(
			LogPMPlayerController,
			Warning,
			TEXT("%s has no IMC_Player assigned; player input will remain disabled."),
			*GetNameSafe(this));
		return;
	}

	if (UEnhancedInputLocalPlayerSubsystem* InputSubsystem =
		LocalPlayer->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
	{
		InputSubsystem->AddMappingContext(PlayerMappingContext, MappingPriority);
		bMappingContextAdded = true;
		if (UEnhancedInputUserSettings* UserSettings = InputSubsystem->GetUserSettings())
		{
			UserSettings->RegisterInputMappingContext(PlayerMappingContext);
		}
	}

	OpenMainMenu();
	if (GEngine)
	{
		GEngine->AddOnScreenDebugMessage(-1, 4.0f, FColor::White,
			TEXT("Fragmentos de memoria: 0"));
	}
}

void APMPlayerController::RegisterMemoryPickupCollected()
{
	++MemoryFragmentsCollected;
	if (GEngine)
	{
		GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Yellow,
			FString::Printf(TEXT("Fragmento de memoria encontrado (%d)"), MemoryFragmentsCollected));
	}
}

void APMPlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	ResetTransientPawnInputState();

	// El LocalPlayer puede sobrevivir a este controller; por eso retiramos el IMC propio.
	if (bMappingContextAdded && PlayerMappingContext)
	{
		if (ULocalPlayer* LocalPlayer = GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* InputSubsystem =
				LocalPlayer->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
			{
				InputSubsystem->RemoveMappingContext(PlayerMappingContext);
			}
		}
	}

	bMappingContextAdded = false;
	Super::EndPlay(EndPlayReason);
}

void APMPlayerController::OnUnPossess()
{
	// Limpia las órdenes mantenidas antes de que Super elimine la referencia al Pawn.
	ResetTransientPawnInputState();
	Super::OnUnPossess();
}

void APMPlayerController::SetPawn(APawn* InPawn)
{
	Super::SetPawn(InPawn);
	ApplyPreferredCameraModeToPawn();
	EnsureTestInteractableDoor();
	EnsureTestMemoryPickup();
}

void APMPlayerController::EnsureTestInteractableDoor()
{
	if (TestInteractableDoor || !GetWorld())
	{
		return;
	}
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		const FVector DoorLocation = PMCharacter->GetActorLocation()
			+ PMCharacter->GetActorForwardVector() * 450.0f
			+ PMCharacter->GetActorRightVector() * 80.0f;
		FActorSpawnParameters SpawnParameters;
		SpawnParameters.Owner = this;
		TestInteractableDoor = GetWorld()->SpawnActor<APMInteractableDoor>(
			APMInteractableDoor::StaticClass(), DoorLocation, PMCharacter->GetActorRotation(), SpawnParameters);
		if (TestInteractableDoor)
		{
			TestInteractableDoor->SetActorLabel(TEXT("Gameplay_InteractableDoor_Runtime"));
			UE_LOG(LogPMPlayerController, Log, TEXT("Runtime interactable door spawned at %s"), *DoorLocation.ToString());
		}
	}
}

void APMPlayerController::EnsureTestMemoryPickup()
{
	if (TestMemoryPickup || !GetWorld())
	{
		return;
	}
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		const FVector PickupLocation = PMCharacter->GetActorLocation()
			+ PMCharacter->GetActorForwardVector() * 700.0f
			+ PMCharacter->GetActorRightVector() * 300.0f
			+ FVector(0.0f, 0.0f, 100.0f);
		FActorSpawnParameters SpawnParameters;
		SpawnParameters.Owner = this;
		TestMemoryPickup = GetWorld()->SpawnActor<APMMemoryPickup>(
			APMMemoryPickup::StaticClass(), PickupLocation, FRotator::ZeroRotator, SpawnParameters);
		if (TestMemoryPickup)
		{
			TestMemoryPickup->SetActorLabel(TEXT("Gameplay_MemoryPickup_Runtime"));
		}
	}
}

void APMPlayerController::SetupInputComponent()
{
	Super::SetupInputComponent();

	UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(InputComponent);
	if (!EnhancedInput)
	{
		UE_LOG(
			LogPMPlayerController,
			Warning,
			TEXT("APMPlayerController requires EnhancedInputComponent."));
		return;
	}

	InputComponent->BindKey(EKeys::Escape, IE_Pressed, this, &APMPlayerController::HandleEscape);
	InputComponent->BindKey(EKeys::E, IE_Pressed, this, &APMPlayerController::HandleInteract);

	if (!MoveAction || !LookAction || !SprintAction || !CrouchAction
		|| !JumpAction || !ToggleCameraAction)
	{
		UE_LOG(
			LogPMPlayerController,
			Warning,
			TEXT("%s has one or more unassigned IA_* assets; only assigned actions will work."),
			*GetNameSafe(this));
	}

	if (MoveAction)
	{
		EnhancedInput->BindAction(
			MoveAction,
			ETriggerEvent::Triggered,
			this,
			&APMPlayerController::HandleMove);
	}

	if (LookAction)
	{
		EnhancedInput->BindAction(
			LookAction,
			ETriggerEvent::Triggered,
			this,
			&APMPlayerController::HandleLook);
	}

	if (SprintAction)
	{
		EnhancedInput->BindAction(
			SprintAction,
			ETriggerEvent::Started,
			this,
			&APMPlayerController::HandleSprintStarted);
		EnhancedInput->BindAction(
			SprintAction,
			ETriggerEvent::Completed,
			this,
			&APMPlayerController::HandleSprintCompleted);
		EnhancedInput->BindAction(
			SprintAction,
			ETriggerEvent::Canceled,
			this,
			&APMPlayerController::HandleSprintCompleted);
	}

	if (CrouchAction)
	{
		EnhancedInput->BindAction(
			CrouchAction,
			ETriggerEvent::Started,
			this,
			&APMPlayerController::HandleCrouchStarted);
		EnhancedInput->BindAction(
			CrouchAction,
			ETriggerEvent::Completed,
			this,
			&APMPlayerController::HandleCrouchCompleted);
		EnhancedInput->BindAction(
			CrouchAction,
			ETriggerEvent::Canceled,
			this,
			&APMPlayerController::HandleCrouchCanceled);
	}

	if (JumpAction)
	{
		EnhancedInput->BindAction(
			JumpAction,
			ETriggerEvent::Started,
			this,
			&APMPlayerController::HandleJumpStarted);
		EnhancedInput->BindAction(
			JumpAction,
			ETriggerEvent::Completed,
			this,
			&APMPlayerController::HandleJumpCompleted);
		EnhancedInput->BindAction(
			JumpAction,
			ETriggerEvent::Canceled,
			this,
			&APMPlayerController::HandleJumpCompleted);
	}

	if (ToggleCameraAction)
	{
		EnhancedInput->BindAction(
			ToggleCameraAction,
			ETriggerEvent::Started,
			this,
			&APMPlayerController::HandleToggleCamera);
	}
}

bool APMPlayerController::InputKey(const FInputKeyEventArgs& Params)
{
	if (Params.Key.IsGamepadKey() && Params.Event == IE_Pressed)
	{
		UE_LOG(LogPMPlayerController, Log, TEXT("Gamepad key received: %s"), *Params.Key.GetFName().ToString());
	}
	if (Params.Key == EKeys::Gamepad_FaceButton_Left && Params.Event == IE_Pressed)
	{
		HandleInteract();
	}
	return Super::InputKey(Params);
}

void APMPlayerController::HandleInteract()
{
	FVector ViewLocation;
	FRotator ViewRotation;
	GetPlayerViewPoint(ViewLocation, ViewRotation);
	const FVector TraceEnd = ViewLocation + ViewRotation.Vector() * 250.0f;
	FCollisionQueryParams QueryParams(SCENE_QUERY_STAT(PMInteract), true, GetPawn());
	FHitResult Hit;
	if (GetWorld() && GetWorld()->LineTraceSingleByChannel(Hit, ViewLocation, TraceEnd, ECC_Visibility, QueryParams))
	{
		if (AActor* Actor = Hit.GetActor(); Actor && Actor->GetClass()->ImplementsInterface(UPMInteractableInterface::StaticClass()))
		{
			IPMInteractableInterface::Execute_Interact(Actor, GetPMPlayerCharacter());
			return;
		}
	}

	// Tolerancia para la puerta de prueba: cerca de ella no exige apuntar al píxel exacto.
	if (TestInteractableDoor && GetPawn() &&
		FVector::DistSquared(GetPawn()->GetActorLocation(), TestInteractableDoor->GetActorLocation()) <= FMath::Square(300.0f))
	{
		TestInteractableDoor->Interact_Implementation(GetPMPlayerCharacter());
	}
	if (TestMemoryPickup && GetPawn() &&
		FVector::DistSquared(GetPawn()->GetActorLocation(), TestMemoryPickup->GetActorLocation()) <= FMath::Square(300.0f))
	{
		TestMemoryPickup->Interact_Implementation(GetPMPlayerCharacter());
	}
}

void APMPlayerController::OpenMainMenu()
{
	bMenuOpen = true;
	bMainMenuOpen = true;
	bSettingsOpen = false;
	bControllerTab = false;
	RebuildSlateMenu();
	SetPause(true);
	SetInputMode(FInputModeUIOnly());
	bShowMouseCursor = true;
}

void APMPlayerController::OpenPauseMenu()
{
	bMenuOpen = true;
	bMainMenuOpen = false;
	bSettingsOpen = false;
	bControllerTab = false;
	RebuildSlateMenu();
	SetPause(true);
	SetInputMode(FInputModeUIOnly());
	bShowMouseCursor = true;
}

void APMPlayerController::CloseMenuAndResume()
{
	bMenuOpen = false;
	bMainMenuOpen = false;
	bSettingsOpen = false;
	if (SlateMenu)
	{
		SlateMenu->ClearChildren();
	}
	SetPause(false);
	FInputModeGameOnly InputMode;
	SetInputMode(InputMode);
	bShowMouseCursor = false;
}

void APMPlayerController::HandleEscape()
{
	if (bMainMenuOpen)
	{
		return;
	}

	if (bMenuOpen)
	{
		if (bSettingsOpen)
		{
			OpenPauseMenu();
		}
		else
		{
			CloseMenuAndResume();
		}
		return;
	}

	OpenPauseMenu();
}

void APMPlayerController::ResetLookSettings()
{
	SetLookSensitivity(1.0f, 1.0f);
	SetInvertLookY(false);
}

void APMPlayerController::RebuildSlateMenu()
{
	if (!GEngine || !GEngine->GameViewport)
	{
		return;
	}

	if (!SlateMenu)
	{
		SAssignNew(SlateMenu, SOverlay);
		GEngine->GameViewport->AddViewportWidgetContent(SlateMenu.ToSharedRef(), 100);
	}

	SlateMenu->ClearChildren();
	TSharedRef<SVerticalBox> Column = SNew(SVerticalBox);
	const FText Title = bSettingsOpen ? FText::FromString(TEXT("Configuración"))
		: (bMainMenuOpen ? FText::FromString(TEXT("Proyecto Memoria")) : FText::FromString(TEXT("Pausa")));
	Column->AddSlot().AutoHeight().Padding(10)[SNew(STextBlock).Text(Title).Font(FCoreStyle::GetDefaultFontStyle("Bold", 32)).Justification(ETextJustify::Center)];

	const auto AddButton = [&Column](const TCHAR* Label, TFunction<FReply()> Callback)
	{
		Column->AddSlot().AutoHeight().Padding(8)[
			SNew(SBox).HeightOverride(58.0f)[
				SNew(SButton).OnClicked_Lambda(MoveTemp(Callback))[
					SNew(STextBlock).Text(FText::FromString(Label)).Font(FCoreStyle::GetDefaultFontStyle("Regular", 22)).Justification(ETextJustify::Center)]]];
	};

	if (bSettingsOpen)
	{
		Column->AddSlot().AutoHeight().Padding(8)[SNew(STextBlock).Text(FText::FromString(TEXT("Sensibilidad horizontal"))).Font(FCoreStyle::GetDefaultFontStyle("Regular", 22))];
		AddButton(TEXT("Teclado y mouse"), [this](){ bControllerTab = false; RebuildSlateMenu(); return FReply::Handled(); });
		AddButton(TEXT("Mando"), [this](){ bControllerTab = true; RebuildSlateMenu(); return FReply::Handled(); });
		const TCHAR* MappingText = bControllerTab
			? TEXT("Mando:\nStick izquierdo: mover\nStick derecho: mirar\nL3: correr\nB/Círculo: agacharse\nA/X: saltar\nY/Triángulo: cambiar cámara")
			: TEXT("Teclado y mouse:\nWASD: mover\nShift: correr\nC: agacharse\nSpace: saltar\nV: cambiar cámara\nMouse: mirar");
		Column->AddSlot().AutoHeight().Padding(8)[SNew(STextBlock).Text(FText::FromString(MappingText)).Font(FCoreStyle::GetDefaultFontStyle("Regular", 20))];
		Column->AddSlot().AutoHeight().Padding(8)[SNew(SBox).HeightOverride(42.0f)[SNew(SSlider).Value_Lambda([this](){ return GetLookSensitivityX() * 0.5f; }).OnValueChanged_Lambda([this](float Value){ SetLookSensitivity(Value * 2.0f, GetLookSensitivityY()); })]];
		Column->AddSlot().AutoHeight().Padding(8)[SNew(STextBlock).Text(FText::FromString(TEXT("Sensibilidad vertical"))).Font(FCoreStyle::GetDefaultFontStyle("Regular", 22))];
		Column->AddSlot().AutoHeight().Padding(8)[SNew(SBox).HeightOverride(42.0f)[SNew(SSlider).Value_Lambda([this](){ return GetLookSensitivityY() * 0.5f; }).OnValueChanged_Lambda([this](float Value){ SetLookSensitivity(GetLookSensitivityX(), Value * 2.0f); })]];
		Column->AddSlot().AutoHeight().Padding(8)[SNew(SCheckBox).IsChecked_Lambda([this](){ return GetInvertLookY() ? ECheckBoxState::Checked : ECheckBoxState::Unchecked; }).OnCheckStateChanged_Lambda([this](ECheckBoxState State){ SetInvertLookY(State == ECheckBoxState::Checked); })[SNew(STextBlock).Text(FText::FromString(TEXT("Invertir cámara vertical"))).Font(FCoreStyle::GetDefaultFontStyle("Regular", 22))]];
		AddButton(TEXT("Restaurar valores"), [this](){ ResetLookSettings(); RebuildSlateMenu(); return FReply::Handled(); });
		AddButton(TEXT("Volver"), [this](){ OpenPauseMenu(); return FReply::Handled(); });
	}
	else if (bMainMenuOpen)
	{
		AddButton(TEXT("Jugar"), [this](){ CloseMenuAndResume(); return FReply::Handled(); });
		AddButton(TEXT("Configuración"), [this](){ bSettingsOpen = true; RebuildSlateMenu(); return FReply::Handled(); });
		AddButton(TEXT("Salir"), [this](){ UKismetSystemLibrary::QuitGame(this, this, EQuitPreference::Quit, false); return FReply::Handled(); });
	}
	else
	{
		AddButton(TEXT("Continuar"), [this](){ CloseMenuAndResume(); return FReply::Handled(); });
		AddButton(TEXT("Configuración"), [this](){ bSettingsOpen = true; RebuildSlateMenu(); return FReply::Handled(); });
		AddButton(TEXT("Volver al menú principal"), [this](){ OpenMainMenu(); return FReply::Handled(); });
		AddButton(TEXT("Salir"), [this](){ UKismetSystemLibrary::QuitGame(this, this, EQuitPreference::Quit, false); return FReply::Handled(); });
	}

	SlateMenu->AddSlot().HAlign(HAlign_Center).VAlign(VAlign_Center)[
		SNew(SBorder).Padding(42.0f).BorderBackgroundColor(FLinearColor(0.015f, 0.02f, 0.03f, 0.96f))[
			SNew(SBox).WidthOverride(720.0f).HeightOverride(560.0f)[Column]]];
}

APMPlayerCharacter* APMPlayerController::GetPMPlayerCharacter() const
{
	return Cast<APMPlayerCharacter>(GetPawn());
}

void APMPlayerController::SetLookSensitivity(
	const float HorizontalSensitivity,
	const float VerticalSensitivity)
{
	LookSensitivityX = FMath::Max(0.0f, HorizontalSensitivity);
	LookSensitivityY = FMath::Max(0.0f, VerticalSensitivity);
	if (UPMGameUserSettings* Settings = UPMGameUserSettings::GetPMGameUserSettings())
	{
		Settings->SetLookSettings(LookSensitivityX, LookSensitivityY, bInvertLookY);
		Settings->SaveSettings();
	}
}

void APMPlayerController::SetInvertLookY(const bool bShouldInvert)
{
	bInvertLookY = bShouldInvert;
	if (UPMGameUserSettings* Settings = UPMGameUserSettings::GetPMGameUserSettings())
	{
		Settings->SetLookSettings(LookSensitivityX, LookSensitivityY, bInvertLookY);
		Settings->SaveSettings();
	}
}

void APMPlayerController::HandleMove(const FInputActionValue& Value)
{
	APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter();
	if (!PMCharacter)
	{
		return;
	}

	const FVector2D MovementInput = Value.Get<FVector2D>();
	const FRotator ControllerRotation = GetControlRotation();
	const FRotator YawRotation(0.0f, ControllerRotation.Yaw, 0.0f);

	const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
	const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);

	PMCharacter->AddMovementInput(ForwardDirection, MovementInput.Y);
	PMCharacter->AddMovementInput(RightDirection, MovementInput.X);
}

void APMPlayerController::HandleLook(const FInputActionValue& Value)
{
	const FVector2D LookInput = Value.Get<FVector2D>();
	// Mouse Y is negative when the physical mouse moves upward.  Gamepad
	// right-stick Y arrives with the opposite sign on the XInput path, so
	// normalize that device-specific sign before applying the user preference.
	const bool bGamepadLookActive = FMath::Abs(GetInputAnalogKeyState(EKeys::Gamepad_RightY)) > KINDA_SMALL_NUMBER;
	const float DeviceDirection = bGamepadLookActive ? 1.0f : -1.0f;
	const float VerticalDirection = bInvertLookY ? -DeviceDirection : DeviceDirection;

	AddYawInput(LookInput.X * LookSensitivityX);
	AddPitchInput(LookInput.Y * LookSensitivityY * VerticalDirection);
}

void APMPlayerController::HandleSprintStarted()
{
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		PMCharacter->SetSprinting(true);
	}
}

void APMPlayerController::HandleSprintCompleted()
{
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		PMCharacter->SetSprinting(false);
	}
}

void APMPlayerController::HandleCrouchStarted()
{
	// Recupera un gesto anterior si Enhanced Input perdió su evento de cierre.
	if (bCrouchInputActive)
	{
		HandleCrouchCanceled();
	}

	APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter();
	if (!PMCharacter)
	{
		return;
	}

	CrouchInputCharacter = PMCharacter;
	bCrouchInputActive = true;
	bWasCrouchedWhenInputStarted = PMCharacter->IsCrouched();

	// La respuesta visual es inmediata; al soltar se decide entre toque y hold.
	if (!bWasCrouchedWhenInputStarted)
	{
		PMCharacter->SetCrouching(true);
	}
}

void APMPlayerController::HandleCrouchCompleted(const FInputActionInstance& Instance)
{
	if (!bCrouchInputActive)
	{
		return;
	}

	if (APMPlayerCharacter* PMCharacter = CrouchInputCharacter.Get())
	{
		const bool bWasHeld = Instance.GetElapsedTime() >= CrouchHoldThreshold;

		// Hold siempre termina de pie. Un toque solo levanta si empezó agachado.
		if (bWasHeld || bWasCrouchedWhenInputStarted)
		{
			PMCharacter->SetCrouching(false);
		}
	}

	ResetCrouchInputState();
}

void APMPlayerController::HandleCrouchCanceled()
{
	if (!bCrouchInputActive)
	{
		return;
	}

	if (APMPlayerCharacter* PMCharacter = CrouchInputCharacter.Get())
	{
		// Una cancelación no cuenta como toque: restaura la postura inicial.
		PMCharacter->SetCrouching(bWasCrouchedWhenInputStarted);
	}

	ResetCrouchInputState();
}

void APMPlayerController::HandleJumpStarted()
{
	JumpInputCharacter.Reset();

	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		if (PMCharacter->TryJumpFromCurrentPosture())
		{
			JumpInputCharacter = PMCharacter;
		}
	}
}

void APMPlayerController::HandleJumpCompleted()
{
	if (APMPlayerCharacter* PMCharacter = JumpInputCharacter.Get())
	{
		PMCharacter->StopJumping();
	}

	JumpInputCharacter.Reset();
}

void APMPlayerController::ResetCrouchInputState()
{
	CrouchInputCharacter.Reset();
	bCrouchInputActive = false;
	bWasCrouchedWhenInputStarted = false;
}

void APMPlayerController::ResetTransientPawnInputState()
{
	// Completed puede no llegar si se pierde la posesión con Sprint presionado.
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		PMCharacter->SetSprinting(false);
	}

	HandleJumpCompleted();
	HandleCrouchCanceled();
}

void APMPlayerController::HandleToggleCamera()
{
	APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter();
	if (!PMCharacter)
	{
		return;
	}

	if (UPMCameraModeComponent* CameraMode = PMCharacter->GetCameraModeComponent())
	{
		const EPMCameraMode NewMode =
			CameraMode->GetCameraMode() == EPMCameraMode::FirstPerson
			? EPMCameraMode::ThirdPerson
			: EPMCameraMode::FirstPerson;
		SetPlayerCameraMode(NewMode);
	}
}

bool APMPlayerController::EnsureCameraPreferenceLoaded()
{
	if (bCameraPreferenceLoaded)
	{
		return true;
	}

	if (!GetLocalPlayer())
	{
		return false;
	}

	bCameraPreferenceLoaded = true;
	if (const UPMGameUserSettings* Settings =
		UPMGameUserSettings::GetPMGameUserSettings())
	{
		PreferredCameraMode = Settings->GetPreferredCameraMode();
		return true;
	}

	UE_LOG(
		LogPMPlayerController,
		Warning,
		TEXT("PMGameUserSettings is not active; camera preference will last only for this session."));
	return true;
}

void APMPlayerController::ApplyPreferredCameraModeToPawn()
{
	if (!EnsureCameraPreferenceLoaded())
	{
		return;
	}

	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		if (UPMCameraModeComponent* CameraMode = PMCharacter->GetCameraModeComponent())
		{
			CameraMode->SetCameraMode(PreferredCameraMode);
		}
	}
}

bool APMPlayerController::SetPlayerCameraMode(const EPMCameraMode NewMode)
{
	APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter();
	if (!PMCharacter)
	{
		return false;
	}

	UPMCameraModeComponent* CameraMode = PMCharacter->GetCameraModeComponent();
	if (!CameraMode || !CameraMode->SetCameraMode(NewMode))
	{
		return false;
	}

	PreferredCameraMode = CameraMode->GetCameraMode();
	bCameraPreferenceLoaded = true;
	PersistPreferredCameraMode();
	return true;
}

void APMPlayerController::PersistPreferredCameraMode()
{
	UPMGameUserSettings* Settings = UPMGameUserSettings::GetPMGameUserSettings();
	if (!Settings || !Settings->SetPreferredCameraMode(PreferredCameraMode))
	{
		UE_LOG(
			LogPMPlayerController,
			Warning,
			TEXT("Could not persist the preferred camera mode."));
		return;
	}

	Settings->SaveSettings();
}
