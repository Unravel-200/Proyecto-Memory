"""Borra de Unreal todas las mallas Blockout de /Game/Modelos3D.

Antes comprueba quien las referencia, para no dejar referencias rotas en
blueprints, materiales o niveles.
"""

import json

import unreal

OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/blockouts_borrados.json"

ar = unreal.AssetRegistryHelpers.get_asset_registry()
todos = ar.get_assets_by_class(
    unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh"), True)
rutas = sorted(str(a.package_name) for a in todos
               if str(a.package_name).startswith("/Game/Modelos3D")
               and "Blockout" in str(a.package_name))
conjunto = set(rutas)
print("mallas Blockout en Unreal: %d" % len(rutas))

# ---------- quien las referencia ----------
externos = {}
for p in rutas:
    refs = unreal.EditorAssetLibrary.find_package_referencers_for_asset(p, False)
    fuera = [str(r) for r in refs if str(r) not in conjunto]
    if fuera:
        externos[p] = fuera

if externos:
    print("\nAVISO: %d mallas tienen referencias externas:" % len(externos))
    for p, r in list(externos.items())[:20]:
        print("   %s  <- %s" % (p.split("/")[-1], ", ".join(r[:3])))
else:
    print("ninguna esta referenciada desde fuera del propio grupo")

json.dump(rutas, open(OUT, "w"), indent=1)

# ---------- borrar ----------
borradas = fallidas = 0
for p in rutas:
    try:
        if unreal.EditorAssetLibrary.delete_asset(p):
            borradas += 1
        else:
            fallidas += 1
            print("   no se pudo borrar:", p)
    except Exception as exc:  # noqa: BLE001
        fallidas += 1
        print("   error con %s: %s" % (p, str(exc)[:90]))

print("\nborradas %d   fallidas %d" % (borradas, fallidas))

quedan = [str(a.package_name) for a in ar.get_assets_by_class(
    unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh"), True)
    if str(a.package_name).startswith("/Game/Modelos3D")
    and "Blockout" in str(a.package_name)]
print("Blockout que quedan en Unreal: %d" % len(quedan))
print("lista de las borradas ->", OUT)
