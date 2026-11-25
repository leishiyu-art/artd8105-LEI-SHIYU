#!/usr/bin/env python3
"""Paper figures, light exhibition poster language, Figma-editable SVG.

Presentation is on the elements (no style-class soup, no embedded images).
Coverage, stitches and the satin formula come from camera.html and the
saved picks in my_work/_local/loom_pick_dump/.
"""

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
DUMP = Path("/Users/leilei/Desktop/Cusor/my_work/_local/loom_pick_dump")

PAPER = "#F3EFE6"
INK = "#1A1714"
MUTED = "#6E665C"
HAIR = "#D4CBBC"
MADDER = "#D24E35"
INDIGO = "#1B3A6B"
CHART = "#D8E272"
WARP = "#E0D3B4"
WEFT = "#1B3A6B"
SKY = "#D5DEE8"
MUD = "#E6D3B0"
WATER = "#7EBBC4"
CANOPY = "#C5CC78"
TRUNK = "#3C4628"

ZH = "'PingFang SC', 'Noto Sans SC', 'Hiragino Sans GB', Helvetica, sans-serif"
EN = "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'SF Mono', ui-monospace, Menlo, monospace"

# Order matches LAYERS in camera.html. cov bitstrings use this order.
LAYERS = [
    ("animal", "琵鹭", "Spoonbill", "#EFE7D6", 5, True),
    ("atmos", "大气", "Air", "#8FA6C6", 4, False),
    ("litho", "地震", "Quake", "#B06A3C", 3, False),
    ("plant", "红树", "Mangrove", "#B4BC57", 3, False),
    ("hydro", "潮汐", "Tide", "#4FB0BE", 8, False),
    ("tech", "仪器", "Instrument", "#C9CDD6", 10, True),
    ("human", "观众", "Visitor", "#D24E35", 6, False),
]
BY = {k: i for i, (k, *_) in enumerate(LAYERS)}
SEL = 4
N = 176  # 2*SEL + 7*24

# Ecological order, top of the section to the cloth.
ECO = ["atmos", "plant", "animal", "hydro", "litho", "tech", "human"]


def sat(i, j, n=1):
    return ((i * 3 - j) % 8 + 8) % 8 < n


def band_x(S):
    return SEL + 2 + max(0.0, min(1.0, S)) * (N - 2 * SEL - 4)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']

    def add(self, s):
        self.p.append(s)

    def g(self, i):
        self.add(f'<g id="{i}">')
        return self

    def ge(self):
        self.add("</g>")
        return self

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="square"{d}/>'
        )

    def circle(self, cx, cy, r, fill=INK, stroke="none", sw=1):
        self.add(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def ellipse(self, x, y, w, h, fill, stroke="none", sw=1):
        self.add(
            f'<ellipse cx="{x + w / 2:.2f}" cy="{y + h / 2:.2f}" rx="{w / 2:.2f}" ry="{h / 2:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def poly(self, pts, fill, stroke="none", sw=1):
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.add(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=14, fill=INK, font="zh", anchor="start", ls=0, weight=400):
        fam = {"zh": ZH, "en": EN, "mono": MONO}[font]
        extra = f' letter-spacing="{ls}"' if ls else ""
        self.add(
            f'<text x="{x:.2f}" y="{y:.2f}" fill="{fill}" font-family="{fam}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'
        )

    def save(self, name):
        doc = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">\n'
            + "\n".join(self.p)
            + "\n</svg>\n"
        )
        path = OUT / name
        path.write_text(doc, encoding="utf-8")
        return path


def meta(fig, num, right):
    fig.g("header")
    fig.text(56, 48, num, 12, MUTED, "mono", ls=2.4)
    fig.text(fig.w - 56, 48, right, 12, MUTED, "mono", anchor="end", ls=1.6)
    fig.rect(56, 62, 42, 3, MADDER)
    fig.ge()


def foot(fig, s):
    fig.g("footer")
    fig.text(56, fig.h - 28, s, 11, MUTED, "mono", ls=0.4)
    fig.ge()


def yarn_of(key):
    return LAYERS[BY[key]]


def cell_up(i, j):
    if i < SEL or i >= N - SEL:
        return (i + j) % 2 == 0
    return sat(i, j, 1)


def draw_satin(fig, x, y, cols, rows, cell, j0=0, i0=0, gap=0.6):
    for j in range(rows):
        for i in range(cols):
            up = cell_up(i0 + i, j0 + j)
            fig.rect(x + i * cell, y + j * cell, cell - gap, cell - gap, WARP if up else WEFT)


def draw_bits(fig, x, y, bits, cell, color, stroke=None):
    """Poster convention: a square where the yarn is present."""
    for i, b in enumerate(bits):
        if b == "1":
            fig.rect(
                x + i * cell,
                y,
                cell - 1,
                cell - 1,
                color,
                stroke or "none",
                0.6 if stroke else 0,
            )


def runs_of(bits, limit, sel=SEL):
    """camera.html runs(): cut a covered run at the yarn float."""
    out = []
    i = sel
    last = len(bits) - sel
    while i < last:
        if bits[i] != "1":
            i += 1
            continue
        e = i
        while e < last and bits[e] == "1" and (e - i) < limit:
            e += 1
        out.append((i, e - i))
        i = e
    return out


def load_pick(name):
    p = json.loads((DUMP / name).read_text())
    assert len(p["cov"]) == 7
    for b in p["cov"]:
        assert len(b) == N
    return p


def header_title(fig, zh, en, y=108):
    fig.g("title")
    fig.text(56, y, zh, 52, INK, "zh", ls=6, weight=500)
    fig.text(56, y + 32, en, 13, MUTED, "en", ls=1.8)
    fig.ge()


# ---------------------------------------------------------------------------
# shared drawings
# ---------------------------------------------------------------------------

def section(fig, x, y, w, h, hydro_f, plant_f, animal_f, gid="section"):
    """Shore-to-channel section. Fractions are band centers on the cloth, not elevations."""
    fig.g(gid)
    bot = y + h
    mud_l = y + h * 0.50
    mud_e = y + h * 0.64
    xe = x + w * hydro_f
    fig.rect(x, y, w, h, SKY)
    for t in (0.14, 0.26, 0.38):
        fig.line(x + 18, y + h * t, x + w - 18, y + h * t, "#8FA6C6", 1)
    fig.poly([(x, mud_l), (xe, mud_e), (xe, bot), (x, bot)], MUD)
    fig.poly([(xe, mud_e), (x + w, mud_e - h * 0.03), (x + w, bot), (xe, bot)], WATER)
    for i in range(4):
        yy = mud_e + 18 + i * ((bot - mud_e - 28) / 4)
        fig.line(xe + 14, yy, x + w - 16, yy, "#F3EFE6", 1.25)
    # mangroves gathered on the plant band
    for k, (df, sc) in enumerate(((-0.09, 0.85), (-0.04, 1.15), (0.01, 0.95), (0.06, 1.2), (0.10, 0.8))):
        fx = min(hydro_f - 0.05, max(0.05, plant_f + df))
        cx = x + w * fx
        base = mud_l + (mud_e - mud_l) * (fx / max(hydro_f, 0.2))
        fig.line(cx, base, cx, base - h * 0.18 * sc, TRUNK, 2)
        rw, rh = 46 * sc, h * 0.15 * sc
        fig.ellipse(cx - rw / 2, base - h * 0.30 * sc - rh * 0.2, rw, rh, CANOPY)
    # spoonbills standing on the mud at their band
    for dx in (-28, 0, 26):
        bx = x + w * animal_f + dx
        if bx > xe - 10:
            bx = xe - 18 + dx * 0.3
        ground = mud_l + (mud_e - mud_l) * ((bx - x) / (xe - x))
        fig.line(bx - 3, ground, bx - 3, ground - 14, INK, 1.2)
        fig.line(bx + 3, ground, bx + 3, ground - 14, INK, 1.2)
        fig.line(bx, ground - 14, bx, ground - 28, INK, 1.3)
        fig.line(bx, ground - 26, bx + 12, ground - 28, INK, 1.3)
        fig.circle(bx, ground - 32, 3.2, INK)
    fig.line(xe, y + 8, xe, bot, INK, 1, "2 3")
    fig.text(x + 8, bot - 10, "岸  SHORE", 11, INK, "mono", ls=1)
    fig.text(x + w - 8, bot - 10, "CHANNEL  水道", 11, "#F3EFE6", "mono", anchor="end", ls=1)
    fig.ge()


def poster_row(fig, x, y, bits, cell, color, stroke=None, rule=True):
    if rule:
        fig.line(x, y + cell * 0.55, x + len(bits) * cell, y + cell * 0.55, color, 1.4)
    draw_bits(fig, x, y, bits, cell, color, stroke)


def cloth_pick(fig, x, y, cell, j, cov, stitches, show_n=None, i0=0):
    """One pick: satin ground, floats cut at the yarn float, then stitch marks."""
    n = show_n or (N - i0)
    draw_satin(fig, x, y, n, 1, cell, j0=j, i0=i0, gap=max(0.35, cell * 0.06))
    for key, *_rest in LAYERS:
        bits = cov[BY[key]]
        color, fl, light = yarn_of(key)[3], yarn_of(key)[4], yarn_of(key)[5]
        for a, ln in runs_of(bits, fl):
            if a + ln <= i0 or a >= i0 + n:
                continue
            start, end = max(a, i0), min(a + ln, i0 + n)
            gap = max(2.0, cell * 0.22)
            fig.rect(
                x + (start - i0) * cell + gap * 0.35,
                y + cell * 0.18,
                max(1.2, (end - start) * cell - gap),
                cell * 0.64,
                color,
                INK if light else "none",
                0.5 if light else 0,
            )
    arm = max(2.2, cell * 0.28)
    for s in stitches:
        if s["i"] < i0 or s["i"] >= i0 + n or s["b"] < 0:
            continue
        cx = x + (s["i"] - i0) * cell + cell * 0.5
        cy = y + cell * 0.5
        fig.line(cx - arm, cy - arm, cx + arm, cy + arm, INK, 1.1)
        fig.line(cx + arm, cy - arm, cx - arm, cy + arm, MADDER, 1.1)


# ---------------------------------------------------------------------------
# Figure 1 — section
# ---------------------------------------------------------------------------

def fig01(p156):
    W, H = 1600, 980
    cell = 7
    fig = Fig(W, H)
    meta(fig, "FIG. 1", "COTAI  22.135 N  113.555 E")
    header_title(fig, "剖面", "The cloth's width is this section. One saved pick sits on the same axis.")
    names = {
        "atmos": "1 year",
        "plant": "1 day",
        "animal": "1 year",
        "hydro": "12.4 h",
        "litho": "event",
        "tech": "1 s",
        "human": "press",
    }
    x, w = 168, N * cell
    hydro = band_x(p156["layers"][BY["hydro"]]["S"]) / N
    plant = band_x(p156["layers"][BY["plant"]]["S"]) / N
    animal = band_x(p156["layers"][BY["animal"]]["S"]) / N
    section(fig, x, 200, w, 380, hydro, plant, animal)
    fig.g("quake")
    ox, oy = x + w + 36, 228
    fig.circle(ox, oy, 8, "#B06A3C")
    for t in (0.16, 0.40, 0.62, 0.86):
        fig.line(ox - 8, oy, x + w, 200 + 380 * t, "#B06A3C", 1)
    fig.text(ox, 258, "地震", 13, INK, "zh", anchor="middle")
    fig.text(ox, 276, "贯穿", 11, MUTED, "mono", anchor="middle", ls=1)
    fig.ge()
    fig.g("pick-156")
    fig.text(x, 616, "PICK 156    21 NOV 2026    14:45    SAVED COVERAGE", 11, MUTED, "mono", ls=1.2)
    for i, key in enumerate(ECO):
        color, light = yarn_of(key)[3], yarn_of(key)[5]
        yy = 636 + i * 28
        fig.text(56, yy + 12, yarn_of(key)[1], 13, INK, "zh")
        poster_row(fig, x, yy, p156["cov"][BY[key]], cell, color, INK if light else None)
        fig.text(x + w + 12, yy + 12, names[key], 12, MUTED, "mono", ls=0.4)
    fig.line(x + hydro * w, 200, x + hydro * w, 636 + 7 * 28, INK, 1, "2 3")
    fig.ge()
    foot(fig, "camera.html  ·  bandX = SEL + 2 + S × 168  ·  pick 156 tide S aligns the water line  ·  no surveyed elevation")
    fig.save("fig01_overview.svg")


# ---------------------------------------------------------------------------
# Figure 2 — process, three drawings
# ---------------------------------------------------------------------------

def fig02(p156):
    W, H = 1600, 640
    fig = Fig(W, H)
    meta(fig, "FIG. 2", "RESEARCH THROUGH DESIGN")
    header_title(fig, "过程", "Site, seven temporal tracks, then the cloth. The tracks are periods, not a saved recording.")
    # 1 section
    fig.g("site")
    fig.text(56, 210, "01  现场", 13, MUTED, "mono", ls=1.2)
    hydro = band_x(p156["layers"][BY["hydro"]]["S"]) / N
    plant = band_x(p156["layers"][BY["plant"]]["S"]) / N
    animal = band_x(p156["layers"][BY["animal"]]["S"]) / N
    section(fig, 56, 230, 440, 280, hydro, plant, animal, "site-section")
    fig.ge()
    fig.rect(520, 360, 36, 6, CHART)
    # 2 seven tracks — square density follows the intrinsic period, not measured samples
    fig.g("tracks")
    fig.text(580, 210, "02  七条时间轨", 13, MUTED, "mono", ls=1.2)
    ticks = {"atmos": 2, "plant": 8, "animal": 2, "hydro": 16, "litho": 3, "tech": 24, "human": 1}
    for i, key in enumerate(ECO):
        color, light = yarn_of(key)[3], yarn_of(key)[5]
        y = 246 + i * 36
        fig.line(580, y + 10, 980, y + 10, color, 1.4)
        n = ticks[key]
        span = 400
        for k in range(n):
            xx = 580 + (k + 0.5) * span / n
            fig.rect(xx, y, 12, 12, color, INK if light else "none", 0.5)
        fig.text(996, y + 12, yarn_of(key)[1], 13, INK, "zh")
    fig.ge()
    fig.rect(1124, 360, 36, 6, CHART)
    # 3 a real ground, one real pick's tide floats on the middle row
    fig.g("cloth")
    fig.text(1184, 210, "03  织造", 13, MUTED, "mono", ls=1.2)
    cell = 14
    bits = p156["cov"][BY["hydro"]]
    cuts = [c for c in runs_of(bits, 8) if c[1] > 2]
    i0, ln = cuts[0]
    draw_satin(fig, 1184, 250, 16, 12, cell, j0=0, i0=i0)
    fig.rect(1184 + 1, 250 + 6 * cell + 3, ln * cell - 2, cell - 6, "#4FB0BE")
    fig.text(1184, 250 + 12 * cell + 28, f"ends {i0}–{i0 + ln - 1}  ·  float 8", 11, MUTED, "mono")
    fig.ge()
    foot(fig, "Tick counts on the middle drawing stand for period length. They are not samples from a sound file.")
    fig.save("fig02_process.svg")


# ---------------------------------------------------------------------------
# Figure 3 — time
# ---------------------------------------------------------------------------

def fig03():
    W, H = 1600, 980
    fig = Fig(W, H)
    meta(fig, "FIG. 3", "THREE CLOCKS")
    header_title(fig, "时间", "Same pick index, different durations. Playback compresses the mudflat clock only.")
    # mudflat clock
    fig.g("mudflat-clock")
    fig.text(56, 200, "01  泥滩钟", 13, MUTED, "mono", ls=1.2)
    x, y, bw = 56, 230, 1200
    past, fut = 384 / 480 * bw, 96 / 480 * bw
    fig.rect(x, y, past, 18, INK)
    fig.rect(x + past, y, fut, 18, "none", INK, 1.2)
    fig.line(x + 383 / 480 * bw, y - 8, x + 383 / 480 * bw, y + 26, MADDER, 1.5)
    fig.text(x, y - 10, "384 PICKS WOVEN", 11, MUTED, "mono", ls=1)
    fig.text(x + past + fut, y - 10, "96 FORECAST", 11, MUTED, "mono", anchor="end", ls=1)
    fig.text(x + 383 / 480 * bw, y + 48, "NOW", 11, MADDER, "mono", anchor="middle", ls=1)
    for i, key in enumerate(ECO):
        color = yarn_of(key)[3]
        yy = y + 70 + i * 16
        fig.line(x, yy, x + bw, yy, color, 2)
    fig.text(x + bw + 16, y + 78, "15 MIN / PICK", 12, INK, "mono", ls=1)
    fig.text(x + bw + 16, y + 98, "seven yarns, one bar", 12, MUTED, "en")
    fig.ge()
    # intrinsic — 24 picks each, durations unequal
    fig.g("intrinsic")
    fig.text(56, 470, "02  自身时间    24 PICKS = ONE CYCLE", 13, MUTED, "mono", ls=1.2)
    dur = {
        "atmos": "1 year",
        "plant": "1 day",
        "animal": "1 year",
        "hydro": "12.4 h",
        "litho": "no cycle",
        "tech": "1 s",
        "human": "—",
    }
    for i, key in enumerate(ECO):
        color, light = yarn_of(key)[3], yarn_of(key)[5]
        yy = 498 + i * 32
        fig.text(56, yy + 14, yarn_of(key)[1], 14, INK, "zh")
        if key == "litho":
            for k, xx in enumerate((200, 280, 390)):
                fig.circle(xx, yy + 8, 5, color)
            fig.text(430, yy + 12, "events, not 24 picks", 12, MUTED, "en")
        elif key == "human":
            fig.rect(200, yy, 14, 14, color)
            fig.text(230, yy + 12, "a press, no cycle", 12, MUTED, "en")
        else:
            for k in range(24):
                fig.rect(200 + k * 16, yy, 12, 14, color, INK if light else "none", 0.4)
        fig.text(1544, yy + 14, dur[key], 13, INK, "mono", anchor="end", ls=0.6)
    fig.ge()
    # playback
    fig.g("playback")
    fig.text(56, 760, "03  回放", 13, MUTED, "mono", ls=1.2)
    fig.rect(56, 800, 360, 10, INK)
    fig.text(56, 788, "15 MIN", 12, INK, "mono", ls=1)
    fig.poly([(430, 796), (430, 814), (520, 808), (520, 802)], CHART)
    fig.rect(536, 802, 48, 6, INK)
    fig.text(536, 788, "1.1 S", 12, INK, "mono", ls=1)
    fig.rect(760, 794, 16, 16, MADDER)
    fig.text(788, 808, "A PRESS IS NOT COMPRESSED", 12, MADDER, "mono", ls=0.8)
    fig.text(56, 840, "384 picks of the woven past play back in about 7 minutes.", 13, MUTED, "en")
    fig.ge()
    foot(fig, "Intrinsic picks are generated from each period. They are not a resample of the mudflat feeds.")
    fig.save("fig03_time.svg")


# ---------------------------------------------------------------------------
# Figure 4 — grammar, AdaCAD pipeline
# ---------------------------------------------------------------------------

def fig04(p156):
    W, H = 1600, 1120
    fig = Fig(W, H)
    meta(fig, "FIG. 4", "WEAVING GRAMMAR")
    header_title(fig, "语法", "One measured tide value, followed into a draft. Yellow marks the step that becomes structure.")
    s = p156["sampled"]
    hydro = p156["layers"][BY["hydro"]]
    # five steps
    labels = [
        ("01", "数值", "value"),
        ("02", "映射", "S and v"),
        ("03", "覆盖", "coverage"),
        ("04", "底组织", "ground"),
        ("05", "一纬", "one pick"),
    ]
    gap, colw = 18, 276
    x0, y0, bh = 48, 200, 300
    for n, (num, zh, en) in enumerate(labels):
        x = x0 + n * (colw + gap)
        fig.g(f"step-{n+1}")
        if n == 2:
            fig.rect(x - 8, y0 - 8, colw + 16, bh + 16, CHART)
        fig.rect(x, y0, colw, bh, PAPER, INK, 1)
        fig.text(x + 14, y0 + 24, f"{num}  {zh}", 13, MUTED, "mono", ls=1)
        fig.text(x + 14, y0 + 42, en.upper(), 11, MUTED, "en", ls=1.2)
        if n == 0:
            rows = [
                ("CO₂", f"{s['co2']:.1f}", "ppm", False),
                ("light", f"{s['sw']:.0f}", "W/m²", False),
                ("tide", f"{s['level']:.2f}", "m", True),
                ("wind", f"{s['wind']:.1f}", "km/h", False),
                ("rain", f"{s['rain']:.0f}", "mm/h", False),
            ]
            for i, (k, v, u, on) in enumerate(rows):
                yy = y0 + 70 + i * 40
                if on:
                    fig.rect(x + 10, yy - 18, colw - 20, 32, CHART)
                fig.text(x + 18, yy + 4, k, 12, MUTED, "mono")
                fig.text(x + colw - 18, yy + 4, f"{v} {u}", 16, INK, "mono", anchor="end")
        elif n == 1:
            fig.line(x + 24, y0 + 150, x + colw - 24, y0 + 150, INK, 1)
            sx = x + 24 + hydro["S"] * (colw - 48)
            fig.circle(sx, y0 + 150, 7, "#4FB0BE", INK, 1)
            fig.text(x + 24, y0 + 180, f"S  {hydro['S']:.2f}", 16, INK, "mono")
            fig.rect(x + 24, y0 + 210, colw - 48, 10, HAIR)
            fig.rect(x + 24, y0 + 210, (colw - 48) * hydro["v"], 10, "#4FB0BE")
            fig.text(x + 24, y0 + 248, f"v  {hydro['v']:.2f}", 16, INK, "mono")
        elif n == 2:
            bits = p156["cov"][BY["hydro"]]
            ones = [i for i, b in enumerate(bits) if b == "1"]
            a, b = max(SEL, ones[0] - 1), min(N - SEL, ones[-1] + 2)
            window = bits[a:b]
            cw = min(12, (colw - 28) / len(window))
            ox = x + (colw - len(window) * cw) / 2
            oy = y0 + 120
            for i, bit in enumerate(window):
                fig.rect(ox + i * cw, oy, cw - 1, cw - 1, "#4FB0BE" if bit == "1" else "none", INK, 0.6)
            fig.text(x + 16, y0 + 250, f"ends {a}–{b - 1}", 12, INK, "mono")
            fig.text(x + 16, y0 + 270, "1 = yarn present", 12, MUTED, "en")
        elif n == 3:
            cw = 18
            ox = x + (colw - 8 * cw) / 2
            oy = y0 + 80
            draw_satin(fig, ox, oy, 8, 8, cw, j0=0, i0=0)
            fig.rect(ox - 3, oy - 3, 8 * cw + 2, 8 * cw + 2, "none", CHART, 2)
            fig.text(x + 16, y0 + 260, "(3i − j) mod 8 < 1", 13, INK, "mono")
        else:
            cw = 14
            bits = p156["cov"][BY["hydro"]]
            ones = [i for i, b in enumerate(bits) if b == "1"]
            i0 = max(0, ones[0] - 1)
            show = min(16, N - i0)
            ox = x + (colw - show * cw) / 2
            oy = y0 + 90
            cloth_pick(fig, ox, oy, cw, j=156, cov=p156["cov"], stitches=[], show_n=show, i0=i0)
            fig.text(x + 16, y0 + 250, f"pick 156, ends {i0}–{i0 + show - 1}", 12, INK, "mono")
            fig.text(x + 16, y0 + 270, "tide float on the ground", 12, MUTED, "en")
        fig.ge()
        if n < 4:
            cx = x + colw + gap / 2
            fig.rect(cx - 8, y0 + bh / 2 - 3, 16, 6, CHART)
    # matrix
    fig.g("matrix")
    fig.text(56, 560, "WHICH OPERATION EACH YARN RECEIVES", 12, MUTED, "mono", ls=1.4)
    heads = ["v  密度", "S  位置", "float  浮长", "stitch  缝合"]
    hx = [420, 680, 940, 1200]
    for h, xx in zip(heads, hx):
        fig.text(xx, 600, h, 12, MUTED, "mono", ls=0.6)
    # open dot = only on event or press; square = visitor's own mark
    sometimes = {"litho", "human"}
    no_pair = {"human"}
    for i, key in enumerate(ECO):
        zh, color, fl, light = yarn_of(key)[1], yarn_of(key)[3], yarn_of(key)[4], yarn_of(key)[5]
        yy = 628 + i * 48
        fig.line(56, yy + 36, 1500, yy + 36, HAIR, 1)
        fig.rect(56, yy + 4, 16, 24, color, INK if light else "none", 0.6)
        fig.text(84, yy + 22, zh, 16, INK, "zh")
        fig.text(170, yy + 22, yarn_of(key)[2], 12, MUTED, "en")
        for xx in hx[:2]:
            if key in sometimes:
                fig.circle(xx + 28, yy + 16, 6, "none", INK, 1.3)
            else:
                fig.circle(xx + 28, yy + 16, 6, INK)
        fig.text(hx[2] + 8, yy + 22, str(fl), 18, INK, "mono")
        if key in no_pair:
            fig.rect(hx[3] + 20, yy + 8, 14, 14, "none", MADDER, 1.4)
        else:
            fig.circle(hx[3] + 27, yy + 16, 6, INK)
    fig.text(56, 980, "Open dot: only when a quake is in the window, or on a press. Open square: the visitor mark, not a pair.", 12, MUTED, "en")
    fig.ge()
    foot(fig, "bandX = 6 + S × 168     w = 2.4 + 9v     d = exp(−(i−bandX)² / 2w²) × (0.62 + 0.38v)     cov = 1 if d > 0.5")
    fig.save("fig04_grammar.svg")


# ---------------------------------------------------------------------------
# Figure 5 — local weave
# ---------------------------------------------------------------------------

def bracket(fig, x, y, w, label):
    fig.line(x, y, x, y + 8, INK, 1)
    fig.line(x + w, y, x + w, y + 8, INK, 1)
    fig.line(x, y + 8, x + w, y + 8, INK, 1)
    fig.text(x + w / 2, y + 22, label, 11, INK, "mono", anchor="middle")


def fig05(p156, p172):
    W, H = 1600, 1180
    fig = Fig(W, H)
    meta(fig, "FIG. 5", "DRAFT DETAIL")
    header_title(fig, "组织", "Ground, float, stitch. Cells are the running formula and two saved picks.")
    cell = 13
    # ground, including 4-end plain selvedge
    fig.g("ground")
    fig.text(56, 200, "01  底组织", 13, MUTED, "mono", ls=1.2)
    cols, rows = 20, 18
    draw_satin(fig, 56, 220, cols, rows, cell, j0=0, i0=0)
    fig.rect(56 + 4 * cell - 2, 220 - 2, 8 * cell + 2, 8 * cell + 2, "none", CHART, 2)
    fig.text(56, 220 + rows * cell + 22, "yellow box = one 8-end repeat, n = 1", 12, MUTED, "en")
    fig.text(56, 220 + rows * cell + 42, "first 4 ends: plain weave selvedge", 12, MUTED, "en")
    fig.text(56, 220 + rows * cell + 70, "sat(i, j, 1)", 14, INK, "mono")
    fig.text(56, 220 + rows * cell + 90, "((3*i - j) % 8 + 8) % 8 < 1", 13, INK, "mono")
    fig.ge()
    # floats
    fig.g("floats")
    fig.text(420, 200, "02  浮长   PICK 156", 13, MUTED, "mono", ls=1.2)

    def float_study(y, key, title):
        bits = p156["cov"][BY[key]]
        fl = yarn_of(key)[4]
        color, light = yarn_of(key)[3], yarn_of(key)[5]
        ones = [i for i, b in enumerate(bits) if b == "1"]
        a, b = ones[0], ones[-1] + 1
        window = bits[a:b]
        cw = 16
        fig.text(420, y, title, 14, INK, "zh")
        fig.text(560, y, f"float {fl}", 13, MUTED, "mono")
        ox, oy = 420, y + 16
        for i, bit in enumerate(window):
            fig.rect(ox + i * cw, oy, cw - 2, cw - 2, color if bit == "1" else "none", INK if bit == "1" and light else HAIR, 0.7)
        cuts = [(i - a, ln) for i, ln in runs_of(bits, fl) if a <= i < b]
        by = oy + cw + 10
        for i0, ln in cuts:
            fig.rect(ox + i0 * cw + 1, by, max(3, ln * cw - 5), 12, color, INK if light else "none", 0.5)
            fig.text(ox + i0 * cw + ln * cw / 2, by + 26, str(ln), 11, MUTED, "mono", anchor="middle")
        fig.text(420, by + 46, "squares are the covered ends; bars below are cut at the float", 12, MUTED, "en")
        return by + 78

    y2 = float_study(230, "hydro", "潮汐  靛青丝")
    float_study(y2 + 10, "plant", "红树  苎麻")
    fig.ge()
    # stitches from pick 172
    fig.g("stitches")
    fig.text(980, 200, "03  缝合   PICK 172", 13, MUTED, "mono", ls=1.2)
    # roost
    fig.text(980, 240, "roost", 12, MUTED, "mono", ls=1)
    fig.line(980, 280, 1220, 280, "#EFE7D6", 8)
    fig.line(980, 300, 1220, 300, "#B4BC57", 6)
    for i, label in ((28, "i 28"), (31, "i 31")):
        # map end 20–40 into the line
        cx = 980 + (i - 20) / 20 * 240
        fig.line(cx - 6, 274, cx + 6, 306, INK, 1.4)
        fig.line(cx + 6, 274, cx - 6, 306, MADDER, 1.4)
        fig.text(cx, 326, label, 11, INK, "mono", anchor="middle")
    fig.text(980, 352, "{ i:28, a:animal, b:plant }", 13, INK, "mono")
    fig.text(980, 372, "{ i:31, a:animal, b:plant }", 13, INK, "mono")
    # jolt
    fig.text(980, 420, "jolt    every 6 ends, five pairs, not the visitor", 12, MUTED, "mono", ls=0.3)
    names = ["琵鹭", "大气", "地震", "红树", "潮汐", "仪器"]
    colors = [yarn_of(k)[3] for k in ["animal", "atmos", "litho", "plant", "hydro", "tech"]]
    for i, (name, color) in enumerate(zip(names, colors)):
        yy = 450 + i * 36
        fig.line(1100, yy, 1320, yy, color, 6)
        fig.text(980, yy + 4, name, 13, INK, "zh")
        if i < 5:
            cx, cy = 1180, yy + 18
            fig.line(cx - 5, cy - 8, cx + 5, cy + 8, INK, 1.2)
            fig.line(cx + 5, cy - 8, cx - 5, cy + 8, MADDER, 1.2)
    fig.text(980, 690, "i = 7, 13, 19 … 169", 14, INK, "mono")
    fig.text(980, 712, "28 positions × 5 pairs = 140", 14, INK, "mono")
    fig.text(980, 734, "140 + 2 roost = 142 on this pick", 13, MUTED, "en")
    # code
    fig.text(980, 780, "for (i = SEL + 3; i < N - SEL; i += 6)", 13, INK, "mono")
    fig.text(980, 800, "  for (q = 0; q < 5; q++) stitch(i, q, q+1)", 13, INK, "mono")
    fig.text(980, 832, "SEL = 4, so the first i is 7.", 12, MUTED, "en")
    fig.text(980, 852, "q stops before the visitor layer.", 12, MUTED, "en")
    fig.ge()
    # a strip of the actual pick 172 so the X positions can be checked
    fig.g("pick-172-strip")
    fig.text(56, 900, "PICK 172    21 NOV 2026    18:45    ALL 176 ENDS", 11, MUTED, "mono", ls=1.2)
    cloth_pick(fig, 56, 918, 8, j=172, cov=p172["cov"], stitches=p172["st"], show_n=N)
    fig.text(56, 952, "M 5.9. Tide 1.48 m. Roost at ends 28 and 31. Jolt at every sixth end from 7 to 169.", 12, MUTED, "en")
    fig.ge()
    foot(fig, "runs() cuts a covered run at the float. Ground is satin n = 1 on the field, plain weave on the 4-end selvedge and on day lines.")
    fig.save("fig05_stitching.svg")


# ---------------------------------------------------------------------------
# Figure 6 — interface, dark screens on the light sheet, photo left as a slot
# ---------------------------------------------------------------------------

def screen(fig, x, y, w, h, gid, title, en):
    fig.g(gid)
    fig.rect(x, y, w, h, "#141714")
    fig.text(x + 16, y + 28, title, 16, "#F3EFE6", "zh")
    fig.text(x + 16, y + 48, en, 11, "#A39A8C", "en", ls=1)
    fig.ge()


def fig06(p156, p172):
    W, H = 1600, 1080
    fig = Fig(W, H)
    meta(fig, "FIG. 6", "EXHIBITION INTERFACE")
    header_title(fig, "界面", "Three views the page already draws. The photograph is a frame, so it stays editable.")
    # front: both saved picks, full width of the cloth
    fig.g("view-front")
    fig.rect(56, 200, 1488, 168, "#141714")
    fig.text(72, 224, "正面", 15, "#F3EFE6", "zh")
    fig.text(130, 224, "FRONT", 11, "#A39A8C", "en", ls=1.2)
    cloth_pick(fig, 72, 244, 8, 156, p156["cov"], p156["st"], show_n=N)
    cloth_pick(fig, 72, 292, 8, 172, p172["cov"], p172["st"], show_n=N)
    fig.text(1492, 252, "156", 11, "#A39A8C", "mono")
    fig.text(1492, 300, "172", 11, "#A39A8C", "mono")
    fig.ge()
    # layers of pick 172, full cloth
    fig.g("view-layers")
    fig.rect(56, 400, 980, 280, "#141714")
    fig.text(72, 426, "分层", 15, "#F3EFE6", "zh")
    fig.text(130, 426, "LAYERS  ·  PICK 172", 11, "#A39A8C", "en", ls=1.2)
    for i, (key, zh, en, color, fl, light) in enumerate(LAYERS):
        yy = 448 + i * 30
        poster_row(fig, 72, yy, p172["cov"][i], 5, color, "#141714" if light else None, rule=False)
        fig.text(968, yy + 12, zh, 12, "#F3EFE6", "zh")
    fig.ge()
    # one layer
    fig.g("view-one")
    fig.rect(1060, 400, 484, 280, "#141714")
    fig.text(1076, 426, "一层", 15, "#F3EFE6", "zh")
    fig.text(1136, 426, "TIDE", 11, "#A39A8C", "en", ls=1.2)
    bits = p172["cov"][BY["hydro"]]
    S = p172["layers"][BY["hydro"]]["S"]
    fig.line(1076, 478, 1488, 478, "#3C4338", 3)
    for a, ln in runs_of(bits, 8):
        fig.rect(1076 + a / N * 412, 470, max(2, ln / N * 412), 14, "#4FB0BE")
    fig.line(1076 + band_x(S) / N * 412, 460, 1076 + band_x(S) / N * 412, 496, "#F3EFE6", 1)
    cuts = [(a, ln) for a, ln in runs_of(bits, 8) if ln > 1]
    gaps = max(0, len(cuts) - 1) * 8
    cw = min(22, (400 - gaps) / max(1, sum(ln for _, ln in cuts)))
    total = sum(ln for _, ln in cuts) * cw + gaps
    ox = 1076 + max(0, (400 - total) / 2)
    oy = 530
    cursor = 0
    for a, ln in cuts:
        draw_satin(fig, ox + cursor, oy, ln, 1, cw, j0=172, i0=a, gap=0.8)
        fig.rect(ox + cursor + 2, oy + 4, ln * cw - 6, cw - 8, "#4FB0BE")
        fig.text(ox + cursor + ln * cw / 2, oy + cw + 18, str(ln), 12, "#F3EFE6", "mono", anchor="middle")
        cursor += ln * cw + 8
    fig.text(1076, 620, f"S {S:.2f}    float 8    pick 172", 13, "#F3EFE6", "mono")
    fig.text(1076, 642, "where this layer sits on the cloth, then the floats", 12, "#A39A8C", "en")
    fig.ge()
    fig.g("photo-slot")
    fig.rect(56, 720, 720, 300, "none", INK, 1)
    fig.line(56, 720, 776, 1020, HAIR, 1)
    fig.line(776, 720, 56, 1020, HAIR, 1)
    fig.text(416, 860, "booth_table.jpg", 16, INK, "mono", anchor="middle", ls=1)
    fig.text(416, 888, "Drop the photograph into this frame.", 13, MUTED, "en", anchor="middle")
    fig.ge()
    fig.g("photo-notes")
    notes = [
        "The monitor shows the separated layers.",
        "A camera sits on the monitor.",
        "No treadle is in the photograph.",
        "Printed sheets lie on the table.",
        "Gesture changes the view.",
        "Gesture writes no strand.",
        "Sound writes no strand.",
    ]
    for i, s in enumerate(notes):
        fig.text(820, 760 + i * 32, s, 15, INK, "en")
    fig.ge()
    foot(fig, "Both rows of the front view are saved picks, all 176 ends. The exhibition stacked a longer cloth than these two.")
    fig.save("fig06_interface.svg")


# ---------------------------------------------------------------------------
# Figure 7 — participation, the rule drawn
# ---------------------------------------------------------------------------

def gauss_bits(S, v, human=False, n=48):
    c = SEL + 2 + S * (N - 2 * SEL - 4)
    w = (3 + 5 * v) if human else (2.4 + 9 * v)
    bits = []
    for i in range(n):
        d = math.exp(-((i - c) ** 2) / (2 * w * w)) * (0.62 + 0.38 * v)
        bits.append("1" if d > 0.5 else "0")
    return "".join(bits)


def fig07():
    W, H = 1600, 560
    fig = Fig(W, H)
    meta(fig, "FIG. 7", "TREADLE")
    header_title(fig, "踩踏", "Drawn from the rule. This is not a saved press.")
    # a column of picks: 2 feeding, the press, 8 startled
    fig.g("sequence")
    cell = 8
    x, y = 56, 210
    n = 140  # ends 0–139 cover the shore and the feeding position
    step = cell + 7
    for r in range(11):
        yy = y + r * step
        draw_satin(fig, x, yy, n, 1, cell, j0=r, i0=0, gap=0.35)
        feeding = r <= 2
        bird = gauss_bits(0.54 if feeding else 0.07, 0.75 if feeding else 0.25, n=n)
        tide = gauss_bits(0.58, 0.55, n=n)
        for i in range(n):
            if bird[i] == "1":
                fig.rect(x + i * cell + 0.4, yy + 1.4, cell - 1.4, cell * 0.62, "#EFE7D6", INK, 0.45)
            if tide[i] == "1":
                fig.rect(x + i * cell + 0.4, yy + 2.4, cell - 1.4, cell * 0.42, "#4FB0BE")
        if feeding:
            marked = False
            for i in range(n):
                if bird[i] == "1" and tide[i] == "1":
                    cx = x + i * cell + cell / 2
                    cy = yy + cell / 2
                    fig.line(cx - 2.4, cy - 2.4, cx + 2.4, cy + 2.4, INK, 1)
                    fig.line(cx + 2.4, cy - 2.4, cx - 2.4, cy + 2.4, MADDER, 1)
                    marked = True
                    break
            if not marked:
                pass
        if r == 2:
            hum = gauss_bits(0.42, 0.9, human=True, n=n)
            for i in range(n):
                if hum[i] == "1":
                    fig.rect(x + i * cell + 0.8, yy + 0.8, cell - 1.6, cell - 1.6, MADDER)
    fig.text(x + n * cell + 14, y + 10, "feeding", 12, INK, "mono", ls=0.5)
    fig.text(x + n * cell + 14, y + 2 * step + 10, "press", 12, MADDER, "mono", ls=0.5)
    fig.line(x + n * cell + 8, y + 3 * step, x + n * cell + 8, y + 10 * step + cell, INK, 1)
    fig.text(x + n * cell + 14, y + 6 * step + 8, "8 picks", 12, INK, "mono", ls=0.5)
    fig.text(x, y + 11 * step + 18, "岸", 12, MUTED, "zh")
    fig.text(x + band_x(0.58) * cell, y + 11 * step + 18, "潮", 12, "#4FB0BE", "zh", anchor="middle")
    fig.ge()
    fig.g("rule")
    ry = y + 11 * step + 52
    fig.text(56, ry, "v = clamp(0.3 + hold / 1400, 0.3, 1)", 14, INK, "mono")
    fig.text(560, ry, "after the press:  S = 0.07    v = 0.25    feed stitches dropped", 14, INK, "mono")
    fig.text(56, ry + 24, "The press pick keeps the feeding stitch. The next eight picks move the spoonbill to the shore.", 13, MUTED, "en")
    fig.ge()
    foot(fig, "S of the visitor strand is hashed from the press count. The red band's place in this drawing is not a measured position.")
    fig.save("fig07_participation.svg")


# ---------------------------------------------------------------------------
# Table 1 — index, one line
# ---------------------------------------------------------------------------

def table01():
    W, H = 1600, 780
    fig = Fig(W, H)
    meta(fig, "TABLE 1", "SEVEN AGENTS")
    header_title(fig, "代理", "One line each. The section in Figure 1 is the same list, drawn.")
    heads = [(56, ""), (120, "AGENT"), (340, "PROXY"), (560, "SOURCE"), (900, "OWN PERIOD"), (1180, "FLOAT")]
    fig.g("columns")
    for x, h in heads:
        fig.text(x, 210, h, 11, MUTED, "mono", ls=1.2)
    fig.line(56, 224, 1544, 224, INK, 1)
    rows = [
        ("atmos", "CO₂  ppm", "CAMS", "1 year", "15 min"),
        ("plant", "light  W/m²", "Open-Meteo", "1 day", "15 min"),
        ("animal", "presence", "iNaturalist", "1 year", "15 min"),
        ("hydro", "level  m", "Open-Meteo Marine", "12.42 h", "15 min"),
        ("litho", "magnitude", "USGS", "event", "15 min, or blank"),
        ("tech", "jitter", "this machine", "1 s", "15 min"),
        ("human", "hold", "treadle", "—", "the press"),
    ]
    for i, (key, proxy, source, period, pick) in enumerate(rows):
        zh, en, color, fl, light = (
            yarn_of(key)[1],
            yarn_of(key)[2],
            yarn_of(key)[3],
            yarn_of(key)[4],
            yarn_of(key)[5],
        )
        yy = 250 + i * 64
        fig.rect(56, yy - 18, 8, 36, color, INK if light else "none", 0.5)
        fig.text(120, yy, zh, 20, INK, "zh")
        fig.text(120, yy + 20, en, 12, MUTED, "en", ls=0.6)
        fig.text(340, yy + 6, proxy, 15, INK, "mono")
        fig.text(560, yy + 6, source, 15, INK, "en")
        fig.text(900, yy + 6, period, 15, INK, "mono")
        fig.text(1180, yy + 6, str(fl), 20, INK, "mono")
        fig.text(1260, yy + 6, pick, 13, MUTED, "mono")
        fig.line(56, yy + 36, 1544, yy + 36, HAIR, 1)
    fig.ge()
    foot(fig, "On the mudflat clock every agent except the visitor advances 15 minutes a pick. Own period is the intrinsic cycle. Earthquakes, not mud.")
    fig.save("table01_agents.svg")


# ---------------------------------------------------------------------------
# Table 2 — rules as marks
# ---------------------------------------------------------------------------

def pair(fig, x, y, c1, c2, broken=False):
    fig.rect(x, y, 18, 18, c1, INK if c1 in ("#EFE7D6", "#C9CDD6") else "none", 0.6)
    if broken:
        fig.line(x + 26, y + 9, x + 40, y + 9, INK, 1, "2 2")
    else:
        fig.line(x + 24, y + 2, x + 42, y + 16, INK, 1.2)
        fig.line(x + 42, y + 2, x + 24, y + 16, MADDER, 1.2)
    fig.rect(x + 48, y, 18, 18, c2, INK if c2 in ("#EFE7D6", "#C9CDD6") else "none", 0.6)


def table02():
    W, H = 1600, 860
    fig = Fig(W, H)
    meta(fig, "TABLE 2", "RELATIONS")
    header_title(fig, "关系", "The condition is the test in the prototype. The mark is what it writes.")
    rules = [
        ("feed", "animal", "hydro", False, "ln < 0.42    presence > 0.3    no wind or rain"),
        ("roost", "animal", "plant", False, "not feeding    ln > 0.7    presence > 0.3"),
        ("submerge", "plant", "hydro", False, "water edge < 0.27     edge = 0.9 − 0.74 ln"),
        ("draw", "plant", "atmos", False, "shortwave > 250 W/m²    CO₂ below the 96-pick mean"),
        ("disturb", "atmos", "hydro", True, "wind > 30 km/h  or  rain > 2 mm/h     jolt is kept"),
        ("jolt", "litho", "tech", False, "strongest M ≥ 4 in the 15 min window, within 2500 km"),
        ("press", "human", "human", False, "v = clamp(0.3 + hold/1400, 0.3, 1)"),
    ]
    fig.g("rules")
    for i, (name, a, b, broken, cond) in enumerate(rules):
        yy = 210 + i * 78
        fig.text(56, yy + 16, f"0{i+1}", 12, MUTED, "mono", ls=1)
        if name == "jolt":
            cols = ["#EFE7D6", "#8FA6C6", "#B06A3C", "#B4BC57", "#4FB0BE", "#C9CDD6"]
            for k, c in enumerate(cols):
                fig.rect(120 + k * 16, yy, 12, 18, c, INK if c in ("#EFE7D6", "#C9CDD6") else "none", 0.4)
            fig.text(230, yy + 14, "× 5 pairs", 12, MUTED, "mono")
        elif name == "press":
            fig.rect(120, yy, 18, 18, MADDER)
        else:
            pair(fig, 120, yy, yarn_of(a)[3], yarn_of(b)[3], broken)
        fig.text(360, yy + 6, name.upper(), 14, INK, "mono", ls=1.4)
        fig.text(360, yy + 30, cond, 15, INK, "mono")
        fig.line(56, yy + 52, 1544, yy + 52, HAIR, 1)
    fig.ge()
    foot(fig, "Disturbance removes ordinary stitches for that pick. Jolt writes 28 × 5 stitches and does not include the visitor. ln is tide normalised on the 480-pick score.")
    fig.save("table02_rules.svg")


def main():
    p156 = load_pick("pick_156.json")
    p172 = load_pick("pick_172.json")
    fig01(p156)
    fig02(p156)
    fig03()
    fig04(p156)
    fig05(p156, p172)
    fig06(p156, p172)
    fig07()
    table01()
    table02()
    print("wrote svgs")


if __name__ == "__main__":
    main()
