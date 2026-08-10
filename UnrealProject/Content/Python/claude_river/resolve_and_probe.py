"""Fuerza la resolucion de las capas del landscape y vuelve a medir los puntos
testigo, para saber si la desviacion era solo un estado sin resolver."""

import json

import unreal

BASE = "C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
D = json.load(open(BASE, encoding="utf-8"))
G, N, STEP, MINXY = D["grid"], D["n"], D["step"], D["min_xy"]

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
landscape = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
             .get_all_level_actors() if isinstance(a, unreal.Landscape)][0]


def base(x, y):
    fx, fy = (x - MINXY) / STEP, (y - MINXY) / STEP
    ix = max(0, min(N - 2, int(fx)))
    iy = max(0, min(N - 2, int(fy)))
    tx, ty = fx - ix, fy - iy
    a = G[iy][ix] * (1 - tx) + G[iy][ix + 1] * tx
    b = G[iy + 1][ix] * (1 - tx) + G[iy + 1][ix + 1] * tx
    return a * (1 - ty) + b * ty


def live(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


probes = [(0, 0), (20000, -30000), (43712, -45424), (-22843, 46321),
          (16269, -47401), (46900, -48030), (13108, -19318), (-5527, 18302)]

print("antes de forzar:")
for x, y in probes:
    print("  (%7d,%8d)  base %9.1f   actual %9.1f" % (x, y, base(x, y), live(x, y)))

print("\nforzando force_layers_full_update()...")
landscape.force_layers_full_update()

print("\ndespues de forzar:")
worst = 0.0
for x, y in probes:
    b, l = base(x, y), live(x, y)
    worst = max(worst, abs(l - b))
    print("  (%7d,%8d)  base %9.1f   actual %9.1f   delta %8.1f" % (x, y, b, l, l - b))
print("\ndesviacion maxima: %.1f uu" % worst)
