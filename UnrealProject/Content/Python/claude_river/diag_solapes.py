# -*- coding: utf-8 -*-
"""Vuelca la caja real (loc + bounds) de cada actor de dos edificios, para
entender por que verificar_campus.py los reporta solapados."""

import sys

import unreal

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
nombres = sys.argv[1:] or ["Medicina", "Soda"]

for a in eas.get_all_level_actors():
    lbl = a.get_actor_label()
    if not lbl.startswith("Campus_"):
        continue
    base = lbl.split("_")[1]
    if base not in nombres:
        continue
    loc = a.get_actor_location()
    rot = a.get_actor_rotation()
    bnd = a.get_actor_bounds(False)
    c, ext = bnd[0], bnd[1]
    print("%-32s loc=(%7.0f,%7.0f,%7.0f) yaw=%5.0f  bbox=(%7.0f,%7.0f)..(%7.0f,%7.0f)"
          % (lbl, loc.x, loc.y, loc.z, rot.yaw,
             c.x - ext.x, c.y - ext.y, c.x + ext.x, c.y + ext.y))
