#include "PMPlayerCharacter.h"

#include "Camera/CameraComponent.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimSequence.h"
#include "Components/CapsuleComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "PMCameraModeComponent.h"
#include "PMPlayerController.h"

APMPlayerCharacter::APMPlayerCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	WalkSpeed = 300.0f;
	SprintSpeed = 550.0f;
	CrouchSpeed = 180.0f;
	bIsSprinting = false;
	bCrouchAnimationActive = false;
	bCrouchAnimationWalking = false;
	StandingMeshRelativeLocation = FVector::ZeroVector;
	bHasStandingMeshRelativeLocation = false;
	bDeathHandled = false;

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
		DefaultAnimInstanceClass = DefaultAnimBP.Class;
		GetMesh()->SetAnimInstanceClass(DefaultAnimBP.Class);
	}
	static ConstructorHelpers::FObjectFinder<UAnimSequence> CrouchIdle(
		TEXT("/Game/Mannequin/Animations/Crouch/Crouching_Idle.Crouching_Idle"));
	if (CrouchIdle.Succeeded())
	{
		CrouchIdleAnimation = CrouchIdle.Object;
	}
	static ConstructorHelpers::FObjectFinder<UAnimSequence> CrouchWalk(
		TEXT("/Game/Mannequin/Animations/Crouch/Crouched_Walking.Crouched_Walking"));
	if (CrouchWalk.Succeeded())
	{
		CrouchWalkAnimation = CrouchWalk.Object;
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
	// El mapa natural usa World Partition y algunos GameModes pueden reutilizar
	// un punto de spawn antiguo. Garantiza que el jugador comience sobre el
	// Landscape, dejando que la gravedad lo coloque sobre el terreno.
	if (GetWorld() && GetWorld()->GetMapName().Contains(TEXT("L_Campus_Natural"))
		&& GetActorLocation().Z < 5000.0f)
	{
		FVector SafeLocation = GetActorLocation();
		SafeLocation.Z = 10000.0f;
		SetActorLocation(SafeLocation, false, nullptr, ETeleportType::TeleportPhysics);
		UE_LOG(LogTemp, Log, TEXT("Natural campus spawn corrected to Z=%.1f"), SafeLocation.Z);
	}
	ApplyMovementSpeed();
}

void APMPlayerCharacter::Tick(const float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (!bDeathHandled && GetActorLocation().Z < -300.0f)
	{
		bDeathHandled = true;
		UE_LOG(LogTemp, Log, TEXT("Player fell below kill threshold at Z=%.1f"), GetActorLocation().Z);
		if (APMPlayerController* PMController = Cast<APMPlayerController>(GetController()))
		{
			PMController->HandlePlayerDeath();
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("Player death had no APMPlayerController"));
		}
		return;
	}
	if (!bCrouchAnimationActive || !GetMesh())
	{
		return;
	}

	const bool bShouldWalk = GetVelocity().SizeSquared2D() > FMath::Square(5.0f);
	if (bShouldWalk != bCrouchAnimationWalking)
	{
		bCrouchAnimationWalking = bShouldWalk;
		if (UAnimSequence* Pose = bShouldWalk ? CrouchWalkAnimation.Get() : CrouchIdleAnimation.Get())
		{
			GetMesh()->PlayAnimation(Pose, true);
		}
	}
}

void APMPlayerCharacter::OnStartCrouch(
	const float HalfHeightAdjust,
	const float ScaledHalfHeightAdjust)
{
	Super::OnStartCrouch(HalfHeightAdjust, ScaledHalfHeightAdjust);

	// También cubre llamadas a Crouch hechas por un Blueprint o sistema futuro.
	bIsSprinting = false;
	// La cápsula conserva su base al agacharse. El mannequin debe subir la
	// misma cantidad para que sus pies sigan apoyados sobre el suelo.
	if (GetMesh())
	{
		if (!bHasStandingMeshRelativeLocation)
		{
			StandingMeshRelativeLocation = GetMesh()->GetRelativeLocation();
			bHasStandingMeshRelativeLocation = true;
		}
		GetMesh()->SetRelativeLocation(
			StandingMeshRelativeLocation + FVector(0.0f, 0.0f, FMath::Abs(ScaledHalfHeightAdjust)));
		bCrouchAnimationActive = true;
		bCrouchAnimationWalking = false;
		if (CrouchIdleAnimation)
		{
			GetMesh()->PlayAnimation(CrouchIdleAnimation, true);
		}
	}
	ApplyMovementSpeed();
}

void APMPlayerCharacter::OnEndCrouch(
	const float HalfHeightAdjust,
	const float ScaledHalfHeightAdjust)
{
	Super::OnEndCrouch(HalfHeightAdjust, ScaledHalfHeightAdjust);
	if (GetMesh())
	{
		if (bHasStandingMeshRelativeLocation)
		{
			GetMesh()->SetRelativeLocation(StandingMeshRelativeLocation);
		}
		bCrouchAnimationActive = false;
		bCrouchAnimationWalking = false;
		if (DefaultAnimInstanceClass)
		{
			GetMesh()->SetAnimInstanceClass(DefaultAnimInstanceClass);
			GetMesh()->InitAnim(true);
		}
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
