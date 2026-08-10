# -*- coding: utf-8 -*-
"""Comprueba el trazado del campus contra el terreno ANTES de colocar nada.

Por cada edificio mide, sobre la huella girada: el desnivel del terreno, la
cota que le tocaria, cuanto habria que rebajar y rellenar, y su distancia al
rio. Ademas busca solapes entre edificios y con la plaza.

Solo lee. No coloca ni modifica nada.
"""

import json
import math
import os
import sys

import unreal

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import campus_trazado
import importlib
importlib.reload(campus_trazado)          # la sesion de Unreal cachea modulos
from campus_trazado import TRAZADO, PLAZA, RIO, HOLGURA_RIO, SEPARACION

ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
MUNDO = ues.get_editor_world()


def suelo(x, y):
    """Cota del terreno en (x, y), en metros. None si no hay terreno."""
    hit = unreal.SystemLibrary.line_trace_single(
        MUNDO, unreal.Vector(x * 100.0, y * 100.0, 100000.0),
        unreal.Vector(x * 100.0, y * 100.0, -100000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, False, [],
        unreal.DrawDebugTrace.NONE, True,
        unreal.LinearColor.RED, unreal.LinearColor.GREEN, 0.0)
    return hit.to_dict()["impact_point"].z / 100.0 if hit else None


def huella(x, y, w, h, yaw):
    """Semiejes de la huella girada: (mitad en X, mitad en Y)."""
    c, s = abs(math.cos(math.radians(yaw))), abs(math.sin(math.radians(yaw)))
    return (w * c + h * s) / 2.0, (w * s + h * c) / 2.0


def dist_rio(x, y):
    m = 1e18
    for i in range(len(RIO) - 1):
        ax, ay = RIO[i]
        bx, by = RIO[i + 1]
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L))
        m = min(m, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return m


def medir(nombre, x, y, ax, ay):
    """Muestrea el terreno bajo la huella cada 5 m."""
    zs = []
    n = 0
    px = -ax
    while px <= ax + 1e-6:
        py = -ay
        while py <= ay + 1e-6:
            z = suelo(x + px, y + py)
            if z is not None:
                zs.append(z)
            n += 1
            py += 5.0
        px += 5.0
    return zs, n


def main():
    dims = json.load(open(os.path.join(AQUI, "edificios_importados.json")))
    tam = {}
    for r in dims:
        clave = r["activo"].split("/")[-1].split(".")[0]
        act = "_".join(clave.split("_")[:3]).replace("SM_Building_", "")
        e = tam.setdefault(act, [1e9, 1e9, -1e9, -1e9])
        e[0] = min(e[0], r["min"][0]); e[1] = min(e[1], r["min"][1])
        e[2] = max(e[2], r["max"][0]); e[3] = max(e[3], r["max"][1])

    print("%-16s %6s %6s %7s %7s %7s %7s %6s" %
          ("edificio", "ancho", "fondo", "desnivel", "cota", "rebaje",
           "relleno", "a rio"))
    cajas, avisos = [], []
    for activo, nombre, x, y, yaw, zona in TRAZADO:
        t = tam[activo]
        w, h = (t[2] - t[0]) / 100.0, (t[3] - t[1]) / 100.0
        ax, ay = huella(x, y, w, h, yaw)
        zs, n = medir(nombre, x, y, ax, ay)
        if not zs:
            avisos.append("%s: sin terreno debajo" % nombre)
            continue
        zs.sort()
        cota = zs[int(len(zs) * 0.60)]          # 60 % del terreno queda debajo
        rebaje = max(zs) - cota
        relleno = cota - min(zs)
        dr = min(dist_rio(x + sx * ax, y + sy * ay)
                 for sx in (-1, 1) for sy in (-1, 1))
        print("%-16s %6.1f %6.1f %7.1f %7.1f %7.1f %7.1f %6.0f" %
              (nombre, w, h, max(zs) - min(zs), cota, rebaje, relleno, dr))
        if dr < HOLGURA_RIO:
            avisos.append("%s: a %.0f m del rio (minimo %.0f)"
                          % (nombre, dr, HOLGURA_RIO))
        cajas.append((nombre, x - ax, y - ay, x + ax, y + ay))

    px, py, pl = PLAZA
    cajas.append(("PLAZA", px - pl / 2, py - pl / 2, px + pl / 2, py + pl / 2))
    for i in range(len(cajas)):
        for j in range(i + 1, len(cajas)):
            a, b = cajas[i], cajas[j]
            sx = min(a[3], b[3]) - max(a[1], b[1])
            sy = min(a[4], b[4]) - max(a[2], b[2])
            if sx > -SEPARACION and sy > -SEPARACION:
                avisos.append("%s y %s se pisan o quedan a menos de %.0f m"
                              % (a[0], b[0], SEPARACION))

    print()
    if avisos:
        print("%d AVISO(S):" % len(avisos))
        for a in avisos:
            print("   ! %s" % a)
    else:
        print("Trazado limpio: nada se pisa, nada invade el rio.")


main()
