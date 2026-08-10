import unreal

rows = []
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if not actor.get_actor_label().startswith('CampusBuilding_'):
        continue
    origin, extent = actor.get_actor_bounds(False)
    dim = extent * 2.0
    scale = actor.get_actor_scale3d()
    mesh = actor.static_mesh_component.static_mesh if hasattr(actor, 'static_mesh_component') else None
    path = mesh.get_path_name() if mesh else 'NONE'
    unreal.log('BUILDING_SCALE label=%s dims_cm=(%.1f,%.1f,%.1f) scale=(%.3f,%.3f,%.3f) mesh=%s' % (actor.get_actor_label(), dim.x, dim.y, dim.z, scale.x, scale.y, scale.z, path))
    rows.append((dim.x, dim.y, dim.z))
if rows:
    avg = tuple(sum(v[i] for v in rows)/len(rows) for i in range(3))
    unreal.log('BUILDING_SCALE_SUMMARY count=%d avg_cm=(%.1f,%.1f,%.1f)' % (len(rows), avg[0], avg[1], avg[2]))
else:
    unreal.log_warning('BUILDING_SCALE_SUMMARY count=0')
