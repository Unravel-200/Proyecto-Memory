"""Pone el cafe de tierra en las riberas bajando el umbral de pendiente.

Medido en el mapa:
  - riberas del rio: mediana 17 grados, p75 23, p90 29
  - resto del mapa: mediana 4, p90 10, p97 14 (solo 0.4% supera 22)

Se ajusta la mezcla del material para que el cafe entre a los 10 grados y sea
pleno a los 22: cubre la ribera y deja los llanos verdes.

Ademas se deshace el cableado de la capa pintada, que no llego a funcionar.
"""

import math

import unreal

MAT_PATH = "/Game/Materials/LandscapeCampus/M_Landscape_Campus_Natural"
ANG0, ANG1 = 10.0, 22.0        # grados: inicio y pleno del cafe
BASURA = ("/Game/Materials/LandscapeCampus/LayerInfo_Tierra",
          "/Game/Materials/LandscapeCampus/LayerInfo_TierraRibera")

c0 = math.cos(math.radians(ANG0))
c1 = math.cos(math.radians(ANG1))
MUL = -1.0 / (c0 - c1)
ADD = c0 / (c0 - c1)
print("alpha = %.2f + (%.2f)*cos(pendiente)   -> cafe de %.0f a %.0f grados"
      % (ADD, MUL, ANG0, ANG1))

mat = unreal.EditorAssetLibrary.load_asset(MAT_PATH)
mel = unreal.MaterialEditingLibrary
exprs = list(mel.get_material_expressions(mat))


def by_class(name):
    return [e for e in exprs if e.get_class().get_name() == "MaterialExpression" + name]


# --- 1) devolver la salida al lerp original y tirar el nodo de capa ---
lerp = by_class("LinearInterpolate")[0]
mel.connect_material_property(lerp, "", unreal.MaterialProperty.MP_BASE_COLOR)
mel.delete_unused_expressions(mat)
print("nodos tras limpiar:", len(list(mel.get_material_expressions(mat))))

# --- 2) nuevo umbral ---
mul = by_class("Multiply")[0]
add = by_class("Add")[0]
mul.set_editor_property("const_b", MUL)
add.set_editor_property("const_b", ADD)
mel.recompile_material(mat)
unreal.EditorAssetLibrary.save_asset(MAT_PATH, only_if_is_dirty=False)
print("material: multiply.b=%.2f  add.b=%.2f  (guardado)"
      % (mul.get_editor_property("const_b"), add.get_editor_property("const_b")))

# --- 3) deshacer el cableado de la capa pintada ---
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
brush = [a for a in actors if a.get_class().get_name() == "WaterBrushManager"][0]
comp = river.get_editor_property("water_body_component")

brush.set_editor_property("affect_weightmap", False)
brush.set_editor_property("affected_weightmap_layers", [])
lws = comp.get_editor_property("layer_weightmap_settings")
for k in [str(k) for k in lws.keys()]:
    try:
        del lws[k]
    except Exception:  # noqa: BLE001
        pass
tl = land.get_editor_property("target_layers")
for k in [str(k) for k in tl.keys()]:
    if k != "__LANDSCAPE_VISIBILITY__":
        try:
            del tl[k]
        except Exception:  # noqa: BLE001
            pass
print("pincel affect_weightmap =", brush.get_editor_property("affect_weightmap"))
print("target_layers:", [str(k) for k in
                         land.get_editor_property("target_layers").keys()])

for p in BASURA:
    if unreal.EditorAssetLibrary.does_asset_exist(p):
        unreal.EditorAssetLibrary.delete_asset(p)
        print("borrado:", p)

# --- 4) que color queda en cada pendiente ---
print("\n  pendiente   alpha   color")
for ang, etiqueta in ((4.1, "llanos (mediana del mapa)"),
                      (10.0, "p90 del mapa"),
                      (14.3, "p97 del mapa"),
                      (16.9, "ribera (mediana)"),
                      (23.3, "ribera (p75)"),
                      (28.7, "ribera (p90)"),
                      (45.0, "montana")):
    a = max(0.0, min(1.0, ADD + MUL * math.cos(math.radians(ang))))
    print("  %6.1f     %5.2f   %-28s %s"
          % (ang, a, etiqueta,
             "verde" if a < 0.15 else ("cafe" if a > 0.85 else "mezcla")))
print("\nSLOPE_OK")
