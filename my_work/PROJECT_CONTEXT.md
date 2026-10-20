# PROJECT_CONTEXT — Living Data Forest

> **For Cursor:** This file is the single source of truth for my project. Use it to fill the course templates in this repo. Rules:
> 1. Always follow the structure of the template files in `course/templates/` — never invent your own section headings.
> 2. Never invent references, authors, page numbers, deadlines or review-form criteria. Anything not verified below must be marked `[VERIFY]`.
> 3. Write in clear academic English, short sentences, no filler.
> 4. Do not fill sections I have not been asked to fill (e.g. section 6 of `idea_evaluation.md`).
> 5. Do not add slides to the defence template.

---

## 0. This week's tasks (due Session 8, Wed 14 Oct 2026)

- [ ] `my_work/idea_evaluation.md` v1 — copy from `course/templates/idea_evaluation.md`; fill **sections 1–5 and 7 only**. Assessed.
- [ ] `my_work/literature_verification.md` — closest works, each checked, plus the gap in one sentence.
- [ ] `my_work/venue/<primary>.md` — Venue Interrogation Protocol Phases 1–2 (incl. review form found).
- [ ] `my_work/venue/<backup>.md` — Phase 1 only.
- [ ] Defence — `course/templates/idea_evaluation_defence.pptx`, 5 slides, 3 min + 2 min Q&A. No extra slides.
- [ ] The made thing — what it is, machine/material, booking.

---

## 1. The project in one paragraph

A research-through-design project that builds a **living data forest**: open environmental and biodiversity data are passed through generative algorithms modelled on nonhuman processes (e.g. flocking, slime-mould growth), which translate them into evolving forms across digital and physical media — an interactive interface, embodied/narrative spaces, and a series of 3D-printed artefacts. The aim is to test whether encountering more-than-human data as an inhabitable environment, rather than as a screen chart, can foster kinship among humans, nonhumans, technology and the environment.

- **Author:** doctoral student (first year), University of Macau; field: HCI / more-than-human design / computational social science.
- **Doctoral aim (one sentence):** How can design boost, rebuild and integrate the kinship between the human, nonhuman, technology and the environment?
- **Theory stance (keep light):** more-than-human design; actor-network theory, new materialism, ecofeminism in the background.
- **Why "forest", not "library":** a library collects and classifies (extractive); a forest grows, interconnects and decays. Each dataset keeps its relations (place, beings, time).

## 2. Research questions

- **Overarching RQ:** How can embodied narrative environments built from nonhuman data foster more-than-human kinship?
- **RQ1 (Translation):** How can nonhuman data be translated into spatial, inhabitable, narrative forms while keeping its relational and situated qualities, rather than reducing it to abstract representation?
- **RQ2 (Experience):** How do people experience and describe kinship when they encounter nonhuman data as an embodied environment, compared with screen-based representations of the same data?
- **RQ3 (Participation, optional / future work):** How does co-constructing or tending the data environment shape people's sense of ownership, care, and kinship toward the nonhuman others it represents?

RQ1 = design contribution; RQ2 = empirical contribution; RQ3 links to my earlier IKEA-effect study (building → ownership). This semester: RQ1 + a first look at RQ2.

## 3. Abstract (IMRD, < 250 words) — current version

**Why (Introduction).** Data traced from more-than-human agencies (other species, ecosystems, the planet, and technologies themselves) is now produced continuously and at planetary scale, as environmental sensor networks, satellite monitoring, automated recorders, and citizen-science platforms turn weather, ecosystems, and species encounters into near-real-time data streams, yet it is mostly shown as screen-based charts made for human analysis. Such charts treat these agencies as data subjects rather than co-inhabitants, leaving little room for the embodied encounters through which kinship forms. How more-than-human data can be materialized into inhabitable, narrative form remains an emerging question in HCI and more-than-human design.

**How (Method).** Following a research-through-design approach, we develop a *living data forest*. Open environmental and biodiversity data are passed through generative algorithms modelled on nonhuman processes, which translate them into evolving forms across digital and physical media. These forms are realized as interactive interfaces, embodied experiences, and narrative spaces, alongside a series of physical artefacts, and refined through iterative prototyping, reflective documentation, and early visitor feedback.

**What (Results).** We expect to contribute a working pipeline from open environmental data to embodied form experience, a set of design decisions for translating nonhuman data without claiming to speak for other species, and early accounts of how people relate to a place through its data.

**So what (Discussion).** These outcomes suggest how data environments can move from representation toward relation, and offer a starting point for designing kinship among humans, nonhumans, technology, and the environment.

## 4. Method and pipeline (for "approach" / feasibility sections)

```
open data  →  nonhuman-inspired algorithm (mediator)  →  evolving form  →  material constraints
(weather, birds,   (boids / flocking; slime-mould      (3D core per      (printability: wall ≥ 1.5 mm,
 species records)   trails as option)                   period)           crest radius, integer ribs)
```

- **Algorithm as mediator:** data sets the *conditions*; the algorithm grows/flocks inside them. This makes translation visible (honest) and gives technology a role as an actor in the kinship.
- **Co-Constraint framing (art class):** three agencies — nonhuman data rewrites parameters; material/printer vetoes what can't exist; human + AI layer sets ranges and is prompted to reorient. The AI asks questions, never speaks *as* a species.
- **Geometry base:** my existing Blender model *HarmonicCore* (parametric printable thin shell, 80 mm tall, wall 2 mm). Ribs will come from algorithm trails instead of fixed harmonics.

### Data sources (verified to exist; live access tested in browser = [VERIFY])

| Source | What | Access |
|---|---|---|
| Open-Meteo | weather, wind, rain, soil moisture | free, no key, works in browser JS |
| eBird API 2.0 | bird sightings by hotspot/region | free key, header `x-ebirdapitoken` |
| iNaturalist API | species observations near a point | free, no key; most records CC BY-NC |

- **Candidate prototype site:** Cotai Ecological Zone, Macau (near UM; ~55 ha; wintering black-faced spoonbills; eBird hotspot `L7490611`, sparse: ~37 checklists). The abstract deliberately does **not** name a site.
- **Collector script:** `cotai_collect.py` saves one JSON snapshot per day (`data/YYYY-MM-DD.json` + `data/latest.json`); optional GitHub Action `collect.yml` runs it daily.

### Outputs and timeline (deadline 27 Nov 2026)

| Week | Dates | Done when |
|---|---|---|
| 1 | 13–19 Oct | Proposal in; daily data collection running |
| 2 | 20–26 Oct | Boids/trails sketch running on real data |
| 3 | 27 Oct–2 Nov | One printable core from one day's data; test print |
| 4 | 3–9 Nov | Website v1 (three.js scene, flock, core, day scrubber) online |
| 5 | 10–16 Nov | Visual polish; weekly cores printing |
| 6 | 17–23 Nov | Hover provenance, visitor trace; 3–5 people try it |
| Final | 24–27 Nov | Documentation, video, written reflection |

Aesthetic: delicate, slow, nonhuman pace; palette from mudflat grey-brown, spoonbill white, black, one muted tidal blue; thin lines, translucent material.

### Risks and fallbacks

| Risk | Fallback |
|---|---|
| Sparse bird data | Treat sightings as events; weather as the continuous stream; collect from week 1 |
| Printer access / print time | Test-print in week 3; FDM PLA if resin unavailable |
| Still human-centric framing | Make it a studied tension; show provenance; AI asks, never speaks for species |
| Scope creep | No VR, no full user study this semester |

## 5. Literature — closest works (status for `literature_verification.md`)

Mark each as checked only after opening the paper. `[OK]` = citation confirmed via publisher/repository page; `[VERIFY]` = still needs opening.

1. **Biggs, H. R., Desjardins, A., et al. (2021).** *Watching Myself Watching Birds.* CHI '21. doi:10.1145/3411764.3445329 `[OK citation; full title subtitle VERIFY]` — first-person design with bird-watching data. **Differs:** personal reflection, not inhabitable narrative environment.
2. **Lee, Y., & Pschetz, L. (2024).** *Pheno-data: Knowledge from tomatoes' becoming with different ecological worlds.* CHI EA '24 (alt.chi). `[OK]` — data from other-than-human perspectives. **Differs:** conceptual/speculative, no embodied data environment.
3. **Lee, Y., Pschetz, L., Karyda, M., et al. (2024).** *Ecological data for manifesting the entanglement of more-than-human livingness.* DIS '24 Companion (workshop). doi:10.1145/3656156.3658388 `[OK]` — data as livingness, relational, situated.
4. **Guerrero Millan, C., Rattay, S., & Lee, Y. (2024).** *A Manifesto for Other-Than-Human Imaginaries of Data.* NordiCHI Adjunct 2024 (presented at DIS 2024). `[VERIFY venue]`
5. **Perovich, L. J., Wylie, S. A., & Bongiovanni, R. (2020).** *Chemicals in the Creek: Designing a situated data physicalization of open government data with the community.* IEEE VIS 2020 / TVCG. arXiv:2009.06155 `[OK; TVCG volume VERIFY]` — situated environmental physicalization. **Differs:** human-centred civic data, not more-than-human kinship.
6. **DataGarden: Exploring our community in a VR data visualization (2023).** CHI '23. arXiv:2310.11521 `[VERIFY authors]` — data as immersive VR space. **Differs:** human community data.
7. **Jansen, Y., et al. (2015).** *Opportunities and challenges for data physicalization.* CHI '15, 3227–3236. doi:10.1145/2702123.2702180 `[OK]` — foundation of the field.
8. **Bae, S. S., Zheng, C., et al. (2022).** *Making Data Tangible: A Cross-disciplinary Design Space for Data Physicalization.* CHI '22. doi:10.1145/3491102.3501939 `[OK]`
9. **Physecology: A Conceptual Framework to describe Data Physicalizations in their Real-World Context (2022).** ACM TOCHI 29(3). doi:10.1145/3505590 `[VERIFY authors]`
10. **Heitlinger, S., Taylor, A., Clarke, R., et al. (2022).** *More-than-Human Data Interactions in the City* (project booklet, MoTH Cities). doi:10.25383/city.19391570 `[OK]` — urban multispecies data. Not peer-reviewed; use as context.
11. **Infotropism: living and robotic plants as interactive displays (2004).** DIS '04. doi:10.1145/1013115.1013145 `[VERIFY authors]` — living plants as data displays.
12. **Chang, M., Shen, C., & Maheshwari, A. (2022).** *Patterns and Opportunities for the Design of Human-Plant Interaction.* DIS '22. `[OK]`
13. **Giaccardi, E., Lenzi, S., Speed, C., Tsaknaki, V., & Zhou, J. (2026).** *More-than-human data practices* (track editorial). DRS 2026. doi:10.21606/DRS.2026.118 `[OK]` — data as relation; nonhumans as data co-producers.
14. **Morais, L., et al. (2024).** *From Exploration to End of Life: Unpacking Sustainability in Physicalization Practices.* CHI '24. arXiv:2402.09860 `[OK]` — relevant to printing many artefacts.

**Gap in one sentence (draft):**
> Data physicalization and immersive visualization have made data tangible and spatial, and more-than-human design has reframed data as relational and co-produced, but few works materialize more-than-human data into embodied, narrative environments or examine whether such encounters foster kinship.

## 6. Venues

- **Primary: ACM DIS 2027** (Designing Interactive Systems) — papers and pictorials; strong fit for more-than-human design and research through design. Phase 1: call, tracks, deadline, page limits. Phase 2: find the reviewer form / review criteria. All 2027 details `[VERIFY]` on the official site.
- **Backup: ACM TEI 2027** (Tangible, Embedded and Embodied Interaction) — fits physical artefacts and embodied interaction. Phase 1 only. `[VERIFY]`

## 7. The made thing

- **What:** one data-driven printed core — the first "tree" in the living data forest series.
- **Machine / material:** SLA resin printer, translucent resin, if available at UM; otherwise FDM, PLA. Approx. 80 mm tall, wall ≥ 1.5 mm.
- **Booking:** `[TO FILL: makerspace name, date, slot]`

## 8. Defence (5 slides, 3 min ≈ 35 s each)

1. **Problem** — more-than-human data shown only as screen charts for humans.
2. **Question + gap** — overarching RQ + gap sentence.
3. **Approach** — the pipeline diagram (data → algorithm → form → material).
4. **Venue + fit** — DIS 2027 + one review criterion I will meet.
5. **Plan + made thing** — 6-week timeline + first printed core.

**Likely questions to prepare:**
- "Isn't this still human-centric?" → Yes, any representation for humans is; I make it a studied tension, show data provenance, and the system never speaks *for* species.
- "Why 3D/environment rather than 2D?" → RQ2 tests exactly that against screen-based representations of the same data.
- "Is the data reliable?" → Weather is continuous and modelled; bird/species records are human encounters, so I present them as encounters, not ground truth.
