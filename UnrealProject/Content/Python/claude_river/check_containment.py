"""Comprobacion densa de contencion sobre el spline realmente aplicado.

Recorre el rio cada STATION_STEP uu (no solo en los puntos de control) y, en
cada estacion, avanza por las dos margenes buscando la orilla: la primera
distancia donde el terreno supera la lamina de agua. Si en alguna estacion no
aparece orilla dentro del alcance, el agua se sale por ahi.
"""

import math

import unreal

STATION_STEP = 400.0
REACH = 5000.0
RAY_STEP = 80.0

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
TRACE = unreal.TraceTypeQuery.ECC_VISIBILITY


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        TRACE, True, [], unreal.DrawDebugTrace.NONE, True)
    if res is None:
        return None
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


river = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
         .get_all_level_actors() if isinstance(a, unreal.WaterBodyRiver)][0]
spline = river.get_component_by_class(unreal.WaterSplineComponent)
comp = river.get_editor_property("water_body_component")

total = spline.get_spline_length()
npts = spline.get_number_of_spline_points()
print("rio: %.0f uu, %d puntos de control, estaciones cada %.0f uu"
      % (total, npts, STATION_STEP))

WS = unreal.SplineCoordinateSpace.WORLD
nstations = int(total / STATION_STEP) + 1

no_shore = []
margins = []
shores = []
prev_z = None
monotone_ok = True

for s in range(nstations):
    d = min(total, s * STATION_STEP)
    loc = spline.get_location_at_distance_along_spline(d, WS)
    dirv = spline.get_direction_at_distance_along_spline(d, WS)
    key = d / total * (npts - 1)
    hw = comp.get_river_width_at_spline_input_key(float(key)) * 0.5
    wz = loc.z

    if prev_z is not None and wz > prev_z + 0.5:
        monotone_ok = False
    prev_z = wz

    nx, ny = -dirv.y, dirv.x
    L = math.hypot(nx, ny) or 1.0
    nx, ny = nx / L, ny / L

    for sgn in (1, -1):
        shore = None
        margin = None
        dd = hw
        while dd <= REACH:
            z = h(loc.x + nx * sgn * dd, loc.y + ny * sgn * dd)
            if z is not None and z >= wz:
                shore, margin = dd, z - wz
                break
            dd += RAY_STEP
        if shore is None:
            no_shore.append((d, sgn, wz))
        else:
            shores.append(shore - hw)
            margins.append(margin)

print("\nestaciones analizadas: %d  (margenes examinadas: %d)"
      % (nstations, nstations * 2))
print("orilla encontrada en %d de %d margenes" % (len(shores), nstations * 2))
if shores:
    print("distancia de la orilla al borde del cauce: min %.0f  medio %.0f  max %.0f uu"
          % (min(shores), sum(shores) / len(shores), max(shores)))
print("cota del spline estrictamente descendente:", monotone_ok)

if no_shore:
    print("\nSIN ORILLA en %d margenes:" % len(no_shore))
    for d, sgn, wz in no_shore[:40]:
        print("  a %.0f uu del nacimiento, margen %s, agua %.1f"
              % (d, "izquierda" if sgn > 0 else "derecha", wz))
else:
    print("\nSIN FUGAS: todas las margenes tienen orilla por encima del agua.")
