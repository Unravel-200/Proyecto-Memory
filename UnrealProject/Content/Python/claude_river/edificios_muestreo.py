"""Copia de seguridad de los edificios y muestreo fino del terreno actual.

El muestreo se hace sobre el terreno YA tallado, para que la colocacion tenga
en cuenta el cauce.
"""

import json
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "edificios_backup.json")
GRID = "C:/Users/jeffa/AppData/Local/Temp/claude/terreno_actual.json"

N = 201
MIN_XY, MAX_XY = -50400.0, 50400.0

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
edificios = [a for a in actors if isinstance(a, unreal.StaticMeshActor)]
ignorar = [a for a in edificios]     # los edificios no deben tapar el trazado


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 80000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, ignorar,
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


# ---------- copia de seguridad ----------
if os.path.exists(BACKUP):
    print("copia ya existente, no se sobrescribe:", BACKUP)
else:
    data = []
    for a in edificios:
        loc, rot, esc = a.get_actor_location(), a.get_actor_rotation(), a.get_actor_scale3d()
        data.append({
            "label": a.get_actor_label(),
            "path": a.get_path_name(),
            "loc": [loc.x, loc.y, loc.z],
            "rot": [rot.pitch, rot.yaw, rot.roll],
            "escala": [esc.x, esc.y, esc.z],
        })
    json.dump(data, open(BACKUP, "w"), indent=1)
    print("copia de seguridad de %d actores -> %s" % (len(data), BACKUP))

# ---------- geometria de cada edificio ----------
info = []
for a in edificios:
    loc = a.get_actor_location()
    origen, extent = a.get_actor_bounds(False)
    comp = a.static_mesh_component
    mesh = comp.static_mesh if comp else None
    info.append({
        "label": a.get_actor_label(),
        "mesh": mesh.get_name() if mesh else None,
        "loc": [loc.x, loc.y, loc.z],
        "yaw": a.get_actor_rotation().yaw,
        # desfase del pivote a la base, constante al mover en XY
        "pivote_a_base": (origen.z - extent.z) - loc.z,
        "medio_x": extent.x,
        "medio_y": extent.y,
        "alto": extent.z * 2.0,
    })

# ---------- rejilla de terreno ----------
step = (MAX_XY - MIN_XY) / (N - 1)
grid = []
for iy in range(N):
    y = MIN_XY + iy * step
    grid.append([h(MIN_XY + ix * step, y) for ix in range(N)])

json.dump({"n": N, "step": step, "min_xy": MIN_XY, "grid": grid,
           "edificios": info}, open(GRID, "w"))
huecos = sum(1 for r in grid for v in r if v is None)
print("rejilla %dx%d (%.0f uu por celda), sin impacto en %d celdas"
      % (N, N, step, huecos))
print("->", GRID)
