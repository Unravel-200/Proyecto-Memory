# -*- coding: utf-8 -*-
"""Importa a Unreal los FBX de las envolventes de los 18 edificios.

Un FBX por nivel, tal y como los exporta Modelos-3D/_PlanosLib/modelar.py.
Van a /Game/Modelos3D/<Edificio>/, junto al resto de activos del edificio.

Crea tambien los tres materiales del campus y los asigna por nombre de slot,
para no arrastrar los materiales del FBX.
"""

import json
import os

import unreal

RAIZ_FBX = r"C:\Users\jeffa\Desktop\Proyecto\Modelos-3D"
AQUI = os.path.dirname(os.path.abspath(__file__))

# carpeta de Modelos-3D -> carpeta de /Game/Modelos3D
CARPETAS = {
    "Biblioteca": "Biblioteca", "Generales": "Generales",
    "Educacion": "Educacion", "Mantenimiento": "Mantenimiento",
    "Ingenieria": "Ingenieria", "Ciencias": "Ciencias",
    "Medicina": "Medicina", "Psicologia": "Psicologia",
    "Informatica": "Informatica", "Artes": "Artes",
    "AuditorioCentral": "AuditorioCentral", "Historia": "Historia",
    "Derecho": "Derecho", "Soda": "Soda", "Gimnasio": "Gimnasio",
    "Residencias": "Residencias", "Rectoria": "Rectoria",
    "CentroCultural": "CentroCultural",
}

MATERIALES = [("M_Concrete_Campus", (0.42, 0.41, 0.39), 0.85),
              ("M_Wall_Campus", (0.62, 0.60, 0.55), 0.80),
              ("M_Glass_Campus", (0.12, 0.20, 0.26), 0.15)]
DIR_MAT = "/Game/Materials/Campus"


def material(nombre, color, rug):
    ruta = "%s/%s" % (DIR_MAT, nombre)
    if unreal.EditorAssetLibrary.does_asset_exist(ruta):
        return unreal.EditorAssetLibrary.load_asset(ruta)
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mat = tools.create_asset(nombre, DIR_MAT, unreal.Material,
                             unreal.MaterialFactoryNew())
    ML = unreal.MaterialEditingLibrary
    c = ML.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector,
                                      -400, 0)
    c.set_editor_property("constant", unreal.LinearColor(*color, 1.0))
    ML.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    r = ML.create_material_expression(mat, unreal.MaterialExpressionConstant,
                                      -400, 200)
    r.set_editor_property("r", rug)
    ML.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    ML.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(ruta)
    return mat


def opciones():
    o = unreal.FbxImportUI()
    o.set_editor_property("import_mesh", True)
    o.set_editor_property("import_textures", False)
    o.set_editor_property("import_materials", False)
    o.set_editor_property("import_as_skeletal", False)
    o.set_editor_property("mesh_type_to_import",
                          unreal.FBXImportType.FBXIT_STATIC_MESH)
    sm = o.static_mesh_import_data
    sm.set_editor_property("combine_meshes", True)
    sm.set_editor_property("generate_lightmap_u_vs", True)
    sm.set_editor_property("auto_generate_collision", False)
    sm.set_editor_property("convert_scene", True)
    sm.set_editor_property("force_front_x_axis", False)
    sm.set_editor_property("convert_scene_unit", True)
    sm.set_editor_property("normal_import_method",
                           unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
    return o


def main():
    mats = [material(*m) for m in MATERIALES]
    tareas = []
    for carpeta, destino in CARPETAS.items():
        d = os.path.join(RAIZ_FBX, carpeta)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.startswith("SM_Building_") and f.endswith(".fbx"):
                tareas.append((os.path.join(d, f),
                               "/Game/Modelos3D/%s" % destino,
                               os.path.splitext(f)[0]))

    ui = opciones()
    datos = []
    for ruta, paquete, nombre in tareas:
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", ruta)
        t.set_editor_property("destination_path", paquete)
        t.set_editor_property("destination_name", nombre)
        t.set_editor_property("automated", True)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", True)
        t.set_editor_property("options", ui)
        datos.append(t)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(datos)

    # ---- materiales del campus por slot y comprobacion de tamano ----
    informe = []
    for t in datos:
        for ruta in t.get_editor_property("imported_object_paths"):
            act = unreal.EditorAssetLibrary.load_asset(ruta)
            if not isinstance(act, unreal.StaticMesh):
                continue
            for i in range(act.get_num_sections(0)):
                act.set_material(i, mats[i] if i < len(mats) else mats[0])
            b = act.get_bounding_box()
            unreal.EditorAssetLibrary.save_asset(ruta)
            informe.append({"activo": ruta,
                            "min": [b.min.x, b.min.y, b.min.z],
                            "max": [b.max.x, b.max.y, b.max.z]})

    with open(os.path.join(AQUI, "edificios_importados.json"), "w") as fh:
        json.dump(informe, fh, indent=1)

    print("importados %d de %d FBX" % (len(informe), len(tareas)))
    for r in informe[:4]:
        mn, mx = r["min"], r["max"]
        print("   %-58s %.0f x %.0f x %.0f uu"
              % (r["activo"].split(".")[-1], mx[0] - mn[0], mx[1] - mn[1],
                 mx[2] - mn[2]))


main()
