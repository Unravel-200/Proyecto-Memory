#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "PMPlayerController.generated.h"

class APMPlayerCharacter;
class UInputAction;
class UInputMappingContext;
struct FInputActionValue;

/**
 * Traduce Enhanced Input a órdenes del personaje.
 *
 * Las reglas de movimiento pertenecen a APMPlayerCharacter y las reglas de
 * perspectiva pertenecen a UPMCameraModeComponent.
 */
UCLASS()
class PROYECTOMEMORIA_API APMPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	APMPlayerController();

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player")
	APMPlayerCharacter* GetPMPlayerCharacter() const;

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Input")
	void SetLookSensitivity(float HorizontalSensitivity, float VerticalSensitivity);

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Input")
	void SetInvertLookY(bool bShouldInvert);

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void SetupInputComponent() override;

	/** IMC_Player: contexto que agrupa todos los controles de esta versión. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputMappingContext> PlayerMappingContext;

	/** IA_Move debe usar Value Type Axis2D. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> MoveAction;

	/** IA_Look debe usar Value Type Axis2D. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> LookAction;

	/** IA_Sprint debe ser una acción Digital que se mantiene presionada. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> SprintAction;

	/** IA_Crouch debe ser una acción Digital de pulsación. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> CrouchAction;

	/** IA_ToggleCamera debe ser una acción Digital de pulsación. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> ToggleCameraAction;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input",
		meta = (ClampMin = "0.0", UIMin = "0.0"))
	float LookSensitivityX;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input",
		meta = (ClampMin = "0.0", UIMin = "0.0"))
	float LookSensitivityY;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	bool bInvertLookY;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	int32 MappingPriority;

private:
	void HandleMove(const FInputActionValue& Value);
	void HandleLook(const FInputActionValue& Value);
	void HandleSprintStarted();
	void HandleSprintCompleted();
	void HandleCrouch();
	void HandleToggleCamera();

	/** Evita retirar del subsistema un contexto que este controller no agregó. */
	bool bMappingContextAdded;
};
