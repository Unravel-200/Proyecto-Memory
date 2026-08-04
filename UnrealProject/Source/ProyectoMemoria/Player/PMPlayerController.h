#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "PMPlayerController.generated.h"

class APMPlayerCharacter;
class APMInteractableDoor;
class APMMemoryPickup;
class SOverlay;
class SWidget;
class UInputAction;
class UInputMappingContext;
enum class EPMCameraMode : uint8;
struct FInputActionInstance;
struct FInputActionValue;
struct FInputKeyEventArgs;

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

	void OpenMainMenu();
	void OpenPauseMenu();
	void CloseMenuAndResume();
	void ResetLookSettings();
	float GetLookSensitivityX() const { return LookSensitivityX; }
	float GetLookSensitivityY() const { return LookSensitivityY; }
	bool GetInvertLookY() const { return bInvertLookY; }

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player")
	APMPlayerCharacter* GetPMPlayerCharacter() const;

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Input")
	void SetLookSensitivity(float HorizontalSensitivity, float VerticalSensitivity);

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Input")
	void SetInvertLookY(bool bShouldInvert);

	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Gameplay")
	void RegisterMemoryPickupCollected();

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void OnUnPossess() override;
	virtual void SetPawn(APawn* InPawn) override;
	virtual void SetupInputComponent() override;
	virtual bool InputKey(const FInputKeyEventArgs& Params) override;

	UFUNCTION()
	void HandleEscape();

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

	/**
	 * IA_Crouch debe ser Digital con trigger predeterminado o Down. No debe usar
	 * Hold, Tap, Pressed, Released ni Pulse: C++ mide la duración completa.
	 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> CrouchAction;

	/** Duración mínima para interpretar IA_Crouch como mantener presionado. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input",
		meta = (ClampMin = "0.05", UIMin = "0.05", UIMax = "1.0", Units = "s"))
	float CrouchHoldThreshold;

	/** IA_Jump debe ser una acción Digital de pulsación. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Input")
	TObjectPtr<UInputAction> JumpAction;

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
	void HandleCrouchStarted();
	void HandleCrouchCompleted(const FInputActionInstance& Instance);
	void HandleCrouchCanceled();
	void HandleJumpStarted();
	void HandleJumpCompleted();
	void HandleToggleCamera();
	void HandleInteract();
	void ResetCrouchInputState();
	void ResetTransientPawnInputState();
	bool EnsureCameraPreferenceLoaded();
	void ApplyPreferredCameraModeToPawn();
	bool SetPlayerCameraMode(EPMCameraMode NewMode);
	void PersistPreferredCameraMode();

	/** Personaje que recibió el inicio de la pulsación, aunque cambie la posesión. */
	TWeakObjectPtr<APMPlayerCharacter> CrouchInputCharacter;

	/** Personaje que recibió Jump Started; Completed no afectará un Pawn nuevo. */
	TWeakObjectPtr<APMPlayerCharacter> JumpInputCharacter;

	/** Permite ignorar eventos Completed/Canceled sin un Started correspondiente. */
	bool bCrouchInputActive;

	/** Postura que se restaurará si Enhanced Input cancela la acción. */
	bool bWasCrouchedWhenInputStarted;

	/** Evita retirar del subsistema un contexto que este controller no agregó. */
	bool bMappingContextAdded;

	/** Preferencia de sesión; sobrevive al reemplazo del Pawn durante un respawn. */
	EPMCameraMode PreferredCameraMode;

	bool bCameraPreferenceLoaded;

	TSharedPtr<SOverlay> SlateMenu;
	TSharedPtr<SWidget> SlateMenuPanel;
	bool bMenuOpen;
	bool bMainMenuOpen;
	bool bSettingsOpen;
	bool bControllerTab;
	int32 MemoryFragmentsCollected;

	UPROPERTY()
	TObjectPtr<APMInteractableDoor> TestInteractableDoor;

	UPROPERTY()
	TObjectPtr<APMMemoryPickup> TestMemoryPickup;

	void RebuildSlateMenu();
	void EnsureTestInteractableDoor();
	void EnsureTestMemoryPickup();
	void RunAutomatedGameplaySmokeTest();
	bool bAutomatedGameplaySmokeScheduled;
};
