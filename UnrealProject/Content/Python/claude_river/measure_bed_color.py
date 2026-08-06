"""Cuanto del fondo del cauce queda verde: pendiente y alpha dentro del canal."""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
ADD, MUL = 17.09, -17.35     # umbral actual del material

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


def slope_deg(x, y, step=150.0):
    za, zb = h(x - step, y), h(x + step, y)
    zc, zd = h(x, y - step), h(x, y + step)
    if None in (za, zb, zc, zd):
        return None
    return math.degrees(math.atan(math.hypot((zb - za) / (2 * step),
                                             (zd - zc) / (2 * step))))


def alpha(ang):
    return max(0.0, min(1.0, ADD + MUL * math.cos(math.radians(ang))))


plan = json.load(open(PLAN, encoding="utf-8"))
c, water, width = plan["center"], plan["water"], plan["width"]
n = len(c)

print("  i   posicion en el canal ->  pendiente / alpha   (0=verde, 1=cafe)")
verdes = tot = 0
for i in range(2, n - 1, 4):
    tx = c[i + 1][0] - c[i - 1][0]
    ty = c[i + 1][1] - c[i - 1][1]
    L = math.hypot(tx, ty) or 1.0
    nx, ny = -ty / L, tx / L
    hw = width[i] * 0.5
    fila = []
    for f, etq in ((0.0, "eje"), (0.5, "1/2"), (0.9, "borde"), (1.25, "talud")):
        o = hw * f
        s = slope_deg(c[i][0] + nx * o, c[i][1] + ny * o)
        if s is None:
            fila.append("%s -" % etq)
            continue
        a = alpha(s)
        tot += 1
        if a < 0.35:
            verdes += 1
        fila.append("%s %4.1f/%.2f" % (etq, s, a))
    print("%3d   %s" % (i, "   ".join(fila)))

print("\nmuestras dentro del canal que salen verdes: %d de %d (%.0f%%)"
      % (verdes, tot, 100.0 * verdes / max(1, tot)))
print("profundidad del agua en la boca: %.0f uu" % plan["depth"][-1])
