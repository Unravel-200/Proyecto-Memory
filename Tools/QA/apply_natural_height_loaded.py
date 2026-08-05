import unreal
path = 'C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/sculpt_landscape_campus.py'
code = open(path, 'r', encoding='utf-8').read().replace("'/Game/Maps/L_Campus_Landscape'", "'/Game/Maps/L_Campus_Natural'")
code = code.replace("levels.load_level(MAP)\n", '')
exec(compile(code, path, 'exec'), {})
