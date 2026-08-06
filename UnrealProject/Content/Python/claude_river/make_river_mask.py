"""Genera una mascara PNG del corredor del rio, en coordenadas del mundo.

Blanco dentro del cauce (lecho y paredes) y en la orilla proxima, con
degradado hacia fuera. El material la muestrea con la posicion del mundo, asi
que tine exactamente el rio: el fondo plano incluido, cosa que la pendiente
sola no puede hacer.

Se ejecuta con el python normal, fuera del editor.
"""

import json
import math
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
OUT = os.path.join(HERE, "T_RiverMask.png")

RES = 1024
MIN_XY, MAX_XY = -50400.0, 50400.0
EXTENT = MAX_XY - MIN_XY
CELL = EXTENT / RES

MARGEN_PLENO = 420.0     # blanco hasta aqui pasado el borde del cauce
MARGEN_FUNDIDO = 1500.0  # y se apaga a esta distancia

plan = json.load(open(PLAN, encoding="utf-8"))
c, width = plan["center"], plan["width"]
n = len(c)

grid = [[0] * RES for _ in range(RES)]


def dist_seg(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 <= 0 else max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy)), t


for i in range(n - 1):
    ax, ay = c[i]
    bx, by = c[i + 1]
    hw0, hw1 = width[i] * 0.5, width[i + 1] * 0.5
    alcance = max(hw0, hw1) + MARGEN_FUNDIDO
    # solo los texeles de la caja del segmento
    x0 = int((min(ax, bx) - alcance - MIN_XY) / CELL) - 1
    x1 = int((max(ax, bx) + alcance - MIN_XY) / CELL) + 1
    y0 = int((min(ay, by) - alcance - MIN_XY) / CELL) - 1
    y1 = int((max(ay, by) + alcance - MIN_XY) / CELL) + 1
    for iy in range(max(0, y0), min(RES, y1 + 1)):
        py = MIN_XY + (iy + 0.5) * CELL
        row = grid[iy]
        for ix in range(max(0, x0), min(RES, x1 + 1)):
            px = MIN_XY + (ix + 0.5) * CELL
            d, t = dist_seg(px, py, ax, ay, bx, by)
            hw = hw0 + (hw1 - hw0) * t
            pleno = hw + MARGEN_PLENO
            fuera = hw + MARGEN_FUNDIDO
            if d <= pleno:
                v = 255
            elif d < fuera:
                v = int(255 * (1.0 - (d - pleno) / (fuera - pleno)) ** 1.5)
            else:
                continue
            if v > row[ix]:
                row[ix] = v

# --- PNG en escala de grises, fila 0 = y minima ---
raw = b"".join(b"\x00" + bytes(grid[iy]) for iy in range(RES))


def chunk(tag, data):
    c_ = struct.pack(">I", len(data)) + tag + data
    return c_ + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", RES, RES, 8, 0, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(raw, 9))
       + chunk(b"IEND", b""))
open(OUT, "wb").write(png)

cubiertos = sum(1 for r in grid for v in r if v > 0)
print("mascara %dx%d  (%.0f uu por texel)" % (RES, RES, CELL))
print("texeles con tinte: %d de %d (%.1f%% del mapa)"
      % (cubiertos, RES * RES, 100.0 * cubiertos / (RES * RES)))
print("blancos plenos: %.1f%% del mapa"
      % (100.0 * sum(1 for r in grid for v in r if v == 255) / (RES * RES)))
print("->", OUT)
