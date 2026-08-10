"""Disena el rio sobre EL RECORRIDO DEL USUARIO, con el estilo de cauce que ya
validamos (lecho encajado, riberas que contienen el agua, cota descendente).

No se re-traza nada: se toman los puntos del spline original, se ordenan en un
solo sentido, se descartan los que retroceden y se recalculan cotas y seccion.
"""

import json
import math

BASE = r"C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
OLD = r"C:/Users/jeffa/Desktop/Proyecto/Proyecto-Memory/UnrealProject/Content/Python/claude_river/river_backup_estado_previo.json"
OUT = r"C:/Users/jeffa/AppData/Local/Temp/claude/river_plan_usuario.json"

D = json.load(open(BASE))
G, N, STEP, MINXY = D["grid"], D["n"], D["step"], D["min_xy"]
pts_old = json.load(open(OLD))["points_world"]

# parametros de cauce (los mismos que dieron el resultado que te gusto)
NPTS = 32
FREEBOARD = 190.0
BANK_MIN = 260.0
MIN_SLOPE = 0.0025
MAX_CUT = 950.0
BANK_OFFSETS = (300.0, 900.0, 1600.0)
W0, W1 = 380.0, 2350.0
D0, D1 = 95.0, 430.0


def terrain(x, y):
    fx, fy = (x - MINXY) / STEP, (y - MINXY) / STEP
    ix = max(0, min(N - 2, int(fx)))
    iy = max(0, min(N - 2, int(fy)))
    tx, ty = fx - ix, fy - iy
    a = G[iy][ix] * (1 - tx) + G[iy][ix + 1] * tx
    b = G[iy + 1][ix] * (1 - tx) + G[iy + 1][ix + 1] * tx
    return a * (1 - ty) + b * ty


# --- recorrido del usuario, en un solo sentido -------------------------------
# rama que arranca en su punto 49 (tile 7_0_0) y baja hasta el centro del mapa
legA = list(range(49, 26, -1))          # 49 .. 27
# cola de la otra rama, que lleva del centro a la desembocadura (tile 2_7_0)
legB = [11, 14, 15, 16, 17, 18, 19, 20, 21]
# se omiten 26, 12 y 13: retroceden sobre el propio recorrido
order = legA + legB

route = [[pts_old[i][0], pts_old[i][1]] for i in order]
print("puntos del usuario reutilizados: %d de %d" % (len(route), len(pts_old)))
print("  inicio  %s   (su punto 49)" % route[0])
print("  fin     %s   (su punto 21)" % route[-1])

# aviso si queda algun retroceso
back = 0
for i in range(1, len(route) - 1):
    ax = route[i][0] - route[i - 1][0]
    ay = route[i][1] - route[i - 1][1]
    bx = route[i + 1][0] - route[i][0]
    by = route[i + 1][1] - route[i][1]
    if ax * bx + ay * by < 0:
        back += 1
        print("  retroceso residual en el punto %d (%s)" % (i, route[i]))
print("retrocesos: %d" % back)


def arclen(p):
    a = [0.0]
    for i in range(1, len(p)):
        a.append(a[-1] + math.dist(p[i - 1], p[i]))
    return a


def smooth(p, w, passes):
    for _ in range(passes):
        q = [list(v) for v in p]
        for i in range(1, len(p) - 1):
            for k in (0, 1):
                q[i][k] = (1 - w) * p[i][k] + w * 0.5 * (p[i - 1][k] + p[i + 1][k])
        p = q
    return p


def resample(p, n):
    acc = arclen(p)
    total = acc[-1]
    out = []
    for i in range(n):
        t = total * i / (n - 1)
        j = 0
        while j < len(acc) - 2 and acc[j + 1] < t:
            j += 1
        seg = acc[j + 1] - acc[j]
        f = 0.0 if seg <= 0 else (t - acc[j]) / seg
        out.append([p[j][0] + f * (p[j + 1][0] - p[j][0]),
                    p[j][1] + f * (p[j + 1][1] - p[j][1])])
    return out


def perp(c, i):
    a = c[i - 1] if i > 0 else c[i]
    b = c[i + 1] if i < len(c) - 1 else c[i]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1.0
    return -ty / L, tx / L


# suavizado MUY leve: solo redondea los codos, conserva su trazado
center = resample(smooth(route, 0.22, 2), NPTS)

# --- meandros suaves, sin sacar el rio de la linea del usuario --------------
MEANDER_MAX_OFFSET = 2400.0   # desviacion maxima respecto a su trazado
MEANDER_MAX_RISE = 520.0      # no trepar lomas
MEANDER_MAX_PIT = 400.0       # no caer en hondonadas
BOUND = 47600.0


def add_meanders(c):
    n = len(c)
    acc = arclen(c)
    total = acc[-1]
    out = [list(v) for v in c]
    for i in range(1, n - 1):
        nx, ny = perp(c, i)
        s = acc[i]
        u = s / total
        amp = 500.0 + 1900.0 * (u ** 0.85)
        amp *= math.sin(math.pi * min(1.0, max(0.0, (u - 0.05) / 0.90))) ** 0.45
        amp = min(amp, MEANDER_MAX_OFFSET)
        off = (math.sin(2 * math.pi * s / 13000.0 + 0.6)
               + 0.40 * math.sin(2 * math.pi * s / 6000.0 + 2.3)) * amp / 1.40
        z0 = terrain(c[i][0], c[i][1])
        sgn = 1.0 if off >= 0 else -1.0
        k = min(abs(off), MEANDER_MAX_OFFSET)
        while k > 0:
            px = c[i][0] + nx * sgn * k
            py = c[i][1] + ny * sgn * k
            z = terrain(px, py)
            if (z - z0 <= MEANDER_MAX_RISE and z0 - z <= MEANDER_MAX_PIT
                    and abs(px) <= BOUND and abs(py) <= BOUND):
                break
            k -= 100.0
        k = max(0.0, k)
        out[i] = [c[i][0] + nx * sgn * k, c[i][1] + ny * sgn * k]
    return out


base_line = [list(v) for v in center]
center = add_meanders(center)
center = smooth(center, 0.25, 1)
center = resample(center, NPTS)
desvio = max(min(math.dist(p, q) for q in base_line) for p in center)
print("meandros anadidos: desviacion maxima respecto a tu trazado %.0f uu" % desvio)


acc = arclen(center)
total = acc[-1]
width = [W0 + (W1 - W0) * ((acc[i] / total) ** 0.62) for i in range(NPTS)]
depth = [D0 + (D1 - D0) * ((acc[i] / total) ** 0.75) for i in range(NPTS)]
terr = [terrain(x, y) for x, y in center]

# Ribera = la barrera mas alta que el agua encontraria al salir por cada
# margen, dentro de una franja proxima al cauce. Tomar el minimo de varias
# distancias (lo que hacia antes) hunde el perfil en cuanto hay un cortado
# lejano, aunque entre medias haya una loma que ya contiene el agua.
BANK_NEAR, BANK_FAR, BANK_STEP = 200.0, 1200.0, 100.0
bank = []
for i in range(NPTS):
    nx, ny = perp(center, i)
    hw = width[i] * 0.5
    sides = []
    for sgn in (1, -1):
        best = -1e9
        d = hw + BANK_NEAR
        while d <= hw + BANK_FAR:
            z = terrain(center[i][0] + nx * sgn * d, center[i][1] + ny * sgn * d)
            best = max(best, z)
            d += BANK_STEP
        sides.append(best)
    bank.append(min(sides))

def fill_sinks(v):
    """Rellena depresiones aisladas del perfil hasta el hombro mas bajo.

    Sin esto, un solo hoyo en el eje obliga a bajar la lamina y arrastra toda
    la excavacion aguas abajo: el rio acabaria en una zanja. Rellenandolo, el
    agua reposa sobre el hoyo (una poza) y el tallado levanta la ribera ahi.
    """
    f = list(v)
    for _ in range(400):
        changed = False
        for i in range(1, len(f) - 1):
            m = min(f[i - 1], f[i + 1])
            if f[i] < m - 1e-6:
                f[i] = m
                changed = True
        if not changed:
            break
    return f


terr_f = fill_sinks(terr)
bank_f = fill_sinks(bank)
cap = [min(terr_f[i] - FREEBOARD, bank_f[i] - BANK_MIN) for i in range(NPTS)]
water = []
for i in range(NPTS):
    water.append(cap[i] if i == 0
                 else min(cap[i], water[-1] - MIN_SLOPE * (acc[i] - acc[i - 1])))
for _ in range(80):
    for i in range(1, NPTS - 1):
        cand = 0.5 * (water[i - 1] + water[i + 1])
        lo = water[i + 1] + MIN_SLOPE * (acc[i + 1] - acc[i])
        hi = water[i - 1] - MIN_SLOPE * (acc[i] - acc[i - 1])
        if lo > hi:
            continue
        top = min(hi, cap[i])
        bot = max(lo, min(top, terr[i] - MAX_CUT))
        water[i] = max(bot, min(top, cand)) if bot <= top else max(lo, min(hi, cand))

bed = [water[i] - depth[i] for i in range(NPTS)]
vel = []
for i in range(NPTS):
    grad = 0.0 if i == 0 else (water[i - 1] - water[i]) / max(1.0, acc[i] - acc[i - 1])
    vel.append(max(80.0, min(340.0, 90.0 + 5200.0 * grad)))
vel[0] = vel[1]
for _ in range(3):
    vel = [vel[0]] + [0.25 * vel[i - 1] + 0.5 * vel[i] + 0.25 * vel[i + 1]
                      for i in range(1, NPTS - 1)] + [vel[-1]]

print("\nlongitud %.0f uu (%.2f km)  recta %.0f  sinuosidad %.2f"
      % (total, total / 1e5, math.dist(center[0], center[-1]),
         total / math.dist(center[0], center[-1])))
print("\n  i     X         Y      terreno   ribera     agua     lecho  ribera-agua  anch  prof  vel")
for i in range(NPTS):
    print("%3d %9.0f %9.0f %9.1f %9.1f %9.1f %9.1f %10.1f %6.0f %5.0f %4.0f"
          % (i, center[i][0], center[i][1], terr[i], bank[i], water[i], bed[i],
             bank[i] - water[i], width[i], depth[i], vel[i]))

drops = [water[i] - water[i + 1] for i in range(NPTS - 1)]
print("\ndesnivel %.0f uu (%.1f m)  pendiente %.2f%%  caida max/tramo %.0f"
      % (water[0] - water[-1], (water[0] - water[-1]) / 100.0,
         100.0 * (water[0] - water[-1]) / total, max(drops)))
print("monotono estricto:", all(d > 0 for d in drops))
print("ribera minima: %.0f uu" % min(bank[i] - water[i] for i in range(NPTS)))
cuts = [max(0.0, terr[i] - water[i]) for i in range(NPTS)]
fills = [max(0.0, water[i] - terr[i]) for i in range(NPTS)]
print("corte    max %.0f uu  medio %.0f uu" % (max(cuts), sum(cuts) / NPTS))
print("relleno  max %.0f uu  puntos con relleno >60: %d"
      % (max(fills), sum(1 for f in fills if f > 60)))

# distancia al centro del mapa
dmin = min(math.hypot(x, y) for x, y in center)
print("distancia minima al centro del mapa: %.0f uu" % dmin)

json.dump(dict(center=center, water=water, bed=bed, terrain=terr, bank=bank,
               width=width, depth=depth, velocity=vel, length=total, acc=acc),
          open(OUT, "w"))
print("\nOK ->", OUT)
