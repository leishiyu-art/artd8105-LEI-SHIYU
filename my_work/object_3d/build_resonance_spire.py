"""Closed circular spire: wide foot, waist, core, solid point.

Flutes are a 7-fold cosine. Micro terraces sit on the outside only, and only
where the profile is narrowing. The tip has no hole. The inner wall follows
the same taper, so the point stays printable.

Does not delete the earlier objects.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "ResonanceSpireGN"
OBJ_NAME = "ResonanceSpire"
HIDE_OBJECTS = (
    "TraceShell",
    "NoiseDisplacedSolid",
    "SphereTubeNet",
    "SchumannResonator",
    "TopographicResonator",
    "HarmonicCore",
    "PlanetaryMonolith",
)

WALL_MM = 3.8
# 112 divides 7 and 8. 320 outer intervals is 0.25 mm on an 80 mm body.
VERTS = 112
NW = 320
NI = 240
WAIST_A = 0.06
WAIST_B = 0.42
CORE_T = 0.55
# 1.40 * R / n keeps a 3.8 mm radial wall near 2 mm true thickness.
FLUTE_COEF = 1.40

INNER_END = NW + NI
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
    _iface(ng, "Base Radius", "NodeSocketFloat", 36.0, 28.0, 44.0, "底部半径，mm", "DISTANCE")
    _iface(ng, "Waist Radius", "NodeSocketFloat", 20.0, 14.0, 28.0, "腰部半径，mm", "DISTANCE")
    _iface(ng, "Core Radius", "NodeSocketFloat", 26.0, 16.0, 32.0, "中段鼓起的半径，mm。再大的话尖顶会悬空", "DISTANCE")
    _iface(ng, "Height", "NodeSocketFloat", 80.0, 70.0, 90.0, "总高，mm", "DISTANCE")
    _iface(ng, "Flute Count", "NodeSocketInt", 7, 7, 8, "一圈竖向凹槽。7 或 8")
    _iface(ng, "Flute Depth", "NodeSocketFloat", 4.5, 0.0, 5.0, "凹槽目标深度，mm。腰和尖端会按壁厚变浅", "DISTANCE")
    _iface(ng, "Step Height", "NodeSocketFloat", 0.5, 0.4, 1.2, "外层等高线的层高，mm", "DISTANCE")
    _iface(
        ng, "Wall Thickness", "NodeSocketFloat", WALL_MM, 2.4, 4.5,
        "沿半径的壁厚，mm",
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


def _switch(g, cond, when_false, when_true, loc):
    node = g.node("GeometryNodeSwitch", loc, input_type="FLOAT")
    g._in(node, "Switch", cond)
    g._in(node, "False", when_false)
    g._in(node, "True", when_true)
    return node.outputs["Output"]


def _smooth(g, edge0, edge1, x, loc):
    span = g.math("SUBTRACT", x, edge0, loc=(loc[0], loc[1]))
    span = g.math("DIVIDE", span, edge1 - edge0, loc=(loc[0] + 160, loc[1]))
    u = g.math("MAXIMUM", 0.0, span, loc=(loc[0] + 320, loc[1]))
    u = g.math("MINIMUM", 1.0, u, loc=(loc[0] + 480, loc[1]))
    u2 = g.math("MULTIPLY", u, u, loc=(loc[0] + 640, loc[1]))
    two_u = g.math("MULTIPLY", u, 2.0, loc=(loc[0] + 640, loc[1] - 60))
    three = g.math("SUBTRACT", 3.0, two_u, loc=(loc[0] + 800, loc[1] - 60))
    return g.math("MULTIPLY", u2, three, loc=(loc[0] + 960, loc[1]))


def _profile(g, z, gi, loc):
    t = g.math("DIVIDE", z, gi.outputs["Height"], loc=loc)
    s_w = _smooth(g, WAIST_A, WAIST_B, t, (loc[0] + 160, loc[1] + 40))
    s_c = _smooth(g, WAIST_B, CORE_T, t, (loc[0] + 160, loc[1] - 80))
    d_w = g.math("SUBTRACT", gi.outputs["Waist Radius"], gi.outputs["Base Radius"], loc=(loc[0] + 1200, loc[1] + 80))
    d_c = g.math("SUBTRACT", gi.outputs["Core Radius"], gi.outputs["Waist Radius"], loc=(loc[0] + 1200, loc[1] - 40))
    body = g.math("MULTIPLY_ADD", s_w, d_w, gi.outputs["Base Radius"], loc=(loc[0] + 1400, loc[1] + 40))
    body = g.math("MULTIPLY_ADD", s_c, d_c, body, loc=(loc[0] + 1580, loc[1]))
    u = g.math("DIVIDE", g.math("SUBTRACT", t, CORE_T, loc=(loc[0] + 1200, loc[1] - 160)), 1.0 - CORE_T, loc=(loc[0] + 1400, loc[1] - 160))
    u = g.math("MAXIMUM", 0.0, u, loc=(loc[0] + 1560, loc[1] - 160))
    u = g.math("MINIMUM", 1.0, u, loc=(loc[0] + 1720, loc[1] - 160))
    spire = g.math("MULTIPLY", gi.outputs["Core Radius"], g.math("SUBTRACT", 1.0, u, loc=(loc[0] + 1720, loc[1] - 240)), loc=(loc[0] + 1900, loc[1] - 200))
    past = _compare(g, "GREATER_THAN", t, CORE_T, (loc[0] + 1720, loc[1] - 320))
    radius = _switch(g, past, body, spire, (loc[0] + 1960, loc[1] - 80))
    return g.math("MAXIMUM", radius, 0.0, loc=(loc[0] + 2140, loc[1] - 80))


def _flute(g, radius, z, theta, gi, loc):
    n = gi.outputs["Flute Count"]
    cap = g.math("MULTIPLY", g.math("DIVIDE", FLUTE_COEF, n, loc=loc), radius, loc=(loc[0] + 180, loc[1]))
    depth = g.math("MINIMUM", gi.outputs["Flute Depth"], cap, loc=(loc[0] + 360, loc[1]))
    # Rise only while the foot is already narrowing, or the crests flare past 45 degrees.
    foot = _smooth(g, 1.0, 11.0, z, (loc[0], loc[1] - 80))
    amp = g.math("MULTIPLY", depth, foot, loc=(loc[0] + 540, loc[1]))
    ang = g.math("MULTIPLY", n, theta, loc=(loc[0] + 360, loc[1] - 80))
    wave = g.math("COSINE", ang, loc=(loc[0] + 540, loc[1] - 80))
    return g.math("MULTIPLY", amp, wave, loc=(loc[0] + 860, loc[1]))


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-2200, 0)
    go.location = (2400, 240)

    cyl = g.node("GeometryNodeMeshCylinder", (-1900, 280), fill_type="NONE")
    cyl.inputs["Vertices"].default_value = VERTS
    cyl.inputs["Side Segments"].default_value = RING_COUNT - 1
    cyl.inputs["Radius"].default_value = 1.0
    cyl.inputs["Depth"].default_value = float(RING_COUNT - 1)

    pos = g.node("GeometryNodeInputPosition", (-1900, -40))
    sep = g.node("ShaderNodeSeparateXYZ", (-1700, -40))
    g.links.new(pos.outputs["Position"], sep.inputs["Vector"])
    offset = (RING_COUNT - 1) / 2.0
    ring = g.math("ROUND", g.math("ADD", sep.outputs["Z"], offset, loc=(-1500, -40)), loc=(-1320, -40))
    theta = g.math("ARCTAN2", sep.outputs["Y"], sep.outputs["X"], loc=(-1320, 100))

    is_inner = _compare(g, "GREATER_THAN", ring, float(NW), (-1100, 200))
    is_weld = _compare(g, "GREATER_THAN", ring, float(INNER_END), (-1100, 40))

    z_outer = g.math("DIVIDE", g.math("MULTIPLY", gi.outputs["Height"], ring, loc=(-900, 520)), float(NW), loc=(-700, 520))
    r_here = _profile(g, z_outer, gi, (-900, 760))
    z_div = g.math("ADD", g.math("DIVIDE", z_outer, gi.outputs["Step Height"], loc=(-700, 360)), 0.001, loc=(-520, 360))
    z_snap = g.math("MULTIPLY", g.math("FLOOR", z_div, loc=(-340, 360)), gi.outputs["Step Height"], loc=(-160, 360))
    r_band = _profile(g, z_snap, gi, (-340, 980))
    narrowing = _compare(g, "LESS_THAN", r_here, r_band, (200, 420))
    r_terr = _switch(g, narrowing, r_here, r_band, (420, 480))
    disp = _flute(g, r_terr, z_outer, theta, gi, (420, 680))
    r_outer = g.math("MAXIMUM", g.math("ADD", r_terr, disp, loc=(620, 560)), 0.0, loc=(800, 560))

    remain = g.math("MULTIPLY", gi.outputs["Height"], 1.0 - CORE_T, loc=(-700, -80))
    z_close = g.math(
        "SUBTRACT",
        gi.outputs["Height"],
        g.math("DIVIDE", g.math("MULTIPLY", gi.outputs["Wall Thickness"], remain, loc=(-500, -160)), gi.outputs["Core Radius"], loc=(-280, -160)),
        loc=(-60, -160),
    )
    j = g.math("SUBTRACT", ring, float(NW), loc=(-700, -280))
    z_inner = g.math(
        "MULTIPLY",
        z_close,
        g.math("SUBTRACT", 1.0, g.math("DIVIDE", j, float(NI), loc=(-500, -280)), loc=(-320, -280)),
        loc=(-100, -280),
    )
    r_in_prof = _profile(g, z_inner, gi, (-700, -480))
    r_in_base = g.math("MAXIMUM", g.math("SUBTRACT", r_in_prof, gi.outputs["Wall Thickness"], loc=(200, -420)), 0.0, loc=(400, -420))
    disp_in = _flute(g, r_in_base, z_inner, theta, gi, (200, -620))
    r_inner = g.math("MAXIMUM", g.math("ADD", r_in_base, disp_in, loc=(620, -480)), 0.0, loc=(800, -480))

    z = _switch(g, is_inner, z_outer, z_inner, (1100, 360))
    z = _switch(g, is_weld, z, 0.0, (1320, 300))
    radius = _switch(g, is_inner, r_outer, r_inner, (1100, 120))
    radius = _switch(g, is_weld, radius, gi.outputs["Base Radius"], (1320, 60))

    cos_th = g.math("COSINE", theta, loc=(1500, -40))
    sin_th = g.math("SINE", theta, loc=(1500, -160))
    x = g.math("MULTIPLY", radius, cos_th, loc=(1680, -40))
    y = g.math("MULTIPLY", radius, sin_th, loc=(1680, -160))
    comb = g.node("ShaderNodeCombineXYZ", (1880, 40))
    g.links.new(x, comb.inputs["X"])
    g.links.new(y, comb.inputs["Y"])
    g.links.new(z, comb.inputs["Z"])

    setpos = g.node("GeometryNodeSetPosition", (1880, 280))
    g.links.new(cyl.outputs["Mesh"], setpos.inputs["Geometry"])
    g.links.new(comb.outputs["Vector"], setpos.inputs["Position"])
    merge = g.node("GeometryNodeMergeByDistance", (2080, 280))
    g.links.new(setpos.outputs["Geometry"], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.02
    shade = g.node("GeometryNodeSetShadeSmooth", (2280, 280))
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
    mod = obj.modifiers.new("Spire", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.objects.active = obj
    for selected in list(bpy.context.selected_objects):
        selected.select_set(False)
    obj.select_set(True)
    _smooth_by_angle(obj)
    names = [m.name for m in obj.modifiers]
    if "Spire" in names:
        obj.modifiers.move(names.index("Spire"), 0)
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
        if c.z < zmin + 1.0 or c.z > zmax - 0.4:
            continue
        outward = f.normal.xy.dot(c.xy)
        if outward > 0.0 and c.xy.length >= 1.0:
            if f.normal.z < worst_nz:
                worst_nz = f.normal.z
            if f.normal.z < -0.7071:
                over_45 += 1
        elif outward < -0.05 and c.xy.length >= 1.0:
            ang = math.degrees(math.asin(min(1.0, max(0.0, -f.normal.z))))
            if ang > inner_worst:
                inner_worst = ang
            if f.normal.z < -0.7071:
                inner_over += 1
    overhang_deg = math.degrees(math.asin(min(1.0, max(0.0, -worst_nz))))
    foot = [v for v in bm.verts if v.co.z < zmin + 0.3]
    foot_r = sorted(math.hypot(v.co.x, v.co.y) for v in foot)
    top = [v for v in bm.verts if v.co.z > zmax - 0.4]
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
        cz = f.calc_center_median().z
        if f.calc_area() < 0.02 or abs(f.normal.z) > 0.55 or cz > zmax - 8.0:
            continue
        origin = f.calc_center_median() - f.normal * 0.15
        loc, nrm, _idx, dist = tree.ray_cast(origin, -f.normal, 12.0)
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
        path = os.path.join(ROOT, "resonance_spire.blend")
        bpy.ops.wm.save_as_mainfile(filepath=path)
        stl_path = os.path.join(ROOT, "resonance_spire.stl")
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
        return {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "check": check,
            "blend": path,
            "stl": stl_path if stl_bytes else None,
            "stl_bytes": stl_bytes,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


RESULT = main()
