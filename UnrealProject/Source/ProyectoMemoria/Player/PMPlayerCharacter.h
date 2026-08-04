#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PMPlayerCharacter.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UPMCameraModeComponent;
class UAnimSequence;
class UAnimInstance;

/**
 * Base C++ del jugador de Proyecto Memoria.
 *
 * El personaje posee los componentes físicos y de cámara. El controller
 * traduce el input y UPMCameraModeComponent decide qué cámara está activa.
 */
UCLASS()
class PROYECTOMEMORIA_API APMPlayerCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	APMPlayerCharacter();

	/** Activa o desactiva la velocidad de carrera. */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Movement")
	void SetSprinting(bool bEnabled);

	/** Solicita explícitamente agacharse o volver a estar de pie. */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Movement")
	void SetCrouching(bool bEnabled);

	/** Alterna entre estar de pie y agachado. */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Movement")
	void ToggleCrouch();

	/**
	 * Intenta levantarse inmediatamente si está agachado y salta solo si la
	 * cápsula de pie cabe. Nunca deja una orden de salto latente bajo un techo.
	 */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Player|Movement")
	bool TryJumpFromCurrentPosture();

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Movement")
	bool IsSprinting() const;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	UPMCameraModeComponent* GetCameraModeComponent() const;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	UCameraComponent* GetFirstPersonCamera() const;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Player|Camera")
	UCameraComponent* GetThirdPersonCamera() const;

protected:
	virtual void Tick(float DeltaSeconds) override;
	virtual void BeginPlay() override;
	virtual void OnStartCrouch(float HalfHeightAdjust, float ScaledHalfHeightAdjust) override;
	virtual void OnEndCrouch(float HalfHeightAdjust, float ScaledHalfHeightAdjust) override;

	/** Cámara colocada a la altura de los ojos. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera")
	TObjectPtr<UCameraComponent> FirstPersonCamera;

	/** Brazo con prueba de colisión para la cámara en tercera persona. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera")
	TObjectPtr<USpringArmComponent> ThirdPersonCameraBoom;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera")
	TObjectPtr<UCameraComponent> ThirdPersonCamera;

	/** Encapsula el cambio 1P/3P y la orientación correspondiente. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Camera")
	TObjectPtr<UPMCameraModeComponent> CameraModeComponent;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Movement",
		meta = (ClampMin = "0.0", UIMin = "0.0", Units = "cm/s"))
	float WalkSpeed;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Movement",
		meta = (ClampMin = "0.0", UIMin = "0.0", Units = "cm/s"))
	float SprintSpeed;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Movement",
		meta = (ClampMin = "0.0", UIMin = "0.0", Units = "cm/s"))
	float CrouchSpeed;

	/** Animaciones importadas para la pose de crouch de esta primera versiÃ³n. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Animation")
	TObjectPtr<UAnimSequence> CrouchIdleAnimation;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Animation")
	TObjectPtr<UAnimSequence> CrouchWalkAnimation;

private:
	void ApplyMovementSpeed();

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "ProyectoMemoria|Player|Movement",
		meta = (AllowPrivateAccess = "true"))
	bool bIsSprinting;
	bool bCrouchAnimationActive;
	bool bCrouchAnimationWalking;
	TSubclassOf<UAnimInstance> DefaultAnimInstanceClass;
};
