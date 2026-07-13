#include "PMPlayerController.h"

#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "InputActionValue.h"
#include "PMCameraModeComponent.h"
#include "PMPlayerCharacter.h"

DEFINE_LOG_CATEGORY_STATIC(LogPMPlayerController, Log, All);

APMPlayerController::APMPlayerController()
{
	LookSensitivityX = 1.0f;
	LookSensitivityY = 1.0f;
	bInvertLookY = false;
	MappingPriority = 0;
	bMappingContextAdded = false;
}

void APMPlayerController::BeginPlay()
{
	Super::BeginPlay();

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

	if (!MoveAction || !LookAction || !SprintAction || !CrouchAction || !ToggleCameraAction)
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
			&APMPlayerController::HandleCrouch);
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

void APMPlayerController::HandleCrouch()
{
	if (APMPlayerCharacter* PMCharacter = GetPMPlayerCharacter())
	{
		PMCharacter->ToggleCrouch();
	}
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
		CameraMode->ToggleCameraMode();
	}
}
