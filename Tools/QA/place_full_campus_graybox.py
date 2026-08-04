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
        unreal.log_warning('Missing graybox asset: ' + path)
        return
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(*location), unreal.Rotator(0.0, yaw, 0.0))
    actor.set_actor_label('CampusBuilding_' + label)
    actor.static_mesh_component.set_static_mesh(mesh)
    actor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

# West bank: Biblioteca, Educación, Ciencias, Historia and Artes.
west = [
    ('Biblioteca', 'Biblioteca', 'SM_VestibuloBlockout_Library_A', (-23000, -30000, 1800), 90),
    ('Educacion', 'Educacion', 'SM_ArchivoBlockout_Educacion_A', (-23000, -15000, 2100), 90),
    ('Ciencias', 'Ciencias', 'SM_InvernaderoBlockout_Ciencias_A', (-23000, 0, 1800), 90),
    ('Historia', 'Historia', 'SM_HemerotecaBlockout_Historia_A', (-23000, 15000, 2100), 90),
    ('Artes', 'Artes', 'SM_TeatroExperimentalBlockout_Artes_A', (-23000, 30000, 2300), 90),
]

# East bank: Generales, Mantenimiento, Ingeniería, Informática and Derecho.
east = [
    ('Generales', 'Generales', 'SM_VestibuloBlockout_Generales_A', (23000, -30000, 1800), -90),
    ('Mantenimiento', 'Mantenimiento', 'SM_TallerBlockout_Mantenimiento_A', (23000, -15000, 1800), -90),
    ('Ingenieria', 'Ingenieria', 'SM_TallerBlockout_Ingenieria_A', (23000, 0, 2300), -90),
    ('Informatica', 'Informatica', 'SM_ServidoresBlockout_Informatica_A', (23000, 15000, 2200), -90),
    ('Derecho', 'Derecho', 'SM_SalaJuicioBlockout_Derecho_A', (23000, 30000, 2100), -90),
]

other = [
    ('Medicina', 'Medicina', 'SM_BibliotecaBlockout_Medicina_A', (-30000, -37000, 1700), 0),
    ('Psicologia', 'Psicologia', 'SM_CamaraGesellBlockout_Psicologia_A', (-8000, -37000, 1600), 0),
    ('Gimnasio', 'Gimnasio', 'SM_GimnasioBlockout_Gimnasio_A', (8000, -37000, 1600), 0),
    ('Residencias', 'Residencias', 'SM_SalaBlockout_Residencias_A', (30000, -37000, 1800), 0),
    ('AuditorioCentral', 'AuditorioCentral', 'SM_SalaBlockout_AuditorioCentral_A', (-30000, 37000, 1900), 0),
    ('DerechoBoveda', 'Derecho', 'SM_BovedaBlockout_Derecho_A', (30000, 37000, 2100), 0),
    ('RectoriaNucleo', 'Rectoria', 'SM_NucleoBlockout_Rectoria_A', (12000, 37000, 2200), 0),
    ('Soda', 'Soda', 'SM_ComedorBlockout_Soda_A', (-12000, 37000, 1800), 0),
    ('CentroCultural', 'CentroCultural', 'SM_SalaInvestigacionBlockout_CentroCultural_A', (15000, -5000, 1900), 0),
]

for item in west + east + other:
    place(*item)

unreal.EditorLevelLibrary.save_current_level()
