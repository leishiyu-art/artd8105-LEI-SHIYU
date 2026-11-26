#!/usr/bin/env python3
"""Reading proof of main.tex. Not a substitute for acmart.

Chrome prints this to PDF when LaTeX is not installed. The submission
source remains main.tex.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEX = (ROOT / "main.tex").read_text(encoding="utf-8")

REFS = {
    "giaccardi2020": "Elisa Giaccardi and Johan Redström. 2020. Technology and More-Than-Human Design. <em>Design Issues</em> 36, 4 (2020), 33–44.",
    "wakkary2021": "Ron Wakkary. 2021. <em>Things We Could Design: For More Than Human-Centered Worlds</em>. MIT Press, Cambridge, MA.",
    "loukissas2019": "Yanni Alexander Loukissas. 2019. <em>All Data Are Local: Thinking Critically in a Data-Driven Society</em>. MIT Press, Cambridge, MA.",
    "gabrys2016": "Jennifer Gabrys. 2016. <em>Program Earth: Environmental Sensing Technology and the Making of a Computational Planet</em>. University of Minnesota Press, Minneapolis, MN.",
    "pschetz2018": "Larissa Pschetz and Michelle Bastian. 2018. Temporal Design: Rethinking Time in Design. <em>Design Studies</em> 56 (2018), 169–184.",
    "zimmerman2007": "John Zimmerman, Jodi Forlizzi, and Shelley Evenson. 2007. Research Through Design as a Method for Interaction Design Research in HCI. In <em>Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI ’07)</em>. ACM, New York, NY, USA, 493–502.",
    "gaver2012": "William Gaver. 2012. What Should We Expect from Research Through Design? In <em>Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI ’12)</em>. ACM, New York, NY, USA, 937–946.",
    "latour2005": "Bruno Latour. 2005. <em>Reassembling the Social: An Introduction to Actor-Network-Theory</em>. Oxford University Press, Oxford.",
    "haraway2008": "Donna J. Haraway. 2008. <em>When Species Meet</em>. University of Minnesota Press, Minneapolis, MN.",
    "haraway2016": "Donna J. Haraway. 2016. <em>Staying with the Trouble: Making Kin in the Chthulucene</em>. Duke University Press, Durham, NC.",
    "giaccardi2016": "Elisa Giaccardi, Nazli Cila, Chris Speed, and Melissa Caldwell. 2016. Thing Ethnography: Doing Design Research with Non-Humans. In <em>Proceedings of the 2016 ACM Conference on Designing Interactive Systems (DIS ’16)</em>. ACM, New York, NY, USA.",
    "wakkary2017": "Ron Wakkary, Doenja Oogjes, Sabrina Hauser, Henry Lin, Cheng Cao, Leo Ma, and Tijs Duel. 2017. Morse Things: A Design Inquiry into the Gap Between Things and Us. In <em>Proceedings of the 2017 Conference on Designing Interactive Systems (DIS ’17)</em>. ACM, New York, NY, USA, 503–514.",
    "nicenboim2025": "Iohanna Nicenboim, Doenja Oogjes, Heidi Biggs, and Seowoo Nam. 2025. Decentering Through Design: Bridging Posthuman Theory with More-than-Human Design Practices. <em>Human–Computer Interaction</em> 40, 1–4 (2025), 195–220.",
    "ingold2022": "Tim Ingold. 2022. <em>Imagining for Real: Essays on Creation, Attention and Correspondence</em>. Routledge, London.",
    "perovich2021": "Laura J. Perovich, Sara Ann Wylie, and Roseann Bongiovanni. 2021. Chemicals in the Creek: Designing a Situated Data Physicalization of Open Government Data with the Community. <em>IEEE Transactions on Visualization and Computer Graphics</em> 27, 2 (2021), 913–923.",
    "lefebvre2004": "Henri Lefebvre. 2004. <em>Rhythmanalysis: Space, Time and Everyday Life</em>. Translated by Stuart Elden and Gerald Moore. Continuum, London.",
    "bastian2022": "Michelle Bastian and Rowan Bayliss Hawitt. 2022. Multi-species, ecological and climate change temporalities: Opening a dialogue with phenology. <em>Environment and Planning E: Nature and Space</em>.",
    "oktay2024": "Gizem Oktay, Minha Lee, Bahareh Barati, and Ron Wakkary. 2024. Caring Through: Engaging with Temporality of Care in More-than-Human Design. In <em>Proceedings of the Halfway to the Future Symposium (HTTF ’24)</em>. ACM, New York, NY, USA.",
    "key2025": "Cayla Key, Cally Gatehouse, Stevie Koepp, and Nick Taylor. 2025. Leaky Cups: Tinkering with Hydrofeminist Temporalities for HCI. In <em>Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems (CHI ’25)</em>. ACM, New York, NY, USA, Article 408, 1–17.",
    "devendorf2022": "Laura Devendorf, Sasha de Koninck, and Etta Sandry. 2022. An Introduction to Weave Structure for HCI: A How-to and Reflection on Modes of Exchange. In <em>Proceedings of the 2022 ACM Designing Interactive Systems Conference (DIS ’22)</em>. ACM, New York, NY, USA, 629–642.",
    "devendorf2023": "Laura Devendorf, Kathryn Walters, Marianne Fairbanks, Etta Sandry, and Emma Goodwill. 2023. AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving. In <em>Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (CHI ’23)</em>. ACM, New York, NY, USA, Article 127.",
    "friske2020": "Mikhaila Friske, Jordan Wirfs-Brock, and Laura Devendorf. 2020. Entangling the Roles of Maker and Interpreter in Interpersonal Data Narratives: Explorations in Yarn and Sound. In <em>Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems (CHI ’20)</em>. ACM, New York, NY, USA.",
    "jansen2015": "Yvonne Jansen, Pierre Dragicevic, Petra Isenberg, Jason Alexander, Abhijit Karnik, Johan Kildal, Sriram Subramanian, and Kasper Hornbæk. 2015. Opportunities and Challenges for Data Physicalization. In <em>Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems (CHI ’15)</em>. ACM, New York, NY, USA, 3227–3236.",
    "purdue2026": "Sydney Purdue, Eduardo Puerta, Enrico Bertini, and Melanie Tory. 2026. Stitching Meaning: Practices of Data Textile Creators. <em>IEEE Transactions on Visualization and Computer Graphics</em> 32, 1 (2026), 725–735.",
    "brantley2007": "Susan L. Brantley, Martin B. Goldhaber, and K. Vala Ragnarsdottir. 2007. Crossing Disciplines and Scales to Understand the Critical Zone. <em>Elements</em> 3, 5 (2007), 307–314.",
}

title = re.search(r"\\title\{(.+)\}", TEX).group(1)
abstract = re.search(r"\\begin\{abstract\}\n(.+)\n\\end\{abstract\}", TEX).group(1)
body = TEX.split("\\maketitle", 1)[1].split("\\bibliographystyle", 1)[0]

order = []
for m in re.finditer(r"\\cite\{([a-z0-9,]+)\}", body + abstract):
    for k in m.group(1).split(","):
        if k not in order:
            order.append(k)
missing = [k for k in order if k not in REFS]
if missing:
    raise SystemExit("missing refs " + ",".join(missing))
num = {k: i + 1 for i, k in enumerate(order)}

labels = {}
fi = ti = 0
for m in re.finditer(r"\\begin\{(figure|table)\}.*?\\label\{([^}]+)\}", body, re.S):
    if m.group(1) == "figure":
        fi += 1
        labels[m.group(2)] = f"Figure\u00a0{fi}"
    else:
        ti += 1
        labels[m.group(2)] = f"Table\u00a0{ti}"


def cite_html(keys):
    return "[" + ", ".join(str(num[k]) for k in keys.split(",")) + "]"


def inline(s):
    tokens = []

    def hold(bit):
        tokens.append(bit)
        return f"@@T{len(tokens) - 1}@@"

    s = s.replace("~", "\u00a0")
    s = s.replace(r"\textsubscript{2}", "₂")
    s = s.replace(r"\(", "").replace(r"\)", "")
    s = s.replace(r"\{", "{").replace(r"\}", "}")
    s = re.sub(r"\\emph\{([^{}]*)\}", lambda m: hold("<em>" + html.escape(m.group(1)) + "</em>"), s)
    s = re.sub(r"\\textbf\{([^{}]*)\}", lambda m: hold("<strong>" + html.escape(m.group(1)) + "</strong>"), s)
    s = re.sub(r"\\texttt\{([^{}]*)\}", lambda m: hold("<code>" + html.escape(m.group(1)) + "</code>"), s)
    s = re.sub(r"\\cite\{([a-z0-9,]+)\}", lambda m: hold(cite_html(m.group(1))), s)
    s = re.sub(r"\\ref\{([a-z:]+)\}", lambda m: hold(labels[m.group(1)]), s)
    s = html.escape(s)
    return re.sub(r"@@T(\d+)@@", lambda m: tokens[int(m.group(1))], s)


def float_html(block, kind):
    bits = []
    for m in re.finditer(r"\\includegraphics\[.*?\]\{([^}]+)\}|\\footnotesize\s+(.+?)\\par", block):
        if m.group(1):
            bits.append(f'<img src="{html.escape(m.group(1))}" alt="">')
        else:
            bits.append(f'<p class="flabel">{html.escape(m.group(2).strip())}</p>')
    cap = re.search(r"\\caption\{((?:[^{}]|\\[a-z]+\{[^{}]*\})*)\}", block, re.S)
    label = re.search(r"\\label\{([^}]+)\}", block).group(1)
    name = labels[label]
    caption = inline(cap.group(1).strip()) if cap else ""
    tag = "figure" if kind == "figure" else "figure"
    return f'<{tag} class="{kind}"><div class="frame">{"".join(bits)}</div><figcaption><b>{name}.</b> {caption}</figcaption></{tag}>'


floats = []


def take_float(m):
    floats.append(float_html(m.group(0), m.group(1)))
    return f"@@FLOAT{len(floats) - 1}@@"


body = re.sub(r"\\Description\{(?:[^{}]|\{[^{}]*\})*\}", "", body)
body = re.sub(r"\\begin\{(figure|table)\}.*?\\end\{\1\}", take_float, body, flags=re.S)

parts = []
in_list = False
for block in re.split(r"\n\s*\n", body.strip()):
    b = block.strip()
    if not b:
        continue
    if b.startswith("@@FLOAT"):
        if in_list:
            parts.append("</ol>")
            in_list = False
        parts.append(floats[int(re.search(r"\d+", b).group(0))])
        continue
    m = re.match(r"\\(section|subsection|subsubsection)\{(.+)\}$", b)
    if m:
        if in_list:
            parts.append("</ol>")
            in_list = False
        tag, cls = {
            "section": ("h2", "sec"),
            "subsection": ("h3", ""),
            "subsubsection": ("h4", ""),
        }[m.group(1)]
        attr = f' class="{cls}"' if cls else ""
        parts.append(f"<{tag}{attr}>{inline(m.group(2))}</{tag}>")
        continue
    if b == r"\begin{enumerate}":
        parts.append("<ol>")
        in_list = True
        continue
    if b == r"\end{enumerate}":
        parts.append("</ol>")
        in_list = False
        continue
    if b.startswith(r"\item "):
        parts.append("<li>" + inline(b[6:]) + "</li>")
        continue
    parts.append("<p>" + inline(b) + "</p>")
if in_list:
    parts.append("</ol>")

refs_html = "\n".join(
    f"<li>{REFS[k]}</li>" for k in order
)

author_name = re.search(r"\\author\{(.+)\}", TEX).group(1)
author_email = re.search(r"\\email\{(.+)\}", TEX).group(1)
institution = re.search(r"\\institution\{(.+)\}", TEX).group(1)
author_html = "<br>".join(
    html.escape(bit) for bit in (author_name, institution, author_email)
)

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  @page {{ size: letter; margin: 0.85in 0.95in 0.9in 0.95in; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: white; color: #111; }}
  body {{
    font-family: "Iowan Old Style", Palatino, "Palatino Linotype", Georgia, serif;
    font-size: 11pt; line-height: 1.42;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  h1 {{
    font-size: 16.5pt; line-height: 1.25; font-weight: 600;
    margin: 0 0 0.55em; letter-spacing: -0.01em;
  }}
  .anon {{ margin: 0 0 1.1em; font-size: 11pt; line-height: 1.35; }}
  .abs h2, h2.plain {{
    font-size: 11pt; margin: 1.15em 0 0.35em; font-weight: 700;
  }}
  .abs p {{ margin: 0 0 0.7em; }}
  .meta {{ font-size: 10pt; line-height: 1.4; margin: 0.35em 0; }}
  .meta b {{ font-weight: 700; }}
  body {{ counter-reset: sec; }}
  h2.sec {{ counter-increment: sec; counter-reset: sub; font-size: 13pt; margin: 1.35em 0 0.45em; font-weight: 650; }}
  h2.sec::before {{ content: counter(sec) ". "; }}
  h3 {{ counter-increment: sub; counter-reset: subsub; font-size: 12pt; margin: 1.15em 0 0.35em; font-weight: 650; }}
  h3::before {{ content: counter(sec) "." counter(sub) " "; }}
  h4 {{ counter-increment: subsub; font-size: 11pt; margin: 1em 0 0.3em; font-style: italic; font-weight: 600; }}
  h4::before {{ content: counter(sec) "." counter(sub) "." counter(subsub) " "; font-style: normal; font-weight: 650; }}
  p {{ margin: 0 0 0.62em; text-align: justify; hyphens: auto; }}
  ol {{ margin: 0.2em 0 0.7em 1.2em; padding: 0; }}
  li {{ margin: 0 0 0.4em; text-align: justify; }}
  figure {{ margin: 1em 0 1.15em; break-inside: avoid; page-break-inside: avoid; }}
  figure img {{ width: 100%; height: auto; display: block; }}
  .flabel {{ font-size: 9pt; margin: 0.15em 0 0.55em; text-align: left; }}
  figcaption {{ font-size: 9.5pt; line-height: 1.35; margin-top: 0.4em; text-align: left; }}
  code {{ font-family: "IBM Plex Mono", ui-monospace, Menlo, monospace; font-size: 0.92em; }}
  h2.refshead {{ font-size: 13pt; margin: 1.4em 0 0.5em; }}
  ol.refs {{ list-style: none; margin: 0; padding: 0; counter-reset: ref; }}
  ol.refs li {{
    counter-increment: ref; font-size: 10pt; line-height: 1.35;
    margin: 0 0 0.45em; padding-left: 1.6em; text-indent: -1.6em; text-align: left;
  }}
  ol.refs li::before {{ content: "[" counter(ref) "] "; }}
  h2, h3, h4 {{ break-after: avoid; page-break-after: avoid; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="anon">{author_html}</p>
<section class="abs">
  <h2 class="plain">ABSTRACT</h2>
  <p>{inline(abstract)}</p>
</section>
<p class="meta"><b>CCS Concepts:</b> Human-centered computing → Interaction design process and methods; Human-centered computing → HCI theory, concepts and models.</p>
<p class="meta"><b>Keywords:</b> computational weaving, more-than-human design, temporal design, environmental data, research through design</p>
{''.join(parts)}
<h2 class="refshead">REFERENCES</h2>
<ol class="refs">
{refs_html}
</ol>
</body>
</html>
"""

out = ROOT / "preview.html"
out.write_text(doc, encoding="utf-8")
print(out, "floats", len(floats), "refs", len(order))
