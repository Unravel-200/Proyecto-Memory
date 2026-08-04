import unreal
MAP = '/Game/Maps/L_Campus_Landscape'
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP)
def run(path, strip=''):
    code = open(path, 'r', encoding='utf-8').read().replace("'/Game/Maps/L_Campus_Blockout'", "'/Game/Maps/L_Campus_Landscape'")
    if strip:
        code = code.replace(strip, '')
    exec(compile(code, path, 'exec'), {})
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/create_campus_blockout.py', 'unreal.EditorLevelLibrary.new_level(MAP)\n')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/shape_campus_relief.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/place_full_campus_graybox.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/add_campus_lighting.py')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('LANDSCAPE_CAMPUS_BUILT ' + MAP)
