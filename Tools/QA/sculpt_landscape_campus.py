import unreal
MAP = '/Game/Maps/L_Campus_Landscape'
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
levels.load_level(MAP)
landscape = None
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if isinstance(actor, unreal.Landscape):
        landscape = actor
        break
if landscape is None:
    raise RuntimeError('No se encontro el Landscape nativo')
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
mat = unreal.load_object(None, '/Game/Materials/M_CampusLandscapeHeight.M_CampusLandscapeHeight')
if mat is None:
    mat = asset_tools.create_asset('M_CampusLandscapeHeight', '/Game/Materials', unreal.Material, unreal.MaterialFactoryNew())
    mel = unreal.MaterialEditingLibrary
    uv = mel.create_material_expression(mat, unreal.MaterialExpressionTextureCoordinate, -900, 0)
    u = mel.create_material_expression(mat, unreal.MaterialExpressionComponentMask, -700, -120)
    v = mel.create_material_expression(mat, unreal.MaterialExpressionComponentMask, -700, 160)
    u.set_editor_property('r', True); u.set_editor_property('g', False); u.set_editor_property('b', False); u.set_editor_property('a', False)
    v.set_editor_property('r', False); v.set_editor_property('g', True); v.set_editor_property('b', False); v.set_editor_property('a', False)
    mel.connect_material_expressions(uv, '', u, '')
    mel.connect_material_expressions(uv, '', v, '')
    um = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -500, -120); um.set_editor_property('ConstB', 5.0)
    vm = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -500, 160); vm.set_editor_property('ConstB', 4.0)
    mel.connect_material_expressions(u, '', um, 'A'); mel.connect_material_expressions(v, '', vm, 'A')
    us = mel.create_material_expression(mat, unreal.MaterialExpressionSine, -300, -120)
    vs = mel.create_material_expression(mat, unreal.MaterialExpressionSine, -300, 160)
    mel.connect_material_expressions(um, '', us, 'Input'); mel.connect_material_expressions(vm, '', vs, 'Input')
    waves = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -80, 40)
    mel.connect_material_expressions(us, '', waves, 'A'); mel.connect_material_expressions(vs, '', waves, 'B')
    waves_scale = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, 120, 40); waves_scale.set_editor_property('ConstB', 0.12)
    mel.connect_material_expressions(waves, '', waves_scale, 'A')
    uoff = mel.create_material_expression(mat, unreal.MaterialExpressionSubtract, -500, 420); uoff.set_editor_property('ConstB', 0.5); mel.connect_material_expressions(u, '', uoff, 'A')
    ab = mel.create_material_expression(mat, unreal.MaterialExpressionAbs, -300, 420); mel.connect_material_expressions(uoff, '', ab, 'Input')
    bank = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -80, 420); bank.set_editor_property('ConstB', 0.40); mel.connect_material_expressions(ab, '', bank, 'A')
    base = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, 120, 220); base.set_editor_property('R', 0.42)
    add = mel.create_material_expression(mat, unreal.MaterialExpressionAdd, 340, 180); mel.connect_material_expressions(base, '', add, 'A'); mel.connect_material_expressions(bank, '', add, 'B')
    add2 = mel.create_material_expression(mat, unreal.MaterialExpressionAdd, 560, 180); mel.connect_material_expressions(add, '', add2, 'A'); mel.connect_material_expressions(waves_scale, '', add2, 'B')
    mel.connect_material_property(add2, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mat.set_editor_property('two_sided', True); mel.recompile_material(mat)
rt = unreal.RenderingLibrary.create_render_target2d(None, 4033, 4033, unreal.TextureRenderTargetFormat.RTF_RGBA16F, unreal.LinearColor(0.42, 0.42, 0.42, 1.0), False)
unreal.RenderingLibrary.draw_material_to_render_target(None, rt, mat)
ok = landscape.landscape_import_heightmap_from_render_target(rt, False, 0)
if not ok:
    raise RuntimeError('No se pudo importar el heightmap al Landscape')
levels.save_current_level()
unreal.log('LANDSCAPE_CAMPUS_SCULPTED ' + MAP)
