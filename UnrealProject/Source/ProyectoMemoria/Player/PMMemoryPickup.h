#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PMInteractableInterface.h"
#include "PMMemoryPickup.generated.h"

class UStaticMeshComponent;
class UPointLightComponent;

UCLASS()
class PROYECTOMEMORIA_API APMMemoryPickup : public AActor, public IPMInteractableInterface
{
	GENERATED_BODY()

public:
	APMMemoryPickup();
	virtual void Tick(float DeltaSeconds) override;
	virtual void Interact_Implementation(class APMPlayerCharacter* Player) override;

private:
	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UStaticMeshComponent> PickupMesh;
	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UPointLightComponent> PickupLight;
	bool bCollected;
};
