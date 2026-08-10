"""Fuerza al landscape a releer las capas de pintura que declara su material.

get_target_layer_names() sale vacio aunque el material ya declara 'Tierra':
la lista de capas del landscape se construye al asignar el material, asi que
se reasigna para que la reconstruya.
"""

import unreal

MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"

land = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        .get_all_level_actors() if isinstance(a, unreal.Landscape)][0]
river = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
         .get_all_level_actors() if isinstance(a, unreal.WaterBodyRiver)][0]
comp = river.get_editor_property("water_body_component")

mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)
print("antes:", [str(x) for x in land.get_target_layer_names()])

land.set_editor_property("landscape_material", None)
land.set_editor_property("landscape_material", mat)
print("material reasignado:", land.get_editor_property("landscape_material"))

print("despues:", [str(x) for x in land.get_target_layer_names()])
print("target_layers:", [str(k) for k in land.get_editor_property("target_layers").keys()])

# volver a lanzar el pincel para que pinte la capa
sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
land.force_layers_full_update()
print("capas objetivo finales:", [str(x) for x in land.get_target_layer_names()])
