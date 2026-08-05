import unreal
def run(path):
    code = open(path, 'r', encoding='utf-8').read()
    exec(compile(code, path, 'exec'), {})
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/place_natural_layout_markers.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/complete_natural_campus_pass.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/align_natural_buildings_to_ground.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/apply_natural_lighting_loaded.py')
run('C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/validate_natural_campus_loaded.py')
unreal.log('NATURAL_CAMPUS_FINAL_STARTUP_DONE')
