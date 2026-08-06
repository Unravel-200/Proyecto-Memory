"""Inspección de estado del río de L_Campus_Natural.

Volcado no destructivo: no modifica nada, solo lee y escribe un JSON.
Se ejecuta dentro del editor con:  py ".../inspect_river.py"
"""

import json
import os

import unreal

OUT = os.environ.get(
    "CLAUDE_RIVER_OUT",
    "C:/Users/jeffa/AppData/Local/Temp/claude/river_state.json",
)


def safe(fn, default=None):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - volcado defensivo
        return "<err: %s>" % exc if default is None else default


def vec(v):
    if v is None:
        return None
    try:
        return [round(v.x, 2), round(v.y, 2), round(v.z, 2)]
    except Exception:  # noqa: BLE001
        return str(v)


def curve_points(curve):
    """FInterpCurveFloat -> lista de (in_val, out_val)."""
    if curve is None:
        return None
    try:
        return [
            [round(p.in_val, 3), round(p.out_val, 3)]
            for p in curve.points
        ]
    except Exception as exc:  # noqa: BLE001
        return "<err: %s>" % exc


def get_prop(obj, name):
    try:
        return obj.get_editor_property(name)
    except Exception:  # noqa: BLE001
        return None


def dump_spline(spline):
    n = spline.get_number_of_spline_points()
    pts = []
    for i in range(n):
        pts.append(
            {
                "i": i,
                "world": vec(
                    spline.get_location_at_spline_point(
                        i, unreal.SplineCoordinateSpace.WORLD
                    )
                ),
                "local": vec(
                    spline.get_location_at_spline_point(
                        i, unreal.SplineCoordinateSpace.LOCAL
                    )
                ),
                "arrive_tangent": vec(
                    spline.get_arrive_tangent_at_spline_point(
                        i, unreal.SplineCoordinateSpace.LOCAL
                    )
                ),
                "leave_tangent": vec(
                    spline.get_leave_tangent_at_spline_point(
                        i, unreal.SplineCoordinateSpace.LOCAL
                    )
                ),
                "type": str(
                    safe(lambda: spline.get_spline_point_type(i), "?")
                ),
                "dist": round(
                    spline.get_distance_along_spline_at_spline_point(i), 1
                ),
            }
        )
    return {
        "num_points": n,
        "length": round(spline.get_spline_length(), 1),
        "closed_loop": bool(safe(lambda: spline.is_closed_loop(), False)),
        "points": pts,
    }


def main():
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = eas.get_all_level_actors()

    state = {
        "engine": unreal.SystemLibrary.get_engine_version(),
        "world": str(
            safe(
                lambda: unreal.get_editor_subsystem(
                    unreal.UnrealEditorSubsystem
                )
                .get_editor_world()
                .get_name()
            )
        ),
        "total_actors_loaded": len(actors),
        "rivers": [],
        "water_zones": [],
        "landscapes": [],
        "landscape_brushes": [],
        "other_water": [],
    }

    for a in actors:
        cls = a.get_class().get_name()

        if isinstance(a, unreal.WaterBodyRiver):
            comp = get_prop(a, "water_body_component")
            spline = a.get_component_by_class(unreal.WaterSplineComponent)
            meta = None
            for cand in ("water_spline_metadata", "WaterSplineMetadata"):
                meta = get_prop(a, cand) or meta
            if meta is None and spline is not None:
                meta = get_prop(spline, "water_spline_metadata")

            entry = {
                "class": cls,
                "name": a.get_name(),
                "label": a.get_actor_label(),
                "path": a.get_path_name(),
                "location": vec(a.get_actor_location()),
                "rotation": str(a.get_actor_rotation()),
                "scale": vec(a.get_actor_scale3d()),
                "spline": dump_spline(spline) if spline else None,
                "metadata": {
                    "depth": curve_points(get_prop(meta, "depth")) if meta else None,
                    "width": curve_points(get_prop(meta, "river_width") or get_prop(meta, "width")) if meta else None,
                    "velocity": curve_points(get_prop(meta, "water_velocity_scalar") or get_prop(meta, "velocity")) if meta else None,
                    "audio": curve_points(get_prop(meta, "audio_intensity")) if meta else None,
                },
            }
            if comp:
                for p in (
                    "affects_landscape",
                    "water_height_map_settings",
                    "curve_settings",
                    "shape_dilation",
                    "max_wave_height_offset",
                    "target_wave_mask_depth",
                    "water_mesh_override",
                    "tessellation_factor",
                    "overlap_material_priority",
                    "channel_depth",
                    "river_to_lake_transition_material",
                    "river_to_ocean_transition_material",
                ):
                    v = get_prop(comp, p)
                    if v is not None:
                        entry["comp_" + p] = str(v)
            state["rivers"].append(entry)

        elif isinstance(a, unreal.WaterZone):
            state["water_zones"].append(
                {
                    "name": a.get_name(),
                    "label": a.get_actor_label(),
                    "location": vec(a.get_actor_location()),
                    "zone_extent": str(get_prop(a, "zone_extent")),
                    "render_target_resolution": str(
                        get_prop(a, "render_target_resolution")
                    ),
                    "capture_z_bounds": str(get_prop(a, "capture_z_bounds")),
                }
            )

        elif isinstance(a, unreal.Landscape):
            state["landscapes"].append(
                {
                    "name": a.get_name(),
                    "label": a.get_actor_label(),
                    "location": vec(a.get_actor_location()),
                    "scale": vec(a.get_actor_scale3d()),
                    "can_have_layers_content": str(
                        get_prop(a, "can_have_layers_content")
                    ),
                    "num_edit_layers": str(
                        safe(lambda: len(a.get_editor_property("landscape_layers")), "?")
                    ),
                }
            )

        elif "Brush" in cls and "Landscape" in cls:
            state["landscape_brushes"].append(
                {"class": cls, "name": a.get_name(), "label": a.get_actor_label()}
            )

        elif "Water" in cls:
            state["other_water"].append(
                {"class": cls, "name": a.get_name(), "label": a.get_actor_label()}
            )

    # Conteo de proxies de landscape cargados
    proxies = [
        a for a in actors if isinstance(a, unreal.LandscapeStreamingProxy)
    ]
    state["landscape_proxies_loaded"] = len(proxies)
    state["landscape_proxy_names"] = sorted(a.get_actor_label() for a in proxies)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    unreal.log("CLAUDE_RIVER_INSPECT_OK -> %s" % OUT)
    print("CLAUDE_RIVER_INSPECT_OK -> %s" % OUT)


main()
