# -*- coding: utf-8 -*-
"""Capturas de control del campus.

    py vista_campus.py <vista>     pide la captura
    py vista_campus.py limpiar     retira las camaras temporales

La captura se escribe en el frame siguiente, asi que la camara NO puede
destruirse en la misma llamada: se limpian todas al final.
"""

import os
import sys

import unreal

SALIDA = (r"C:\Users\jeffa\AppData\Local\Temp\claude"
          r"\C--Users-jeffa-Desktop-Proyecto"
          r"\bc48160b-174e-4e3d-9cbd-b957a9ba6e7c\scratchpad\campus")

VISTAS = {
    # nombre:     (posicion,                  pitch, yaw,  fov)
    "cenital":   ((-15000, -20000, 120000),    -89,    0,   75),
    "sur":       ((-25000, -78000,  16000),     -9,   62,   60),
    "plaza":     ((-19000, -34000,   3500),     -4,   88,   75),
    "norte":     (( 20000,  78000,  18000),    -11, -105,   60),
    "rio":       (( 10000, -12000,  22000),    -22,  125,   70),
}

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def limpiar():
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("TMP_Vista_"):
            eas.destroy_actor(a)
            n += 1
    print("camaras temporales retiradas: %d" % n)


def pedir(nombre):
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    pos, pitch, yaw, fov = VISTAS[nombre]
    cam = eas.spawn_actor_from_class(unreal.CameraActor, unreal.Vector(*pos),
                                     unreal.Rotator(0.0, pitch, yaw))
    cam.set_actor_label("TMP_Vista_%s" % nombre)
    cam.camera_component.set_editor_property("field_of_view", fov)
    unreal.AutomationLibrary.take_high_res_screenshot(
        1600, 900, os.path.join(SALIDA, "%s.png" % nombre), cam)
    print("pedida la vista %s" % nombre)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "cenital"
    limpiar() if arg == "limpiar" else pedir(arg)
