import unreal

mat = unreal.load_object(None, '/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural.M_Landscape_Campus_Natural')
if mat is None:
    raise RuntimeError('No se encontro el material de Landscape existente')
count = 0
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if isinstance(actor, unreal.LandscapeProxy):
        actor.set_editor_property('landscape_material', mat)
        count += 1
unreal.EditorLevelLibrary.save_current_level()
unreal.log('LANDSCAPE_MATERIAL_ONLY_ASSIGNED proxies=%d' % count)
