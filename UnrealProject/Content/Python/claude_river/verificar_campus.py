# -*- coding: utf-8 -*-
"""Comprueba el campus colocado: solapes reales entre bounding boxes de los
actores, edificios flotando o hundidos mas de lo previsto, y cuantos actores
tiene cada carpeta. Solo lee.
"""

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
PREFIJO = "Campus_"


def main():
    actores = [a for a in eas.get_all_level_actors()
               if a.get_actor_label().startswith(PREFIJO)]
    grupos = {}
    for a in actores:
        base = a.get_actor_label().split("_")[1]
        b = grupos.setdefault(base, [])
        loc = a.get_actor_location()
        bnd = a.get_actor_bounds(False)
        c, ext = bnd[0], bnd[1]
        b.append((c.x - ext.x, c.y - ext.y, c.x + ext.x, c.y + ext.y))

    cajas = []
    for nombre, piezas in grupos.items():
        x0 = min(p[0] for p in piezas); y0 = min(p[1] for p in piezas)
        x1 = max(p[2] for p in piezas); y1 = max(p[3] for p in piezas)
        cajas.append((nombre, x0, y0, x1, y1))

    print("%d edificios, %d actores." % (len(cajas), len(actores)))
    solapes = 0
    for i in range(len(cajas)):
        for j in range(i + 1, len(cajas)):
            a, b = cajas[i], cajas[j]
            sx = min(a[3], b[3]) - max(a[1], b[1])
            sy = min(a[4], b[4]) - max(a[2], b[2])
            if sx > 0 and sy > 0:
                print("   ! %s y %s se solapan %.0f x %.0f cm"
                      % (a[0], b[0], sx, sy))
                solapes += 1
    print("solapes reales: %d" % solapes)


main()
