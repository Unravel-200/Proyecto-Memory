"""Limpia lo que quedo en disco tras borrar los mapas."""

import unreal

DIRS = ["/Game/__ExternalActors__/Maps/L_Campus_Landscape",
        "/Game/__ExternalObjects__/Maps/L_Campus_Landscape"]
ASSETS = ["/Game/Maps/L_AssetValidation", "/Game/Maps/L_Campus_Blockout"]

eal = unreal.EditorAssetLibrary

for d in DIRS:
    if eal.does_directory_exist(d):
        try:
            ok = eal.delete_directory(d)
            print("%-56s %s" % (d, "borrado" if ok else "NO se pudo"))
        except Exception as exc:  # noqa: BLE001
            print("%-56s error %s" % (d, str(exc)[:80]))
    else:
        print("%-56s no existe" % d)

for a in ASSETS:
    if eal.does_asset_exist(a):
        try:
            ok = eal.delete_asset(a)
            print("%-56s %s" % (a, "borrado" if ok else "NO se pudo"))
        except Exception as exc:  # noqa: BLE001
            print("%-56s error %s" % (a, str(exc)[:80]))
    else:
        print("%-56s ya no esta en el registro" % a)

print("\n=== mundos que quedan en el registro ===")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
for x in sorted(str(a.package_name) for a in ar.get_assets_by_class(
        unreal.TopLevelAssetPath("/Script/Engine", "World"), True)
        if str(a.package_name).startswith("/Game")):
    print("   ", x)
