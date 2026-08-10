import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
aligned = 0
prefixes = ('CampusBuilding_', 'Road_', 'Path_', 'Plaza_', 'BridgeMarker_', 'RavineBuffer_')
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if not actor.get_actor_label().startswith(prefixes):
        continue
    loc = actor.get_actor_location()
    origin, extent = actor.get_actor_bounds(False)
    start = unreal.Vector(loc.x, loc.y, 50000.0)
    end = unreal.Vector(loc.x, loc.y, -50000.0)
    try:
        hit = unreal.SystemLibrary.line_trace_single(world, start, end, unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [actor], unreal.DrawDebugTrace.NONE)
        if hit:
            bottom_offset = loc.z - (origin.z - extent.z)
            actor.set_actor_location(unreal.Vector(loc.x, loc.y, hit.location.z + bottom_offset), False, False)
            aligned += 1
    except Exception as e:
        unreal.log_warning('Ground align ' + actor.get_actor_label() + ': ' + repr(e))
if aligned == 0:
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label().startswith(prefixes):
            loc = actor.get_actor_location()
            actor.set_actor_location(unreal.Vector(loc.x, loc.y, 300.0), False, False)
            aligned += 1
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_BUILDINGS_ALIGNED=' + str(aligned))
