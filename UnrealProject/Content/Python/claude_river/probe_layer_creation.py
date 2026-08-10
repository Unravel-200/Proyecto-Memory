"""Comprueba si puedo crear y asignar una capa de pintura desde Python."""

import unreal

PATH = "/Game/Materials/LandscapeCampus"
NAME = "LayerInfo_Tierra"

# 1) crear el LandscapeLayerInfoObject
info = unreal.EditorAssetLibrary.load_asset("%s/%s" % (PATH, NAME))
if info:
    print("ya existia:", info.get_path_name())
else:
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    try:
        info = tools.create_asset(NAME, PATH, unreal.LandscapeLayerInfoObject, None)
        print("creado:", info.get_path_name() if info else None)
    except Exception as exc:  # noqa: BLE001
        print("create_asset fallo:", str(exc)[:160])

if info:
    for p, v in (("layer_name", "Tierra"), ("hardness", 0.5),
                 ("no_weight_blend", False)):
        try:
            info.set_editor_property(p, v)
            print("  %s = %s" % (p, info.get_editor_property(p)))
        except Exception as exc:  # noqa: BLE001
            print("  %s: <err> %s" % (p, str(exc)[:90]))

# 2) probar la estructura de target layer
try:
    s = unreal.LandscapeTargetLayerSettings()
    print("\nLandscapeTargetLayerSettings creado")
    for p in ("layer_info_obj", "layer_info", "info", "layer_name"):
        try:
            s.set_editor_property(p, info)
            print("  set %s -> OK" % p)
        except Exception as exc:  # noqa: BLE001
            print("  set %s -> %s" % (p, str(exc)[:90]))
except Exception as exc:  # noqa: BLE001
    print("no puedo crear LandscapeTargetLayerSettings:", str(exc)[:120])

# 3) ver como esta el mapa de target layers del landscape
land = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        .get_all_level_actors() if isinstance(a, unreal.Landscape)][0]
tl = land.get_editor_property("target_layers")
print("\ntarget_layers actual:", tl, type(tl).__name__)
try:
    print("  claves:", list(tl.keys()))
except Exception as exc:  # noqa: BLE001
    print("  <err>", str(exc)[:90])

# 4) funciones del landscape que suenen a capas objetivo
print("\nfunciones candidatas:",
      [n for n in dir(land) if "target" in n.lower() or "layer_info" in n.lower()])
