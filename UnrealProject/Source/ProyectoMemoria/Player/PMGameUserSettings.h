#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameUserSettings.h"
#include "PMCameraModeComponent.h"
#include "PMGameUserSettings.generated.h"

/**
 * Preferencias persistentes del jugador que pertenecen a esta instalación.
 *
 * Los bindings personalizables se incorporarán en la etapa de menús. Esta clase
 * empieza por conservar la perspectiva entre respawns y ejecuciones.
 */
UCLASS(Config=GameUserSettings, ConfigDoNotCheckDefaults)
class PROYECTOMEMORIA_API UPMGameUserSettings : public UGameUserSettings
{
	GENERATED_BODY()

public:
	virtual void SetToDefaults() override;
	virtual void ValidateSettings() override;

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings")
	static UPMGameUserSettings* GetPMGameUserSettings();

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings|Camera")
	EPMCameraMode GetPreferredCameraMode() const;

	/** Cambia el valor en memoria. SaveSettings confirma la escritura a disco. */
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Settings|Camera")
	bool SetPreferredCameraMode(EPMCameraMode NewMode);

	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings|Look")
	float GetLookSensitivityX() const { return LookSensitivityX; }
	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings|Look")
	float GetLookSensitivityY() const { return LookSensitivityY; }
	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings|Look")
	bool GetInvertLookY() const { return bInvertLookY; }
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Settings|Look")
	void SetLookSettings(float NewSensitivityX, float NewSensitivityY, bool bNewInvertLookY);
	UFUNCTION(BlueprintPure, Category = "ProyectoMemoria|Settings|Display")
	float GetBrightness() const { return Brightness; }
	UFUNCTION(BlueprintCallable, Category = "ProyectoMemoria|Settings|Display")
	void SetBrightness(float NewBrightness);

private:
	static bool IsSupportedCameraMode(EPMCameraMode CameraMode);

	UPROPERTY(Config)
	EPMCameraMode PreferredCameraMode = EPMCameraMode::FirstPerson;

	UPROPERTY(Config)
	float LookSensitivityX = 1.0f;
	UPROPERTY(Config)
	float LookSensitivityY = 1.0f;
	UPROPERTY(Config)
	bool bInvertLookY = false;

	UPROPERTY(Config)
	float Brightness = 1.0f;
};
