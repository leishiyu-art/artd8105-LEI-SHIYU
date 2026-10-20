#!/usr/bin/env python3
"""Second print check: open an STL outside Blender.

Reports triangle count, bounding box in mm (1 unit = 1 mm),
signed volume, and connected-component count after welding vertices.
"""
from __future__ import annotations

import argparse
import struct
import sys
from collections import defaultdict


def load_stl(path: str):
    with open(path, "rb") as f:
        header = f.read(80)
        if len(header) < 80:
            raise ValueError("file too small to be an STL")
        rest = f.read()
    if rest[:5].lower() == b"solid" or header[:5].lower() == b"solid":
        # Might still be binary if it starts with solid but has a count.
        if len(rest) >= 4:
            count = struct.unpack_from("<I", rest, 0)[0]
            if 84 + count * 50 == 80 + len(rest):
                return _parse_binary(header + rest)
        text = (header + rest).decode("utf-8", errors="replace")
        return _parse_ascii(text)
    return _parse_binary(header + rest)


def _parse_binary(data: bytes):
    count = struct.unpack_from("<I", data, 80)[0]
    tris = []
    off = 84
    for _ in range(count):
        nums = struct.unpack_from("<12fH", data, off)
        tris.append((nums[3:6], nums[6:9], nums[9:12]))
        off += 50
    return tris


def _parse_ascii(text: str):
    tris = []
    verts = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) >= 4 and parts[0] == "vertex":
            verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            if len(verts) == 3:
                tris.append(tuple(verts))
                verts = []
    return tris


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def signed_volume(tris):
    acc = 0.0
    for a, b, c in tris:
        acc += _dot(a, _cross(b, c))
    return acc / 6.0


def bounds(tris):
    xs, ys, zs = [], [], []
    for tri in tris:
        for v in tri:
            xs.append(v[0])
            ys.append(v[1])
            zs.append(v[2])
    return {
        "min": (min(xs), min(ys), min(zs)),
        "max": (max(xs), max(ys), max(zs)),
        "size": (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)),
    }


def weld_key(v, quant=1e-4):
    return (round(v[0] / quant), round(v[1] / quant), round(v[2] / quant))


class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa != pb:
            self.p[pb] = pa


def component_count(tris):
    keys = {}
    verts = []
    faces = []
    for tri in tris:
        idx = []
        for v in tri:
            k = weld_key(v)
            if k not in keys:
                keys[k] = len(verts)
                verts.append(v)
            idx.append(keys[k])
        faces.append(tuple(idx))
    uf = UnionFind(len(verts))
    edge_faces = defaultdict(int)
    nonmanifold = 0
    boundary = 0
    for a, b, c in faces:
        uf.union(a, b)
        uf.union(b, c)
        for e in (tuple(sorted((a, b))), tuple(sorted((b, c))), tuple(sorted((c, a)))):
            edge_faces[e] += 1
    for n in edge_faces.values():
        if n != 2:
            if n == 1:
                boundary += 1
            else:
                nonmanifold += 1
    roots = {uf.find(i) for i in range(len(verts))} if verts else set()
    return {
        "vertices_welded": len(verts),
        "components": len(roots),
        "boundary_edges": boundary,
        "nonmanifold_edges": nonmanifold,
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("stl")
    args = p.parse_args(argv)
    tris = load_stl(args.stl)
    if not tris:
        print("no triangles")
        return 2
    box = bounds(tris)
    vol = signed_volume(tris)
    top = component_count(tris)
    print("file:", args.stl)
    print("triangles:", len(tris))
    print("bbox_min_mm: %.4f %.4f %.4f" % box["min"])
    print("bbox_max_mm: %.4f %.4f %.4f" % box["max"])
    print("bbox_size_mm: %.4f %.4f %.4f" % box["size"])
    print("signed_volume_mm3: %.4f" % vol)
    print("components:", top["components"])
    print("vertices_welded:", top["vertices_welded"])
    print("boundary_edges:", top["boundary_edges"])
    print("nonmanifold_edges:", top["nonmanifold_edges"])
    print("volume_positive:", vol > 0)
    print("one_shell:", top["components"] == 1)
    print("closed_manifold_edges:", top["boundary_edges"] == 0 and top["nonmanifold_edges"] == 0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
