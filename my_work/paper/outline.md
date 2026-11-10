# Weaving With: Polyrhythm Loom — DIS Paper Outline

Revised 11 Nov 2026. English extracted from the student's bilingual outline. Wording unchanged. This replaces the outline in commit `eb5ae5f`; that version stays in git history.

Figures are listed in `my_work/paper/figure_plan.md`.

## Title

Weaving With: Polyrhythm Loom — Composing More-than-Human Temporalities into a Shared Cloth

**Alternative:** Separate and Align: Designing for Polyrhythmic Co-presence of More-than-Human Agents through Computational Weaving

**Paper type:** Research through Design paper, framed as an existence proof. Structure: Introduction and contribution → Related work → Design requirements → System → Demonstration and analysis → Discussion and limitations → Conclusion.

## Contribution

**Type:** existence proof. The paper demonstrates one new capability; the other pieces support it.

**Claim:** We demonstrate that the intrinsic rhythms of multiple more-than-human agents can be composed into one shared, perceivable structure without collapsing them onto a single human clock.

**What is newly possible:** Data interfaces usually either put every agent on one time axis, where slow agents flatten into a line, or draw them in separate panels with no relation between them. Polyrhythm Loom lets each agent keep its own time while meeting the others in one cloth.

**Inspectable evidence** (no participants needed):

1. The running system: the web loom and the installation.
2. The same data woven under the common clock and under intrinsic clocks, side by side.
3. The time-span figure: the same 480 picks hold 20 seconds for the device and 20 years for the spoonbill.

**Conditions and limits:** Seven agents, one scenario (the Cotai mudflat), partly modelled data, k = 24 as a design decision, no study of human perception yet.

**Where the other pieces go:**

| Piece | Role | Section |
|---|---|---|
| Polyrhythm Loom artifact | The proof itself | 4 System |
| Design trajectory | Source of the design requirements | 3 Design requirements |
| Recompile pipeline | Part of the system | 4.3 |
| Separate and align | Transferable concept drawn out in discussion | 6.1 |

## Abstract

150–200 words, written last.

Problem (interfaces flatten nonhuman time onto a human clock, or split agents apart) → what is newly possible → the system → the two-clock demonstration → separate and align → limits.

## 1. Introduction and Contribution (~10%)

- **Hook:** On the Cotai mudflat, tidal cycles, the geological time of sedimentation, the seasonal rhythm of migratory birds and human commuting hours all coexist, yet most environmental data interfaces put them on the same x-axis.
- **Problem:** MtHD calls for decentering, but at the level of data, time has rarely been designed with care. Interfaces either force every agent onto one clock, where slow agents vanish, or split agents into separate panels with no relation.
- **Contribution:** the one-sentence claim from the Contribution section above, stated in the last paragraph of the Introduction.
- **RQs**
  - **RQ1** How can design make heterogeneous more-than-human temporalities perceivable without collapsing them into human clock time? Answered by the system (Section 4).
  - **RQ2** When the same data is woven under a common clock and under intrinsic clocks, what becomes visible and what disappears? Answered by the demonstration (Section 5).
  - How people perceive the time-scale difference is not a research question here; it needs a participant study and moves to Limitations (6.5).
- **Approach:** Research through Design; the system was built and exhibited in November 2026, with no human participants.

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

## 3. Design Requirements (~12%)

Each requirement comes from a turn in the design process; the trajectory is reported here as the source of the requirements, not as a separate chronicle.

| Requirement | Where it came from | How the system meets it |
|---|---|---|
| R1 Each agent by its own measure | Under a common clock, 480 picks hold 20 s for the device but 20 yr for the spoonbill; slow agents flatten into a line. | Equal beats: one cycle = 24 picks for every agent (4.2). |
| R2 One cloth, not boxes | The zone-per-agent prototype was criticised as fragmented; the time-lens variant was dropped because its patterns did not work aesthetically. | A shared satin ground where ridges swing, cross and sum (4.4). |
| R3 A shared place | Listening Sea had a single source, far from the designer's own situation; random frequencies read as patchwork; the Wenchuan window felt too heavy. | The Cotai mudflat as one scenario, with own sensors on site (4.1). |
| R4 The human is one voice | The audience moved from weaving their own cloth, to one of seven, to stepping back to watch and listen. | The loom runs on the agents' rhythms; the treadle is one voice of seven (4.6). |
| R5 Feasible under booth and ethics limits | Limited booth space and production time; no participant study at this stage. | Digital-first: a tablet plus parallel acrylic layers; real weaving postponed (4.6). |

## 4. System: Polyrhythm Loom (~20%)

The system answers RQ1; each subsection names the requirement it meets.

### 4.1 Scenario & seven agents (R3)

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

### 4.2 Agent classification and equal beats (R1)

- **Spheres × rhythms:** Agents are classified by where they act (the spheres of the Critical Zone), not by what they are; each data series is read as cyclic, linear or event. Humans are not a sphere; they enter as visitors.
- **Equal beats:** one pick = period ÷ k, with k = 24, so one cycle is 24 picks for every agent; event agents advance one pick per event, the visitor one pick per press.
- **Why k = 24:** a plant pick is exactly 1 h; 3 full 8-end satin repeats per cycle; far above the Nyquist limit of 2 samples per cycle; 480 picks = 20 cycles fits one cloth.

### 4.3–4.6

- **4.3 Recompile pipeline:** Complex data → simple data → weaving data (the score) → pixel → textile and screen. A five-step diagram; what each step loses and keeps (an honest account of the cost of simplification).
- **4.4 Weaving grammar and polyrhythm (R2):** Mapping rules for warp, weft, colour and nodes; agents swing as ridges on one satin ground and sum where they cross; how cycles repel and cooperate (resonance, off-beats, nodes where phases coincide); key time points labelled as nodes.
- **4.5 Interface:** The layered-loom web page: agent clocks, the loom, body time; real-time data and labelled nodes.
- **4.6 Installation (R4, R5):** A tablet plus parallel acrylic layers (one cloth from the front, separate layers from the side), the physical form of "separate and align"; treadle (Arduino UNO R4 WiFi) as one voice of seven, with sound and vibration feedback.

## 5. Demonstration and Analysis (~15%)

This is the evidence core of the paper and answers RQ2.

- **5.1 Deployment:** The November 2026 exhibition: booth size, tablet and acrylic layers, treadle; which data were real and which modelled; how long the system ran.
- **5.2 Two-clock comparison:** The same data woven under the common clock (1 pick = 1 h) and under intrinsic clocks (1 cycle = 24 picks), side by side. Under the common clock slow agents flatten (8 presses turn the tide 0.64 of a cycle but CO₂ only 0.0009); under intrinsic clocks every agent shows its shape, but the fact that they happen at the same moment is hidden.
- **5.3 Process materials:** Build log, design decision records, screenshots of discarded versions, the AI-assisted workflow (Cursor + MCP); roles of the professors, the textile-artist friend and the technicians.
- **5.4 Conditions and ethics:** No participant data were collected; the treadle records no personal data; exhibition notes are first-person designer observations and make no claims about visitors' perception.

## 6. Discussion and Limitations (~15%)

- **6.1 Separate and align as an intermediate-level concept:** Define it: each agent is measured by its own cycle (separate) and all cycles share one count of beats (align). Show how it differs from a single shared axis and from separate small multiples, and why it transfers to other MtHD data projects.
- **6.2 Weaving as a relational data grammar:** Cloth accumulates and interlacing is relation, an ontology different from a chart's.
- **6.3 Decentering, and its limits:** The human is one voice and steps back, but periods, k and mapping rules are still written by the designer. Acknowledge this and limit the claim to making difference perceivable, not "letting species speak".
- **6.4 Situatedness:** Own sensors versus public APIs; situatedness in Loukissas's sense.
- **6.5 Limitations & future work:** How people perceive time-scale difference needs a participant study after ethics review (DIS version); modelled data to be replaced with real data; tide keeps only the M2 constituent; the device's 1 s period is the most arbitrary; limits of the sphere classification; real weaving on the jacquard or flat knitting machine; post-exhibition material directions.

## 7. Conclusion (~3%)

Restate the claim, what the demonstration showed, and what the next phase tests.

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
