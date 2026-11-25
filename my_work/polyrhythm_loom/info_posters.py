"""A2 information posters in the visual system of the main Polyrhythm Loom poster.

Sentences are shortened from the student's paper and pictorial. They are not new claims.
"""

from pathlib import Path

W, H = 1240, 1754
GROUND = "#070C12"
LIME = "#D8E272"
WHITE = "#FFFDF4"
INK = "#F3F0E6"
MUTED = "#9AA196"
DIM = "#6E746C"
MADDER = "#D24E35"

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "V": ["10001", "10001", "10001", "10001", "01010", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
}


def hx(*ns):
    n = 2166136261
    for x in ns:
        n ^= int(x) & 0xFFFFFFFF
        n = (n * 16777619) & 0xFFFFFFFF
    return n


def rect(x, y, w, h, fill, opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{op}/>'


def pixel_word(text, x, y, cell=5, gap=1.6, fill=LIME):
    parts = []
    step = cell + gap
    cursor = x
    for glyph in text:
        bits = FONT[glyph]
        for r, row in enumerate(bits):
            for c, bit in enumerate(row):
                if bit == "1":
                    parts.append(rect(cursor + c * step, y + r * step, cell, cell, fill))
        cursor += 5 * step + step * 1.6
    width = cursor - x - step * 1.6
    return parts, width, 7 * step - gap


def block_num(text, x, y, cell=20, gap=5):
    parts = []
    step = cell + gap
    cursor = x
    for li, glyph in enumerate(text):
        bits = FONT[glyph]
        for r, row in enumerate(bits):
            for c, bit in enumerate(row):
                if bit != "1":
                    continue
                color = LIME if (r + c + li) % 3 == 0 else WHITE
                parts.append(rect(cursor + c * step, y + r * step, cell, cell, color))
        cursor += 5 * step + gap * 2
    width = cursor - x - gap * 2
    height = 7 * step - gap
    # a ground-colored cut through the digits only, like the scan on the main title
    cut_y = y + 3 * step - 1
    parts.append(rect(x - 2, cut_y, width + 4, 6, GROUND))
    parts.append(rect(x - 2, cut_y + 8, width * 0.42, 2, LIME))
    return parts, width, height


def ground():
    parts = [rect(0, 0, W, H, GROUND)]
    for y in range(0, H, 4):
        tone = 14 + (y // 4 % 7)
        parts.append(rect(0, y, W, 1, f"#{tone:02x}{tone+6:02x}{tone+12:02x}", 0.45))
    for i in range(26):
        y = 30 + hx(i, 1) % (H - 60)
        x = hx(i, 2) % 700
        w = 90 + hx(i, 3) % 460
        colors = ("#16343C", "#243024", "#3C4424", "#1A2836", "#2A2418")
        parts.append(rect(x, y, w, 2 + hx(i, 4) % 2, colors[i % 5], 0.38))
    for i in range(70):
        x = 20 + hx(i, 5) % (W - 40)
        y = 20 + hx(i, 6) % (H - 40)
        fill = LIME if i % 5 == 0 else WHITE
        parts.append(rect(x, y, 2.2, 2.2, fill, 0.35))
    return parts


def header(n):
    parts, _, _ = pixel_word("WEAVING", 68, 58, cell=4.2, gap=1.5, fill=LIME)
    parts.append(
        '<text class="mono" x="1172" y="72" text-anchor="end">COTAI MUDFLAT</text>'
    )
    parts.append(
        '<text class="mono" x="1172" y="92" text-anchor="end">MACAU</text>'
    )
    parts.append(
        f'<text class="mono" x="1172" y="118" text-anchor="end">0{n}  /  03</text>'
    )
    return parts


def footer():
    parts = [
        rect(68, 1668, 18, 46, LIME),
        rect(68, 1696, 46, 18, LIME),
        '<text class="zh" x="132" y="1688">澳门大学</text>',
        '<text class="en small" x="132" y="1712">SHIYU LEI  ·  2026</text>',
    ]
    word, _, _ = pixel_word("WITH", 1048, 1664, cell=4.2, gap=1.5, fill=LIME)
    parts.extend(word)
    return parts


def title(zh, en, y):
    return [
        f'<text class="title" x="68" y="{y}">{zh}</text>',
        f'<text class="kicker" x="68" y="{y+36}">{en}</text>',
    ], y + 64


STYLE = """<style>
text{font-family:"Noto Sans SC","PingFang SC",sans-serif;fill:#F3F0E6}
.title{font-size:52px;font-weight:500;letter-spacing:0.04em;fill:#FFFDF4}
.kicker{font-family:Archivo,"Noto Sans SC",sans-serif;font-size:16px;letter-spacing:0.22em;fill:#D8E272}
.zh{font-size:24px;font-weight:500;fill:#F3F0E6}
.zh sm,.sub{font-size:20px;font-weight:400;fill:#F3F0E6}
.en{font-family:Archivo,"Noto Sans SC",sans-serif;font-size:15px;letter-spacing:0.01em;fill:#9AA196}
.en.small{font-size:13px;letter-spacing:0.14em}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13px;letter-spacing:0.16em;fill:#9AA196}
.label{font-size:22px;font-weight:500;fill:#FFFDF4}
.note{font-size:18px;fill:#F3F0E6}
</style>"""


def wrap(body, name):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{STYLE}
{"".join(body)}
</svg>'''


def icon_one_thread(x, y):
    return [
        rect(x, y + 70, 210, 10, LIME),
        rect(x + 18, y + 88, 64, 3, WHITE, 0.7),
        rect(x, y + 48, 36, 3, LIME, 0.35),
    ]


def icon_scatter(x, y):
    parts = []
    spots = [
        (0, 18, 54, 8), (70, 46, 28, 8), (120, 8, 70, 8),
        (20, 78, 40, 8), (96, 96, 86, 8), (40, 130, 22, 8),
        (150, 64, 48, 8), (8, 156, 76, 8), (110, 150, 34, 8),
    ]
    for i, (dx, dy, w, h) in enumerate(spots):
        fill = LIME if i % 2 == 0 else WHITE
        parts.append(rect(x + dx, y + dy, w, h, fill, 0.85))
    return parts


def icon_cloth(x, y):
    parts = []
    for i in range(6):
        parts.append(rect(x, y + 16 + i * 24, 230, 10, WHITE if i % 2 else LIME))
    for k in range(5):
        parts.append(rect(x + 18 + k * 42, y + 6, 8, 150, "#0C1218"))
    parts.append(rect(x + 100, y + 64, 22, 22, LIME))
    return parts


def icon_raw(x, y):
    parts = []
    for i in range(16):
        parts.append(rect(x + hx(i, 7) % 100, y + 8 + hx(i, 8) % 72, 8, 8, LIME if i % 3 else WHITE, 0.85))
    return parts


def icon_simple(x, y):
    parts = [rect(x, y + 96, 120, 1, DIM)]
    heights = [78, 70, 46, 24, 16, 30, 52, 72, 60, 40]
    for i, ht in enumerate(heights):
        parts.append(rect(x + i * 12, y + ht, 8, 96 - ht, LIME if i % 2 == 0 else WHITE))
    return parts


def icon_score(x, y):
    parts = []
    for i in range(16):
        parts.append(rect(x + i * 8, y + 28 + (i * 13 % 40), 5, 36, LIME if i % 3 else WHITE))
    return parts


def icon_draft(x, y):
    parts = []
    for r in range(8):
        for c in range(8):
            on = (3 * c - r) % 8 < 3
            if on:
                parts.append(rect(x + c * 14, y + r * 12, 10, 8, LIME if (r + c) % 4 == 0 else WHITE))
    return parts


def icon_textile(x, y):
    parts = []
    for i in range(7):
        parts.append(rect(x, y + 8 + i * 13, 118, 7, LIME if i % 2 == 0 else WHITE))
        parts.append(rect(x + 10 + i * 16, y + 2, 7, 96, "#101820" if i % 2 else LIME))
    parts.append(rect(x + 72, y + 34, 28, 6, MADDER))
    return parts


def icon_clock(x, y):
    parts = []
    for i, lv in enumerate((34, 36, 32, 8, 38, 35)):
        fill = LIME if i == 3 else "#243028"
        base = y + 8 + i * 20
        parts.append(rect(x, base, 270, 7, fill))
        if i == 3:
            for k, h in enumerate((10, 22, 6, 26, 12, 4, 18)):
                parts.append(rect(x + 12 + k * 36, base - h, 12, h, LIME))
    return parts


def icon_apart(x, y):
    parts = []
    spots = [(0, 4), (92, 22), (176, 0), (28, 78), (124, 96), (210, 70)]
    for i, (dx, dy) in enumerate(spots):
        parts.append(rect(x + dx, y + dy, 52, 34, "#141C18"))
        parts.append(rect(x + dx + 8, y + dy + 14, 36, 6, LIME if i % 2 == 0 else WHITE))
    return parts


def icon_cross(x, y):
    parts = []
    for i in range(6):
        parts.append(rect(x, y + 14 + i * 20, 270, 8, WHITE if i % 2 else LIME))
    for i in range(5):
        parts.append(rect(x + 16 + i * 50, y + 4, 8, 128, "#0C1218"))
    parts.append(rect(x + 116, y + 54, 24, 24, LIME))
    return parts


def lines(items, x, y, cls, leading):
    parts = []
    for i, text in enumerate(items):
        parts.append(f'<text class="{cls}" x="{x}" y="{y + i * leading}">{text}</text>')
    return parts


def poster_origin():
    body = ground() + header(1)
    body += title("这个系统从哪来", "WHERE IT CAME FROM", 188)[0]
    rows = [
        ("01", "听海", [
            "一张水听器，萨利希海。",
            "船的噪声盖过虎鲸。很远，只有一个源。",
        ], ["One hydrophone, Salish Sea. Ship noise over orca calls.", "Far away, and only one source."], icon_one_thread),
        ("02", "散开的数据", [
            "各处拼来的数据，",
            "读起来像互不相关的频率。",
        ], ["Scattered datasets.", "A patchwork of unrelated frequencies."], icon_scatter),
        ("03", "路氹泥滩", [
            "一个能走到、能自己采样的地方。",
            "下滩要等退潮。潮决定这一天，",
            "也在布上留下一条脊。",
        ], ["A place we can visit and sample.", "Low tide sets the day, and a ridge in the cloth."], icon_cloth),
    ]
    y = 290
    for num, label, zh, en, icon in rows:
        parts, nw, _ = block_num(num, 68, y, cell=16, gap=4)
        body += parts
        tx = 68 + nw + 40
        body.append(f'<text class="label" x="{tx}" y="{y + 32}">{label}</text>')
        body += lines(zh, tx, y + 74, "sub", 32)
        body += lines(en, tx, y + 74 + 32 * len(zh) + 10, "en", 22)
        body += icon(960, y + 8)
        y += 300
    decisions = [
        ("同一只钟", "慢的没有错，只是看不见。", "Not wrong. Invisible."),
        ("各占一条经", "清楚，但并排，不相遇。", "Legible, and apart."),
        ("七个里的一个", "踏板是一声，不是总开关。", "One voice, not the control."),
    ]
    y = 1388
    body.append(rect(68, y, 1104, 1, LIME, 0.45))
    x = 68
    for label, zh, en in decisions:
        body.append(f'<text class="label" x="{x}" y="{y + 46}">{label}</text>')
        body.append(f'<text class="note" x="{x}" y="{y + 82}">{zh}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 110}">{en}</text>')
        x += 380
    body += footer()
    return wrap(body, "origin")


def poster_pipeline():
    body = ground() + header(2)
    body += title("从数据到编织", "FROM DATA TO WEAVING", 168)[0]
    stages = [
        ("01", "原始", "单位、采样和缺口混在一起。", "Mixed units, rates and gaps.", icon_raw),
        ("02", "拆开", "趋势、周期、剩余，收到 0–1。", "Trend, cycle, residual. Scaled to 0–1.", icon_simple),
        ("03", "织谱", "同一份数据，按两只钟重采样成纬。", "Resampled to picks, under both clocks.", icon_score),
        ("04", "纹板", "每一纬一行 0 和 1。", "One row of 0s and 1s per pick.", icon_draft),
        ("05", "同一张布", "屏幕能读，提花机也能读。", "The screen, and a jacquard loom.", icon_textile),
    ]
    y = 270
    for num, label, zh, en, icon in stages:
        body += pixel_word(num, 68, y + 18, cell=7, gap=2.2, fill=LIME)[0]
        body += icon(214, y + 2)
        body.append(f'<text class="label" x="380" y="{y + 36}">{label}</text>')
        body.append(f'<text class="sub" x="380" y="{y + 70}">{zh}</text>')
        body.append(f'<text class="en" x="380" y="{y + 98}">{en}</text>')
        y += 132
    body.append(rect(68, y + 6, 1104, 1, LIME, 0.45))
    body.append(f'<text class="note" x="68" y="{y + 44}">每一步都故意丢掉一些。丢掉的是翻译，不是要藏的误差。</text>')
    body.append(f'<text class="en" x="68" y="{y + 70}">Each stage drops detail on purpose. The loss is the translation.</text>')
    parts, nw, _ = block_num("24", 68, y + 100, cell=15, gap=4)
    body += parts
    tx = 68 + nw + 36
    body.append(f'<text class="label" x="{tx}" y="{y + 148}">每个周期 24 纬</text>')
    body.append(f'<text class="sub" x="{tx}" y="{y + 184}">没有谁的钟是标准。日光的一纬，正好一小时。</text>')
    body.append(f'<text class="en" x="{tx}" y="{y + 214}">Every cycle is 24 picks. No clock is the standard.</text>')
    agents = [
        ("CO₂", "一年 · 一纬 15 天"),
        ("日光", "一天 · 一纬 1 小时"),
        ("黑脸琵鹭", "越冬 · 一纬 15 天"),
        ("潮", "12.4 小时 · 一纬 31 分"),
        ("泥", "周期未定"),
        ("设备", "1 秒 · 一纬 0.04 秒"),
        ("访客", "踩一次 · 不记个人信息"),
    ]
    ay = y + 280
    body.append(f'<text class="mono" x="68" y="{ay}">SEVEN AGENTS</text>')
    for i, (name, meta) in enumerate(agents):
        col = i % 2
        row = i // 2
        x = 68 + col * 560
        yy = ay + 36 + row * 32
        body.append(f'<text class="note" x="{x}" y="{yy}">{name}</text>')
        body.append(f'<text class="en" x="{x + 150}" y="{yy}">{meta}</text>')
    body.append('<text class="en" x="68" y="1616">设备和访客是现场的。其余五条按来源建模，之后换成实测。</text>')
    body.append('<text class="en" x="68" y="1640">The device and the visitor run live. The other five are modelled, and will be measured.</text>')
    body += footer()
    return wrap(body, "pipeline")


def poster_relation():
    body = ground() + header(3)
    body += title("数据作为关系", "DATA AS RELATION", 176)[0]
    body.append('<text class="sub" x="68" y="300">图把值放在轴上。布把所有线留在一起，一纬一纬往前。</text>')
    body.append('<text class="en" x="68" y="328">A chart places values on axes. A cloth holds every thread, and advances one pick at a time.</text>')
    rows = [
        ("01", "共用一只钟", [
            "对齐了，没有分开。",
            "慢的摊成线，快的糊成噪声。",
        ], ["Aligns without separating.", "The slow flatten. The fast blur."], icon_clock),
        ("02", "各自一幅", [
            "分开了，没有对齐。",
            "形状还在，彼此没了。",
        ], ["Separates without aligning.", "Each keeps its shape. The relation is gone."], icon_apart),
        ("03", "分开，再对齐", [
            "各用自己的周期，每个周期同样 24 纬。",
            "交叉的地方，关系才成立。",
        ], ["Each by its own cycle, the same 24 picks.", "Where threads cross, a relation is made."], icon_cross),
    ]
    y = 390
    for num, label, zh, en, icon in rows:
        parts, nw, _ = block_num(num, 68, y, cell=15, gap=4)
        body += parts
        tx = 68 + nw + 36
        body.append(f'<text class="label" x="{tx}" y="{y + 34}">{label}</text>')
        body += lines(zh, tx, y + 76, "sub", 32)
        body += lines(en, tx, y + 76 + 32 * len(zh) + 8, "en", 22)
        body += icon(860, y + 8)
        y += 310
    body.append(rect(68, 1404, 1104, 1, LIME, 0.45))
    body.append('<text class="label" x="68" y="1456">一次交叉不是同一时刻。</text>')
    body.append('<text class="sub" x="68" y="1496">同一份数据织两段，两段停在同一个瞬间。</text>')
    body.append('<text class="en" x="68" y="1530">A crossing is not the same moment. Two sections of one cloth, ending together.</text>')
    body += footer()
    return wrap(body, "relation")


def main():
    root = Path("/Users/leilei/Desktop/Cusor/my_work/polyrhythm_loom")
    files = {
        "info_01_origin.svg": poster_origin(),
        "info_02_pipeline.svg": poster_pipeline(),
        "info_03_relation.svg": poster_relation(),
    }
    for name, svg in files.items():
        (root / name).write_text(svg)
        print(name, len(svg))
    svgs = "\n".join(
        f'<section id="{name}">{svg}</section>' for name, svg in files.items()
    )
    html = f'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>信息海报 · Polyrhythm Loom</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500&display=swap">
<style>
body {{ margin: 0; background: #141816; }}
section {{ width: 1240px; margin: 32px auto; }}
svg {{ display: block; width: 1240px; height: auto; }}
</style>
</head>
<body>
{svgs}
</body>
</html>'''
    (root / "info_posters.html").write_text(html)


if __name__ == "__main__":
    main()
