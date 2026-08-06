"""Devuelve el actor del rio a su estado previo a la intervencion.

Restaura la transformada del actor, los puntos del spline y los metadatos
guardados en river_backup_estado_previo.json.

OJO: esto NO deshace el tallado del terreno. El esculpido se escribio en la
capa de edicion 'Layer' del landscape y no hay copia de las alturas previas.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "river_backup_estado_previo.json")

data = json.load(open(BACKUP, encoding="utf-8"))

river = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
         .get_all_level_actors() if isinstance(a, unreal.WaterBodyRiver)][0]
spline = river.get_component_by_class(unreal.WaterSplineComponent)
comp = river.get_editor_property("water_body_component")

loc = data["actor_location"]
river.set_actor_location(unreal.Vector(loc[0], loc[1], loc[2]), False, False)

pts = [unreal.Vector(p[0], p[1], p[2]) for p in data["points_world"]]
spline.set_spline_points(pts, unreal.SplineCoordinateSpace.WORLD, True)
for i in range(len(pts)):
    spline.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)

for i in range(len(pts)):
    comp.set_river_width_at_spline_input_key(float(i), float(data["width"][i]))
    comp.set_river_depth_at_spline_input_key(float(i), float(data["depth"][i]))
    comp.set_water_velocity_at_spline_input_key(float(i), float(data["velocity"][i]))

print("rio restaurado: %d puntos, longitud %.0f uu"
      % (spline.get_number_of_spline_points(), spline.get_spline_length()))
print("AVISO: el tallado del terreno no se revierte con esto.")
