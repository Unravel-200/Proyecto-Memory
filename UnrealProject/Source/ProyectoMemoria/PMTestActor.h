#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PMTestActor.generated.h"

// Prueba mínima de integración C++ <-> Blueprint (v0.0.1).
UCLASS()
class PROYECTOMEMORIA_API APMTestActor : public AActor
{
	GENERATED_BODY()

public:
	APMTestActor();

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Test")
	FString TestLabel;

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Test")
	void RunTestPing();

	UFUNCTION(BlueprintImplementableEvent, Category = "ProyectoMemoria|Test")
	void OnTestPing();
};
