"""Verifica el resultado midiendo secciones transversales reales del terreno."""

import json
import math

import unreal

PLAN = "C:/Users/jeffa/AppData/Local/Temp/claude/river_plan_usuario.json"
OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/verify.json"

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


plan = json.load(open(PLAN, encoding="utf-8"))
c = plan["center"]
water = plan["water"]
bed = plan["bed"]
width = plan["width"]
n = len(c)

rows = []
worst_spill = None
worst_clip = None

for i in range(n):
    if i == 0:
        tx, ty = c[1][0] - c[0][0], c[1][1] - c[0][1]
    elif i == n - 1:
        tx, ty = c[-1][0] - c[-2][0], c[-1][1] - c[-2][1]
    else:
        tx, ty = c[i + 1][0] - c[i - 1][0], c[i + 1][1] - c[i - 1][1]
    L = math.hypot(tx, ty)
    nx, ny = -ty / L, tx / L

    hw = width[i] * 0.5
    offs = [0.0, hw * 0.5, hw, hw + 300.0, hw + 900.0, hw + 1600.0]
    prof = {}
    for o in offs:
        za = h(c[i][0] + nx * o, c[i][1] + ny * o)
        zb = h(c[i][0] - nx * o, c[i][1] - ny * o)
        prof[o] = (za, zb)

    center_z = prof[0.0][0]
    edge = [v for v in prof[hw] if v is not None]
    bank900 = [v for v in prof[hw + 900.0] if v is not None]
    bank1600 = [v for v in prof[hw + 1600.0] if v is not None]

    # el agua se sale si la ribera no la supera
    contain = min(bank900) - water[i] if bank900 else None
    # el agua queda cortada por el terreno si el borde del cauce esta por encima
    clip = max(edge) - water[i] if edge else None

    rows.append({
        "i": i, "water": water[i], "bed_plan": bed[i], "bed_real": center_z,
        "edge": edge, "bank900": bank900, "bank1600": bank1600,
        "contain": contain, "clip": clip, "half_width": hw,
    })
    if contain is not None and (worst_spill is None or contain < worst_spill[1]):
        worst_spill = (i, contain)
    if clip is not None and (worst_clip is None or clip > worst_clip[1]):
        worst_clip = (i, clip)

print("  i    agua   lecho_plan lecho_real  borde_cauce   ribera+900  contencion  recorte")
for r in rows:
    print("%3d %8.1f %10.1f %10.1f %12s %12s %10s %8s"
          % (r["i"], r["water"], r["bed_plan"],
             -9999 if r["bed_real"] is None else r["bed_real"],
             "/".join("%.0f" % v for v in r["edge"]) if r["edge"] else "-",
             "/".join("%.0f" % v for v in r["bank900"]) if r["bank900"] else "-",
             "%.0f" % r["contain"] if r["contain"] is not None else "-",
             "%.0f" % r["clip"] if r["clip"] is not None else "-"))

print("\nlecho: error medio %.1f uu"
      % (sum(abs(r["bed_real"] - r["bed_plan"]) for r in rows if r["bed_real"] is not None)
         / max(1, sum(1 for r in rows if r["bed_real"] is not None))))
print("contencion minima (ribera a +900 sobre el agua): punto %d, %.0f uu"
      % worst_spill)
print("recorte maximo (borde del cauce sobre el agua): punto %d, %.0f uu"
      % worst_clip)

json.dump(rows, open(OUT, "w"))
print("VERIFY_OK ->", OUT)
