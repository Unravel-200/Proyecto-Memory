"""Devuelve los edificios a las posiciones que tenian antes de recolocarlos."""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "edificios_backup.json")

previo = {r["label"]: r for r in json.load(open(BACKUP, encoding="utf-8"))}
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()

n = 0
for a in actors:
    if not isinstance(a, unreal.StaticMeshActor):
        continue
    r = previo.get(a.get_actor_label())
    if r is None:
        continue
    a.set_actor_location(unreal.Vector(*r["loc"]), False, False)
    a.set_actor_rotation(unreal.Rotator(r["rot"][0], r["rot"][1], r["rot"][2]), False)
    a.set_actor_scale3d(unreal.Vector(*r["escala"]))
    n += 1
print("restaurados %d actores a su estado previo" % n)
