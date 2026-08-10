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
    mat = unreal.load_object(None, '/Game/Materials/CampusLayout/M_CampusTerrainFallback.M_CampusTerrainFallback')
    if mat: actor.static_mesh_component.set_material(0, mat)
    return actor

tools = unreal.AssetToolsHelpers.get_asset_tools(); mel = unreal.MaterialEditingLibrary
mat = unreal.load_object(None, '/Game/Materials/CampusLayout/M_CampusTerrainFallback.M_CampusTerrainFallback')
if mat is None:
    mat = tools.create_asset('M_CampusTerrainFallback', '/Game/Materials/CampusLayout', unreal.Material, unreal.MaterialFactoryNew())
    expr = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -200, 0)
    expr.set_editor_property('Constant', unreal.LinearColor(0.10, 0.34, 0.07, 1.0)); mel.connect_material_property(expr, '', unreal.MaterialProperty.MP_BASE_COLOR)
    mel.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat)
for old in list(unreal.EditorLevelLibrary.get_all_level_actors()):
    if old.get_actor_label().startswith('NaturalHillFallback_') or old.get_actor_label() == 'NaturalTerrainFallback':
        unreal.EditorLevelLibrary.destroy_actor(old)
spawn_mesh('NaturalTerrainFallback', '/Engine/BasicShapes/Cube.Cube', (0,0,-100), (1200,900,2))
hills = [
    (-38000,-30000,900,(75,60,16)), (-26000,-24000,1250,(95,70,22)), (-12000,-28500,650,(65,55,12)),
    (16000,-27000,1050,(90,65,18)), (30000,-22000,1450,(110,80,25)), (-33000,-5000,800,(80,55,14)),
    (-18000,-7000,1350,(100,70,24)), (18000,-5000,850,(70,55,14)), (34000,2000,1200,(95,70,20)),
    (-30000,18000,1100,(90,65,20)), (-11000,22000,700,(70,55,13)), (15000,20000,1350,(105,75,23)),
    (30000,28000,900,(80,60,16)), (-25000,36000,1200,(95,70,21)), (9000,37000,800,(70,55,14))]
for i, (x,y,z,s) in enumerate(hills):
    spawn_mesh('NaturalHillFallback_%02d' % i, '/Engine/BasicShapes/Sphere.Sphere', (x,y,z), s)
unreal.EditorLevelLibrary.save_current_level(); unreal.log('NATURAL_GROUND_FALLBACK_READY hills=%d' % len(hills))
