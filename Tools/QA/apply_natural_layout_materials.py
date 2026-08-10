import unreal
tools = unreal.AssetToolsHelpers.get_asset_tools(); mel = unreal.MaterialEditingLibrary
folder = '/Game/Materials/CampusLayout'
colors = {'M_CampusRoad': unreal.LinearColor(0.08,0.09,0.10,1), 'M_CampusPath': unreal.LinearColor(0.24,0.18,0.10,1), 'M_CampusPlaza': unreal.LinearColor(0.38,0.38,0.34,1), 'M_CampusBridge': unreal.LinearColor(0.10,0.22,0.30,1), 'M_CampusRavineBuffer': unreal.LinearColor(0.08,0.28,0.16,1)}
mats = {}
for name, color in colors.items():
    mat = unreal.load_object(None, folder+'/'+name+'.'+name)
    if mat is None:
        mat = tools.create_asset(name, folder, unreal.Material, unreal.MaterialFactoryNew())
        expr = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -200, 0); expr.set_editor_property('Constant', color); mel.connect_material_property(expr, '', unreal.MaterialProperty.MP_BASE_COLOR)
        mel.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat)
    mats[name] = mat
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    label = actor.get_actor_label(); mat = None
    if label.startswith('Road_'): mat = mats['M_CampusRoad']
    elif label.startswith('Path_'): mat = mats['M_CampusPath']
    elif label.startswith('Plaza_'): mat = mats['M_CampusPlaza']
    elif label.startswith('BridgeMarker_'): mat = mats['M_CampusBridge']
    elif label.startswith('RavineBuffer_'): mat = mats['M_CampusRavineBuffer']
    if mat and hasattr(actor, 'static_mesh_component'): actor.static_mesh_component.set_material(0, mat)
unreal.EditorLevelLibrary.save_current_level(); unreal.log('NATURAL_LAYOUT_MATERIALS_APPLIED')
