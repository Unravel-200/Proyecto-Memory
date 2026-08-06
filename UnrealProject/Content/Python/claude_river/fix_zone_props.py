"""Restaura los valores originales de la WaterZone.

Los structs que devuelve get_editor_property son referencias vivas: al mutarlos
para provocar un PostEditChange se perdieron los valores de partida. Aqui se
reponen explicitamente los que tenia el mapa al empezar.
"""

import unreal

ORIG_EXTENT = (100800.0, 100800.0)
ORIG_RT = (1024, 1024)
ORIG_LOC = (0.0, 0.0, 1765.625)

zone = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        .get_all_level_actors() if isinstance(a, unreal.WaterZone)][0]

zone.set_editor_property("zone_extent", unreal.Vector2D(*ORIG_EXTENT))
zone.set_editor_property("render_target_resolution", unreal.IntPoint(*ORIG_RT))
zone.set_actor_location(unreal.Vector(*ORIG_LOC), False, False)

e = zone.get_editor_property("zone_extent")
r = zone.get_editor_property("render_target_resolution")
print("zone_extent               = (%.0f, %.0f)" % (e.x, e.y))
print("render_target_resolution  = (%d, %d)" % (r.x, r.y))
print("location                  = %s" % zone.get_actor_location())
