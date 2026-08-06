"""Que pinta el terreno en las riberas: capas de pintura y ajustes de weightmap."""

import unreal

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
landscape = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
brush = [a for a in actors if a.get_class().get_name() == "WaterBrushManager"][0]
comp = river.get_editor_property("water_body_component")

print("=== LANDSCAPE ===")
mat = landscape.get_editor_property("landscape_material")
print("  material:", mat.get_path_name() if mat else None)
print("  target layers:", landscape.get_editor_property("target_layers"))
print("  nombres de capa objetivo:", landscape.get_target_layer_names())

print("\n=== CAPAS DE PINTURA DEL MATERIAL ===")
if mat:
    try:
        names = unreal.MaterialEditingLibrary.get_material_layer_names(mat) \
            if hasattr(unreal.MaterialEditingLibrary, "get_material_layer_names") else None
        print("  get_material_layer_names:", names)
    except Exception as exc:  # noqa: BLE001
        print("  get_material_layer_names: <err>", str(exc)[:80])
    try:
        params = unreal.MaterialEditingLibrary.get_scalar_parameter_names(mat)
        print("  parametros escalares:", list(params)[:30])
    except Exception as exc:  # noqa: BLE001
        print("  escalares: <err>", str(exc)[:80])
    try:
        tex = unreal.MaterialEditingLibrary.get_texture_parameter_names(mat)
        print("  parametros de textura:", list(tex)[:30])
    except Exception as exc:  # noqa: BLE001
        print("  texturas: <err>", str(exc)[:80])
    try:
        vec = unreal.MaterialEditingLibrary.get_vector_parameter_names(mat)
        print("  parametros vectoriales:", list(vec)[:30])
    except Exception as exc:  # noqa: BLE001
        print("  vectoriales: <err>", str(exc)[:80])

print("\n=== LAYER INFO OBJECTS EN EL PROYECTO ===")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
found = ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Landscape",
                                                        "LandscapeLayerInfoObject"), True)
for a in found:
    print("  ", a.package_name)
if not found:
    print("   ninguno")

print("\n=== AJUSTES DE WEIGHTMAP DEL RIO ===")
for p in ("water_body_weightmap_settings", "layer_weightmap_settings",
          "weightmap_settings", "water_heightmap_settings"):
    try:
        print("  %s = %s" % (p, str(comp.get_editor_property(p))[:400]))
    except Exception:  # noqa: BLE001
        print("  %s = <no existe>" % p)

print("\n=== PINCEL ===")
for p in ("affect_weightmap", "affected_weightmap_layers", "affect_heightmap"):
    try:
        print("  %s = %s" % (p, brush.get_editor_property(p)))
    except Exception:  # noqa: BLE001
        print("  %s = <no existe>" % p)
