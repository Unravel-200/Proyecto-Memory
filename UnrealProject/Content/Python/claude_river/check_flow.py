"""Comprueba que el vector de flujo apunta siempre aguas abajo (un solo sentido)."""

import math

import unreal

river = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
         .get_all_level_actors() if isinstance(a, unreal.WaterBodyRiver)][0]
spline = river.get_component_by_class(unreal.WaterSplineComponent)
comp = river.get_editor_property("water_body_component")

npts = spline.get_number_of_spline_points()
total = spline.get_spline_length()
WS = unreal.SplineCoordinateSpace.WORLD

print("puntos %d   longitud %.0f uu" % (npts, total))
print(" key      z      dz/ds      |v|    v.aguas_abajo   anchura  profundidad")

bad_dir = 0
bad_z = 0
prev = None
rows = 0
for s in range(0, 201):
    d = total * s / 200.0
    key = d / total * (npts - 1)
    loc = spline.get_location_at_distance_along_spline(d, WS)
    tan = spline.get_direction_at_distance_along_spline(d, WS)
    v = comp.get_water_velocity_vector_at_spline_input_key(float(key))
    dot = v.x * tan.x + v.y * tan.y + v.z * tan.z
    mag = math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)
    if mag > 1e-3 and dot <= 0:
        bad_dir += 1
    if prev is not None and loc.z > prev[1] + 0.5:
        bad_z += 1
    if s % 20 == 0:
        grad = 0.0 if prev is None else (prev[1] - loc.z) / max(1.0, d - prev[0])
        print("%5.1f %8.1f %9.4f %8.1f %14.1f %9.0f %10.0f"
              % (key, loc.z, grad, mag, dot,
                 comp.get_river_width_at_spline_input_key(float(key)),
                 comp.get_river_depth_at_spline_input_key(float(key))))
        rows += 1
    prev = (d, loc.z)

print("\nmuestras: 201")
print("tramos donde la cota sube:            %d" % bad_z)
print("muestras con flujo contracorriente:   %d" % bad_dir)
print("SENTIDO UNICO:", bad_z == 0 and bad_dir == 0)
