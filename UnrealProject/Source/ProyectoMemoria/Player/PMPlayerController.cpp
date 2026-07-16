#include "PMPlayerController.h"

#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "InputAction.h"
#include "InputActionValue.h"
#include "PMCameraModeComponent.h"
#include "PMGameUserSettings.h"
#include "PMPlayerCharacter.h"

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
}

void APMPlayerController::BeginPlay()
{
	Super::BeginPlay();

	ApplyPreferredCameraModeToPawn();

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
}

void APMPlayerController::SetInvertLookY(const bool bShouldInvert)
{
	bInvertLookY = bShouldInvert;
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
	const float VerticalDirection = bInvertLookY ? -1.0f : 1.0f;

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
