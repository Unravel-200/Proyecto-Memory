"""Fuerza el PostEditChange de la WaterZone para que recalcule sus limites y
vuelva a renderizar la superficie de agua."""

import unreal

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
zone = [a for a in actors if isinstance(a, unreal.WaterZone)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]

print("zona:", zone.get_actor_label(), zone.get_actor_location())

# reenviar propiedades de forma -> PostEditChangeProperty -> MarkForRebuild
ext = zone.get_editor_property("zone_extent")
zone.set_editor_property("zone_extent", unreal.Vector2D(ext.x + 100.0, ext.y + 100.0))
zone.set_editor_property("zone_extent", ext)
print("zone_extent reenviado:", ext)

res = zone.get_editor_property("render_target_resolution")
zone.set_editor_property("render_target_resolution", unreal.IntPoint(res.x // 2, res.y // 2))
zone.set_editor_property("render_target_resolution", res)
print("render_target_resolution reenviado:", res)

# recentrar la zona en Z sobre el rango real del rio
spl = river.get_component_by_class(unreal.WaterSplineComponent)
zs = [spl.get_location_at_spline_point(i, unreal.SplineCoordinateSpace.WORLD).z
      for i in range(spl.get_number_of_spline_points())]
mid = (min(zs) + max(zs)) / 2.0
loc = zone.get_actor_location()
print("z del rio: %.1f .. %.1f  (centro %.1f)   z de la zona: %.1f"
      % (min(zs), max(zs), mid, loc.z))
zone.set_actor_location(unreal.Vector(loc.x, loc.y, mid), False, False)
print("zona recolocada en z=%.1f" % mid)

# y volver a marcar el rio
comp = river.get_editor_property("water_body_component")
sd = comp.get_editor_property("shape_dilation")
comp.set_editor_property("shape_dilation", float(sd) + 1.0)
comp.set_editor_property("shape_dilation", float(sd))

sm = river.get_components_by_class(unreal.SplineMeshComponent)
print("SplineMesh del rio: %d  (visibles %d)"
      % (len(sm), sum(1 for c in sm if c.get_editor_property("visible"))))
print("ZONE_REBUILD_OK")
