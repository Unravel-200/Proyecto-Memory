"""Registra la capa 'Tierra' y hace que el pincel de agua la pinte en las riberas.

No toca el material (ya tiene el nodo LandscapeLayerWeight de la vez anterior)
y NO reasigna landscape_material: eso tumba el editor.
"""

import json
import math
import os

import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, "river_plan_usuario.json")
INFO_PATH = "/Game/Materials/LandscapeCampus/LayerInfo_Tierra"
LAYER = "Tierra"
BANK_FALLOFF = 1300.0
FINAL_OPACITY = 1.0

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
land = [a for a in actors if isinstance(a, unreal.Landscape)][0]
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
brush = [a for a in actors if a.get_class().get_name() == "WaterBrushManager"][0]
comp = river.get_editor_property("water_body_component")


def h(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


# ---------- 1) confirmar que el calado esta aplicado en el terreno ----------
plan = json.load(open(PLAN, encoding="utf-8"))
c, water, depth = plan["center"], plan["water"], plan["depth"]
n = len(c)
print("=== calado real ===")
for i in (6, 15, 24, n - 2):
    z = h(c[i][0], c[i][1])
    print("  punto %2d: agua %8.1f  lecho %8.1f  calado %6.1f  (pedido %6.1f)"
          % (i, water[i], z, water[i] - z, depth[i]))

# ---------- 2) registrar la capa ----------
info = unreal.EditorAssetLibrary.load_asset(INFO_PATH)
print("\ncapa:", info.get_path_name() if info else "NO EXISTE")

tl = land.get_editor_property("target_layers")
if LAYER not in [str(k) for k in tl.keys()]:
    st = unreal.LandscapeTargetLayerSettings()
    st.set_editor_property("layer_info_obj", info)
    tl[LAYER] = st          # el mapa es referencia viva
print("target_layers:", [str(k) for k in
                         land.get_editor_property("target_layers").keys()])

# ---------- 3) que el pincel la pinte ----------
ws = unreal.WaterBodyWeightmapSettings()
ws.set_editor_property("falloff_width", BANK_FALLOFF)
ws.set_editor_property("edge_offset", 0.0)
ws.set_editor_property("final_opacity", FINAL_OPACITY)
lws = comp.get_editor_property("layer_weightmap_settings")
lws[LAYER] = ws
try:
    comp.set_editor_property("layer_weightmap_settings", lws)
except Exception:  # noqa: BLE001
    pass

brush.set_editor_property("affect_weightmap", True)
brush.set_editor_property("affected_weightmap_layers", [LAYER])
print("pincel: affect_weightmap=%s capas=%s"
      % (brush.get_editor_property("affect_weightmap"),
         [str(x) for x in brush.get_editor_property("affected_weightmap_layers")]))

sd = float(comp.get_editor_property("shape_dilation"))
comp.set_editor_property("shape_dilation", sd + 1.0)
comp.set_editor_property("shape_dilation", sd)
land.force_layers_full_update()

# ---------- 4) comprobar que hay weightmap asignado ----------
mid = c[n // 2]
best, bestd = None, 1e18
for a in actors:
    if isinstance(a, unreal.LandscapeStreamingProxy):
        loc = a.get_actor_location()
        d = math.dist((loc.x, loc.y), mid)
        if d < bestd:
            best, bestd = a, d
print("\nproxy junto al rio:", best.get_actor_label())
lcs = best.get_components_by_class(unreal.LandscapeComponent)
print("propiedades de LandscapeComponent con 'weight':",
      [p for p in dir(lcs[0]) if "weight" in p.lower()])
for lc in lcs[:2]:
    for p in ("weightmap_layer_allocations", "weightmap_layer_allocation_infos",
              "weightmap_layers", "weightmap_textures"):
        try:
            v = lc.get_editor_property(p)
            print("  %s -> %s" % (p, str(v)[:220]))
        except Exception:  # noqa: BLE001
            pass
print("WIRE_OK")
