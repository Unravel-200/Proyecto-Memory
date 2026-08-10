import unreal

MAP = '/Game/Maps/L_Campus_Blockout'
unreal.EditorLevelLibrary.load_level(MAP)

for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_actor_label().startswith('CampusBuilding_'):
        unreal.EditorLevelLibrary.destroy_actor(actor)

def place(label, folder, asset, location, yaw=0.0):
    path = '/Game/Modelos3D/%s/%s.%s' % (folder, asset, asset)
    mesh = unreal.load_object(None, path)
    if mesh is None:
        unreal.log_error('Missing building asset: ' + path)
        return None
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        unreal.Rotator(0.0, yaw, 0.0))
    actor.set_actor_label('CampusBuilding_' + label)
    actor.static_mesh_component.set_static_mesh(mesh)
    actor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return actor

# Demonstration arrangement: clear zones around the ravine and main roads.
place('Plaza', 'Plaza', 'SM_PlazaFloorBlockout_A', (15000.0, 0.0, 1650.0))
place('Biblioteca', 'Biblioteca', 'SM_VestibuloBlockout_Library_A', (-19000.0, -18000.0, 1750.0), 90.0)
place('Generales', 'Generales', 'SM_VestibuloBlockout_Generales_A', (18000.0, -18000.0, 1800.0), -90.0)
place('Educacion', 'Educacion', 'SM_AulaBlockout_Educacion_A', (-19000.0, 18000.0, 2100.0))
place('Ingenieria', 'Ingenieria', 'SM_TallerBlockout_Ingenieria_A', (18000.0, 18000.0, 2300.0), 90.0)
place('Ciencias', 'Ciencias', 'SM_InvernaderoBlockout_Ciencias_A', (-26000.0, 30000.0, 1850.0))
place('Residencias', 'Residencias', 'SM_SalaBlockout_Residencias_A', (25000.0, 30000.0, 2200.0), 90.0)
place('Mantenimiento', 'Mantenimiento', 'SM_TallerBlockout_Mantenimiento_A', (26000.0, -27000.0, 1800.0), -90.0)

unreal.EditorLevelLibrary.save_current_level()
