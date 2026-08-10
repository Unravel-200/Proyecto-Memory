import unreal

unreal.EditorLevelLibrary.load_level("/Game/Maps/L_Developer_Testing")
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    unreal.log("ACTOR label={} class={}".format(actor.get_actor_label(), actor.get_class().get_name()))
    if actor.get_actor_label() == "Gameplay_InteractableDoor":
        unreal.log("DOOR_FOUND class={} location={} collision={}".format(
            actor.get_class().get_name(), actor.get_actor_location(),
            actor.get_editor_property("root_component").get_collision_profile_name()))
