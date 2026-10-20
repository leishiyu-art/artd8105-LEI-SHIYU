# Declarations

ARTD8105 · Session 4 · course project proposal stance (not the Nake studio exercise).  
About two minutes each in class; no slides. None of this binds until 7 October.

---

## Territory

I keep circling **cross-species communication**: whether technology can support encounter between humans and other species that is not translation into human language and not nature-as-decoration. I draw on **new materialism**, **intersectional ecofeminism**, and **actor-network theory (ANT)**.

I want a **generative system with two non-equivalent agencies**:

1. a **nonhuman / environmental signal** that rewrites part of the generative rule-space (shared control over the making); and  
2. an **AI prompt layer aimed at the human** — not to speak *for* other species, but to **push / prompt the human toward other kinds of agency** (decentering, noticing extractive mappings, slowing the urge to beautify or translate).

So the question is double: what “communication” means when control is shared with nonhumans, **and** how AI can promote a human → other-species / other-agency orientation without recentring human interpretation of the other.

---

## Where it came from

- Reading notes: `my_work/reading_notes/nicenboim2024.md` (more-than-human / decentering; AI tactics that situate / materialize / enact — useful for the **human-facing** AI layer)  
- Reading notes: `my_work/reading_notes/galanter2003.md` (generative systems and ceding control — method reference)  
- Theory still to log with DOI: new materialism; intersectional ecofeminism; ANT  
- Own practice: instruction → parameters → generative tool (`instruction.md`, `parameters.md`, `tools/tool.html`) as a **method** for shared-control systems, not as the project’s subject  

---

## The rung

Ladder: `rule in 2D → rule in 3D → external data → live input → capture → learned models`

**I choose: external data as the core material rung**, with a **limited, human-facing AI prompt layer** on top (not a model that classifies animals).

**Why:**  
- Nonhuman traces must change the generative process (external data) if other beings are actants.  
- AI enters as **prompting the human** toward other agencies — aligned with decentering — **not** as a translator or detector of what the other “means.”  
- I still refuse learned models trained to label or speak for another species; that would recentre human meaning-making under an ecofeminist critique.

---

## The field

**Conversation:** multispecies / more-than-human design; Animal-Computer Interaction; critical AI + decentering; practice-led generative systems.

**Candidate venues (unverified — I will check CFP and fit myself):**

1. **ACI — International Conference on Animal-Computer Interaction**  
2. **ACM DIS (Designing Interactive Systems)**  
3. **ACM CHI** *or* **SIGGRAPH / SIGGRAPH Asia Art Papers / Art Gallery** (not the main technical track)

---

## What you would make

### One sentence

I would make **Co-Constraint**: a small generative drawing system where (1) one nonhuman/environmental data stream rewrites a few authored parameters, and (2) an AI layer prompts **me** to reorient toward other agencies — without claiming to know what the other species is saying.

### What the system is (v1 architecture)

Five parts. Keep v1 small.

```text
[Nonhuman / environmental signal] ----maps to----> [2–3 generative parameters]
                                                      |
[Human protocol: authored rules] -----------------> [Generative 2D engine] --> drawing
                                                      ^
[AI prompt layer → HUMAN only] -----questions / slows / decenters the human’s edits
```

**1 · Human protocol**  
I author the rule types (density, rhythm, permission to mark, bounds). I do not paint frame by frame.

**2 · Nonhuman channel (external data, one stream)**  
One restrained input: e.g. humidity/light by a plant, or a field recording reduced to a time series — **not** species labels. This stream rewrites parameters. It is never sent to an LLM to be “explained.”

**3 · Mapping table (shared control)**  
Visible mapping: signal bands → only 2–3 parameters. I may change the mapping ranges; I may not override live values to make a prettier frame.

**4 · AI prompt layer (human → other agency)**  
AI talks **to the human author**, not for the animal. Examples of what it may do:

- ask which constraints I am unwilling to share, and why;  
- flag when my mapping looks extractive (signal only used to decorate);  
- propose a decentering move (e.g. widen what the signal can rewrite; remove a human-only aesthetic override);  
- refuse to provide “the animal said X” narratives.

AI must **not**: classify the species on screen, invent the other’s voice, or auto-beautify the image.

This is the “AI promoting human → other kind of species / agency” part: **prompting as orientation**, not promotion-as-marketing and not translation-as-speech.

**5 · Output**  
Accumulating generative drawing + raw signal graph + list of parameters currently rewritten + the latest human-facing prompt. Optional later: SVG / small plotter print as evidence.

### What would still surprise me

If the AI prompts change what I am willing to author — and if some prompts make the nonhuman channel *more* present in the rule-space while making the picture *less* flattering — that tension is a finding.

### What I am not making (v1)

- An AI that translates or speaks for another species  
- A classifier of animal behaviour or emotion  
- A prompt-to-image tool that only *looks* ecological  
- A large multi-animal installation  

### Next decisions I still owe

1. **Which** nonhuman channel and **where** (site / accountability).  
2. How the AI is constrained (scripted critique vs limited LLM with a hard system prompt that forbids translation-of-the-other).  
3. Screen-only first, or small physical output.  

---

## The pairing sentence

I am going to make **Co-Constraint, a generative drawing system co-driven by one nonhuman data stream and an AI layer that prompts the human toward other agencies**, using **authored rules, a visible signal-to-parameter mapping, external data, and human-facing AI prompts that refuse to speak for other species**, and it would tell someone in **more-than-human design / ACI / critical AI** that **AI can support cross-species encounter by reorienting human authorship — not by translating other beings into human meaning**.
