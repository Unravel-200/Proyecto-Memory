import unreal

MAP = '/Game/Maps/L_Campus_Blockout'
unreal.EditorLevelLibrary.load_level(MAP)

actors = unreal.EditorLevelLibrary.get_all_level_actors()
for actor in actors:
    if actor.get_actor_label() in ('Campus_Sun', 'Campus_Sky'):
        unreal.EditorLevelLibrary.destroy_actor(actor)

sun = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.DirectionalLight,
    unreal.Vector(0.0, 0.0, 5000.0),
    unreal.Rotator(-45.0, -35.0, 0.0))
sun.set_actor_label('Campus_Sun')
sun.light_component.set_intensity(8.0)
sun.light_component.set_light_color(unreal.LinearColor(1.0, 0.95, 0.85, 1.0))
sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)

sky = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SkyLight,
    unreal.Vector(0.0, 0.0, 4000.0),
    unreal.Rotator(0.0, 0.0, 0.0))
sky.set_actor_label('Campus_Sky')
sky.light_component.set_intensity(1.5)
sky.light_component.set_light_color(unreal.LinearColor(0.65, 0.75, 1.0, 1.0))
sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)

unreal.EditorLevelLibrary.save_current_level()
