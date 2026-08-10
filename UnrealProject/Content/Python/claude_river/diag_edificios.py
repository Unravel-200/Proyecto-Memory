"""Inventario de los edificios del mapa y su estado respecto al terreno."""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/edificios.json"

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 80000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    if not d["blocking_hit"]:
        return None, None
    a = d["hit_actor"]
    return float(d["impact_point"].z), (a.get_actor_label() if a else None)


plan = json.load(open(PLAN, encoding="utf-8"))
eje = plan["center"]
ancho = plan["width"]

smas = [a for a in actors if isinstance(a, unreal.StaticMeshActor)]
print("StaticMeshActor en el mapa: %d\n" % len(smas))

rows = []
for a in smas:
    loc = a.get_actor_location()
    comp = a.static_mesh_component
    mesh = comp.static_mesh if comp else None
    bmin, bmax = a.get_actor_bounds(False)
    # distancia al eje del rio
    dmin, idx = 1e18, 0
    for i, q in enumerate(eje):
        d = math.dist((loc.x, loc.y), q)
        if d < dmin:
            dmin, idx = d, i
    suelo, quien = h(loc.x, loc.y)
    rows.append({
        "label": a.get_actor_label(),
        "mesh": mesh.get_name() if mesh else None,
        "mesh_path": mesh.get_path_name() if mesh else None,
        "loc": [round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)],
        "rot": [round(a.get_actor_rotation().pitch, 1),
                round(a.get_actor_rotation().yaw, 1),
                round(a.get_actor_rotation().roll, 1)],
        "escala": [round(v, 3) for v in (a.get_actor_scale3d().x,
                                         a.get_actor_scale3d().y,
                                         a.get_actor_scale3d().z)],
        "tam": [round(bmax.x * 2, 0), round(bmax.y * 2, 0), round(bmax.z * 2, 0)],
        "base_z": round(bmin.z - bmax.z, 1),
        "suelo": None if suelo is None else round(suelo, 1),
        "suelo_es": quien,
        "dist_rio": round(dmin, 0),
        "margen_rio": round(dmin - ancho[idx] * 0.5, 0),
    })

rows.sort(key=lambda r: r["dist_rio"])
print("%-26s %-22s %26s %14s %9s %9s" %
      ("etiqueta", "malla", "posicion", "tamano XY", "suelo", "dist.rio"))
for r in rows:
    print("%-26s %-22s %26s %14s %9s %9s"
          % (r["label"][:26], str(r["mesh"])[:22],
             str(r["loc"]), "%.0fx%.0f" % (r["tam"][0], r["tam"][1]),
             r["suelo"], r["dist_rio"]))

print("\n=== problemas ===")
for r in rows:
    avisos = []
    if r["suelo"] is not None:
        dz = r["loc"][2] - r["suelo"]
        if dz > 300:
            avisos.append("flotando %.0f uu" % dz)
        elif dz < -300:
            avisos.append("enterrado %.0f uu" % -dz)
    if r["margen_rio"] < 0:
        avisos.append("DENTRO del cauce")
    elif r["margen_rio"] < 1500:
        avisos.append("a %.0f uu del borde del cauce" % r["margen_rio"])
    if avisos:
        print("  %-26s %s" % (r["label"][:26], "; ".join(avisos)))

json.dump(rows, open(OUT, "w"))
print("\n->", OUT)

print("\n=== mallas disponibles en el proyecto ===")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
for a in ar.get_assets_by_class(
        unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh"), True):
    p = str(a.package_name)
    if p.startswith("/Game"):
        print("  ", p)
