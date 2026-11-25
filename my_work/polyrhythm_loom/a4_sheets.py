"""Three A4 table sheets. Copy shortened from the student's PDF.

Visual system matches the dark pixel posters: ground, lime, white.
"""

import math
from pathlib import Path

import info_posters as P

W, H = P.W, P.H
LIME, WHITE = P.LIME, P.WHITE
MUD = "#241C16"
MADDER = "#D24E35"


def rule(y):
    return P.rect(68, y, 1104, 1, LIME, 0.4)


def head(zh, en, x, y):
    return [
        f'<text class="label" x="{x}" y="{y}">{zh}</text>',
        f'<text class="kicker" x="{x + len(zh) * 28 + 16}" y="{y - 2}">{en}</text>',
    ]


def chrome(n, zh, en, y=168):
    body = P.ground()
    body += P.pixel_word("WEAVING", 68, 48, cell=4.2, gap=1.5, fill=LIME)[0]
    body.append('<text class="mono" x="1172" y="62" text-anchor="end">COTAI MUDFLAT</text>')
    body.append('<text class="mono" x="1172" y="82" text-anchor="end">MACAU</text>')
    body.append(f'<text class="mono" x="1172" y="106" text-anchor="end">0{n}  /  03</text>')
    body += P.title(zh, en, y)[0]
    return body


def footer():
    return P.footer()


def line(x1, y1, x2, y2, stroke=LIME, width=2, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}"{extra}/>'
    )


def sheet_site():
    body = chrome(1, "场地", "THE SITE", 156)
    body.append('<text class="sub" x="68" y="268">一个共同的场景：路氹城生态保护区的泥滩</text>')
    body.append('<text class="en" x="68" y="294">One shared scene: the Cotai mudflat</text>')

    body += head("剖面", "TRANSECT", 68, 348)
    # frame and mud wedge, shore high at the left, channel low at the right
    body.append(P.rect(68, 372, 1104, 430, "#10140F"))
    body.append(
        '<path d="M68,560 L280,590 L1172,760 L1172,802 L68,640 Z" fill="#241C16"/>'
    )
    body.append(line(68, 560, 1172, 760, LIME, 2))
    # mangroves on the high shore
    for i, cx in enumerate((150, 210, 270, 330)):
        body.append(f'<circle cx="{cx}" cy="{500 - (i % 2) * 8}" r="22" fill="{LIME}"/>')
        body.append(f'<rect x="{cx - 3}" y="520" width="6" height="36" fill="{LIME}"/>')
    # high water, low water
    body.append(line(360, 548, 1140, 690, LIME, 2, "7 6"))
    body.append(line(430, 630, 1140, 748, WHITE, 2, "2 5"))
    # two birds at the low-water edge
    body.append('<path d="M760,688 l10,-14 l10,14 l-4,-4 l-6,0 z" fill="#FFFDF4"/>')
    body.append('<path d="M800,704 l8,-12 l8,12 l-3,-3 l-5,0 z" fill="#FFFDF4"/>')

    labels = [
        (80, 400, "岸", "SHORE"),
        (1040, 400, "水道", "CHANNEL"),
        (380, 500, "红树林", "MANGROVES"),
        (470, 520, "高潮栖息", "ROOST"),
        (820, 500, "高潮", "HIGH WATER"),
        (620, 760, "低潮觅食", "FEED AT LOW WATER"),
        (980, 700, "低潮", "LOW WATER"),
        (120, 690, "泥 · 沉积物", "MUD"),
    ]
    for x, y, zh, en in labels:
        body.append(f'<text class="note" x="{x}" y="{y}" font-size="16">{zh}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 18}" font-size="12">{en}</text>')

    body.append('<text class="sub" x="68" y="844">布的宽度就是这条剖面，长度是时间，一纬十五分钟。</text>')
    body.append('<text class="en" x="68" y="870">The cloth’s width is this transect. Its length is time, 15 minutes a pick.</text>')

    body.append(rule(900))
    body += head("推测", "SPECULATIVE", 68, 944)
    body.append('<text class="en" x="68" y="974">同一条剖面，按关键带重读。从树冠到地下水的一层薄壳。不是测绘图。</text>')
    body.append('<text class="en" x="68" y="996">The same cut, read as the critical zone. The thin layer from canopy to groundwater.</text>')

    bands = [
        ("大气圈", "ATMOSPHERE", "二氧化碳、风、雨", "CO₂, wind, rain"),
        ("生物圈", "BIOSPHERE", "红树林、黑脸琵鹭", "Mangroves, spoonbills"),
        ("水圈", "HYDROSPHERE", "潮", "Tide"),
        ("岩石圈", "LITHOSPHERE", "泥与沉积", "Mud and sediment"),
        ("技术圈", "TECHNOSPHERE", "仪器", "The measuring instruments"),
    ]
    for i, (zh, en, what, what_en) in enumerate(bands):
        y = 1024 + i * 78
        body.append(P.rect(68, y, 1104, 64, "#141A14" if i % 2 == 0 else "#101610"))
        body.append(P.rect(68, y, 8, 64, LIME if i % 2 == 0 else WHITE))
        body.append(f'<text class="note" x="96" y="{y + 28}">{zh}</text>')
        body.append(f'<text class="en" x="96" y="{y + 50}">{en}</text>')
        body.append(f'<text class="sub" x="420" y="{y + 30}">{what}</text>')
        body.append(f'<text class="en" x="420" y="{y + 52}">{what_en}</text>')
        # shore-to-channel ticks, same axis as the transect
        body.append(P.rect(860, y + 28, 280, 3, LIME, 0.7))
        body.append(f'<text class="en" x="860" y="{y + 22}" font-size="11">岸</text>')
        body.append(f'<text class="en" x="1108" y="{y + 22}" font-size="11">水道</text>')

    body.append('<text class="sub" x="68" y="1448">观众不是一个圈层。人从一个小口进入。</text>')
    body.append('<text class="en" x="68" y="1474">Humans are not a sphere. They enter as visitors.</text>')

    facts = [
        ("越冬地", "1989 年首次记录到 6 只", "Wintering ground. First record, 1989: 6 birds."),
        ("重要鸟区", "2004 年起，澳门唯一的国际重要鸟区", "An Important Bird Area since 2004. Macau’s only one."),
        ("7,746 只", "2026 年全球普查，已由濒危降为易危", "Worldwide count, 2026. Downlisted from Endangered to Vulnerable."),
        ("展期", "正值琵鹭抵达越冬", "The show opens in their arrival season."),
    ]
    for i, (title, zh, en) in enumerate(facts):
        x = 68 + (i % 2) * 560
        y = 1516 + (i // 2) * 70
        body.append(f'<text class="note" x="{x}" y="{y}">{title}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 22}">{zh}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 42}">{en}</text>')
    body.append('<text class="en" x="68" y="1656">事实来自新华社，2026 年 6 月 5 日。 Facts: Xinhua, 5 June 2026.</text>')
    body += footer()
    return P.wrap(body, "site")


def log_pos(seconds, x0, width):
    # axis runs from 1 second to 100 years
    span = math.log10(100 * 365.25 * 86400)
    return x0 + width * (math.log10(seconds) / span)


def sheet_time():
    body = chrome(2, "时间尺度", "TIME SCALES", 150)
    body.append('<text class="sub" x="68" y="262">同样 480 纬：机器 20 秒，琵鹭 20 年</text>')
    body.append('<text class="en" x="68" y="288">The same 480 picks: 20 seconds for a machine, 20 years for a bird.</text>')

    x0, width = 280, 860
    ticks = [
        (1, "1 秒", "1 s"),
        (60, "1 分", "1 min"),
        (3600, "1 时", "1 h"),
        (86400, "1 日", "1 day"),
        (365.25 * 86400, "1 年", "1 yr"),
        (10 * 365.25 * 86400, "10 年", "10 yr"),
    ]
    for seconds, zh, en in ticks:
        x = log_pos(seconds, x0, width)
        body.append(line(x, 340, x, 980, "#243028", 1))
        body.append(f'<text class="en" x="{x}" y="328" text-anchor="middle">{en}</text>')

    five_days = log_pos(5 * 86400, x0, width)
    body.append(line(five_days, 336, five_days, 1004, MADDER, 2, "4 5"))
    body.append(f'<text class="en" x="{five_days + 8}" y="356" fill="{MADDER}">5 天 · 泥滩时钟</text>')

    rows = [
        ("仪器", "Device", 20, "20 秒"),
        ("潮", "Tide", 10 * 86400, "10 天"),
        ("植物", "Plants", 20 * 86400, "20 天"),
        ("地震", "Earthquakes", 3 * 365.25 * 86400, "约 3 年"),
        ("大气", "CO₂", 20 * 365.25 * 86400, "20 年"),
        ("琵鹭", "Spoonbill", 20 * 365.25 * 86400, "20 年"),
    ]
    for i, (zh, en, seconds, label) in enumerate(rows):
        y = 390 + i * 96
        body.append(f'<text class="note" x="68" y="{y + 22}">{zh}</text>')
        body.append(f'<text class="en" x="68" y="{y + 44}">{en}</text>')
        x1 = log_pos(seconds, x0, width)
        body.append(P.rect(x0, y + 8, max(8, x1 - x0), 22, LIME if i % 2 == 0 else WHITE))
        body.append(f'<text class="note" x="{x1 + 10}" y="{y + 26}" font-size="16">{label}</text>')

    body.append('<text class="sub" x="68" y="1048">泥滩时钟：一纬十五分钟。这 480 纬对谁都是 5 天，慢的几乎拉成一条直线。</text>')
    body.append('<text class="en" x="68" y="1076">Mudflat clock: 1 pick = 15 minutes, 5 days for everyone. Slow agents become almost a flat line.</text>')

    body.append(rule(1112))
    body += head("等拍", "EQUAL BEATS", 68, 1160)
    body.append('<text class="sub" x="68" y="1204">一个周期二十四纬。没有谁的钟是标准。</text>')
    body.append('<text class="en" x="68" y="1230">One cycle = 24 picks. No agent’s clock is the standard.</text>')

    presses = [
        ("大气", "4 个月", "4 months"),
        ("植物", "8 小时", "8 hours"),
        ("琵鹭", "4 个月", "4 months"),
        ("潮", "4.1 小时", "4.1 hours"),
        ("地震", "8 次", "8 quakes"),
        ("仪器", "0.33 秒", "0.33 s"),
    ]
    for i, (zh, amount, en) in enumerate(presses):
        x = 68 + i * 190
        body.append(P.rect(x, 1272, 120, 14, LIME))
        body.append(f'<text class="note" x="{x}" y="1316">{zh}</text>')
        body.append(f'<text class="sub" x="{x}" y="1344">{amount}</text>')
        body.append(f'<text class="en" x="{x}" y="1368">{en}</text>')
    body.append('<text class="sub" x="68" y="1424">踩八下：六支表转过同样的角度，时间各不相同。</text>')
    body.append('<text class="en" x="68" y="1452">Eight presses: the same angle on every dial, a different time on each.</text>')
    body.append('<text class="en" x="68" y="1496">泥滩时钟下，这八纬让潮转过 0.16 圈，二氧化碳只转过 0.0002 圈。</text>')
    body.append('<text class="en" x="68" y="1522">Under the mudflat clock, eight picks turn the tide 0.16 of a cycle, and CO₂ only 0.0002.</text>')
    body += footer()
    return P.wrap(body, "time")


def satin_cells(x, y, n, cell=11):
    parts = []
    for j in range(8):
        for i in range(8):
            if (3 * i - j) % 8 < n:
                parts.append(P.rect(x + i * cell, y + j * cell, cell - 2, cell - 2, LIME if (i + j) % 3 else WHITE))
    return parts


def swatch(kind, x, y, s=150):
    parts = [P.rect(x, y, s, s, "#101610")]
    if kind == "ridge":
        for i in range(9):
            px = x + 14 + i * 14
            py = y + s / 2 + math.sin(i / 8 * math.tau) * 40
            parts.append(P.rect(px, py, 10, 10, LIME))
    elif kind == "cross":
        for i in range(9):
            parts.append(P.rect(x + 14 + i * 14, y + 20 + i * 12, 10, 10, LIME))
            parts.append(P.rect(x + 14 + i * 14, y + s - 30 - i * 12, 10, 10, WHITE))
        parts.append(P.rect(x + s / 2 - 8, y + s / 2 - 8, 18, 18, LIME))
    elif kind == "ground":
        parts += satin_cells(x + 30, y + 30, 4, 11)
    elif kind == "lozenge":
        for i in range(5):
            w = 10 + i * 16 if i < 3 else 10 + (4 - i) * 16
            parts.append(P.rect(x + (s - w) / 2, y + 30 + i * 20, w, 12, LIME))
    elif kind == "bar":
        parts += satin_cells(x + 30, y + 24, 3, 11)
        parts.append(P.rect(x + 8, y + 18, s - 16, 6, WHITE))
        parts.append(P.rect(x + 8, y + 28, s - 16, 6, WHITE))
    elif kind == "indigo":
        tones = (0.35, 0.5, 0.7, 0.85, 1)
        for i, op in enumerate(tones):
            parts.append(P.rect(x + 14, y + 14 + i * 20, s - 28, 12, LIME, op))
    elif kind == "madder":
        parts += satin_cells(x + 30, y + 22, 3, 11)
        parts.append(P.rect(x + 10, y + s / 2, s - 20, 10, MADDER))
    return parts


def sheet_method():
    body = chrome(3, "方法", "METHOD", 150)
    body.append('<text class="sub" x="68" y="258">关系怎么缝，数据怎么变成布。</text>')
    body.append('<text class="en" x="68" y="284">How meetings are stitched, and how data becomes cloth.</text>')

    body += head("关系", "RELATIONS", 68, 332)
    body.append('<text class="en" x="280" y="330">缝合是真实的相遇，不是频率的巧合。</text>')
    binds = [
        ("觅食", "FEEDING", "低潮打开泥滩，琵鹭顺着水线出去。", "Low water opens the mud; the birds follow the edge out."),
        ("栖息", "ROOSTING", "高潮涨到红树，琵鹭等在边上。", "High water reaches the mangroves; the birds wait there."),
        ("吸收", "DRAWDOWN", "光照强，且二氧化碳低于当日平均。", "Strong light, and CO₂ below its daily mean."),
    ]
    parts_ = [
        ("扰动", "DISTURBANCE", "风超过 30 km/h，或雨超过 2 mm/h，层就分开。", "Wind over 30 km/h or rain over 2 mm/h: the layers part."),
        ("惊扰", "STARTLE", "觅食时踩下，琵鹭离开泥滩两小时。", "A press while they feed sends the birds off for two hours."),
        ("贯穿", "JOLT", "远方地震：一根线同时穿过七层。", "A distant quake: one thread through all seven layers."),
    ]
    body.append('<text class="kicker" x="68" y="368">协同 · 层缝在一起</text>')
    body.append('<text class="kicker" x="660" y="368">相斥 · 层分开</text>')
    for i, ((a, ae, b, be), (c, ce, d, de)) in enumerate(zip(binds, parts_)):
        y = 400 + i * 108
        body.append(P.rect(68, y, 8, 88, LIME))
        body.append(f'<text class="note" x="92" y="{y + 28}">{a}</text>')
        body.append(f'<text class="en" x="180" y="{y + 28}">{ae}</text>')
        body.append(f'<text class="en" x="92" y="{y + 58}">{b}</text>')
        body.append(f'<text class="en" x="92" y="{y + 80}">{be}</text>')
        body.append(P.rect(660, y, 8, 88, WHITE))
        body.append(f'<text class="note" x="684" y="{y + 28}">{c}</text>')
        body.append(f'<text class="en" x="772" y="{y + 28}">{ce}</text>')
        body.append(f'<text class="en" x="684" y="{y + 58}">{d}</text>')
        body.append(f'<text class="en" x="684" y="{y + 80}">{de}</text>')
    body.append('<text class="en" x="68" y="736">每个节点都写在布边：潮、日出、觅食、二氧化碳的低点、地震。</text>')

    body.append(rule(764))
    body += head("重编", "RECOMPILE", 68, 808)
    steps = [
        ("01", "复杂数据", "COMPLEX", "单位和缺口混在一起", "raw/*.csv"),
        ("02", "简化数据", "SIMPLE", "0–1：趋势、周期、剩余", "simple/*.csv"),
        ("03", "乐谱", "SCORE", "按两只钟重采样", "score.json"),
        ("04", "像素", "PIXEL", "每纬一行 0 和 1", "draft.png"),
        ("05", "织物", "TEXTILE", "屏幕与七层", "layers + screen"),
    ]
    for i, (num, zh, en, sub, file_) in enumerate(steps):
        x = 68 + i * 230
        body += P.pixel_word(num, x, 836, cell=5, gap=1.5, fill=LIME)[0]
        body.append(f'<text class="note" x="{x}" y="900">{zh}</text>')
        body.append(f'<text class="en" x="{x}" y="922">{en}</text>')
        body.append(f'<text class="en" x="{x}" y="952">{sub}</text>')
        body.append(f'<text class="mono" x="{x}" y="978">{file_}</text>')
        if i < 4:
            body.append(P.rect(x + 168, 848, 40, 3, LIME))
    body.append('<text class="en" x="68" y="1016">一张乐谱同时驱动屏幕和分层实物。观众看见的，和刻出来的，是同一个源。</text>')

    body.append(rule(1044))
    body += head("织造语法", "GRAMMAR", 68, 1088)
    body.append('<text class="en" x="360" y="1086">数据决定图案，时间决定纬。</text>')
    words = [
        ("ridge", "脊线", "RIDGE", "周期变成摆动"),
        ("cross", "交汇", "CROSSING", "相遇处相加"),
        ("ground", "底色", "GROUND", "趋势变成明暗"),
        ("lozenge", "菱花", "LOZENGE", "一次事件，一朵花"),
        ("bar", "小节线", "BAR LINE", "每 24 纬，两根平纹"),
        ("indigo", "靛蓝五染", "INDIGO", "这一纬的和弦决定深浅"),
        ("madder", "茜草挖花", "MADDER", "观众踩下，多一根纬"),
    ]
    for i, (kind, zh, en, sub) in enumerate(words):
        col = i if i < 4 else i - 4
        row = 0 if i < 4 else 1
        x = 68 + col * 280
        y = 1116 + row * 250
        body += swatch(kind, x, y, 118)
        body.append(f'<text class="note" x="{x}" y="{y + 146}">{zh}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 168}">{en}</text>')
        body.append(f'<text class="en" x="{x}" y="{y + 190}">{sub}</text>')
    body.append('<text class="en" x="68" y="1632">行动者在共同的经区里摆动，彼此穿过，而不是各占一个格子。</text>')
    body += footer()
    return P.wrap(body, "method")


def main():
    root = Path("/Users/leilei/Desktop/Cusor/my_work/polyrhythm_loom")
    files = {
        "a4_01_site.svg": sheet_site(),
        "a4_02_time.svg": sheet_time(),
        "a4_03_method.svg": sheet_method(),
    }
    for name, svg in files.items():
        (root / name).write_text(svg)
        print(name, len(svg))
    sections = "\n".join(f'<section id="{n}">{s}</section>' for n, s in files.items())
    html = f'''<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><title>A4 · Polyrhythm Loom</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500&display=swap">
<style>
body {{ margin: 0; background: #141816; }}
section {{ width: 1240px; margin: 28px auto; }}
svg {{ display: block; width: 1240px; height: auto; }}
</style></head><body>
{sections}
</body></html>'''
    (root / "a4_sheets.html").write_text(html)


if __name__ == "__main__":
    main()
