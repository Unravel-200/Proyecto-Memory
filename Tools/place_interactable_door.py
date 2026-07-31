import unreal

LEVEL = "/Game/Maps/L_Developer_Testing"
unreal.EditorLevelLibrary.load_level(LEVEL)
door_class = unreal.load_class(None, "/Script/ProyectoMemoria.PMInteractableDoor")
if not door_class:
    raise RuntimeError("No se pudo cargar PMInteractableDoor")

for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_actor_label() == "Gameplay_InteractableDoor":
        unreal.EditorLevelLibrary.destroy_actor(actor)

door = unreal.EditorLevelLibrary.spawn_actor_from_class(
    door_class, unreal.Vector(-300, -500, 100), unreal.Rotator(0, 0, 0)
)
door.set_actor_label("Gameplay_InteractableDoor")
unreal.EditorLevelLibrary.save_current_level()
unreal.log("INTERACTABLE_DOOR_PLACED")
