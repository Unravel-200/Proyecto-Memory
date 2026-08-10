"""Pone los edificios derechos y reexporta su geometria para recolocarlos.

Todas las mallas estan authorizadas con la altura en Z (es la dimension menor:
420-1020 uu, alturas de planta). Los que llevan pitch +-90 quedan de canto.
Se anula pitch y roll; al enderezarlos la huella cambia mucho, asi que hace
falta volver a calcular donde va cada uno.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "edificios_backup.json")
OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/edificios_derechos.json"

previo = {r["label"]: r for r in json.load(open(BACKUP, encoding="utf-8"))}

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
edificios = [a for a in actors if isinstance(a, unreal.StaticMeshActor)
             and a.get_actor_label().startswith("CampusBuilding_")]

print("%-28s %14s %-22s -> %-22s" %
      ("edificio", "pitch antes", "huella antes", "huella ahora"))
info = []
for a in sorted(edificios, key=lambda x: x.get_actor_label()):
    r = a.get_actor_rotation()
    _, ext0 = a.get_actor_bounds(False)
    antes = "%.0f x %.0f" % (ext0.x * 2, ext0.y * 2)
    pitch0 = r.pitch

    a.set_actor_rotation(unreal.Rotator(0.0, r.yaw, 0.0), False)

    loc = a.get_actor_location()
    origen, ext = a.get_actor_bounds(False)
    label = a.get_actor_label()
    # posicion que el usuario le habia dado originalmente
    orig = previo.get(label, {}).get("loc", [loc.x, loc.y, loc.z])
    info.append({
        "label": label,
        "deseada": [orig[0], orig[1]],
        "loc": [loc.x, loc.y, loc.z],
        "pivote_a_base": (origen.z - ext.z) - loc.z,
        "medio_x": ext.x,
        "medio_y": ext.y,
        "alto": ext.z * 2.0,
    })
    print("%-28s %14.0f %-22s -> %-22s"
          % (label[:28], pitch0, antes, "%.0f x %.0f" % (ext.x * 2, ext.y * 2)))

json.dump(info, open(OUT, "w"))
print("\n->", OUT)
