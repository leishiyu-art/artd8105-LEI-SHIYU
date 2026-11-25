"""Nine 1920×1080 slides as Figma-editable SVG. Cloths stay linked, not embedded."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
W, H = 1920, 1080
SANS = "'PingFang SC', 'Noto Sans SC', Helvetica, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, monospace"
ARCH = "Archivo, Helvetica, sans-serif"
LIME, WHITE, INK, MUTED = "#D8E272", "#FFFDF4", "#F3F0E6", "#9AA196"
GROUND, MADDER = "#070C12", "#D24E35"
CLOTH = "../../paper/figures/patterns"

FONT = {
    "A": "01110,10001,10001,11111,10001,10001,10001",
    "C": "01111,10000,10000,10000,10000,10000,01111",
    "E": "11111,10000,10000,11110,10000,10000,11111",
    "G": "01111,10000,10000,10111,10001,10001,01110",
    "H": "10001,10001,10001,11111,10001,10001,10001",
    "I": "11111,00100,00100,00100,00100,00100,11111",
    "N": "10001,11001,10101,10011,10001,10001,10001",
    "T": "11111,00100,00100,00100,00100,00100,00100",
    "V": "10001,10001,10001,10001,01010,01010,00100",
    "W": "10001,10001,10001,10101,10101,11011,10001",
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def px(word, cell=4.2, gap=1.5):
    step = cell + gap
    parts, x = [], 0
    for g in word:
        for r, row in enumerate(FONT[g].split(",")):
            for c, bit in enumerate(row):
                if bit == "1":
                    parts.append(
                        f'<rect x="{x + c * step:.1f}" y="{r * step:.1f}" width="{cell}" height="{cell}" fill="{LIME}"/>'
                    )
        x += 5 * step + step * 1.6
    h = 7 * step - gap
    return f'<g id="pixel-{word}">{"".join(parts)}</g>', x, h


def t(x, y, s, size, fill, font, spacing=0, anchor="start", weight=500):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    anc = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}"'
        f'{ls}{anc} dominant-baseline="hanging" font-family="{font}">{esc(s)}</text>'
    )


def chrome(n, title, kicker, body, title_size=56):
    weaving, _, _ = px("WEAVING")
    with_, ww, wh = px("WITH", 3.2)
    meta = (
        f'<text x="1848" y="36" fill="{MUTED}" font-size="12" font-weight="500" letter-spacing="2.1" '
        f'text-anchor="end" dominant-baseline="hanging" font-family="{MONO}">'
        f'<tspan x="1848">COTAI MUDFLAT</tspan>'
        f'<tspan x="1848" dy="20">MACAU</tspan>'
        f'<tspan x="1848" dy="20">{n:02d}  /  09</tspan></text>'
    )
    head = f'<g id="header">{weaving}<g transform="translate(72,36)">{weaving}</g>{meta}</g>'
    # weaving was included twice; rebuild cleanly below
    return head, with_, ww, wh, title, kicker, body, title_size


def frame(n, title, kicker, body, title_size=56, extra=""):
    weaving, _, _ = px("WEAVING")
    with_, ww, _ = px("WITH", 3.2)
    meta = (
        f'<text x="1848" y="36" fill="{MUTED}" font-size="12" font-weight="500" letter-spacing="2.1" '
        f'text-anchor="end" dominant-baseline="hanging" font-family="{MONO}">'
        f'<tspan x="1848">COTAI MUDFLAT</tspan>'
        f'<tspan x="1848" dy="20">MACAU</tspan>'
        f'<tspan x="1848" dy="20">{n:02d}  /  09</tspan></text>'
    )
    titles = ""
    if title:
        titles = (
            f'<g id="title">'
            f'{t(72, 112, title, title_size, WHITE, SANS, 3)}'
            f'{t(72, 112 + title_size + 16, kicker, 15, LIME, ARCH, 3.3, weight=400)}'
            f'</g>'
        )
    footer = (
        f'<g id="footer">'
        f'<rect x="72" y="1024" width="8" height="28" fill="{LIME}"/>'
        f'<rect x="72" y="1044" width="28" height="8" fill="{LIME}"/>'
        f'{t(114, 1024, "澳门大学", 16, INK, SANS)}'
        f'{t(114, 1048, "SHIYU LEI  ·  2026", 11, MUTED, ARCH, 1.6, weight=400)}'
        f'<g transform="translate({1848 - ww:.1f},1026)">{with_}</g>'
        f'</g>'
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <g id="ground">
    <rect width="{W}" height="{H}" fill="{GROUND}"/>
    <rect width="{W}" height="{H}" fill="url(#scan)"/>
    <rect width="{W}" height="220" fill="url(#wash)"/>
  </g>
  {extra}
  <g id="header"><g transform="translate(72,36)">{weaving}</g>{meta}</g>
  {titles}
  {body}
  {footer}
  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect y="3" width="4" height="1" fill="#ffffff" fill-opacity="0.035"/>
    </pattern>
    <linearGradient id="wash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
  </defs>
</svg>
'''


def save(n, name, svg):
    path = OUT / f"slide_{n:02d}_{name}.svg"
    path.write_text(svg, encoding="utf-8")
    print(path.name, path.stat().st_size)


def slide_01():
    rows = [
        ("#4FB0BE", "12.4 h", "潮"),
        ("#B4BC57", "1 day", "红树"),
        ("#8FA6C6", "1 year", "大气 · 琵鹭"),
        ("#B06A3C", "event", "地震"),
        ("#D24E35", "press", "观众"),
    ]
    y = 430
    lines = []
    for color, num, name in rows:
        lines.append(t(72, y, num, 54, color, MONO))
        lines.append(t(400, y + 16, name, 22, INK, SANS, 5))
        y += 78
    ask = (
        f'{t(72, 214, "潮、一年、一次地震、踩下去的一下。", 22, INK, SANS, 0.8, weight=400)}'
        f'{t(72, 250, "Have you thought about what lies beyond the human time scale?", 16, MUTED, ARCH, 0.6, weight=400)}'
    )
    body = f'<g id="question">{ask}</g><g id="scales">{"".join(lines)}</g>'
    save(1, "beyond", frame(1, "超出人的时间尺度", "BEYOND HUMAN TIME", body))


def slide_02():
    drawing = '''
      <rect width="760" height="460" fill="#10151c"/>
      <rect width="760" height="150" fill="#15202c"/>
      <rect y="210" width="760" height="250" fill="#1a2216"/>
      <polygon points="500,188 760,214 760,460 455,460" fill="#102830"/>
      <line x1="478" y1="168" x2="455" y2="460" stroke="#FFFDF4" stroke-width="1.5" stroke-dasharray="1 7"/>
      <rect x="40" y="52" width="680" height="8" fill="#8FA6C6"/>
      <g fill="#C5CC78">
        <rect x="56" y="132" width="16" height="16"/><rect x="76" y="132" width="16" height="16"/><rect x="96" y="132" width="16" height="16"/>
        <rect x="66" y="152" width="16" height="16"/><rect x="86" y="152" width="16" height="16"/>
        <rect x="156" y="118" width="16" height="16"/><rect x="176" y="118" width="16" height="16"/><rect x="196" y="118" width="16" height="16"/>
        <rect x="166" y="138" width="16" height="16"/><rect x="186" y="138" width="16" height="16"/>
        <rect x="256" y="140" width="16" height="16"/><rect x="276" y="140" width="16" height="16"/><rect x="296" y="140" width="16" height="16"/>
        <rect x="266" y="160" width="16" height="16"/><rect x="286" y="160" width="16" height="16"/>
        <rect x="348" y="124" width="16" height="16"/><rect x="368" y="124" width="16" height="16"/><rect x="388" y="124" width="16" height="16"/>
        <rect x="358" y="144" width="16" height="16"/><rect x="378" y="144" width="16" height="16"/>
      </g>
      <g fill="#3e4c28">
        <rect x="76" y="168" width="16" height="48"/><rect x="176" y="154" width="16" height="62"/>
        <rect x="276" y="176" width="16" height="44"/><rect x="368" y="160" width="16" height="56"/>
      </g>
      <rect x="70" y="292" width="86" height="8" fill="#EFE7D6"/>
      <rect x="188" y="318" width="48" height="8" fill="#EFE7D6"/>
      <g fill="#4FB0BE">
        <rect x="530" y="300" width="28" height="10"/><rect x="566" y="286" width="36" height="10"/>
        <rect x="610" y="300" width="28" height="10"/><rect x="646" y="274" width="40" height="10"/>
        <rect x="694" y="292" width="28" height="10"/>
      </g>
      <g fill="#B06A3C">
        <rect x="468" y="36" width="8" height="8"/><rect x="468" y="64" width="8" height="8"/>
        <rect x="466" y="120" width="8" height="8"/><rect x="462" y="188" width="8" height="8"/>
        <rect x="458" y="250" width="8" height="8"/><rect x="454" y="320" width="8" height="8"/>
        <rect x="450" y="388" width="8" height="8"/>
      </g>
    '''
    agents = [
        ("#8FA6C6", "大气", "1 year"),
        ("#B4BC57", "红树", "1 day"),
        ("#EFE7D6", "琵鹭", "1 year"),
        ("#4FB0BE", "潮汐", "12.4 h"),
        ("#B06A3C", "地震", "event"),
        ("#C9CDD6", "仪器", "1 s"),
        ("#D24E35", "观众", "press"),
    ]
    rows = []
    y = 250
    for color, name, period in agents:
        rows.append(
            f'<rect x="1288" y="{y}" width="14" height="28" fill="{color}"/>'
            f'{t(1320, y, name, 26, INK, SANS, 3)}'
            f'{t(1848, y + 6, period, 14, MUTED, MONO, 1, "end", 400)}'
            f'<line x1="1288" y1="{y + 58}" x2="1848" y2="{y + 58}" stroke="#ffffff" stroke-opacity="0.1"/>'
        )
        y += 100
    body = (
        f'<g id="section">'
        f'<clipPath id="mapclip"><rect x="72" y="248" width="1148" height="730"/></clipPath>'
        f'<g clip-path="url(#mapclip)"><g transform="translate(40,248) scale(1.55)">{drawing}</g></g>'
        f'{t(88, 938, "岸  SHORE", 13, INK, MONO, 2, weight=500)}'
        f'{t(1188, 938, "水道", 13, LIME, MONO, 2, "end", 500)}'
        f'</g>'
        f'<g id="agents">{"".join(rows)}</g>'
    )
    save(2, "wetland", frame(2, "路氹湿地", "A SPECULATIVE MAP   ·   SEVEN AGENTS", body))


def slide_03():
    pattern = "1001011100101110"
    cell, gap = 56, 8
    label_w, row_gap = 168, 28
    block_w = label_w + row_gap + 16 * cell + 15 * gap
    x0 = (W - block_w) / 2
    y0 = 470
    bits, picks, floats = [], [], []
    x = x0 + label_w + row_gap
    run_n, run_on, run_x = 0, pattern[0] == "1", x
    def flush(n, on, rx):
        w = n * cell + (n - 1) * gap
        if on:
            floats.append(f'<rect x="{rx}" y="{y0 + 196}" width="{w}" height="{cell}" fill="{LIME}"/>')
        return rx + w + gap
    for i, b in enumerate(pattern + "x"):
        on = b == "1"
        if i < 16:
            fill = WHITE if on and i % 5 == 0 else (LIME if on else "none")
            stroke = WHITE if on and i % 5 == 0 else (LIME if on else "rgba(216,226,114,0.28)")
            # SVG stroke does not take rgba in all editors; use opacity
            if on:
                bits.append(f'<rect x="{x}" y="{y0}" width="{cell}" height="{cell}" fill="{fill}"/>')
            else:
                bits.append(f'<rect x="{x}" y="{y0}" width="{cell}" height="{cell}" fill="none" stroke="{LIME}" stroke-opacity="0.28"/>')
            pick = WHITE if on and i % 5 == 0 else (LIME if on else "#1B3A4A")
            picks.append(f'<rect x="{x}" y="{y0 + 98}" width="{cell}" height="{cell}" fill="{pick}"/>')
            x += cell + gap
        if b != "x" and on == run_on:
            run_n += 1
        else:
            run_x = flush(run_n, run_on, run_x)
            run_n, run_on = 1, on
    labels = (
        f'{t(x0, y0 + 4, "二进制", 22, INK, SANS, 3)}'
        f'{t(x0, y0 + 32, "A CELL", 12, LIME, ARCH, 1.8, weight=400)}'
        f'{t(x0, y0 + 102, "一纬", 22, INK, SANS, 3)}'
        f'{t(x0, y0 + 130, "A PICK", 12, LIME, ARCH, 1.8, weight=400)}'
        f'{t(x0, y0 + 204, "浮长", 22, INK, SANS, 3)}'
        f'{t(x0, y0 + 232, "A FLOAT", 12, LIME, ARCH, 1.8, weight=400)}'
    )
    body = f'<g id="binary">{labels}{"".join(bits)}{"".join(picks)}{"".join(floats)}</g>'
    save(3, "binary", frame(3, "为什么是织", "BINARY   ·   TIME SCALE", body))


def image(href, x, y, w, h, clip, ratio="xMidYMid slice", opacity=1):
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return (
        f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
        f'<image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{ratio}" clip-path="url(#{clip})"{op}/>'
    )


def slide_04():
    gap = 22
    avail = 1776 - 2 * gap
    w1 = avail * 1.3 / 3.3
    w3 = avail * 0.7 / 3.3
    y, h = 248, 740
    panels = []
    specs = [
        (72, w1, "15 MIN", "湿地时间", f"{CLOTH}/mudflat/composite.png", "mud"),
        (72 + w1 + gap, w1, "24 PICKS", "固有时间", f"{CLOTH}/intrinsic/composite.png", "own"),
    ]
    for x, w, tag, name, href, cid in specs:
        panels.append(
            f'<g id="{cid}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#10151c"/>'
            f'{t(x + 22, y + 22, tag, 12, LIME, MONO, 2, weight=500)}'
            f'{t(x + 22, y + 48, name, 28, INK, SANS, 2)}'
            f'{image(href, x + 18, y + 110, w - 36, h - 132, cid + "img")}'
            f'</g>'
        )
    x = 72 + 2 * (w1 + gap)
    panels.append(
        f'<g id="press">'
        f'<rect x="{x}" y="{y}" width="{w3}" height="{h}" fill="#10151c"/>'
        f'{t(x + 22, y + 22, "PRESS", 12, LIME, MONO, 2, weight=500)}'
        f'{t(x + 22, y + 48, "参与", 28, INK, SANS, 2)}'
        f'<rect x="{x + 18}" y="{y + 110}" width="{w3 - 36}" height="{h - 132}" fill="none" stroke="{MADDER}" stroke-opacity="0.45"/>'
        f'<rect x="{x + w3 / 2 - 36}" y="{y + h / 2 - 10}" width="72" height="72" fill="{MADDER}"/>'
        f'{t(x + w3 / 2, y + h / 2 + 78, "踩踏", 16, MADDER, SANS, 3, "middle")}'
        f'</g>'
    )
    save(4, "time", frame(4, "两种时间", "WETLAND   ·   INTRINSIC   ·   PARTICIPATORY", "".join(panels)))


def slide_05():
    steps = [("01", "数值", "TIDE  ·  LIGHT  ·  CO₂"), ("02", "参数", "S  ·  V"), ("03", "浮长", "FLOAT"), ("04", "缝合", "STITCH")]
    y = 360
    rows = []
    for n, zh, en in steps:
        rows.append(
            f'{t(72, y, n, 13, LIME, MONO, 2, weight=500)}'
            f'{t(150, y - 8, zh, 36, INK, SANS, 4)}'
            f'{t(150, y + 40, en, 14, MUTED, ARCH, 1.6, weight=400)}'
        )
        y += 130
    img_x, img_w = 860, 988
    img_h = img_w * 960 / 1760
    img_y = 248 + (740 - img_h) / 2
    body = f'<g id="steps">{"".join(rows)}</g><g id="tide">{image(CLOTH + "/mudflat/hydro_with_ground.png", img_x, img_y, img_w, img_h, "tideimg", "xMidYMid meet")}</g>'
    save(5, "grammar", frame(5, "编织语法", "DATA   →   PARAMETER   →   PATTERN", body))


def slide_06():
    sources = [
        ("#4FB0BE", "潮位", "MARINE"),
        ("#B4BC57", "日照", "OPEN-METEO"),
        ("#8FA6C6", "CO₂", "CAMS"),
        ("#B06A3C", "地震", "USGS"),
        ("#EFE7D6", "琵鹭", "INATURALIST"),
    ]
    cols = []
    x = 72
    cw = 1776 / 5
    for color, zh, en in sources:
        cols.append(
            f'<line x1="{x}" y1="860" x2="{x + cw - 28}" y2="860" stroke="{color}" stroke-width="2"/>'
            f'{t(x, 880, zh, 22, INK, SANS, 1.5)}'
            f'{t(x, 916, en, 13, MUTED, ARCH, 0.8, weight=400)}'
        )
        x += cw
    body = (
        f'{t(72, 250, "22.135 N", 42, WHITE, MONO, 3)}'
        f'{t(72, 308, "113.555 E", 42, WHITE, MONO, 3)}'
        f'{image(CLOTH + "/mudflat/composite.png", 72, 430, 1776, 360, "day", "xMidYMid slice")}'
        f'<g id="sources">{"".join(cols)}</g>'
    )
    save(6, "situated", frame(6, "在场的数据", "SITUATED ENVIRONMENTAL DATA", body))


def slide_07():
    cols = []
    labels = [("连接", "CONNECTION"), ("中介", "MEDIATOR"), ("构成", "COMPOSITION")]
    drawings = [
        '<rect x="8" y="92" width="250" height="14" fill="#D8E272"/>'
        '<rect x="148" y="16" width="14" height="168" fill="#4FB0BE"/>'
        '<rect x="136" y="80" width="38" height="38" fill="#D8E272"/>',
        '<rect x="16" y="36" width="100" height="12" fill="#8FA6C6"/>'
        '<rect x="196" y="36" width="108" height="12" fill="#B4BC57"/>'
        '<rect x="142" y="22" width="32" height="40" fill="#D8E272"/>'
        '<rect x="64" y="128" width="150" height="12" fill="#4FB0BE"/>'
        '<rect x="210" y="156" width="70" height="12" fill="#EFE7D6"/>',
        '<rect x="16" y="28" width="288" height="12" fill="#D8E272"/>'
        '<rect x="16" y="52" width="288" height="12" fill="#FFFDF4"/>'
        '<rect x="16" y="76" width="288" height="12" fill="#4FB0BE"/>'
        '<rect x="16" y="100" width="288" height="12" fill="#B4BC57"/>'
        '<rect x="16" y="124" width="288" height="12" fill="#B06A3C"/>'
        '<rect x="16" y="148" width="288" height="12" fill="#EFE7D6"/>'
        '<rect x="168" y="68" width="28" height="28" fill="#D8E272"/>',
    ]
    cw = (1776 - 56) / 3
    for i, ((zh, en), draw) in enumerate(zip(labels, drawings)):
        x = 72 + i * (cw + 28)
        cols.append(
            f'<g id="rel-{i}">'
            f'<line x1="{x}" y1="248" x2="{x + cw}" y2="248" stroke="{LIME}" stroke-opacity="0.4"/>'
            f'{t(x, 270, zh, 36, INK, SANS, 4)}'
            f'{t(x, 320, en, 14, LIME, ARCH, 2.8, weight=400)}'
            f'<g transform="translate({x},400) scale({cw / 320:.3f})">{draw}</g>'
            f'</g>'
        )
    save(7, "relation", frame(7, "数据作为关系", "CONNECTION   ·   MEDIATOR   ·   COMPOSITION", "".join(cols)))


def slide_08():
    cells = []
    for j in range(8):
        for i in range(8):
            on = ((i * 3 - j) % 8 + 8) % 8 < 1
            cells.append(
                f'<rect x="{i * 36}" y="{j * 36}" width="30" height="30" fill="{LIME if on else "#1C2430"}"/>'
            )
    body = (
        f'<g id="cad">'
        f'<rect x="72" y="280" width="312" height="460" fill="#10151c"/>'
        f'<g transform="translate(84,366)">{"".join(cells)}</g>'
        f'{image(CLOTH + "/intrinsic/composite.png", 400, 280, 628, 460, "proc")}'
        f'{t(72, 770, "CAD  ·  图像", 48, INK, SANS, 4)}'
        f'{t(72, 834, "PROCESSING", 14, MUTED, ARCH, 2.2, weight=400)}'
        f'</g>'
        f'<g id="with-blank">'
        f'<rect x="1060" y="280" width="788" height="680" fill="none" stroke="{LIME}" stroke-opacity="0.55" stroke-dasharray="2 6"/>'
        f'{t(1088, 840, "with", 56, WHITE, ARCH, 1, weight=500)}'
        f'{t(1088, 910, "________", 18, MUTED, MONO, 2, weight=400)}'
        f'</g>'
    )
    save(8, "after", frame(8, "之后", "CAD   ·   IMAGE   ·   COLLABORATION", body))


def slide_09():
    extra = (
        f'<g id="cloth-behind">'
        f'{image(CLOTH + "/mudflat/composite.png", 0, 0, W, H, "full", "xMidYMid slice", 0.42)}'
        f'<rect width="{W}" height="{H}" fill="url(#veil)"/>'
        f'</g>'
    )
    # frame() puts extra before header, but veil gradient must be in defs.
    # Build this slide directly so the gradient exists.
    weaving, _, _ = px("WEAVING")
    with_, ww, _ = px("WITH", 3.2)
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect y="3" width="4" height="1" fill="#ffffff" fill-opacity="0.035"/>
    </pattern>
    <linearGradient id="wash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GROUND}" stop-opacity="0.94"/>
      <stop offset="0.44" stop-color="{GROUND}" stop-opacity="0.94"/>
      <stop offset="1" stop-color="{GROUND}" stop-opacity="0.18"/>
    </linearGradient>
    <clipPath id="full"><rect width="{W}" height="{H}"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{GROUND}"/>
  <image href="{CLOTH}/mudflat/composite.png" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" opacity="0.42" clip-path="url(#full)"/>
  <rect width="{W}" height="{H}" fill="url(#veil)"/>
  <g id="header"><g transform="translate(72,36)">{weaving}</g>
    <text x="1848" y="36" fill="{MUTED}" font-size="12" font-weight="500" letter-spacing="2.1" text-anchor="end" dominant-baseline="hanging" font-family="{MONO}">
      <tspan x="1848">COTAI MUDFLAT</tspan><tspan x="1848" dy="20">MACAU</tspan><tspan x="1848" dy="20">09  /  09</tspan>
    </text>
  </g>
  <g id="takeaway">
    {t(72, 760, "一次交叉", 64, WHITE, SANS, 3)}
    {t(72, 836, "不是同一时刻。", 64, WHITE, SANS, 3)}
    {t(72, 920, "A CROSSING IS NOT ONE MOMENT", 15, LIME, ARCH, 3.3, weight=400)}
  </g>
  <g id="footer">
    <rect x="72" y="1024" width="8" height="28" fill="{LIME}"/>
    <rect x="72" y="1044" width="28" height="8" fill="{LIME}"/>
    {t(114, 1024, "澳门大学", 16, INK, SANS)}
    {t(114, 1048, "SHIYU LEI  ·  2026", 11, MUTED, ARCH, 1.6, weight=400)}
    <g transform="translate({1848 - ww:.1f},1026)">{with_}</g>
  </g>
</svg>
'''
    save(9, "crossing", svg)


if __name__ == "__main__":
    slide_01()
    slide_02()
    slide_03()
    slide_04()
    slide_05()
    slide_06()
    slide_07()
    slide_08()
    slide_09()
