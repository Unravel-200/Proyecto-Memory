"""Refina el rio sobre el eje ya aplicado, sin moverlo lateralmente.

Corrige los dos defectos medidos:
  1. el cauce plano era mas estrecho que la lamina de agua -> el terreno
     recortaba el rio por los bordes;
  2. el nacimiento caia en la cumbre, donde el terreno se desploma por los
     flancos y no contiene el agua -> se recorta la cabecera hasta el primer
     punto realmente encajonado.

Como el eje no cambia, el nuevo tallado sobrescribe el anterior en el mismo
corredor y no deja cicatriz.
"""

import json
import math
import os

import unreal

BASE = "C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/river_plan_final.json"

FREEBOARD = 190.0
BANK_MIN = 260.0
MIN_SLOPE = 0.0025
MAX_CUT = 950.0
SEGMENTS = 8
SUBDIV = 32
BANK_OFFSETS = (300.0, 900.0, 1600.0)   # se mide la ribera a varias distancias

D = json.load(open(BASE, encoding="utf-8"))
G, N, STEP, MINXY = D["grid"], D["n"], D["step"], D["min_xy"]


def terrain(x, y):
    """Terreno natural (antes de tallar), del muestreo previo."""
    fx, fy = (x - MINXY) / STEP, (y - MINXY) / STEP
    ix = max(0, min(N - 2, int(fx)))
    iy = max(0, min(N - 2, int(fy)))
    tx, ty = fx - ix, fy - iy
    a = G[iy][ix] * (1 - tx) + G[iy][ix + 1] * tx
    b = G[iy + 1][ix] * (1 - tx) + G[iy + 1][ix + 1] * tx
    return a * (1 - ty) + b * ty


def get_actors():
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    river = landscape = None
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.WaterBodyRiver):
            river = a
        elif isinstance(a, unreal.Landscape):
            landscape = a
    return river, landscape


def perp(c, i):
    a = c[i - 1] if i > 0 else c[i]
    b = c[i + 1] if i < len(c) - 1 else c[i]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty)
    return (-ty / L, tx / L) if L > 1e-6 else (0.0, 1.0)


def river_width(u):
    return 380.0 + (2350.0 - 380.0) * (u ** 0.62)


def river_depth(u):
    return 95.0 + (430.0 - 95.0) * (u ** 0.75)


def build_profile(center):
    n = len(center)
    acc = [0.0]
    for i in range(1, n):
        acc.append(acc[-1] + math.dist(center[i - 1], center[i]))
    total = acc[-1]

    width = [river_width(acc[i] / total) for i in range(n)]
    depth = [river_depth(acc[i] / total) for i in range(n)]
    terr = [terrain(x, y) for x, y in center]

    # ribera: el punto mas bajo de las dos margenes a varias distancias
    bank = []
    for i in range(n):
        nx, ny = perp(center, i)
        hw = width[i] * 0.5
        vals = []
        for extra in BANK_OFFSETS:
            o = hw + extra
            vals.append(terrain(center[i][0] + nx * o, center[i][1] + ny * o))
            vals.append(terrain(center[i][0] - nx * o, center[i][1] - ny * o))
        bank.append(min(vals))

    cap = [min(terr[i] - FREEBOARD, bank[i] - BANK_MIN) for i in range(n)]
    water = []
    for i in range(n):
        water.append(cap[i] if i == 0
                     else min(cap[i], water[-1] - MIN_SLOPE * (acc[i] - acc[i - 1])))
    for _ in range(80):
        for i in range(1, n - 1):
            cand = 0.5 * (water[i - 1] + water[i + 1])
            lo = water[i + 1] + MIN_SLOPE * (acc[i + 1] - acc[i])
            hi = water[i - 1] - MIN_SLOPE * (acc[i] - acc[i - 1])
            if lo > hi:
                continue
            top = min(hi, cap[i])
            bot = max(lo, min(top, terr[i] - MAX_CUT))
            water[i] = (max(bot, min(top, cand)) if bot <= top
                        else max(lo, min(hi, cand)))

    bed = [water[i] - depth[i] for i in range(n)]
    vel = []
    for i in range(n):
        grad = 0.0 if i == 0 else (water[i - 1] - water[i]) / max(1.0, acc[i] - acc[i - 1])
        vel.append(max(80.0, min(340.0, 90.0 + 5200.0 * grad)))
    if n > 1:
        vel[0] = vel[1]
    for _ in range(3):
        vel = [vel[0]] + [0.25 * vel[i - 1] + 0.5 * vel[i] + 0.25 * vel[i + 1]
                          for i in range(1, n - 1)] + [vel[-1]]
    return dict(center=center, acc=acc, length=total, width=width, depth=depth,
                terrain=terr, bank=bank, water=water, bed=bed, velocity=vel)


def main():
    river, landscape = get_actors()
    spline = river.get_component_by_class(unreal.WaterSplineComponent)
    n0 = spline.get_number_of_spline_points()
    center = []
    for i in range(n0):
        p = spline.get_location_at_spline_point(i, unreal.SplineCoordinateSpace.WORLD)
        center.append([p.x, p.y])
    print("eje leido del editor: %d puntos" % len(center))

    # 1) recortar la cabecera hasta el primer punto con ribera suficiente
    p = build_profile(center)
    start = 0
    for i in range(len(center)):
        if p["bank"][i] - p["water"][i] >= BANK_MIN - 1.0:
            start = i
            break
    # ademas exigir que el nacimiento este encajonado, no en un espolon
    while start < len(center) - 4:
        nx, ny = perp(center, start)
        hw = p["width"][start] * 0.5
        z0 = p["terrain"][start]
        flanks = [terrain(center[start][0] + s * nx * (hw + 900.0),
                          center[start][1] + s * ny * (hw + 900.0)) for s in (1, -1)]
        if min(flanks) > z0 - 120.0:
            break
        print("  descarto el punto %d como nacimiento: flanco %.0f uu por debajo"
              % (start, z0 - min(flanks)))
        start += 1

    if start:
        print("cabecera recortada: el rio nace en el punto %d %s"
              % (start, center[start]))
        center = center[start:]
    p = build_profile(center)

    n = len(center)
    print("longitud %.0f uu (%.2f km)  desnivel %.0f uu  pendiente %.2f%%"
          % (p["length"], p["length"] / 1e5, p["water"][0] - p["water"][-1],
             100.0 * (p["water"][0] - p["water"][-1]) / p["length"]))
    print("ribera minima sobre el agua: %.0f uu"
          % min(p["bank"][i] - p["water"][i] for i in range(n)))

    # 2) reconstruir el spline con el perfil corregido
    origin = unreal.Vector(center[0][0], center[0][1], p["water"][0])
    river.set_actor_location(origin, False, False)
    pts = [unreal.Vector(center[i][0], center[i][1], p["water"][i]) for i in range(n)]
    spline.set_spline_points(pts, unreal.SplineCoordinateSpace.WORLD, True)
    for i in range(n):
        spline.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)

    comp = river.get_editor_property("water_body_component")
    for i in range(n):
        comp.set_river_width_at_spline_input_key(float(i), float(p["width"][i]))
        comp.set_river_depth_at_spline_input_key(float(i), float(p["depth"][i]))
        comp.set_water_velocity_at_spline_input_key(float(i), float(p["velocity"][i]))
    print("spline: %d puntos, longitud %.0f uu" % (n, spline.get_spline_length()))

    # 3) re-tallar: el lecho plano ha de ser algo mas ancho que la lamina
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    layer = "Layer"
    for cand in ("Layer", "Layer0", "Base"):
        if landscape.get_edit_layer_by_name_bp(cand) == landscape.get_edit_layers_bp()[0]:
            layer = cand
            break

    def half_flat(i):
        return p["width"][i] * 0.5 + 120.0

    def falloff(i):
        # el talud alcanza la lamina a "shore" del borde del cauce
        shore = 0.22 * p["width"][i] * 0.5 + 200.0
        rise = max(150.0, p["bank"][i] - p["bed"][i])
        return max(260.0, min(2200.0, shore * rise / max(60.0, p["depth"][i])))

    bounds = []
    for s in range(SEGMENTS):
        a = int(round(s * (n - 1) / SEGMENTS))
        b = int(round((s + 1) * (n - 1) / SEGMENTS))
        bounds.append((a, min(b + 1, n - 1)))

    print("re-tallando el cauce en la capa '%s'..." % layer)
    for a, b in bounds:
        sp = unreal.new_object(unreal.SplineComponent, world)
        pl = [unreal.Vector(center[i][0], center[i][1], p["bed"][i]) for i in range(a, b + 1)]
        # prolongar los extremos para que el tallado no se quede corto
        if a == 0:
            d = unreal.Vector(pl[0].x - pl[1].x, pl[0].y - pl[1].y, pl[0].z - pl[1].z)
            L = math.hypot(d.x, d.y) or 1.0
            pl.insert(0, unreal.Vector(pl[0].x + d.x / L * 400, pl[0].y + d.y / L * 400,
                                       pl[0].z + d.z / L * 400))
        if b == n - 1:
            d = unreal.Vector(pl[-1].x - pl[-2].x, pl[-1].y - pl[-2].y, pl[-1].z - pl[-2].z)
            L = math.hypot(d.x, d.y) or 1.0
            pl.append(unreal.Vector(pl[-1].x + d.x / L * 800, pl[-1].y + d.y / L * 800,
                                    pl[-1].z + d.z / L * 800))
        sp.set_spline_points(pl, unreal.SplineCoordinateSpace.WORLD, True)
        for i in range(len(pl)):
            sp.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)
        landscape.editor_apply_spline(
            sp, start_width=half_flat(a), end_width=half_flat(b),
            start_side_falloff=falloff(a), end_side_falloff=falloff(b),
            start_roll=0.0, end_roll=0.0, num_subdivisions=SUBDIV,
            raise_heights=True, lower_heights=True,
            paint_layer=None, edit_layer_name=layer)
        print("  tramo %2d-%2d  semiancho %6.0f->%6.0f  falloff %6.0f->%6.0f"
              % (a, b, half_flat(a), half_flat(b), falloff(a), falloff(b)))

    try:
        landscape.force_layers_full_update()
    except Exception as exc:  # noqa: BLE001
        print("aviso:", exc)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(p, open(OUT, "w"))
    print("REFINE_OK ->", OUT)


main()
