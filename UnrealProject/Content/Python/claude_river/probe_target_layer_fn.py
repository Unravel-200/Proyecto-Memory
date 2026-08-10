"""Busca la funcion que registra una capa de pintura en el landscape."""

import unreal

L = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
     .get_all_level_actors() if isinstance(a, unreal.Landscape)][0]
info = unreal.EditorAssetLibrary.load_asset(
    "/Game/Materials/LandscapeCampus/LayerInfo_Tierra")

st = unreal.LandscapeTargetLayerSettings()
st.set_editor_property("layer_info_obj", info)

candidatos = [
    ("AddTargetLayer", ("Tierra", st)),
    ("UpdateTargetLayer", ("Tierra", st)),
    ("AddTargetLayerBP", ("Tierra", st)),
    ("CreateLayerInfo", ("Tierra",)),
    ("AddLayerInfo", (info,)),
    ("SetTargetLayer", ("Tierra", st)),
    ("EditorAddTargetLayer", ("Tierra", st)),
]

for name, args in candidatos:
    try:
        r = L.call_method(name, args)
        print("  %-22s -> OK  %s" % (name, r))
    except Exception as exc:  # noqa: BLE001
        msg = str(exc).replace("\n", " ")
        estado = "no existe" if "Failed to find function" in msg else msg[:130]
        print("  %-22s -> %s" % (name, estado))

print("\ntarget_layers ahora:",
      [str(k) for k in L.get_editor_property("target_layers").keys()])
print("get_target_layer_names:", [str(x) for x in L.get_target_layer_names()])
