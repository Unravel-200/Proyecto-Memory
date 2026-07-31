import unreal

SAMPLES = [
    "/Game/Modelos3D/Residencias/SM_Wardrobe_Residencias_A",
    "/Game/Modelos3D/Residencias/SM_BathroomSet_Residencias_A",
    "/Game/Modelos3D/Biblioteca/SM_DoorLeaf_LibraryMain_A_L",
    "/Game/Modelos3D/Exteriores/SM_ParkingLotLarge_Exteriores_A" if unreal.EditorAssetLibrary.does_asset_exist(
        "/Game/Modelos3D/Exteriores/SM_ParkingLotLarge_Exteriores_A") else "/Game/Modelos3D/Exteriores/SM_Bus_Exteriores_A",
    "/Game/Modelos3D/Ingenieria/SM_StorageShelf_Ingenieria_A",
]

report_lines = []
for path in SAMPLES:
    if not unreal.EditorAssetLibrary.does_asset_exist(path):
        report_lines.append("{} | NO EXISTE".format(path))
        continue
    mesh = unreal.EditorAssetLibrary.load_asset(path)
    bounds = mesh.get_bounding_box()
    size = bounds.max - bounds.min
    body_setup = mesh.get_editor_property("body_setup")
    num_convex = 0
    num_boxes = 0
    if body_setup:
        agg = body_setup.get_editor_property("agg_geom")
        num_convex = len(agg.get_editor_property("convex_elems"))
        num_boxes = len(agg.get_editor_property("box_elems"))
    num_materials = len(mesh.get_editor_property("static_materials")) if mesh.get_editor_property(
        "static_materials") is not None else -1
    report_lines.append(
        "{} | size_cm=({:.1f},{:.1f},{:.1f}) | box_collision={} | convex_collision={} | materiales={}".format(
            path, size.x, size.y, size.z, num_boxes, num_convex, num_materials
        )
    )

with open(r"C:\Users\jeffa\Desktop\Proyecto\Proyecto-Memory\verify_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

unreal.log("VERIFY_DONE")
for line in report_lines:
    unreal.log("VERIFY: " + line)
