import unreal

ROOT = 'C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/'
def run(name):
    path = ROOT + name
    code = open(path, 'r', encoding='utf-8').read()
    exec(compile(code, path, 'exec'), {})

# Recreate the map from Unreal's OpenWorld template. This removes all prior
# buildings, fallback meshes, markers and level-only actors from the map.
run('create_natural_campus.py')
run('apply_natural_height_loaded.py')
run('setup_campus_landscape_material.py')
unreal.log('NATURAL_LANDSCAPE_RESET_FROM_SCRATCH')
