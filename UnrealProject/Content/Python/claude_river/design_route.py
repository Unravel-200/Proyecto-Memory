"""Diseno del rio: nacimiento en el tile 7_0_0, desembocadura en el 2_7_0.

Criterio hidrologico: la ruta minimiza la barrera maxima que hay que atravesar
(inundacion por prioridad desde la desembocadura), lo que equivale a seguir el
drenaje natural con la minima excavacion. El perfil de agua se toma del propio
campo de barrera, garantizando descenso monotono -> un unico sentido de flujo.

Produce river_plan.json. No toca el editor.
"""

import heapq
import json
import math

SRC = r"C:/Users/jeffa/AppData/Local/Temp/claude/terrain_base.json"
OUT = r"C:/Users/jeffa/AppData/Local/Temp/claude/river_plan.json"

D = json.load(open(SRC))
G = D["grid"]
N = D["n"]
STEP = D["step"]
MIN = D["min_xy"]

TILE = 12600.0
BASE = -50400.0
MARGIN = 2
BOUND = 47600.0
INF = float("inf")

# parametros del rio
NPTS = 34
FREEBOARD = 190.0        # incision del agua bajo la cota de vertido
MIN_SLOPE = 0.0025       # pendiente minima -> nunca se estanca ni se invierte
MAX_CUT = 950.0          # excavacion maxima deseable bajo el terreno
BANK_MIN = 260.0         # ribera minima por encima del agua -> no se desborda
W_PIT = 5.0              # rechazo a las cubetas cerradas
MEANDER_MAX_RISE = 380.0
MEANDER_MAX_PIT = 240.0


def to_world(ix, iy):
    return MIN + ix * STEP, MIN + iy * STEP


def clamp_xy(p):
    return [max(-BOUND, min(BOUND, p[0])), max(-BOUND, min(BOUND, p[1]))]


def bilerp(F, x, y, fallback=None):
    fx = (x - MIN) / STEP
    fy = (y - MIN) / STEP
    ix = max(0, min(N - 2, int(fx)))
    iy = max(0, min(N - 2, int(fy)))
    tx, ty = fx - ix, fy - iy
    v = [F[iy][ix], F[iy][ix + 1], F[iy + 1][ix], F[iy + 1][ix + 1]]
    if any(q == INF for q in v):
        return fallback
    a = v[0] * (1 - tx) + v[1] * tx
    b = v[2] * (1 - tx) + v[3] * tx
    return a * (1 - ty) + b * ty


def terrain(x, y):
    return bilerp(G, x, y)


# ---------- desembocadura: lo mas bajo del tile 2_7_0 junto al borde este ----------
ex0, ex1 = BASE + 2 * TILE, BASE + 3 * TILE
ey0, ey1 = BASE + 7 * TILE, BASE + 8 * TILE
cands = []
for iy in range(MARGIN, N - MARGIN):
    for ix in range(MARGIN, N - MARGIN):
        x, y = to_world(ix, iy)
        if ex0 <= x <= ex1 and ey0 <= y <= ey1 and y >= ey1 - 3 * STEP:
            cands.append((G[iy][ix], ix, iy))
cands.sort()
_, exi, eyi = cands[0]

# ---------- inundacion por prioridad (minimax) desde la desembocadura ----------
NB = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
BUCKET = 40.0

bar = [[INF] * N for _ in range(N)]
dst = [[INF] * N for _ in range(N)]
nxt = [[None] * N for _ in range(N)]
bar[eyi][exi] = G[eyi][exi]
dst[eyi][exi] = 0.0
pq = [(math.floor(G[eyi][exi] / BUCKET), 0.0, exi, eyi)]
while pq:
    bq, d, ix, iy = heapq.heappop(pq)
    if (bq, d) > (math.floor(bar[iy][ix] / BUCKET), dst[iy][ix]):
        continue
    for dx, dy in NB:
        jx, jy = ix + dx, iy + dy
        if not (MARGIN <= jx < N - MARGIN and MARGIN <= jy < N - MARGIN):
            continue
        nb = max(bar[iy][ix], G[jy][jx])
        nd = d + STEP * math.hypot(dx, dy) + W_PIT * (nb - G[jy][jx])
        key_old = (INF if bar[jy][jx] == INF else math.floor(bar[jy][jx] / BUCKET),
                   dst[jy][jx])
        if (math.floor(nb / BUCKET), nd) < key_old:
            bar[jy][jx] = nb
            dst[jy][jx] = nd
            nxt[jy][jx] = (ix, iy)
            heapq.heappush(pq, (math.floor(nb / BUCKET), nd, jx, jy))


def barrier(x, y):
    return bilerp(bar, x, y, fallback=terrain(x, y))


# ---------- nacimiento: lo mas alto del tile 7_0_0 que drena sin barrera ----------
sx0, sx1 = BASE + 7 * TILE, BASE + 8 * TILE
sy0, sy1 = BASE + 0 * TILE, BASE + 1 * TILE
def enclosure(x, y, radius=1100.0, samples=16):
    """Fraccion del anillo alrededor de (x,y) que esta mas alto.
    Alto => cabecera de vaguada; bajo => cumbre o espolon."""
    z0 = terrain(x, y)
    higher = 0
    for k in range(samples):
        a = 2 * math.pi * k / samples
        if terrain(x + radius * math.cos(a), y + radius * math.sin(a)) > z0:
            higher += 1
    return higher / samples


pool = []
for iy in range(MARGIN, N - MARGIN):
    for ix in range(MARGIN, N - MARGIN):
        x, y = to_world(ix, iy)
        if sx0 <= x <= sx1 and sy0 <= y <= sy1 and bar[iy][ix] < INF:
            pool.append((bar[iy][ix] - G[iy][ix], -G[iy][ix], ix, iy, x, y, G[iy][ix]))
pool.sort()
# de los que drenan sin barrera, el mas alto que ademas este encajonado: un
# manantial en cumbre no contiene el agua, tiene que nacer en una vaguada
drenan = [p for p in pool if p[0] <= 1.0] or pool[:40]
best = None
for p in drenan:
    enc = enclosure(p[4], p[5])
    if enc >= 0.45 and (best is None or p[6] > best[1]):
        best = (p, p[6], enc)
if best is None:
    best = (drenan[0], drenan[0][6], enclosure(drenan[0][4], drenan[0][5]))
p, sz, enc = best
excess, _, sxi, syi, sxw, syw, _ = p
print("NACIMIENTO     (%.0f, %.0f)  terreno %.0f  exceso %.1f  encajonamiento %.2f"
      % (sxw, syw, sz, excess, enc))
print("DESEMBOCADURA  (%.0f, %.0f)  terreno %.0f            [tile 2_7_0]"
      % (to_world(exi, eyi) + (G[eyi][exi],)))

# ---------- eje bruto ----------
raw = []
cur = (sxi, syi)
for _ in range(100000):
    raw.append(to_world(*cur))
    if cur == (exi, eyi):
        break
    cur = nxt[cur[1]][cur[0]]
    if cur is None:
        break
print("celdas del eje:", len(raw))


def smooth(p, w=0.5, passes=1):
    for _ in range(passes):
        q = [list(v) for v in p]
        for i in range(1, len(p) - 1):
            for k in (0, 1):
                q[i][k] = (1 - w) * p[i][k] + w * 0.5 * (p[i - 1][k] + p[i + 1][k])
        p = q
    return p


def perp(p, i):
    ax, ay = p[i - 1][0], p[i - 1][1]
    bx, by = p[i + 1][0], p[i + 1][1]
    tx, ty = bx - ax, by - ay
    L = math.hypot(tx, ty)
    if L < 1e-6:
        return None
    return -ty / L, tx / L


def snap_to_valley(p, reach=1400.0, frac=0.45):
    q = [list(v) for v in p]
    for i in range(1, len(p) - 1):
        nv = perp(p, i)
        if nv is None:
            continue
        nx, ny = nv
        best, bz = 0.0, terrain(p[i][0], p[i][1])
        s = -reach
        while s <= reach:
            zz = terrain(p[i][0] + nx * s, p[i][1] + ny * s)
            if zz < bz:
                bz, best = zz, s
            s += 140.0
        q[i] = clamp_xy([p[i][0] + nx * best * frac, p[i][1] + ny * best * frac])
    return q


pts = [list(v) for v in raw]
for _ in range(12):
    pts = smooth(pts, 0.5, 2)
    pts = snap_to_valley(pts)
pts = smooth(pts, 0.5, 6)

# prolongar hasta el borde este del mapa
last, prev_ = pts[-1], pts[-3]
dx, dy = last[0] - prev_[0], last[1] - prev_[1]
if dy > 1e-6:
    t = (50400.0 - last[1]) / dy
    if 0 < t < 6:
        pts.append([last[0] + dx * t, 50400.0])


def arclen(p):
    acc = [0.0]
    for i in range(1, len(p)):
        acc.append(acc[-1] + math.dist(p[i - 1], p[i]))
    return acc


def resample_by_slope(p, n, k=9.0):
    """Concentra puntos donde el terreno cae con fuerza."""
    acc_c = [0.0]
    for i in range(1, len(p)):
        acc_c.append(acc_c[-1] + math.dist(p[i - 1], p[i])
                     + k * abs(terrain(*p[i]) - terrain(*p[i - 1])))
    total_c = acc_c[-1]
    out = []
    for i in range(n):
        t = total_c * i / (n - 1)
        j = 0
        while j < len(acc_c) - 2 and acc_c[j + 1] < t:
            j += 1
        seg = acc_c[j + 1] - acc_c[j]
        f = 0.0 if seg <= 0 else (t - acc_c[j]) / seg
        out.append([p[j][0] + f * (p[j + 1][0] - p[j][0]),
                    p[j][1] + f * (p[j + 1][1] - p[j][1])])
    return out


center = resample_by_slope(pts, NPTS)


def add_meanders(c):
    n = len(c)
    acc = arclen(c)
    total = acc[-1]
    out = [list(v) for v in c]
    for i in range(1, n - 1):
        nv = perp(c, i)
        if nv is None:
            continue
        nx, ny = nv
        s = acc[i]
        u = s / total
        amp = 300.0 + 1250.0 * (u ** 1.1)
        amp *= math.sin(math.pi * min(1.0, max(0.0, (u - 0.04) / 0.92))) ** 0.5
        off = (math.sin(2 * math.pi * s / 17000.0 + 0.7)
               + 0.42 * math.sin(2 * math.pi * s / 7600.0 + 2.1)) * amp / 1.42
        floor_z = terrain(c[i][0], c[i][1])
        sgn = 1.0 if off >= 0 else -1.0
        k = abs(off)
        while k > 0:
            px, py = c[i][0] + nx * sgn * k, c[i][1] + ny * sgn * k
            zz = terrain(px, py)
            if zz - floor_z <= MEANDER_MAX_RISE and barrier(px, py) - zz <= MEANDER_MAX_PIT:
                break
            k -= 120.0
        out[i] = clamp_xy([c[i][0] + nx * sgn * max(0.0, k),
                           c[i][1] + ny * sgn * max(0.0, k)])
    return out


center = add_meanders(center)
center = smooth(center, 0.30, 2)
center = add_meanders(center)


# ---------- perfil longitudinal ----------
def river_width(u):
    return 380.0 + (2350.0 - 380.0) * (u ** 0.62)


def compute_profile(c):
    acc = arclen(c)
    total = acc[-1]
    terr = [terrain(x, y) for x, y in c]
    bars = [barrier(x, y) for x, y in c]

    # cota de ribera: terreno en los bordes del cauce, no en el eje (el eje es
    # la vaguada y puede ir hundido sin que el agua se desborde)
    bank = []
    for i in range(len(c)):
        off = river_width(acc[i] / total) * 0.5 + 300.0
        nv = perp(c, i) if 0 < i < len(c) - 1 else perp(c, min(max(i, 1), len(c) - 2))
        if nv is None:
            bank.append(terr[i])
            continue
        nx, ny = nv
        bank.append(min(terrain(c[i][0] + nx * off, c[i][1] + ny * off),
                        terrain(c[i][0] - nx * off, c[i][1] - ny * off)))

    # techo por punto: ni por encima de la cota de vertido menos el resguardo,
    # ni tan alto que la ribera no contenga el agua
    cap = [min(bars[i] - FREEBOARD, bank[i] - BANK_MIN) for i in range(len(c))]
    water = []
    for i in range(len(c)):
        water.append(cap[i] if i == 0
                     else min(cap[i], water[-1] - MIN_SLOPE * (acc[i] - acc[i - 1])))
    for _ in range(80):
        for i in range(1, len(c) - 1):
            cand = 0.5 * (water[i - 1] + water[i + 1])
            lo = water[i + 1] + MIN_SLOPE * (acc[i + 1] - acc[i])
            hi = water[i - 1] - MIN_SLOPE * (acc[i] - acc[i - 1])
            if lo > hi:
                continue
            top = min(hi, cap[i])
            bot = max(lo, min(top, terr[i] - MAX_CUT))
            water[i] = (max(bot, min(top, cand)) if bot <= top
                        else max(lo, min(hi, cand)))
    return acc, terr, bars, water, bank


def nudge_to_drainage(c, bars, reach=1500.0, frac=0.55):
    """Lleva el eje hacia la superficie de drenaje natural: ni metido en
    cubetas cerradas (que hundirian el perfil) ni trepando lomas."""
    q = [list(v) for v in c]
    for i in range(1, len(c) - 1):
        nv = perp(c, i)
        if nv is None:
            continue
        nx, ny = nv
        ref = bars[i]
        best_s, best_pen = 0.0, None
        s = -reach
        while s <= reach:
            zz = terrain(c[i][0] + nx * s, c[i][1] + ny * s)
            pen = (1.6 * max(0.0, ref - zz)      # hundido = cubeta
                   + 1.2 * max(0.0, zz - ref)    # elevado = loma
                   + 0.05 * abs(s))              # no alejarse sin motivo
            if best_pen is None or pen < best_pen:
                best_pen, best_s = pen, s
            s += 100.0
        q[i] = clamp_xy([c[i][0] + nx * best_s * frac,
                         c[i][1] + ny * best_s * frac])
    return q


for _ in range(4):
    acc, terr, bars, water, bank = compute_profile(center)
    center = nudge_to_drainage(center, bars)
    center = smooth(center, 0.25, 1)
acc, terr, bars, water, bank = compute_profile(center)

total_len = acc[-1]
straight = math.dist(center[0], center[-1])

# ---------- anchura / profundidad / velocidad ----------
width, depth, vel, bed = [], [], [], []
for i in range(NPTS):
    u = acc[i] / total_len
    width.append(380.0 + (2350.0 - 380.0) * (u ** 0.62))
    depth.append(95.0 + (430.0 - 95.0) * (u ** 0.75))
    grad = 0.0 if i == 0 else (water[i - 1] - water[i]) / max(1.0, acc[i] - acc[i - 1])
    vel.append(max(80.0, min(340.0, 90.0 + 5200.0 * grad)))
    bed.append(water[i] - depth[i])
vel[0] = vel[1]
for _ in range(3):
    vel = [vel[0]] + [0.25 * vel[i - 1] + 0.5 * vel[i] + 0.25 * vel[i + 1]
                      for i in range(1, NPTS - 1)] + [vel[-1]]

print("\nlongitud %.0f uu (%.2f km)   recta %.0f   sinuosidad %.2f"
      % (total_len, total_len / 100000.0, straight, total_len / straight))
print("\n  i     X         Y      terreno   ribera     agua     lecho  ribera-agua  anch  prof  vel")
for i in range(NPTS):
    fb = bank[i] - water[i]
    flag = "  <-- ribera baja" if fb < 200 else ("  <-- corte hondo" if terr[i] - water[i] > 750 else "")
    print("%3d %9.0f %9.0f %9.1f %9.1f %9.1f %9.1f %10.1f %6.0f %5.0f %4.0f%s"
          % (i, center[i][0], center[i][1], terr[i], bank[i], water[i], bed[i],
             fb, width[i], depth[i], vel[i], flag))

drops = [water[i] - water[i + 1] for i in range(NPTS - 1)]
fills = [max(0.0, water[i] - terr[i]) for i in range(NPTS)]
cuts = [max(0.0, terr[i] - water[i]) for i in range(NPTS)]
print("\ndesnivel %.0f uu (%.1f m)  pendiente media %.2f%%  caida max/tramo %.0f"
      % (water[0] - water[-1], (water[0] - water[-1]) / 100.0,
         100.0 * (water[0] - water[-1]) / total_len, max(drops)))
print("monotono estricto:", all(d > 0 for d in drops))
print("relleno  max %.0f uu   puntos con relleno >60: %d"
      % (max(fills), sum(1 for f in fills if f > 60)))
print("corte    max %.0f uu   medio %.0f uu" % (max(cuts), sum(cuts) / len(cuts)))
mb = min(bank[i] - water[i] for i in range(NPTS))
print("ribera minima sobre el agua: %.0f uu (%.2f m)" % (mb, mb / 100.0))

json.dump({"center": center, "water": water, "bed": bed, "terrain": terr,
           "bank": bank, "width": width, "depth": depth, "velocity": vel,
           "length": total_len, "arc": acc}, open(OUT, "w"))
print("\nOK ->", OUT)
