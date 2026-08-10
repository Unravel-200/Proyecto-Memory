"""Inventario de todas las mallas Blockout con sus dimensiones locales.

Sirve para saber si son piezas interiores (volumenes de sala, de una planta)
o envolventes de edificio completo.
"""

import json

import unreal

OUT = "C:/Users/jeffa/AppData/Local/Temp/claude/blockouts.json"

ar = unreal.AssetRegistryHelpers.get_asset_registry()
todos = ar.get_assets_by_class(
    unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh"), True)
rutas = sorted(str(a.package_name) for a in todos
               if str(a.package_name).startswith("/Game/Modelos3D")
               and "Blockout" in str(a.package_name))

filas = []
for p in rutas:
    m = unreal.EditorAssetLibrary.load_asset(p)
    if m is None:
        continue
    b = m.get_bounding_box()
    dx, dy, dz = (b.max.x - b.min.x, b.max.y - b.min.y, b.max.z - b.min.z)
    carpeta = p.split("/")[3]
    filas.append({"carpeta": carpeta, "nombre": p.split("/")[-1],
                  "dx": dx, "dy": dy, "dz": dz,
                  "area": dx * dy / 10000.0,       # m2
                  "alto_m": dz / 100.0})

filas.sort(key=lambda r: (r["carpeta"], -r["area"]))
actual = None
for r in filas:
    if r["carpeta"] != actual:
        actual = r["carpeta"]
        print("\n--- %s ---" % actual)
        print("   %-52s %10s %8s %8s" % ("malla", "planta m2", "ancho m", "alto m"))
    print("   %-52s %10.0f %8.1f %8.1f"
          % (r["nombre"][:52], r["area"], max(r["dx"], r["dy"]) / 100.0, r["alto_m"]))

alturas = sorted(r["alto_m"] for r in filas)
areas = sorted(r["area"] for r in filas)
print("\n=== resumen de %d blockouts ===" % len(filas))
print("altura:  min %.1f m   mediana %.1f m   max %.1f m"
      % (alturas[0], alturas[len(alturas) // 2], alturas[-1]))
print("planta:  min %.0f m2  mediana %.0f m2  max %.0f m2"
      % (areas[0], areas[len(areas) // 2], areas[-1]))
print("con altura <= 6 m (una planta): %d de %d"
      % (sum(1 for a in alturas if a <= 6.0), len(alturas)))

json.dump(filas, open(OUT, "w"))
print("->", OUT)
