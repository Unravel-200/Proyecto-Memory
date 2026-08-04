#include "PMMemoryPickup.h"

#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"
#include "PMPlayerController.h"
#include "PMPlayerCharacter.h"
#include "GameFramework/PlayerController.h"

APMMemoryPickup::APMMemoryPickup()
	: bCollected(false)
	, BobTime(0.0f)
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
	PickupLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("PickupLight"));
	PickupLight->SetupAttachment(RootComponent);
	PickupLight->SetIntensity(1800.0f);
	PickupLight->SetAttenuationRadius(500.0f);
	PickupLight->SetLightColor(FLinearColor(0.2f, 0.65f, 1.0f));
	PickupLight->SetCastShadows(false);
}

void APMMemoryPickup::BeginPlay()
{
	Super::BeginPlay();
	BaseLocation = GetActorLocation();
}

void APMMemoryPickup::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	BobTime += DeltaSeconds;
	SetActorLocation(BaseLocation + FVector(0.0f, 0.0f, FMath::Sin(BobTime * 2.0f) * 8.0f));
	if (PickupLight)
	{
		PickupLight->SetIntensity(1800.0f + FMath::Sin(BobTime * 3.0f) * 450.0f);
	}
	AddActorLocalRotation(FRotator(0.0f, 90.0f * DeltaSeconds, 0.0f));
}

void APMMemoryPickup::Interact_Implementation(APMPlayerCharacter* Player)
{
	if (bCollected)
	{
		return;
	}
	bCollected = true;
	if (Player)
	{
		if (APMPlayerController* Controller = Cast<APMPlayerController>(Player->GetController()))
		{
			Controller->RegisterMemoryPickupCollected();
		}
	}
	UE_LOG(LogTemp, Log, TEXT("Memory pickup collected"));
	Destroy();
}
