import os
import unreal

ROOT = "/Game/Modelos3D"
REPORT = r"C:\Users\jeffa\Desktop\Proyecto\Proyecto-Memory\Tools\Logs\verify_all_imported_2026-07-31.txt"
registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = registry.get_assets_by_path(unreal.Name(ROOT), True)
meshes = [a for a in assets if str(a.asset_class_path.asset_name) == "StaticMesh"]
lines = ["VERIFY ALL IMPORTED ASSETS", "===========================", "Total StaticMesh: {}".format(len(meshes))]
bad_bounds, bad_materials, bad_collision, errors = [], [], [], []

for data in sorted(meshes, key=lambda item: str(item.package_name)):
    path = "{}.{}".format(data.package_name, data.asset_name)
    try:
        mesh = unreal.load_asset(path)
        bounds = mesh.get_bounding_box()
        size = bounds.max - bounds.min
        if size.x <= 0 or size.y <= 0 or size.z <= 0:
            bad_bounds.append(path)
        materials = mesh.get_editor_property("static_materials") or []
        if len(materials) == 0:
            bad_materials.append(path)
        body = mesh.get_editor_property("body_setup")
        agg = body.get_editor_property("agg_geom") if body else None
        convex = len(agg.get_editor_property("convex_elems")) if agg else 0
        boxes = len(agg.get_editor_property("box_elems")) if agg else 0
        if convex + boxes == 0:
            bad_collision.append(path)
    except Exception as exc:
        errors.append("{} | {}".format(path, exc))

lines += [
    "Bounds invalidos: {}".format(len(bad_bounds)),
    "Sin materiales: {}".format(len(bad_materials)),
    "Sin colision convex/box: {}".format(len(bad_collision)),
    "Errores de lectura: {}".format(len(errors)),
]
for title, values in (("BOUNDS_INVALIDOS", bad_bounds), ("SIN_MATERIALES", bad_materials), ("SIN_COLISION", bad_collision), ("ERRORES", errors)):
    lines += ["", title, "-" * len(title)] + (values or ["(ninguno)"])

os.makedirs(os.path.dirname(REPORT), exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as handle:
    handle.write("\n".join(lines) + "\n")
unreal.log("VERIFY_ALL_DONE meshes={} bounds={} materials={} collision={} errors={}".format(
    len(meshes), len(bad_bounds), len(bad_materials), len(bad_collision), len(errors)))
