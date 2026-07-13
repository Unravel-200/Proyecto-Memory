#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PMCameraModeComponent.generated.h"

class UCameraComponent;
class USpringArmComponent;

/** Perspectivas jugables disponibles en v0.1.0. */
UENUM(BlueprintType)
enum class EPMCameraMode : uint8
{
	FirstPerson UMETA(DisplayName = "First Person"),
	ThirdPerson UMETA(DisplayName = "Third Person")
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(
	FPMCameraModeChangedSignature,
	EPMCameraMode,
	PreviousMode,
	EPMCameraMode,
	NewMode);

/**
 * Controla la perspectiva del jugador sin recibir input directamente.
 *
 * APMPlayerCharacter posee las cámaras. APMPlayerController solicita los
 * cambios y este componente aplica activación, FOV y política de rotación.
 */
UCLASS(ClassGroup = (ProyectoMemoria))
class PROYECTOMEMORIA_API UPMCameraModeComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UPMCameraModeComponent();

	/**
	 * Registra las cámaras creadas por el mismo APMPlayerCharacter propietario.
	 * Debe llamarse durante la construcción, antes de BeginPlay.
	 */
	void ConfigureCameras(
		UCameraComponent* InFirstPersonCamera,
		UCameraComponent* InThirdPersonCamera,
		USpringArmComponent* InThirdPersonCameraBoom);

	/**
	 * Cambia la perspectiva.
	 * @return true si las referencias eran válidas y el modo se aplicó.
	 */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Camera")
	bool SetCameraMode(EPMCameraMode NewMode);

	/**
	 * Alterna el modo y devuelve el modo resultante. Si falta configuración,
	 * conserva y devuelve el modo actual.
	 */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Camera")
	EPMCameraMode ToggleCameraMode();

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	EPMCameraMode GetCameraMode() const;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	bool IsFirstPerson() const;

	/** Devuelve la cámara activa o nullptr si la configuración está incompleta. */
	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	UCameraComponent* GetActiveCamera() const;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	bool HasValidCameraSetup() const;

	/** Permite que Blueprint reaccione visualmente sin controlar el estado. */
	UPROPERTY(BlueprintAssignable, Category = "ProyectoMemoria|Player|Camera")
	FPMCameraModeChangedSignature OnCameraModeChanged;

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera")
	EPMCameraMode InitialMode;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera",
		meta = (ClampMin = "5.0", ClampMax = "170.0", UIMin = "60.0", UIMax = "120.0"))
	float FirstPersonFieldOfView;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera",
		meta = (ClampMin = "5.0", ClampMax = "170.0", UIMin = "60.0", UIMax = "120.0"))
	float ThirdPersonFieldOfView;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera",
		meta = (ClampMin = "0.0", UIMin = "0.0", Units = "cm"))
	float ThirdPersonArmLength;

private:
	void ApplyCameraMode();
	void ApplyOwnerRotationPolicy() const;

	/** Referencias no serializadas; las cámaras son propiedad del Character. */
	UPROPERTY(Transient)
	TObjectPtr<UCameraComponent> FirstPersonCamera;

	UPROPERTY(Transient)
	TObjectPtr<UCameraComponent> ThirdPersonCamera;

	UPROPERTY(Transient)
	TObjectPtr<USpringArmComponent> ThirdPersonCameraBoom;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera",
		meta = (AllowPrivateAccess = "true"))
	EPMCameraMode CurrentMode;
};
