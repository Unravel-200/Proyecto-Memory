"""Comprueba (a) el nuevo calado y (b) si la capa 'Tierra' se esta pintando."""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
comp = river.get_editor_property("water_body_component")


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


plan = json.load(open(PLAN, encoding="utf-8"))
c, water, depth = plan["center"], plan["water"], plan["depth"]
n = len(c)

print("=== CALADO ===")
print("  i     agua    lecho_real   calado real   calado pedido")
reales = []
for i in range(0, n, 3):
    z = h(c[i][0], c[i][1])
    real = (water[i] - z) if z is not None else 0.0
    reales.append(real)
    print("%3d %9.1f %11.1f %13.1f %15.1f" % (i, water[i], z, real, depth[i]))
print("  calado medido: %.0f -> %.0f uu" % (reales[0], reales[-1]))
print("  metadato del rio en la boca: %.0f uu"
      % comp.get_river_depth_at_spline_input_key(float(n - 1)))

print("\n=== CAPA DE TIERRA ===")
print("  target_layers:", [str(k) for k in land.get_editor_property("target_layers").keys()])
print("  get_target_layer_names:", [str(x) for x in land.get_target_layer_names()])

# buscar asignaciones de weightmap en los componentes de un proxy junto al rio
mid = c[n // 2]
best, bestd = None, 1e18
for a in actors:
    if isinstance(a, unreal.LandscapeStreamingProxy):
        d = math.dist((a.get_actor_location().x, a.get_actor_location().y), mid)
        if d < bestd:
            best, bestd = a, d
print("  proxy mas cercano al rio:", best.get_actor_label())
comps = best.get_components_by_class(unreal.LandscapeComponent)
print("  componentes de landscape:", len(comps))
for lc in comps[:3]:
    for p in ("weightmap_layer_allocations", "weightmap_layer_allocation_infos"):
        try:
            allocs = lc.get_editor_property(p)
            print("   ", p, "->", str(allocs)[:300])
            break
        except Exception:  # noqa: BLE001
            continue
