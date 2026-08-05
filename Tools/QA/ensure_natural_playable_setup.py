import unreal

actors = unreal.EditorLevelLibrary.get_all_level_actors()
starts = [a for a in actors if isinstance(a, unreal.PlayerStart)]
primary = next((a for a in starts if a.get_actor_label() == 'PlayerStart_Campus_Natural'), None)
if primary is None:
    primary = starts[0] if starts else unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-28000,-30000,650), unreal.Rotator(0,90,0))
primary.set_actor_label('PlayerStart_Campus_Natural')
primary.set_actor_location(unreal.Vector(-28000,-30000,650), False, False)
primary.set_actor_rotation(unreal.Rotator(0,90,0), False)
for start in starts:
    if start != primary:
        unreal.EditorLevelLibrary.destroy_actor(start)
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_PLAYABLE_SETUP_READY starts=1')
