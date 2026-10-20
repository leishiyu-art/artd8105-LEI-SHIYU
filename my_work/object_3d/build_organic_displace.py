"""Replace the tube-net node tree with a solid icosphere displaced along its normals.

Does not delete TraceShell or NoiseDisplacedSolid.
Does not write triangles_trace_shell.* or noise_displaced_solid.*.
"""
from __future__ import annotations

import math
import os
from collections import deque

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

ROOT = "/Users/leilei/Desktop/Cusor/my_work/object_3d"
GROUP_NAME = "OrganicDisplaceGN"
OBJ_NAME = "SphereTubeNet"
KEEP_OBJECTS = ("TraceShell", "NoiseDisplacedSolid")
# Finer of the two they allowed. In this Blender, 4 → 1280 faces; 5 → 5120.
SUBDIVISIONS = 5


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

    def math(self, op, a, b=None, loc=(0, 0)):
        node = self.node("ShaderNodeMath", loc, operation=op)
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
        if op in {"DOT_PRODUCT", "LENGTH", "DISTANCE"}:
            return node.outputs["Value"]
        return node.outputs[0]

    def _in(self, node, key, sock):
        if sock is None:
            return
        target = node.inputs[key] if not isinstance(key, int) else node.inputs[key]
        if hasattr(sock, "rna_type"):
            self.links.new(sock, target)
        else:
            target.default_value = sock


def _enabled(node, name):
    matches = [s for s in node.inputs if s.name == name and s.enabled]
    if not matches:
        raise KeyError(name)
    return matches[0]


def _iface(ng, name, stype, default, vmin, vmax, desc):
    item = ng.interface.new_socket(name=name, in_out="INPUT", socket_type=stype)
    item.description = desc
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
    _iface(ng, "Base Radius", "NodeSocketFloat", 30.0, 10.0, 80.0, "mm")
    _iface(ng, "Warp Amount", "NodeSocketFloat", 4.0, 0.0, 20.0, "mm; FDM preset keeps this small so the shell does not fold into itself")
    _iface(ng, "Noise Scale", "NodeSocketFloat", 0.4, 0.05, 4.0, "warp frequency only; detail noise is out of the offset")
    _iface(ng, "Breathing Frequency", "NodeSocketFloat", 1.0, 0.0, 6.0, "1 = one pinch-swell-pinch. Higher stacks lobes through each other")
    _iface(ng, "Amplitude", "NodeSocketFloat", 4.0, 0.0, 12.0, "mm radial breath. 12 mm crossed on this radius")
    _iface(ng, "Cell Scale", "NodeSocketFloat", 0.18, 0.05, 2.0, "lower = larger pores. FDM wants pores several mm across")
    _iface(ng, "Wall Band", "NodeSocketFloat", 0.35, 0.01, 0.5, "0.35 keeps one manifold shell with holes; lower splits or pinches")
    ng.nodes.new("NodeGroupInput")
    ng.nodes.new("NodeGroupOutput")
    return ng


def fill_group(ng):
    g = GN(ng)
    gi = next(n for n in ng.nodes if n.bl_idname == "NodeGroupInput")
    go = next(n for n in ng.nodes if n.bl_idname == "NodeGroupOutput")
    gi.location = (-1100, 0)
    go.location = (1900, 80)

    ico = g.node("GeometryNodeMeshIcoSphere", (-880, 200))
    g.links.new(gi.outputs["Base Radius"], ico.inputs["Radius"])
    ico.inputs["Subdivisions"].default_value = SUBDIVISIONS

    pos = g.node("GeometryNodeInputPosition", (-880, -40))
    nrm = g.node("GeometryNodeInputNormal", (900, -200))

    # Low-frequency vector warp. Scale stays at 1/4 of the detail noise.
    warp_scale = g.math("MULTIPLY", gi.outputs["Noise Scale"], 0.25, loc=(-880, -220))
    warp_noise = g.node("ShaderNodeTexNoise", (-640, -180), noise_dimensions="3D", noise_type="FBM", normalize=True)
    g.links.new(pos.outputs["Position"], warp_noise.inputs["Vector"])
    g.links.new(warp_scale, warp_noise.inputs["Scale"])
    warp_noise.inputs["Detail"].default_value = 1.0
    warp_noise.inputs["Roughness"].default_value = 0.5
    half = g.node("FunctionNodeInputVector", (-640, -380))
    half.vector = (0.5, 0.5, 0.5)
    signed_vec = g.vmath("SUBTRACT", warp_noise.outputs["Color"], half.outputs[0], loc=(-400, -220))
    unit_vec = g.vmath("SCALE", signed_vec, loc=(-200, -220), scale=2.0)
    warp_vec = g.vmath("SCALE", unit_vec, loc=(0, -220), scale=gi.outputs["Warp Amount"])
    warped = g.vmath("ADD", pos.outputs["Position"], warp_vec, loc=(200, -160))

    detail = g.node("ShaderNodeTexNoise", (200, 40), noise_dimensions="3D", noise_type="FBM", normalize=True)
    g.links.new(warped, detail.inputs["Vector"])
    g.links.new(gi.outputs["Noise Scale"], detail.inputs["Scale"])
    detail.inputs["Detail"].default_value = 2.0
    detail.inputs["Roughness"].default_value = 0.5
    signed = g.math("MULTIPLY", g.math("SUBTRACT", detail.outputs["Fac"], 0.5, loc=(440, 80)), 2.0, loc=(640, 80))

    # One cosine along height: bottom and top draw in, the middle pushes out.
    zsplit = g.node("ShaderNodeSeparateXYZ", (-640, -520))
    g.links.new(pos.outputs["Position"], zsplit.inputs["Vector"])
    z_norm = g.math("DIVIDE", zsplit.outputs["Z"], gi.outputs["Base Radius"], loc=(-400, -520))
    angle = g.math("MULTIPLY", g.math("MULTIPLY", z_norm, gi.outputs["Breathing Frequency"], loc=(-180, -520)), math.pi, loc=(20, -520))
    breath = g.math("COSINE", angle, loc=(220, -520))

    # Print pass: the cosine is the silhouette. The signed detail noise is not added.
    radial = g.math("MULTIPLY", gi.outputs["Amplitude"], breath, loc=(1060, 40))
    offset = g.vmath("SCALE", nrm.outputs["Normal"], loc=(1060, -80), scale=radial)

    displace = g.node("GeometryNodeSetPosition", (1280, 160))
    g.links.new(ico.outputs["Mesh"], displace.inputs["Geometry"])
    g.links.new(offset, displace.inputs["Offset"])

    # Distance-to-edge cut: cell interiors become through-holes. Walls stay.
    cells = g.node("ShaderNodeTexVoronoi", (1280, -80), voronoi_dimensions="3D", feature="DISTANCE_TO_EDGE", distance="EUCLIDEAN")
    cells.inputs["Randomness"].default_value = 0.0
    g.links.new(pos.outputs["Position"], cells.inputs["Vector"])
    g.links.new(gi.outputs["Cell Scale"], cells.inputs["Scale"])
    cut = g.node("FunctionNodeCompare", (1500, -80), data_type="FLOAT", operation="GREATER_THAN")
    g.links.new(cells.outputs["Distance"], cut.inputs[0])
    g.links.new(gi.outputs["Wall Band"], cut.inputs[1])
    dele = g.node("GeometryNodeDeleteGeometry", (1720, 80), domain="FACE")
    g.links.new(displace.outputs["Geometry"], dele.inputs["Geometry"])
    g.links.new(cut.outputs[0], dele.inputs["Selection"])

    smooth = g.node("GeometryNodeSetShadeSmooth", (1940, 80), domain="FACE")
    smooth.inputs["Shade Smooth"].default_value = True
    g.links.new(dele.outputs["Geometry"], smooth.inputs["Mesh"])

    bbox = g.node("GeometryNodeBoundBox", (1500, -20))
    g.links.new(smooth.outputs["Mesh"], bbox.inputs["Geometry"])
    zmin = g.node("ShaderNodeSeparateXYZ", (1700, -120))
    g.links.new(bbox.outputs["Min"], zmin.inputs["Vector"])
    lift_z = g.math("ADD", g.math("SUBTRACT", 0.0, zmin.outputs["Z"], loc=(1700, -200)), 3.2, loc=(1900, -200))
    lift = g.node("ShaderNodeCombineXYZ", (1900, 0))
    g.links.new(lift_z, lift.inputs["Z"])
    place = g.node("GeometryNodeTransform", (1720, 180))
    g.links.new(smooth.outputs["Mesh"], place.inputs["Geometry"])
    g.links.new(lift.outputs["Vector"], place.inputs["Translation"])
    g.links.new(place.outputs["Geometry"], go.inputs["Geometry"])
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
    obj.hide_set(False)
    obj.hide_viewport = False
    for other in KEEP_OBJECTS:
        other_obj = bpy.data.objects.get(other)
        if other_obj is not None:
            other_obj.hide_viewport = True
    for mod in list(obj.modifiers):
        if mod.name in {"SphereTubeNet", "OrganicDisplace", "Wall"}:
            obj.modifiers.remove(mod)
    mod = obj.modifiers.new("OrganicDisplace", "NODES")
    mod.node_group = ng
    wall = obj.modifiers.new("Wall", "SOLIDIFY")
    wall.thickness = 2.0
    wall.offset = 0.0
    try:
        wall.use_rim = True
        wall.use_even_offset = False
    except Exception:
        pass
    bpy.context.view_layer.objects.active = obj
    for selected in bpy.context.selected_objects:
        selected.select_set(False)
    obj.select_set(True)
    if not any(m.name == "Smooth by Angle" for m in obj.modifiers):
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=0.523599)
        except Exception:
            pass
    names = [m.name for m in obj.modifiers]
    if "OrganicDisplace" in names:
        obj.modifiers.move(names.index("OrganicDisplace"), 0)
    names = [m.name for m in obj.modifiers]
    if "Wall" in names:
        obj.modifiers.move(names.index("Wall"), 1)
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
    islands = _islands(bm)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    bm_t = bm.copy()
    bmesh.ops.triangulate(bm_t, faces=bm_t.faces)
    tree = BVHTree.FromBMesh(bm_t)
    bm_t.faces.ensure_lookup_table()
    vert_sets = [{v.index for v in f.verts} for f in bm_t.faces]
    cross = 0
    for a, b in tree.overlap(tree) or []:
        if a >= b or vert_sets[a] & vert_sets[b]:
            continue
        if (bm_t.faces[a].calc_center_median() - bm_t.faces[b].calc_center_median()).length <= 6.0:
            cross += 1
    smooth_faces = sum(1 for f in bm.faces if f.smooth)
    nverts = len(bm.verts)
    nfaces = len(bm.faces)
    bm_t.free()
    bm.free()
    ev.to_mesh_clear()
    return {
        "verts": nverts,
        "faces": nfaces,
        "smooth_faces": smooth_faces,
        "nonmanifold_edges": nonmanifold,
        "boundary_edges": boundary,
        "volume_mm3": vol,
        "islands": islands,
        "min_z": min(zs),
        "size_mm": (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)),
        "self_intersect_pairs": cross,
        "modifiers": [m.name for m in obj.modifiers],
    }


def main():
    import traceback
    try:
        ng = create_group()
        fill_group(ng)
        obj = setup_object(ng)
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception:
            pass
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != "VIEW_3D":
                    continue
                area.spaces.active.shading.type = "SOLID"
        obj.update_tag(refresh={"OBJECT", "DATA"})
        bpy.context.view_layer.update()
        check = blender_check(obj)
        path = os.path.join(ROOT, "organic_displace.blend")
        bpy.ops.wm.save_as_mainfile(filepath=path)
        return {
            "ok": True,
            "nodes": len(ng.nodes),
            "object": obj.name,
            "group": ng.name,
            "kept": [n for n in KEEP_OBJECTS if bpy.data.objects.get(n)],
            "check": check,
            "blend": path,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


RESULT = main()
