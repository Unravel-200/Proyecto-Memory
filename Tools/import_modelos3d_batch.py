import unreal
import os

SOURCE_ROOT = r"C:\Users\jeffa\Desktop\Proyecto\Modelos-3D"
DEST_ROOT = "/Game/Modelos3D"
REPORT_PATH = r"C:\Users\jeffa\Desktop\Proyecto\Proyecto-Memory\import_report.txt"

ZONES = [
    "Artes", "AuditorioCentral", "Biblioteca", "CentroCultural", "Ciencias",
    "Derecho", "Educacion", "Exteriores", "Generales", "Gimnasio", "Historia",
    "Informatica", "Ingenieria", "Mantenimiento", "Medicina", "Plaza",
    "Psicologia", "Rectoria", "Residencias", "Soda",
]

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

imported = []
failed = []

for zone in ZONES:
    src_dir = os.path.join(SOURCE_ROOT, zone)
    if not os.path.isdir(src_dir):
        continue
    dest_path = "{}/{}".format(DEST_ROOT, zone)
    for fname in sorted(os.listdir(src_dir)):
        if not fname.lower().endswith(".fbx"):
            continue
        fpath = os.path.join(src_dir, fname)
        try:
            task = unreal.AssetImportTask()
            task.filename = fpath
            task.destination_path = dest_path
            task.automated = True
            task.save = True
            task.replace_existing = True

            options = unreal.FbxImportUI()
            options.import_mesh = True
            options.import_as_skeletal = False
            options.import_materials = True
            options.import_textures = True
            try:
                options.static_mesh_import_data.set_editor_property("combine_meshes", False)
            except Exception:
                pass
            task.options = options

            asset_tools.import_asset_tasks([task])
            paths = list(task.get_editor_property("imported_object_paths"))
            if paths:
                imported.append((fname, zone, paths))
            else:
                failed.append((fname, zone, "sin objetos importados"))
        except Exception as exc:
            failed.append((fname, zone, str(exc)))

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("ARCHIVO | ZONA | ASSETS_IMPORTADOS\n")
    for fname, zone, paths in imported:
        f.write("{} | {} | {}\n".format(fname, zone, ";".join(paths)))
    f.write("\nFALLIDOS ({}):\n".format(len(failed)))
    for fname, zone, err in failed:
        f.write("{} | {} | {}\n".format(fname, zone, err))

unreal.log("IMPORT_SUMMARY: {} archivos importados, {} fallidos".format(len(imported), len(failed)))
unreal.log("IMPORT_DONE")

unreal.SystemLibrary.quit_editor()
