"""Pone tierra (cafe) en las riberas del rio, y solo ahi.

El material del landscape colorea por pendiente: verde en lo llano, cafe solo
en taludes de mas de ~45 grados. Las riberas del rio rondan los 30-35, asi que
salian verdes. Bajar ese umbral tenirira de cafe media montana, de modo que en
vez de eso se anade una capa de pintura 'Tierra' que el pincel de agua pinta
unicamente alrededor del cauce:

  - material: nodo LandscapeLayerWeight. Donde la capa vale 0 se ve exactamente
    lo de antes; donde vale 1, el cafe de tierra.
  - pincel de agua: pinta esa capa a lo largo del rio.
"""

import unreal

LAYER = "Tierra"
INFO_PATH = "/Game/Materials/LandscapeCampus/LayerInfo_Tierra"
MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"
DIRT = (0.26, 0.22, 0.16)     # el cafe de tierra que ya usa tu material
BANK_FALLOFF = 1300.0         # hasta donde llega la tierra desde el cauce
EDGE_OFFSET = 0.0
FINAL_OPACITY = 1.0

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
brush = [a for a in actors if a.get_class().get_name() == "WaterBrushManager"][0]
comp = river.get_editor_property("water_body_component")

# ---------- 1) capa de pintura ----------
info = unreal.EditorAssetLibrary.load_asset(INFO_PATH)
if info is None:
    info = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        "LayerInfo_Tierra", "/Game/Materials/LandscapeCampus",
        unreal.LandscapeLayerInfoObject, None)
unreal.EditorAssetLibrary.save_asset(INFO_PATH, only_if_is_dirty=False)
print("capa de pintura:", info.get_path_name())

# 'target_layers' es de solo lectura via set_editor_property, pero el mapa que
# devuelve get_editor_property es una referencia viva: mutarlo si funciona.
tl = land.get_editor_property("target_layers")
if LAYER not in [str(k) for k in tl.keys()]:
    st = unreal.LandscapeTargetLayerSettings()
    st.set_editor_property("layer_info_obj", info)
    tl[LAYER] = st
print("target_layers:", [str(k) for k in
                         land.get_editor_property("target_layers").keys()])

# ---------- 2) material ----------
mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)
mel = unreal.MaterialEditingLibrary

existing = [e for e in mel.get_material_expressions(mat)
            if e.get_class().get_name() == "MaterialExpressionLandscapeLayerWeight"]
if existing:
    print("el material ya tiene el nodo de capa, no se toca")
else:
    lerp = [e for e in mel.get_material_expressions(mat)
            if e.get_class().get_name() == "MaterialExpressionLinearInterpolate"][0]

    dirt = mel.create_material_expression(
        mat, unreal.MaterialExpressionConstant3Vector, -420, 300)
    dirt.set_editor_property("constant", unreal.LinearColor(DIRT[0], DIRT[1], DIRT[2], 1.0))

    lw = mel.create_material_expression(
        mat, unreal.MaterialExpressionLandscapeLayerWeight, -180, 160)
    lw.set_editor_property("parameter_name", LAYER)
    for p, v in (("preview_weight", 0.0), ("const_base", unreal.Vector(0, 0, 0))):
        try:
            lw.set_editor_property(p, v)
        except Exception:  # noqa: BLE001
            pass

    names = list(mel.get_material_expression_input_names(lw))
    print("entradas del nodo de capa:", names)
    base_pin = "Base" if "Base" in names else names[0]
    layer_pin = "Layer" if "Layer" in names else names[1]

    mel.connect_material_expressions(lerp, "", lw, base_pin)
    mel.connect_material_expressions(dirt, "", lw, layer_pin)
    mel.connect_material_property(lw, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.recompile_material(mat)
    print("material: LandscapeLayerWeight('%s') insertado antes de BaseColor" % LAYER)

unreal.EditorAssetLibrary.save_asset(MAT_PATH, only_if_is_dirty=False)

# ---------- 3) que el pincel pinte esa capa ----------
ws = unreal.WaterBodyWeightmapSettings()
ws.set_editor_property("falloff_width", BANK_FALLOFF)
ws.set_editor_property("edge_offset", EDGE_OFFSET)
ws.set_editor_property("final_opacity", FINAL_OPACITY)

lws = comp.get_editor_property("layer_weightmap_settings")
lws[LAYER] = ws
comp.set_editor_property("layer_weightmap_settings", lws)
print("ajustes de weightmap del rio:", [str(k) for k in
                                        comp.get_editor_property("layer_weightmap_settings").keys()])

brush.set_editor_property("affect_weightmap", True)
brush.set_editor_property("affected_weightmap_layers", [LAYER])
print("pincel: affect_weightmap=%s  capas=%s"
      % (brush.get_editor_property("affect_weightmap"),
         [str(x) for x in brush.get_editor_property("affected_weightmap_layers")]))

# ---------- 4) recalcular ----------
sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
land.force_layers_full_update()
print("DIRT_OK")
