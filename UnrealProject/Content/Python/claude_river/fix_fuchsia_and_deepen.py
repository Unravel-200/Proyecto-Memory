"""Arregla el fucsia, sube el calado y busca como tenir el lecho.

El fucsia: LinearInterpolate no acota el alpha, asi que con el umbral nuevo las
pendientes fuertes daban alpha de hasta 17 y el color se extrapolaba mucho mas
alla del cafe (verde negativo, rojo alto). Se mete un Clamp 0..1 en el alpha.
"""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"

D0, D1 = 180.0, 810.0     # nuevo calado: nacimiento -> desembocadura
CHANNEL_DEPTH = 810.0

mel = unreal.MaterialEditingLibrary
mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)


def by_class(name):
    return [e for e in mel.get_material_expressions(mat)
            if e.get_class().get_name() == "MaterialExpression" + name]


# ---------- 1) acotar el alpha ----------
if by_class("Clamp"):
    print("el material ya tiene el Clamp")
else:
    add = by_class("Add")[0]
    lerp = by_class("LinearInterpolate")[0]
    clamp = mel.create_material_expression(mat, unreal.MaterialExpressionClamp, -260, 240)
    for p, v in (("min_default", 0.0), ("max_default", 1.0)):
        try:
            clamp.set_editor_property(p, v)
        except Exception:  # noqa: BLE001
            pass
    mel.connect_material_expressions(add, "", clamp, "")
    mel.connect_material_expressions(clamp, "", lerp, "Alpha")
    mel.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(MAT_PATH, only_if_is_dirty=False)
    print("Clamp(0..1) insertado entre Add y el alpha del Lerp")
    print("nodos:", len(list(mel.get_material_expressions(mat))))

# ---------- 2) mas calado ----------
plan = json.load(open(PLAN, encoding="utf-8"))
acc, total = plan["acc"], plan["length"]
n = len(plan["center"])
depth = [D0 + (D1 - D0) * ((acc[i] / total) ** 0.75) for i in range(n)]

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
comp = river.get_editor_property("water_body_component")

for i in range(n):
    comp.set_river_depth_at_spline_input_key(float(i), float(depth[i]))
cs = comp.get_editor_property("curve_settings")
cs.set_editor_property("channel_depth", CHANNEL_DEPTH)
comp.set_editor_property("curve_settings", cs)

sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
land.force_layers_full_update()

plan["depth"] = depth
plan["bed"] = [plan["water"][i] - depth[i] for i in range(n)]
json.dump(plan, open(PLAN, "w"))
print("calado: %.0f -> %.0f uu   channel_depth=%.0f" % (depth[0], depth[-1], CHANNEL_DEPTH))

# ---------- 3) funciones de material del plugin Water ----------
ar = unreal.AssetRegistryHelpers.get_asset_registry()
fns = ar.get_assets_by_class(
    unreal.TopLevelAssetPath("/Script/Engine", "MaterialFunction"), True)
inter = [str(a.package_name) for a in fns
         if "/Water/" in str(a.package_name)
         and any(k in str(a.package_name).lower()
                 for k in ("info", "depth", "mask", "terrain", "landscape", "shore"))]
print("\nfunciones de material del plugin Water que podrian dar el lecho:")
for p in sorted(inter)[:25]:
    print("  ", p)
if not inter:
    print("   ninguna con esos nombres")
