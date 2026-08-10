import unreal
ROOT = 'C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/'
def run(name):
    path = ROOT + name; code = open(path, 'r', encoding='utf-8').read(); exec(compile(code, path, 'exec'), {})
run('wipe_natural_map_loaded.py')
run('apply_natural_height_loaded.py')
run('setup_campus_landscape_material.py')
unreal.log('NATURAL_LANDSCAPE_REBUILT_FROM_NATIVE')
