import unreal
for a in list(unreal.EditorLevelLibrary.get_all_level_actors()):
    if a.get_actor_label() == 'Natural_SkyAtmosphere':
        unreal.EditorLevelLibrary.destroy_actor(a)
sky = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
sky.set_actor_label('Natural_SkyAtmosphere')
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_LIGHTING_VISIBILITY_READY')
