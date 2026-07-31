#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "PMInteractableInterface.generated.h"

class APMPlayerCharacter;

UINTERFACE(BlueprintType)
class PROYECTOMEMORIA_API UPMInteractableInterface : public UInterface
{
	GENERATED_BODY()
};

class PROYECTOMEMORIA_API IPMInteractableInterface
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "ProyectoMemoria|Interaction")
	void Interact(APMPlayerCharacter* Player);
};
