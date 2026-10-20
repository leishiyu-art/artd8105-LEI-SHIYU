"""Topographic resonator: terraced Schumann ribs on a support-free FDM shell.

The radius is constant on each height step (floor of z), then steps inward.
Does not delete TraceShell, NoiseDisplacedSolid, or SphereTubeNet.
Does not write triangles_trace_shell.* or noise_displaced_solid.* or organic_fdm.stl.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "TopographicResonatorGN"
OBJ_NAME = "TopographicResonator"
PREVIOUS_OBJ = "SchumannResonator"
KEEP_OBJECTS = ("TraceShell", "NoiseDisplacedSolid", "SphereTubeNet")

# Print limits, not a look. Wall 2 mm. Lip stays 2 mm clear of the axis
# so the inward wall does not cross itself. Top cap diameter is 8 mm.
WALL_MM = 2.0
LIP_MM = WALL_MM + 2.0
# 168 divides both 7 and 8, so either rib count she named lands on vertices.
# Third harmonic is 3n, so 8 verts per finest crest at n=7 (21 crests).
VERTS = 168
# 400 steps over the outer wall: 80 mm / 400 = 0.2 mm, one FDM layer.
# A 0.6 mm terrace then holds the same radius for three layers.
SIDE_SEGMENTS = 400
# Solidify along normals pinches the concave side of the ribs.
# The shell is two copies of the same radial function, 2 mm apart.
# A radial graph does not pass through itself.
# 1 + 1/2 + 1/3. Peak of the three cosines is normalised to 1.
HARM_NORM = 1.0 + 0.5 + (1.0 / 3.0)


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
    _iface(
        ng, "Step Height", "NodeSocketFloat", 0.6, 0.4, 0.8,
        "每一级等高线的高度，mm。0.4、0.6、0.8 都是 0.2 mm 层高的整数倍。越小越密",
        "DISTANCE",
    )
    _iface(
        ng,         "Tectonic Amplitude", "NodeSocketFloat", 1.6, 0.0, 3.0,
        "每一层波瓣的径向起伏，mm。超过 1.6 时，波瓣的陡面会薄于 1.2 mm",
        "DISTANCE",
    )
    _iface(
        ng, "Helix Twist", "NodeSocketFloat", math.radians(36.0),
        math.radians(-120.0), math.radians(120.0),
        "从底到顶，褶皱转过的角度。太大时上一阶会伸到下一阶的外面",
        "ANGLE",
    )
    _iface(
        ng, "Base Radius", "NodeSocketFloat", 30.0, 16.0, 40.0,
        "底圈半径，mm", "DISTANCE",
    )
    _iface(
        ng, "Harmonic Frequency", "NodeSocketInt", 7, 3, 12,
        "一圈主波瓣的个数。整数倍才能在一圈里闭上",
    )
    _iface(
        ng, "Core Offset", "NodeSocketFloat", 0.8, 0.0, 2.0,
        "单一波瓣，mm。用来打破 7 次对称，底和顶收成 0",
        "DISTANCE",
    )
    _iface(
        ng, "Height", "NodeSocketFloat", 80.0, 40.0, 120.0,
        "高度，mm", "DISTANCE",
    )
    _iface(
        ng, "Wall Thickness", "NodeSocketFloat", WALL_MM, 1.5, 2.5,
        "沿半径的壁厚，mm", "DISTANCE",
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


def _smoothstep(g, edge0, edge1, x, loc):
    span = g.math("SUBTRACT", x, edge0, loc=(loc[0] - 180, loc[1]))
    span = g.math("DIVIDE", span, edge1 - edge0, loc=(loc[0] - 40, loc[1]))
    u = g.math("MAXIMUM", 0.0, span, loc=loc)
    u = g.math("MINIMUM", 1.0, u, loc=(loc[0] + 160, loc[1]))
    u2 = g.math("MULTIPLY", u, u, loc=(loc[0] + 320, loc[1]))
    two_u = g.math("MULTIPLY", u, 2.0, loc=(loc[0] + 320, loc[1] - 80))
    three = g.math("SUBTRACT", 3.0, two_u, loc=(loc[0] + 480, loc[1] - 80))
    return g.math("MULTIPLY", u2, three, loc=(loc[0] + 640, loc[1]))


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-2400, 0)
    go.location = (2000, 200)

    # A cylinder is already wrapped, so there is no seam to weld.
    # Rings: 0..nv outer, nv+1..2*nv+1 inner, last ring repeats the outer foot.
    nu = VERTS
    nv = SIDE_SEGMENTS
    rings = 2 * nv + 3  # 163
    cyl = g.node("GeometryNodeMeshCylinder", (-2100, 280), fill_type="NONE")
    cyl.inputs["Vertices"].default_value = nu
    cyl.inputs["Side Segments"].default_value = rings - 1
    cyl.inputs["Radius"].default_value = 1.0
    cyl.inputs["Depth"].default_value = float(rings - 1)

    pos = g.node("GeometryNodeInputPosition", (-2100, -40))
    sep = g.node("ShaderNodeSeparateXYZ", (-1880, -40))
    g.links.new(pos.outputs["Position"], sep.inputs["Vector"])
    # Depth 162, centred, so z runs -81..81 in steps of 1.
    ring = g.math("ROUND", g.math("ADD", sep.outputs["Z"], float(nv + 1), loc=(-1680, -40)), loc=(-1480, -40))
    theta = g.math("ARCTAN2", sep.outputs["Y"], sep.outputs["X"], loc=(-1480, 80))

    is_weld = _compare(g, "GREATER_EQUAL", ring, float(2 * nv + 2) - 0.5, (-1680, -180))
    is_past = _compare(g, "GREATER_THAN", ring, float(nv), (-1680, -300))
    not_weld = _bool(g, "NOT", is_weld, loc=(-1480, -180))
    is_inner = _bool(g, "AND", is_past, not_weld, loc=(-1280, -240))

    t_outer = g.math("DIVIDE", ring, float(nv), loc=(-1480, -420))
    inner_k = g.math("SUBTRACT", ring, float(nv + 1), loc=(-1480, -540))
    t_inner = g.math(
        "SUBTRACT",
        1.0,
        g.math("DIVIDE", inner_k, float(nv), loc=(-1280, -540)),
        loc=(-1080, -540),
    )
    t_body = _switch(g, is_inner, t_outer, t_inner, (-880, -420))
    t = _switch(g, is_weld, t_body, 0.0, (-680, -360))

    # Terrace: radius follows floor(z / step) so each band is a vertical riser.
    # The real z of the vertices is left alone, so the band has thickness.
    # Mask fades the stair off at the foot and at the nose.
    z_mm = g.math("MULTIPLY", gi.outputs["Height"], t, loc=(-480, -360))
    z_div = g.math("DIVIDE", z_mm, gi.outputs["Step Height"], loc=(-280, -360))
    # A hair above an exact multiple, so floor does not fall back one step.
    z_div = g.math("ADD", z_div, 0.001, loc=(-140, -360))
    z_snap = g.math(
        "MULTIPLY",
        g.math("FLOOR", z_div, loc=(-80, -360)),
        gi.outputs["Step Height"],
        loc=(120, -360),
    )
    t_snap = g.math("DIVIDE", z_snap, gi.outputs["Height"], loc=(320, -360))
    rise = _smoothstep(g, 0.0, 0.05, t, (-200, -560))
    nose = _smoothstep(g, 0.86, 1.0, t, (-200, -720))
    stay = g.math("SUBTRACT", 1.0, nose, loc=(280, -720))
    mask = g.math("MULTIPLY", rise, stay, loc=(480, -640))
    # t_eval = t + (t_snap - t) * mask
    t_delta = g.math("SUBTRACT", t_snap, t, loc=(480, -480))
    t_eval = g.math("MULTIPLY_ADD", t_delta, mask, t, loc=(700, -420))
    pi_t = g.math("MULTIPLY", t_eval, math.pi, loc=(-480, 80))

    # R(z) = Lip + (BaseRadius - Lip) * (1 + cos(pi z / H)) / 2
    # Slope is 0 at the base and at the lip, max about 22 deg at mid height.
    cos_pit = g.math("COSINE", pi_t, loc=(-520, 200))
    half_cos = g.math("MULTIPLY_ADD", cos_pit, 0.5, 0.5, loc=(-320, 200))
    r_delta = g.math("SUBTRACT", gi.outputs["Base Radius"], LIP_MM, loc=(-520, 40))
    r_prof = g.math("MULTIPLY_ADD", half_cos, r_delta, LIP_MM, loc=(-120, 160))

    # Envelope is 0 at both ends, so the base is a flat circle and the lip is round.
    sin_pit = g.math("SINE", pi_t, loc=(-520, -80))
    env = g.math("MULTIPLY", sin_pit, sin_pit, loc=(-320, -80))

    # phi uses the terraced height, so a whole step shares one cross-section.
    twist_t = g.math("MULTIPLY", gi.outputs["Helix Twist"], t_eval, loc=(-480, -200))
    phi = g.math("ADD", theta, twist_t, loc=(-520, -200))

    n = gi.outputs["Harmonic Frequency"]
    n2 = g.math("MULTIPLY", n, 2.0, loc=(-900, -340))
    n3 = g.math("MULTIPLY", n, 3.0, loc=(-900, -480))
    nphi = g.math("MULTIPLY", n, phi, loc=(-300, -280))
    n2phi = g.math("MULTIPLY", n2, phi, loc=(-300, -400))
    n3phi = g.math("MULTIPLY", n3, phi, loc=(-300, -520))
    h1 = g.math("COSINE", nphi, loc=(-80, -280))
    h2 = g.math("COSINE", n2phi, loc=(-80, -400))
    h3 = g.math("COSINE", n3phi, loc=(-80, -520))
    # Integer harmonics 1n, 2n, 3n. Weights 1, 1/2, 1/3, then normalised to peak 1.
    h2w = g.math("MULTIPLY", h2, 0.5, loc=(120, -400))
    h3w = g.math("MULTIPLY", h3, 1.0 / 3.0, loc=(120, -520))
    sum12 = g.math("ADD", h1, h2w, loc=(320, -360))
    raw = g.math("ADD", sum12, h3w, loc=(520, -420))
    wave = g.math("DIVIDE", raw, HARM_NORM, loc=(720, -420))

    disp = g.math("MULTIPLY", gi.outputs["Tectonic Amplitude"], env, loc=(520, -80))
    disp = g.math("MULTIPLY", disp, wave, loc=(720, -80))
    # One-lobe offset. It is not a multiple of n, so the section is not n-fold.
    core = g.math("MULTIPLY", gi.outputs["Core Offset"], env, loc=(520, -200))
    core = g.math("MULTIPLY", core, g.math("COSINE", theta, loc=(520, -320)), loc=(720, -240))
    r_raw = g.math("ADD", r_prof, disp, loc=(920, 40))
    r_raw = g.math("ADD", r_raw, core, loc=(1040, 40))
    # Grooves may not pass the lip radius, or the 2 mm wall crosses the axis.
    r_outer = g.math("MAXIMUM", r_raw, LIP_MM, loc=(1100, 40))
    r_gap = g.math("SUBTRACT", r_outer, gi.outputs["Wall Thickness"], loc=(1280, -40))
    r_inner = g.math("MAXIMUM", r_gap, 1.0, loc=(1460, -40))
    radius = _switch(g, is_inner, r_outer, r_inner, (1640, 40))

    cos_th = g.math("COSINE", theta, loc=(1280, -200))
    sin_th = g.math("SINE", theta, loc=(1280, -320))
    x = g.math("MULTIPLY", radius, cos_th, loc=(1500, -200))
    y = g.math("MULTIPLY", radius, sin_th, loc=(1500, -320))
    # Vertex height stays on the true parameter. Only the radius is terraced.
    z0 = g.math("MULTIPLY", gi.outputs["Height"], t, loc=(1500, -440))

    comb = g.node("ShaderNodeCombineXYZ", (1720, -80))
    g.links.new(x, comb.inputs["X"])
    g.links.new(y, comb.inputs["Y"])
    g.links.new(z0, comb.inputs["Z"])

    setpos = g.node("GeometryNodeSetPosition", (1720, 280))
    g.links.new(cyl.outputs["Mesh"], setpos.inputs["Geometry"])
    g.links.new(comb.outputs["Vector"], setpos.inputs["Position"])

    merge = g.node("GeometryNodeMergeByDistance", (1940, 280))
    g.links.new(setpos.outputs["Geometry"], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.001

    shade = g.node("GeometryNodeSetShadeSmooth", (2160, 280))
    shade.inputs["Shade Smooth"].default_value = True
    g.links.new(merge.outputs["Geometry"], shade.inputs["Mesh"])
    g.links.new(shade.outputs["Mesh"], go.inputs["Geometry"])


def setup_object(ng):
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"

    obj = bpy.data.objects.get(OBJ_NAME)
    if obj is None:
        previous = bpy.data.objects.get(PREVIOUS_OBJ)
        if previous is not None:
            previous.name = OBJ_NAME
            previous.data.name = OBJ_NAME
            obj = previous
    if obj is None:
        mesh = bpy.data.meshes.new(OBJ_NAME)
        obj = bpy.data.objects.new(OBJ_NAME, mesh)
        bpy.context.collection.objects.link(obj)
    obj.hide_set(False)
    obj.hide_viewport = False
    obj.location = (0.0, 0.0, 0.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    for other in KEEP_OBJECTS:
        other_obj = bpy.data.objects.get(other)
        if other_obj is not None:
            other_obj.hide_viewport = True
    for mod in list(obj.modifiers):
        obj.modifiers.remove(mod)
    mod = obj.modifiers.new("Topographic", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.objects.active = obj
    for selected in list(bpy.context.selected_objects):
        selected.select_set(False)
    obj.select_set(True)
    _smooth_by_angle(obj)
    names = [m.name for m in obj.modifiers]
    if "Topographic" in names:
        obj.modifiers.move(names.index("Topographic"), 0)
    return obj


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
        return
    except Exception:
        pass
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=0.523599)
    except Exception:
        pass


def _show_nodes(ng):
    shown = False
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "VIEW_3D":
                continue
            if area.type not in {"NODE_EDITOR", "DOPESHEET", "TIMELINE", "GRAPH_EDITOR", "INFO"}:
                continue
            area.type = "NODE_EDITOR"
            space = area.spaces.active
            try:
                space.tree_type = "GeometryNodeTree"
                space.node_tree = ng
                shown = True
            except Exception:
                pass
            if shown:
                return True
    return False


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
    # Outer underside, skipping the foot on the bed. Angle from vertical:
    # 0 = vertical wall, 90 = horizontal ceiling. Past 45 the slicer wants support.
    worst_nz = 0.0
    over_45 = 0
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z < zmin + 0.6:
            continue
        radial = c.xy
        if radial.length < 1.0:
            continue
        if f.normal.xy.dot(radial) <= 0.0:
            continue
        if f.normal.z < worst_nz:
            worst_nz = f.normal.z
        if f.normal.z < -0.7071:
            over_45 += 1
    overhang_deg = math.degrees(math.asin(min(1.0, max(0.0, -worst_nz))))
    foot = [v for v in bm.verts if v.co.z < zmin + 0.3]
    foot_r = sorted(math.hypot(v.co.x, v.co.y) for v in foot)
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
        ca = fa.calc_center_median()
        cb = fb.calc_center_median()
        if (ca - cb).length > 1.2:
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
        if f.calc_area() < 0.02:
            continue
        if abs(f.normal.z) > 0.5:
            continue
        origin = f.calc_center_median() - f.normal * 0.15
        loc, nrm, _idx, dist = tree.ray_cast(origin, -f.normal, 6.0)
        if loc is None or nrm is None:
            continue
        if nrm.dot(f.normal) > -0.5:
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
    smooth_faces = sum(1 for f in bm.faces if f.smooth)
    out = {
        "verts": len(bm.verts),
        "faces": len(bm.faces),
        "smooth_faces": smooth_faces,
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


def main():
    import traceback
    try:
        ng = create_group()
        fill_group(ng)
        obj = setup_object(ng)
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != "VIEW_3D":
                    continue
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
        nodes_open = _show_nodes(ng)
        path = os.path.join(ROOT, "topographic_resonator.blend")
        bpy.ops.wm.save_as_mainfile(filepath=path)
        stl_path = os.path.join(ROOT, "topographic_resonator.stl")
        stl_bytes = None
        printable = (
            check["islands"] == 1
            and check["nonmanifold_edges"] == 0
            and check["boundary_edges"] == 0
            and check["volume_mm3"] > 0
            and check["self_intersect_pairs"] == 0
            and (check.get("thick_min") or 0) >= 1.2
        )
        if printable:
            bpy.ops.wm.stl_export(
                filepath=stl_path,
                export_selected_objects=True,
                ascii_format=False,
            )
            stl_bytes = os.path.getsize(stl_path)
        return {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "group": ng.name,
            "nodes_editor": nodes_open,
            "kept": [n for n in KEEP_OBJECTS if bpy.data.objects.get(n)],
            "check": check,
            "blend": path,
            "stl": stl_path if stl_bytes else None,
            "stl_bytes": stl_bytes,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


RESULT = main()
