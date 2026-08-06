"""Aplica el plan del rio: reconstruye el spline y talla el cauce.

- El spline pasa a ir en un unico sentido, del tile 7_0_0 al 2_7_0, con cota
  estrictamente descendente.
- Anchura, profundidad y velocidad crecen/decrecen de forma coherente.
- El cauce se talla con ALandscape::EditorApplySpline por tramos, con el lecho
  por debajo de la lamina de agua y riberas que la contienen.

NO guarda: los cambios quedan en el editor para revisarlos.
"""

import json
import os

import unreal

PLAN = "C:/Users/jeffa/AppData/Local/Temp/claude/river_plan.json"
BACKUP = "C:/Users/jeffa/AppData/Local/Temp/claude/river_backup.json"

SEGMENTS = 8          # tramos de tallado (anchura/falloff interpolados en cada uno)
SUBDIV = 32           # subdivisiones por tramo
BED_FLAT_FRAC = 0.28  # semianchura plana del lecho, como fraccion de la anchura


def get_actors():
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    river = landscape = None
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.WaterBodyRiver):
            river = a
        elif isinstance(a, unreal.Landscape):
            landscape = a
    return river, landscape


def edit_layer_name(landscape):
    """Descubre el nombre de la capa de edicion de esculpido."""
    layers = landscape.get_edit_layers_bp()
    if not layers:
        return ""
    target = layers[0]
    for cand in ("Layer", "Layer0", "Base", "Sculpt", "Default"):
        if landscape.get_edit_layer_by_name_bp(cand) == target:
            return cand
    return "Layer"


def backup(river):
    if os.path.exists(BACKUP):
        print("copia de seguridad ya existente, no se sobrescribe ->", BACKUP)
        return
    spline = river.get_component_by_class(unreal.WaterSplineComponent)
    comp = river.get_editor_property("water_body_component")
    n = spline.get_number_of_spline_points()
    data = {
        "actor_location": [river.get_actor_location().x,
                           river.get_actor_location().y,
                           river.get_actor_location().z],
        "points_world": [],
        "width": [], "depth": [], "velocity": [],
    }
    for i in range(n):
        p = spline.get_location_at_spline_point(i, unreal.SplineCoordinateSpace.WORLD)
        data["points_world"].append([p.x, p.y, p.z])
        data["width"].append(comp.get_river_width_at_spline_input_key(float(i)))
        data["depth"].append(comp.get_river_depth_at_spline_input_key(float(i)))
        data["velocity"].append(comp.get_water_velocity_at_spline_input_key(float(i)))
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    with open(BACKUP, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    print("copia de seguridad del estado previo ->", BACKUP)


def rebuild_spline(river, plan):
    center = plan["center"]
    water = plan["water"]
    n = len(center)

    # el actor se coloca en el nacimiento: el punto 0 pasa a ser el origen
    origin = unreal.Vector(center[0][0], center[0][1], water[0])
    river.set_actor_location(origin, False, False)
    river.set_actor_rotation(unreal.Rotator(0, 0, 0), False)

    spline = river.get_component_by_class(unreal.WaterSplineComponent)
    pts = [unreal.Vector(center[i][0], center[i][1], water[i]) for i in range(n)]
    spline.set_spline_points(pts, unreal.SplineCoordinateSpace.WORLD, True)
    for i in range(n):
        spline.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)
    spline.update_spline() if hasattr(spline, "update_spline") else None
    print("spline reconstruido: %d puntos, longitud %.0f uu"
          % (spline.get_number_of_spline_points(), spline.get_spline_length()))
    return spline


def set_metadata(river, plan):
    comp = river.get_editor_property("water_body_component")
    n = len(plan["center"])
    for i in range(n):
        k = float(i)
        comp.set_river_width_at_spline_input_key(k, float(plan["width"][i]))
        comp.set_river_depth_at_spline_input_key(k, float(plan["depth"][i]))
        comp.set_water_velocity_at_spline_input_key(k, float(plan["velocity"][i]))
    print("metadatos aplicados: anchura %.0f->%.0f, profundidad %.0f->%.0f, "
          "velocidad %.0f->%.0f"
          % (plan["width"][0], plan["width"][-1],
             plan["depth"][0], plan["depth"][-1],
             plan["velocity"][0], plan["velocity"][-1]))


def carve(landscape, plan, layer):
    """Talla el cauce por tramos con un spline transitorio a cota de lecho."""
    center = plan["center"]
    water = plan["water"]
    bed = plan["bed"]
    width = plan["width"]
    depth = plan["depth"]
    n = len(center)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

    def half_flat(i):
        return width[i] * BED_FLAT_FRAC

    def falloff(i):
        # el talud alcanza la lamina de agua justo en el borde del cauce
        hw = width[i] * 0.5
        bank_over_bed = max(120.0, (water[i] - bed[i]) + 260.0)
        return max(200.0, (hw - half_flat(i)) * bank_over_bed / max(60.0, depth[i]))

    bounds = []
    for s in range(SEGMENTS):
        a = int(round(s * (n - 1) / SEGMENTS))
        b = int(round((s + 1) * (n - 1) / SEGMENTS))
        bounds.append((a, min(b + 1, n - 1)))   # solape de 1 punto

    for a, b in bounds:
        sp = unreal.new_object(unreal.SplineComponent, world)
        pts = [unreal.Vector(center[i][0], center[i][1], bed[i]) for i in range(a, b + 1)]
        sp.set_spline_points(pts, unreal.SplineCoordinateSpace.WORLD, True)
        for i in range(len(pts)):
            sp.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)
        landscape.editor_apply_spline(
            sp,
            start_width=half_flat(a), end_width=half_flat(b),
            start_side_falloff=falloff(a), end_side_falloff=falloff(b),
            start_roll=0.0, end_roll=0.0,
            num_subdivisions=SUBDIV,
            raise_heights=True, lower_heights=True,
            paint_layer=None, edit_layer_name=layer,
        )
        print("  tramo %2d-%2d  semiancho %6.0f->%6.0f  falloff %6.0f->%6.0f"
              % (a, b, half_flat(a), half_flat(b), falloff(a), falloff(b)))


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    river, landscape = get_actors()
    if river is None or landscape is None:
        print("ERROR: no encuentro el rio o el landscape")
        return

    backup(river)

    rebuild_spline(river, plan)
    set_metadata(river, plan)

    try:
        river.on_water_body_changed(True, False)
    except Exception as exc:  # noqa: BLE001
        print("aviso on_water_body_changed:", exc)

    layer = edit_layer_name(landscape)
    print("tallando el cauce en la capa de edicion '%s'..." % layer)
    carve(landscape, plan, layer)

    try:
        landscape.force_layers_full_update()
    except Exception as exc:  # noqa: BLE001
        print("aviso force_layers_full_update:", exc)

    print("APPLY_OK  (sin guardar: revisa en el editor)")


main()
