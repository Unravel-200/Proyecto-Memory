import unreal

kept = 0; removed = 0
lighting_types = (unreal.DirectionalLight, unreal.SkyLight, unreal.PointLight, unreal.SpotLight, unreal.RectLight, unreal.ExponentialHeightFog)
for actor in list(unreal.EditorLevelLibrary.get_all_level_actors()):
    if isinstance(actor, lighting_types):
        kept += 1
    else:
        unreal.EditorLevelLibrary.destroy_actor(actor); removed += 1
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_MAP_EMPTY_KEEPING_LIGHTING kept=%d removed=%d' % (kept, removed))
