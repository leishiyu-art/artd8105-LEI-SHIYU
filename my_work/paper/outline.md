# Weaving With: Polyrhythm Loom — DIS Paper Outline

11 Nov 2026 · @blueeegho

English extracted from the bilingual outline supplied by the student. Wording unchanged. Chinese lines removed.

## Title

Weaving With: Polyrhythm Loom — Composing More-than-Human Temporalities into a Shared Cloth

**Alternative:** Separate and Align: Designing for Polyrhythmic Co-presence of More-than-Human Agents through Computational Weaving

**Paper type:** Research through Design paper. The contribution is both an artifact (Polyrhythm Loom) and the methods and concepts drawn from the design trajectory from Listening Sea to the Loom.

## Contributions

Listed at the end of the Introduction.

1. **Design artifact:** Polyrhythm Loom, a digital loom driven by the intrinsic rhythms of seven agents, with the human as one voice among them.
2. **Method:** The recompile pipeline (complex data → simple data → weaving data → pixel → textile), which compiles heterogeneous time scales into one weaving rhythm.
3. **Concept:** "Separate and align", a temporal design strategy that keeps each agent's intrinsic time while aligning them to a common clock.
4. **Reflection on the trajectory:** The move from the single-source Listening Sea to a multi-agent, situated Cotai mudflat; the reasons behind each turn are knowledge in themselves.

## Abstract

150–200 words, written last.

Problem (data visualization flattens nonhuman time onto a human clock) → what we made → method → key insight → significance for MtHD/HCI.

## 1. Introduction (~10%)

- **Hook:** On the Cotai mudflat, tidal cycles, the geological time of sedimentation, the seasonal rhythm of migratory birds and human commuting hours all coexist, yet most environmental data interfaces put them on the same x-axis.
- **Problem:** MtHD calls for decentering, but at the level of data, time has rarely been designed with care. Visualization by default is read by humans, one-way, and unified by clock time.
- **RQs**
  - **RQ1** How can design make heterogeneous more-than-human temporalities perceivable without collapsing them into human clock time?
  - **RQ2** As a computational-material metaphor and technique, what does weaving (warp and weft interlacing, the shed, cloth accumulating) offer to "data as relation"?
  - **RQ3** When the human is only one of seven agents and steps back to watch and listen, how is the encounter between people and data reconfigured?
  - **Note:** the course version involves no human participants, so RQ3 is answered as design reflection, not empirical findings; a study is added for the DIS submission.
- **Contribution list**

## 2. Related Work (~20%)

Each subsection ends with what it means for this project and what gap it leaves; a final paragraph sums up the gap.

### 2.1 More-than-Human Design in HCI

Theoretical roots of decentering (posthumanism, entanglement HCI) and practice (human–fungi, birdwatching, multispecies participation in smart cities). Key point: most work addresses who takes part, rarely when or at what rhythm.

### 2.2 Time, Rhythm and Temporality in Design

Temporal design, slow technology, rhythmanalysis, Tsing's polyphonic assemblage, Bastian's critique of clocks in ecological crisis, slow violence. This is the paper's most distinctive theoretical anchor and can be given more space.

### 2.3 Data Physicalization and Situated Data

Opportunities and challenges of physicalization, data feminism, "all data are local", Dear Data-style handmade data. Leads to: on-site sensing (your own sensors on the mudflat) versus public APIs (Orcasound).

### 2.4 Weaving, Computation and Textile Interfaces

Jacquard and the history of computing, weaving as binary art and an algebra of patterns, smart textiles and double weaving in HCI. Leads to: weaving is not just an output medium; its structure (warp = time, weft = one pick by an agent) is itself a grammar of relation.

## 3. Conceptual Framework (~10%)

- **3.1 Data as relation:** Data is not an abstract representation of the world but a relation lived and felt in interaction.
- **3.2 Agent classification: critical-zone spheres × rhythm:** The spheres of the Critical Zone (lithosphere, hydrosphere, atmosphere, biosphere…) on one axis, rhythm types on the other; explain why this framework rather than species taxonomy.
- **3.3 Separate and align:** Common clock and intrinsic time side by side; each agent centred on its own cycle, then how many cycles are compiled into one weaving rhythm.
- **3.4 Polyrhythm:** How cycles repel and cooperate (resonance, off-beats, "nodes" where phases coincide).

## 4. Methodology (~8%)

- Research through Design, presenting iterations as an annotated portfolio.
- Team and roles: you, the professors, a textile-artist friend, technicians.
- Process materials: build log, design decision records, AI-assisted workflow (Cursor + MCP automated modelling) as part of methodological transparency.
- Ethics: no human participant data collected at this stage; exhibition observations are informal.

## 5. Design Trajectory (~15%)

This is the "development of the research". Each stage follows the same structure: what we did → what we found → why we turned.

- **5.1 Listening Sea (Orcasound):** A single agent, a live hydrophone, the built-in narrative of ship noise masking orcas, remote listeners diluting the audience's ego. Reason to turn: a single data source, too far from the designer's own situation, so it was repositioned as a process piece.
- **5.2 From one voice to many:** Beginning to classify agents and introducing the spheres framework.
- **5.3 The time-lens variant (discarded):** Why it was dropped, and why "it doesn't work aesthetically" is a valid judgement in RtD.
- **5.4 Choosing a shared scenario:** From a patchwork of random frequencies to a shared narrative; the Wenchuan earthquake window was dropped (too heavy, ethically and emotionally) in favour of the Cotai mudflat (local, can be sampled in person); earthquakes remain as distant events passing through.
- **5.5 From material loom to digital-first:** The jacquard and the GS-S252 flat knitting machine were put on hold in favour of a tablet plus acrylic layers; the audience moved from "weaving their own cloth" to "one of seven collaborators", then to "stepping back to watch and listen".

## 6. Polyrhythm Loom: The System (~15%)

### 6.1 Scenario & seven agents

| Agent | Sphere | Source | Period | 1 pick |
|---|---|---|---|---|
| CO₂ | Atmosphere | NOAA Mauna Loa | 1 yr | 15 days |
| Daylight · plants | Biosphere | SMG sunshine / solar elevation | 1 day | 1 h |
| Black-faced spoonbill | Biosphere | HKBWS census / Macau counts | 1 yr | 15 days |
| Tide | Hydrosphere | SMG tide tables | 12.42 h | 31 min |
| Mud · sediment | Lithosphere | On-site sensors | TBD | TBD |
| Device | Technosphere | Measured live | 1 s | 0.04 s |
| Visitor | — | Treadle, no personal data | — | 1 press |

Open question: the period and sensor plan for mud · sediment still need to be confirmed.

### 6.2–6.5

- **6.2 Recompile pipeline:** A five-step diagram; what each step loses and keeps (an honest account of the cost of simplification).
- **6.3 Weaving grammar:** Mapping rules for warp, weft, colour and nodes; how different cycles are compiled into shuttle rhythm; key time points labelled as nodes.
- **6.4 Interface:** The layered-loom web page, real-time data, labelled nodes.
- **6.5 Installation:** A tablet plus parallel acrylic layers (one cloth from the front, separate layers from the side): the physical form of "separate and align"; treadle (Arduino UNO R4 WiFi) with sound and vibration feedback.

## 7. Exhibition as Encounter (~7%)

Deployment of the November exhibition, spatial constraints, informal observations (no claims). Can be written as first-person designer observation, marked as the place where the DIS version adds a study.

## 8. Discussion (~12%)

- **8.1 Separate and align as a temporal design strategy:** Intermediate-level knowledge transferable to other MtHD data projects.
- **8.2 Weaving as a relational data grammar:** Cloth accumulates and interlacing is relation, an ontology different from a chart's.
- **8.3 Decentering, and its limits:** The human is one voice and steps back; but directly answer the expected objection: the mapping rules are still written by humans, so is this still human-centred? Position: acknowledge the tension and explain why decentering at the level of narrative and concept still has value, rather than claiming to "let species speak".
- **8.4 Situatedness:** Own sensors versus APIs; situatedness in Loukissas's sense.
- **8.5 Limitations & future work:** Real weaving (jacquard / flat knitting), user studies, limits of the sphere classification, post-exhibition material directions (agents marking real material during the show).

## 9. Conclusion (~3%)

Figures are listed in `my_work/paper/figure_plan.md`.

## References

"(to verify)" marks items whose year or details need checking before writing.

### MtHD / HCI

- Giaccardi, E. & Redström, J. (2020). Technology and More-Than-Human Design. *Design Issues* 36(4).
- Wakkary, R. (2021). *Things We Could Design: For More Than Human-Centered Worlds*. MIT Press.
- Forlano, L. (2017). Posthumanism and Design. *She Ji* 3(1).
- Frauenberger, C. (2019). Entanglement HCI the Next Wave? *ACM TOCHI* 27(1).
- Coskun, A. et al. (2022). More-than-human Concepts, Methodologies, and Practices in HCI. CHI EA (workshop).
- Liu, J., Byrne, D. & Devendorf, L. (2018). Design for Collaborative Survival: An Inquiry into Human-Fungi Relationships. CHI '18.
- Biggs, H., Bardzell, J. & Bardzell, S. (2021). Watching Myself Watching Birds: Abjection, Ecological Thinking, and Posthuman Design. CHI '21.
- Clarke, R. et al. (2019). More-than-human participation: design for sustainable smart city futures. *Interactions*. (to verify)

### Time and rhythm

- Pschetz, L. & Bastian, M. (2018). Temporal Design: Rethinking time in design. *Design Studies* 56.
- Bastian, M. (2012). Fatally Confused: Telling the Time in the Midst of Ecological Crises. *Environmental Philosophy* 9(1).
- Hallnäs, L. & Redström, J. (2001). Slow Technology. *Personal and Ubiquitous Computing* 5(3).
- Lefebvre, H. (2004). *Rhythmanalysis*. Continuum.
- Tsing, A. L. (2015). *The Mushroom at the End of the World*. Princeton UP.
- Ingold, T. (1993). The Temporality of the Landscape. *World Archaeology* 25(2).
- Nixon, R. (2011). *Slow Violence and the Environmentalism of the Poor*. Harvard UP.

### Spheres and theory

- Latour, B. & Weibel, P. (eds.) (2020). *Critical Zones: The Science and Politics of Landing on Earth*. MIT Press / ZKM.
- Arènes, A., Latour, B. & Gaillardet, J. (2018). Giving depth to the surface. *The Anthropocene Review* 5(2).
- Haraway, D. (2016). *Staying with the Trouble*. Duke UP.
- Barad, K. (2007). *Meeting the Universe Halfway*. Duke UP.

### Data

- Jansen, Y. et al. (2015). Opportunities and Challenges for Data Physicalization. CHI '15.
- D'Ignazio, C. & Klein, L. (2020). *Data Feminism*. MIT Press.
- Loukissas, Y. (2019). *All Data Are Local*. MIT Press.
- Lupi, G. & Posavec, S. (2016). *Dear Data*. Princeton Architectural Press.
- Bakker, K. (2022). *The Sounds of Life*. Princeton UP.

### Weaving

- Plant, S. (1997). *Zeros + Ones*. Doubleday.
- Harlizius-Klück, E. (2017). Weaving as Binary Art and the Algebra of Patterns. *Textile* 15(2). (to verify)
- Devendorf, L. & Di Lauro, C. (2019). Adapting Double Weaving and Yarn Plying Techniques for Smart Textiles Applications. TEI '19.
- Ingold, T. (2013). *Making*. Routledge.

### Method

- Zimmerman, J., Forlizzi, J. & Evenson, S. (2007). Research through Design as a Method for Interaction Design Research in HCI. CHI '07.
- Gaver, W. (2012). What Should We Expect from Research Through Design? CHI '12.
- Bowers, J. (2012). The Logic of Annotated Portfolios. DIS '12.
- Höök, K. & Löwgren, J. (2012). Strong Concepts. *ACM TOCHI* 19(3).
