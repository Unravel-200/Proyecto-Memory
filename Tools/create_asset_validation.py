import unreal

LEVEL = "/Game/Maps/L_AssetValidation"
SAMPLES = [
    ("/Game/Modelos3D/Residencias/SM_Wardrobe_Residencias_A", (0, 0, 0)),
    ("/Game/Modelos3D/Residencias/SM_BathroomSet_Residencias_A", (500, 0, 0)),
    ("/Game/Modelos3D/Biblioteca/SM_DoorLeaf_LibraryMain_A_L", (1000, 0, 0)),
    ("/Game/Modelos3D/Exteriores/SM_ParkingLotLarge_Exteriores_A", (1500, 0, 0)),
    ("/Game/Modelos3D/Ingenieria/SM_StorageShelf_Ingenieria_A", (2000, 0, 0)),
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

for path, xyz in SAMPLES:
    mesh = unreal.load_asset(path)
    if not mesh:
        unreal.log_warning("AssetValidation missing: {}".format(path))
        continue
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(*xyz), unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label("VALIDATE_" + path.rsplit("/", 1)[-1])
    actor.static_mesh_component.set_static_mesh(mesh)
    actor.static_mesh_component.set_collision_profile_name("BlockAll")

unreal.EditorLevelLibrary.save_current_level()
unreal.log("ASSET_VALIDATION_DONE {}".format(LEVEL))
