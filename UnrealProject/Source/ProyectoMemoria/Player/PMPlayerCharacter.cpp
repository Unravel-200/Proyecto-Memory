#include "PMPlayerCharacter.h"

#include "Camera/CameraComponent.h"
#include "Animation/AnimInstance.h"
#include "Components/CapsuleComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "PMCameraModeComponent.h"

APMPlayerCharacter::APMPlayerCharacter()
{
	PrimaryActorTick.bCanEverTick = false;

	WalkSpeed = 300.0f;
	SprintSpeed = 550.0f;
	CrouchSpeed = 180.0f;
	bIsSprinting = false;

	GetCapsuleComponent()->InitCapsuleSize(42.0f, 96.0f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = true;
	bUseControllerRotationRoll = false;

	UCharacterMovementComponent* Movement = GetCharacterMovement();
	Movement->MaxWalkSpeed = WalkSpeed;
	Movement->MaxWalkSpeedCrouched = CrouchSpeed;
	Movement->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	Movement->bOrientRotationToMovement = false;
	Movement->GetNavAgentPropertiesRef().bCanCrouch = true;

	// Mannequin provisional incluido desde los recursos estándar de UE 5.8.
	// Se mantiene como fallback C++ para que el BP pueda cambiarlo más adelante.
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> DefaultMesh(
		TEXT("/Game/Mannequin/Character/Mesh/SK_Mannequin.SK_Mannequin"));
	if (DefaultMesh.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(DefaultMesh.Object);
		GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -96.0f));
		GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> DefaultAnimBP(
		TEXT("/Game/Mannequin/Animations/ThirdPerson_AnimBP"));
	if (DefaultAnimBP.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(DefaultAnimBP.Class);
	}

	FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
	FirstPersonCamera->SetupAttachment(GetCapsuleComponent());
	FirstPersonCamera->SetRelativeLocation(FVector(-10.0f, 0.0f, 64.0f));
	FirstPersonCamera->bUsePawnControlRotation = true;

	ThirdPersonCameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("ThirdPersonCameraBoom"));
	ThirdPersonCameraBoom->SetupAttachment(GetCapsuleComponent());
	ThirdPersonCameraBoom->TargetArmLength = 300.0f;
	ThirdPersonCameraBoom->bUsePawnControlRotation = true;
	ThirdPersonCameraBoom->bDoCollisionTest = true;
	ThirdPersonCameraBoom->bEnableCameraLag = false;
	ThirdPersonCameraBoom->bEnableCameraRotationLag = false;
	ThirdPersonCameraBoom->ProbeSize = 12.0f;
	ThirdPersonCameraBoom->ProbeChannel = ECC_Camera;

	ThirdPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("ThirdPersonCamera"));
	ThirdPersonCamera->SetupAttachment(ThirdPersonCameraBoom, USpringArmComponent::SocketName);
	ThirdPersonCamera->bUsePawnControlRotation = false;

	CameraModeComponent = CreateDefaultSubobject<UPMCameraModeComponent>(TEXT("CameraModeComponent"));
	CameraModeComponent->ConfigureCameras(
		FirstPersonCamera,
		ThirdPersonCamera,
		ThirdPersonCameraBoom);
}

void APMPlayerCharacter::BeginPlay()
{
	Super::BeginPlay();
	ApplyMovementSpeed();
}

void APMPlayerCharacter::OnStartCrouch(
	const float HalfHeightAdjust,
	const float ScaledHalfHeightAdjust)
{
	Super::OnStartCrouch(HalfHeightAdjust, ScaledHalfHeightAdjust);

	// También cubre llamadas a Crouch hechas por un Blueprint o sistema futuro.
	bIsSprinting = false;
	if (USkeletalMeshComponent* CharacterMesh = GetMesh())
	{
		// El AnimBP provisional no trae una pose de crouch; compactamos la malla
		// y la bajamos con la cápsula para mantener pies y cámara alineados.
		CharacterMesh->SetRelativeScale3D(FVector(1.0f, 1.0f, 0.85f));
		// El root del mannequin está en los pies; conservar la misma altura evita
		// que la escala visual atraviese el suelo.
		CharacterMesh->SetRelativeLocation(FVector(0.0f, 0.0f, -96.0f));
	}
	ApplyMovementSpeed();
}

void APMPlayerCharacter::OnEndCrouch(
	const float HalfHeightAdjust,
	const float ScaledHalfHeightAdjust)
{
	Super::OnEndCrouch(HalfHeightAdjust, ScaledHalfHeightAdjust);
	if (USkeletalMeshComponent* CharacterMesh = GetMesh())
	{
		CharacterMesh->SetRelativeScale3D(FVector::OneVector);
		CharacterMesh->SetRelativeLocation(FVector(0.0f, 0.0f, -96.0f));
	}
	ApplyMovementSpeed();
}

void APMPlayerCharacter::SetSprinting(const bool bEnabled)
{
	bIsSprinting = bEnabled && !bIsCrouched;
	ApplyMovementSpeed();
}

void APMPlayerCharacter::SetCrouching(const bool bEnabled)
{
	if (bEnabled)
	{
		SetSprinting(false);
		Crouch();
		return;
	}

	UnCrouch();
}

void APMPlayerCharacter::ToggleCrouch()
{
	SetCrouching(!IsCrouched());
}

bool APMPlayerCharacter::TryJumpFromCurrentPosture()
{
	StopJumping();

	if (IsCrouched())
	{
		SetCrouching(false);

		// ACharacter::UnCrouch solo cambia la intención. Ejecutar la operación
		// pública del Movement permite saber en esta misma pulsación si hay
		// espacio real para recuperar la cápsula de pie.
		if (UCharacterMovementComponent* Movement = GetCharacterMovement())
		{
			Movement->UnCrouch(false);
		}
	}

	if (IsCrouched() || !CanJump())
	{
		StopJumping();
		return false;
	}

	Jump();
	return true;
}

bool APMPlayerCharacter::IsSprinting() const
{
	return bIsSprinting;
}

UPMCameraModeComponent* APMPlayerCharacter::GetCameraModeComponent() const
{
	return CameraModeComponent;
}

UCameraComponent* APMPlayerCharacter::GetFirstPersonCamera() const
{
	return FirstPersonCamera;
}

UCameraComponent* APMPlayerCharacter::GetThirdPersonCamera() const
{
	return ThirdPersonCamera;
}

void APMPlayerCharacter::ApplyMovementSpeed()
{
	UCharacterMovementComponent* Movement = GetCharacterMovement();
	if (!Movement)
	{
		return;
	}

	Movement->MaxWalkSpeed = bIsSprinting && !bIsCrouched
		? SprintSpeed
		: WalkSpeed;
	Movement->MaxWalkSpeedCrouched = CrouchSpeed;
}
