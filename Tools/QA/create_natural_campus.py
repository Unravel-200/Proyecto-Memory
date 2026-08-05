import unreal
MAP = '/Game/Maps/L_Campus_Natural'
TEMPLATE = '/Engine/Maps/Templates/OpenWorld'
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not levels.new_level_from_template(MAP, TEMPLATE):
    raise RuntimeError('No se pudo crear el nivel natural desde la plantilla OpenWorld')
levels.load_level(MAP)
levels.save_current_level()
unreal.log('NATURAL_CAMPUS_CREATED ' + MAP)
