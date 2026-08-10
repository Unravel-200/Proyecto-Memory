# -*- coding: utf-8 -*-
"""Comprueba que ningun actor Campus_* quede fuera del landscape real
(-504..504 en X e Y), midiendo su bounding box de verdad, no la teoria."""

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
LIM = 50400.0   # cm

fuera = 0
for a in eas.get_all_level_actors():
    lbl = a.get_actor_label()
    if not lbl.startswith("Campus_"):
        continue
    bnd = a.get_actor_bounds(False)
    c, ext = bnd[0], bnd[1]
    x0, y0, x1, y1 = c.x - ext.x, c.y - ext.y, c.x + ext.x, c.y + ext.y
    if x0 < -LIM or x1 > LIM or y0 < -LIM or y1 > LIM:
        print("   ! %s se sale del landscape: (%.0f,%.0f)..(%.0f,%.0f)"
              % (lbl, x0, y0, x1, y1))
        fuera += 1

print("%d actor(es) fuera del landscape real" % fuera)
