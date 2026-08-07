# -*- coding: utf-8 -*-
"""Resuelve el trazado del campus contra el relieve real.

El diseno urbano lo pongo yo: dos zonas, cada una con una avenida y dos
hileras de edificios enfrentadas. Lo que resuelve el programa es DONDE cae
cada edificio a lo largo de su hilera, deslizandolo para que el terreno bajo
su huella sea lo mas parejo posible sin romper el orden ni las separaciones.

Se ejecuta fuera de Unreal: lee malla_alturas.json y escribe campus_trazado.py.
"""

import itertools
import json
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

RIO = [(469, -480), (402, -430), (323, -409), (251, -367), (204, -300),
       (152, -236), (108, -165), (60, -98), (12, -31), (-9, 49), (-50, 117),
       (-69, 195), (-94, 274), (-171, 306), (-201, 384), (-229, 463),
       (-237, 504)]

# huellas reales de las envolventes importadas, en metros
TAM = {"Sciences": (75, 55), "Medicine": (75, 50), "Library": (55, 45),
       "GeneralStudies": (70, 45), "Education": (50, 35),
       "Maintenance": (40, 25), "Engineering": (85, 60), "Psychology": (45, 35),
       "Cafeteria": (35, 25), "Residence": (55, 18), "CulturalCenter": (30, 20),
       "History": (50, 40), "Law": (55, 40), "Informatics": (55, 40),
       "Arts": (60, 45), "Auditorium": (45, 40), "Gym": (65, 45),
       "Pool": (40, 25), "Rectorate": (50, 40)}

NOMBRE = {"Sciences": "Ciencias", "Medicine": "Medicina", "Library": "Biblioteca",
          "GeneralStudies": "Generales", "Education": "Educacion",
          "Maintenance": "Mantenimiento", "Engineering": "Ingenieria",
          "Psychology": "Psicologia", "Cafeteria": "Soda",
          "Residence": "Residencias", "CulturalCenter": "CentroCultural",
          "History": "Historia", "Law": "Derecho", "Informatics": "Informatica",
          "Arts": "Artes", "Auditorium": "Auditorio", "Gym": "Gimnasio",
          "Pool": "Piscina", "Rectorate": "Rectoria"}

# El landscape real es -504..504 en X e Y (8x8 LandscapeStreamingProxy de
# 126 m, medido con diag_tiles.py). Con eso, y el rio partiendo el mapa en
# diagonal, hay mucho mas suelo bueno del que ocupaba el primer trazado (dos
# avenidas de 600x150 y 300x170 m pegadas al rio, con el resto del mapa -mas
# de 800.000 m2- vacio). Este trazado usa una RETICULA de 5 avenidas -3 al
# sur del rio, 2 al norte- en vez de una sola por lado, para repartir los
# mismos 18 edificios sobre un area mucho mayor sin perder la logica de
# noches de Definitivo sec. 3.
#
# YAW: el exportador FBX invierte el eje Y de Blender a Unreal (ver docstring
# de colocar_campus.py), asi que con yaw=0 la fachada mira a +Y, no a -Y. La
# tabla real, medida sobre el mesh importado:
#     yaw=0    fachada mira a +Y (norte)
#     yaw=180  fachada mira a -Y (sur)
#     yaw=90   fachada mira a -X (oeste)
#     yaw=270  fachada mira a +X (este)
FILAS = [
    # ---- zona sur: 3 avenidas este-oeste, Y = -400 / -250 / -100 ----
    # S1 (Y=-400): la mas alejada del rio en toda su longitud; ciencia e
    # ingenieria, los edificios de mas huella, van aqui donde sobra sitio.
    dict(id="S1n", zona="sur", eje="X", avenida=-400.0, lado=+1, yaw=180,
         desde=-480.0, hasta=140.0, retiro=15.0,
         edificios=["Sciences", "Medicine"]),
    dict(id="S1s", zona="sur", eje="X", avenida=-400.0, lado=-1, yaw=0,
         desde=-480.0, hasta=140.0, retiro=15.0,
         edificios=["Maintenance", "Engineering"]),
    # S2 (Y=-250): franja intermedia
    dict(id="S2n", zona="sur", eje="X", avenida=-250.0, lado=+1, yaw=180,
         desde=-480.0, hasta=100.0, retiro=15.0,
         edificios=["Library", "GeneralStudies"]),
    dict(id="S2s", zona="sur", eje="X", avenida=-250.0, lado=-1, yaw=0,
         desde=-480.0, hasta=100.0, retiro=15.0,
         edificios=["Psychology", "Cafeteria"]),
    # S3 (Y=-100): la mas cercana al rio, por eso el rango mas corto al este
    dict(id="S3n", zona="sur", eje="X", avenida=-100.0, lado=+1, yaw=180,
         desde=-480.0, hasta=60.0, retiro=15.0,
         edificios=["Education"]),
    dict(id="S3s", zona="sur", eje="X", avenida=-100.0, lado=-1, yaw=0,
         desde=-480.0, hasta=60.0, retiro=15.0,
         edificios=["Residence", "CulturalCenter"]),
    # ---- zona norte: 2 avenidas norte-sur, X = 80 / 260 ----
    dict(id="N1o", zona="norte", eje="Y", avenida=80.0, lado=-1, yaw=270,
         desde=90.0, hasta=420.0, retiro=15.0,
         edificios=["Arts", "Auditorium"]),
    dict(id="N1e", zona="norte", eje="Y", avenida=80.0, lado=+1, yaw=90,
         desde=90.0, hasta=420.0, retiro=15.0,
         edificios=["Law", "Gym"]),
    dict(id="N2o", zona="norte", eje="Y", avenida=260.0, lado=-1, yaw=270,
         desde=60.0, hasta=380.0, retiro=15.0,
         edificios=["History", "Informatics"]),
    dict(id="N2e", zona="norte", eje="Y", avenida=260.0, lado=+1, yaw=90,
         desde=60.0, hasta=380.0, retiro=15.0,
         edificios=["Pool"]),
]

# la torre de 40 m cierra el eje norte, entre las dos avenidas, mirando al
# sur para que se vea de frente al recorrer cualquiera de las dos hacia ella
REMATE = dict(activo="Rectorate", zona="norte", yaw=180, x=170.0, y=None,
              buscar=(400.0, 460.0))

PLAZA = (-330.0, -175.0, 45.0)     # cruce entre S1 y S2, punto medio de la
                                    # reticula sur (Definitivo sec. 11)
SEPARACION = 30.0          # piso duro
GAP_OBJETIVO = 32.0        # separacion que el solver busca de verdad
GAP_MAX = 85.0             # tope al reparto cuando sobra sitio: sin esto,
                           # una fila corta (1-2 edificios) en una avenida
                           # larga dejaria TODO el sobrante en un solo hueco
                           # inmenso en vez de repartirlo
GAP_PARQUE = 60.0          # a partir de aqui el hueco se marca como parque,
                           # no se deja como vacio sin explicar
HOLGURA_RIO = 55.0


def cargar():
    with open(os.path.join(AQUI, "malla_alturas.json")) as fh:
        return json.load(fh)


class Relieve(object):
    def __init__(self, m):
        self.Z, self.P = m["z"], m["paso"]
        self.x0, self.y0 = m["x0"], m["y0"]

    def rango(self, cx, cy, ax, ay):
        """(desnivel, minimo, maximo) bajo una huella centrada en (cx, cy)."""
        vs = []
        i0 = int(math.floor((cx - ax - self.x0) / self.P))
        i1 = int(math.ceil((cx + ax - self.x0) / self.P))
        j0 = int(math.floor((cy - ay - self.y0) / self.P))
        j1 = int(math.ceil((cy + ay - self.y0) / self.P))
        for i in range(max(0, i0), min(len(self.Z), i1 + 1)):
            for j in range(max(0, j0), min(len(self.Z[0]), j1 + 1)):
                v = self.Z[i][j]
                if v is not None:
                    vs.append(v)
        if not vs:
            return None
        return max(vs) - min(vs), min(vs), max(vs)


def dist_rio(x, y):
    m = 1e18
    for i in range(len(RIO) - 1):
        ax, ay = RIO[i]
        bx, by = RIO[i + 1]
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L == 0 else max(0.0, min(1.0,
                                            ((x - ax) * dx + (y - ay) * dy) / L))
        m = min(m, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return m


def semiejes(activo, yaw):
    w, h = TAM[activo]
    c, s = abs(math.cos(math.radians(yaw))), abs(math.sin(math.radians(yaw)))
    return (w * c + h * s) / 2.0, (w * s + h * c) / 2.0


VENTANA = 18.0    # cuanto puede desviarse del hueco objetivo buscando terreno


def horario_ideal(fila, orden):
    """Posicion ideal de cada edificio de la hilera, calculada UNA VEZ para
    toda la fila. Es la referencia fija contra la que cada edificio busca su
    mejor terreno; ancla la busqueda al plan global, no al resultado del
    anterior (ver docstring de resolver_fila).

    El hueco entre edificios REPARTE el sobrante de la avenida en vez de
    dejarlo todo pegado al extremo `desde`: si no, una fila de 1-2 edificios
    en una avenida larga (aqui hay avenidas de 620 m para filas de 1-2
    edificios, a proposito, para repartir el campus sobre mas mapa) dejaria
    un solo vacio inmenso al final en vez de un campus con aire parejo. El
    hueco tiene un tope (GAP_MAX): pasado eso ya no sirve para "dar espacio",
    es terreno sin uso, y ese sobrante se usa para CENTRAR la fila en su
    avenida en vez de seguir estirando el hueco.
    """
    largos = []
    for activo in orden:
        ax, ay = semiejes(activo, fila["yaw"])
        largos.append(ax if fila["eje"] == "X" else ay)
    disponible = fila["hasta"] - fila["desde"]
    ancho_total = sum(2.0 * l for l in largos)
    n = len(orden)
    huecos = max(0, n - 1)

    if huecos:
        gap = (disponible - ancho_total) / float(huecos)
        gap = max(SEPARACION, min(gap, GAP_MAX))
    else:
        gap = 0.0
    ancho_usado = ancho_total + huecos * gap
    inicio = fila["desde"] + max(0.0, (disponible - ancho_usado) / 2.0)

    u, objetivos = inicio, []
    for largo in largos:
        u += largo
        objetivos.append(u)
        u += largo + gap
    return objetivos, gap


def resolver_fila(rel, fila, orden, ocupado):
    """Coloca una hilera en el orden dado. Devuelve (colocados, ocupado).

    La busqueda de terreno de cada edificio se hace en una VENTANA acotada
    alrededor de su posicion en `horario_ideal`, no alrededor de donde quedo
    el edificio anterior. Anclar la ventana al resultado del paso previo (lo
    que hacia la primera version) deja que la deriva se acumule: cada
    edificio se corre un poco hacia mejor terreno, y para el quinto de la
    fila ya no queda margen antes del rio, aunque la suma total SI cabria si
    cada uno se hubiera quedado cerca de su hueco. Con el horario fijo, la
    ventana de cada edificio no depende de los anteriores; solo se ensancha
    como ultimo recurso, edificio por edificio.

    `piso` sigue siendo un limite duro (el borde derecho del edificio previo
    + SEPARACION): la ventana ancla la BUSQUEDA, pero nunca se permite un
    solape real.
    """
    objetivos, _ = horario_ideal(fila, orden)
    puestos, ocup = [], list(ocupado)
    piso = fila["desde"]
    for activo, objetivo in zip(orden, objetivos):
        ax, ay = semiejes(activo, fila["yaw"])
        # profundidad perpendicular a la avenida
        perp = ay if fila["eje"] == "X" else ax
        largo = ax if fila["eje"] == "X" else ay
        fijo = fila["avenida"] + fila["lado"] * (fila["retiro"] + perp)

        mejor = None
        for radio in (VENTANA, VENTANA * 3, None):   # None = toda la fila
            u0 = max(piso + largo,
                     fila["desde"] + largo if radio is None else objetivo - radio)
            u1 = min(fila["hasta"] - largo,
                     fila["hasta"] - largo if radio is None else objetivo + radio)
            u = u0
            while u <= u1:
                # holgura perpendicular: la hilera puede quebrarse un poco
                for d in (0.0, -12.0, 12.0, -24.0, 24.0, -36.0, 36.0, -48.0, 48.0):
                    f = fijo + fila["lado"] * d
                    cx, cy = (u, f) if fila["eje"] == "X" else (f, u)
                    r = rel.rango(cx, cy, ax, ay)
                    if r is None:
                        continue
                    dr = min(dist_rio(cx + sx * ax, cy + sy * ay)
                             for sx in (-1, 1) for sy in (-1, 1))
                    if dr < HOLGURA_RIO:
                        continue
                    if any(min(a[2], cx + ax) - max(a[0], cx - ax) > -SEPARACION
                           and min(a[3], cy + ay) - max(a[1], cy - ay) > -SEPARACION
                           for a in ocup):
                        continue
                    # penaliza alejarse del horario ideal, no del anterior:
                    # es lo que evita la deriva acumulada (ver docstring).
                    coste = r[0] + abs(u - objetivo) * 0.09 + abs(d) * 0.020
                    if mejor is None or coste < mejor[0]:
                        mejor = (coste, u, cx, cy, r)
                u += 5.0
            if mejor is not None:
                break

        if mejor is None:
            return None, ocupado
        _, u, cx, cy, r = mejor
        ocup.append((cx - ax, cy - ay, cx + ax, cy + ay))
        puestos.append((activo, NOMBRE[activo], cx, cy, fila["yaw"],
                        fila["zona"], r, fila["id"]))
        piso = u + largo + SEPARACION
    return puestos, ocup


def resolver():
    rel = Relieve(cargar())
    salida, ocupado = [], []

    px, py, pl = PLAZA
    ocupado.append((px - pl / 2, py - pl / 2, px + pl / 2, py + pl / 2))

    for fila in FILAS:
        # el orden dentro de una hilera es libre -todos son de la misma zona-,
        # asi que se prueban las permutaciones y gana la que deja el peor
        # edificio mejor asentado. El primero en elegir se lleva el mejor
        # suelo, y quien deba ser el primero lo decide el terreno.
        base = fila["edificios"]
        mejor = None
        for orden in itertools.permutations(base):
            puestos, ocup = resolver_fila(rel, fila, orden, ocupado)
            if puestos is None:
                continue
            peor = max(p[6][0] for p in puestos)
            suma = sum(p[6][0] for p in puestos)
            if mejor is None or (peor, suma) < (mejor[0], mejor[1]):
                mejor = (peor, suma, puestos, ocup)
        if mejor is None:
            print("   ! la hilera %s no cabe" % base)
            continue
        salida.extend(mejor[2])
        ocupado = mejor[3]

    # remate del eje norte
    ax, ay = semiejes(REMATE["activo"], REMATE["yaw"])
    mejor = None
    v = REMATE["buscar"][0]
    while v <= REMATE["buscar"][1]:
        for dx in (-60.0, -30.0, 0.0, 30.0, 60.0):
            cx, cy = REMATE["x"] + dx, v
            r = rel.rango(cx, cy, ax, ay)
            if r is None:
                continue
            if min(dist_rio(cx + sx * ax, cy + sy * ay)
                   for sx in (-1, 1) for sy in (-1, 1)) < HOLGURA_RIO:
                continue
            if any(min(a[2], cx + ax) - max(a[0], cx - ax) > -SEPARACION
                   and min(a[3], cy + ay) - max(a[1], cy - ay) > -SEPARACION
                   for a in ocupado):
                continue
            if mejor is None or r[0] < mejor[0][0]:
                mejor = (r, cx, cy)
        v += 10.0
    if mejor:
        r, cx, cy = mejor
        salida.append((REMATE["activo"], NOMBRE[REMATE["activo"]], cx, cy,
                       REMATE["yaw"], REMATE["zona"], r, "REMATE"))
    return salida


CABECERA = '''# -*- coding: utf-8 -*-
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
'''

PIE = ''']

# plaza central (Definitivo sec. 11: plaza 45 x 45, fuente de 20 m)
PLAZA = (%.1f, %.1f, %.1f)

# el rio, en metros, tal y como lo devuelve campus_terreno.py
RIO = %r

HOLGURA_RIO = %.1f        # m libres entre edificio y eje del rio
SEPARACION = %.1f         # m minimos entre dos edificios
'''


def huecos(filas):
    """Separacion real entre vecinos de la misma hilera. Los que superen
    GAP_PARQUE se devuelven como sitio de parque: centro y tamano del hueco
    disponible entre las dos fachadas."""
    eje_de = {f["id"]: f["eje"] for f in FILAS}
    por_fila = {}
    for activo, nombre, cx, cy, yaw, zona, r, fid in filas:
        if fid == "REMATE":
            continue
        ax, ay = semiejes(activo, yaw)
        por_fila.setdefault(fid, []).append((cx, cy, ax, ay, nombre))

    reporte, parques = [], []
    for fid, v in por_fila.items():
        eje = eje_de[fid]
        v.sort(key=lambda p: p[0] if eje == "X" else p[1])
        for (cx0, cy0, ax0, ay0, n0), (cx1, cy1, ax1, ay1, n1) in zip(v, v[1:]):
            if eje == "X":
                gap = (cx1 - ax1) - (cx0 + ax0)
                centro = ((cx0 + ax0 + cx1 - ax1) / 2.0, (cy0 + cy1) / 2.0)
            else:
                gap = (cy1 - ay1) - (cy0 + ay0)
                centro = ((cx0 + cx1) / 2.0, (cy0 + ay0 + cy1 - ay1) / 2.0)
            reporte.append((n0, n1, gap))
            if gap >= GAP_PARQUE:
                parques.append((n0, n1, centro[0], centro[1], gap))
    return reporte, parques


def main():
    filas = resolver()
    print("%-16s %-5s %-6s %8s %8s %5s %9s %7s" %
          ("edificio", "fila", "zona", "X", "Y", "yaw", "desnivel", "cotas"))
    lineas = []
    for activo, nombre, cx, cy, yaw, zona, r, fid in filas:
        print("%-16s %-5s %-6s %8.0f %8.0f %5d %9.1f   %.1f .. %.1f" %
              (nombre, fid, zona, cx, cy, yaw, r[0], r[1], r[2]))
        lineas.append('    ("%s", "%s", %.0f, %.0f, %d, "%s"),'
                      % (activo, nombre, cx, cy, yaw, zona))
    peor = max(r[0] for *_, r, _fid in filas)
    print("\n%d edificios. Desnivel maximo bajo una huella: %.1f m" %
          (len(filas), peor))

    reporte, parques = huecos(filas)
    print("\nseparacion real entre vecinos de hilera:")
    for n0, n1, gap in reporte:
        marca = "  <- PARQUE" if gap >= GAP_PARQUE else ""
        print("   %-16s -> %-16s %6.1f m%s" % (n0, n1, gap, marca))

    ruta = os.path.join(AQUI, "campus_trazado.py")
    lp = ['    ("%s", "%s", %.0f, %.0f, %.1f),' % (n0, n1, cx, cy, gap)
          for n0, n1, cx, cy, gap in parques]
    with open(ruta, "w") as fh:
        fh.write(CABECERA + "\n".join(lineas) + "\n"
                 + PIE % (PLAZA[0], PLAZA[1], PLAZA[2], RIO, HOLGURA_RIO,
                          SEPARACION)
                 + "\n# Huecos entre vecinos >= %.0f m: candidatos a parque o\n"
                   "# plaza secundaria. (edificio antes, edificio despues,\n"
                   "# X del centro, Y del centro, ancho del hueco en m)\n"
                   "PARQUES = [\n%s\n]\n" % (GAP_PARQUE, "\n".join(lp)))
    print("-> %s  (%d parque(s) marcado(s))" % (ruta, len(parques)))


if __name__ == "__main__":
    main()
