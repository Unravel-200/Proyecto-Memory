"""Importa la mascara del rio y la conecta al material del landscape.

Resultado: cafe donde manda la pendiente (taludes) O donde manda la mascara
(lecho del cauce y orilla proxima). Asi el fondo plano del rio, que la
pendiente nunca podia coger, tambien queda cafe.
"""

import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "T_RiverMask.png")
TEX_PATH = "/Game/Materials/LandscapeCampus/T_RiverMask"
MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"
MIN_XY, EXTENT = -50400.0, 100800.0

# ---------- 1) importar la textura ----------
task = unreal.AssetImportTask()
task.set_editor_property("filename", PNG)
task.set_editor_property("destination_path", "/Game/Materials/LandscapeCampus")
task.set_editor_property("destination_name", "T_RiverMask")
task.set_editor_property("automated", True)
task.set_editor_property("replace_existing", True)
task.set_editor_property("save", True)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

tex = unreal.EditorAssetLibrary.load_asset(TEX_PATH)
print("textura:", tex)
for p, v in (("srgb", False),
             ("compression_settings", unreal.TextureCompressionSettings.TC_MASKS),
             ("address_x", unreal.TextureAddress.TA_CLAMP),
             ("address_y", unreal.TextureAddress.TA_CLAMP)):
    try:
        tex.set_editor_property(p, v)
    except Exception as exc:  # noqa: BLE001
        print("  %s: %s" % (p, str(exc)[:70]))
unreal.EditorAssetLibrary.save_asset(TEX_PATH, only_if_is_dirty=False)

# ---------- 2) material ----------
mel = unreal.MaterialEditingLibrary
mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)


def by_class(name):
    return [e for e in mel.get_material_expressions(mat)
            if e.get_class().get_name() == "MaterialExpression" + name]


if by_class("TextureSample"):
    print("el material ya tiene la mascara conectada")
else:
    clamp = by_class("Clamp")[0]
    lerp = by_class("LinearInterpolate")[0]

    wp = mel.create_material_expression(mat, unreal.MaterialExpressionWorldPosition, -1100, 460)
    mask_rg = mel.create_material_expression(mat, unreal.MaterialExpressionComponentMask, -900, 460)
    mask_rg.set_editor_property("r", True)
    mask_rg.set_editor_property("g", True)
    mask_rg.set_editor_property("b", False)
    mask_rg.set_editor_property("a", False)

    add = mel.create_material_expression(mat, unreal.MaterialExpressionAdd, -740, 460)
    add.set_editor_property("const_b", -MIN_XY)

    div = mel.create_material_expression(mat, unreal.MaterialExpressionDivide, -600, 460)
    div.set_editor_property("const_b", EXTENT)

    ts = mel.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -440, 460)
    ts.set_editor_property("texture", tex)
    try:
        ts.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
    except Exception as exc:  # noqa: BLE001
        print("  sampler_type:", str(exc)[:70])

    mx = mel.create_material_expression(mat, unreal.MaterialExpressionMax, -240, 320)

    mel.connect_material_expressions(wp, "", mask_rg, "")
    mel.connect_material_expressions(mask_rg, "", add, "")
    mel.connect_material_expressions(add, "", div, "")
    mel.connect_material_expressions(div, "", ts, "UVs")
    mel.connect_material_expressions(clamp, "", mx, "A")
    mel.connect_material_expressions(ts, "R", mx, "B")
    mel.connect_material_expressions(mx, "", lerp, "Alpha")

    mel.recompile_material(mat)
    print("material: alpha = max(pendiente, mascara del rio)")

unreal.EditorAssetLibrary.save_asset(MAT_PATH, only_if_is_dirty=False)
print("nodos del material:", len(list(mel.get_material_expressions(mat))))
print("MASK_OK")
