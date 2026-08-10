"""Fuerza la regeneracion de la malla de agua del rio.

La edicion del spline desde Python no dispara el PostEditChange del componente,
asi que las mallas de superficie se quedaron con la forma del spline anterior.
Aqui se provoca ese PostEditChange tocando propiedades del componente.
"""

import unreal

river = [a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
         .get_all_level_actors() if isinstance(a, unreal.WaterBodyRiver)][0]
comp = river.get_editor_property("water_body_component")
spline = river.get_component_by_class(unreal.WaterSplineComponent)


def report(tag):
    sm = river.get_components_by_class(unreal.SplineMeshComponent)
    vis = sum(1 for c in sm if c.get_editor_property("visible"))
    print("  [%s] puntos spline=%d  SplineMesh=%d  visibles=%d"
          % (tag, spline.get_number_of_spline_points(), len(sm), vis))
    return len(sm), vis


report("inicio")

# 1) reenviar los puntos del spline por la ruta que marca el componente sucio
try:
    spline.update_spline()
    print("  update_spline() ok")
except Exception as exc:  # noqa: BLE001
    print("  update_spline:", exc)

# 2) provocar PostEditChangeProperty en el componente de agua
sd = comp.get_editor_property("shape_dilation")
comp.set_editor_property("shape_dilation", float(sd) + 1.0)
comp.set_editor_property("shape_dilation", float(sd))
print("  shape_dilation reenviado (%.1f)" % sd)
report("tras shape_dilation")

# 3) idem con una propiedad de forma del cuerpo de agua
for prop in ("max_wave_height_offset", "collision_height_offset"):
    try:
        v = comp.get_editor_property(prop)
        comp.set_editor_property(prop, float(v) + 1.0)
        comp.set_editor_property(prop, float(v))
        print("  %s reenviado" % prop)
    except Exception as exc:  # noqa: BLE001
        print("  %s: %s" % (prop, str(exc)[:70]))
report("tras offsets")

# 4) reenviar la transformada del actor (dispara PostEditMove)
loc = river.get_actor_location()
river.set_actor_location(unreal.Vector(loc.x + 1.0, loc.y, loc.z), False, False)
river.set_actor_location(loc, False, False)
print("  transformada reenviada")
n, v = report("tras mover")

# 5) si sigue sin verse, activar la malla estatica del cuerpo de agua
if v == 0:
    try:
        comp.set_water_body_static_mesh_enabled(True)
        print("  set_water_body_static_mesh_enabled(True)")
    except Exception as exc:  # noqa: BLE001
        print("  static mesh enable:", str(exc)[:90])
    report("tras static mesh")
