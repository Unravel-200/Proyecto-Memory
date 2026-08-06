import unreal

r = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
     if isinstance(a, unreal.WaterBodyRiver)][0]
c = r.get_editor_property("water_body_component")
print("key   width      depth      velocidad")
for k in (0, 5, 10, 20, 30, 40, 49):
    print("%3d  %9.1f  %9.1f  %9.1f" % (
        k,
        c.get_river_width_at_spline_input_key(float(k)),
        c.get_river_depth_at_spline_input_key(float(k)),
        c.get_water_velocity_at_spline_input_key(float(k)),
    ))
print("water_heightmap_settings:", c.get_editor_property("water_heightmap_settings"))
print("collision_height_offset:", c.get_editor_property("collision_height_offset"))
