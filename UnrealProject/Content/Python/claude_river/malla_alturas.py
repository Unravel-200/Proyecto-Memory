# -*- coding: utf-8 -*-
"""Muestrea el terreno del campus en una rejilla de 10 m y lo guarda.

Con esto el resto del analisis (buscar sitio llano, medir desnivel bajo una
huella) se hace sin volver a trazar rayos, que es lo lento.
"""

import json
import os

import unreal

AQUI = os.path.dirname(os.path.abspath(__file__))
# Limite REAL del landscape: 8x8 LandscapeStreamingProxy de 126 m, medido
# directamente de sus actor bounds (diag_tiles.py). -560/440 (usado antes)
# salia de un calculo con loc+bounds mal combinado y colocaba el borde del
# mapa 43-56 m mas alla del landscape real por el lado oeste/sur -y por eso
# dos edificios terminaron con la mitad fuera del mapa.
PASO = 10.0
X0, X1 = -504.0, 504.0
Y0, Y1 = -504.0, 504.0

ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
MUNDO = ues.get_editor_world()

nx = int((X1 - X0) / PASO) + 1
ny = int((Y1 - Y0) / PASO) + 1
Z = []
for i in range(nx):
    x = X0 + i * PASO
    fila = []
    for j in range(ny):
        y = Y0 + j * PASO
        hit = unreal.SystemLibrary.line_trace_single(
            MUNDO, unreal.Vector(x * 100.0, y * 100.0, 100000.0),
            unreal.Vector(x * 100.0, y * 100.0, -100000.0),
            unreal.TraceTypeQuery.ECC_VISIBILITY, False, [],
            unreal.DrawDebugTrace.NONE, True,
            unreal.LinearColor.RED, unreal.LinearColor.GREEN, 0.0)
        fila.append(round(hit.to_dict()["impact_point"].z / 100.0, 2)
                    if hit else None)
    Z.append(fila)
    if i % 20 == 0:
        print("  fila %d de %d" % (i, nx))

ruta = os.path.join(AQUI, "malla_alturas.json")
with open(ruta, "w") as fh:
    json.dump({"paso": PASO, "x0": X0, "y0": Y0, "nx": nx, "ny": ny, "z": Z},
              fh)
vals = [v for f in Z for v in f if v is not None]
print("rejilla %d x %d, cotas %.1f .. %.1f m" % (nx, ny, min(vals), max(vals)))
print("-> %s" % ruta)
