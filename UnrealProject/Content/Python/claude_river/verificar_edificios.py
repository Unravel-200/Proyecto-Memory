"""Verifica la colocacion: apoyo en el suelo, holgura al rio y solapes.

El trazado ignora los propios edificios, si no golpearia sus tejados en vez
del terreno.
"""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
smas = [a for a in actors if isinstance(a, unreal.StaticMeshActor)]
edificios = [a for a in smas if a.get_actor_label().startswith("CampusBuilding_")]


def suelo(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 80000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, smas,
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


plan = json.load(open(PLAN, encoding="utf-8"))
eje, anchos = plan["center"], plan["width"]


def dist_rio(x, y):
    mejor, hw = 1e18, 0.0
    for i in range(len(eje) - 1):
        ax, ay = eje[i]
        bx, by = eje[i + 1]
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        t = 0.0 if L2 <= 0 else max(0.0, min(1.0, ((x - ax) * vx + (y - ay) * vy) / L2))
        d = math.hypot(x - (ax + t * vx), y - (ay + t * vy))
        if d < mejor:
            mejor, hw = d, (anchos[i] + (anchos[i + 1] - anchos[i]) * t) * 0.5
    return mejor - hw


print("%-28s %9s %9s %10s %11s" %
      ("edificio", "base", "suelo", "diferencia", "margen rio"))
peor_base = 0.0
peor_rio = 1e18
datos = []
for a in edificios:
    loc = a.get_actor_location()
    origen, extent = a.get_actor_bounds(False)
    base = origen.z - extent.z
    # cota del terreno bajo las cuatro esquinas de la huella
    zs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            z = suelo(loc.x + sx * extent.x * 0.9, loc.y + sy * extent.y * 0.9)
            if z is not None:
                zs.append(z)
    zc = suelo(loc.x, loc.y)
    if zc is not None:
        zs.append(zc)
    ref = max(zs) if zs else None
    dif = None if ref is None else base - ref
    m = dist_rio(loc.x, loc.y)
    datos.append((a, loc, extent, dif, m))
    if dif is not None:
        peor_base = max(peor_base, abs(dif))
    peor_rio = min(peor_rio, m)
    print("%-28s %9.1f %9.1f %10s %11.0f"
          % (a.get_actor_label()[:28], base, ref if ref else -9999,
             "-" if dif is None else "%.1f" % dif, m))

print("\ndesviacion maxima de la base respecto al suelo: %.0f uu" % peor_base)
print("margen minimo al cauce: %.0f uu" % peor_rio)

print("\n=== solapes ===")
solapes = 0
for i in range(len(datos)):
    for j in range(i + 1, len(datos)):
        (a1, l1, e1, _, _), (a2, l2, e2, _, _) = datos[i], datos[j]
        if (abs(l1.x - l2.x) < e1.x + e2.x) and (abs(l1.y - l2.y) < e1.y + e2.y):
            solapes += 1
            print("  %s  <->  %s" % (a1.get_actor_label(), a2.get_actor_label()))
print("  solapes: %d" % solapes)
