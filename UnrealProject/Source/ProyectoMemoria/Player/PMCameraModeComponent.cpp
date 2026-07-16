#include "PMCameraModeComponent.h"

#include "Camera/CameraComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"

DEFINE_LOG_CATEGORY_STATIC(LogPMCameraMode, Log, All);

UPMCameraModeComponent::UPMCameraModeComponent()
{
	PrimaryComponentTick.bCanEverTick = false;

	InitialMode = EPMCameraMode::FirstPerson;
	CurrentMode = InitialMode;
	bHasRuntimeModeOverride = false;
	FirstPersonFieldOfView = 90.0f;
	ThirdPersonFieldOfView = 90.0f;
	ThirdPersonArmLength = 300.0f;
}

void UPMCameraModeComponent::BeginPlay()
{
	Super::BeginPlay();

	const EPMCameraMode ModeToApply = bHasRuntimeModeOverride
		? CurrentMode
		: InitialMode;
	if (!SetCameraMode(ModeToApply))
	{
		UE_LOG(
			LogPMCameraMode,
			Warning,
			TEXT("UPMCameraModeComponent on %s has an incomplete camera setup."),
			*GetNameSafe(GetOwner()));
	}
}

void UPMCameraModeComponent::ConfigureCameras(
	UCameraComponent* InFirstPersonCamera,
	UCameraComponent* InThirdPersonCamera,
	USpringArmComponent* InThirdPersonCameraBoom)
{
	FirstPersonCamera = InFirstPersonCamera;
	ThirdPersonCamera = InThirdPersonCamera;
	ThirdPersonCameraBoom = InThirdPersonCameraBoom;
}

bool UPMCameraModeComponent::SetCameraMode(const EPMCameraMode NewMode)
{
	const bool bIsSupportedMode = NewMode == EPMCameraMode::FirstPerson
		|| NewMode == EPMCameraMode::ThirdPerson;
	if (!bIsSupportedMode || !HasValidCameraSetup())
	{
		return false;
	}

	const EPMCameraMode PreviousMode = CurrentMode;
	CurrentMode = NewMode;
	bHasRuntimeModeOverride = true;
	ApplyCameraMode();

	if (PreviousMode != CurrentMode)
	{
		OnCameraModeChanged.Broadcast(PreviousMode, CurrentMode);
	}

	return true;
}

EPMCameraMode UPMCameraModeComponent::ToggleCameraMode()
{
	const EPMCameraMode NewMode = CurrentMode == EPMCameraMode::FirstPerson
		? EPMCameraMode::ThirdPerson
		: EPMCameraMode::FirstPerson;

	SetCameraMode(NewMode);
	return CurrentMode;
}

EPMCameraMode UPMCameraModeComponent::GetCameraMode() const
{
	return CurrentMode;
}

bool UPMCameraModeComponent::IsFirstPerson() const
{
	return CurrentMode == EPMCameraMode::FirstPerson;
}

UCameraComponent* UPMCameraModeComponent::GetActiveCamera() const
{
	if (!HasValidCameraSetup())
	{
		return nullptr;
	}

	return IsFirstPerson()
		? FirstPersonCamera.Get()
		: ThirdPersonCamera.Get();
}

bool UPMCameraModeComponent::HasValidCameraSetup() const
{
	const AActor* OwnerActor = GetOwner();

	return IsValid(OwnerActor)
		&& OwnerActor->IsA<ACharacter>()
		&& IsValid(FirstPersonCamera)
		&& IsValid(ThirdPersonCamera)
		&& IsValid(ThirdPersonCameraBoom)
		&& FirstPersonCamera->GetOwner() == OwnerActor
		&& ThirdPersonCamera->GetOwner() == OwnerActor
		&& ThirdPersonCameraBoom->GetOwner() == OwnerActor;
}

void UPMCameraModeComponent::ApplyCameraMode()
{
	// SetCameraMode valida las tres referencias antes de entrar aquí.
	const bool bUseFirstPerson = IsFirstPerson();

	FirstPersonCamera->SetFieldOfView(FirstPersonFieldOfView);
	FirstPersonCamera->SetActive(bUseFirstPerson);

	ThirdPersonCamera->SetFieldOfView(ThirdPersonFieldOfView);
	ThirdPersonCamera->SetActive(!bUseFirstPerson);

	ThirdPersonCameraBoom->TargetArmLength = ThirdPersonArmLength;
	ThirdPersonCameraBoom->bDoCollisionTest = !bUseFirstPerson;

	ApplyOwnerRotationPolicy();
}

void UPMCameraModeComponent::ApplyOwnerRotationPolicy() const
{
	ACharacter* CharacterOwner = Cast<ACharacter>(GetOwner());
	if (!CharacterOwner)
	{
		return;
	}

	const bool bUseFirstPerson = IsFirstPerson();
	CharacterOwner->bUseControllerRotationYaw = bUseFirstPerson;

	if (UCharacterMovementComponent* Movement = CharacterOwner->GetCharacterMovement())
	{
		Movement->bOrientRotationToMovement = !bUseFirstPerson;
	}
}
