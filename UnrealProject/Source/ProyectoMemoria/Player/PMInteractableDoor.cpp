#include "PMInteractableDoor.h"

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"

APMInteractableDoor::APMInteractableDoor()
	: OpenAngle(90.0f)
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
		DoorMesh->SetRelativeScale3D(FVector(0.12f, 1.0f, 2.0f));
		// El actor funciona como bisagra; el mesh queda desplazado a un borde.
		DoorMesh->SetRelativeLocation(FVector(0.0f, 50.0f, 0.0f));
	}
}

void APMInteractableDoor::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	CurrentAngle = FMath::FInterpTo(CurrentAngle, TargetAngle, DeltaSeconds, 6.0f);
	SetActorRotation(FRotator(0.0f, CurrentAngle, 0.0f));
}

void APMInteractableDoor::Interact_Implementation(APMPlayerCharacter* Player)
{
	bIsOpen = !bIsOpen;
	TargetAngle = bIsOpen ? OpenAngle : 0.0f;
}
