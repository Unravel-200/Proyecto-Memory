#include "PMGameUserSettings.h"

void UPMGameUserSettings::SetToDefaults()
{
	Super::SetToDefaults();
	PreferredCameraMode = EPMCameraMode::FirstPerson;
	LookSensitivityX = 1.0f;
	LookSensitivityY = 1.0f;
	bInvertLookY = false;
}

void UPMGameUserSettings::ValidateSettings()
{
	Super::ValidateSettings();

	if (!IsSupportedCameraMode(PreferredCameraMode))
	{
		PreferredCameraMode = EPMCameraMode::FirstPerson;
	}
	LookSensitivityX = FMath::Clamp(LookSensitivityX, 0.0f, 2.0f);
	LookSensitivityY = FMath::Clamp(LookSensitivityY, 0.0f, 2.0f);
}

void UPMGameUserSettings::SetLookSettings(const float NewSensitivityX, const float NewSensitivityY, const bool bNewInvertLookY)
{
	LookSensitivityX = FMath::Clamp(NewSensitivityX, 0.0f, 2.0f);
	LookSensitivityY = FMath::Clamp(NewSensitivityY, 0.0f, 2.0f);
	bInvertLookY = bNewInvertLookY;
}

UPMGameUserSettings* UPMGameUserSettings::GetPMGameUserSettings()
{
	return Cast<UPMGameUserSettings>(UGameUserSettings::GetGameUserSettings());
}

EPMCameraMode UPMGameUserSettings::GetPreferredCameraMode() const
{
	return IsSupportedCameraMode(PreferredCameraMode)
		? PreferredCameraMode
		: EPMCameraMode::FirstPerson;
}

bool UPMGameUserSettings::SetPreferredCameraMode(const EPMCameraMode NewMode)
{
	if (!IsSupportedCameraMode(NewMode))
	{
		return false;
	}

	PreferredCameraMode = NewMode;
	return true;
}

bool UPMGameUserSettings::IsSupportedCameraMode(const EPMCameraMode CameraMode)
{
	return CameraMode == EPMCameraMode::FirstPerson
		|| CameraMode == EPMCameraMode::ThirdPerson;
}
