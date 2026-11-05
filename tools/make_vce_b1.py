# IsoRim Waylith - Vanilla Chemfuel Expanded Pack, model batch B1 (phase 1, Blender preview round 1).
# Low-poly models of VCE's art, 128 px a cell, built from a per-shape art analysis (parts, footprint, heights; in the phase 1 report).
# Self-contained, no Blender needed: writes Models/*.obj (with vt) and Models/vce_b1.mtl.
# Game axes while building: x east, y up, z north, one cell a unit, origin = footprint centre on the ground, facing north.
# OBJ stores z flipped (IsoRim's rule). Decals (paint) are single sheets lifted 0.004 off a face: no outline, no shell.
# usage: <Blender>\5.2\python\bin\python.exe -I make_vce_b1.py <abs Models dir>
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Models')
os.makedirs(OUT, exist_ok=True)
LIB = 'vce_b1.mtl'
LIFT = 0.004
STOREY = 1.60

METAL = 'IsoRim/Swatches/Metal'
# name: (Kd, metal swatch?). Kd sampled from VCE's textures; paint (decals) has no swatch.
MATS = {
    # chemfuel tank
    'vce_ct_red': ((0.37, 0.19, 0.19), True), 'vce_ct_panel': ((0.29, 0.15, 0.15), False),
    'vce_ct_strap': ((0.40, 0.38, 0.37), True), 'vce_ct_plate': ((0.52, 0.49, 0.48), True),
    'vce_ct_fan': ((0.33, 0.38, 0.33), False), 'vce_ct_blade': ((0.56, 0.54, 0.52), False),
    # deepchem tank
    'vce_dt_body': ((0.28, 0.28, 0.28), True), 'vce_dt_collar': ((0.33, 0.33, 0.33), True),
    'vce_dt_end': ((0.16, 0.16, 0.16), False), 'vce_dt_plate': ((0.25, 0.25, 0.25), False),
    'vce_dt_hub': ((0.42, 0.42, 0.41), True), 'vce_dt_foot': ((0.30, 0.12, 0.12), True),
    # tap and drain, chemfuel / deepchem
    'vce_hc_frame': ((0.39, 0.20, 0.22), True), 'vce_hc_front': ((0.26, 0.13, 0.13), True),
    'vce_hc_wall': ((0.29, 0.16, 0.16), False), 'vce_hc_floor': ((0.52, 0.49, 0.48), True),
    'vce_hc_halo': ((0.44, 0.41, 0.40), False), 'vce_hc_ring': ((0.26, 0.21, 0.21), False), 'vce_hc_dial': ((0.60, 0.57, 0.56), False),
    'vce_hc_slopeN': ((0.45, 0.43, 0.42), True), 'vce_hc_slopeW': ((0.52, 0.49, 0.48), True), 'vce_hc_grate': ((0.33, 0.29, 0.29), False), 'vce_hc_hole': ((0.20, 0.17, 0.17), False),
    'vce_hd_frame': ((0.42, 0.26, 0.23), True), 'vce_hd_front': ((0.19, 0.08, 0.09), True),
    'vce_hd_wall': ((0.25, 0.10, 0.11), False), 'vce_hd_floor': ((0.30, 0.29, 0.27), True),
    'vce_hd_halo': ((0.36, 0.34, 0.33), False), 'vce_hd_ring': ((0.24, 0.20, 0.20), False), 'vce_hd_dial': ((0.54, 0.51, 0.50), False),
    'vce_hd_slopeN': ((0.22, 0.22, 0.21), True), 'vce_hd_slopeW': ((0.29, 0.28, 0.27), True), 'vce_hd_grate': ((0.17, 0.16, 0.16), False), 'vce_hd_hole': ((0.09, 0.09, 0.09), False),
    # valves
    'vce_vc_pipe': ((0.55, 0.35, 0.33), True), 'vce_vc_body': ((0.42, 0.26, 0.26), True), 'vce_vc_dome': ((0.50, 0.36, 0.35), True),
    'vce_vc_collar': ((0.47, 0.30, 0.29), True), 'vce_vc_stem': ((0.30, 0.17, 0.17), False),
    'vce_vc_disc': ((0.50, 0.34, 0.33), True), 'vce_vc_cut': ((0.30, 0.15, 0.15), False), 'vce_vc_hub': ((0.46, 0.30, 0.29), True),
    'vce_vd_pipe': ((0.31, 0.31, 0.31), True), 'vce_vd_body': ((0.25, 0.22, 0.22), True), 'vce_vd_dome': ((0.35, 0.31, 0.31), True),
    'vce_vd_collar': ((0.37, 0.15, 0.15), True), 'vce_vd_stem': ((0.26, 0.26, 0.26), False),
    'vce_vd_disc': ((0.41, 0.18, 0.19), True), 'vce_vd_cut': ((0.20, 0.19, 0.20), False), 'vce_vd_hub': ((0.34, 0.34, 0.34), True),
    # refinery
    'vce_rf_plinth': ((0.33, 0.18, 0.18), True), 'vce_rf_plinthF': ((0.24, 0.10, 0.10), True), 'vce_rf_inset': ((0.25, 0.09, 0.09), False),
    'vce_rf_hood': ((0.53, 0.53, 0.53), True), 'vce_rf_block': ((0.46, 0.46, 0.46), True), 'vce_rf_silo': ((0.56, 0.56, 0.56), True),
    'vce_rf_chim': ((0.24, 0.24, 0.24), True), 'vce_rf_collar': ((0.45, 0.45, 0.45), True), 'vce_rf_rim': ((0.30, 0.30, 0.30), True),
    'vce_rf_mouth': ((0.07, 0.07, 0.07), False), 'vce_rf_vent': ((0.46, 0.45, 0.44), False), 'vce_rf_slat': ((0.26, 0.27, 0.26), False),
    'vce_rf_rad': ((0.50, 0.50, 0.49), True), 'vce_rf_rib': ((0.40, 0.40, 0.40), False),
    'vce_rf_manT': ((0.42, 0.42, 0.42), True), 'vce_rf_manB': ((0.37, 0.37, 0.37), True), 'vce_rf_manF': ((0.34, 0.34, 0.34), True),
    'vce_rf_pad': ((0.52, 0.50, 0.48), True), 'vce_rf_finL': ((0.64, 0.64, 0.63), True), 'vce_rf_finD': ((0.34, 0.34, 0.34), True),
    'vce_rf_neck': ((0.30, 0.30, 0.30), True), 'vce_rf_pipeD': ((0.27, 0.27, 0.27), True), 'vce_rf_flangeD': ((0.36, 0.11, 0.11), True),
    'vce_rf_pipeC': ((0.50, 0.31, 0.29), True), 'vce_rf_flangeC': ((0.56, 0.38, 0.33), True),
    # pumpjack
    'vce_pj_slab': ((0.32, 0.17, 0.17), True), 'vce_pj_pit': ((0.11, 0.11, 0.11), False), 'vce_pj_plate': ((0.52, 0.52, 0.52), True),
    'vce_pj_plateF': ((0.25, 0.27, 0.28), True), 'vce_pj_hoodA': ((0.34, 0.34, 0.34), True), 'vce_pj_hoodB': ((0.28, 0.28, 0.28), True),
    'vce_pj_hoodT': ((0.36, 0.36, 0.36), True), 'vce_pj_face': ((0.21, 0.21, 0.21), True), 'vce_pj_arch': ((0.12, 0.12, 0.12), False),
    'vce_pj_guide': ((0.41, 0.41, 0.41), False), 'vce_pj_ramp': ((0.31, 0.31, 0.31), True), 'vce_pj_rampC': ((0.40, 0.40, 0.40), False),
    'vce_pj_pipe': ((0.28, 0.28, 0.28), True), 'vce_pj_flange': ((0.36, 0.36, 0.36), True),
    'vce_pj_head': ((0.44, 0.27, 0.27), True), 'vce_pj_slot': ((0.27, 0.26, 0.26), False), 'vce_pj_collar': ((0.36, 0.18, 0.19), True),
    'vce_pj_ribL': ((0.42, 0.23, 0.25), True), 'vce_pj_ribD': ((0.31, 0.15, 0.16), True), 'vce_pj_grey': ((0.36, 0.36, 0.36), True),
    'vce_pj_ring': ((0.17, 0.17, 0.17), False), 'vce_pj_rod': ((0.32, 0.32, 0.32), True),
    # deepchem item
    'vce_it_body': ((0.36, 0.14, 0.15), False), 'vce_it_hoop': ((0.24, 0.09, 0.09), False), 'vce_it_lid': ((0.42, 0.20, 0.21), False),
    'vce_it_cap': ((0.36, 0.37, 0.36), False), 'vce_it_mark': ((0.24, 0.09, 0.09), False),
}


def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a):
    l = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NZ = (0, 0, -1)


class Shell:
    def __init__(self, m):
        self.m, self.key, self.faces = m, {}, []

    def vert(self, p):
        k = (round(p[0], 5), round(p[1], 5), round(p[2], 5))
        if k not in self.key:
            self.key[k] = len(self.m.v)
            self.m.v.append(tuple(float(x) for x in k))
        return self.key[k]

    def face(self, pts, mat):
        idx = []
        for p in pts:
            i = self.vert(p)
            if not idx or idx[-1] != i:
                idx.append(i)
        if len(idx) > 1 and idx[0] == idx[-1]:
            idx.pop()
        if len(idx) >= 3:
            self.faces.append((tuple(idx), mat))


class Model:
    def __init__(self, name):
        self.name = name
        self.shells, self.v, self.sheets = [], [], []

    def shell(self):
        s = Shell(self)
        self.shells.append(s)
        return s

    def decal(self, pts, mat, n, lift=LIFT):
        """A flat sheet on a face: pts convex, n the face's outward normal, lifted along it."""
        n = norm(n)
        self.sheets.append(([add(p, mul(n, lift)) for p in pts], mat, n))

    def disc(self, c, u, v, n, r, mat, k=16, lift=LIFT, ry=None):
        ry = r if ry is None else ry
        pts = [add(add(c, mul(u, r * math.cos(2 * math.pi * i / k))), mul(v, ry * math.sin(2 * math.pi * i / k))) for i in range(k)]
        self.decal(pts, mat, n, lift)

    def rect(self, c, u, v, n, hu, hv, mat, lift=LIFT):
        pts = [add(add(c, mul(u, a * hu)), mul(v, b * hv)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        self.decal(pts, mat, n, lift)


def loft(m, rings, matfn, cap0=None, cap1=None):
    """Closed shell through rings of equal length. matfn(i, j): band i, edge j. cap0 / cap1: materials of the end caps."""
    s = m.shell()
    k = len(rings[0])
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        for j in range(k):
            s.face([a[j], a[(j + 1) % k], b[(j + 1) % k], b[j]], matfn(i, j))
    if cap0:
        s.face(list(reversed(rings[0])), cap0)
    if cap1:
        s.face(rings[-1], cap1)
    return s


def plan(poly, y):
    return [(p[0], y, p[1]) for p in poly]


def prism(m, poly, y0, y1, side, top, bevel=0.0):
    """Plan polygon (x, z) from y0 to y1, closed. bevel: top edge pulled in by about that much (convex polygons)."""
    rings = [plan(poly, y0)]
    if bevel:
        cx = sum(p[0] for p in poly) / len(poly)
        cz = sum(p[1] for p in poly) / len(poly)
        ins = []
        for p in poly:
            dx, dz = p[0] - cx, p[1] - cz
            l = math.hypot(dx, dz)
            ins.append((p[0] - dx / l * bevel * 1.3, p[1] - dz / l * bevel * 1.3))
        rings += [plan(poly, y1 - bevel), plan(ins, y1)]
    else:
        rings.append(plan(poly, y1))
    return loft(m, rings, lambda i, j: side, cap0=side, cap1=top)


def rectp(x0, x1, z0, z1, c=0.0):
    if not c:
        return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    return [(x0 + c, z0), (x1 - c, z0), (x1, z0 + c), (x1, z1 - c), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c), (x0, z0 + c)]


def box(m, x0, x1, y0, y1, z0, z1, side, top=None, c=0.0, bevel=0.0):
    return prism(m, rectp(x0, x1, z0, z1, c), y0, y1, side, top or side, bevel)


def lathe(m, cx, cz, prof, n=12, phase=0.0, matfn=None):
    """Upright turned shape. prof: (r, y, mat of the band above this point). A last r > 0 gets a cap in its mat."""
    rings = []
    for r, y, _ in prof:
        rings.append([(cx + r * math.cos(phase + 2 * math.pi * j / n), y, cz + r * math.sin(phase + 2 * math.pi * j / n)) for j in range(n)])
    f = matfn or (lambda i, j: prof[i][2])
    return loft(m, rings, f, cap0=(prof[0][2] if prof[0][0] > 0 else None), cap1=(prof[-1][2] if prof[-1][0] > 0 else None))


def tube(m, path, r, mat, n=6):
    """Pipe along a polyline, mitred at the bends, closed at both ends."""
    t0 = norm(sub(path[1], path[0]))
    up = Y if abs(dot(t0, Y)) < 0.9 else X
    u = norm(cross(t0, up))
    v = norm(cross(u, t0))
    ring = [add(path[0], add(mul(u, r * math.cos(2 * math.pi * j / n + math.pi / n)), mul(v, r * math.sin(2 * math.pi * j / n + math.pi / n)))) for j in range(n)]
    rings = [ring]
    for i in range(1, len(path)):
        d = norm(sub(path[i], path[i - 1]))
        pn = norm(add(d, norm(sub(path[i + 1], path[i])))) if i + 1 < len(path) else d
        rings.append([add(p, mul(d, dot(sub(path[i], p), pn) / dot(d, pn))) for p in rings[-1]])
    return loft(m, rings, lambda i, j: mat, cap0=mat, cap1=mat)


# ---------------- tanks
def tank_chem():
    m = Model('vce_tank_chem')
    W, H, L, C, E = 0.90, 1.05, 1.41, 0.10, 0.09
    straps = (-0.94, 0.0, 0.94)
    SW = 0.055

    def sec(z, w, h):
        return [(-w, 0, z), (w, 0, z), (w, h - C, z), (w - C, h, z), (-w + C, h, z), (-w, h - C, z)]
    rings, kinds = [sec(-L, W - E, H - 0.07)], ['red']
    rings.append(sec(-L + E, W, H)); kinds.append('red')
    for c in straps:
        rings.append(sec(c - SW, W, H)); kinds.append('strap')
        rings.append(sec(c - SW, W + 0.02, H + 0.02)); kinds.append('strap')
        rings.append(sec(c + SW, W + 0.02, H + 0.02)); kinds.append('strap')
        rings.append(sec(c + SW, W, H)); kinds.append('red')
    rings.append(sec(L - E, W, H)); kinds.append('red')
    rings.append(sec(L, W - E, H - 0.07))
    loft(m, rings, lambda i, j: 'vce_ct_strap' if kinds[i] == 'strap' else 'vce_ct_red', cap0='vce_ct_red', cap1='vce_ct_red')
    # raised panels on the top, between the straps (paint)
    for z0, z1 in ((-1.30, -1.03), (-0.84, -0.09), (0.09, 0.84), (1.03, 1.30)):
        m.rect((0, H, (z0 + z1) / 2), X, Z, Y, 0.62, (z1 - z0) / 2, 'vce_ct_panel')

    # arch plates: three on each long side (at the straps), one on each end; the middle ones carry the fan
    outline = [(-0.23, 0.0), (0.23, 0.0)] + [(0.23 * math.cos(math.pi * i / 5), 0.50 + 0.23 * math.sin(math.pi * i / 5)) for i in range(0, 6)]

    def plate(place, t0, t1, fan, n, u):
        loft(m, [[place(a, b, t0) for a, b in outline], [place(a, b, t1) for a, b in outline]], lambda i, j: 'vce_ct_plate', cap0='vce_ct_plate', cap1='vce_ct_plate')
        if fan:
            c = place(0, 0.40, t1)
            m.disc(c, u, Y, n, 0.17, 'vce_ct_fan', k=14)
            for q in range(4):
                a0 = math.radians(20 + 90 * q)
                a1 = a0 + math.radians(48)
                pp = [add(add(c, mul(u, r * math.cos(a))), mul(Y, r * math.sin(a))) for r, a in ((0.045, a0), (0.145, a0), (0.145, a1), (0.045, a1))]
                m.decal(pp, 'vce_ct_blade', n, lift=2 * LIFT)
            m.disc(c, u, Y, n, 0.04, 'vce_ct_blade', k=8, lift=2 * LIFT)

    for sgn in (1, -1):
        for zc in straps:
            plate(lambda a, b, t: (sgn * t, b, zc + a), W - 0.01, 0.96, zc == 0.0, (sgn, 0, 0), Z)
        plate(lambda a, b, t: (a, b, sgn * t), L - 0.03, 1.465, True, (0, 0, sgn), X)
    return m


def tank_deep():
    """A lying round tank sunk into a flat base: round sections, cut by a chord inside the base, so nothing goes below ground."""
    m = Model('vce_tank_deep')
    CY, N = 0.665, 16      # axis height: collar top 1.595, under the storey
    BASE, CUT = 0.24, 0.12  # base top; the chord closing each section, hidden in the base
    RC, RM, RE = 0.93, 0.86, 0.86    # collar, middle, end chamfer radius

    def sec(z, r):
        a0 = math.asin((CUT - CY) / r)          # below the axis: negative
        return [(r * math.cos(a0 + (math.pi - 2 * a0) * j / N), CY + r * math.sin(a0 + (math.pi - 2 * a0) * j / N), z) for j in range(N + 1)]
    st = [(-1.30, RE, 'c'), (-1.24, RC, 'c'), (-0.70, RC, 'c'), (-0.66, RM, 'b'), (0.66, RM, 'c'), (0.70, RC, 'c'), (1.24, RC, 'c'), (1.30, RE, 'c')]
    loft(m, [sec(z, r) for z, r, _ in st], lambda i, j: 'vce_dt_body' if st[i][2] == 'b' else 'vce_dt_collar', cap0='vce_dt_end', cap1='vce_dt_end')
    box(m, -0.96, 0.96, 0, BASE, -1.40, 1.40, 'vce_dt_foot', c=0.06)
    for sgn in (1, -1):
        # the plate on the end, cut level with the base top
        pts = [(0.66 * math.cos(2 * math.pi * i / N), max(BASE + 0.002, CY + 0.66 * math.sin(2 * math.pi * i / N)), sgn * 1.30) for i in range(N)]
        m.decal(pts, 'vce_dt_plate', (0, 0, sgn))

        def circ(z, r):
            return [(r * math.cos(2 * math.pi * j / 12), CY + r * math.sin(2 * math.pi * j / 12), sgn * z) for j in range(12)]
        # the hub on the end: two steps along the axis
        loft(m, [circ(1.29, 0.34), circ(1.37, 0.34), circ(1.37, 0.25), circ(1.45, 0.25)], lambda i, j: 'vce_dt_hub', cap0='vce_dt_hub', cap1='vce_dt_hub')
    return m


# ---------------- tap and drain (basins)
BASIN_H, BASIN_A = 0.20, 0.46
RX, RN, RS = 0.33, 0.33, -0.25        # the opening: half width, north edge, south edge


def basin_ring(y):
    return [(-BASIN_A, y, -BASIN_A), (BASIN_A, y, -BASIN_A), (BASIN_A, y, BASIN_A), (-BASIN_A, y, BASIN_A)]


def open_ring(y, x=RX, n=RN, s=RS):
    return [(-x, y, s), (x, y, s), (x, y, n), (-x, y, n)]


def tap(p, name):
    m = Model(name)
    FLOOR = 0.12
    rings = [basin_ring(0), basin_ring(BASIN_H), open_ring(BASIN_H), open_ring(FLOOR)]
    loft(m, rings, lambda i, j: (p + 'front', p + 'frame', p + 'wall')[i], cap0=p + 'front', cap1=p + 'floor')
    c = (0.0, FLOOR, 0.04)
    m.disc(c, X, Z, Y, 0.135, p + 'halo', k=16)
    m.disc(c, X, Z, Y, 0.09, p + 'ring', k=16, lift=2 * LIFT)
    m.disc(c, X, Z, Y, 0.07, p + 'dial', k=14, lift=3 * LIFT)
    a = math.radians(68)
    m.rect(c, (math.cos(a), 0, math.sin(a)), (-math.sin(a), 0, math.cos(a)), Y, 0.062, 0.016, p + 'ring', lift=4 * LIFT)
    return m


def drain(p, name):
    m = Model(name)
    RIM, GRATE = 0.175, 0.12
    rings = [basin_ring(0), basin_ring(BASIN_H), open_ring(BASIN_H), open_ring(RIM), open_ring(GRATE, 0.20, 0.07, RS)]

    def fn(i, j):
        if i < 2:
            return (p + 'front', p + 'frame')[i]
        if i == 2:
            return p + 'wall'
        return (p + 'wall', p + 'slopeW', p + 'slopeN', p + 'slopeW')[j]
    loft(m, rings, fn, cap0=p + 'front', cap1=p + 'grate')
    for r_, z in enumerate((0.0, -0.075, -0.15, -0.215)):       # the holes of the grate (paint), rows staggered as VCE's
        for x in ((-0.135, -0.045, 0.045, 0.135) if r_ % 2 == 0 else (-0.09, 0.0, 0.09)):
            m.disc((x, GRATE, z), X, Z, Y, 0.021, p + 'hole', k=6)
    return m


# ---------------- valves
def stub(m, p, turn):
    """One pipe stub lying on the ground from the body to the cell edge; turn: quarter turns from north."""
    def sec(t, r):
        h, tp = (0.165, 0.245) if r > 0.13 else (0.145, 0.22)
        out = []
        for a, b in [(-r, 0.0), (r, 0.0), (r, h), (r * 0.56, tp), (-r * 0.56, tp), (-r, h)]:
            x, z = a, t
            for _ in range(turn):
                x, z = z, -x
            out.append((x, b, z))
        return out
    st = [(0.20, 0.125, 'p'), (0.25, 0.15, 'k'), (0.30, 0.15, 'k'), (0.30, 0.125, 'p'), (0.49, 0.125, 'p')]
    loft(m, [sec(t, r) for t, r, _ in st], lambda i, j: p + ('collar' if st[i][2] == 'k' else 'pipe'), cap0=p + 'pipe', cap1=p + 'pipe')


def valve(p, name, on):
    m = Model(name)
    for t in range(4):
        stub(m, p, t)
    if on:
        lathe(m, 0, 0, [(0.24, 0.0, p + 'body'), (0.24, 0.22, p + 'dome'), (0.21, 0.31, p + 'dome'), (0.12, 0.40, p + 'dome'), (0.0, 0.43, p + 'dome')], n=12)
    else:
        TOP = 0.44
        lathe(m, 0, 0, [(0.24, 0.0, p + 'body'), (0.24, 0.22, p + 'stem'), (0.15, 0.25, p + 'stem'), (0.15, 0.37, p + 'disc'), (0.265, 0.385, p + 'disc'), (0.265, TOP, p + 'disc'),
                        (0.075, TOP, p + 'hub'), (0.07, 0.495, p + 'hub'), (0.0, 0.51, p + 'hub')], n=12)
        # the three cut-outs of the handwheel (paint)
        for deg in (170, 50, -70):
            a0, a1 = math.radians(deg - 30), math.radians(deg + 30)
            pts = [(r * math.cos(a), TOP, r * math.sin(a)) for r, a in ((0.095, a0 + 0.2), (0.225, a0), (0.235, (a0 + a1) / 2), (0.225, a1), (0.095, a1 - 0.2))]
            m.decal(pts, p + 'cut', Y)
    return m


# ---------------- refinery
def refinery():
    m = Model('vce_refinery')
    P = 0.14
    prism(m, rectp(-1.46, 1.46, -1.46, 1.46, 0.14), 0, P, 'vce_rf_plinthF', 'vce_rf_plinth')
    m.rect((0, P, -0.99), X, Z, Y, 0.95, 0.42, 'vce_rf_inset')    # the dark red frame the three units stand in
    # hood across the north, with the block in front of it
    hp = [(-1.42, 0.35), (1.42, 0.35), (1.42, 1.32), (1.30, 1.44), (-1.30, 1.44), (-1.42, 1.32)]
    prism(m, hp, P - 0.01, 0.95, 'vce_rf_hood', 'vce_rf_hood', bevel=0.06)
    box(m, -1.30, 0.60, P - 0.01, 0.70, -0.05, 0.345, 'vce_rf_block', c=0.05)
    # the silo at the north-west: a plain standing cylinder, flat top (user review 1)
    s = 'vce_rf_silo'
    lathe(m, -0.84, 0.72, [(0.52, P - 0.01, s), (0.52, 1.50, s)], n=14)
    # the chimney, top 1.95 (user review 1: over the storey, accepted for now): VCE's fire overlay burns at its mouth
    lathe(m, 0.0, 0.72, [(0.30, 0.90, 'vce_rf_collar'), (0.30, 1.00, 'vce_rf_collar'), (0.27, 1.07, 'vce_rf_chim'), (0.27, 1.86, 'vce_rf_rim'), (0.30, 1.90, 'vce_rf_rim'),
                         (0.30, 1.95, 'vce_rf_rim'), (0.20, 1.95, 'vce_rf_mouth'), (0.20, 1.85, 'vce_rf_mouth'), (0.0, 1.85, 'vce_rf_mouth')], n=10)
    # louvred vent on the hood (paint)
    m.rect((0.66, 0.95, 0.86), X, Z, Y, 0.28, 0.36, 'vce_rf_vent')
    for i in range(5):
        m.rect((0.68, 0.95, 0.60 + i * 0.13), X, Z, Y, 0.22, 0.04, 'vce_rf_slat', lift=2 * LIFT)
    # radiator box beside the manifold, ribs on its top (paint)
    box(m, 0.62, 1.34, P - 0.01, 0.80, -0.05, 0.33, 'vce_rf_block', 'vce_rf_rad', bevel=0.03)
    for i in range(6):
        m.rect((0.76 + i * 0.09, 0.80, 0.14), X, Z, Y, 0.016, 0.13, 'vce_rf_rib')
    # manifold: the long grey bar along x, three tones (top, bevel, front)
    sec = [(-0.07, P - 0.01), (-0.55, P - 0.01), (-0.55, 0.50), (-0.42, 0.60), (-0.27, 0.72), (-0.07, 0.72)]
    mf = {0: 'vce_rf_manF', 1: 'vce_rf_manF', 2: 'vce_rf_manB', 3: 'vce_rf_manB', 4: 'vce_rf_manT', 5: 'vce_rf_manF'}
    loft(m, [[(x, y, z) for z, y in sec] for x in (-0.93, 0.93)], lambda i, j: mf[j], cap0='vce_rf_manF', cap1='vce_rf_manF')
    # three louvred vents on their pads (user review 1): flat octagonal panels with horizontal slats (paint), each with a neck to the manifold
    for cx in (-0.62, 0.0, 0.62):
        box(m, cx - 0.27, cx + 0.27, P - 0.01, 0.19, -1.36, -0.62, 'vce_rf_pad')
        prism(m, rectp(cx - 0.23, cx + 0.23, -1.23, -0.73, 0.08), 0.18, 0.25, 'vce_rf_finD', 'vce_rf_finL')
        for dz in (-0.12, 0.0, 0.12):
            m.rect((cx, 0.25, -0.98 + dz), X, Z, Y, 0.205, 0.038, 'vce_rf_finD')
        box(m, cx - 0.07, cx + 0.07, P - 0.01, 0.27, -0.75, -0.54, 'vce_rf_neck')
    # deepchem in (west, dark), chemfuel out (east, red-brown): two elbows each, down to flanges on the plinth
    for sgn, pipe, fl, xp in ((-1, 'vce_rf_pipeD', 'vce_rf_flangeD', 1.20), (1, 'vce_rf_pipeC', 'vce_rf_flangeC', 1.16)):
        for z, y in ((-0.18, 0.50), (-0.43, 0.34)):
            tube(m, [(sgn * 0.91, y, z), (sgn * xp, y, z), (sgn * xp, P + 0.02, z)], 0.065, pipe)
            lathe(m, sgn * xp, z, [(0.115, P - 0.01, fl), (0.115, 0.20, fl)], n=8)
    return m


# ---------------- pumpjack
PJ_SLAB = 0.10
PJ_TOP = 0.62      # both blocks' top
PJ_PIT = 0.46      # the well between the two plates reaches z +-0.46


def pumpjack_base():
    m = Model('vce_pumpjack_base')
    box(m, -1.36, 1.36, 0, PJ_SLAB, -1.20, 1.20, 'vce_pj_slab')
    m.rect((0, PJ_SLAB, 0), X, Z, Y, 0.95, PJ_PIT + 0.01, 'vce_pj_pit')
    T = 0.30
    n = [(-1.46, 0.68), (-1.0, PJ_PIT), (1.0, PJ_PIT), (1.46, 0.68), (1.46, 1.34), (1.34, 1.46), (-1.34, 1.46), (-1.46, 1.34)]
    prism(m, n, 0, T, 'vce_pj_plateF', 'vce_pj_plate')
    prism(m, [(x, -z) for x, z in n], 0, T, 'vce_pj_plateF', 'vce_pj_plate')
    # the two blocks either side of the well: one matching pair, the same hipped shape mirrored, top PJ_TOP (user review of the
    # in-game sheet). The camera looks over the south block: with its top at 0.62 the sight line meets the arm's axis at about
    # 0.30, so the collar (0.58) and the whole head stay in view at rest.
    F = PJ_PIT - 0.008
    low = [(-0.98, F), (0.98, F), (0.98, 0.82), (0.32, 1.26), (-0.32, 1.26), (-0.98, 0.82)]
    high = [(-0.84, F), (0.84, F), (0.84, 0.76), (0.27, 1.10), (-0.27, 1.10), (-0.84, 0.76)]
    for sgn in (1, -1):
        lo_ = [(x, sgn * z) for x, z in low]
        hi_ = [(x, sgn * z) for x, z in high]
        rings = [plan(lo_, PJ_SLAB - 0.01), plan(lo_, 0.36), plan(hi_, PJ_TOP)]
        loft(m, rings, lambda i, j: 'vce_pj_face' if j == 0 else ('vce_pj_hoodA' if i == 0 else 'vce_pj_hoodB'), cap0='vce_pj_face', cap1='vce_pj_hoodT')
    # arch and the two guide bars on the north block's front (paint)
    k = 12
    pts = [(0.43 * math.cos(math.pi * i / k), 0.28 + 0.24 * math.sin(math.pi * i / k), F) for i in range(k + 1)] + [(-0.43, PJ_SLAB, F), (0.43, PJ_SLAB, F)]
    m.decal(pts, 'vce_pj_arch', NZ)
    for x in (-0.63, 0.63):
        m.rect((x, 0.37, F), X, Y, NZ, 0.085, 0.17, 'vce_pj_guide')
    # the lighter strip on the south block's top (paint)
    m.decal([(-0.30, PJ_TOP, -1.00), (0.30, PJ_TOP, -1.00), (0.07, PJ_TOP, -0.54), (-0.07, PJ_TOP, -0.54)], 'vce_pj_rampC', Y)
    # the two pipes round the machine
    PIPE, lo, hi = 0.07, 0.46, 0.72    # the south pipe crosses over the block
    tube(m, [(-1.16, 0.12, 0.14), (-1.16, lo, 0.14), (-1.16, lo, 1.33), (1.24, lo, 1.33), (1.24, lo, 0.88), (1.24, T + 0.02, 0.88)], PIPE, 'vce_pj_pipe')
    tube(m, [(-1.24, T + 0.02, -0.62), (-1.24, hi, -0.62), (-1.24, hi, -0.86), (1.24, hi, -0.86), (1.24, hi, -1.14), (1.24, T + 0.02, -1.14)], PIPE, 'vce_pj_pipe')
    f = 'vce_pj_flange'
    for x, z, y in ((-1.16, 0.14, PJ_SLAB), (1.24, 0.88, T), (-1.24, -0.62, T), (1.24, -1.14, T)):
        lathe(m, x, z, [(0.125, y - 0.01, f), (0.125, y + 0.07, f)], n=8)
    return m


def pumpjack_arm():
    """The moving part, origin at its lowest point on the axis."""
    m = Model('vce_pumpjack_arm')
    N = 12
    g, h, c = 'vce_pj_grey', 'vce_pj_head', 'vce_pj_collar'
    prof = [(0.29, 0.0, g), (0.29, 0.08, 'vce_pj_ring'), (0.30, 0.12, g), (0.29, 0.16, g), (0.29, 0.22, 'rib'), (0.36, 0.24, 'rib'), (0.36, 0.50, c), (0.42, 0.52, c), (0.42, 0.60, c),
            (0.33, 0.62, h), (0.33, 0.92, h), (0.285, 1.06, h), (0.16, 1.15, h), (0.0, 1.18, h)]
    ph = -math.pi / 2 + math.pi / N    # a facet straight at the south

    def fn(i, j):
        t = prof[i][2]
        return ('vce_pj_ribL' if j % 2 else 'vce_pj_ribD') if t == 'rib' else t
    lathe(m, 0, 0, prof, n=N, phase=ph, matfn=fn)
    # three window slots on the south of the head (paint on the facets)
    r = 0.33
    for k in (-1, 0, 1):
        a0 = -math.pi / 2 + k * 2 * math.pi / N - math.pi / N
        a1 = a0 + 2 * math.pi / N
        p0, p1 = (r * math.cos(a0), 0, r * math.sin(a0)), (r * math.cos(a1), 0, r * math.sin(a1))
        mid = mul(add(p0, p1), 0.5)
        m.rect((mid[0], 0.76, mid[2]), norm(sub(p1, p0)), Y, norm(mid), math.dist(p0, p1) / 2 * 0.72, 0.10, 'vce_pj_slot')
    return m


def pumpjack_rod():
    """A plain rod one cell tall: stretched from the ground to the arm's lowest point."""
    m = Model('vce_pumpjack_rod')
    lathe(m, 0, 0, [(0.21, 0.0, 'vce_pj_rod'), (0.21, 1.0, 'vce_pj_rod')], n=10)
    return m


# ---------------- item
def deepchem():
    m = Model('vce_deepchem')
    N, R, b, h, l = 12, 0.27, 'vce_it_body', 'vce_it_hoop', 'vce_it_lid'
    lathe(m, 0, 0, [(R, 0.0, b), (R, 0.10, h), (R, 0.14, b), (R, 0.36, h), (R, 0.40, b), (R, 0.50, l)], n=N)
    lathe(m, -0.11, 0.10, [(0.07, 0.48, 'vce_it_cap'), (0.07, 0.54, 'vce_it_cap')], n=8)
    m.disc((0, 0.50, 0), X, Z, Y, 0.235, 'vce_it_hoop', k=12)
    m.disc((0, 0.50, 0), X, Z, Y, 0.215, 'vce_it_lid', k=12, lift=2 * LIFT)
    # the diamond mark, folded over the facet edge at the south-east (lathe vertices every 30 degrees)
    a = math.radians(-60)
    e = (R * math.cos(a), 0, R * math.sin(a))
    top, bot = add(e, (0, 0.355, 0)), add(e, (0, 0.145, 0))
    for deg in (-90, -30):
        q = math.radians(deg)
        p = (R * math.cos(q), 0, R * math.sin(q))
        tip = add(add(e, mul(norm(sub(p, e)), 0.105)), (0, 0.25, 0))
        m.decal([top, bot, tip], 'vce_it_mark', norm(add(e, p)))
    return m


# ---------------- writing and checks
def obj_of(p):
    return (p[0], p[1], -p[2])


def check_and_orient(m):
    """Turns each shell outward (in OBJ space), checks it is closed and consistently wound."""
    warn = []
    for si, s in enumerate(m.shells):
        vol = 0.0
        for idx, _ in s.faces:
            a = obj_of(m.v[idx[0]])
            for k in range(1, len(idx) - 1):
                vol += dot(a, cross(obj_of(m.v[idx[k]]), obj_of(m.v[idx[k + 1]])))
        if vol < 0:
            s.faces = [(tuple(reversed(i)), t) for i, t in s.faces]
        edges = {}
        for idx, _ in s.faces:
            for k in range(len(idx)):
                e = (idx[k], idx[(k + 1) % len(idx)])
                edges[e] = edges.get(e, 0) + 1
        bad = [e for e, c in edges.items() if c != 1 or edges.get((e[1], e[0]), 0) != 1]
        if bad:
            warn.append('shell %d not closed: %d edges' % (si, len(bad)))
    return warn


def write(m):
    warn = check_and_orient(m)
    lines = ['# %s: IsoRim Waylith - Vanilla Chemfuel Expanded Pack, batch B1 (tools/make_vce_b1.py)' % m.name, 'mtllib ' + LIB]
    verts = list(m.v)
    faces = [f for s in m.shells for f in s.faces]
    for pts, t, n in m.sheets:
        base = len(verts)
        verts += [tuple(p) for p in pts]
        idx = list(range(base, base + len(pts)))
        a, b, c = obj_of(verts[idx[0]]), obj_of(verts[idx[1]]), obj_of(verts[idx[2]])
        if dot(cross(sub(b, a), sub(c, a)), obj_of(n)) < 0:
            idx.reverse()
        faces.append((tuple(idx), t))
    for v in verts:
        p = obj_of(v)
        lines.append('v %.5f %.5f %.5f' % (p[0] + 0.0, p[1] + 0.0, p[2] + 0.0))
    vts, vtl, body, cur, tris = {}, [], [], None, 0
    for idx, t in sorted(faces, key=lambda f: f[1]):
        if t != cur:
            body.append('usemtl ' + t); cur = t
        a, b, c = verts[idx[0]], verts[idx[1]], verts[idx[-1]]
        n = cross(sub(b, a), sub(c, a))
        ax = max(range(3), key=lambda i: abs(n[i]))
        u_i, v_i = {0: (2, 1), 1: (0, 2), 2: (0, 1)}[ax]
        part = []
        for i in idx:
            key = (round(verts[i][u_i], 4), round(verts[i][v_i], 4))
            if key not in vts:
                vts[key] = len(vtl) + 1
                vtl.append('vt %.4f %.4f' % key)
            part.append('%d/%d' % (i + 1, vts[key]))
        for k in range(1, len(part) - 1):
            body.append('f %s %s %s' % (part[0], part[k], part[k + 1]))
            tris += 1
    lines += vtl + body
    open(os.path.join(OUT, m.name + '.obj'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    xs = [v[0] for v in verts]; ys = [v[1] for v in verts]; zs = [v[2] for v in verts]
    print('%-22s tris %4d  x %.3f..%.3f  y %.3f..%.3f  z %.3f..%.3f %s' % (m.name, tris, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), '; '.join(warn)))
    if min(ys) < -1e-6:
        print('  !! below the ground')
    return max(ys)


def main():
    models = [tank_chem(), tank_deep(),
              tap('vce_hc_', 'vce_tap_chem'), tap('vce_hd_', 'vce_tap_deep'),
              drain('vce_hc_', 'vce_drain_chem'), drain('vce_hd_', 'vce_drain_deep'),
              valve('vce_vc_', 'vce_valve_chem_on', True), valve('vce_vc_', 'vce_valve_chem_off', False),
              valve('vce_vd_', 'vce_valve_deep_on', True), valve('vce_vd_', 'vce_valve_deep_off', False),
              refinery(), pumpjack_base(), pumpjack_arm(), pumpjack_rod(), deepchem()]
    used = set()
    for m in models:
        top = write(m)
        if top > STOREY and m.name != 'vce_refinery':      # the refinery's chimney: accepted, user review 1
            print('  !! over the storey:', m.name, top)
        used |= {t for s in m.shells for _, t in s.faces} | {t for _, t, _ in m.sheets}
    out = ["# IsoRim Waylith - Vanilla Chemfuel Expanded Pack, batch B1: fixed colours sampled from VCE's textures."]
    for k in sorted(used):
        kd, metal = MATS[k]
        out.append('newmtl %s\nKd %.2f %.2f %.2f' % (k, *kd))
        if metal:
            out.append('map_Kd ' + METAL)
    open(os.path.join(OUT, LIB), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')


main()
