"""Prueba decisiva: ¿el pincel de agua esta tallando el terreno AHORA?

Mide unos testigos, desactiva affects_landscape, vuelve a medir y restaura.
Si el terreno cambia, el pincel funciona en esta sesion.
"""

import unreal

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
river = [a for a in actors if isinstance(a, unreal.WaterBodyRiver)][0]
landscape = [a for a in actors if isinstance(a, unreal.Landscape)][0]
comp = river.get_editor_property("water_body_component")


def live(x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 60000.0), unreal.Vector(x, y, -60000.0),
        unreal.TraceTypeQuery.ECC_VISIBILITY, True, [],
        unreal.DrawDebugTrace.NONE, True)
    hit = res[1] if isinstance(res, tuple) else res
    d = hit.to_dict()
    return float(d["impact_point"].z) if d["blocking_hit"] else None


# testigos: junto al rio antiguo y lejos de el
probes = [(0, 0), (580, -467), (1192, -3391), (20000, -30000),
          (46900, -48030), (-40000, 40000), (30000, 30000)]

prev = comp.get_editor_property("affects_landscape")
print("affects_landscape:", prev)

antes = [live(*p) for p in probes]

comp.set_editor_property("affects_landscape", False)
landscape.force_layers_full_update()
sin = [live(*p) for p in probes]

comp.set_editor_property("affects_landscape", prev)
landscape.force_layers_full_update()
despues = [live(*p) for p in probes]

print("\n     punto            con pincel   sin pincel      dif    restaurado")
tallando = 0
for p, a, s, d in zip(probes, antes, sin, despues):
    dif = (a - s) if (a is not None and s is not None) else 0.0
    if abs(dif) > 1.0:
        tallando += 1
    print("  (%7d,%7d) %11.1f %12.1f %8.1f %12.1f" % (p[0], p[1], a, s, dif, d))

print("\ntestigos alterados por el pincel: %d de %d" % (tallando, len(probes)))
print("EL PINCEL TALLA:", tallando > 0)
