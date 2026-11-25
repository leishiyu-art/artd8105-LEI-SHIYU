"""One A2 system diagram for Polyrhythm Loom.

Copy is shortened from the student's PDF, Weaving With Polyrhythm Loom.
It is not a new account of the system.
"""

from pathlib import Path

import info_posters as P

W, H = P.W, P.H
LIME, WHITE, MUTED = P.LIME, P.WHITE, P.MUTED


def rule(y):
    return P.rect(68, y, 1104, 1, LIME, 0.4)


def head(zh, en, y):
    return [
        f'<text class="label" x="68" y="{y}">{zh}</text>',
        f'<text class="kicker" x="{68 + len(zh) * 26 + 18}" y="{y - 2}">{en}</text>',
    ]


def ticks(x, y, n, width=36):
    parts = []
    for i in range(n):
        fill = LIME if i % 2 == 0 else WHITE
        parts.append(P.rect(x, y + i * 7, width, 4, fill))
    return parts


def system():
    body = P.ground()
    body += P.pixel_word("WEAVING", 68, 52, cell=4.2, gap=1.5, fill=LIME)[0]
    body.append('<text class="mono" x="1172" y="68" text-anchor="end">COTAI MUDFLAT</text>')
    body.append('<text class="mono" x="1172" y="88" text-anchor="end">MACAU</text>')
    body += P.title("系统", "THE SYSTEM", 156)[0]
    body.append('<text class="sub" x="68" y="268">每个行动者的时间是一根线。每个交织点是一次关系。</text>')
    body.append('<text class="en" x="68" y="292">Each agent’s time is a thread. Every interlacement is a relation.</text>')

    # site
    body.append(rule(318))
    body += head("场地", "SITE", 356)
    zones = [("岸", 68, 150), ("泥滩", 230, 420), ("水道", 662, 200)]
    for i, (name, x, w) in enumerate(zones):
        body.append(P.rect(x, 384, w, 28, LIME if i == 1 else WHITE, 0.9))
        body.append(f'<text class="note" x="{x}" y="440">{name}</text>')
    body.append('<text class="sub" x="900" y="406">一纬十五分钟</text>')
    body.append('<text class="en" x="900" y="430">15 min a pick</text>')
    body.append('<text class="en" x="68" y="468">布的宽度是这条剖面，从岸到水道。长度是时间。</text>')

    # agents
    body.append(rule(496))
    body += head("七个行动者", "AGENTS", 534)
    agents = [
        ("大气", "1 天", 6),
        ("红树林", "1 天", 6),
        ("黑脸琵鹭", "潮 · 1 年", 10),
        ("潮汐", "12.42 时", 5),
        ("泥", "12.42 时", 5),
        ("仪器", "1 秒", 12),
        ("观众", "一踩", 3),
    ]
    for i, (name, period, n) in enumerate(agents):
        x = 68 + i * 160
        body += ticks(x, 556, n)
        body.append(f'<text class="note" x="{x}" y="652">{name}</text>')
        body.append(f'<text class="en" x="{x}" y="674">{period}</text>')
    body.append('<text class="en" x="68" y="708">远方地震穿过七层。实时读取，离线以模型兜底。琵鹭用的是记录。</text>')

    # stitches
    body.append(rule(736))
    body += head("缝合", "STITCHES", 774)
    binds = [
        ("觅食", "琵鹭 × 潮 × 泥"),
        ("栖息", "高潮涨到红树边"),
        ("吸收", "强光，二氧化碳低于日均"),
    ]
    parts = [
        ("扰动", "风 > 30 km/h，或雨 > 2 mm/h"),
        ("惊扰", "觅食时踩下，琵鹭离开两小时"),
        ("贯穿", "一次地震，一根线穿过七层"),
    ]
    body.append('<text class="kicker" x="68" y="812">协同</text>')
    body.append('<text class="kicker" x="660" y="812">相斥</text>')
    for i, ((a, b), (c, d)) in enumerate(zip(binds, parts)):
        y = 850 + i * 40
        body.append(P.rect(68, y - 14, 86, 8, LIME))
        body.append(f'<text class="note" x="168" y="{y}">{a}</text>')
        body.append(f'<text class="en" x="250" y="{y}">{b}</text>')
        body.append(P.rect(660, y - 14, 36, 8, WHITE))
        body.append(P.rect(708, y - 14, 36, 8, WHITE, 0.35))
        body.append(f'<text class="note" x="760" y="{y}">{c}</text>')
        body.append(f'<text class="en" x="842" y="{y}">{d}</text>')
    body.append('<text class="en" x="68" y="978">缝合是真实的相遇，不是频率的巧合。</text>')

    # clocks
    body.append(rule(1004))
    body += head("两只钟", "TWO CLOCKS", 1042)
    body += P.block_num("15", 68, 1064, cell=12, gap=3)[0]
    body.append('<text class="label" x="250" y="1104">泥滩时钟</text>')
    body.append('<text class="sub" x="250" y="1138">一纬十五分钟</text>')
    body.append('<text class="en" x="250" y="1164">慢的几乎拉成一条直线。</text>')
    body += P.block_num("24", 700, 1064, cell=12, gap=3)[0]
    body.append('<text class="label" x="882" y="1104">固有时间</text>')
    body.append('<text class="sub" x="882" y="1138">一个周期二十四纬。</text>')
    body.append('<text class="en" x="882" y="1166">No agent’s clock is the standard.</text>')
    body.append('<text class="en" x="68" y="1224">踩八下：每个表转过同样的角度，时间各不相同。</text>')

    # pipeline
    body.append(rule(1252))
    body += head("重编", "RECOMPILE", 1290)
    steps = [
        ("01", "复杂", "单位混在一起"),
        ("02", "简化", "趋势、周期、剩余"),
        ("03", "乐谱", "按两只钟重采样"),
        ("04", "像素", "每纬一行 0 和 1"),
        ("05", "织物", "屏幕与七层"),
    ]
    for i, (num, name, sub) in enumerate(steps):
        x = 68 + i * 230
        body += P.pixel_word(num, x, 1312, cell=5, gap=1.6, fill=LIME)[0]
        body.append(f'<text class="label" x="{x}" y="1362">{name}</text>')
        body.append(f'<text class="en" x="{x}" y="1386">{sub}</text>')
        if i < 4:
            body.append(P.rect(x + 72, 1326, 52, 3, LIME))
    body.append('<text class="en" x="68" y="1420">一张乐谱，同时驱动屏幕和七层亚克力。</text>')

    # grammar and out
    body.append(rule(1452))
    body += head("词汇与出口", "GRAMMAR", 1490)
    body.append('<text class="note" x="68" y="1536">经</text>')
    body.append('<text class="sub" x="120" y="1536">脊线 · 交汇 · 底色 · 菱花</text>')
    body.append('<text class="note" x="68" y="1574">纬</text>')
    body.append('<text class="sub" x="120" y="1574">小节线 · 靛蓝五染 · 茜草挖花</text>')
    body.append('<text class="note" x="680" y="1536">出口</text>')
    body.append('<text class="sub" x="760" y="1536">屏幕 · 七层亚克力 · 踏板</text>')
    body.append('<text class="en" x="760" y="1566">正面是一块布，侧面是七层。</text>')
    body.append('<text class="en" x="68" y="1620">数据决定图案，时间决定纬。</text>')

    body += P.footer()
    return P.wrap(body, "system")


def main():
    root = Path("/Users/leilei/Desktop/Cusor/my_work/polyrhythm_loom")
    svg = system()
    (root / "system.svg").write_text(svg)
    html = f'''<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><title>系统 · Polyrhythm Loom</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500&display=swap">
<style>body{{margin:0;background:#141816}} svg{{display:block;width:1240px;height:auto;margin:24px auto}}</style>
</head><body>{svg}</body></html>'''
    (root / "system.html").write_text(html)
    print("wrote", len(svg))


if __name__ == "__main__":
    main()
