#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PMInteractableInterface.h"
#include "PMInteractableDoor.generated.h"

class UStaticMeshComponent;

UCLASS()
class PROYECTOMEMORIA_API APMInteractableDoor : public AActor, public IPMInteractableInterface
{
	GENERATED_BODY()

public:
	APMInteractableDoor();

	virtual void Interact_Implementation(class APMPlayerCharacter* Player) override;

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Door")
	TObjectPtr<UStaticMeshComponent> DoorMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Door")
	float OpenAngle;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Door")
	bool bIsOpen;
};
