"""Build the TraceShell Geometry Nodes graph. Run inside Blender."""
from __future__ import annotations

import math
import os

import bpy
import bmesh
from mathutils import Vector

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "TraceShellGN"
OBJ_NAME = "TraceShell"


class GN:
    def __init__(self, ng):
        self.ng = ng
        self.links = ng.links
        self.n = 0

    def node(self, idname, loc, **kw):
        node = self.ng.nodes.new(idname)
        node.location = loc
        node.width = min(180, getattr(node, "width", 140))
        for k, v in kw.items():
            if hasattr(node, k):
                setattr(node, k, v)
        self.n += 1
        return node

    def math(self, op, a, b=None, loc=(0, 0), c=None):
        node = self.node("ShaderNodeMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        if c is not None:
            self._in(node, 2, c)
        return node.outputs[0]

    def imath(self, op, a, b=None, loc=(0, 0)):
        node = self.node("FunctionNodeIntegerMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        return node.outputs[0]

    def vmath(self, op, a, b=None, loc=(0, 0), scale=None):
        node = self.node("ShaderNodeVectorMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        if scale is not None:
            self._in(node, "Scale", scale)
        return node.outputs[0] if op not in {"DOT_PRODUCT", "LENGTH", "DISTANCE"} else node.outputs["Value"]

    def cmp(self, op, a, b, loc=(0, 0), dtype="FLOAT"):
        node = self.node("FunctionNodeCompare", loc, data_type=dtype, operation=op)
        self._in(node, 0, a)
        self._in(node, 1, b)
        return node.outputs[0]

    def switch(self, dtype, cond, false, true, loc=(0, 0)):
        node = self.node("GeometryNodeSwitch", loc, input_type=dtype)
        self._in(node, "Switch", cond)
        self._in(node, "False", false)
        self._in(node, "True", true)
        return node.outputs[0]

    def rand(self, seed, idx, loc, vmin=0.0, vmax=1.0):
        node = self.node("FunctionNodeRandomValue", loc, data_type="FLOAT")
        node.inputs["Min"].default_value = vmin
        node.inputs["Max"].default_value = vmax
        self._in(node, "ID", idx)
        self._in(node, "Seed", seed)
        return node.outputs["Value"]

    def bool(self, op, a, b=None, loc=(0, 0)):
        node = self.node("FunctionNodeBooleanMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        return node.outputs[0]

    def combine(self, x, y, z, loc=(0, 0)):
        node = self.node("ShaderNodeCombineXYZ", loc)
        self._in(node, 0, x)
        self._in(node, 1, y)
        self._in(node, 2, z)
        return node.outputs[0]

    def value(self, v, loc):
        node = self.node("ShaderNodeValue", loc)
        node.outputs[0].default_value = float(v)
        return node.outputs[0]

    def vec(self, xyz, loc):
        node = self.node("FunctionNodeInputVector", loc)
        node.vector = Vector(xyz)
        return node.outputs[0]

    def _in(self, node, key, sock):
        if sock is None:
            return
        target = node.inputs[key]
        if hasattr(sock, "rna_type"):
            self.links.new(sock, target)
        else:
            target.default_value = sock


def _clear_test_groups():
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith("_"):
            bpy.data.node_groups.remove(ng)


def _iface(ng, name, in_out, stype, default=None, vmin=None, vmax=None, desc=""):
    item = ng.interface.new_socket(name=name, in_out=in_out, socket_type=stype)
    if desc:
        item.description = desc
    if default is not None:
        try:
            item.default_value = default
        except Exception:
            pass
    if vmin is not None:
        try:
            item.min_value = vmin
        except Exception:
            pass
    if vmax is not None:
        try:
            item.max_value = vmax
        except Exception:
            pass
    return item


def _node_override(obj, ng):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != "NODE_EDITOR":
                continue
            space = area.spaces.active
            space.tree_type = "GeometryNodeTree"
            space.node_tree = ng
            for region in area.regions:
                if region.type == "WINDOW":
                    return {
                        "window": window,
                        "area": area,
                        "region": region,
                        "space_data": space,
                        "screen": window.screen,
                        "object": obj,
                        "active_object": obj,
                        "scene": bpy.context.scene,
                    }
    raise RuntimeError("No NODE_EDITOR area. Keep Blender on a node editor screen.")


def add_repeat_zone_pair(obj, ng):
    ov = _node_override(obj, ng)
    before = set(ng.nodes.keys())
    with bpy.context.temp_override(**ov):
        result = bpy.ops.node.add_repeat_zone(use_transform=False)
        if result != {"FINISHED"}:
            raise RuntimeError("add_repeat_zone failed: %s" % result)
    new = [n for n in ng.nodes if n.name not in before]
    ri = next(n for n in new if n.bl_idname == "GeometryNodeRepeatInput")
    ro = next(n for n in new if n.bl_idname == "GeometryNodeRepeatOutput")
    return ri, ro


def create_group():
    if GROUP_NAME in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[GROUP_NAME])
    ng = bpy.data.node_groups.new(GROUP_NAME, "GeometryNodeTree")
    try:
        ng.is_modifier = True
    except Exception:
        pass
    _iface(ng, "Geometry", "OUTPUT", "NodeSocketGeometry")
    _iface(ng, "Count", "INPUT", "NodeSocketInt", 8, 3, 40, "Samples along the helix")
    _iface(ng, "Overlap", "INPUT", "NodeSocketFloat", 0.70, 0.20, 0.92, "Higher = tighter coil")
    _iface(ng, "Size Min", "INPUT", "NodeSocketFloat", 6.0, 4.0, 40.0, "mm; B raised")
    _iface(ng, "Size Max", "INPUT", "NodeSocketFloat", 12.0, 4.0, 40.0)
    _iface(ng, "Prism Thickness", "INPUT", "NodeSocketFloat", 2.5, 1.5, 20.0)
    _iface(ng, "Wall Thickness", "INPUT", "NodeSocketFloat", 2.5, 1.2, 20.0, "mm min triangle altitude")
    _iface(ng, "Correlation", "INPUT", "NodeSocketFloat", 0.35, 0.0, 1.0)
    _iface(ng, "Max Turn Deg", "INPUT", "NodeSocketFloat", 35.0, 0.0, 90.0)
    _iface(ng, "Reverse", "INPUT", "NodeSocketBool", True)
    _iface(ng, "Beat N", "INPUT", "NodeSocketInt", 4, 0, 20, "0 = off")
    _iface(ng, "Beat Scale", "INPUT", "NodeSocketFloat", 1.45, 1.2, 2.0)
    _iface(ng, "Seed", "INPUT", "NodeSocketInt", 1, 0, 99999)
    _iface(ng, "Fade Affects Size", "INPUT", "NodeSocketBool", False)
    _iface(ng, "Helix Turns", "INPUT", "NodeSocketFloat", 1.0, 0.25, 6.0, "pitch must exceed 2× triangle; 1.0 is clearance not taste")
    _iface(ng, "Helix Radius", "INPUT", "NodeSocketFloat", 16.0, 6.0, 32.0)
    _iface(ng, "Torque Deg", "INPUT", "NodeSocketFloat", 240.0, 0.0, 720.0, "triangle twist along helix")
    ng.nodes.new("NodeGroupInput")
    ng.nodes.new("NodeGroupOutput")
    return ng


def fill_helix(ng):
    """Triangle cross-section swept along a torsion helix. No Repeat Zone."""
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-900, 0)
    go.location = (2800, 0)

    # --- helix (the connecting trace) ---
    extra_torque = g.math("ADD", 0.6, gi.outputs["Overlap"], loc=(-500, 420))
    rotations = gi.outputs["Helix Turns"]
    height = g.value(28.0, (-500, 220))
    res_mul = g.imath("MULTIPLY", gi.outputs["Count"], 16, loc=(-500, 140))
    res = g.imath("MAXIMUM", res_mul, 64, loc=(-280, 140))
    spiral = g.node("GeometryNodeCurveSpiral", (-80, 280))
    g.links.new(res, spiral.inputs["Resolution"])
    g.links.new(rotations, spiral.inputs["Rotations"])
    g.links.new(gi.outputs["Helix Radius"], spiral.inputs["Start Radius"])
    g.links.new(gi.outputs["Helix Radius"], spiral.inputs["End Radius"])
    g.links.new(height, spiral.inputs["Height"])

    # sit in the 80x80x40 box; z high enough that a Size Max bead stays above the bed
    place = g.node("GeometryNodeTransform", (140, 280))
    g.links.new(spiral.outputs["Curve"], place.inputs["Geometry"])
    g.links.new(g.vec((40.0, 40.0, 8.0), (140, 80)), place.inputs["Translation"])

    resample = g.node("GeometryNodeResampleCurve", (360, 280), mode="COUNT")
    g.links.new(place.outputs["Geometry"], resample.inputs["Curve"])
    g.links.new(res, resample.inputs["Count"])

    # --- torque + reverse at halfway by count/factor ---
    fac = g.node("GeometryNodeSplineParameter", (360, 520))
    # one random ID per Count-sample, not per resampled point (that jitter folded the tube)
    seg = g.node("FunctionNodeFloatToInt", (560, 700))
    g.links.new(g.math("MULTIPLY", fac.outputs["Factor"], gi.outputs["Count"], loc=(360, 700)), seg.inputs[0])
    past_amt = g.math("DIVIDE", g.math("SUBTRACT", fac.outputs["Factor"], 0.42, loc=(560, 620)), 0.16, loc=(760, 620))
    past_clamped = g.math("MINIMUM", 1.0, g.math("MAXIMUM", 0.0, past_amt, loc=(960, 640)), loc=(1160, 640))
    # 1 → -1 across the midpoint if Reverse is on
    smooth_sign = g.math("SUBTRACT", 1.0, g.math("MULTIPLY", past_clamped, 2.0, loc=(1360, 620)), loc=(1560, 620))
    sign = g.switch("FLOAT", gi.outputs["Reverse"], 1.0, smooth_sign, loc=(1760, 600))
    torque_rad = g.math("MULTIPLY", g.math("MULTIPLY", gi.outputs["Torque Deg"], extra_torque, loc=(360, 460)), math.pi / 180.0, loc=(560, 460))
    base_tilt = g.math("MULTIPLY", g.math("MULTIPLY", torque_rad, fac.outputs["Factor"], loc=(760, 460)), sign, loc=(960, 460))
    u = g.rand(gi.outputs["Seed"], seg.outputs[0], (560, 360))
    noise = g.math(
        "MULTIPLY",
        g.math("MULTIPLY", g.math("SUBTRACT", u, 0.5, loc=(760, 360)), 2.0, loc=(960, 360)),
        g.math("MULTIPLY", gi.outputs["Max Turn Deg"], math.pi / 180.0, loc=(760, 280)),
        loc=(1160, 340),
    )
    tilt = g.math("ADD", base_tilt, g.math("MULTIPLY", noise, g.math("SUBTRACT", 1.0, g.math("MULTIPLY", gi.outputs["Correlation"], 0.65, loc=(960, 240)), loc=(1160, 240)), loc=(1360, 280)), loc=(1560, 400))
    set_tilt = g.node("GeometryNodeSetCurveTilt", (560, 280))
    g.links.new(resample.outputs["Curve"], set_tilt.inputs["Curve"])
    g.links.new(tilt, set_tilt.inputs["Tilt"])

    # --- radius: size min–max, beat, optional fade ---
    u2 = g.rand(g.imath("ADD", gi.outputs["Seed"], 11, loc=(560, -40)), seg.outputs[0], (760, -40))
    size_ind = g.math("MULTIPLY_ADD", g.math("SUBTRACT", gi.outputs["Size Max"], gi.outputs["Size Min"], loc=(960, 40)), u2, loc=(1160, 40), c=gi.outputs["Size Min"])
    size = g.math("ADD", g.math("MULTIPLY", gi.outputs["Correlation"], gi.outputs["Size Min"], loc=(1160, -40)), g.math("MULTIPLY", g.math("SUBTRACT", 1.0, gi.outputs["Correlation"], loc=(960, -80)), size_ind, loc=(1160, -100)), loc=(1360, -20))
    beat0 = g.cmp("EQUAL", gi.outputs["Beat N"], 0, loc=(960, -200), dtype="INT")
    beat_safe = g.switch("INT", beat0, gi.outputs["Beat N"], 1, loc=(1160, -200))
    mod = g.imath("FLOORED_MODULO", seg.outputs[0], beat_safe, loc=(1360, -200))
    is_beat = g.bool("AND", g.bool("NOT", beat0, loc=(1360, -280)), g.cmp("EQUAL", mod, 0, loc=(1560, -200), dtype="INT"), loc=(1760, -220))
    size_b = g.switch("FLOAT", is_beat, size, g.math("MULTIPLY", size, gi.outputs["Beat Scale"], loc=(1760, -100)), loc=(1960, -80))
    fade_t = fac.outputs["Factor"]
    fade_mul = g.math("SUBTRACT", 1.0, g.math("MULTIPLY", fade_t, 0.35, loc=(1760, -300)), loc=(1960, -300))
    size_f = g.math("MAXIMUM", gi.outputs["Size Min"], g.math("MULTIPLY", size_b, fade_mul, loc=(2160, -200)), loc=(2360, -160))
    draw = g.switch("FLOAT", gi.outputs["Fade Affects Size"], size_b, size_f, loc=(2160, -40))
    # Curve radius is a multiplier on the profile; profile is built in mm so radius ~ 1
    rad = g.math("DIVIDE", draw, gi.outputs["Size Min"], loc=(2360, 40))
    set_rad = g.node("GeometryNodeSetCurveRadius", (780, 200))
    g.links.new(set_tilt.outputs["Curve"], set_rad.inputs["Curve"])
    g.links.new(rad, set_rad.inputs["Radius"])

    # --- free-three-point triangle profile (not a circle) ---
    base = g.math("MAXIMUM", gi.outputs["Size Min"], g.math("MULTIPLY", gi.outputs["Wall Thickness"], 2.2, loc=(-200, -420)), loc=(0, -420))
    ht = g.math("MAXIMUM", g.math("MULTIPLY", gi.outputs["Wall Thickness"], 1.3, loc=(-200, -500)), g.math("MULTIPLY", gi.outputs["Size Min"], 0.85, loc=(0, -500)), loc=(200, -460))
    half = g.math("MULTIPLY", base, 0.5, loc=(200, -360))
    shift = g.math("MULTIPLY", base, 0.18, loc=(200, -540))
    pts = g.node("GeometryNodePoints", (420, -440))
    pts.inputs["Count"].default_value = 3
    pidx = g.node("GeometryNodeInputIndex", (420, -560))
    sw = g.node("GeometryNodeIndexSwitch", (640, -440), data_type="VECTOR")
    while len(sw.index_switch_items) < 3:
        sw.index_switch_items.new()
    p0 = g.combine(g.math("SUBTRACT", 0.0, half, loc=(420, -640)), 0.0, 0.0, loc=(640, -640))
    p1 = g.combine(half, 0.0, 0.0, loc=(640, -720))
    p2 = g.combine(shift, ht, 0.0, loc=(640, -800))
    g.links.new(pidx.outputs["Index"], sw.inputs["Index"])
    g.links.new(p0, sw.inputs[1])
    g.links.new(p1, sw.inputs[2])
    g.links.new(p2, sw.inputs[3])
    g.links.new(sw.outputs[0], pts.inputs["Position"])
    to_curve = g.node("GeometryNodePointsToCurves", (860, -440))
    g.links.new(pts.outputs["Points"], to_curve.inputs["Points"])
    poly = g.node("GeometryNodeCurveSplineType", (970, -440))
    poly.spline_type = "POLY"
    g.links.new(to_curve.outputs["Curves"], poly.inputs["Curve"])
    cyclic = g.node("GeometryNodeSetSplineCyclic", (1080, -440))
    g.links.new(poly.outputs["Curve"], cyclic.inputs["Curve"])
    cyclic.inputs["Cyclic"].default_value = True

    c2m = g.node("GeometryNodeCurveToMesh", (1100, 180))
    g.links.new(set_rad.outputs["Curve"], c2m.inputs["Curve"])
    g.links.new(cyclic.outputs["Curve"], c2m.inputs["Profile Curve"])
    c2m.inputs["Fill Caps"].default_value = True
    c2m.inputs["Scale"].default_value = 1.0

    merge = g.node("GeometryNodeMergeByDistance", (1400, 180))
    merge.inputs["Distance"].default_value = 0.25
    g.links.new(c2m.outputs["Mesh"], merge.inputs["Geometry"])
    g.links.new(merge.outputs["Geometry"], go.inputs["Geometry"])
    return ng


def fill_group(ng, ri, ro):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-1400, 0)
    go.location = (8800, 0)
    ri.location = (0, 80)
    ro.location = (5400, 80)
    for name, st in (
        ("Pos", "VECTOR"),
        ("HeadingXY", "FLOAT"),
        ("HeadingZ", "FLOAT"),
        ("Size", "FLOAT"),
        ("P0", "VECTOR"),
        ("P1", "VECTOR"),
        ("P2", "VECTOR"),
    ):
        ro.repeat_items.new(st, name)

    g.links.new(gi.outputs["Count"], ri.inputs["Iterations"])

    start = g.vec((10.0, 70.0, 4.0), (-900, 400))
    g.links.new(start, ri.inputs["Pos"])
    g.links.new(start, ri.inputs["P0"])
    g.links.new(start, ri.inputs["P1"])
    g.links.new(start, ri.inputs["P2"])
    ri.inputs["HeadingXY"].default_value = -math.pi / 4
    ri.inputs["HeadingZ"].default_value = 0.08
    avg = g.math("MULTIPLY", g.math("ADD", gi.outputs["Size Min"], gi.outputs["Size Max"], loc=(-1100, 200)), 0.5, loc=(-900, 140))
    g.links.new(avg, ri.inputs["Size"])

    i = ri.outputs["Iteration"]
    pos = ri.outputs["Pos"]
    hxy = ri.outputs["HeadingXY"]
    hz = ri.outputs["HeadingZ"]
    prev_size = ri.outputs["Size"]
    prev0 = ri.outputs["P0"]
    prev1 = ri.outputs["P1"]
    prev2 = ri.outputs["P2"]
    acc = ri.outputs["Geometry"]

    # --- reverse / beat / size ---
    half = g.imath("DIVIDE_FLOOR", gi.outputs["Count"], 2, loc=(250, 700))
    past = g.cmp("GREATER_EQUAL", i, half, loc=(450, 700), dtype="INT")
    do_rev = g.bool("AND", gi.outputs["Reverse"], past, loc=(650, 700))
    sign = g.switch("FLOAT", do_rev, 1.0, -1.0, loc=(850, 700))

    u = g.rand(gi.outputs["Seed"], i, (250, 520))
    seed2 = g.imath("ADD", gi.outputs["Seed"], 11, loc=(250, 430))
    u2 = g.rand(seed2, i, (450, 430))
    seed3 = g.imath("ADD", gi.outputs["Seed"], 23, loc=(250, 340))
    u3 = g.rand(seed3, i, (450, 340))
    seed4 = g.imath("ADD", gi.outputs["Seed"], 37, loc=(250, 250))
    u4 = g.rand(seed4, i, (450, 250))
    seed5 = g.imath("ADD", gi.outputs["Seed"], 41, loc=(250, 160))
    u5 = g.rand(seed5, i, (450, 160))

    size_ind = g.math("MULTIPLY_ADD", g.math("SUBTRACT", gi.outputs["Size Max"], gi.outputs["Size Min"], loc=(450, 520)), u2, loc=(650, 520), c=gi.outputs["Size Min"])
    one_minus_c = g.math("SUBTRACT", 1.0, gi.outputs["Correlation"], loc=(650, 430))
    size_corr = g.math("ADD",
                       g.math("MULTIPLY", gi.outputs["Correlation"], prev_size, loc=(850, 500)),
                       g.math("MULTIPLY", one_minus_c, size_ind, loc=(850, 420)),
                       loc=(1050, 460))

    beat0 = g.cmp("EQUAL", gi.outputs["Beat N"], 0, loc=(650, 300), dtype="INT")
    beat_safe = g.switch("INT", beat0, gi.outputs["Beat N"], 1, loc=(850, 260))
    mod = g.imath("FLOORED_MODULO", i, beat_safe, loc=(1050, 260))
    is_mod0 = g.cmp("EQUAL", mod, 0, loc=(1250, 260), dtype="INT")
    is_beat = g.bool("AND", g.bool("NOT", beat0, loc=(1050, 180)), is_mod0, loc=(1250, 180))
    size_beat = g.switch("FLOAT", is_beat, size_corr, g.math("MULTIPLY", size_corr, gi.outputs["Beat Scale"], loc=(1250, 80)), loc=(1450, 140))

    count_minus = g.imath("ADD", gi.outputs["Count"], -1, loc=(650, -80))
    fade_t = g.math("DIVIDE", i, g.math("MAXIMUM", count_minus, 1.0, loc=(850, -80)), loc=(1050, -80))
    fade_mul = g.math("SUBTRACT", 1.0, g.math("MULTIPLY", fade_t, 0.5, loc=(1250, -80)), loc=(1450, -80))
    size_fade = g.math("MAXIMUM", gi.outputs["Size Min"], g.math("MULTIPLY", size_beat, fade_mul, loc=(1650, -40)), loc=(1850, -20))
    draw_size = g.switch("FLOAT", gi.outputs["Fade Affects Size"], size_beat, size_fade, loc=(2050, 80))

    # --- heading ---
    turn_scale = g.math("SUBTRACT", 1.0, g.math("MULTIPLY", gi.outputs["Correlation"], 0.65, loc=(850, 800)), loc=(1050, 800))
    max_rad = g.math("MULTIPLY", gi.outputs["Max Turn Deg"], math.pi / 180.0, loc=(850, 880))
    turn = g.math("MULTIPLY",
                  g.math("MULTIPLY", g.math("MULTIPLY", g.math("SUBTRACT", u3, 0.5, loc=(1050, 640)), 2.0, loc=(1250, 640)), max_rad, loc=(1450, 640)),
                  g.math("MULTIPLY", turn_scale, sign, loc=(1450, 720)),
                  loc=(1650, 680))
    new_hxy = g.math("ADD", hxy, turn, loc=(1850, 680))
    zturn = g.math("MULTIPLY", turn, 0.35, loc=(1850, 600))
    new_hz = g.math("MINIMUM", 0.45, g.math("MAXIMUM", -0.45, g.math("ADD", hz, g.math("MULTIPLY", zturn, u4, loc=(1850, 520)), loc=(2050, 560)), loc=(2250, 560)), loc=(2450, 560))

    cos_xy = g.math("COSINE", new_hxy, loc=(1850, 400))
    sin_xy = g.math("SINE", new_hxy, loc=(1850, 320))
    cos_z = g.math("COSINE", new_hz, loc=(1850, 240))
    sin_z = g.math("SINE", new_hz, loc=(1850, 160))
    T = g.vmath("NORMALIZE", g.combine(
        g.math("MULTIPLY", cos_xy, cos_z, loc=(2050, 400)),
        g.math("MULTIPLY", sin_xy, cos_z, loc=(2050, 320)),
        sin_z,
        loc=(2250, 320),
    ), loc=(2450, 320))

    step = g.math("MULTIPLY", draw_size, g.math("SUBTRACT", 1.02, gi.outputs["Overlap"], loc=(1850, 40)), loc=(2050, 40))
    moved = g.vmath("ADD", pos, g.vmath("SCALE", T, loc=(2250, 120), scale=step), loc=(2450, 80))
    is_first = g.cmp("EQUAL", i, 0, loc=(2250, -40), dtype="INT")
    new_pos = g.switch("VECTOR", is_first, moved, pos, loc=(2650, 0))

    box_min = g.vec((6.0, 6.0, 2.0), (2450, -120))
    box_max = g.vec((74.0, 74.0, 36.0), (2450, -200))
    new_pos = g.vmath("MINIMUM", g.vmath("MAXIMUM", new_pos, box_min, loc=(2850, -80)), box_max, loc=(3050, -80))

    # --- frame N, B ---
    up = g.vec((0.0, 0.0, 1.0), (2450, 200))
    alt_up = g.vec((0.0, 1.0, 0.0), (2450, 120))
    dot_up = g.vmath("DOT_PRODUCT", T, up, loc=(2650, 200))
    use_alt = g.cmp("GREATER_THAN", g.math("ABSOLUTE", dot_up, loc=(2850, 200)), 0.9, loc=(3050, 200))
    up2 = g.switch("VECTOR", use_alt, up, alt_up, loc=(3250, 200))
    B = g.vmath("NORMALIZE", g.vmath("CROSS_PRODUCT", T, up2, loc=(2650, 40)), loc=(2850, 40))
    N = g.vmath("CROSS_PRODUCT", B, T, loc=(3050, 40))

    roll = g.math("MULTIPLY", g.math("MULTIPLY", g.math("SUBTRACT", u, 0.5, loc=(2650, -200)), math.pi, loc=(2850, -200)), sign, loc=(3050, -200))
    cr = g.math("COSINE", roll, loc=(3250, -160))
    sr = g.math("SINE", roll, loc=(3250, -240))
    # N' = N*cos + cross(T,N)*sin
    Np = g.vmath("ADD",
                 g.vmath("SCALE", N, loc=(3450, 40), scale=cr),
                 g.vmath("SCALE", g.vmath("CROSS_PRODUCT", T, N, loc=(3450, -40)), loc=(3650, -40), scale=sr),
                 loc=(3850, 0))
    Bp = g.vmath("CROSS_PRODUCT", T, Np, loc=(3450, 140))

    # --- free triangle in plane: base + height + apex shift ---
    base = g.math("MAXIMUM", gi.outputs["Size Min"], g.math("MULTIPLY", draw_size, 0.85, loc=(2650, -320)), loc=(2850, -320))
    hmin = g.math("MULTIPLY", gi.outputs["Wall Thickness"], 1.15, loc=(2650, -400))
    height = g.math("MAXIMUM", hmin, g.math("MULTIPLY", draw_size, g.math("MULTIPLY_ADD", 0.35, u5, loc=(2650, -480), c=0.45), loc=(2850, -480)), loc=(3050, -400))
    shift = g.math("MULTIPLY", g.math("MULTIPLY", g.math("SUBTRACT", u4, 0.5, loc=(2650, -560)), base, loc=(2850, -560)), 0.9, loc=(3050, -560))
    half_b = g.math("MULTIPLY", base, 0.5, loc=(3050, -320))
    lx0 = g.math("SUBTRACT", 0.0, half_b, loc=(3250, -280))
    ly0 = g.value(0.0, (3250, -360))
    lx1 = half_b
    ly1 = ly0
    lx2 = shift
    ly2 = height

    def plane_pt(lx, ly, loc):
        return g.vmath("ADD",
                       g.vmath("ADD", new_pos, g.vmath("SCALE", Np, loc=loc, scale=lx), loc=(loc[0] + 200, loc[1])),
                       g.vmath("SCALE", Bp, loc=(loc[0] + 200, loc[1] - 80), scale=ly),
                       loc=(loc[0] + 400, loc[1] - 40))

    raw0 = plane_pt(lx0, ly0, (3250, -640))
    raw1 = plane_pt(lx1, ly1, (3250, -820))
    raw2 = plane_pt(lx2, ly2, (3250, -1000))

    share = g.math("MULTIPLY", gi.outputs["Overlap"], g.math("MULTIPLY_ADD", 0.15, u5, loc=(2650, -720), c=0.45), loc=(2850, -720))
    share_i = g.switch("FLOAT", is_first, share, 0.0, loc=(3050, -720))

    def mixv(a, b, t, loc):
        return g.vmath("ADD", a, g.vmath("SCALE", g.vmath("SUBTRACT", b, a, loc=loc), loc=(loc[0] + 180, loc[1]), scale=t), loc=(loc[0] + 360, loc[1]))

    p0 = mixv(raw0, prev0, share_i, (3600, -640))
    p1 = mixv(raw1, prev1, g.math("MULTIPLY", share_i, 0.55, loc=(3400, -820)), (3600, -820))
    p2 = raw2

    q0 = g.vmath("ADD", p0, g.vmath("SCALE", T, loc=(3900, -640), scale=gi.outputs["Prism Thickness"]), loc=(4100, -640))
    q1 = g.vmath("ADD", p1, g.vmath("SCALE", T, loc=(3900, -820), scale=gi.outputs["Prism Thickness"]), loc=(4100, -820))
    q2 = g.vmath("ADD", p2, g.vmath("SCALE", T, loc=(3900, -1000), scale=gi.outputs["Prism Thickness"]), loc=(4100, -1000))

    pts = g.node("GeometryNodePoints", (4300, -700))
    pts.inputs["Count"].default_value = 6
    idx = g.node("GeometryNodeInputIndex", (4300, -860))
    sw = g.node("GeometryNodeIndexSwitch", (4500, -700), data_type="VECTOR")
    while len(sw.index_switch_items) < 6:
        sw.index_switch_items.new()
    g.links.new(idx.outputs["Index"], sw.inputs["Index"])
    g.links.new(p0, sw.inputs[1])
    g.links.new(p1, sw.inputs[2])
    g.links.new(p2, sw.inputs[3])
    g.links.new(q0, sw.inputs[4])
    g.links.new(q1, sw.inputs[5])
    g.links.new(q2, sw.inputs[6])
    g.links.new(sw.outputs[0], pts.inputs["Position"])
    hull = g.node("GeometryNodeConvexHull", (4700, -700))
    g.links.new(pts.outputs["Points"], hull.inputs["Geometry"])

    join = g.node("GeometryNodeJoinGeometry", (4900, -400))
    g.links.new(acc, join.inputs[0])
    g.links.new(hull.outputs[0], join.inputs[0])
    merged = g.switch("GEOMETRY", is_first, join.outputs["Geometry"], hull.outputs["Convex Hull"], loc=(5100, -280))

    g.links.new(merged, ro.inputs["Geometry"])
    g.links.new(new_pos, ro.inputs["Pos"])
    g.links.new(new_hxy, ro.inputs["HeadingXY"])
    g.links.new(new_hz, ro.inputs["HeadingZ"])
    g.links.new(size_corr, ro.inputs["Size"])
    g.links.new(p0, ro.inputs["P0"])
    g.links.new(p1, ro.inputs["P1"])
    g.links.new(p2, ro.inputs["P2"])

    # --- keep largest island ---
    mesh_out = ro.outputs["Geometry"]
    merge = g.node("GeometryNodeMergeByDistance", (5600, 80))
    merge.inputs["Distance"].default_value = 0.05
    g.links.new(mesh_out, merge.inputs["Geometry"])
    island = g.node("GeometryNodeInputMeshIsland", (5850, 260))
    eq = g.cmp("EQUAL", island.outputs["Island Index"], 0, loc=(6000, 260), dtype="INT")
    sep = g.node("GeometryNodeSeparateGeometry", (6150, 80), domain="FACE")
    g.links.new(merge.outputs["Geometry"], sep.inputs["Geometry"])
    g.links.new(eq, sep.inputs["Selection"])
    mb = g.node("GeometryNodeMeshBoolean", (6400, 80))
    mb.operation = "UNION"
    mb.solver = "EXACT"
    try:
        mb.inputs["Self Intersection"].default_value = True
        mb.inputs["Hole Tolerant"].default_value = True
    except Exception:
        pass
    g.links.new(sep.outputs["Selection"], mb.inputs[0])
    g.links.new(sep.outputs["Inverted"], mb.inputs[1])
    go.location = (6700, 80)
    g.links.new(mb.outputs[0], go.inputs["Geometry"])
    return ng


def setup_scene(ng):
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"

    obj = bpy.data.objects.get("Cube") or bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        mesh = bpy.data.meshes.new(OBJ_NAME)
        obj = bpy.data.objects.new(OBJ_NAME, mesh)
        bpy.context.collection.objects.link(obj)
    obj.name = OBJ_NAME
    obj.location = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    for mod in list(obj.modifiers):
        obj.modifiers.remove(mod)
    mod = obj.modifiers.new("TraceShell", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    return obj


def write_stl(obj, path):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    mesh = ev.to_mesh()
    mesh.calc_loop_triangles()
    tris = []
    for lt in mesh.loop_triangles:
        co = [tuple(mesh.vertices[i].co) for i in lt.vertices]
        n = tuple(lt.normal)
        tris.append((n, co[0], co[1], co[2]))
    ev.to_mesh_clear()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"TraceShell".ljust(80, b"\0"))
        f.write(struct_pack_count(len(tris)))
        for n, a, b, c in tris:
            f.write(_pack_tri(n, a, b, c))
    return len(tris)


def struct_pack_count(n):
    import struct
    return struct.pack("<I", n)


def _pack_tri(n, a, b, c):
    import struct
    return struct.pack("<12fH", *(n + a + b + c + (0,)))


def blender_check(obj):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    mesh = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    nonmanifold = sum(1 for e in bm.edges if not e.is_manifold)
    boundary = sum(1 for e in bm.edges if e.is_boundary)
    vol = bm.calc_volume(signed=True)
    # islands via verts
    seen = set()
    islands = 0
    from collections import deque
    adj = {v.index: [e.other_vert(v).index for e in v.link_edges] for v in bm.verts}
    for v in bm.verts:
        if v.index in seen:
            continue
        islands += 1
        q = deque([v.index])
        seen.add(v.index)
        while q:
            cur = q.popleft()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
    bbox = [tuple(mesh.vertices[i].co) for i in range(len(mesh.vertices))] if mesh.vertices else []
    if bbox:
        xs, ys, zs = zip(*bbox)
        bounds = ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)))
        size = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    else:
        bounds = ((0, 0, 0), (0, 0, 0))
        size = (0, 0, 0)

    # Helix side faces are non-planar quads; rays from quad centers graze the same face.
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.faces.ensure_lookup_table()
    from mathutils.bvhtree import BVHTree
    tree = BVHTree.FromBMesh(bm)
    min_th = None
    hits = 0
    for face in bm.faces:
        if face.calc_area() < 0.2:
            continue
        origin = face.calc_center_median() - face.normal * 0.15
        hit = tree.ray_cast(origin, -face.normal, 1000.0)
        if hit is None:
            continue
        loc, nrm, idx, dist = hit
        if nrm is not None and abs(nrm.dot(face.normal)) < 0.3:
            continue
        th = dist + 0.15
        if 0.2 < th < 80.0:
            hits += 1
            min_th = th if min_th is None else min(min_th, th)
    nverts = len(bm.verts)
    nfaces = len(bm.faces)
    bm.free()
    ev.to_mesh_clear()
    return {
        "verts": nverts,
        "faces": nfaces,
        "nonmanifold_edges": nonmanifold,
        "boundary_edges": boundary,
        "volume_mm3": vol,
        "islands": islands,
        "bounds_min": bounds[0],
        "bounds_max": bounds[1],
        "size_mm": size,
        "min_thickness_mm": min_th,
        "thickness_samples": hits,
    }


def main():
    import traceback
    RESULT = {"ok": False}
    try:
        _clear_test_groups()
        for ob_name in ("_LoopTest",):
            ob = bpy.data.objects.get(ob_name)
            if ob:
                bpy.data.objects.remove(ob, do_unlink=True)
        ng = create_group()
        obj = setup_scene(ng)
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception:
            pass
        fill_helix(ng)
        bpy.context.view_layer.update()
        check = blender_check(obj)
        stl_path = os.path.join(ROOT, "triangles_trace_shell.stl")
        ntris = write_stl(obj, stl_path)
        blend_path = os.path.join(ROOT, "triangles_trace_shell.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        RESULT = {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "stl_tris": ntris,
            "check": check,
            "blend": blend_path,
            "stl": stl_path,
        }
    except Exception as e:
        RESULT = {"ok": False, "error": str(e), "trace": traceback.format_exc()}
    return RESULT


RESULT = main()
