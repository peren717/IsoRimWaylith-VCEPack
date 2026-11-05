# Blender (5.x, headless) review renders for make_vce_b1.py. Game look as tools\stylefurn_review.py: Kd as sRGB, 3-band stepped sun,
# the game's inverted hull (0.03, vertices at y = 0 stay on the ground), glow unlit. Camera from the south, pitch 38, orthographic.
# usage: blender --background --factory-startup --python vce_b1_review.py -- <Models dir> <IsoRim Models dir> <abs out dir> [job ...]
# writes <job>_{game,g45,back,front,side,top,play}.png; job parts carry dy (lift) and ys (height scale): the pumpjack's arm and rod.
import bpy, math, os, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:]
MODELS, ISO, OUT = argv[0], argv[1], argv[2]
os.makedirs(OUT, exist_ok=True)
OUTLINE = 0.03
AMB, SUN = 0.50, 0.62
PX = 460

REST, RISE = 0.36, 0.75     # pumpjack: arm's lowest point at rest, 3D rise at VCHE's top of stroke
def pump(rise):
    y = REST + rise
    return [dict(obj='vce_pumpjack_base'), dict(obj='vce_pumpjack_rod', ys=y), dict(obj='vce_pumpjack_arm', dy=y)]

J = []
def job(name, parts, tz, sz, rot=0):
    J.append(dict(name=name, parts=parts if isinstance(parts, list) else [dict(obj=parts)], tz=tz, sz=sz, rot=rot))
for s in ('chem', 'deep'):
    for tag, r in (('N', 0), ('E', 1), ('S', 2), ('W', 3)):
        job('tank_%s_%s' % (s, tag), 'vce_tank_' + s, 0.35, 3.9, r)
    job('tap_' + s, 'vce_tap_' + s, 0.10, 1.5)
    job('drain_' + s, 'vce_drain_' + s, 0.10, 1.5)
    job('valve_%s_on' % s, 'vce_valve_%s_on' % s, 0.15, 1.5)
    job('valve_%s_off' % s, 'vce_valve_%s_off' % s, 0.15, 1.5)
job('refinery', 'vce_refinery', 0.45, 3.9)
job('pumpjack_rest', pump(0.0), 0.65, 3.9)
job('pumpjack_top', pump(RISE), 0.65, 3.9)
job('item', 'vce_deepchem', 0.22, 1.0)


def lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def read_mtl(path, mats):
    cur = None
    for line in open(path, encoding='utf-8', errors='replace'):
        q = line.split()
        if not q:
            continue
        if q[0] == 'newmtl':
            cur = q[1]; mats[cur] = (0.8, 0.8, 0.8)
        elif q[0] == 'Kd' and cur:
            mats[cur] = tuple(float(x) for x in q[1:4])


def read_obj(path, rot, dy, ys):
    mats, vs, fs, cur = {}, [], [], 'default'
    for line in open(path, encoding='utf-8', errors='replace'):
        q = line.split()
        if not q:
            continue
        if q[0] == 'v':
            x, y, z = map(float, q[1:4])
            gx, gz = x, -z
            for _ in range(rot):
                gx, gz = gz, -gx
            vs.append((gx, y * ys + dy, -gz))
        elif q[0] == 'f':
            idx = [int(t.split('/')[0]) for t in q[1:]]
            idx = [i - 1 if i > 0 else len(vs) + i for i in idx]
            for k in range(1, len(idx) - 1):
                fs.append(((idx[0], idx[k], idx[k + 1]), cur))
        elif q[0] == 'usemtl':
            cur = q[1]
        elif q[0] == 'mtllib':
            for d in (os.path.dirname(path), ISO):
                f = os.path.join(d, q[1])
                if os.path.exists(f):
                    read_mtl(f, mats); break
    return vs, fs, mats


_mat = {}
def material(rgb, emit=False):
    key = (tuple(round(c, 4) for c in rgb), emit)
    if key in _mat:
        return _mat[key]
    m = bpy.data.materials.new('m%d' % len(_mat))
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    if emit:
        em.inputs['Color'].default_value = (*lin(rgb), 1)
        m.use_backface_culling = True
    else:
        dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (1, 1, 1, 1)
        s2r = nt.nodes.new('ShaderNodeShaderToRGB')
        bw = nt.nodes.new('ShaderNodeRGBToBW')
        nt.links.new(dif.outputs[0], s2r.inputs[0]); nt.links.new(s2r.outputs['Color'], bw.inputs[0])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
        e = ramp.color_ramp.elements
        e[0].position = 0.0; e[0].color = (0, 0, 0, 1)
        e[1].position = 0.25; e[1].color = (0.5, 0.5, 0.5, 1)
        e3 = e.new(0.75); e3.color = (1, 1, 1, 1)
        nt.links.new(bw.outputs[0], ramp.inputs[0])
        mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'MULTIPLY_ADD'
        mr.inputs[1].default_value = SUN; mr.inputs[2].default_value = AMB
        nt.links.new(ramp.outputs['Color'], mr.inputs[0])
        mul = nt.nodes.new('ShaderNodeMixRGB'); mul.blend_type = 'MULTIPLY'; mul.inputs['Fac'].default_value = 1.0
        mul.inputs['Color1'].default_value = (*lin(rgb), 1)
        nt.links.new(mr.outputs[0], mul.inputs['Color2'])
        nt.links.new(mul.outputs[0], em.inputs['Color'])
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    _mat[key] = m
    return m


def game_hull(vs, fs, width):
    key = lambda v: (round(v[0] * 1e4), round(v[1] * 1e4), round(v[2] * 1e4))
    fn, vol = [], 0.0
    for (a, b, c), _ in fs:
        A, B, C = Vector(vs[a]), Vector(vs[b]), Vector(vs[c])
        n = (B - A).cross(C - A); vol += A.dot(B.cross(C))
        fn.append(n.normalized() if n.length > 1e-12 else Vector())
    if vol < 0:
        fn = [-n for n in fn]
    at = {}
    for ((a, b, c), _), n in zip(fs, fn):
        for i in (a, b, c):
            l = at.setdefault(key(vs[i]), [])
            if all(n.dot(q) <= 0.999 for q in l):
                l.append(Vector(n))
    off = {}
    for k, l in at.items():
        d = sum(l, Vector())
        off[k] = d.normalized() * width if d.length > 1e-6 else Vector()
    hv = []
    for v in vs:
        p = Vector(v) + off.get(key(v), Vector())
        if v[1] == 0:       # vertices on the ground only move sideways (keeps the outline on the ground)
            p.y = 0
        hv.append(tuple(p))
    return hv, vol < 0


ROOT = []
HULL = None
def make(path, rot=0, dy=0.0, ys=1.0):
    vs, fs, mats = read_obj(path, rot, dy, ys)
    hv, flip = game_hull(vs, fs, OUTLINE)
    tb = lambda v: (v[0], -v[2], v[1])
    me = bpy.data.meshes.new(os.path.basename(path))
    me.from_pydata([tb(v) for v in vs], [], [f for f, _ in fs])
    names = sorted(set(n for _, n in fs))
    for n in names:
        me.materials.append(material(tuple(min(1.0, c) for c in mats.get(n, (0.8, 0.8, 0.8)))))
    for p, (_, n) in zip(me.polygons, fs):
        p.material_index = names.index(n)
    o = bpy.data.objects.new(me.name, me); bpy.context.scene.collection.objects.link(o); ROOT.append(o)
    hm = bpy.data.meshes.new(me.name + '_hull')
    faces = [(c, b, a_) for (a_, b, c), _ in fs] if not flip else [f for f, _ in fs]
    hm.from_pydata([tb(v) for v in hv], [], faces)
    hm.materials.append(HULL)
    ho = bpy.data.objects.new(hm.name, hm); bpy.context.scene.collection.objects.link(ho); ROOT.append(ho)


def clear():
    for o in list(ROOT):
        me = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(me)
    ROOT.clear()


def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    sc.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new('W'); w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (*lin((0.42, 0.50, 0.38)), 1)
    sc.world = w
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.14159; sun.use_shadow = False
    so = bpy.data.objects.new('sun', sun); so.rotation_euler = (math.radians(45), 0, math.radians(-35))
    sc.collection.objects.link(so)
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    global HULL
    HULL = material((0.02, 0.02, 0.02), emit=True)
    return sc, co


def look(co, tgt, yaw, pitch, scale):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = 10
    co.location = Vector(tgt) + Vector((-math.sin(yr) * math.cos(pr) * d, -math.cos(yr) * math.cos(pr) * d, math.sin(pr) * d))
    co.rotation_euler = (math.radians(90 - pitch), 0, -yr)
    co.data.ortho_scale = scale


def shot(sc, path, w, h):
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


sc, co = setup()
ONLY = argv[3:]
for j in J:
    if ONLY and j['name'] not in ONLY:
        continue
    clear()
    for p in j['parts']:
        make(os.path.join(MODELS, p['obj'] + '.obj'), j['rot'], p.get('dy', 0.0), p.get('ys', 1.0))
    tz, sz = j['tz'], j['sz']
    for name, yaw, pitch in (('game', 0, 38), ('g45', 45, 38), ('back', 180, 38), ('front', 0, 0), ('side', -90, 0), ('top', 0, 90)):
        look(co, (0, 0, tz if pitch else sz / 2 - 0.2), yaw, pitch, sz)
        shot(sc, os.path.join(OUT, '%s_%s.png' % (j['name'], name)), PX, PX)
    look(co, (0, 0, tz), 0, 38, sz)
    shot(sc, os.path.join(OUT, '%s_play.png' % j['name']), int(sz * 50), int(sz * 50))
print('done')
