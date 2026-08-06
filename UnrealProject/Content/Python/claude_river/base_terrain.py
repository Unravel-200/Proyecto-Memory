"""Muestrea el terreno BASE (sin el tallado del rio) y restaura el estado.

Desactiva temporalmente affects_landscape del rio, fuerza el recalculo de las
capas de edicion del landscape, muestrea, y vuelve a dejarlo como estaba.
"""

import json
import os

import unreal

OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
MIN_XY = -50400.0
MAX_XY = 50400.0
N = 129

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
TRACE = unreal.TraceTypeQuery.ECC_VISIBILITY


def height_at(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world,
        unreal.Vector(x, y, 60000.0),
        unreal.Vector(x, y, -60000.0),
        TRACE,
        True,
        [],
        unreal.DrawDebugTrace.NONE,
        True,
    )
    if res is None:
        return None
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    if not d["blocking_hit"]:
        return None
    return float(d["impact_point"].z)


def sample_grid():
    stepv = (MAX_XY - MIN_XY) / (N - 1)
    out = []
    for iy in range(N):
        y = MIN_XY + iy * stepv
        out.append([
            (lambda z: None if z is None else round(z, 1))(
                height_at(MIN_XY + ix * stepv, y)
            )
            for ix in range(N)
        ])
    return out, stepv


def refresh(landscape, brush, river):
    try:
        river.on_water_body_changed()
    except Exception as exc:  # noqa: BLE001
        print("  on_water_body_changed:", exc)
    try:
        brush.force_update()
    except Exception as exc:  # noqa: BLE001
        print("  brush.force_update:", exc)
    try:
        landscape.force_layers_full_update()
    except Exception as exc:  # noqa: BLE001
        print("  force_layers_full_update:", exc)


def main():
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    river = landscape = brush = None
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.WaterBodyRiver):
            river = a
        elif isinstance(a, unreal.Landscape):
            landscape = a
        elif a.get_class().get_name() == "WaterBrushManager":
            brush = a

    try:
        layers = landscape.get_edit_layers_bp()
        print("EDIT_LAYERS:", [str(l) for l in layers])
    except Exception as exc:  # noqa: BLE001
        print("EDIT_LAYERS: <err>", exc)

    comp = river.get_editor_property("water_body_component")
    prev = comp.get_editor_property("affects_landscape")
    print("affects_landscape previo:", prev)

    # puntos testigo para verificar restauracion
    probes = [(46900, -48030), (13108, -19318), (-5527, 18302), (-23732, 50361),
              (20000, -30000), (0, 0)]
    before = [height_at(*p) for p in probes]

    grid = None
    try:
        comp.set_editor_property("affects_landscape", False)
        refresh(landscape, brush, river)
        grid, stepv = sample_grid()
    finally:
        comp.set_editor_property("affects_landscape", prev)
        refresh(landscape, brush, river)

    after = [height_at(*p) for p in probes]

    data = {
        "min_xy": MIN_XY,
        "max_xy": MAX_XY,
        "n": N,
        "step": (MAX_XY - MIN_XY) / (N - 1),
        "grid": grid,
        "probes": [
            {"xy": p, "before": b, "after": a, "delta": None if (b is None or a is None) else round(a - b, 2)}
            for p, b, a in zip(probes, before, after)
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh)

    print("BASE_OK ->", OUT)
    for pr in data["probes"]:
        print("  probe", pr["xy"], "before", pr["before"], "after", pr["after"], "delta", pr["delta"])


main()
