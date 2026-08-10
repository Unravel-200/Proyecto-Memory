"""Compara mi LayerInfo con uno valido de fabrica: sospecho que el mio esta
incompleto (LayerName vacio), y por eso el pincel no pinta nada."""

import unreal

for path in ("/Game/Materials/LandscapeCampus/LayerInfo_Tierra",
             "/Landmass/PreviewContent/LayerInfos/Mud_LayerInfo",
             "/Landmass/PreviewContent/LayerInfos/Grass_LayerInfo"):
    a = unreal.EditorAssetLibrary.load_asset(path)
    print("\n%s" % path)
    if a is None:
        print("   no se pudo cargar")
        continue
    for p in ("layer_name", "LayerName", "hardness", "no_weight_blend",
              "layer_usage_debug_color", "minimum_collision_relevance_weight"):
        try:
            print("   %-34s = %s" % (p, a.get_editor_property(p)))
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if "Failed to find property" in msg:
                print("   %-34s = <no existe>" % p)
            else:
                print("   %-34s = <solo lectura>  %s" % (p, msg[:60]))
    # intento leer el nombre por reflexion generica
    try:
        print("   to_dict:", {k: str(v)[:40] for k, v in a.to_dict().items()})
    except Exception:  # noqa: BLE001
        pass
