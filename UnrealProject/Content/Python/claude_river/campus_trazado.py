# -*- coding: utf-8 -*-
"""Trazado del campus: donde va cada edificio y por que.

GENERADO por resolver_trazado.py. El diseno urbano es fijo -una reticula de 5
avenidas, 3 al sur del rio y 2 al norte, cada una con dos hileras
enfrentadas- y el programa desliza cada edificio a lo largo de su hilera
hasta encontrar el suelo mas parejo, repartiendo el hueco sobrante en vez de
dejarlo todo pegado a un extremo (ver horario_ideal en resolver_trazado.py).

El rio cruza el mapa en diagonal y lo parte en dos. El landscape real mide
1008 x 1008 m (-504..504 en X e Y); la reticula usa una fraccion mucho mayor
de esa area que el primer trazado, que eran dos avenidas sueltas pegadas al
rio con todo el resto del mapa vacio.

Zona sur (avenidas S1 Y=-400, S2 Y=-250, S3 Y=-100): noches 1 y 2.
Zona norte (avenidas N1 X=80, N2 X=260): noche 3. La Rectoria remata el eje
norte entre las dos avenidas, mas al norte: noche 4.

    Noche 1  Biblioteca, Plaza, Generales, Educacion, Mantenimiento
    Noche 2  Ingenieria, Ciencias, Medicina, Psicologia
    Noche 3  Informatica, Artes, Auditorio, Historia, Derecho, Gimnasio
    Noche 4  Residencias, Rectoria (torre de 40 m, remate del eje norte)

La fachada principal de cada envolvente mira a -Y, asi que el yaw de cada
hilera es el que la pone de cara a su avenida.

Coordenadas en metros; el centro de la huella, no el pivote.
"""

# (activo, nombre, X, Y, yaw, zona)
TRAZADO = [
    ("Medicine", "Medicina", -243, -360, 180, "sur"),
    ("Sciences", "Ciencias", -83, -406, 180, "sur"),
    ("Engineering", "Ingenieria", -230, -445, 0, "sur"),
    ("Maintenance", "Mantenimiento", -83, -476, 0, "sur"),
    ("GeneralStudies", "Generales", -273, -260, 180, "sur"),
    ("Library", "Biblioteca", -110, -164, 180, "sur"),
    ("Psychology", "Psicologia", -178, -270, 0, "sur"),
    ("Cafeteria", "Soda", -108, -326, 0, "sur"),
    ("Education", "Educacion", -208, -20, 180, "sur"),
    ("CulturalCenter", "CentroCultural", -283, -101, 0, "sur"),
    ("Residence", "Residencias", -150, -100, 0, "sur"),
    ("Arts", "Artes", 54, 197, 270, "norte"),
    ("Auditorium", "Auditorio", 9, 330, 270, "norte"),
    ("Gym", "Gimnasio", 130, 187, 90, "norte"),
    ("Law", "Derecho", 163, 332, 90, "norte"),
    ("History", "Historia", 237, 152, 270, "norte"),
    ("Informatics", "Informatica", 237, 294, 270, "norte"),
    ("Pool", "Piscina", 324, 222, 90, "norte"),
    ("Rectorate", "Rectoria", 230, 420, 180, "norte"),
]

# plaza central (Definitivo sec. 11: plaza 45 x 45, fuente de 20 m)
PLAZA = (-330.0, -175.0, 45.0)

# el rio, en metros, tal y como lo devuelve campus_terreno.py
RIO = [(469, -480), (402, -430), (323, -409), (251, -367), (204, -300), (152, -236), (108, -165), (60, -98), (12, -31), (-9, 49), (-50, 117), (-69, 195), (-94, 274), (-171, 306), (-201, 384), (-229, 463), (-237, 504)]

HOLGURA_RIO = 55.0        # m libres entre edificio y eje del rio
SEPARACION = 30.0         # m minimos entre dos edificios

# Huecos entre vecinos >= 60 m: candidatos a parque o
# plaza secundaria. (edificio antes, edificio despues,
# X del centro, Y del centro, ancho del hueco en m)
PARQUES = [
    ("Medicina", "Ciencias", -163, -383, 85.0),
    ("Ingenieria", "Mantenimiento", -146, -460, 85.0),
    ("Generales", "Biblioteca", -188, -212, 100.0),
    ("CentroCultural", "Residencias", -223, -100, 90.0),
    ("Artes", "Auditorio", 32, 267, 80.0),
    ("Gimnasio", "Derecho", 146, 262, 85.0),
    ("Historia", "Informatica", 237, 222, 90.0),
]
