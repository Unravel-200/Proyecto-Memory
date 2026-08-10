"""Diagnostico de por que no se ve agua."""

import unreal


def p(obj, name, label=None):
    try:
        v = obj.get_editor_property(name)
        print("   %-38s = %s" % (label or name, str(v)[:220]))
        return v
    except Exception:  # noqa: BLE001
        print("   %-38s = <no existe>" % (label or name))
        return None


eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()
river = zone = mesh_actor = None
for a in actors:
    if isinstance(a, unreal.WaterBodyRiver):
        river = a
    elif isinstance(a, unreal.WaterZone):
        zone = a
    elif a.get_class().get_name() in ("WaterMeshActor",):
        mesh_actor = a

print("=== ACTOR RIO ===")
print("   label:", river.get_actor_label(), " oculto:", river.is_temporarily_hidden_in_editor())
print("   location:", river.get_actor_location())
comp = river.get_editor_property("water_body_component")
print("   componente:", comp.get_class().get_name())
for n in ("visible", "hidden_in_game", "water_material", "water_static_mesh_material",
          "water_lod_material", "water_info_material", "underwater_post_process_material",
          "water_hlod_material", "affects_landscape", "affects_water_mesh",
          "affects_water_info", "is_water_body_initialized",
          "water_body_static_mesh_settings", "shape_dilation",
          "max_wave_height_offset", "tessellation_factor", "always_generate_waves",
          "can_affect_navigation", "collision_height_offset"):
    p(comp, n)

print("\n   componentes del actor:")
for c in river.get_components_by_class(unreal.SceneComponent):
    try:
        vis = c.get_editor_property("visible")
    except Exception:  # noqa: BLE001
        vis = "?"
    print("     %-42s visible=%s" % (c.get_class().get_name(), vis))

print("\n=== WATER ZONE ===")
if zone is None:
    print("   NO HAY WaterZone EN EL NIVEL")
else:
    print("   label:", zone.get_actor_label(), " loc:", zone.get_actor_location())
    for n in ("zone_extent", "render_target_resolution", "capture_z_bounds",
              "water_height_extents", "ground_z_min", "far_distance_material",
              "far_distance_mesh_extent", "tessellation_factor",
              "local_tessellation_extent", "enable_local_only_tessellation",
              "non_tessellated_lod_section_scale", "water_mesh_component"):
        p(zone, n)

print("\n=== SUBSISTEMA / CVARS ===")
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
for cv in ("r.Water.WaterMesh.Enabled", "r.Water.SingleLayerWater.Reflection",
           "r.Water.WaterMesh.LODCountBias", "r.Water.WaterInfo.RenderMethod",
           "r.Water.EnableWaterInfoRendering"):
    try:
        print("   %-40s = %s" % (cv, unreal.SystemLibrary.get_console_variable_float_value(cv)))
    except Exception as exc:  # noqa: BLE001
        print("   %-40s = <err> %s" % (cv, str(exc)[:60]))

print("\n=== RANGO Z DEL RIO ===")
spl = river.get_component_by_class(unreal.WaterSplineComponent)
zs = [spl.get_location_at_spline_point(i, unreal.SplineCoordinateSpace.WORLD).z
      for i in range(spl.get_number_of_spline_points())]
print("   z de %.1f a %.1f" % (min(zs), max(zs)))
if zone is not None:
    print("   z de la WaterZone: %.1f" % zone.get_actor_location().z)
