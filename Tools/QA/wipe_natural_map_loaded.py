import unreal

actors = unreal.EditorLevelLibrary.get_all_level_actors()
kept = 0; removed = 0
for actor in actors:
    if isinstance(actor, (unreal.Landscape, unreal.LandscapeProxy)):
        kept += 1
    else:
        unreal.EditorLevelLibrary.destroy_actor(actor); removed += 1
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_MAP_WIPED kept_landscape=%d removed=%d' % (kept, removed))
