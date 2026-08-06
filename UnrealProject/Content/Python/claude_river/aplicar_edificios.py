"""Aplica la colocacion calculada a los edificios del campus.

Solo toca los CampusBuilding_*: los cubos RavineBuffer se dejan como estaban.
Reversible con edificios_backup.json (ver restaurar_edificios.py).
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
COLOCACION = os.path.join(HERE, "edificios_colocacion.json")

plan = {r["label"]: r for r in json.load(open(COLOCACION, encoding="utf-8"))
        if r.get("ok")}

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
movidos = omitidos = 0
for a in actors:
    if not isinstance(a, unreal.StaticMeshActor):
        continue
    label = a.get_actor_label()
    if not label.startswith("CampusBuilding_"):
        omitidos += 1
        continue
    r = plan.get(label)
    if r is None:
        print("  sin colocacion para", label)
        continue
    antes = a.get_actor_location()
    a.set_actor_location(unreal.Vector(*r["loc"]), False, False)
    movidos += 1
    print("  %-28s z %8.1f -> %8.1f   xy %s"
          % (label[:28], antes.z, r["loc"][2],
             "igual" if r["desplazado"] == 0 else "movido %.0f uu" % r["desplazado"]))

print("\nedificios recolocados: %d   actores no tocados: %d" % (movidos, omitidos))
print("APLICADO (sin guardar)")
