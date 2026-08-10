"""Borra los edificios del campus, dejando antes una copia que permite recrearlos.

La copia previa (edificios_backup.json) solo guardaba transformadas; esta
guarda ademas la malla de cada actor, que es lo que hace falta para volver a
crearlos si hiciera falta.

Los cubos RavineBuffer_* no se tocan: no son edificios.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
COPIA = os.path.join(HERE, "edificios_borrados.json")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()
objetivo = [a for a in actors if isinstance(a, unreal.StaticMeshActor)
            and a.get_actor_label().startswith("CampusBuilding_")]
otros = [a for a in actors if isinstance(a, unreal.StaticMeshActor)
         and not a.get_actor_label().startswith("CampusBuilding_")]

datos = []
for a in objetivo:
    loc, rot, esc = a.get_actor_location(), a.get_actor_rotation(), a.get_actor_scale3d()
    comp = a.static_mesh_component
    mesh = comp.static_mesh if comp else None
    mats = []
    if comp:
        for i in range(comp.get_num_materials()):
            m = comp.get_material(i)
            mats.append(m.get_path_name() if m else None)
    datos.append({
        "label": a.get_actor_label(),
        "mesh": mesh.get_path_name() if mesh else None,
        "materiales": mats,
        "loc": [loc.x, loc.y, loc.z],
        "rot": [rot.pitch, rot.yaw, rot.roll],
        "escala": [esc.x, esc.y, esc.z],
        "movilidad": str(comp.get_editor_property("mobility")) if comp else None,
    })

json.dump(datos, open(COPIA, "w"), indent=1)
print("copia completa de %d edificios (con malla y materiales) -> %s"
      % (len(datos), COPIA))

borrados = 0
for a in objetivo:
    etiqueta = a.get_actor_label()
    if eas.destroy_actor(a):
        borrados += 1
        print("  borrado: %s" % etiqueta)
    else:
        print("  NO se pudo borrar: %s" % etiqueta)

print("\nborrados %d de %d edificios" % (borrados, len(objetivo)))
print("no tocados (%d):" % len(otros),
      ", ".join(a.get_actor_label() for a in otros))

restantes = [a for a in eas.get_all_level_actors()
             if isinstance(a, unreal.StaticMeshActor)
             and a.get_actor_label().startswith("CampusBuilding_")]
print("CampusBuilding_* que quedan en el mapa: %d" % len(restantes))
