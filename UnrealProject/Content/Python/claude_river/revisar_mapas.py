"""Comprueba si es seguro borrar L_Campus_Blockout, L_AssetValidation y
L_Campus_Landscape: quien los referencia y que contienen.
"""

import unreal

CANDIDATOS = ["/Game/Maps/L_Campus_Blockout",
              "/Game/Maps/L_AssetValidation",
              "/Game/Maps/L_Campus_Landscape"]
CONSERVAR = ["/Game/Maps/L_Campus_Natural", "/Game/Maps/L_Developer_Testing"]

ar = unreal.AssetRegistryHelpers.get_asset_registry()

print("=== QUIEN REFERENCIA A CADA MAPA ===")
for m in CANDIDATOS + CONSERVAR:
    refs = unreal.EditorAssetLibrary.find_package_referencers_for_asset(m, False)
    externas = [str(r) for r in refs
                if not str(r).startswith("/Game/__External")
                and str(r) != m]
    marca = "  (se conserva)" if m in CONSERVAR else ""
    print("\n%s%s" % (m, marca))
    print("   referencias totales: %d   externas (no sus propios actores): %d"
          % (len(refs), len(externas)))
    for r in externas[:15]:
        print("      <- %s" % r)

print("\n=== DEPENDENCIAS DE CADA MAPA (que usa el mapa) ===")
for m in CANDIDATOS:
    deps = ar.get_dependencies(m, unreal.AssetRegistryDependencyOptions())
    propios = [str(d) for d in (deps or []) if str(d).startswith("/Game")]
    print("%-34s depende de %d assets de /Game" % (m.split("/")[-1], len(propios)))

print("\n=== CONFIGURACION DE MAPAS DEL PROYECTO ===")
for clave in ("editor_startup_map", "game_default_map", "server_default_map",
              "transition_map", "game_instance_class"):
    try:
        s = unreal.get_default_object(unreal.GameMapsSettings)
        print("   %-22s = %s" % (clave, s.get_editor_property(clave)))
    except Exception as exc:  # noqa: BLE001
        print("   %-22s = <n/d> %s" % (clave, str(exc)[:60]))

print("\n=== BLUEPRINTS DEL PROYECTO ===")
bps = ar.get_assets_by_class(
    unreal.TopLevelAssetPath("/Script/Engine", "Blueprint"), True)
lista = [str(b.package_name) for b in bps if str(b.package_name).startswith("/Game")]
print("   blueprints en /Game: %d" % len(lista))
for b in lista:
    print("      %s" % b)
