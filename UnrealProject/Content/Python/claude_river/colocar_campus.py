# -*- coding: utf-8 -*-
"""Coloca en L_Campus_Natural las envolventes de los 18 edificios.

Un actor por nivel, todos con la misma transformada y colgados del actor de
planta baja, para que el edificio se mueva como una pieza. Cada uno va a su
carpeta del World Outliner.

El pivote de las mallas es la esquina suroeste al nivel del suelo EN BLENDER,
pero el exportador FBX (axis_forward=-Z, axis_up=Y, la convencion estandar
Blender->Unreal) invierte el eje Y al cruzar a Unreal: el mesh importado se
extiende en Y local de -H a 0, no de 0 a H. Confirmado leyendo el bounding box
del mesh importado (edificios_importados.json): min Y = -5000, max Y = 0 para
un edificio de 50 m de fondo.

Esto tiene dos consecuencias, no una:
1. El CENTRO local de la huella esta en (W/2, -H/2), no en (W/2, H/2). La
   posicion del actor (su pivote) se calcula desde ahi.
2. La fachada -que en Blender mira al muro sur, en Y local = 0- termina en el
   extremo ALTO del rango [-H, 0], no en el bajo. Con yaw=0 la fachada mira a
   +Y (norte), no a -Y como parece intuitivo. campus_trazado.py ya tiene los
   yaw corregidos para que cada fachada mire a su avenida.

La cota de planta baja es el punto MAS ALTO del terreno bajo la huella, para
que ningun promontorio asome dentro del edificio; el desnivel que queda del
lado bajo lo resuelve un zocalo perimetral (ver basamento()).
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
from campus_trazado import TRAZADO

PREFIJO = "Campus_"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
MUNDO = ues.get_editor_world()


def suelo(x, y):
    hit = unreal.SystemLibrary.line_trace_single(
        MUNDO, unreal.Vector(x * 100.0, y * 100.0, 100000.0),
        unreal.Vector(x * 100.0, y * 100.0, -100000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, False, [],
        unreal.DrawDebugTrace.NONE, True,
        unreal.LinearColor.RED, unreal.LinearColor.GREEN, 0.0)
    return hit.to_dict()["impact_point"].z / 100.0 if hit else None


# La misma rejilla de 10 m que valido resolver_trazado.py: el editor no
# siempre tiene cargada la coleccion de una LandscapeStreamingProxy al hacer
# un trazado en vivo (el streaming depende de la vista de la camara), y eso
# dejaba huellas enteras sin un solo punto valido cerca del borde del mapa.
# Colocar desde la misma malla que decidio el trazado evita esa carrera y
# ademas es lo unico consistente con lo que ya se valido.
with open(os.path.join(AQUI, "malla_alturas.json")) as _fh:
    _M = json.load(_fh)
_Z, _P, _X0, _Y0 = _M["z"], _M["paso"], _M["x0"], _M["y0"]


def cota_de(x, y, ax, ay):
    """Cota de la planta baja y suelo minimo bajo la huella, en metros.

    Se toma el punto MAS ALTO del terreno: asi ningun trozo de loma asoma
    dentro del edificio. El hueco que queda del lado bajo lo cierra el
    basamento. Si la malla no tiene ningun punto en la huella (raro: solo
    pasa muy cerca del borde del landscape) se completa con un trazado en
    vivo como respaldo.
    """
    zs = []
    i0 = int(math.floor((x - ax - _X0) / _P))
    i1 = int(math.ceil((x + ax - _X0) / _P))
    j0 = int(math.floor((y - ay - _Y0) / _P))
    j1 = int(math.ceil((y + ay - _Y0) / _P))
    for i in range(max(0, i0), min(len(_Z), i1 + 1)):
        for j in range(max(0, j0), min(len(_Z[0]), j1 + 1)):
            v = _Z[i][j]
            if v is not None:
                zs.append(v)
    if not zs:
        px = -ax
        while px <= ax + 1e-6:
            py = -ay
            while py <= ay + 1e-6:
                z = suelo(x + px, y + py)
                if z is not None:
                    zs.append(z)
                py += 5.0
            px += 5.0
    if not zs:
        return None, 0.0, 0.0
    return max(zs), max(zs) - min(zs), min(zs)


def basamento(nombre, zona, cx, cy, ax, ay, cota, zmin, cajas):
    """Zocalo perimetral que resuelve el desnivel bajo el edificio.

    Es un anillo, no un bloque: por dentro de la huella estan los sotanos.
    Sobresale 3 m y baja 1 m por debajo del punto mas bajo del terreno, de
    modo que por el lado bajo hace de muro de contencion y por el alto queda
    enterrado.
    """
    m = 3.0
    z0, z1 = zmin - 1.0, cota
    if z1 - z0 < 0.35:
        return 0
    cubo = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    mat = unreal.EditorAssetLibrary.load_asset(
        "/Game/Materials/Campus/M_Concrete_Campus")
    tramos = [(cx, cy - ay - m / 2.0, 2 * (ax + m), m),
              (cx, cy + ay + m / 2.0, 2 * (ax + m), m),
              (cx - ax - m / 2.0, cy, m, 2 * ay),
              (cx + ax + m / 2.0, cy, m, 2 * ay)]
    for i, (px, py, sx, sy) in enumerate(tramos):
        act = eas.spawn_actor_from_object(
            cubo, unreal.Vector(px * 100.0, py * 100.0,
                                (z0 + z1) / 2.0 * 100.0),
            unreal.Rotator(0.0, 0.0, 0.0))
        act.set_actor_scale3d(unreal.Vector(sx, sy, z1 - z0))
        act.set_actor_label("%s%s_Basamento_%d" % (PREFIJO, nombre, i))
        act.set_folder_path("Campus/%s/%s" % (zona.capitalize(), nombre))
        smc = act.get_component_by_class(unreal.StaticMeshComponent)
        smc.set_material(0, mat)
        smc.set_mobility(unreal.ComponentMobility.STATIC)
        cajas.append(act)
    return len(tramos)


def limpiar():
    """Retira una colocacion anterior de este mismo script, envolventes y
    zocalos por igual: los dos llevan el mismo prefijo."""
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith(PREFIJO):
            eas.destroy_actor(a)
            n += 1
    return n


def main():
    dims = json.load(open(os.path.join(AQUI, "edificios_importados.json")))
    # activo -> {clave de nivel: ruta} y huella comun
    niveles, tam = {}, {}
    for r in dims:
        nombre = r["activo"].split("/")[-1].split(".")[0]
        partes = nombre.split("_")               # SM Building <Activo> <Nivel> A
        activo, clave = partes[2], partes[3]
        niveles.setdefault(activo, {})[clave] = r["activo"]
        e = tam.setdefault(activo, [1e9, 1e9, -1e9, -1e9])
        e[0] = min(e[0], r["min"][0]); e[1] = min(e[1], r["min"][1])
        e[2] = max(e[2], r["max"][0]); e[3] = max(e[3], r["max"][1])

    borrados = limpiar()
    if borrados:
        print("retirados %d actores de una colocacion anterior" % borrados)

    orden = ["S3", "S2", "S1", "N0", "N1", "N2", "N3", "N4", "N5", "NT"]
    informe = []
    for activo, nombre, cx, cy, yaw, zona in TRAZADO:
        t = tam[activo]
        w, h = (t[2] - t[0]) / 100.0, (t[3] - t[1]) / 100.0
        rad = math.radians(yaw)
        c, s = math.cos(rad), math.sin(rad)
        ax = (w * abs(c) + h * abs(s)) / 2.0
        ay = (w * abs(s) + h * abs(c)) / 2.0
        cota, desnivel, zmin = cota_de(cx, cy, ax, ay)
        if cota is None:
            print("   ! %s: sin terreno debajo, se omite" % nombre)
            continue

        # el pivote es la esquina (0,0); el centro LOCAL real es (w/2, -h/2)
        # por la inversion de Y del FBX (ver docstring del modulo)
        ox = (w / 2.0) * c - (-h / 2.0) * s
        oy = (w / 2.0) * s + (-h / 2.0) * c
        loc = unreal.Vector((cx - ox) * 100.0, (cy - oy) * 100.0, cota * 100.0)
        rot = unreal.Rotator(0.0, 0.0, yaw)

        raiz = None
        claves = sorted(niveles[activo],
                        key=lambda k: orden.index(k) if k in orden else 99)
        for clave in claves:
            malla = unreal.EditorAssetLibrary.load_asset(niveles[activo][clave])
            act = eas.spawn_actor_from_object(malla, loc, rot)
            act.set_actor_label("%s%s_%s" % (PREFIJO, nombre, clave))
            act.set_folder_path("Campus/%s/%s" % (zona.capitalize(), nombre))
            act.get_component_by_class(
                unreal.StaticMeshComponent).set_mobility(
                    unreal.ComponentMobility.STATIC)
            if clave == "N0" or raiz is None:
                raiz = act
            elif act is not raiz:
                act.attach_to_actor(raiz, "",
                                    unreal.AttachmentRule.KEEP_WORLD,
                                    unreal.AttachmentRule.KEEP_WORLD,
                                    unreal.AttachmentRule.KEEP_WORLD, False)
        zocalo = basamento(nombre, zona, cx, cy, ax, ay, cota, zmin, [])
        informe.append({"edificio": nombre, "zona": zona, "x": cx, "y": cy,
                        "yaw": yaw, "cota": cota, "desnivel": desnivel,
                        "zmin": zmin, "w": w, "h": h,
                        "niveles": len(claves), "basamento": zocalo})

    with open(os.path.join(AQUI, "campus_colocado.json"), "w") as fh:
        json.dump(informe, fh, indent=1)

    print("%-16s %-6s %8s %8s %5s %7s %9s %4s %4s"
          % ("edificio", "zona", "X", "Y", "yaw", "cota", "desnivel", "niv",
             "zocalo"))
    for r in informe:
        print("%-16s %-6s %8.0f %8.0f %5.0f %7.1f %9.1f %4d %6d"
              % (r["edificio"], r["zona"], r["x"], r["y"], r["yaw"],
                 r["cota"], r["desnivel"], r["niveles"], r["basamento"]))
    print("\n%d edificios, %d envolventes + %d piezas de zocalo."
          % (len(informe), sum(r["niveles"] for r in informe),
             sum(r["basamento"] for r in informe)))


main()
