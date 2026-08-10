"""Diagnostico del sistema de capas de edicion y del pincel de agua."""

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
river = landscape = brush = None
for a in eas.get_all_level_actors():
    if isinstance(a, unreal.WaterBodyRiver):
        river = a
    elif isinstance(a, unreal.Landscape):
        landscape = a
    elif a.get_class().get_name() == "WaterBrushManager":
        brush = a

print("=== EDIT LAYERS ===")
layers = landscape.get_edit_layers_bp()
for i, l in enumerate(layers):
    print(" [%d] class=%s" % (i, l.get_class().get_name()))
    for p in ("name", "guid", "visible", "locked", "alpha_for_target_type"):
        try:
            print("      %s = %s" % (p, l.get_editor_property(p)))
        except Exception as exc:  # noqa: BLE001
            print("      %s = <err %s>" % (p, exc))
    print("      dir:", [n for n in dir(l) if not n.startswith("_") and "get_" not in n][:40])

print("\n=== CLASES DE EDIT LAYER DISPONIBLES ===")
print([n for n in dir(unreal) if n.startswith("LandscapeEditLayer")])

print("\n=== LANDSCAPE: props relevantes ===")
for p in ("can_have_layers_content", "b_can_have_layers_content", "landscape_guid",
          "use_generated_landscape_split_mesh_actors", "target_layers"):
    try:
        print("  %s = %s" % (p, str(landscape.get_editor_property(p))[:200]))
    except Exception as exc:  # noqa: BLE001
        print("  %s = <no existe>" % p)

print("\n=== WATER BRUSH MANAGER ===")
print("  class:", brush.get_class().get_name())
print("  es LandscapeBlueprintBrushBase:", isinstance(brush, unreal.LandscapeBlueprintBrushBase))
for p in ("heightmap_rta", "heightmap_rtb", "jump_flood_rta", "jump_flood_rtb",
          "depth_and_shape_rt", "water_depth_and_velocity_rt", "combined_velocity_and_height_rta",
          "combined_velocity_and_height_rtb", "weightmap_rta", "weightmap_rtb",
          "affect_heightmap", "affect_weightmap", "affected_weightmap_layers",
          "owning_landscape", "target_landscape", "brush_render_target_type"):
    try:
        v = brush.get_editor_property(p)
        print("  %s = %s" % (p, str(v)[:160]))
    except Exception:  # noqa: BLE001
        print("  %s = <no existe>" % p)

print("\n  props con 'rt' o 'render':", [n for n in dir(brush) if ("rt" in n.lower() or "render" in n.lower()) and not n.startswith("_")][:60])

print("\n=== BRUSHES REGISTRADOS EN LA CAPA ===")
for i, l in enumerate(layers):
    for p in ("brushes", "landscape_brushes", "blueprint_brushes"):
        try:
            print("  capa %d %s = %s" % (i, p, str(l.get_editor_property(p))[:300]))
        except Exception:  # noqa: BLE001
            pass

print("\n=== API landscape: funciones de capa ===")
print([n for n in dir(landscape) if "layer" in n.lower()])
print("\n=== unreal: utilidades de landscape ===")
print([n for n in dir(unreal) if "Landscape" in n and ("Util" in n or "Library" in n or "Subsystem" in n)])
print("\n=== unreal: subsistemas water ===")
print([n for n in dir(unreal) if "Water" in n][:60])
