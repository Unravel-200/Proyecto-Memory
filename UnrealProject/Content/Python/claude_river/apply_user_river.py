"""Aplica el rio sobre EL RECORRIDO DEL USUARIO usando el pincel de agua.

El pincel funciona en esta sesion, asi que el cauce se talla solo, de forma
procedural y no destructiva: no se esculpe el landscape a mano.

  1. spline con el trazado del usuario, sentido unico y cota descendente;
  2. anchura / profundidad / velocidad por punto;
  3. ajuste del pincel para dar al cauce el calado deseado;
  4. regeneracion de la malla de agua (sin esto la superficie se queda con la
     forma del spline anterior y no se ve agua).

No guarda nada.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")

# perfil del cauce que hay que reproducir
CHANNEL_DEPTH = 420.0      # calado del canal bajo la lamina
CURVE_RAMP_WIDTH = 700.0   # anchura de la rampa de ribera
CHANNEL_EDGE_OFFSET = 0.0
FALLOFF_WIDTH = 1400.0     # fundido con el terreno de alrededor
FALLOFF_ANGLE = 45.0
EDGE_OFFSET = 256.0
Z_OFFSET = 16.0


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    center, water = plan["center"], plan["water"]
    width, depth, vel = plan["width"], plan["depth"], plan["velocity"]
    n = len(center)

    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
    landscape = [a for a in actors if isinstance(a, unreal.Landscape)][0]
    spline = river.get_component_by_class(unreal.WaterSplineComponent)
    comp = river.get_editor_property("water_body_component")

    print("estado previo: %d puntos, %.0f uu"
          % (spline.get_number_of_spline_points(), spline.get_spline_length()))

    # --- 1) spline ---
    river.set_actor_location(
        unreal.Vector(center[0][0], center[0][1], water[0]), False, False)
    river.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
    pts = [unreal.Vector(center[i][0], center[i][1], water[i]) for i in range(n)]
    spline.set_spline_points(pts, unreal.SplineCoordinateSpace.WORLD, True)
    for i in range(n):
        spline.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)

    # --- 2) metadatos ---
    for i in range(n):
        comp.set_river_width_at_spline_input_key(float(i), float(width[i]))
        comp.set_river_depth_at_spline_input_key(float(i), float(depth[i]))
        comp.set_water_velocity_at_spline_input_key(float(i), float(vel[i]))
    print("spline: %d puntos, %.0f uu   anchura %.0f->%.0f  prof %.0f->%.0f  vel %.0f->%.0f"
          % (spline.get_number_of_spline_points(), spline.get_spline_length(),
             width[0], width[-1], depth[0], depth[-1], vel[0], vel[-1]))

    # --- 3) forma del cauce que talla el pincel ---
    cs = comp.get_editor_property("curve_settings")
    cs.set_editor_property("channel_depth", CHANNEL_DEPTH)
    cs.set_editor_property("curve_ramp_width", CURVE_RAMP_WIDTH)
    cs.set_editor_property("channel_edge_offset", CHANNEL_EDGE_OFFSET)
    comp.set_editor_property("curve_settings", cs)

    hm = comp.get_editor_property("water_heightmap_settings")
    fo = hm.get_editor_property("falloff_settings")
    fo.set_editor_property("falloff_width", FALLOFF_WIDTH)
    fo.set_editor_property("falloff_angle", FALLOFF_ANGLE)
    fo.set_editor_property("edge_offset", EDGE_OFFSET)
    fo.set_editor_property("z_offset", Z_OFFSET)
    hm.set_editor_property("falloff_settings", fo)
    comp.set_editor_property("water_heightmap_settings", hm)

    comp.set_editor_property("affects_landscape", True)
    print("pincel: channel_depth %.0f  ramp %.0f  falloff %.0f"
          % (CHANNEL_DEPTH, CURVE_RAMP_WIDTH, FALLOFF_WIDTH))

    # --- 4) regenerar malla de agua y capas del landscape ---
    sd = float(comp.get_editor_property("shape_dilation"))
    comp.set_editor_property("shape_dilation", sd + 1.0)
    comp.set_editor_property("shape_dilation", sd)
    sm = river.get_components_by_class(unreal.SplineMeshComponent)
    print("malla de agua: %d SplineMesh (esperado %d)" % (len(sm), n - 1))

    try:
        landscape.force_layers_full_update()
    except Exception as exc:  # noqa: BLE001
        print("aviso:", exc)

    print("APPLY_OK  (sin guardar)")


main()
