import unreal

def remove(label):
    for a in list(unreal.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label() == label:
            unreal.EditorLevelLibrary.destroy_actor(a)
remove('PlayerStart_NaturalCampus')
remove('NavBounds_NaturalCampus')
player = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0,0,1200), unreal.Rotator(0,0,0))
player.set_actor_label('PlayerStart_NaturalCampus')
nav = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
nav.set_actor_label('NavBounds_NaturalCampus'); nav.set_actor_scale3d(unreal.Vector(1000,1000,20))
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_PLAYABLE_BOUNDS_READY')
