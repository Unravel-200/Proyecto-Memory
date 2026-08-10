"""Por que los edificios se ven tumbados: rotaciones y dimensiones locales."""

import unreal

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
edificios = [a for a in actors if isinstance(a, unreal.StaticMeshActor)
             and a.get_actor_label().startswith("CampusBuilding_")]

print("%-28s %-22s %-24s %-26s" %
      ("edificio", "rotacion (P,Y,R)", "malla local (X,Y,Z)", "en el mundo (X,Y,Z)"))
for a in sorted(edificios, key=lambda x: x.get_actor_label()):
    r = a.get_actor_rotation()
    comp = a.static_mesh_component
    mesh = comp.static_mesh if comp else None
    local = "-"
    if mesh:
        b = mesh.get_bounding_box()
        local = "%.0f x %.0f x %.0f" % (b.max.x - b.min.x,
                                        b.max.y - b.min.y,
                                        b.max.z - b.min.z)
    _, ext = a.get_actor_bounds(False)
    print("%-28s %-22s %-24s %-26s"
          % (a.get_actor_label()[:28],
             "%.0f, %.0f, %.0f" % (r.pitch, r.yaw, r.roll),
             local,
             "%.0f x %.0f x %.0f" % (ext.x * 2, ext.y * 2, ext.z * 2)))

print("\nsi la dimension Z local es la menor de las tres, la malla esta tumbada")
