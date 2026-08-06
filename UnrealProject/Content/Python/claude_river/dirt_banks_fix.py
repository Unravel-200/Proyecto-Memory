"""Rehace la capa de tierra a partir de un LayerInfo valido.

El LayerInfo que cree por Python tenia LayerName vacio (esa propiedad es de
solo lectura), y por eso el pincel no pintaba nada. Se duplica uno de fabrica,
que ya trae LayerName='Mud', y se usa ese nombre en todas partes: material,
capas del landscape, ajustes del rio y pincel.
"""

import unreal

SRC_INFO = "/Landmass/PreviewContent/LayerInfos/Mud_LayerInfo"
DST_INFO = "/Game/Materials/LandscapeCampus/LayerInfo_TierraRibera"
MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"
OLD_LAYER = "Tierra"
LAYER = "Mud"                 # debe coincidir con LayerName del LayerInfo
BANK_FALLOFF = 1300.0

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
brush = [a for a in actors if a.get_class().get_name() == "WaterBrushManager"][0]
comp = river.get_editor_property("water_body_component")

# ---------- 1) LayerInfo valido ----------
info = unreal.EditorAssetLibrary.load_asset(DST_INFO)
if info is None:
    unreal.EditorAssetLibrary.duplicate_asset(SRC_INFO, DST_INFO)
    info = unreal.EditorAssetLibrary.load_asset(DST_INFO)
unreal.EditorAssetLibrary.save_asset(DST_INFO, only_if_is_dirty=False)
print("LayerInfo: %s   LayerName=%s" % (info.get_path_name(),
                                        info.get_editor_property("layer_name")))

# ---------- 2) material: renombrar la capa del nodo ----------
mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)
mel = unreal.MaterialEditingLibrary
nodes = [e for e in mel.get_material_expressions(mat)
         if e.get_class().get_name() == "MaterialExpressionLandscapeLayerWeight"]
for nd in nodes:
    nd.set_editor_property("parameter_name", LAYER)
    print("nodo del material -> capa '%s'" % nd.get_editor_property("parameter_name"))
if nodes:
    mel.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(MAT_PATH, only_if_is_dirty=False)

# ---------- 3) capas del landscape ----------
tl = land.get_editor_property("target_layers")
for k in [str(k) for k in tl.keys()]:
    if k == OLD_LAYER:
        try:
            del tl[k]
        except Exception as exc:  # noqa: BLE001
            print("no pude quitar '%s': %s" % (k, str(exc)[:70]))
st = unreal.LandscapeTargetLayerSettings()
st.set_editor_property("layer_info_obj", info)
tl[LAYER] = st
print("target_layers:", [str(k) for k in
                         land.get_editor_property("target_layers").keys()])

# ---------- 4) rio y pincel ----------
ws = unreal.WaterBodyWeightmapSettings()
ws.set_editor_property("falloff_width", BANK_FALLOFF)
ws.set_editor_property("edge_offset", 0.0)
ws.set_editor_property("final_opacity", 1.0)
lws = comp.get_editor_property("layer_weightmap_settings")
for k in [str(k) for k in lws.keys()]:
    if k == OLD_LAYER:
        try:
            del lws[k]
        except Exception:  # noqa: BLE001
            pass
lws[LAYER] = ws
print("weightmap del rio:", [str(k) for k in
                             comp.get_editor_property("layer_weightmap_settings").keys()])

brush.set_editor_property("affect_weightmap", True)
brush.set_editor_property("affected_weightmap_layers", [LAYER])
print("pincel: capas =", [str(x) for x in
                          brush.get_editor_property("affected_weightmap_layers")])

# ---------- 5) recalcular ----------
sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
land.force_layers_full_update()
print("capas objetivo del landscape:", [str(x) for x in land.get_target_layer_names()])
print("FIX_OK")
