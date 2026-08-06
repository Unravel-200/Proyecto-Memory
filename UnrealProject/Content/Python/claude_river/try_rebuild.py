"""Busca la via para regenerar la malla de agua del rio."""

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
zone = [a for a in actors if isinstance(a, unreal.WaterZone)][0]
comp = river.get_editor_property("water_body_component")

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

print("\n=== mallas del rio ===")
sm = [c for c in river.get_components_by_class(unreal.SplineMeshComponent)]
print("  SplineMeshComponent:", len(sm), " visibles:", sum(1 for c in sm if c.get_editor_property("visible")))
static = [c for c in river.get_components_by_class(unreal.StaticMeshComponent)]
print("  StaticMeshComponent (incl. derivados):", len(static))
for c in static[:6]:
    print("    ", c.get_class().get_name(),
          "mesh=", c.get_editor_property("static_mesh"),
          "visible=", c.get_editor_property("visible"))

print("\n=== water zone ===")
print("  water_mesh:", zone.get_editor_property("water_mesh"))
print("  info tex array:", zone.get_editor_property("water_info_texture_array"))

print("\n=== UFUNCTIONs candidatas ===")
for obj, name in ((comp, "comp"), (river, "river"), (zone, "zone")):
    for fn in ("UpdateAll", "UpdateWaterBodyRenderData", "UpdateComponentVisibility",
               "UpdateWaterBodyStaticMeshComponents", "UpdateWaterSpriteComponent",
               "UpdateMaterialInstances", "OnWaterBodyChanged", "MarkForRebuild",
               "MarkWaterMeshComponentForRebuild", "UpdateWaterInfoTexture",
               "RebuildWaterMesh", "MarkWaterMeshGridDirty", "Update"):
        try:
            r = obj.call_method(fn)
            print("  %-6s %-38s -> OK %s" % (name, fn, r))
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if "Failed to find function" not in msg:
                print("  %-6s %-38s -> %s" % (name, fn, msg[:90]))
