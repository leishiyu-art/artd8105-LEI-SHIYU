"""Planetary monolith: tri-lobed plan, inward terraces, closed flat top.

The cavity opens on the bed and closes inside with a cone. A flat lid across
the cavity would be a bridge. The cone angle is solved so the inner ceiling
stays near 37 degrees from vertical.

Does not delete TraceShell, NoiseDisplacedSolid, SphereTubeNet,
SchumannResonator, TopographicResonator, or HarmonicCore.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "PlanetaryMonolithGN"
OBJ_NAME = "PlanetaryMonolith"
HIDE_OBJECTS = (
    "TraceShell",
    "NoiseDisplacedSolid",
    "SphereTubeNet",
    "SchumannResonator",
    "TopographicResonator",
    "HarmonicCore",
)

WALL_MM = 2.5
# 180 divides the three lobes. 160 wall intervals is 0.5 mm on an 80 mm body.
VERTS = 180
NW = 160
NC = 16
NCONE = 40
# Inner ceiling slope: horizontal run / vertical rise. 0.75 is about 37 degrees.
CONE_SLOPE = 0.75

P_CENTER = NW + NC
CONE_END = P_CENTER + NCONE
INNER_END = CONE_END + NW
WELD_END = INNER_END + 2
RING_COUNT = WELD_END + 1


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
    _iface(ng, "Base Radius", "NodeSocketFloat", 32.0, 24.0, 48.0, "底部平均半径，mm。三叶还会再向外鼓", "DISTANCE")
    _iface(ng, "Top Radius", "NodeSocketFloat", 16.0, 12.0, 36.0, "顶部平均半径，mm。平顶，不是开口", "DISTANCE")
    _iface(ng, "Lobe", "NodeSocketFloat", 0.22, 0.08, 0.40, "三叶的深浅。0 是圆")
    _iface(ng, "Step Height", "NodeSocketFloat", 2.0, 0.8, 6.0, "每一层岩层的高度，mm。用 0.2 的倍数", "DISTANCE")
    _iface(ng, "Height", "NodeSocketFloat", 80.0, 70.0, 90.0, "总高，mm", "DISTANCE")
    _iface(
        ng, "Wall Thickness", "NodeSocketFloat", WALL_MM, 1.8, 3.5,
        "沿半径的壁厚，mm。平顶下面的锥形空腔按这个厚度收口",
        "DISTANCE",
    )
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


def _between(g, ring, lo, hi, loc):
    gt = _compare(g, "GREATER_THAN", ring, float(lo), loc)
    le = _compare(g, "LESS_EQUAL", ring, float(hi), (loc[0] + 180, loc[1] - 40))
    return _bool(g, "AND", gt, le, (loc[0] + 360, loc[1]))


def _profile_smooth(g, z, gi, loc):
    """Untouched taper. The cavity uses this so inner steps do not hang downward."""
    t = g.math("DIVIDE", z, gi.outputs["Height"], loc=loc)
    delta = g.math("SUBTRACT", gi.outputs["Top Radius"], gi.outputs["Base Radius"], loc=(loc[0], loc[1] - 70))
    return g.math("MULTIPLY_ADD", delta, t, gi.outputs["Base Radius"], loc=(loc[0] + 200, loc[1]))


def _profile(g, z, gi, loc):
    """Terrace the height, then linearly taper from base to top."""
    z_div = g.math("DIVIDE", z, gi.outputs["Step Height"], loc=(loc[0], loc[1]))
    z_div = g.math("ADD", z_div, 0.001, loc=(loc[0] + 160, loc[1]))
    steps = g.math("FLOOR", z_div, loc=(loc[0] + 320, loc[1]))
    z_snap = g.math("MULTIPLY", steps, gi.outputs["Step Height"], loc=(loc[0] + 480, loc[1]))
    z_snap = g.math("MINIMUM", z_snap, gi.outputs["Height"], loc=(loc[0] + 660, loc[1]))
    t = g.math("DIVIDE", z_snap, gi.outputs["Height"], loc=(loc[0] + 840, loc[1]))
    delta = g.math("SUBTRACT", gi.outputs["Top Radius"], gi.outputs["Base Radius"], loc=(loc[0] + 840, loc[1] - 80))
    return g.math("MULTIPLY_ADD", delta, t, gi.outputs["Base Radius"], loc=(loc[0] + 1040, loc[1]))


def _lobed(g, radius, theta, gi, loc):
    three = g.math("MULTIPLY", theta, 3.0, loc=loc)
    wave = g.math("COSINE", three, loc=(loc[0] + 160, loc[1]))
    amp = g.math("MULTIPLY", gi.outputs["Lobe"], wave, loc=(loc[0] + 320, loc[1]))
    scale = g.math("ADD", 1.0, amp, loc=(loc[0] + 480, loc[1]))
    r = g.math("MULTIPLY", radius, scale, loc=(loc[0] + 640, loc[1]))
    return g.math("MAXIMUM", r, 1.0, loc=(loc[0] + 800, loc[1]))


def _cone_height(g, gi, loc):
    """C such that the widest inner radius closes at CONE_SLOPE."""
    k = g.math(
        "DIVIDE",
        g.math("SUBTRACT", gi.outputs["Top Radius"], gi.outputs["Base Radius"], loc=loc),
        gi.outputs["Height"],
        loc=(loc[0] + 180, loc[1]),
    )
    one_l = g.math("ADD", 1.0, gi.outputs["Lobe"], loc=(loc[0] + 180, loc[1] - 80))
    span = g.math("SUBTRACT", gi.outputs["Height"], gi.outputs["Wall Thickness"], loc=(loc[0] + 360, loc[1]))
    base_term = g.math("MULTIPLY_ADD", k, span, gi.outputs["Base Radius"], loc=(loc[0] + 540, loc[1]))
    grown = g.math("MULTIPLY", base_term, one_l, loc=(loc[0] + 720, loc[1]))
    num = g.math("SUBTRACT", grown, gi.outputs["Wall Thickness"], loc=(loc[0] + 900, loc[1]))
    den = g.math("MULTIPLY_ADD", k, one_l, CONE_SLOPE, loc=(loc[0] + 720, loc[1] - 120))
    cone = g.math("DIVIDE", num, den, loc=(loc[0] + 1080, loc[1]))
    cone = g.math("MAXIMUM", cone, 6.0, loc=(loc[0] + 1240, loc[1]))
    limit = g.math("SUBTRACT", span, 10.0, loc=(loc[0] + 1080, loc[1] - 80))
    return g.math("MINIMUM", cone, limit, loc=(loc[0] + 1400, loc[1]))


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-2400, 0)
    go.location = (2800, 200)

    cyl = g.node("GeometryNodeMeshCylinder", (-2100, 280), fill_type="NONE")
    cyl.inputs["Vertices"].default_value = VERTS
    cyl.inputs["Side Segments"].default_value = RING_COUNT - 1
    cyl.inputs["Radius"].default_value = 1.0
    cyl.inputs["Depth"].default_value = float(RING_COUNT - 1)

    pos = g.node("GeometryNodeInputPosition", (-2100, -40))
    sep = g.node("ShaderNodeSeparateXYZ", (-1900, -40))
    g.links.new(pos.outputs["Position"], sep.inputs["Vector"])
    offset = (RING_COUNT - 1) / 2.0
    ring = g.math("ROUND", g.math("ADD", sep.outputs["Z"], offset, loc=(-1700, -40)), loc=(-1520, -40))
    theta = g.math("ARCTAN2", sep.outputs["Y"], sep.outputs["X"], loc=(-1520, 80))

    is_cap = _between(g, ring, NW, P_CENTER, (-1200, 360))
    is_cone = _between(g, ring, P_CENTER, CONE_END, (-1200, 200))
    is_inner = _between(g, ring, CONE_END, INNER_END, (-1200, 40))
    is_weld = _compare(g, "GREATER_THAN", ring, float(INNER_END), (-1200, -120))

    cone_h = _cone_height(g, gi, (-1200, -280))
    join_z = g.math(
        "SUBTRACT",
        g.math("SUBTRACT", gi.outputs["Height"], gi.outputs["Wall Thickness"], loc=(-980, -280)),
        cone_h,
        loc=(-780, -280),
    )

    # Outer wall: terraces from the foot up to the flat top.
    z_outer = g.math("DIVIDE", g.math("MULTIPLY", gi.outputs["Height"], ring, loc=(-700, 520)), float(NW), loc=(-520, 520))
    r_outer = _lobed(g, _profile(g, z_outer, gi, (-700, 680)), theta, gi, (-200, 680))

    # Flat tri-lobed lid. The last ring of this run sits at the centre.
    s_cap = g.math("DIVIDE", g.math("SUBTRACT", ring, float(NW), loc=(-700, 300)), float(NC), loc=(-520, 300))
    r_top = _lobed(g, gi.outputs["Top Radius"], theta, gi, (-700, 160))
    r_cap = g.math("MULTIPLY", r_top, g.math("SUBTRACT", 1.0, s_cap, loc=(-300, 300)), loc=(-120, 300))

    # Underside cone: centre just under the lid, then out to the cavity wall.
    s_cone = g.math("DIVIDE", g.math("SUBTRACT", ring, float(P_CENTER), loc=(-700, 40)), float(NCONE), loc=(-520, 40))
    z_cone = g.math(
        "SUBTRACT",
        g.math("SUBTRACT", gi.outputs["Height"], gi.outputs["Wall Thickness"], loc=(-520, -40)),
        g.math("MULTIPLY", s_cone, cone_h, loc=(-300, 0)),
        loc=(-80, 0),
    )
    r_join = _lobed(g, _profile_smooth(g, join_z, gi, (-700, -160)), theta, gi, (-200, -160))
    r_hole = g.math("SUBTRACT", r_join, gi.outputs["Wall Thickness"], loc=(40, -160))
    r_hole = g.math("MAXIMUM", r_hole, 1.5, loc=(220, -160))
    r_cone = g.math("MULTIPLY", r_hole, s_cone, loc=(400, -40))

    # Inner wall, from the cone join down to the foot.
    j_inner = g.math("SUBTRACT", ring, float(CONE_END), loc=(-700, -360))
    t_down = g.math("DIVIDE", j_inner, float(NW), loc=(-520, -360))
    z_inner = g.math("MULTIPLY", join_z, g.math("SUBTRACT", 1.0, t_down, loc=(-340, -360)), loc=(-160, -360))
    r_inner_wall = _lobed(g, _profile_smooth(g, z_inner, gi, (-700, -520)), theta, gi, (-200, -520))
    r_inner_wall = g.math("SUBTRACT", r_inner_wall, gi.outputs["Wall Thickness"], loc=(40, -520))
    r_inner_wall = g.math("MAXIMUM", r_inner_wall, 1.5, loc=(220, -520))

    r_foot = _lobed(g, gi.outputs["Base Radius"], theta, gi, (-200, -700))

    z = z_outer
    z = _switch(g, is_cap, z, gi.outputs["Height"], (700, 420))
    z = _switch(g, is_cone, z, z_cone, (920, 360))
    z = _switch(g, is_inner, z, z_inner, (1140, 300))
    z = _switch(g, is_weld, z, 0.0, (1360, 240))

    radius = r_outer
    radius = _switch(g, is_cap, radius, r_cap, (700, 120))
    radius = _switch(g, is_cone, radius, r_cone, (920, 60))
    radius = _switch(g, is_inner, radius, r_inner_wall, (1140, 0))
    radius = _switch(g, is_weld, radius, r_foot, (1360, -60))

    cos_th = g.math("COSINE", theta, loc=(1500, -80))
    sin_th = g.math("SINE", theta, loc=(1500, -200))
    x = g.math("MULTIPLY", radius, cos_th, loc=(1680, -80))
    y = g.math("MULTIPLY", radius, sin_th, loc=(1680, -200))
    comb = g.node("ShaderNodeCombineXYZ", (1880, -40))
    g.links.new(x, comb.inputs["X"])
    g.links.new(y, comb.inputs["Y"])
    g.links.new(z, comb.inputs["Z"])

    setpos = g.node("GeometryNodeSetPosition", (1880, 260))
    g.links.new(cyl.outputs["Mesh"], setpos.inputs["Geometry"])
    g.links.new(comb.outputs["Vector"], setpos.inputs["Position"])
    merge = g.node("GeometryNodeMergeByDistance", (2080, 260))
    g.links.new(setpos.outputs["Geometry"], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.01
    shade = g.node("GeometryNodeSetShadeSmooth", (2280, 260))
    shade.inputs["Shade Smooth"].default_value = True
    g.links.new(merge.outputs["Geometry"], shade.inputs["Mesh"])
    g.links.new(shade.outputs["Mesh"], go.inputs["Geometry"])


def _smooth_by_angle(obj):
    if any(m.name == "Smooth by Angle" for m in obj.modifiers):
        return
    path = (
        "/Applications/Blender.app/Contents/Resources/5.2/"
        "datafiles/assets/nodes/geometry_nodes_essentials.blend"
    )
    try:
        if "Smooth by Angle" not in bpy.data.node_groups:
            with bpy.data.libraries.load(path, link=False) as (src, dst):
                dst.node_groups = ["Smooth by Angle"]
        mod = obj.modifiers.new("Smooth by Angle", "NODES")
        mod.node_group = bpy.data.node_groups["Smooth by Angle"]
        for item in mod.node_group.interface.items_tree:
            if getattr(item, "name", "") == "Angle":
                mod.properties.inputs[item.identifier]["value"] = 0.523599
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
    mod = obj.modifiers.new("Monolith", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.objects.active = obj
    for selected in list(bpy.context.selected_objects):
        selected.select_set(False)
    obj.select_set(True)
    _smooth_by_angle(obj)
    names = [m.name for m in obj.modifiers]
    if "Monolith" in names:
        obj.modifiers.move(names.index("Monolith"), 0)
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
    zmax = max(zs)
    worst_nz = 0.0
    over_45 = 0
    inner_worst = 0.0
    inner_over = 0
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z < zmin + 1.0:
            continue
        outward = f.normal.xy.dot(c.xy)
        if outward > 0.0 and c.xy.length >= 1.0:
            if f.normal.z < worst_nz:
                worst_nz = f.normal.z
            if f.normal.z < -0.7071:
                over_45 += 1
        elif outward < -0.05 and c.z > zmin + 4.0:
            ang = math.degrees(math.asin(min(1.0, max(0.0, -f.normal.z))))
            if ang > inner_worst:
                inner_worst = ang
            if f.normal.z < -0.7071:
                inner_over += 1
    overhang_deg = math.degrees(math.asin(min(1.0, max(0.0, -worst_nz))))
    foot = [v for v in bm.verts if v.co.z < zmin + 0.3]
    foot_r = sorted(math.hypot(v.co.x, v.co.y) for v in foot)
    top = [v for v in bm.verts if v.co.z > zmax - 0.3]
    top_r = sorted(math.hypot(v.co.x, v.co.y) for v in top)
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
        "max_z": round(zmax, 3),
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
        "inner_ceiling_deg": round(inner_worst, 1),
        "inner_faces_over_45": inner_over,
        "foot_r_mm": (
            round(foot_r[0], 2) if foot_r else None,
            round(foot_r[-1], 2) if foot_r else None,
        ),
        "top_r_mm": (
            round(top_r[0], 2) if top_r else None,
            round(top_r[-1], 2) if top_r else None,
        ),
        "modifiers": [m.name for m in obj.modifiers],
    }
    bm_t.free()
    bm.free()
    ev.to_mesh_clear()
    return out


def _cone_report(base, top, height, wall, lobe):
    k = (top - base) / height
    num = (base + k * (height - wall)) * (1.0 + lobe) - wall
    den = CONE_SLOPE + k * (1.0 + lobe)
    cone = num / den
    cone = max(6.0, min(cone, height - wall - 10.0))
    return round(cone, 2), round(height - wall - cone, 2)


def main():
    import traceback
    try:
        ng = create_group()
        fill_group(ng)
        obj = setup_object(ng)
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
        path = os.path.join(ROOT, "planetary_monolith.blend")
        bpy.ops.wm.save_as_mainfile(filepath=path)
        stl_path = os.path.join(ROOT, "planetary_monolith.stl")
        stl_bytes = None
        printable = (
            check["islands"] == 1
            and check["nonmanifold_edges"] == 0
            and check["boundary_edges"] == 0
            and check["volume_mm3"] > 0
            and check["self_intersect_pairs"] == 0
            and check["outer_faces_over_45"] == 0
            and check["inner_faces_over_45"] == 0
            and (check.get("thick_min") or 0) >= 1.5
        )
        if printable:
            for selected in list(bpy.context.selected_objects):
                selected.select_set(False)
            obj.select_set(True)
            bpy.ops.wm.stl_export(filepath=stl_path, export_selected_objects=True, ascii_format=False)
            stl_bytes = os.path.getsize(stl_path)
        cone, join = _cone_report(32.0, 16.0, 80.0, WALL_MM, 0.22)
        return {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "check": check,
            "cone_mm": cone,
            "join_z_mm": join,
            "blend": path,
            "stl": stl_path if stl_bytes else None,
            "stl_bytes": stl_bytes,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


RESULT = main()
