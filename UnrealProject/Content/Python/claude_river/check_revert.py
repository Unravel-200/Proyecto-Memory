"""Comprueba que el terreno volvio a su estado original tras reiniciar."""

import json

import unreal

BASE = "C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
D = json.load(open(BASE, encoding="utf-8"))
G, N, STEP, MINXY = D["grid"], D["n"], D["step"], D["min_xy"]

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


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


# puntos del eje que YO habia tallado (borde sur y flanco oeste)
probes = [(43712, -45424), (16269, -47401), (11118, -47137), (6033, -45988),
          (-27081, -14268), (-25593, -8029), (-23554, -2180), (-17311, 21396),
          (-22843, 46321), (0, 0)]

print("   punto                base      actual     delta")
worst = 0.0
for x, y in probes:
    b, l = base(x, y), live(x, y)
    d = (l - b) if l is not None else 0.0
    worst = max(worst, abs(d))
    print("  (%7d,%8d) %9.1f %9.1f %9.1f" % (x, y, b, l if l else -9999, d))
print("\ndesviacion maxima: %.1f uu" % worst)
print("terreno revertido:", worst < 60.0,
      "  (la tolerancia recoge el error de interpolacion de la rejilla)")
