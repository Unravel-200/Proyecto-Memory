"""Reconstruye las conexiones del material para saber que color va a cada lado."""

import unreal

mat = unreal.EditorAssetLibrary.load_asset(
    "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural")
exprs = list(unreal.MaterialEditingLibrary.get_material_expressions(mat))

ids = {}
for i, e in enumerate(exprs):
    cls = e.get_class().get_name().replace("MaterialExpression", "")
    tag = "%s#%d" % (cls, i)
    try:
        if cls == "Constant3Vector":
            c = e.get_editor_property("constant")
            tag += "(%.2f,%.2f,%.2f)" % (c.r, c.g, c.b)
        elif cls == "Constant":
            tag += "(%.3f)" % e.get_editor_property("r")
    except Exception:  # noqa: BLE001
        pass
    ids[e] = tag


def src(node, pin):
    try:
        inp = node.get_editor_property(pin)
    except Exception:  # noqa: BLE001
        return None
    if inp is None:
        return None
    try:
        ex = inp.get_editor_property("expression")
    except Exception:  # noqa: BLE001
        return None
    return ids.get(ex) if ex else None


PINS = {
    "DotProduct": ("a", "b"),
    "Multiply": ("a", "b"),
    "Add": ("a", "b"),
    "LinearInterpolate": ("a", "b", "alpha"),
}

print("conexiones:")
for e in exprs:
    cls = e.get_class().get_name().replace("MaterialExpression", "")
    pins = PINS.get(cls)
    if not pins:
        continue
    parts = []
    for p in pins:
        s = src(e, p)
        if s is None:
            # valor constante en el propio pin
            try:
                cv = e.get_editor_property("const_" + p)
                s = "const=%s" % cv
            except Exception:  # noqa: BLE001
                s = "-"
        parts.append("%s=%s" % (p, s))
    print("  %-28s  %s" % (ids[e], "  ".join(parts)))

print("\nsalida del material:")
for prop in ("base_color", "roughness", "metallic"):
    try:
        inp = mat.get_editor_property(prop)
        ex = inp.get_editor_property("expression")
        print("  %-12s <- %s" % (prop, ids.get(ex) if ex else None))
    except Exception as exc:  # noqa: BLE001
        print("  %-12s <err> %s" % (prop, str(exc)[:70]))
