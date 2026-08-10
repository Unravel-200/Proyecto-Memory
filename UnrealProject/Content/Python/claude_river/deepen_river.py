"""Aumenta el calado del rio manteniendo la lamina de agua donde esta.

Se profundiza el lecho (metadato de profundidad por punto y channel_depth del
pincel), no se sube el nivel: asi el agua gana calado sin acercarse a la ribera.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")

FACTOR = 1.35          # +35 % de calado
CHANNEL_DEPTH = 580.0  # calado del canal que talla el pincel

plan = json.load(open(PLAN, encoding="utf-8"))
depth = [d * FACTOR for d in plan["depth"]]

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
landscape = [a for a in actors if isinstance(a, unreal.Landscape)][0]
comp = river.get_editor_property("water_body_component")

n = len(depth)
for i in range(n):
    comp.set_river_depth_at_spline_input_key(float(i), float(depth[i]))

cs = comp.get_editor_property("curve_settings")
cs.set_editor_property("channel_depth", CHANNEL_DEPTH)
comp.set_editor_property("curve_settings", cs)

# provocar el recalculo del pincel
sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
landscape.force_layers_full_update()

print("profundidad %.0f -> %.0f  (antes %.0f -> %.0f)"
      % (depth[0], depth[-1], plan["depth"][0], plan["depth"][-1]))
print("channel_depth del pincel: %.0f" % CHANNEL_DEPTH)

# guardar el nuevo perfil en el plan para que las verificaciones cuadren
plan["depth"] = depth
plan["bed"] = [plan["water"][i] - depth[i] for i in range(n)]
json.dump(plan, open(PLAN, "w"))
print("DEEPEN_OK")
