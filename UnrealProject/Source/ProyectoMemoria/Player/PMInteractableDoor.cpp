#include "PMInteractableDoor.h"

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"
#include "Logging/LogMacros.h"
#include "PMPlayerCharacter.h"

APMInteractableDoor::APMInteractableDoor()
	: OpenAngle(-90.0f)
	, bIsOpen(false)
	, CurrentAngle(0.0f)
	, TargetAngle(0.0f)
{
	PrimaryActorTick.bCanEverTick = true;
	DoorMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DoorMesh"));
	RootComponent = DoorMesh;
	DoorMesh->SetCollisionProfileName(TEXT("BlockAll"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> DefaultMesh(
		TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (DefaultMesh.Succeeded())
	{
		DoorMesh->SetStaticMesh(DefaultMesh.Object);
		DoorMesh->SetRelativeScale3D(FVector(0.08f, 0.65f, 1.6f));
		// El actor funciona como bisagra; el mesh queda desplazado a un borde.
		DoorMesh->SetRelativeLocation(FVector(0.0f, -32.5f, 0.0f));
	}
}

void APMInteractableDoor::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	CurrentAngle = FMath::FInterpTo(CurrentAngle, TargetAngle, DeltaSeconds, 6.0f);
	SetActorRotation(FRotator(0.0f, CurrentAngle, 0.0f));
	if (DoorMesh)
	{
		const bool bShouldBlock = FMath::Abs(CurrentAngle) < 65.0f;
		DoorMesh->SetCollisionEnabled(
			bShouldBlock ? ECollisionEnabled::QueryAndPhysics : ECollisionEnabled::NoCollision);
	}
}

void APMInteractableDoor::Interact_Implementation(APMPlayerCharacter* Player)
{
	if (bIsOpen && Player
		&& FVector::DistSquared(Player->GetActorLocation(), GetActorLocation()) < FMath::Square(120.0f))
	{
		UE_LOG(LogTemp, Log, TEXT("Door close blocked: player is still in the doorway"));
		return;
	}
	bIsOpen = !bIsOpen;
	if (bIsOpen)
	{
		const FVector ToPlayer = Player
			? (Player->GetActorLocation() - GetActorLocation()).GetSafeNormal()
			: GetActorForwardVector();
		const float Side = FVector::DotProduct(ToPlayer, GetActorRightVector());
		TargetAngle = (Side >= 0.0f ? -1.0f : 1.0f) * FMath::Abs(OpenAngle);
	}
	else
	{
		TargetAngle = 0.0f;
	}
	if (DoorMesh)
	{
		DoorMesh->SetCollisionEnabled(
			bIsOpen ? ECollisionEnabled::QueryOnly : ECollisionEnabled::QueryAndPhysics);
	}
	UE_LOG(LogTemp, Log, TEXT("Interactable door toggled: %s"), bIsOpen ? TEXT("Open") : TEXT("Closed"));
}
