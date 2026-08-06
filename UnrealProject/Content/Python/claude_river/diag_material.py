"""Inspecciona el material del landscape para localizar como colorea taludes."""

import unreal

mat = unreal.EditorAssetLibrary.load_asset(
    "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural")
print("material:", mat, type(mat).__name__)

exprs = unreal.MaterialEditingLibrary.get_material_expressions(mat)
print("expresiones: %d" % len(exprs))
for e in exprs:
    cls = e.get_class().get_name()
    extra = ""
    try:
        if cls == "MaterialExpressionConstant":
            extra = "= %s" % e.get_editor_property("r")
        elif cls == "MaterialExpressionConstant3Vector":
            c = e.get_editor_property("constant")
            extra = "= (%.3f, %.3f, %.3f)" % (c.r, c.g, c.b)
        elif cls == "MaterialExpressionConstant4Vector":
            c = e.get_editor_property("constant")
            extra = "= (%.3f, %.3f, %.3f, %.3f)" % (c.r, c.g, c.b, c.a)
        elif cls in ("MaterialExpressionScalarParameter",
                     "MaterialExpressionVectorParameter",
                     "MaterialExpressionTextureSampleParameter2D",
                     "MaterialExpressionStaticSwitchParameter"):
            extra = "param '%s'" % e.get_editor_property("parameter_name")
        elif cls == "MaterialExpressionTextureSample":
            t = e.get_editor_property("texture")
            extra = "tex %s" % (t.get_name() if t else None)
        elif cls == "MaterialExpressionComment":
            extra = "// %s" % str(e.get_editor_property("text"))[:60]
        elif cls == "MaterialExpressionLandscapeLayerBlend":
            layers = e.get_editor_property("layers")
            extra = "capas: %s" % [l.get_editor_property("layer_name") for l in layers]
        elif cls == "MaterialExpressionLandscapeLayerSample":
            extra = "capa '%s'" % e.get_editor_property("parameter_name")
    except Exception as exc:  # noqa: BLE001
        extra = "<err %s>" % str(exc)[:40]
    print("  %-46s %s" % (cls, extra))
