import unreal

LEVEL = "/Game/Maps/L_AssetValidation"
ZONES = [
    "Artes", "AuditorioCentral", "Biblioteca", "CentroCultural", "Ciencias",
    "Derecho", "Educacion", "Exteriores", "Generales", "Gimnasio", "Historia",
    "Informatica", "Ingenieria", "Mantenimiento", "Medicina", "Plaza",
    "Psicologia", "Rectoria", "Residencias", "Soda",
]

if unreal.EditorAssetLibrary.does_asset_exist(LEVEL):
    unreal.EditorLevelLibrary.load_level(LEVEL)
else:
    unreal.EditorLevelLibrary.new_level(LEVEL)

world = unreal.EditorLevelLibrary.get_editor_world()

# Lighting and a neutral platform make the validation map readable on first open.
sun = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.DirectionalLight, unreal.Vector(0, 0, 1200), unreal.Rotator(-45, -35, 0)
)
sun.set_actor_label("VALIDATE_Sun")
sun.light_component.set_editor_property("intensity", 5.0)
sky = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SkyLight, unreal.Vector(0, 0, 800), unreal.Rotator(0, 0, 0)
)
sky.set_actor_label("VALIDATE_Sky")
sky.light_component.set_editor_property("intensity", 1.0)
floor_mesh = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
if floor_mesh:
    floor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(1000, 0, -100), unreal.Rotator(0, 0, 0)
    )
    floor.set_actor_label("VALIDATE_Platform")
    floor.set_actor_scale3d(unreal.Vector(30, 12, 0.1))
    floor.static_mesh_component.set_static_mesh(floor_mesh)
    floor.static_mesh_component.set_collision_profile_name("BlockAll")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
samples = []
for index, zone in enumerate(ZONES):
    assets = registry.get_assets_by_path(unreal.Name("/Game/Modelos3D/" + zone), True)
    meshes = sorted(
        ["{}.{}".format(a.package_name, a.asset_name) for a in assets
         if str(a.asset_class_path.asset_name) == "StaticMesh" and str(a.asset_name).startswith("SM_")],
        key=lambda value: value.lower(),
    )
    if not meshes:
        unreal.log_warning("AssetValidation sin StaticMesh en zona: {}".format(zone))
        continue
    column, row = index % 5, index // 5
    samples.append((meshes[0], (column * 900, row * 900, 0), zone))

for path, xyz, zone in samples:
    mesh = unreal.load_asset(path)
    if not mesh:
        unreal.log_warning("AssetValidation missing: {}".format(path))
        continue
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(*xyz), unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label("VALIDATE_{}_{}".format(zone, path.rsplit("/", 1)[-1]))
    actor.static_mesh_component.set_static_mesh(mesh)
    actor.static_mesh_component.set_collision_profile_name("BlockAll")

unreal.EditorLevelLibrary.save_current_level()
unreal.log("ASSET_VALIDATION_DONE {}".format(LEVEL))
