"""Planetary harmonic core: wide foot, waist, spherical bulge, flat mouth.

Fins are a 7-fold cosine. Twist runs from 0 to the slider between 30% and 70%
of the height. Where that twist is fast, or the radius is tight, the fin depth
is held down so the wall stays >= 1.5 mm and the flare stays under 45 degrees.

Does not delete TraceShell, NoiseDisplacedSolid, SphereTubeNet, or the
earlier resonator objects.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "HarmonicCoreGN"
OBJ_NAME = "HarmonicCore"
HIDE_OBJECTS = (
    "TraceShell",
    "NoiseDisplacedSolid",
    "SphereTubeNet",
    "SchumannResonator",
    "TopographicResonator",
)

WALL_MM = 3.5
# Outer rings. At 24 ribs and ~300° of twist, 160 rings jump the crest by ~6
# vertices per step, which reads as a sawtooth. 960 rings moves it about one
# vertex per step. Around the circle, 288 is 12 samples per rib.
VERTS = 288
SIDE_SEGMENTS = 960


class GN:
    def __init__(self, ng):
        self.ng = ng
        self.links = ng.links

    def node(self, idname, loc, **kw):
        node = self.ng.nodes.new(idname)
        node.location = loc
        for k, v in kw.items():
            if hasattr(node, k):
                setattr(node, k, v)
        return node

    def math(self, op, a, b=None, c=None, loc=(0, 0)):
        node = self.node("ShaderNodeMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        if c is not None:
            self._in(node, 2, c)
        return node.outputs[0]

    def _in(self, node, key, sock):
        if sock is None:
            return
        target = node.inputs[key] if not isinstance(key, int) else node.inputs[key]
        if hasattr(sock, "rna_type"):
            self.links.new(sock, target)
        else:
            target.default_value = sock


def _iface(ng, name, stype, default, vmin, vmax, desc, subtype=None):
    item = ng.interface.new_socket(name=name, in_out="INPUT", socket_type=stype)
    item.description = desc
    if subtype:
        item.subtype = subtype
    item.default_value = default
    item.min_value = vmin
    item.max_value = vmax
    return item


def create_group():
    if GROUP_NAME in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[GROUP_NAME])
    ng = bpy.data.node_groups.new(GROUP_NAME, "GeometryNodeTree")
    try:
        ng.is_modifier = True
    except Exception:
        pass
    ng.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    _iface(ng, "Base Radius", "NodeSocketFloat", 35.0, 24.0, 45.0, "底部半径，mm", "DISTANCE")
    _iface(ng, "Waist Radius", "NodeSocketFloat", 18.0, 12.0, 28.0, "30% 高度的束腰半径，mm", "DISTANCE")
    _iface(ng, "Core Radius", "NodeSocketFloat", 32.0, 20.0, 42.0, "70% 高度的球面半径，mm", "DISTANCE")
    _iface(ng, "Top Radius", "NodeSocketFloat", 14.0, 8.0, 24.0, "顶部平切口半径，mm", "DISTANCE")
    _iface(ng, "Height", "NodeSocketFloat", 85.0, 80.0, 90.0, "高度，mm", "DISTANCE")
    _iface(ng, "Harmonic Frequency", "NodeSocketInt", 12, 5, 32, "一圈翼片的条数")
    _iface(
        ng, "Fin Amplitude", "NodeSocketFloat", 6.0, 0.0, 8.0,
        "翼片目标深度，mm。条数变多时，同样壁厚下实际深度会变浅",
        "DISTANCE",
    )
    _iface(
        ng, "Helix Twist", "NodeSocketFloat", math.radians(285.0),
        0.0, math.radians(540.0),
        "30% 到 70% 之间转过的角度。两端转速为 0。12 条肋时 285° 让上下肋错开半格；360° 会重新对齐",
        "ANGLE",
    )
    _iface(
        ng, "Wall Thickness", "NodeSocketFloat", WALL_MM, 2.0, 4.0,
        "沿半径的壁厚，mm。陡的翼片上，真实壁厚会薄于这个数",
        "DISTANCE",
    )
    _iface(
        ng, "Pulse Intensity", "NodeSocketFloat", 0.7, 0.0, 3.0,
        "呼吸幅度，mm。波峰停在可打印的深度上，波谷再收进去",
        "DISTANCE",
    )
    _iface(ng, "Time Scale", "NodeSocketFloat", 30.0, 1.0, 240.0, "帧数除以这个数得到时间 t。30 是一拍呼吸的示例")
    _iface(
        ng, "Breath Amplitude", "NodeSocketFloat", 4.0, 0.0, 8.0,
        "腰和鼓起的外扩，mm。呼吸因子再乘上这个数，大约 3–5 mm",
        "DISTANCE",
    )
    _iface(
        ng, "Spin Rate", "NodeSocketFloat", 0.2, 0.0, 2.0,
        "肋条相位每单位时间转过的弧度。0.2 是缓转",
    )
    _iface(
        ng, "Crest Radius", "NodeSocketFloat", 1.5, 0.4, 4.0,
        "肋脊最小圆角，mm。1.5 是手指按上去是圆的；再小，印出来会割手",
        "DISTANCE",
    )
    _iface(
        ng, "Shape Amount", "NodeSocketFloat", 0.12, 0.0, 0.40,
        "开口和整体一起呼吸的幅度。0.12 时身体上下 12%，口径上下 22%。0 就只剩旋转",
    )
    _iface(ng, "Petal Count", "NodeSocketInt", 5, 3, 8, "顶口和底口的花瓣数。必须是整数，接缝才闭得上")
    ng.nodes.new("NodeGroupInput")
    ng.nodes.new("NodeGroupOutput")
    return ng


def _compare(g, op, a, b, loc):
    node = g.node("FunctionNodeCompare", loc, data_type="FLOAT", operation=op)
    g._in(node, "A", a)
    g._in(node, "B", b)
    return node.outputs["Result"]


def _bool(g, op, a, b=None, loc=(0, 0)):
    node = g.node("FunctionNodeBooleanMath", loc, operation=op)
    g._in(node, 0, a)
    if b is not None:
        g._in(node, 1, b)
    return node.outputs[0]


def _switch(g, cond, when_false, when_true, loc):
    node = g.node("GeometryNodeSwitch", loc, input_type="FLOAT")
    g._in(node, "Switch", cond)
    g._in(node, "False", when_false)
    g._in(node, "True", when_true)
    return node.outputs["Output"]


def _smoothstep(g, edge0, edge1, x, loc):
    span = g.math("SUBTRACT", x, edge0, loc=(loc[0] - 160, loc[1]))
    span = g.math("DIVIDE", span, edge1 - edge0, loc=(loc[0] - 20, loc[1]))
    u = g.math("MAXIMUM", 0.0, span, loc=loc)
    u = g.math("MINIMUM", 1.0, u, loc=(loc[0] + 140, loc[1]))
    u2 = g.math("MULTIPLY", u, u, loc=(loc[0] + 280, loc[1]))
    two_u = g.math("MULTIPLY", u, 2.0, loc=(loc[0] + 280, loc[1] - 70))
    three = g.math("SUBTRACT", 3.0, two_u, loc=(loc[0] + 420, loc[1] - 70))
    return g.math("MULTIPLY", u2, three, loc=(loc[0] + 560, loc[1]))


def _clamped_u(g, edge0, edge1, x, loc):
    span = g.math("SUBTRACT", x, edge0, loc=(loc[0] - 80, loc[1]))
    span = g.math("DIVIDE", span, edge1 - edge0, loc=loc)
    u = g.math("MAXIMUM", 0.0, span, loc=(loc[0] + 140, loc[1]))
    return g.math("MINIMUM", 1.0, u, loc=(loc[0] + 280, loc[1]))


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-2600, 0)
    go.location = (2600, 200)

    nu = VERTS
    nv = SIDE_SEGMENTS
    rings = 2 * nv + 3
    cyl = g.node("GeometryNodeMeshCylinder", (-2300, 280), fill_type="NONE")
    cyl.inputs["Vertices"].default_value = nu
    cyl.inputs["Side Segments"].default_value = rings - 1
    cyl.inputs["Radius"].default_value = 1.0
    cyl.inputs["Depth"].default_value = float(rings - 1)

    pos = g.node("GeometryNodeInputPosition", (-2300, -40))
    sep = g.node("ShaderNodeSeparateXYZ", (-2080, -40))
    g.links.new(pos.outputs["Position"], sep.inputs["Vector"])
    ring = g.math("ROUND", g.math("ADD", sep.outputs["Z"], float(nv + 1), loc=(-1880, -40)), loc=(-1680, -40))
    theta = g.math("ARCTAN2", sep.outputs["Y"], sep.outputs["X"], loc=(-1680, 80))

    is_weld = _compare(g, "GREATER_EQUAL", ring, float(2 * nv + 2) - 0.5, (-1680, -180))
    is_past = _compare(g, "GREATER_THAN", ring, float(nv), (-1680, -300))
    not_weld = _bool(g, "NOT", is_weld, loc=(-1480, -180))
    is_inner = _bool(g, "AND", is_past, not_weld, loc=(-1280, -240))

    t_outer = g.math("DIVIDE", ring, float(nv), loc=(-1480, -420))
    inner_k = g.math("SUBTRACT", ring, float(nv + 1), loc=(-1480, -540))
    t_inner = g.math(
        "SUBTRACT", 1.0,
        g.math("DIVIDE", inner_k, float(nv), loc=(-1280, -540)),
        loc=(-1080, -540),
    )
    t_body = _switch(g, is_inner, t_outer, t_inner, (-880, -420))
    t = _switch(g, is_weld, t_body, 0.0, (-680, -360))

    # One planetary breath: the whole body and the two openings share sin(t).
    # Openings use a larger gain, so the caliber moves more than the silhouette.
    scene_time = g.node("GeometryNodeInputSceneTime", (-2300, -900))
    t_time = g.math("DIVIDE", scene_time.outputs["Frame"], gi.outputs["Time Scale"], loc=(-2000, -900))
    shape = gi.outputs["Shape Amount"]
    breath = g.math("SINE", t_time, loc=(-1800, -980))

    def _swell(sock, gain, loc):
        amp = g.math("MULTIPLY", shape, gain, loc=(loc[0] - 180, loc[1] - 60))
        scale = g.math("MULTIPLY_ADD", breath, amp, 1.0, loc=loc)
        return g.math("MULTIPLY", sock, scale, loc=(loc[0] + 180, loc[1]))

    base_r = _swell(gi.outputs["Base Radius"], 1.80, (-1100, 700))
    top_r = _swell(gi.outputs["Top Radius"], 1.80, (-1100, 560))
    waist_r = _swell(gi.outputs["Waist Radius"], 1.0, (-1100, 420))
    core_r = _swell(gi.outputs["Core Radius"], 1.0, (-1100, 280))
    height_r = _swell(gi.outputs["Height"], 1.0, (-1100, 140))
    helix_r = _swell(gi.outputs["Helix Twist"], 0.35, (-1100, 0))
    fin_r = _swell(gi.outputs["Fin Amplitude"], 0.40, (-1100, -140))
    crest_r = _swell(gi.outputs["Crest Radius"], 0.20, (-1100, -280))
    wall_r = _swell(gi.outputs["Wall Thickness"], 0.12, (-1100, -420))

    # Wide foot, smooth waist at 30%, smooth maximum at 70%, flat mouth.
    s_waist = _smoothstep(g, 0.05, 0.30, t, (-400, 420))
    s_core = _smoothstep(g, 0.30, 0.70, t, (-400, 280))
    s_top = _smoothstep(g, 0.70, 0.96, t, (-400, 140))
    d_waist = g.math("SUBTRACT", waist_r, base_r, loc=(-200, 520))
    d_core = g.math("SUBTRACT", core_r, waist_r, loc=(-200, 380))
    d_top = g.math("SUBTRACT", top_r, core_r, loc=(-200, 240))
    r1 = g.math("MULTIPLY_ADD", s_waist, d_waist, base_r, loc=(40, 460))
    r2 = g.math("MULTIPLY_ADD", s_core, d_core, r1, loc=(240, 380))
    radius_profile = g.math("MULTIPLY_ADD", s_top, d_top, r2, loc=(440, 300))

    # BreathFactor = sin(t·0.5)·0.7 + abs(cos(t·1.5))·0.3
    # Slow sine plus a quicker absolute cosine: inhale, hold, faster exhale.
    slow = g.math("SINE", g.math("MULTIPLY", t_time, 0.5, loc=(560, 160)), loc=(740, 160))
    quick = g.math("ABSOLUTE", g.math("COSINE", g.math("MULTIPLY", t_time, 1.5, loc=(560, 40)), loc=(740, 40)), loc=(920, 40))
    breath = g.math(
        "MULTIPLY_ADD",
        slow,
        0.7,
        g.math("MULTIPLY", quick, 0.3, loc=(920, 120)),
        loc=(1100, 140),
    )
    swell = _smoothstep(g, 0.14, 0.30, t, (740, -80))
    swell_out = _smoothstep(g, 0.72, 0.90, t, (740, -160))
    swell = g.math("MULTIPLY", swell, g.math("SUBTRACT", 1.0, swell_out, loc=(1100, -120)), loc=(1280, -80))
    r_breath = g.math(
        "MULTIPLY",
        g.math("MULTIPLY", breath, gi.outputs["Breath Amplitude"], loc=(1280, 40)),
        swell,
        loc=(1480, 20),
    )
    radius_profile = g.math("ADD", radius_profile, r_breath, loc=(1660, 200))

    # Middle twist: BaseTwist + t·0.1, still zero at 30% and at 70%.
    twist_s = _smoothstep(g, 0.30, 0.70, t, (-400, -40))
    twist = g.math(
        "MULTIPLY",
        g.math("MULTIPLY_ADD", t_time, 0.1, helix_r, loc=(-200, -40)),
        twist_s,
        loc=(40, -40),
    )

    # Ridge curvature is A · n² · (1/R² + (dΦ/dz)²). Cap A so the crest
    # radius stays at Crest Radius.
    n = gi.outputs["Harmonic Frequency"]
    a_thick = g.math(
        "MULTIPLY",
        g.math("DIVIDE", 1.50, n, loc=(800, -440)),
        radius_profile,
        loc=(980, -440),
    )
    a_deep = g.math("MINIMUM", fin_r, a_thick, loc=(1180, -440))
    u_tw = _clamped_u(g, 0.30, 0.70, t, (700, -280))
    ds_du = g.math(
        "MULTIPLY",
        6.0,
        g.math("MULTIPLY", u_tw, g.math("SUBTRACT", 1.0, u_tw, loc=(900, -360)), loc=(1080, -320)),
        loc=(1260, -320),
    )
    rate_z = g.math(
        "DIVIDE",
        g.math("MULTIPLY", helix_r, g.math("DIVIDE", ds_du, 0.40, loc=(1260, -440)), loc=(1460, -400)),
        height_r,
        loc=(1660, -400),
    )
    inv_r = g.math("DIVIDE", 1.0, radius_profile, loc=(1460, -520))
    grad2 = g.math(
        "MULTIPLY",
        g.math("MULTIPLY", n, n, loc=(1660, -560)),
        g.math(
            "ADD",
            g.math("MULTIPLY", inv_r, inv_r, loc=(1660, -640)),
            g.math("MULTIPLY", rate_z, rate_z, loc=(1660, -720)),
            loc=(1840, -640),
        ),
        loc=(2040, -560),
    )
    a_round = g.math(
        "DIVIDE",
        1.0,
        g.math("MULTIPLY", crest_r, grad2, loc=(2220, -520)),
        loc=(2400, -480),
    )
    a_cap = g.math("MINIMUM", a_deep, a_round, loc=(1480, -80))
    body_in = _smoothstep(g, 0.08, 0.18, t, (700, 200))
    body_out = _smoothstep(g, 0.84, 0.94, t, (700, 80))
    body = g.math("MULTIPLY", body_in, g.math("SUBTRACT", 1.0, body_out, loc=(1100, 140)), loc=(1280, 160))
    a_body = g.math("MULTIPLY", a_cap, body, loc=(1680, 40))
    # The crest-radius cap flattens the fast twist. Put a groove back
    # through that band so the ribs actually spiral. 0.80·R/n is shallower
    # than the bulb flutes, deep enough to read.
    a_twist_cap = g.math(
        "MULTIPLY",
        g.math("DIVIDE", 0.80, n, loc=(800, -200)),
        radius_profile,
        loc=(1000, -200),
    )
    a_twist = g.math("MINIMUM", a_deep, a_twist_cap, loc=(1200, -160))
    mid_in = _smoothstep(g, 0.30, 0.36, t, (700, -20))
    mid_out = _smoothstep(g, 0.64, 0.72, t, (700, -100))
    mid_mask = g.math(
        "MULTIPLY",
        mid_in,
        g.math("SUBTRACT", 1.0, mid_out, loc=(1100, -60)),
        loc=(1280, -40),
    )
    a_mid = g.math("MULTIPLY", a_twist, mid_mask, loc=(1480, -40))
    a_eff = g.math("MAXIMUM", a_body, a_mid, loc=(1680, -20))

    # Breath stays inside the local depth, so a 0.7 mm pulse cannot erase
    # the twist groove.
    sine = g.math("SINE", t_time, loc=(-1800, -800))
    pulse_use = g.math(
        "MINIMUM",
        gi.outputs["Pulse Intensity"],
        g.math("MULTIPLY", a_eff, 0.45, loc=(1880, -40)),
        loc=(2060, -20),
    )
    rest = g.math("SUBTRACT", a_eff, pulse_use, loc=(2240, 40))
    breathed = g.math("MULTIPLY_ADD", sine, pulse_use, rest, loc=(2420, 40))
    breathed = g.math("MAXIMUM", breathed, 0.0, loc=(2580, -20))
    a_live = g.math("MINIMUM", breathed, a_eff, loc=(2740, 40))

    spin = g.math("MULTIPLY", t_time, gi.outputs["Spin Rate"], loc=(1500, -160))
    phi = g.math("ADD", g.math("ADD", theta, twist, loc=(1680, -40)), spin, loc=(1860, -40))
    nphi = g.math("MULTIPLY", n, phi, loc=(1860, -80))
    wave = g.math("COSINE", nphi, loc=(2040, -80))
    disp = g.math("MULTIPLY", a_live, wave, loc=(2220, 40))

    # Petals at the foot and the mouth. The phase turns along z, so the
    # wall is a crank rather than a vertical extrusion. Top lobes sit
    # half a petal off the bottom ones.
    foot_env = g.math(
        "SUBTRACT", 1.0, _smoothstep(g, 0.04, 0.22, t, (1500, 280)), loc=(1900, 280),
    )
    top_env = _smoothstep(g, 0.78, 0.96, t, (1500, 180))
    petal_env = g.math("ADD", foot_env, top_env, loc=(2100, 230))
    a_petal = g.math(
        "MINIMUM",
        4.2,
        g.math("MULTIPLY", 0.15, radius_profile, loc=(1700, 360)),
        loc=(1900, 360),
    )
    a_petal = g.math("MULTIPLY", a_petal, petal_env, loc=(2280, 280))
    half_petal = g.math("DIVIDE", math.pi, gi.outputs["Petal Count"], loc=(1700, 80))
    crank = g.math(
        "MULTIPLY_ADD",
        top_env,
        g.math("ADD", half_petal, 0.70, loc=(1900, 40)),
        g.math("MULTIPLY", foot_env, 0.70, loc=(1900, 120)),
        loc=(2100, 80),
    )
    crank = g.math("ADD", crank, g.math("MULTIPLY", t_time, gi.outputs["Spin Rate"], loc=(2100, -20)), loc=(2280, 60))
    petal_phi = g.math(
        "MULTIPLY",
        gi.outputs["Petal Count"],
        g.math("ADD", theta, crank, loc=(2280, 140)),
        loc=(2460, 160),
    )
    disp = g.math(
        "MULTIPLY_ADD",
        a_petal,
        g.math("COSINE", petal_phi, loc=(2460, 260)),
        disp,
        loc=(2660, 80),
    )
    r_outer = g.math("ADD", radius_profile, disp, loc=(2840, 180))
    r_outer = g.math("MAXIMUM", r_outer, g.math("ADD", wall_r, 1.0, loc=(2220, 280)), loc=(2380, 180))
    r_inner = g.math("SUBTRACT", r_outer, wall_r, loc=(2380, 40))
    r_inner = g.math("MAXIMUM", r_inner, 1.0, loc=(2540, 40))
    radius = _switch(g, is_inner, r_outer, r_inner, (2540, 160))

    cos_th = g.math("COSINE", theta, loc=(2380, -160))
    sin_th = g.math("SINE", theta, loc=(2380, -280))
    x = g.math("MULTIPLY", radius, cos_th, loc=(2580, -160))
    y = g.math("MULTIPLY", radius, sin_th, loc=(2580, -280))
    z0 = g.math("MULTIPLY", height_r, t, loc=(2380, -400))
    comb = g.node("ShaderNodeCombineXYZ", (2760, -80))
    g.links.new(x, comb.inputs["X"])
    g.links.new(y, comb.inputs["Y"])
    g.links.new(z0, comb.inputs["Z"])

    setpos = g.node("GeometryNodeSetPosition", (2760, 280))
    g.links.new(cyl.outputs["Mesh"], setpos.inputs["Geometry"])
    g.links.new(comb.outputs["Vector"], setpos.inputs["Position"])
    merge = g.node("GeometryNodeMergeByDistance", (2960, 280))
    g.links.new(setpos.outputs["Geometry"], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.001
    shade = g.node("GeometryNodeSetShadeSmooth", (3160, 280))
    shade.inputs["Shade Smooth"].default_value = True
    g.links.new(merge.outputs["Geometry"], shade.inputs["Mesh"])
    g.links.new(shade.outputs["Mesh"], go.inputs["Geometry"])


def _smooth_by_angle(obj):
    path = (
        "/Applications/Blender.app/Contents/Resources/5.2/"
        "datafiles/assets/nodes/geometry_nodes_essentials.blend"
    )
    try:
        if "Smooth by Angle" not in bpy.data.node_groups:
            with bpy.data.libraries.load(path, link=False) as (src, dst):
                dst.node_groups = ["Smooth by Angle"]
        mod = obj.modifiers.get("Smooth by Angle")
        if mod is None:
            mod = obj.modifiers.new("Smooth by Angle", "NODES")
            mod.node_group = bpy.data.node_groups["Smooth by Angle"]
        # 60°: the helix stays one smooth surface. The flat foot is nearer 90° and stays crisp.
        for item in mod.node_group.interface.items_tree:
            if getattr(item, "name", "") == "Angle":
                mod.properties.inputs[item.identifier]["value"] = math.radians(60.0)
    except Exception:
        pass


def setup_object(ng):
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    obj = bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        mesh = bpy.data.meshes.new(OBJ_NAME)
        obj = bpy.data.objects.new(OBJ_NAME, mesh)
        bpy.context.collection.objects.link(obj)
    obj.hide_set(False)
    obj.hide_viewport = False
    obj.location = (0.0, 0.0, 0.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    for name in HIDE_OBJECTS:
        other = bpy.data.objects.get(name)
        if other is not None:
            other.hide_viewport = True
    for mod in list(obj.modifiers):
        obj.modifiers.remove(mod)
    mod = obj.modifiers.new("HarmonicCore", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.objects.active = obj
    for selected in list(bpy.context.selected_objects):
        selected.select_set(False)
    obj.select_set(True)
    _smooth_by_angle(obj)
    names = [m.name for m in obj.modifiers]
    if "HarmonicCore" in names:
        obj.modifiers.move(names.index("HarmonicCore"), 0)
    return obj


def _islands(bm):
    seen = set()
    islands = 0
    adj = {v.index: [e.other_vert(v).index for e in v.link_edges] for v in bm.verts}
    for v in bm.verts:
        if v.index in seen:
            continue
        islands += 1
        q = deque([v.index])
        seen.add(v.index)
        while q:
            cur = q.popleft()
            for nb in adj.get(cur, []):
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
    return islands


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
    islands = _islands(bm)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    zmin = min(zs)
    worst_nz = 0.0
    over_45 = 0
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z < zmin + 0.6:
            continue
        if c.xy.length < 1.0:
            continue
        if f.normal.xy.dot(c.xy) <= 0.0:
            continue
        if f.normal.z < worst_nz:
            worst_nz = f.normal.z
        if f.normal.z < -0.7071:
            over_45 += 1
    overhang_deg = math.degrees(math.asin(min(1.0, max(0.0, -worst_nz))))
    foot = [v for v in bm.verts if v.co.z < zmin + 0.3]
    foot_r = sorted(math.hypot(v.co.x, v.co.y) for v in foot)
    # A full self-intersection scan on the dense helix is what froze the machine before.
    # Manifold, boundary, and volume still run on every build.
    if len(bm.faces) > 200000:
        out = {
            "verts": len(bm.verts),
            "faces": len(bm.faces),
            "nonmanifold_edges": nonmanifold,
            "boundary_edges": boundary,
            "volume_mm3": round(vol, 2),
            "islands": islands,
            "min_z": round(zmin, 3),
            "max_z": round(max(zs), 3),
            "size_mm": (
                round(max(xs) - min(xs), 2),
                round(max(ys) - min(ys), 2),
                round(max(zs) - min(zs), 2),
            ),
            "self_intersect_pairs": None,
            "self_intersect_skipped": True,
            "thick_min": None,
            "thick_p5": None,
            "thick_p50": None,
            "outer_overhang_deg": round(overhang_deg, 1),
            "outer_faces_over_45": over_45,
            "foot_r_mm": (
                round(foot_r[0], 2) if foot_r else None,
                round(foot_r[-1], 2) if foot_r else None,
            ),
            "modifiers": [m.name for m in obj.modifiers],
        }
        bm.free()
        ev.to_mesh_clear()
        return out
    bm_t = bm.copy()
    bmesh.ops.triangulate(bm_t, faces=bm_t.faces)
    bm_t.faces.ensure_lookup_table()
    bm_t.normal_update()
    tree = BVHTree.FromBMesh(bm_t)
    from mathutils.geometry import intersect_ray_tri
    cross = 0
    for a, b in tree.overlap(tree) or []:
        if a >= b:
            continue
        fa, fb = bm_t.faces[a], bm_t.faces[b]
        if {v.index for v in fa.verts} & {v.index for v in fb.verts}:
            continue
        if (fa.calc_center_median() - fb.calc_center_median()).length > 1.2:
            continue
        ta = [v.co.copy() for v in fa.verts]
        tb = [v.co.copy() for v in fb.verts]
        cut = False
        for src, tri in ((ta, tb), (tb, ta)):
            for k in range(3):
                a0, a1 = src[k], src[(k + 1) % 3]
                direction = a1 - a0
                length = direction.length
                if length < 1e-6:
                    continue
                hit = intersect_ray_tri(tri[0], tri[1], tri[2], direction / length, a0)
                if hit is None:
                    continue
                along = (hit - a0).dot(direction)
                if 0.02 * length < along < 0.98 * length:
                    cut = True
                    break
            if cut:
                break
        if cut:
            cross += 1
    thicks = []
    for f in bm_t.faces:
        if f.calc_area() < 0.02 or abs(f.normal.z) > 0.55:
            continue
        origin = f.calc_center_median() - f.normal * 0.15
        loc, nrm, _idx, dist = tree.ray_cast(origin, -f.normal, 8.0)
        if loc is None or nrm is None or nrm.dot(f.normal) > -0.35:
            continue
        thickness = dist + 0.15
        if thickness < 0.4:
            continue
        thicks.append(thickness)
    thicks.sort()

    def _pct(p):
        if not thicks:
            return None
        i = min(len(thicks) - 1, int(p / 100.0 * (len(thicks) - 1)))
        return round(thicks[i], 3)

    out = {
        "verts": len(bm.verts),
        "faces": len(bm.faces),
        "nonmanifold_edges": nonmanifold,
        "boundary_edges": boundary,
        "volume_mm3": round(vol, 2),
        "islands": islands,
        "min_z": round(zmin, 3),
        "max_z": round(max(zs), 3),
        "size_mm": (
            round(max(xs) - min(xs), 2),
            round(max(ys) - min(ys), 2),
            round(max(zs) - min(zs), 2),
        ),
        "self_intersect_pairs": cross,
        "thick_min": _pct(0),
        "thick_p5": _pct(5),
        "thick_p50": _pct(50),
        "outer_overhang_deg": round(overhang_deg, 1),
        "outer_faces_over_45": over_45,
        "foot_r_mm": (
            round(foot_r[0], 2) if foot_r else None,
            round(foot_r[-1], 2) if foot_r else None,
        ),
        "modifiers": [m.name for m in obj.modifiers],
    }
    bm_t.free()
    bm.free()
    ev.to_mesh_clear()
    return out


def _snapshot():
    obj = bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        return {}
    mod = next(
        (m for m in obj.modifiers if m.type == "NODES" and m.node_group and m.node_group.name == GROUP_NAME),
        None,
    )
    if mod is None:
        return {}
    saved = {}
    for item in mod.node_group.interface.items_tree:
        if getattr(item, "in_out", "") != "INPUT":
            continue
        try:
            saved[item.name] = mod.properties.inputs[item.identifier]["value"]
        except Exception:
            pass
    return saved


def _restore(obj, saved):
    mod = obj.modifiers.get("HarmonicCore")
    if mod is None:
        return []
    applied = []
    for item in mod.node_group.interface.items_tree:
        if item.name not in saved:
            continue
        try:
            mod.properties.inputs[item.identifier]["value"] = saved[item.name]
            applied.append(item.name)
        except Exception:
            pass
    return applied


def _crest(obj, z0):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    me = ev.to_mesh()
    rs = [math.hypot(v.co.x, v.co.y) for v in me.vertices if z0 <= v.co.z < z0 + 1.0]
    ev.to_mesh_clear()
    return round(max(rs), 3) if rs else None


def main():
    import traceback
    try:
        saved = _snapshot()
        ng = create_group()
        fill_group(ng)
        obj = setup_object(ng)
        restored = _restore(obj, saved)
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == "VIEW_3D":
                    area.spaces.active.shading.type = "SOLID"
        obj.update_tag(refresh={"OBJECT", "DATA"})
        bpy.context.view_layer.update()
        check = blender_check(obj)
        if check["volume_mm3"] < 0:
            shade = next(n for n in ng.nodes if n.bl_idname == "GeometryNodeSetShadeSmooth")
            link = shade.inputs["Mesh"].links[0]
            src = link.from_socket
            ng.links.remove(link)
            flip = ng.nodes.new("GeometryNodeFlipFaces")
            flip.location = (shade.location.x - 180, shade.location.y)
            ng.links.new(src, flip.inputs["Mesh"])
            ng.links.new(flip.outputs["Mesh"], shade.inputs["Mesh"])
            obj.update_tag(refresh={"OBJECT", "DATA"})
            bpy.context.view_layer.update()
            check = blender_check(obj)
            check["flipped"] = True
        path = os.path.join(ROOT, "harmonic_core.blend")
        bpy.ops.wm.save_as_mainfile(filepath=path)
        stl_path = os.path.join(ROOT, "harmonic_core.stl")
        stl_bytes = None
        printable = (
            check["islands"] == 1
            and check["nonmanifold_edges"] == 0
            and check["boundary_edges"] == 0
            and check["volume_mm3"] > 0
            and check["self_intersect_pairs"] == 0
            and check["outer_faces_over_45"] == 0
            and (check.get("thick_min") or 0) >= 1.5
        )
        if printable:
            for selected in list(bpy.context.selected_objects):
                selected.select_set(False)
            obj.select_set(True)
            bpy.ops.wm.stl_export(filepath=stl_path, export_selected_objects=True, ascii_format=False)
            stl_bytes = os.path.getsize(stl_path)
        scene = bpy.context.scene
        motion = {}
        for frame in (1, 31, 94):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            motion[str(frame)] = _crest(obj, 14.0)
        scene.frame_set(1)
        return {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "restored": restored,
            "motion_r_at_z14": motion,
            "check": check,
            "blend": path,
            "stl": stl_path if stl_bytes else None,
            "stl_bytes": stl_bytes,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


RESULT = main()
