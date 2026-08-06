"""Mide la pendiente real de las riberas y de las laderas del mapa.

Sirve para elegir el umbral del material: el cafe tiene que cubrir la ribera
sin tragarse los llanos.
"""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


def slope_deg(x, y, step=200.0):
    """Pendiente del terreno en (x,y), en grados."""
    za = h(x - step, y)
    zb = h(x + step, y)
    zc = h(x, y - step)
    zd = h(x, y + step)
    if None in (za, zb, zc, zd):
        return None
    gx = (zb - za) / (2 * step)
    gy = (zd - zc) / (2 * step)
    return math.degrees(math.atan(math.hypot(gx, gy)))


plan = json.load(open(PLAN, encoding="utf-8"))
c, width = plan["center"], plan["width"]
n = len(c)

bank = []
for i in range(1, n - 1):
    tx = c[i + 1][0] - c[i - 1][0]
    ty = c[i + 1][1] - c[i - 1][1]
    L = math.hypot(tx, ty) or 1.0
    nx, ny = -ty / L, tx / L
    hw = width[i] * 0.5
    for sgn in (1, -1):
        for extra in (150.0, 400.0, 700.0):
            s = slope_deg(c[i][0] + nx * sgn * (hw + extra),
                          c[i][1] + ny * sgn * (hw + extra))
            if s is not None:
                bank.append(s)

bank.sort()


def pct(v, p):
    return v[max(0, min(len(v) - 1, int(len(v) * p)))]


print("pendiente de las riberas (%d muestras):" % len(bank))
print("   p10 %.1f   p25 %.1f   mediana %.1f   p75 %.1f   p90 %.1f  max %.1f"
      % (pct(bank, .10), pct(bank, .25), pct(bank, .50),
         pct(bank, .75), pct(bank, .90), bank[-1]))

# terreno general, lejos del rio
lejos = []
for x in range(-44000, 44001, 5500):
    for y in range(-44000, 44001, 5500):
        if min(math.dist((x, y), q) for q in c) < 6000:
            continue
        s = slope_deg(x, y)
        if s is not None:
            lejos.append(s)
lejos.sort()
print("\npendiente del resto del mapa (%d muestras):" % len(lejos))
print("   p25 %.1f   mediana %.1f   p75 %.1f   p90 %.1f   p97 %.1f  max %.1f"
      % (pct(lejos, .25), pct(lejos, .50), pct(lejos, .75),
         pct(lejos, .90), pct(lejos, .97), lejos[-1]))
print("   proporcion del mapa por encima de 22 grados: %.1f%%"
      % (100.0 * sum(1 for s in lejos if s > 22) / len(lejos)))
print("   proporcion del mapa por encima de 34 grados: %.1f%%"
      % (100.0 * sum(1 for s in lejos if s > 34) / len(lejos)))
