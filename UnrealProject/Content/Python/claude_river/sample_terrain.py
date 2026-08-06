"""Muestreo de alturas del terreno por trazado de rayos. No modifica nada.

Uso:  py ".../sample_terrain.py"
Salida: C:/Users/jeffa/AppData/Local/Temp/claude/terrain_grid.json
"""

import json
import os

import unreal

OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/terrain_grid.json"

MIN_XY = -50400.0
MAX_XY = 50400.0
N = 129  # 129x129 -> paso de 787.5 uu

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
TRACE = unreal.TraceTypeQuery.ECC_VISIBILITY


def height_at(x, y):
    """Devuelve Z del terreno en (x, y) o None."""
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


def main():
    # --- info de capas de edicion del landscape ---
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    landscape = None
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.Landscape):
            landscape = a
            break

    layers = "<n/d>"
    for cand in ("edit_layers", "landscape_edit_layers", "layers"):
        try:
            v = landscape.get_editor_property(cand)
            layers = "%s = %s" % (cand, str(v)[:500])
            break
        except Exception:  # noqa: BLE001
            continue

    step = (MAX_XY - MIN_XY) / (N - 1)
    grid = []
    misses = 0
    for iy in range(N):
        y = MIN_XY + iy * step
        row = []
        for ix in range(N):
            x = MIN_XY + ix * step
            z = height_at(x, y)
            if z is None:
                misses += 1
                row.append(None)
            else:
                row.append(round(z, 1))
        grid.append(row)

    data = {
        "min_xy": MIN_XY,
        "max_xy": MAX_XY,
        "n": N,
        "step": step,
        "misses": misses,
        "edit_layers": layers,
        "grid": grid,  # grid[iy][ix], x = MIN + ix*step, y = MIN + iy*step
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    print("TERRAIN_OK ->", OUT, "misses=", misses, "layers=", layers[:200])


main()
