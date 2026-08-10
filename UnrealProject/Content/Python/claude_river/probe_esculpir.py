# -*- coding: utf-8 -*-
"""Que ofrece esta version de Unreal para modificar el relieve desde Python.

Solo consulta la API; no toca el landscape.
"""

import unreal

CANDIDATOS = ["LandscapeEditorSubsystem", "LandscapeEditorObject",
              "LandscapeProxy", "Landscape", "LandscapeSubsystem",
              "LandscapeEditLayer", "EditorLandscapeLibrary",
              "LandscapeEditorUtilities", "LandscapePatchComponent",
              "LandscapeTexturePatch", "LandscapeHeightPatch",
              "LandscapeCircleHeightPatch"]

print("--- clases disponibles ---")
for c in CANDIDATOS:
    print("  %-32s %s" % (c, "si" if hasattr(unreal, c) else "NO"))

print("\n--- metodos utiles en LandscapeProxy ---")
for m in sorted(dir(unreal.LandscapeProxy)):
    if any(k in m.lower() for k in ("height", "import", "export", "edit",
                                    "layer", "flatten", "sculpt")):
        print("  %s" % m)

print("\n--- subsistemas de editor con 'landscape' ---")
for m in sorted(dir(unreal)):
    if "landscape" in m.lower() and m not in CANDIDATOS:
        print("  %s" % m)
