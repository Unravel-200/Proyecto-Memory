import unreal

def remove(label):
    for a in list(unreal.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label() == label:
            unreal.EditorLevelLibrary.destroy_actor(a)
def add(cls, label, loc, rot):
    remove(label)
    a = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, unreal.Vector(*loc), unreal.Rotator(*rot))
    a.set_actor_label(label)
    return a
sun = add(unreal.DirectionalLight, 'Natural_Sun', (0,0,5000), (-45,-35,0))
sun.light_component.set_intensity(8.0); sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
sky = add(unreal.SkyLight, 'Natural_Sky', (0,0,4000), (0,0,0))
sky.light_component.set_intensity(1.5); sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
add(unreal.ExponentialHeightFog, 'Natural_Atmosphere', (0,0,0), (0,0,0))
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_ONLY_LIGHTING_READY actors=3')
