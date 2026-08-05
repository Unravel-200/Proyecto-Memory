import unreal
MAP = '/Game/Maps/L_Campus_Natural'
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP)
tools = unreal.AssetToolsHelpers.get_asset_tools()
folder = '/Game/Materials/LandscapeCampus'
for name in ('LI_Grass', 'LI_Soil', 'LI_Rock', 'LI_CreekTransition'):
    path = folder + '/' + name + '.' + name
    if unreal.load_object(None, path) is None:
        try:
            li = tools.create_asset(name, folder, unreal.LandscapeLayerInfoObject, unreal.LandscapeLayerInfoObjectFactory())
            li.set_editor_property('layer_name', unreal.Name(name.replace('LI_', '')))
        except Exception as e:
            unreal.log_warning('LayerInfo ' + name + ': ' + repr(e))
mat = unreal.load_object(None, folder + '/M_Landscape_Campus_Natural.M_Landscape_Campus_Natural')
if mat is None:
    mat = tools.create_asset('M_Landscape_Campus_Natural', folder, unreal.Material, unreal.MaterialFactoryNew())
    mel = unreal.MaterialEditingLibrary
    normal = mel.create_material_expression(mat, unreal.MaterialExpressionVertexNormalWS, -700, 0)
    up = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -700, 180); up.set_editor_property('Constant', unreal.LinearColor(0.0, 0.0, 1.0, 1.0))
    dot = mel.create_material_expression(mat, unreal.MaterialExpressionDotProduct, -500, 0); mel.connect_material_expressions(normal, '', dot, 'A'); mel.connect_material_expressions(up, '', dot, 'B')
    slope = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -300, 0); slope.set_editor_property('ConstB', -3.0); mel.connect_material_expressions(dot, '', slope, 'A')
    slope_bias = mel.create_material_expression(mat, unreal.MaterialExpressionAdd, -100, 0); slope_bias.set_editor_property('ConstB', 2.1); mel.connect_material_expressions(slope, '', slope_bias, 'A')
    grass = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 180); grass.set_editor_property('Constant', unreal.LinearColor(0.12, 0.30, 0.08, 1.0))
    rock = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 360); rock.set_editor_property('Constant', unreal.LinearColor(0.26, 0.22, 0.16, 1.0))
    lerp = mel.create_material_expression(mat, unreal.MaterialExpressionLinearInterpolate, 180, 160)
    mel.connect_material_expressions(grass, '', lerp, 'A'); mel.connect_material_expressions(rock, '', lerp, 'B'); mel.connect_material_expressions(slope_bias, '', lerp, 'Alpha')
    mel.connect_material_property(lerp, '', unreal.MaterialProperty.MP_BASE_COLOR)
    rough = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, 180, 380); rough.set_editor_property('R', 0.85); mel.connect_material_property(rough, '', unreal.MaterialProperty.MP_ROUGHNESS)
    mat.set_editor_property('two_sided', True); mel.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat)
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if isinstance(actor, unreal.Landscape):
        actor.set_editor_property('landscape_material', mat)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('CAMPUS_LANDSCAPE_MATERIAL_READY')
