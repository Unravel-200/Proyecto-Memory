"""Asienta cada edificio midiendo el terreno bajo su huella real.

Usar la cota maxima deja huecos en las esquinas bajas; usar la minima entierra
demasiado. Se toma el percentil 25 y se hunde un poco: el edificio queda
apoyado, con el borde ligeramente clavado en el suelo y sin huecos visibles.
"""

import unreal

EMPOTRE = 30.0     # cuanto se clava en el suelo
MUESTRAS = 5       # rejilla de trazados por huella

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
smas = [a for a in actors if isinstance(a, unreal.StaticMeshActor)]
edificios = [a for a in smas if a.get_actor_label().startswith("CampusBuilding_")]


def suelo(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 80000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, smas,
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


print("%-28s %10s %10s %9s %9s" %
      ("edificio", "z antes", "z despues", "desnivel", "ajuste"))
for a in edificios:
    loc = a.get_actor_location()
    origen, extent = a.get_actor_bounds(False)
    pivote_a_base = (origen.z - extent.z) - loc.z

    zs = []
    for i in range(MUESTRAS):
        for j in range(MUESTRAS):
            fx = -1.0 + 2.0 * i / (MUESTRAS - 1)
            fy = -1.0 + 2.0 * j / (MUESTRAS - 1)
            z = suelo(loc.x + fx * extent.x * 0.92, loc.y + fy * extent.y * 0.92)
            if z is not None:
                zs.append(z)
    if not zs:
        print("%-28s  sin terreno bajo la huella" % a.get_actor_label()[:28])
        continue
    zs.sort()
    p25 = zs[max(0, int(len(zs) * 0.25))]
    nz = p25 - EMPOTRE - pivote_a_base
    a.set_actor_location(unreal.Vector(loc.x, loc.y, nz), False, False)
    print("%-28s %10.1f %10.1f %9.0f %9.1f"
          % (a.get_actor_label()[:28], loc.z, nz, zs[-1] - zs[0], nz - loc.z))

print("\nASENTADO (sin guardar)")
