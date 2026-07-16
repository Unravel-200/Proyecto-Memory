#include "PMGameUserSettings.h"

void UPMGameUserSettings::SetToDefaults()
{
	Super::SetToDefaults();
	PreferredCameraMode = EPMCameraMode::FirstPerson;
}

void UPMGameUserSettings::ValidateSettings()
{
	Super::ValidateSettings();

	if (!IsSupportedCameraMode(PreferredCameraMode))
	{
		PreferredCameraMode = EPMCameraMode::FirstPerson;
	}
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
