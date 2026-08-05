import unreal
cube = unreal.load_object(None, '/Engine/BasicShapes/Cube.Cube')
def marker(label, loc, dims, color=None):
    for old in unreal.EditorLevelLibrary.get_all_level_actors():
        if old.get_actor_label() == label:
            unreal.EditorLevelLibrary.destroy_actor(old)
    a = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc), unreal.Rotator(0,0,0))
    a.set_actor_label(label); a.static_mesh_component.set_static_mesh(cube); a.set_actor_scale3d(unreal.Vector(dims[0]/100.0, dims[1]/100.0, dims[2]/100.0)); a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return a
# Circulation references: dimensions follow the project guide (7-8 m main avenue, 3-4 m paths).
marker('Road_Main_EastWest', (0, -10000, 180), (70000, 800, 24))
marker('Road_Main_NorthSouth', (0, 10000, 180), (800, 70000, 24))
marker('Path_West_Campus', (-15000, 0, 190), (500, 70000, 20))
marker('Path_East_Campus', (15000, 0, 190), (500, 70000, 20))
marker('Plaza_Central', (0, -10000, 210), (9000, 9000, 30))
marker('Plaza_North', (0, 30000, 220), (7000, 5000, 30))
marker('Plaza_South', (0, -40000, 220), (7000, 5000, 30))
starts = [a for a in unreal.EditorLevelLibrary.get_all_level_actors() if isinstance(a, unreal.PlayerStart)]
if not starts:
    p = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-28000, -30000, 500), unreal.Rotator(0,90,0)); p.set_actor_label('PlayerStart_Campus_Natural')
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_CAMPUS_PASS_COMPLETE')
