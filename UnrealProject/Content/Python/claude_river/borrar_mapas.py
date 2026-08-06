"""Borra los tres mapas sin uso, tras confirmar que nadie los referencia."""

import unreal

MAPAS = ["/Game/Maps/L_Campus_Blockout",
         "/Game/Maps/L_AssetValidation",
         "/Game/Maps/L_Campus_Landscape"]

ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
abierto = ues.get_editor_world().get_path_name()
print("mapa abierto ahora mismo:", abierto)

for m in MAPAS:
    if m in abierto:
        print("ABORTADO: %s esta abierto en el editor" % m)
        raise SystemExit(1)

# ultima comprobacion de referencias antes de tocar nada
for m in MAPAS:
    refs = [str(r) for r in
            unreal.EditorAssetLibrary.find_package_referencers_for_asset(m, False)
            if not str(r).startswith("/Game/__External") and str(r) != m]
    if refs:
        print("ABORTADO: %s sigue referenciado por %s" % (m, refs[:5]))
        raise SystemExit(1)
print("confirmado: ninguno tiene referencias externas\n")

for m in MAPAS:
    try:
        ok = unreal.EditorAssetLibrary.delete_asset(m)
        print("%-38s %s" % (m, "borrado" if ok else "NO se pudo borrar"))
    except Exception as exc:  # noqa: BLE001
        print("%-38s error: %s" % (m, str(exc)[:110]))

print("\n=== mapas que quedan ===")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
for a in sorted(ar.get_assets_by_class(
        unreal.TopLevelAssetPath("/Script/Engine", "World"), True),
        key=lambda x: str(x.package_name)):
    p = str(a.package_name)
    if p.startswith("/Game"):
        print("   ", p)
