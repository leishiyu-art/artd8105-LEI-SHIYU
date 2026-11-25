---
title: "AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving"
authors: "Laura Devendorf, Kathryn Walters, Marianne Fairbanks, Etta Sandry, Emma Goodwill"
year: 2023
venue: "CHI 2023, Hamburg"
venue_type: "conference"
doi_or_url: "https://doi.org/10.1145/3544548.3581571"
verified: true
stream: "personal"
topic_tags: []         # 你来填，例如 weaving / parametric-design / notation / craft-hci
subconversation: ""
relevance: ""          # core | adjacent | background | rejected — 你来选
date_read: 2026-11-22
---

# AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving

## 1 · Why this paper

This CHI ’23 Honorable Mention paper is the foundational HCI reference for **computational weaving as notation**.Because *Polyrhythm Loom* relies on a *"weaving-inspired computational grammar"* to translate ecological signals into digital strands and conditional inter-layer connections, I need to engage directly with Devendorf et al.’s argument that parametric dataflows formalize weave logic—and show how my work pushes that notation from *static fabrication* into *unfolding temporal relations*.

## 2 · Summary

- What it talks about: Presents the overhaul of **AdaCAD**—an open-source web-based weave drafting workspace—into a parametric dataflow tool, co-developed and evaluated with experimental weavers (Walters, Sandry, Fairbanks).
- Main contributions: (1) A parametric **dataflow architecture** encoding weave structures and manipulations as modular,chainable "operations"; (2) an empirical/first-person account of how weavers use parametric notation to document and explain complex multi-layer structures; (3) a theoretical framing of parametric weave drafts as **boundary objects**bridging textile craft and HCI engineering.
- Problem & importance: Smart textiles in HCI demand deep structural weaving knowledge (e.g., multi-layer pockets,conductive paths), yet traditional CAD drafting tools hide the *generative logic* behind a finished drawdown, making cross-disciplinary collaboration and adaptation across looms difficult.
- Innovation & benefits: Instead of editing pixel-by-pixel drafts, designers wire operations together via inlets and outlets; changing any upstream parameter propagates automatically through the entire structure, turning weave logic into a legible, shareable, and remixable specification.
- Advance over prior work: Extends earlier *AdaCAD* (CHI ’19) and traditional weaving notation by treating **parametric dataflows** not merely as automation, but as an evolved *notational language* that makes tacit structural reasoning explicit between craftspeople and engineers.

## 3 · Critical thinking

- Pre-loom determinism vs. on-loom improvisation: Encoding weave logic as a dataflow graph privileges *upfront structural planning* before a file is sent to a Jacquard/TC2 loom. It struggles to capture live, improvisational adjustments made at the loom in response to yarn tension or breakage (a gap the lab itself later had to patch with hardware in *Loom Pedals*, TEI ’24).
- "Boundary object" still leans toward software mental models: Node-and-wire dataflows (operations, inlets, outlets,parameter propagation) naturally speak to computer scientists and CAD users, but they still abstract away physical yarn behavior (twist, elasticity, shrinkage). Craftspeople have to translate tactile intuition into directed graphs, while engineers still aren't forced to confront material physics.
- Elite collaborator bias: The evaluation centers on collaborations with leading experimental textile scholars (Walters,Sandry, Fairbanks) who already straddle craft and computation, leaving open how well parametric notation works for traditional weavers or pure CS/HCI researchers.

## 4 · Creative thinking

- Sparks: AdaCAD’s core insight—that **dataflows make structural relationships explicit and mutable**—directly mirrors *Polyrhythm Loom*’s computational grammar. The difference is what flows through the graph: AdaCAD flows *static geometric parameters* to produce a fixed fabric, whereas *Polyrhythm Loom* flows *heterogeneous ecological temporalities* so the digital fabric continuously accumulates, shifts, or interrupts its inter-layer bindings.
- New application: *Polyrhythm Loom* could export its live ecological weave states as AdaCAD-compatible drafts or drawdowns, letting visitors physically weave a "time-slice" of Cotai mudflat relations on a Jacquard loom.
- Alternative method: Instead of asking humans to manually wire parametric nodes to design a cloth, *Polyrhythm Loom* treats **environmental signals and visitor presence as live parameters** that continuously re-wire conditional inter-layer connections in real time.

## 5 · Form — read it as a genre, not just as content

- Length & venue format: **18 pages** (CHI ’23 Article 127, ACM single-column format).
- First contribution claim (from Abstract / Research page):
  > *"Through our design and evaluation of AdaCAD we found that parametric design helps weavers notate and explain the logics behind the complex structures they generate."*
- Genre & structure: **Systems + RtD/First-Person Collaboration paper**—combines open-source tool building (TypeScript dataflow workspace) with collaborative textile case studies and theoretical reflection (histories of woven notation + boundary object theory).
- Artifact vs. analysis: Balances **system architecture/notation design** with **qualitative case studies** of actual woven artifacts produced by collaborating weavers.
- Related work: Connects (1) craft/weaving integration in HCI, (2) histories of woven notation (from punchcards to modern drafting), and (3) Star & Griesemer’s **boundary object theory**.
- Process evidence: First-person research, collaborative residency/sampling outputs (e.g., multi-layer lattices,drafts/dataflows), and qualitative feedback from smart-textile weavers—not a lab usability experiment with p-values.
- Voice & tense: First-person plural (*"we"*); present tense for tool architecture and theoretical claims, past tense for design/evaluation findings.

## 6 · Venue signal

Winning a **CHI Honorable Mention** proves that deeply craft-rooted, open-source toolmaking paired with **theoretical reframing** (*"parametric design as notation / boundary object"*) can triumph even at metrics-heavy CHI. For **DIS**, this is an even stronger green light: DIS *loves* textile-computation hybrids (e.g., *Weaving Textile-form Interfaces* at DIS ’23,*Animated Linen* and *Design Bookkeeping* at DIS ’24—all of which build on AdaCAD). To stand out at DIS, pair your *Polyrhythm Loom* artifact with a clear **notational/grammatical contribution** (how your computational grammar represents *relation* and *temporality*) rather than just showing an interactive installation.

## 7 · Take-home

- Learned & new: Reframing a software/algorithmic mechanism as **notation**—a medium that externalizes and communicates structural logic—is a super persuasive way to elevate technical implementation into design theory.
- Application: Cite *AdaCAD* (CHI ’23) in *Polyrhythm Loom*’s Related Work to ground **"computational weaving"** in HCI,then clearly distinguish your move: AdaCAD uses parametric notation to *author* static physical structures, whereas *Polyrhythm Loom* uses a weaving-inspired grammar to *mediate* live, asynchronous more-than-human temporalities.
- Good writing sample? **Yes**, especially conceptually—pairing a working open-source computational tool with first-person craft collaborations and a sharp sociological lens (*boundary objects*) is a classic Devendorf/Unstable Design Lab playbook worth studying closely.

