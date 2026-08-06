"""Mide el peso de la capa 'Tierra' dentro y fuera del cauce."""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
LAYER = "Mud"

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
proxies = [a for a in actors if isinstance(a, unreal.LandscapeStreamingProxy)]
comps = []
for p in proxies:
    comps.extend(p.get_components_by_class(unreal.LandscapeComponent))
print("componentes de landscape: %d" % len(comps))


def weight(x, y):
    """Peso de la capa en (x,y); prueba en todos los componentes cercanos."""
    loc = unreal.Vector(x, y, 0.0)
    best = None
    for lc in comps:
        try:
            w = lc.editor_get_paint_layer_weight_by_name_at_location(loc, LAYER)
        except Exception:  # noqa: BLE001
            continue
        if w is not None and w >= 0.0:
            if best is None or w > best:
                best = w
    return best


plan = json.load(open(PLAN, encoding="utf-8"))
c, width = plan["center"], plan["width"]
n = len(c)

print("\n  i    eje    borde   +600    +1500   +3000   (peso de '%s', 0..1)" % LAYER)
for i in range(0, n, 3):
    a = c[i - 1] if i > 0 else c[i]
    b = c[i + 1] if i < n - 1 else c[i]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1.0
    nx, ny = -ty / L, tx / L
    hw = width[i] * 0.5
    vals = []
    for off in (0.0, hw, hw + 600.0, hw + 1500.0, hw + 3000.0):
        w = weight(c[i][0] + nx * off, c[i][1] + ny * off)
        vals.append("  -  " if w is None else "%5.2f" % w)
    print("%3d  %s" % (i, "  ".join(vals)))

print("\nlejos del rio (esquinas del mapa):")
for p in ((-45000, -45000), (45000, 45000), (0, -45000)):
    w = weight(*p)
    print("   %-20s %s" % (str(p), "  -  " if w is None else "%.2f" % w))
