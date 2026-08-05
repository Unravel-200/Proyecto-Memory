import unreal

def find(label):
    return next((a for a in unreal.EditorLevelLibrary.get_all_level_actors() if a.get_actor_label() == label), None)
def spawn_mesh(label, mesh_path, loc, scale):
    old = find(label)
    if old:
        unreal.EditorLevelLibrary.destroy_actor(old)
    mesh = unreal.load_object(None, mesh_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc), unreal.Rotator(0,0,0))
    actor.set_actor_label(label); actor.static_mesh_component.set_static_mesh(mesh); actor.set_actor_scale3d(unreal.Vector(*scale)); actor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    mat = unreal.load_object(None, '/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural.M_Landscape_Campus_Natural')
    if mat: actor.static_mesh_component.set_material(0, mat)
    return actor

spawn_mesh('NaturalTerrainFallback', '/Engine/BasicShapes/Cube.Cube', (0,0,-100), (1200,900,2))
hills = [(-32000,-26000,1400,(180,130,18)), (-9000,-30000,900,(140,110,12)), (18000,-25000,1700,(190,140,20)), (-26000,18000,1200,(160,120,16)), (12000,22000,1500,(200,150,18)), (36000,12000,1000,(130,100,14))]
for i, (x,y,z,s) in enumerate(hills):
    spawn_mesh('NaturalHillFallback_%02d' % i, '/Engine/BasicShapes/Sphere.Sphere', (x,y,z), s)
unreal.EditorLevelLibrary.save_current_level(); unreal.log('NATURAL_GROUND_FALLBACK_READY hills=%d' % len(hills))
