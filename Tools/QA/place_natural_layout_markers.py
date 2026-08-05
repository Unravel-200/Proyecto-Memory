import unreal
path = 'C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/Tools/QA/place_full_campus_graybox.py'
code = open(path, 'r', encoding='utf-8').read().replace("'/Game/Maps/L_Campus_Blockout'", "'/Game/Maps/L_Campus_Natural'")
code = code.replace('unreal.EditorLevelLibrary.load_level(MAP)\n', '')
exec(compile(code, path, 'exec'), {})
CUBE = unreal.load_object(None, '/Engine/BasicShapes/Cube.Cube')
def marker(label, loc, dims):
    a = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc), unreal.Rotator(0,0,0))
    a.set_actor_label(label); a.static_mesh_component.set_static_mesh(CUBE); a.set_actor_scale3d(unreal.Vector(dims[0]/100.0, dims[1]/100.0, dims[2]/100.0)); a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
for y in (-30000.0, 0.0, 30000.0):
    marker('BridgeMarker_%d' % int(y), (0.0, y, 250.0), (1200.0, 350.0, 80.0))
for y in (-30000.0, 0.0, 30000.0):
    marker('RavineBuffer_%d' % int(y), (0.0, y, 80.0), (2000.0, 1800.0, 20.0))
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_LAYOUT_MARKERS_READY')
