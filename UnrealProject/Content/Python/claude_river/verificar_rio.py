# -*- coding: utf-8 -*-
"""Distancia real de cada edificio colocado al spline del rio, medida en el
propio Unreal (no contra la copia de puntos en campus_trazado.py)."""

import math

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
PREFIJO = "Campus_"

pts = None
for a in eas.get_all_level_actors():
    if "WaterBodyRiver" in a.get_class().get_name():
        spl = a.get_component_by_class(unreal.WaterSplineComponent)
        if spl:
            n = spl.get_number_of_spline_points()
            pts = [spl.get_location_at_spline_point(
                       i, unreal.SplineCoordinateSpace.WORLD)
                   for i in range(n)]
            break

if not pts:
    print("no se encontro el rio")
else:
    grupos = {}
    for a in eas.get_all_level_actors():
        lbl = a.get_actor_label()
        if not lbl.startswith(PREFIJO) or "Basamento" in lbl:
            continue
        base = lbl.split("_")[1]
        bnd = a.get_actor_bounds(False)
        c, ext = bnd[0], bnd[1]
        b = grupos.setdefault(base, [1e18, 1e18, -1e18, -1e18])
        b[0] = min(b[0], c.x - ext.x); b[1] = min(b[1], c.y - ext.y)
        b[2] = max(b[2], c.x + ext.x); b[3] = max(b[3], c.y + ext.y)

    def dmin(x0, y0, x1, y1):
        m = 1e18
        for i in range(len(pts) - 1):
            for t100 in range(0, 101, 20):
                t = t100 / 100.0
                px = pts[i].x + (pts[i + 1].x - pts[i].x) * t
                py = pts[i].y + (pts[i + 1].y - pts[i].y) * t
                cx = min(max(px, x0), x1)
                cy = min(max(py, y0), y1)
                m = min(m, math.hypot(px - cx, py - cy))
        return m

    print("%-16s %8s" % ("edificio", "a rio (m)"))
    peor = None
    for nombre, b in sorted(grupos.items()):
        d = dmin(*b) / 100.0
        print("%-16s %8.1f" % (nombre, d))
        if peor is None or d < peor[1]:
            peor = (nombre, d)
    print("\nmas cercano: %s a %.1f m" % peor)
