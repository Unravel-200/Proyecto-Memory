import unreal

path = 'C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/fix_natural_landscape_visuals.py'
code = open(path, 'r', encoding='utf-8').read()
exec(compile(code, path, 'exec'), {})
unreal.log('NATURAL_LIGHTING_APPLIED')
