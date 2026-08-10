# -*- coding: utf-8 -*-
"""Levanta el estado del terreno de L_Campus_Natural para poder decidir donde
va cada edificio: extension del landscape, recorrido del rio, actores ya
colocados y una rejilla de alturas y pendientes.

Solo lee. Escribe un JSON al lado de este script.
"""

import json
import os

import unreal

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "campus_terreno.json")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
mundo = ues.get_editor_world()
actores = eas.get_all_level_actors()

datos = {"mapa": mundo.get_name(), "actores": {}, "rio": [], "landscape": {}}

# ---- inventario por clase ----
for a in actores:
    c = a.get_class().get_name()
    datos["actores"][c] = datos["actores"].get(c, 0) + 1

# ---- extension del landscape ----
xs, ys = [], []
for a in actores:
    if "LandscapeStreamingProxy" in a.get_class().get_name():
        o = a.get_actor_location()
        b = a.get_actor_bounds(False)
        xs += [o.x - b[1].x, o.x + b[1].x]
        ys += [o.y - b[1].y, o.y + b[1].y]
if xs:
    datos["landscape"] = {"x0": min(xs), "x1": max(xs),
                          "y0": min(ys), "y1": max(ys)}

# ---- recorrido del rio ----
for a in actores:
    if "WaterBodyRiver" in a.get_class().get_name():
        spl = a.get_component_by_class(unreal.WaterSplineComponent)
        if spl is None:
            continue
        n = spl.get_number_of_spline_points()
        pts = []
        for i in range(n):
            p = spl.get_location_at_spline_point(
                i, unreal.SplineCoordinateSpace.WORLD)
            pts.append([round(p.x, 1), round(p.y, 1), round(p.z, 1)])
        datos["rio"].append({"actor": a.get_actor_label(), "puntos": pts})

# ---- rejilla de alturas por trazado vertical ----
if datos["landscape"]:
    L = datos["landscape"]
    paso = 2000.0                      # 20 m
    rejilla = []
    x = L["x0"]
    while x <= L["x1"]:
        fila = []
        y = L["y0"]
        while y <= L["y1"]:
            ini = unreal.Vector(x, y, 100000.0)
            fin = unreal.Vector(x, y, -100000.0)
            hit = unreal.SystemLibrary.line_trace_single(
                mundo, ini, fin,
                unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [],
                unreal.DrawDebugTrace.NONE, True,
                unreal.LinearColor.RED, unreal.LinearColor.GREEN, 0.0)
            fila.append(round(hit.to_dict()["impact_point"].z, 1)
                        if hit else None)
            y += paso
        rejilla.append(fila)
        x += paso
    datos["rejilla"] = {"paso": paso, "x0": L["x0"], "y0": L["y0"],
                        "z": rejilla}

with open(SALIDA, "w") as fh:
    json.dump(datos, fh, indent=1)

print("mapa: %s" % datos["mapa"])
print("landscape: %s" % datos["landscape"])
print("rios: %d" % len(datos["rio"]))
for r in datos["rio"]:
    print("   %s  %d puntos" % (r["actor"], len(r["puntos"])))
print("clases con mas actores:")
for c, n in sorted(datos["actores"].items(), key=lambda k: -k[1])[:14]:
    print("   %-44s %d" % (c, n))
print("-> %s" % SALIDA)
