import unreal

MAP = '/Game/Maps/L_Campus_Landscape'
TEMPLATE = '/Engine/Maps/Templates/OpenWorld'
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not levels.new_level_from_template(MAP, TEMPLATE):
    raise RuntimeError('No se pudo crear el nivel Landscape desde OpenWorld')
levels.load_level(MAP)
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    unreal.log('LANDSCAPE_CAMPUS_ACTOR ' + actor.get_actor_label() + ' ' + actor.get_class().get_name())
levels.save_current_level()
unreal.log('LANDSCAPE_CAMPUS_CREATED ' + MAP)
