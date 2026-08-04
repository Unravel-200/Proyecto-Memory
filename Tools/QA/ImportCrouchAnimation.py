import unreal

destination = "/Game/Mannequin/Animations/Crouch"
sources = [
    r"C:\\Users\\jeffa\\Desktop\\Proyecto\\Proyecto-Memory\\UnrealProject\\Content\\Mannequin\\Animations\\Crouching_Idle.FBX",
    r"C:\\Users\\jeffa\\Desktop\\Proyecto\\Proyecto-Memory\\UnrealProject\\Content\\Mannequin\\Animations\\Crouched_Walking.FBX",
    r"C:\\Users\\jeffa\\Desktop\\Proyecto\\Proyecto-Memory\\UnrealProject\\Content\\Mannequin\\Animations\\Standing_To_Crouched.FBX",
    r"C:\\Users\\jeffa\\Desktop\\Proyecto\\Proyecto-Memory\\UnrealProject\\Content\\Mannequin\\Animations\\Crouched_To_Standing.FBX",
]

tasks = []
for source in sources:
    task = unreal.AssetImportTask()
    task.filename = source
    task.destination_path = destination
    task.automated = True
    task.replace_existing = True
    task.save = True
    options = unreal.FbxImportUI()
    options.import_mesh = False
    options.import_as_skeletal = True
    options.import_animations = True
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
    options.skeleton = unreal.load_object(None, "/Game/Mannequin/Character/Mesh/SK_Mannequin_Skeleton")
    task.options = options
    tasks.append(task)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
unreal.EditorAssetLibrary.save_directory(destination)
