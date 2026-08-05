import unreal
mat = unreal.load_object(None, '/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural.M_Landscape_Campus_Natural')
if mat is None:
    raise RuntimeError('No se encontro el material natural')
count = 0
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if isinstance(actor, unreal.LandscapeProxy):
        actor.set_editor_property('landscape_material', mat)
        count += 1
    if isinstance(actor, unreal.DirectionalLight):
        actor.light_component.set_intensity(8.0)
        actor.light_component.set_light_color(unreal.LinearColor(1.0, 0.96, 0.88, 1.0))
    if isinstance(actor, unreal.SkyLight):
        actor.light_component.set_intensity(1.5)
unreal.EditorLevelLibrary.save_current_level()
unreal.log('NATURAL_LANDSCAPE_VISUALS_FIXED proxies=' + str(count))
