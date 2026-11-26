#!/usr/bin/env python3
"""Turn full_paper.md into an ACM DIS 2027 review manuscript.

The prose stays the student's. This script only applies the template:
sectioning, numeric citations, figure placement, and LaTeX escapes.
Working notes in 【】 and the figure-slot lines are not copied into the paper.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "full_paper.md"
OUT = ROOT / "main.tex"

CITES = [
    ("[Giaccardi and Redström 2020; Wakkary 2021]", r"\cite{giaccardi2020,wakkary2021}"),
    ("[Loukissas 2019; Gabrys 2016]", r"\cite{loukissas2019,gabrys2016}"),
    ("[Zimmerman et al. 2007; Gaver 2012]", r"\cite{zimmerman2007,gaver2012}"),
    ("[Pschetz and Bastian 2018; Bastian and Hawitt 2022]", r"\cite{pschetz2018,bastian2022}"),
    ("[Latour 2005; Haraway 2016]", r"\cite{latour2005,haraway2016}"),
    ("Pschetz and Bastian [2018]", r"Pschetz and Bastian~\cite{pschetz2018}"),
    ("[Pschetz and Bastian 2018]", r"\cite{pschetz2018}"),
    ("[Latour 2005]", r"\cite{latour2005}"),
    ("[Haraway 2008]", r"\cite{haraway2008}"),
    ("[Haraway 2016]", r"\cite{haraway2016}"),
    ("[Giaccardi et al. 2016]", r"\cite{giaccardi2016}"),
    ("[Wakkary et al. 2017]", r"\cite{wakkary2017}"),
    ("[Perovich et al. 2021]", r"\cite{perovich2021}"),
    ("[Lefebvre 2004]", r"\cite{lefebvre2004}"),
    ("[Key et al. 2025]", r"\cite{key2025}"),
    ("[Devendorf et al. 2023]", r"\cite{devendorf2023}"),
    ("[Brantley et al. 2007]", r"\cite{brantley2007}"),
    ("Nicenboim et al. [2025]", r"Nicenboim et al.~\cite{nicenboim2025}"),
    ("Loukissas [2019]", r"Loukissas~\cite{loukissas2019}"),
    ("Gabrys [2016]", r"Gabrys~\cite{gabrys2016}"),
    ("Ingold [2022]", r"Ingold~\cite{ingold2022}"),
    ("Bastian and Bayliss Hawitt [2022]", r"Bastian and Bayliss Hawitt~\cite{bastian2022}"),
    ("Oktay et al. [2024]", r"Oktay et al.~\cite{oktay2024}"),
    ("Devendorf, de Koninck, and Sandry [2022]", r"Devendorf, de Koninck, and Sandry~\cite{devendorf2022}"),
    ("Friske, Wirfs-Brock, and Devendorf [2020]", r"Friske, Wirfs-Brock, and Devendorf~\cite{friske2020}"),
    ("Jansen et al. [2015]", r"Jansen et al.~\cite{jansen2015}"),
    ("Purdue et al. [2025]", r"Purdue et al.~\cite{purdue2026}"),
]

FIG1 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig01_overview.png}
  \caption{A shore-to-channel section of the Cotai mudflat, with pick 156 (21 November 2026, 14:45) drawn on the same axis. The dashed line is that pick's tide position. Spoonbills and mangroves sit toward the shore; the air strand sits toward the channel. The earthquake mark is outside the section. No elevation was surveyed.}
  \Description{A shore-to-channel section. Mangroves and spoonbills are on the shore side, tide on the channel side, and an earthquake mark sits outside the section. Below, pick 156 shows seven strands on the same axis.}
  \label{fig:section}
\end{figure}
"""

FIG2 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig02_process.png}
  \caption{Three drawings: the section, seven tracks whose tick counts stand for each period, and one tide float of length 8 on the satin ground. The middle drawing is not a sound recording.}
  \Description{Three panels. A mudflat section, seven period tracks, and a satin ground with one tide float.}
  \label{fig:process}
\end{figure}
"""

FIG3 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig03_time.png}
  \caption{Mudflat Clock is one shared bar, 384 woven picks and 96 of forecast, 15 minutes each. Intrinsic Time gives each cycle 24 picks and a different duration. Playback shortens 15 minutes to about 1.1 seconds. A press is not shortened.}
  \Description{Three clocks. A shared 480-pick bar, seven agent cycles of 24 picks with different durations, and playback that compresses 15 minutes to about 1.1 seconds.}
  \label{fig:clocks}
\end{figure}
"""

TAB2 = r"""
\begin{table}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/table02_rules.png}
  \caption{The seven relational tests in the prototype, and the mark each one writes. Thresholds are the ones in the running page.}
  \Description{Seven rules: feed, roost, submerge, draw, disturb, jolt, and press, each with its condition and the mark it writes.}
  \label{tab:rules}
\end{table}
"""

FIG4 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig04_grammar.png}
  \caption{The grammar followed through the tide value of pick 156: 0.72 m, then S and v, then the covered ends, then one repeat of the ground, then that float on the ground. The matrix shows which operation each yarn receives. Open dots occur only on a quake or a press.}
  \Description{Five steps from measured values to one pick, then a matrix of density, position, float, and stitch for seven yarns.}
  \label{fig:grammar}
\end{figure}
"""

FIG5 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig05_stitching.png}
  \caption{The ground is satin with \(n = 1\), and the first four ends are plain weave. Pick 156's tide run is cut at float 8 into 8, 8 and 7; the mangrove run is cut at float 3. Pick 172 carries two roost stitches, at ends 28 and 31, and a jolt every sixth end. The bottom row is all 176 ends of that pick.}
  \Description{Satin ground, the floats of pick 156, the roost and jolt stitches of pick 172, and the full row of that pick.}
  \label{fig:stitch}
\end{figure}
"""

FIG6 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig06_interface.png}
  \caption{The front view and the separated layers are picks 156 and 172. The single-layer panel is the tide of pick 172, first located on the cloth, then cut into floats. The empty frame is for the installation photograph. No treadle is in that photograph.}
  \Description{Composite rows for picks 156 and 172, separated layers, the tide layer cut into floats, and an empty frame for an installation photograph.}
  \label{fig:interface}
\end{figure}
"""

FIG7 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/fig07_participation.png}
  \caption{A designed press, not a saved one. While the spoonbill strand is feeding beside the tide, the press adds a visitor strand. The next eight picks move the spoonbill strand to the shore and drop the feeding stitch. The visitor strand's position in the drawing is not a measured place.}
  \Description{A cloth excerpt in which a press adds a visitor strand beside a feeding spoonbill strand. Later picks move that strand toward the shore.}
  \label{fig:press}
\end{figure}
"""

FIG8 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/patterns/mudflat/composite.png}\\[6pt]
  {\footnotesize Mudflat Clock\par}
  \vspace{8pt}
  \includegraphics[width=\textwidth]{../figures/patterns/intrinsic/composite.png}\\[6pt]
  {\footnotesize Intrinsic Time\par}
  \caption{The composite cloth under Mudflat Clock and under Intrinsic Time, the two views in the project slides. Width runs from shore to channel. Picks accumulate down the cloth. A press is not in these two frames.}
  \Description{Two full composite weaves. The upper cloth is Mudflat Clock and the lower cloth is Intrinsic Time.}
  \label{fig:cloth}
\end{figure}
"""

FIG9 = r"""
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig09_relation.png}
  \caption{Connection, mediator, and composition, drawn as in the project slides. A mark sits where strands meet, between sources, or on a stack of yarns.}
  \Description{Three drawings labelled connection, mediator, and composition. Strands cross, a block sits between separate bars, and stacked yarns carry one binding square.}
  \label{fig:relation}
\end{figure}
"""

TAB1 = r"""
\begin{table}[t]
  \centering
  \includegraphics[width=\textwidth]{../figures/table01_agents.png}
  \caption{The seven agents, each with proxy, source, own period, float, and how it advances on the mudflat clock. The section is Figure~\ref{fig:section}.}
  \Description{Seven agents: air, mangrove, spoonbill, tide, quake, instrument, and visitor, with proxy, source, period, and float.}
  \label{tab:agents}
\end{table}
"""


def slots(text):
    """Replace figure-slot lines. Longer markers first."""
    reps = [
        ("**[FIGURE 2 — Research-through-design process: situated exploration, sound-based studies, and computational weaving iterations]**", FIG2),
        ("**[TABLE 1 — Agent, Environmental Proxy, Data Source, Spatial and Temporal Characteristics, and Weaving Role 参考speculative map 画一个地形剖面图]**", TAB1),
        ("**[INSERT FIGURE 3 HERE — Temporal Translation Architecture: Mudflat Clock and Intrinsic Time]**", ""),
        ("**[FIGURE 3 — Two Temporal Perspectives: Coexistence through Shared Environmental Time and Difference through Agent-Specific Rhythms, with Exhibition Playback as a Third Temporal Layer]**", FIG3),
        ("**[TABLE 2 — Environmental Variables, Temporal Treatment, Strand Parameters, and Relational Conditions]**", TAB2),
        ("**[FIGURE 4 — Computational weaving grammar: Input → Mapping → Structure → Output]**", FIG4),
        ("**[FIGURE 5 — From one pick's strand coverage to conditional inter-layer connections and accumulated digital fabric]**", FIG5),
        ("**[FIGURE 6 — Installation overview: exhibition setup, composite weave, separated layers, and embodied interaction]**", FIG6),
        ("**[INSERT FIGURE — Temporal Outcomes: Shared Mudflat Clock, Agent-Specific Models, and Accumulating Digital Fabric]**", FIG8),
        ("**[INSERT FIGURE — Relational Composition in the Digital Weave: Individual Strands and Conditional Connections]**", ""),
        ("**[INSERT FIGURE — Conditional Binding and Parting: Environmental Conditions and Their Structural Consequences]**", ""),
        ("**[INSERT FIGURE — Exhibition Documentation: Installation, Visitor Interaction, and Evolving Digital Fabric]**", ""),
    ]
    for old, new in reps:
        if old not in text:
            raise SystemExit("missing slot:\n" + old[:80])
        text = text.replace(old, new.strip())
    return text


def esc_text(s):
    s = s.replace("\\", "\\textbackslash{}")
    for a, b in (
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
    ):
        s = s.replace(a, b)
    s = s.replace("₂", r"\textsubscript{2}")
    return s


def markup(s):
    """Citations and code are already tokenised. Escape, then emphasis."""
    tokens = {}

    def hold(m):
        key = f"ZXQ{len(tokens)}QXZ"
        tokens[key] = m.group(0)
        return key

    s = re.sub(r"\\cite\{[a-z0-9,]+\}|\\ref\{[a-z:]+\}", hold, s)
    s = re.sub(r"`([^`]+)`", lambda m: hold(type("M", (), {"group": lambda self, i=0: "\\texttt{" + esc_text(m.group(1)) + "}"})()), s)
    # simpler code hold
    return s, tokens  # placeholder, replaced below


def inline(s):
    chunks = []
    pos = 0
    pattern = re.compile(r"(\\cite\{[a-z0-9,]+\}|\\ref\{[a-z:]+\})")
    # also code
    pattern = re.compile(r"(\\cite\{[a-z0-9,]+\}|\\ref\{[a-z:]+\}|`[^`]+`)")
    parts = []
    for m in pattern.finditer(s):
        parts.append(("text", s[pos:m.start()]))
        parts.append(("keep", m.group(0)))
        pos = m.end()
    parts.append(("text", s[pos:]))
    out = []
    for kind, chunk in parts:
        if kind == "text":
            chunk = esc_text(chunk)
            chunk = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", chunk)
            chunk = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", chunk)
            out.append(chunk)
        elif chunk.startswith("`"):
            out.append("\\texttt{" + esc_text(chunk[1:-1]) + "}")
        else:
            out.append(chunk)
    return "".join(out)


def heading_cmd(num, title):
    dots = num.count(".")
    cmd = {1: "subsection", 2: "subsubsection"}[dots]
    return f"\\{cmd}{{{inline(title)}}}"


PREAMBLE = r"""\documentclass[manuscript,review,anonymous]{acmart}

% DIS 2027 papers: acmart, manuscript, review, anonymous.
% Abstract in the source is 171 words. The call's limit is 150.
% CCS concepts and keywords are a starting set for the template.
% The city is the one in the course briefing of 6 October 2026.
% The call's dates table, as saved in my_work/venue/dis-2027.md, did not name it.

\setcopyright{acmlicensed}
\copyrightyear{2027}
\acmYear{2027}
\acmDOI{10.1145/nnnnnnn.nnnnnnn}
\acmConference[DIS '27]{Designing Interactive Systems Conference}{June 28--July 2, 2027}{Stockholm, Sweden}
\acmISBN{978-1-4503-XXXX-X/27/06}

\begin{document}

\title{Weaving with More-than-Human Rhythms: Temporal and Relational Composition through Environmental Data}

\author{Shiyu Lei}
\affiliation{%
  \institution{University of Macau}
  \city{Macau}
  \country{China}}
\renewcommand{\shortauthors}{Anonymous Author(s)}

\begin{abstract}
@@ABSTRACT@@
\end{abstract}

\begin{CCSXML}
<ccs2012>
<concept>
<concept_id>10003120.10003123.10010860</concept_id>
<concept_desc>Human-centered computing~Interaction design process and methods</concept_desc>
<concept_significance>500</concept_significance>
</concept>
<concept>
<concept_id>10003120.10003121.10003126</concept_id>
<concept_desc>Human-centered computing~HCI theory, concepts and models</concept_desc>
<concept_significance>300</concept_significance>
</concept>
</ccs2012>
\end{CCSXML}

\ccsdesc[500]{Human-centered computing~Interaction design process and methods}
\ccsdesc[300]{Human-centered computing~HCI theory, concepts and models}

\keywords{computational weaving, more-than-human design, temporal design, environmental data, research through design}

\maketitle
"""


def convert(md):
    md = md.split("## Reference")[0]
    md = slots(md)
    md = md.replace("support.The resulting", "support. The resulting")
    md = re.sub(r"【[^】]*】", "", md)
    for src, dst in CITES:
        md = md.replace(src, dst)
    # Figure 1 must be the first figure so the printed FIG. numbers match.
    md = md.replace(
        "## Related Work",
        FIG1.strip() + "\n\n## Related Work",
        1,
    )
    # Figure 7 before any later figure, at the treadle subsection.
    md = md.replace(
        "**3.6.3 Navigating and Attending to the Weave**",
        FIG7.strip() + "\n\n**3.6.3 Navigating and Attending to the Weave**",
        1,
    )
    # Slide 7's three drawings, after the sentence that names the operations.
    needle = "We understand this relational role of data through three connected operations: **connection, mediation, and composition**."
    if needle not in md:
        raise SystemExit("relation sentence missing")
    md = md.replace(needle, needle + "\n\n" + FIG9.strip(), 1)

    abstract = re.search(r"## Abstract\n\n(.+?)\n\n## Introduction", md, re.S).group(1).strip()
    body = re.search(r"## Introduction\n\n(.*)\Z", md, re.S).group(1).strip()

    blocks = re.split(r"\n\s*\n", body)
    expanded = []
    for block in blocks:
        b = block.strip()
        if re.match(r"\d+\.\s+", b):
            expanded.extend(re.split(r"\n(?=\d+\.\s+)", b))
        else:
            expanded.append(b)
    blocks = expanded
    out = []
    enum = False

    def close_enum():
        nonlocal enum
        if enum:
            out.append("\\end{enumerate}")
            enum = False

    for block in blocks:
        b = block.strip()
        if not b:
            continue
        if b.startswith("\\begin{figure}") or b.startswith("\\begin{table}"):
            close_enum()
            out.append(b)
            continue
        m = re.match(r"^##\s+\*{0,2}(?:\d+\.\s+)?(.+?)\*{0,2}\s*$", b)
        if m:
            close_enum()
            out.append("\\section{" + inline(m.group(1)) + "}")
            continue
        m = re.match(r"^\*\*(\d+(?:\.\d+)+)\s+(.+?)\*\*$", b)
        if m:
            close_enum()
            out.append(heading_cmd(m.group(1), m.group(2)))
            continue
        m = re.match(r"^(\d+)\.\s+(.+)$", b, re.S)
        if m:
            if not enum:
                out.append("\\begin{enumerate}")
                enum = True
            out.append("\\item " + inline(m.group(2)))
            continue
        close_enum()
        out.append(inline(b))

    close_enum()
    tex = PREAMBLE.replace("@@ABSTRACT@@", inline(abstract))
    tex += "\\section{Introduction}\n\n" + "\n\n".join(out)
    tex += "\n\n\\bibliographystyle{ACM-Reference-Format}\n\\bibliography{references}\n\n\\end{document}\n"
    return tex


def main():
    raise SystemExit(
        "main.tex uses screenshots from the slides PDF. "
        "Running this script would put the older generated figures back."
    )
    tex = convert(SRC.read_text(encoding="utf-8"))
    if "【" in tex or "参考speculative" in tex or "INSERT FIGURE" in tex:
        raise SystemExit("working note survived")
    if tex.count("\\begin{figure}") != 9:
        raise SystemExit("figure count " + str(tex.count("\\begin{figure}")))
    if tex.count("\\begin{table}") != 2:
        raise SystemExit("table count")
    if "weaving-insp " not in tex and "weaving-insp\n" not in tex:
        raise SystemExit("truncated sentence was altered")
    OUT.write_text(tex, encoding="utf-8")
    print(OUT, "chars", len(tex))


if __name__ == "__main__":
    main()
