#!/usr/bin/env python3
"""Build a simple 5-minute oral deck for Frieder Nake, Nr. 6."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import nsmap
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

INK = RGBColor(0x14, 0x14, 0x14)
PAPER = RGBColor(0xF7, 0xF5, 0xF0)
MUTED = RGBColor(0x6A, 0x66, 0x60)
RULE = RGBColor(0xC8, 0xC2, 0xB8)
ACCENT = RGBColor(0x2A, 0x2A, 0x2A)

W = Inches(13.333)
H = Inches(7.5)


def set_run(run, size, bold=False, color=INK, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Calibri"
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    if latin is None:
        latin = etree.SubElement(rPr, qn("a:latin"))
    latin.set("typeface", "Calibri")


def add_textbox(slide, l, t, w, h, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size, bold=bold, color=color, italic=italic)
    return box


def add_multiline(slide, l, t, w, h, lines, size=20, color=INK, bold=False, space_after=10):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = line
        set_run(run, size, bold=bold, color=color)
    return box


def fill_slide(slide, color=PAPER):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = bg._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def hairline(slide, l, t, w):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, Emu(12700))
    line.fill.solid()
    line.fill.fore_color.rgb = RULE
    line.line.fill.background()


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def draw_grid_motif(slide, left, top, cols=8, rows=6, cell=0.22):
    """Abstract plotter-like blocks — homage, not a copy of Nr. 6."""
    cell_in = Inches(cell)
    gap = Inches(0.04)
    pattern = [
        [0, 1, 0, 1, 1, 0, 0, 1],
        [1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 0, 0],
    ]
    hatch = [
        [None, "h", None, "v", "h", None, None, "v"],
        ["v", "h", None, None, "v", "h", None, None],
        [None, None, "h", "v", None, "h", "v", None],
        ["h", None, "v", None, None, None, "h", "v"],
        [None, "v", "h", None, "v", None, None, "h"],
        ["h", None, None, "v", "h", "v", None, None],
    ]
    for r in range(rows):
        for c in range(cols):
            x = left + c * (cell_in + gap)
            y = top + r * (cell_in + gap)
            sq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, cell_in, cell_in)
            sq.line.color.rgb = INK
            sq.line.width = Pt(0.75)
            if pattern[r][c]:
                sq.fill.solid()
                sq.fill.fore_color.rgb = PAPER
                # hatch lines
                kind = hatch[r][c]
                n = 4
                if kind == "h":
                    for i in range(1, n):
                        ly = y + cell_in * i / n
                        ln = slide.shapes.add_shape(
                            MSO_SHAPE.RECTANGLE, x + Emu(20000), ly, cell_in - Emu(40000), Emu(9000)
                        )
                        ln.fill.solid()
                        ln.fill.fore_color.rgb = INK
                        ln.line.fill.background()
                elif kind == "v":
                    for i in range(1, n):
                        lx = x + cell_in * i / n
                        ln = slide.shapes.add_shape(
                            MSO_SHAPE.RECTANGLE, lx, y + Emu(20000), Emu(9000), cell_in - Emu(40000)
                        )
                        ln.fill.solid()
                        ln.fill.fore_color.rgb = INK
                        ln.line.fill.background()
            else:
                sq.fill.background()


def card(slide, l, t, w, h, num, title, body):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    sh.line.color.rgb = RULE
    sh.line.width = Pt(0.75)
    add_textbox(slide, l + Inches(0.22), t + Inches(0.16), w - Inches(0.4), Inches(0.32), num, 12, color=MUTED)
    add_textbox(slide, l + Inches(0.22), t + Inches(0.42), w - Inches(0.4), Inches(0.4), title, 18, bold=True)
    add_textbox(slide, l + Inches(0.22), t + Inches(0.88), w - Inches(0.44), h - Inches(1.05), body, 14, color=MUTED)


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # --- 1 Title ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    draw_grid_motif(s, Inches(8.6), Inches(1.55))
    add_textbox(s, Inches(0.7), Inches(1.35), Inches(7.5), Inches(0.4), "5-minute oral presentation", 14, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(1.85), Inches(7.6), Inches(1.6), "Frieder Nake", 54, bold=True)
    add_textbox(s, Inches(0.7), Inches(3.35), Inches(7.6), Inches(0.7), "Nr. 6", 36, italic=True)
    hairline(s, Inches(0.7), Inches(4.2), Inches(3.2))
    add_textbox(
        s,
        Inches(0.7),
        Inches(4.45),
        Inches(7.5),
        Inches(1.2),
        "1965  ·  plotter drawing  ·  computer grafik, Stuttgart",
        18,
        color=MUTED,
    )
    notes(
        s,
        "Hi everyone. Today, I want to present a landmark piece created in 1965 by Frieder Nake, titled simply: Nr. 6.\n\n"
        "Frieder Nake is a German mathematician, computer scientist, and one of the absolute pioneers of digital art. "
        "Back in November 1965, he and Georg Nees curated a show called computer grafik in Stuttgart. "
        "This wasn't just another gallery opening—it was historically one of the very first public exhibitions of computer-generated art in Europe.\n\n"
        "The work Nr. 6 is a precise, black-and-white plotter drawing on paper. At first glance, it looks like a clean, abstract grid of geometric lines and square blocks. "
        "But its true significance lies in how and why it was constructed through code.",
    )

    # --- 2 Who & work ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    add_textbox(s, Inches(0.7), Inches(0.4), Inches(12), Inches(0.35), "01  ·  0:00–0:45", 13, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(0.75), Inches(12), Inches(0.7), "Who he is, and the work", 32, bold=True)
    hairline(s, Inches(0.7), Inches(1.5), Inches(1.8))

    facts = [
        ("Artist", "Frieder Nake — German mathematician, computer scientist, pioneer of digital art"),
        ("Moment", "November 1965: computer grafik, Stuttgart, with Georg Nees"),
        ("History", "One of the first public exhibitions of computer-generated art in Europe"),
        ("Work", "Nr. 6 — black-and-white plotter drawing: grids, lines, square blocks"),
        ("Claim", "Significance is not the look — it is how and why it was constructed through code"),
    ]
    y = Inches(1.85)
    for label, body in facts:
        add_textbox(s, Inches(0.7), y, Inches(1.8), Inches(0.7), label, 16, bold=True, color=INK)
        add_textbox(s, Inches(2.7), y, Inches(9.6), Inches(0.85), body, 18, color=MUTED)
        y += Inches(0.95)
    notes(
        s,
        "Frieder Nake is a German mathematician, computer scientist, and one of the absolute pioneers of digital art. "
        "Back in November 1965, he and Georg Nees curated a show called computer grafik in Stuttgart. "
        "This wasn't just another gallery opening—it was historically one of the very first public exhibitions of computer-generated art in Europe.\n\n"
        "The work Nr. 6 is a precise, black-and-white plotter drawing on paper. At first glance, it looks like a clean, abstract grid of geometric lines and square blocks. "
        "But its true significance lies in how and why it was constructed through code.",
    )

    # --- 3 Context ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    add_textbox(s, Inches(0.7), Inches(0.4), Inches(12), Inches(0.35), "02  ·  0:45–2:00", 13, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(0.75), Inches(12), Inches(0.7), "1965, cybernetics, information aesthetics", 30, bold=True)
    hairline(s, Inches(0.7), Inches(1.5), Inches(1.8))

    cols = [
        ("Cold War machine", "Computers were not personal creative tools. They were military-industrial assets — trajectory, control, calculation."),
        ("Cybernetics", "Feedback, information, self-regulating systems. Control is shared, observed, and redesigned."),
        ("Post-war Germany", "How to protect society from emotional propaganda and fascism. Rationality as a civic defence."),
    ]
    for i, (title, body) in enumerate(cols):
        x = Inches(0.7) + i * Inches(4.15)
        box = slide_card = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.85), Inches(3.9), Inches(2.55))
        slide_card.fill.solid()
        slide_card.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        slide_card.line.color.rgb = RULE
        slide_card.line.width = Pt(0.75)
        add_textbox(s, x + Inches(0.25), Inches(2.05), Inches(3.4), Inches(0.5), title, 18, bold=True)
        add_textbox(s, x + Inches(0.25), Inches(2.55), Inches(3.4), Inches(1.6), body, 15, color=MUTED)

    quote = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(4.65), Inches(11.9), Inches(2.15))
    quote.fill.solid()
    quote.fill.fore_color.rgb = INK
    quote.line.fill.background()
    add_textbox(
        s,
        Inches(1.0),
        Inches(4.9),
        Inches(11.3),
        Inches(0.9),
        "“Rationality is humanity's first defense against fascism.”",
        22,
        italic=True,
        color=PAPER,
    )
    add_textbox(
        s,
        Inches(1.0),
        Inches(5.8),
        Inches(11.3),
        Inches(0.7),
        "Max Bense → Information Aesthetics: beauty measured and generated through autonomous systems.\nNake reclaims the calculating machine — military control out; mathematical rationality in.",
        15,
        color=RGBColor(0xC8, 0xC2, 0xB8),
    )
    notes(
        s,
        "To really understand Nr. 6, we have to step into the atmosphere of 1965. This was the height of the Cold War, and computers weren't personal creative tools—they were massive military-industrial assets used for trajectory calculations and control systems.\n\n"
        "What fascinated me when studying this period is how Cybernetics—the science of feedback, information, and self-regulating systems—was reshaping how people thought about control. At the same time, post-war Germany was deeply haunted by World War II, asking how to protect society from emotional propaganda and fascism.\n\n"
        "Nake’s mentor, philosopher Max Bense, synthesized these ideas into 'Information Aesthetics.' Influenced by cybernetic theory, Bense argued that beauty could be scientifically measured and generated through autonomous systems. He famously stated: 'Rationality is humanity's first defense against fascism.'\n\n"
        "So when Nake took a cold-war calculating machine and programmed it to generate art through cybernetic feedback logic, it was a profound act. He was reclaiming technology from military control, stripping away dangerous emotional manipulation, and replacing it with pure, neutral, mathematical rationality.",
    )

    # --- 4 Procedure ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    add_textbox(s, Inches(0.7), Inches(0.4), Inches(12), Inches(0.35), "03  ·  2:00–3:15", 13, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(0.75), Inches(12), Inches(0.7), "The procedure — four steps", 32, bold=True)
    hairline(s, Inches(0.7), Inches(1.5), Inches(1.8))

    steps = [
        ("01", "Define the grid", "A 2D matrix across a blank canvas — an empty chessboard."),
        ("02", "Symbol palette", "Primitives: horizontal, vertical, diagonal lines, and square blocks."),
        ("03", "Probabilistic evaluation", "Each cell is placed by a pseudo-random generator bounded by a probability matrix. High density vs. empty space."),
        ("04", "Mechanical execution", "Coordinates go to a Zuse Z64 Graphomat. A mechanical arm holds an ink pen."),
    ]
    for i, (num, title, body) in enumerate(steps):
        x = Inches(0.7) + (i % 2) * Inches(6.2)
        y = Inches(1.8) + (i // 2) * Inches(2.15)
        card(s, x, y, Inches(5.9), Inches(1.95), num, title, body)

    notes(
        s,
        "Now, let’s look at the algorithm itself. If you wanted to recreate Nr. 6 today, here is the exact 4-step procedure Nake designed:\n\n"
        "Step 1: Define the Grid. Construct a standard 2D grid matrix across a blank canvas, like an empty chessboard.\n"
        "Step 2: Establish a Symbol Palette. Create a library of basic geometric primitives—horizontal lines, vertical strokes, diagonal lines, and square blocks.\n"
        "Step 3: Probabilistic Evaluation. As the algorithm traverses through each cell, it doesn't place shapes arbitrarily. It uses a pseudo-random number generator bounded by a precise probability matrix. High probability values yield dense, clustered lines; zero probability leaves clean, negative space.\n"
        "Step 4: Mechanical Execution. The computer exports these calculated coordinates directly to a Zuse Z64 Graphomat plotter, where a mechanical arm holds an ink pen to draw the final piece.\n\n"
        "If a stranger executes this same procedure with Nake's probability matrix, they will yield a drawing structurally identical in language, yet unique in its probabilistic details.",
    )

    # --- 5 Why ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    add_textbox(s, Inches(0.7), Inches(0.4), Inches(12), Inches(0.35), "04  ·  3:15–5:00", 13, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(0.75), Inches(12), Inches(0.7), "Why this work", 32, bold=True)
    hairline(s, Inches(0.7), Inches(1.5), Inches(1.8))

    points = [
        ("Cede control", "Nake does not draw the picture. He designs the rulebook and hands execution to system + probability. (Galanter: generative art / meta-designer)"),
        ("Cybernetic moment", "The computer stops being a passive tool and becomes an autonomous system. Control is shared."),
        ("More-than-human design", "Non-human agency — computational rules, simulation, environmental feedback — enters embodied spatial narrative."),
        ("The closing claim", "Algorithms are not only cold code. Rationality, rules, and code can be liberating, poetic, and human."),
    ]
    y = Inches(1.8)
    for title, body in points:
        add_textbox(s, Inches(0.7), y, Inches(3.4), Inches(1.1), title, 20, bold=True)
        add_textbox(s, Inches(4.3), y, Inches(8.3), Inches(1.15), body, 18, color=MUTED)
        y += Inches(1.2)
    notes(
        s,
        "I chose Frieder Nake and Nr. 6 because I’ve always been deeply interested in Cybernetics—specifically, how systems operate when control is shared or ceded. "
        "Nr. 6 marks the exact historical moment when artists stopped treating the computer as a passive tool, and began designing autonomous cybernetic systems.\n\n"
        "As Philip Galanter highlights in generative art theory, Nake didn't draw the picture—he designed the rulebook and ceded control to the system and probability. He became a meta-designer.\n\n"
        "This directly feeds into my own research direction in More-than-Human Design. I am exploring how we can integrate non-human agency—whether that’s computational rules, game simulation mechanics, or environmental feedback loops—into embodied spatial narratives. "
        "Looking back at Nr. 6 reminds us that algorithms aren't just cold code. When we treat generative systems as active agents in a cybernetic feedback loop, we open up a dialogue between human intent and non-human agency.\n\n"
        "Nr. 6 proved 60 years ago that rationality, system rules, and code can be liberating, poetic, and profoundly human. Thank you!",
    )

    # --- 6 Thank you ---
    s = prs.slides.add_slide(blank)
    fill_slide(s)
    draw_grid_motif(s, Inches(8.6), Inches(1.7))
    add_textbox(s, Inches(0.7), Inches(2.2), Inches(7.6), Inches(1.2), "Thank you", 54, bold=True)
    hairline(s, Inches(0.7), Inches(3.5), Inches(2.4))
    add_textbox(
        s,
        Inches(0.7),
        Inches(3.8),
        Inches(7.6),
        Inches(1.4),
        "Frieder Nake  ·  Nr. 6  ·  1965\nQuestions welcome.",
        18,
        color=MUTED,
    )
    notes(s, "Nr. 6 proved 60 years ago that rationality, system rules, and code can be liberating, poetic, and profoundly human. Thank you!")

    out = "/Users/leilei/Desktop/Cusor/my_work/presentations/Nake_Nr6_5min.pptx"
    prs.save(out)
    print(out)


if __name__ == "__main__":
    build()
