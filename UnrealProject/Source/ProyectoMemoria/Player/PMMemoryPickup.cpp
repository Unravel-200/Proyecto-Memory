#include "PMMemoryPickup.h"

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"

APMMemoryPickup::APMMemoryPickup()
	: bCollected(false)
{
	PrimaryActorTick.bCanEverTick = true;
	PickupMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PickupMesh"));
	RootComponent = PickupMesh;
	PickupMesh->SetCollisionProfileName(TEXT("BlockAll"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Mesh(
		TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (Mesh.Succeeded())
	{
		PickupMesh->SetStaticMesh(Mesh.Object);
		PickupMesh->SetRelativeScale3D(FVector(0.35f));
	}
}

void APMMemoryPickup::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	AddActorLocalRotation(FRotator(0.0f, 90.0f * DeltaSeconds, 0.0f));
}

void APMMemoryPickup::Interact_Implementation(APMPlayerCharacter* Player)
{
	if (bCollected)
	{
		return;
	}
	bCollected = true;
	UE_LOG(LogTemp, Log, TEXT("Memory pickup collected"));
	Destroy();
}
