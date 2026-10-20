"""Build SphereTubeNet: icosphere edges → circular tubes. Run inside Blender.

Does not delete TraceShell or NoiseDisplacedSolid.
Does not write triangles_trace_shell.* or noise_displaced_solid.*.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "SphereTubeNetGN"
OBJ_NAME = "SphereTubeNet"
KEEP_OBJECTS = ("TraceShell", "NoiseDisplacedSolid")


class GN:
    def __init__(self, ng):
        self.ng = ng
        self.links = ng.links

    def node(self, idname, loc, **kw):
        node = self.ng.nodes.new(idname)
        node.location = loc
        node.width = min(180, getattr(node, "width", 140))
        for k, v in kw.items():
            if hasattr(node, k):
                setattr(node, k, v)
        return node

    def math(self, op, a, b=None, loc=(0, 0), c=None):
        node = self.node("ShaderNodeMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        if c is not None:
            self._in(node, 2, c)
        return node.outputs[0]

    def vmath(self, op, a, b=None, loc=(0, 0), scale=None):
        node = self.node("ShaderNodeVectorMath", loc, operation=op)
        self._in(node, 0, a)
        if b is not None:
            self._in(node, 1, b)
        if scale is not None:
            self._in(node, "Scale", scale)
        if op in {"DOT_PRODUCT", "LENGTH", "DISTANCE"}:
            return node.outputs["Value"]
        return node.outputs[0]

    def switch(self, dtype, cond, false, true, loc=(0, 0)):
        node = self.node("GeometryNodeSwitch", loc, input_type=dtype)
        self._in(node, "Switch", cond)
        self._in(node, "False", false)
        self._in(node, "True", true)
        return node.outputs[0]

    def _in(self, node, key, sock):
        if sock is None:
            return
        target = node.inputs[key]
        if hasattr(sock, "rna_type"):
            self.links.new(sock, target)
        else:
            target.default_value = sock


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


def create_group():
    if GROUP_NAME in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[GROUP_NAME])
    ng = bpy.data.node_groups.new(GROUP_NAME, "GeometryNodeTree")
    try:
        ng.is_modifier = True
    except Exception:
        pass
    _iface(ng, "Geometry", "OUTPUT", "NodeSocketGeometry")
    _iface(ng, "Radius", "INPUT", "NodeSocketFloat", 30.0, 10.0, 80.0)
    _iface(ng, "Subdivisions", "INPUT", "NodeSocketInt", 1, 1, 3, "C=1 twenty windows; D=2 eighty")
    _iface(ng, "CageScale", "INPUT", "NodeSocketFloat", 0.5, 0.05, 4.0)
    _iface(ng, "CageAmplitude", "INPUT", "NodeSocketFloat", 4.0, 0.0, 8.0, "human base mm; signal may rewrite")
    _iface(ng, "Seed", "INPUT", "NodeSocketFloat", 0.0, 0.0, 999.0)
    _iface(ng, "TubeRadius", "INPUT", "NodeSocketFloat", 2.0, 1.2, 8.0, "mm; never below 1.2")
    _iface(ng, "RadiusAmp", "INPUT", "NodeSocketFloat", 0.4, 0.0, 2.0, "human base mm; signal may rewrite")
    _iface(ng, "Signal", "INPUT", "NodeSocketFloat", 0.0, 0.0, 1.0, "0-1 stand-in for the nonhuman channel")
    _iface(ng, "Influence", "INPUT", "NodeSocketFloat", 0.7, 0.0, 1.0, "lerp weight; 0.7 matches co_constraint.html")
    _iface(ng, "Correlation", "INPUT", "NodeSocketFloat", 0.35, 0.0, 1.0, "radius: 1 = edge order only; opening value from the triangle tool")
    _iface(ng, "Reverse", "INPUT", "NodeSocketBool", True, desc="halfway by edge count, radius ramp turns back")
    _iface(ng, "AlongSwell", "INPUT", "NodeSocketFloat", 0.8, 0.0, 3.0, "mm amplitude of the sine along each tube")
    _iface(ng, "AlongCycles", "INPUT", "NodeSocketFloat", 1.0, 0.25, 4.0, "how many sine waves fit on one tube")
    _iface(ng, "AlongPhase", "INPUT", "NodeSocketFloat", 0.0, 0.0, 1.0, "hand scrub; shifts the wave. Not driven by the frame")
    _iface(ng, "AlongSamples", "INPUT", "NodeSocketInt", 8, 4, 12, "points along each tube")
    ng.nodes.new("NodeGroupInput")
    ng.nodes.new("NodeGroupOutput")
    return ng


def _noise_signed(g, gi, vector, scale_sock, w_sock, loc_x, loc_y):
    """4D FBM; Fac remapped 0–1 → −1…+1. Same as NoiseDisplaceGN."""
    noise = g.node("ShaderNodeTexNoise", (loc_x, loc_y), noise_dimensions="4D", noise_type="FBM", normalize=True)
    g.links.new(vector, noise.inputs["Vector"])
    g.links.new(w_sock, noise.inputs["W"])
    g.links.new(scale_sock, noise.inputs["Scale"])
    noise.inputs["Detail"].default_value = 2.0
    noise.inputs["Roughness"].default_value = 0.5
    noise.inputs["Lacunarity"].default_value = 2.0
    signed = g.math("SUBTRACT", noise.outputs[0], 0.5, loc=(loc_x + 200, loc_y))
    return g.math("MULTIPLY", signed, 2.0, loc=(loc_x + 400, loc_y))


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-1200, 0)
    go.location = (2400, 80)

    # live = humanBase + (signalShaped - humanBase) * Influence
    # CageAmplitude shaped onto 0..8 mm. RadiusAmp shaped onto 0..(TubeRadius-1.2).
    signal = gi.outputs["Signal"]
    infl = gi.outputs["Influence"]
    amp_shaped = g.math("MULTIPLY", signal, 8.0, loc=(-1100, 360))
    amp_live = g.math(
        "MULTIPLY_ADD",
        g.math("SUBTRACT", amp_shaped, gi.outputs["CageAmplitude"], loc=(-900, 360)),
        infl,
        loc=(-680, 360),
        c=gi.outputs["CageAmplitude"],
    )
    amp_live = g.math("MINIMUM", 8.0, g.math("MAXIMUM", 0.0, amp_live, loc=(-460, 360)), loc=(-260, 360))
    rad_room = g.math("MAXIMUM", 0.0, g.math("SUBTRACT", gi.outputs["TubeRadius"], 1.2, loc=(-1100, 200)), loc=(-880, 200))
    rad_shaped = g.math("MULTIPLY", signal, rad_room, loc=(-680, 200))
    rad_live = g.math(
        "MULTIPLY_ADD",
        g.math("SUBTRACT", rad_shaped, gi.outputs["RadiusAmp"], loc=(-480, 200)),
        infl,
        loc=(-260, 200),
        c=gi.outputs["RadiusAmp"],
    )
    rad_live = g.math("MINIMUM", rad_room, g.math("MAXIMUM", 0.0, rad_live, loc=(-40, 200)), loc=(160, 200))

    ico = g.node("GeometryNodeMeshIcoSphere", (-900, 80))
    g.links.new(gi.outputs["Radius"], ico.inputs["Radius"])
    g.links.new(gi.outputs["Subdivisions"], ico.inputs["Subdivisions"])

    pos = g.node("GeometryNodeInputPosition", (-900, -200))
    nrm = g.node("GeometryNodeInputNormal", (-500, -320))
    signed = _noise_signed(g, gi, pos.outputs["Position"], gi.outputs["CageScale"], gi.outputs["Seed"], -700, -180)
    times_amp = g.math("MULTIPLY", signed, amp_live, loc=(-100, -80))
    along = g.vmath("SCALE", nrm.outputs["Normal"], loc=(80, -40), scale=times_amp)
    displace = g.node("GeometryNodeSetPosition", (80, 120))
    g.links.new(ico.outputs["Mesh"], displace.inputs["Geometry"])
    g.links.new(along, displace.inputs["Offset"])

    to_curve = g.node("GeometryNodeMeshToCurve", (300, 120))
    g.links.new(displace.outputs["Geometry"], to_curve.inputs["Mesh"])

    # Radius proceeds along icosphere edge index. Reverse folds the ramp at half the edges.
    dom = g.node("GeometryNodeAttributeDomainSize", (300, 420))
    dom.component = "CURVE"
    g.links.new(to_curve.outputs["Curve"], dom.inputs["Geometry"])
    n_splines = dom.outputs["Spline Count"]
    on_curve = g.node("GeometryNodeFieldOnDomain", (300, 300), data_type="FLOAT", domain="CURVE")
    idx = g.node("GeometryNodeInputIndex", (80, 300))
    g.links.new(idx.outputs["Index"], on_curve.inputs["Value"])
    spline_i = on_curve.outputs["Value"]
    denom = g.math("MAXIMUM", 1.0, g.math("SUBTRACT", n_splines, 1.0, loc=(520, 460)), loc=(720, 460))
    t = g.math("DIVIDE", spline_i, denom, loc=(920, 420))
    fold = g.math("MINIMUM", t, g.math("SUBTRACT", 1.0, t, loc=(920, 340)), loc=(1120, 380))
    signed_rev = g.math("SUBTRACT", g.math("MULTIPLY", fold, 4.0, loc=(1320, 380)), 1.0, loc=(1520, 380))
    signed_mono = g.math("SUBTRACT", g.math("MULTIPLY", t, 2.0, loc=(1120, 260)), 1.0, loc=(1320, 260))
    signed_seq = g.switch("FLOAT", gi.outputs["Reverse"], signed_mono, signed_rev, loc=(1720, 320))
    corr = gi.outputs["Correlation"]
    one_m_corr = g.math("SUBTRACT", 1.0, corr, loc=(1720, 200))

    w2 = g.math("ADD", gi.outputs["Seed"], 11.0, loc=(300, -200))
    signed_r = _noise_signed(g, gi, pos.outputs["Position"], gi.outputs["CageScale"], w2, 300, -360)
    mixed = g.math(
        "ADD",
        g.math("MULTIPLY", corr, signed_seq, loc=(1920, 240)),
        g.math("MULTIPLY", one_m_corr, signed_r, loc=(1920, 140)),
        loc=(2120, 180),
    )
    rad_delta = g.math("MULTIPLY", mixed, rad_live, loc=(2320, 80))
    rad_raw = g.math("ADD", gi.outputs["TubeRadius"], rad_delta, loc=(2520, 40))
    rad = g.math("MAXIMUM", 1.2, rad_raw, loc=(2720, 40))

    # Same sine on every tube. Phase is a hand slider, not the frame.
    # Each tube is shifted by its edge index, so they are not copies.
    resample = g.node("GeometryNodeResampleCurve", (2920, 220), mode="COUNT")
    g.links.new(to_curve.outputs["Curve"], resample.inputs["Curve"])
    g.links.new(gi.outputs["AlongSamples"], resample.inputs["Count"])
    fac = g.node("GeometryNodeSplineParameter", (2920, -40))
    tube_off = g.math("DIVIDE", spline_i, g.math("MAXIMUM", 1.0, n_splines, loc=(3120, -160)), loc=(3320, -120))
    arg = g.math(
        "ADD",
        g.math("ADD", g.math("MULTIPLY", gi.outputs["AlongCycles"], fac.outputs["Factor"], loc=(3120, -40)), gi.outputs["AlongPhase"], loc=(3320, -40)),
        tube_off,
        loc=(3520, -40),
    )
    wave = g.math("SINE", g.math("MULTIPLY", arg, math.tau, loc=(3720, -40)), loc=(3920, -40))
    swell = g.math("MULTIPLY", wave, gi.outputs["AlongSwell"], loc=(4120, 0))
    rad_along = g.math("MAXIMUM", 1.2, g.math("ADD", rad, swell, loc=(4120, 80)), loc=(4320, 80))

    set_rad = g.node("GeometryNodeSetCurveRadius", (4320, 120))
    g.links.new(resample.outputs["Curve"], set_rad.inputs["Curve"])
    g.links.new(rad_along, set_rad.inputs["Radius"])

    store = g.node("GeometryNodeStoreNamedAttribute", (3140, 120), data_type="FLOAT", domain="POINT")
    store.inputs["Name"].default_value = "tube_r"
    g.links.new(set_rad.outputs["Curve"], store.inputs["Geometry"])
    g.links.new(rad_along, store.inputs["Value"])
    store_seq = g.node("GeometryNodeStoreNamedAttribute", (3360, 120), data_type="FLOAT", domain="POINT")
    store_seq.inputs["Name"].default_value = "seq_s"
    g.links.new(store.outputs["Geometry"], store_seq.inputs["Geometry"])
    g.links.new(signed_seq, store_seq.inputs["Value"])

    circle = g.node("GeometryNodeCurvePrimitiveCircle", (760, -80))
    circle.mode = "RADIUS"
    circle.inputs["Resolution"].default_value = 12
    circle.inputs["Radius"].default_value = 1.0

    c2m = g.node("GeometryNodeCurveToMesh", (1020, 80))
    g.links.new(store_seq.outputs["Geometry"], c2m.inputs["Curve"])
    g.links.new(circle.outputs["Curve"], c2m.inputs["Profile Curve"])
    c2m.inputs["Fill Caps"].default_value = True

    merge = g.node("GeometryNodeMergeByDistance", (1260, 80))
    merge.inputs["Distance"].default_value = 0.15
    g.links.new(c2m.outputs["Mesh"], merge.inputs["Geometry"])

    mb = g.node("GeometryNodeMeshBoolean", (1480, 80))
    mb.operation = "UNION"
    mb.solver = "EXACT"
    mesh_in = next(s for s in mb.inputs if s.type == "GEOMETRY" and s.enabled)
    g.links.new(merge.outputs["Geometry"], mesh_in)
    try:
        mb.inputs["Self Intersection"].default_value = True
        mb.inputs["Hole Tolerant"].default_value = True
    except Exception:
        pass

    bbox = g.node("GeometryNodeBoundBox", (1760, -40))
    g.links.new(mb.outputs["Mesh"], bbox.inputs["Geometry"])
    zmin = g.node("ShaderNodeSeparateXYZ", (1960, -120))
    g.links.new(bbox.outputs["Min"], zmin.inputs[0])
    lift_z = g.math("ADD", g.math("SUBTRACT", 0.0, zmin.outputs["Z"], loc=(2160, -80)), 1.2, loc=(2360, -80))
    lift = g.node("ShaderNodeCombineXYZ", (1960, 40))
    g.links.new(lift_z, lift.inputs["Z"])
    place = g.node("GeometryNodeTransform", (1760, 120))
    g.links.new(mb.outputs["Mesh"], place.inputs["Geometry"])
    g.links.new(lift.outputs[0], place.inputs["Translation"])
    store_amp = g.node("GeometryNodeStoreNamedAttribute", (2000, 160), data_type="FLOAT", domain="POINT")
    store_amp.inputs["Name"].default_value = "live_amp"
    g.links.new(place.outputs["Geometry"], store_amp.inputs["Geometry"])
    g.links.new(amp_live, store_amp.inputs["Value"])
    store_ra = g.node("GeometryNodeStoreNamedAttribute", (2200, 160), data_type="FLOAT", domain="POINT")
    store_ra.inputs["Name"].default_value = "live_rad_amp"
    g.links.new(store_amp.outputs["Geometry"], store_ra.inputs["Geometry"])
    g.links.new(rad_live, store_ra.inputs["Value"])
    g.links.new(store_ra.outputs["Geometry"], go.inputs["Geometry"])
    return ng


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
    obj.name = OBJ_NAME
    obj.location = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.hide_set(False)
    obj.hide_viewport = False
    obj.hide_render = False
    for other in KEEP_OBJECTS:
        o = bpy.data.objects.get(other)
        if o is not None:
            o.hide_viewport = True
    for mod in list(obj.modifiers):
        if mod.name == "SphereTubeNet":
            obj.modifiers.remove(mod)
    mod = obj.modifiers.new("SphereTubeNet", "NODES")
    mod.node_group = ng
    names = [m.name for m in obj.modifiers]
    if "Smooth by Angle" in names and "SphereTubeNet" in names:
        obj.modifiers.move(names.index("SphereTubeNet"), 0)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    for o in bpy.context.selected_objects:
        if o != obj:
            o.select_set(False)
    return obj


def _island_count(bm):
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
            for nb in adj[cur]:
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
    islands = _island_count(bm)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    bounds = ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))) if xs else ((0, 0, 0), (0, 0, 0))
    size = (bounds[1][0] - bounds[0][0], bounds[1][1] - bounds[0][1], bounds[1][2] - bounds[0][2])

    def _attr_vals(name):
        if name not in mesh.attributes:
            return None
        attr = mesh.attributes[name]
        try:
            return [attr.data[i].value for i in range(len(attr.data))]
        except Exception:
            return None

    min_r = max_r = None
    tube_vals = _attr_vals("tube_r")
    if tube_vals:
        kept = [v for v in tube_vals if v > 0.05]
        if kept:
            min_r = min(kept)
            max_r = max(kept)
    seq_vals = _attr_vals("seq_s")
    seq_span = (min(seq_vals), max(seq_vals)) if seq_vals else None
    live_amp_vals = _attr_vals("live_amp")
    live_ra_vals = _attr_vals("live_rad_amp")
    live_amp = live_amp_vals[0] if live_amp_vals else None
    live_rad_amp = live_ra_vals[0] if live_ra_vals else None

    bm_t = bm.copy()
    bmesh.ops.triangulate(bm_t, faces=bm_t.faces)
    tree = BVHTree.FromBMesh(bm_t)
    bm_t.faces.ensure_lookup_table()
    pairs = tree.overlap(tree) or []
    vert_sets = [{v.index for v in f.verts} for f in bm_t.faces]
    cross = 0
    for a, b in pairs:
        if a >= b:
            continue
        if vert_sets[a] & vert_sets[b]:
            continue
        ca = bm_t.faces[a].calc_center_median()
        cb = bm_t.faces[b].calc_center_median()
        # AABB false positives on long thin tube triangles (~16 mm centers)
        if (ca - cb).length > 6.0:
            continue
        cross += 1
    min_th = None
    hits = 0
    bm_t.faces.ensure_lookup_table()
    for face in bm_t.faces:
        if face.calc_area() < 0.15:
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
    bm_t.free()
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
        "min_z": bounds[0][2],
        "min_tube_radius_attr": min_r,
        "max_tube_radius_attr": max_r,
        "seq_span": seq_span,
        "live_amp": live_amp,
        "live_rad_amp": live_rad_amp,
        "min_thickness_mm": min_th,
        "thickness_samples": hits,
        "self_intersect_pairs": cross,
    }


def _snapshot_inputs(obj):
    mod = obj.modifiers.get("SphereTubeNet") if obj else None
    if mod is None or mod.node_group is None:
        return {}
    ins = mod.properties.inputs
    saved = {}
    for item in mod.node_group.interface.items_tree:
        if getattr(item, "in_out", None) != "INPUT":
            continue
        try:
            saved[item.name] = getattr(ins, item.identifier).value
        except Exception:
            pass
    return saved


def _restore_inputs(obj, saved):
    mod = obj.modifiers.get("SphereTubeNet")
    if mod is None or not saved:
        return
    ins = mod.properties.inputs
    for item in mod.node_group.interface.items_tree:
        if getattr(item, "in_out", None) != "INPUT" or item.name not in saved:
            continue
        try:
            getattr(ins, item.identifier).value = saved[item.name]
        except Exception:
            pass


def _show_node_editor(ng, obj):
    """The bottom editor was the Timeline. Switch one area to the geometry node tree."""
    wm = bpy.context.window_manager
    for window in wm.windows:
        for area in window.screen.areas:
            if area.type not in {"DOPESHEET_EDITOR", "DOPESHEET", "TIMELINE"}:
                continue
            area.type = "NODE_EDITOR"
            space = area.spaces.active
            space.tree_type = "GeometryNodeTree"
            space.node_tree = ng
            try:
                space.pin = True
            except Exception:
                pass
            return
    for window in wm.windows:
        for area in window.screen.areas:
            if area.type != "NODE_EDITOR":
                continue
            space = area.spaces.active
            space.tree_type = "GeometryNodeTree"
            space.node_tree = ng
            return


def main():
    import traceback
    RESULT = {"ok": False}
    try:
        existing = bpy.data.objects.get(OBJ_NAME)
        saved_inputs = _snapshot_inputs(existing) if existing else {}
        ng = create_group()
        fill_group(ng)
        obj = setup_object(ng)
        _restore_inputs(obj, saved_inputs)
        _show_node_editor(ng, obj)
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception:
            pass
        bpy.context.view_layer.update()
        check = blender_check(obj)
        ins = obj.modifiers["SphereTubeNet"].properties.inputs
        by_name = {}
        for item in ng.interface.items_tree:
            if getattr(item, "in_out", None) != "INPUT":
                continue
            by_name[item.name] = getattr(ins, item.identifier)
        signal_sock = by_name["Signal"]
        saved_signal = signal_sock.value

        def _refresh():
            obj.update_tag(refresh={"OBJECT", "DATA"})
            ng.update_tag()
            bpy.context.view_layer.update()

        sweep = {}
        for value in (0.0, 1.0):
            signal_sock.value = value
            _refresh()
            swept = blender_check(obj)
            sweep[str(value)] = {
                "live_amp": swept["live_amp"],
                "live_rad_amp": swept["live_rad_amp"],
                "volume_mm3": swept["volume_mm3"],
                "islands": swept["islands"],
                "self_intersect_pairs": swept["self_intersect_pairs"],
                "min_tube_radius_attr": swept["min_tube_radius_attr"],
                "min_z": swept["min_z"],
            }
        signal_sock.value = saved_signal
        _refresh()
        check = blender_check(obj)
        blend_path = os.path.join(ROOT, "sphere_tube_net.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        RESULT = {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "kept": [n for n in KEEP_OBJECTS if bpy.data.objects.get(n)],
            "check": check,
            "signal_sweep": sweep,
            "blend": blend_path,
        }
    except Exception as e:
        RESULT = {"ok": False, "error": str(e), "trace": traceback.format_exc()}
    return RESULT


RESULT = main()
