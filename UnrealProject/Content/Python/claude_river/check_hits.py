"""Que actor golpea el rayo en los puntos que se desvian."""

import unreal

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

probes = [(0, 0), (43712, -45424), (-22843, 46321), (16269, -47401), (20000, -30000)]

for x, y in probes:
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    if not d["blocking_hit"]:
        print("(%8d,%8d)  SIN IMPACTO" % (x, y))
        continue
    actor = d["hit_actor"]
    comp = d["hit_component"]
    name = "?"
    try:
        name = actor.get_actor_label() if actor else "None"
    except Exception:  # noqa: BLE001
        name = str(actor)
    print("(%8d,%8d)  z=%9.1f  actor=%-34s comp=%s"
          % (x, y, d["impact_point"].z, name,
             comp.get_class().get_name() if comp else "None"))

# multi trace: todo lo que hay en la vertical de (0,0)
print("\ntodo lo que hay en la vertical de (0,0):")
res = unreal.SystemLibrary.line_trace_multi(
    world, unreal.Vector(0, 0, 60000.0), unreal.Vector(0, 0, -60000.0),
    unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
    unreal.DrawDebugTrace.NONE, True)
hits = res[1] if isinstance(res, tuple) else res
for h in (hits or []):
    d = h.to_dict()
    a = d["hit_actor"]
    print("   z=%9.1f  %-34s %s"
          % (d["impact_point"].z,
             a.get_actor_label() if a else "None",
             d["hit_component"].get_class().get_name() if d["hit_component"] else ""))
