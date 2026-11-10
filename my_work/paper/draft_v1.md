# Weaving With: Polyrhythm Loom — Composing More-than-Human Temporalities into a Shared Cloth

Filed 11 Nov 2026 from the student's draft. Wording unchanged, including bracketed notes still to fill.

## Abstract

Environmental data about other species and earth processes are usually shown on a single human clock. On one shared time axis, slow agents flatten into lines and fast ones blur into noise; drawn in separate panels instead, they lose their relation to one another. We present Polyrhythm Loom, a digital loom that composes the intrinsic rhythms of seven agents on a Macau mudflat into one shared cloth: the tide, daylight, a migratory spoonbill, atmospheric CO₂, mud and sediment, a computing device, and a human visitor. Each agent is measured by its own cycle, and all cycles share one count of beats: one cycle equals 24 picks of weft. We describe the design requirements that emerged across our research-through-design process, the system's recompile pipeline and weave grammar, and an exhibition deployment. Weaving the same data under a common clock and under intrinsic clocks shows what each hides. We name the underlying strategy separate and align, discuss how the designer's authorship persists in the mapping rules, and outline the participant study that will follow.

**Keywords:** more-than-human design, temporality, rhythm, data physicalization, computational weaving, research through design

## 1 Introduction

On the Cotai mudflat in Macau, several clocks run at once. The tide rises and falls roughly every 12.4 hours. Black-faced spoonbills arrive each autumn and leave in spring. Atmospheric CO₂ rises and falls once a year as northern vegetation breathes. Mud settles grain by grain, and a tablet placed on the shore counts its own seconds. If we draw all of these on one chart with an x-axis in hours, the spoonbill becomes a flat line and the device becomes a blur. If we give each its own panel, each keeps its shape, but we can no longer see that they are happening together, in the same place.

More-than-human design (MtHD) in HCI has asked designers to move the human out of the centre and to treat other species, materials and technologies as participants in design [Giaccardi and Redström 2020; Wakkary 2021; Nicenboim et al. 2025]. Much of this work asks who takes part. Less of it asks whose time a design runs on. Temporal design argues that clock time is only one of many times at play in the world [Pschetz and Bastian 2018], and recent HCI work has begun to design with nonhuman temporalities directly [Key et al. 2025]. Data physicalization has moved environmental data off the screen and into material form [Jansen et al. 2015; Jones et al. 2024]. Yet most of these systems still place their data on a single timeline, or give each data source a separate place.

In this paper we present Polyrhythm Loom, a digital loom that composes the intrinsic rhythms of seven agents on the Cotai mudflat into one shared cloth. Our claim is an existence proof: the intrinsic rhythms of multiple more-than-human agents can be composed into one shared, perceivable structure without collapsing them onto a single human clock. The loom does this by measuring every agent by its own cycle and giving every cycle the same number of beats. Weaving offers a natural grammar for this: the weft advances pick by pick, the warp holds every thread in the same cloth, and where threads cross, a relation is made.

We ask two research questions:

- **RQ1.** How can design make heterogeneous more-than-human temporalities perceivable without collapsing them into human clock time?
- **RQ2.** When the same data is woven under a common clock and under intrinsic clocks, what becomes visible and what disappears?

We answer RQ1 through the system (Section 4) and RQ2 through a demonstration that weaves the same data both ways (Section 5). How visitors perceive these differences is an important question, but it requires a participant study under ethics review; we treat it as future work (Section 6.5).

We followed a research-through-design approach [Zimmerman et al. 2007; Gaver 2012]. Polyrhythm Loom grew out of an earlier probe, Listening Sea, which turned a single live hydrophone stream into sound and touch. It was built over October and November 2026 with faculty, a textile artist and technicians, and exhibited in Macau in November 2026 [update after the exhibition].

This paper contributes:

1. An existence proof: Polyrhythm Loom, a working system and installation in which seven agents' intrinsic rhythms share one cloth, with the human as one voice among seven.
2. Five design requirements, each traced to a turn in our design process, for composing more-than-human time.
3. A two-clock analysis of what a common clock and intrinsic clocks each reveal and hide in the same data.
4. An intermediate-level concept, separate and align, that other designers working with multi-agent environmental data can reuse.

## 2 Related Work

We build on four threads in HCI and design research: decentering the human, time as a design material, situated and physical data, and weaving as computation. For each, we note what our work takes from it and what remains open.

### 2.1 Decentering the Human in Design

More-than-human design asks designers to see artifacts, species and environments as co-participants rather than as resources or backdrops [Giaccardi and Redström 2020; Wakkary 2021]. Nicenboim et al. [2025] trace this move back to posthuman theory and show how designers both apply it and produce their own posthuman knowledge through making.

In practice, HCI researchers have decentered the human in several ways. Thing ethnography attached cameras and sensors to everyday objects to study homes from the objects' point of view [Giaccardi et al. 2016]. Morse Things were networked bowls that talked to each other in their own code, on their own schedule, and only partly let people in [Wakkary et al. 2017]. Liu et al. [2018] designed tools that slowed foragers down so they could notice fungi, and Biggs et al. [2021] used first-person birdwatching to reflect on how a human observer frames other species. Lee et al. [2024] followed greenhouse, heirloom and wild tomatoes to show that each "experiences" agricultural data differently, while Ofer and Alistar [2024] proposed tracing as a strategy for orienting to nonhuman perspectives. At the city scale, Heitlinger et al. [2019] brought multispecies participation into smart-city design.

These works mainly ask who takes part and from whose perspective the world is seen. Time is often present, as in the slow attention of the foragers or the private schedule of Morse Things, but it is rarely the design material itself. We ask what changes when several nonhuman agents each keep their own time inside one artifact.

### 2.2 Time as a Design Material

Slow technology proposed that interaction can be designed for reflection rather than efficiency, making time itself something people notice [Hallnäs and Redström 2001]. Odom and colleagues developed this into long-term field studies: Photobox printed a random photo from a person's collection a few times a month [Odom et al. 2014], and Olly replayed songs from a listener's history at an unhurried pace over fifteen months, helping people reflect on their listening data [Odom et al. 2019]. These artifacts show that tempo shapes how people relate to data. Yet each has one tempo, and it is set to human life.

Temporal design goes further by arguing that clock time is only one of many times at play, and that design often hides the others [Pschetz and Bastian 2018]. Leaky Cups brought this argument to more-than-human HCI: cups that leak in response to local water data let a river's time drive a domestic object, drawing on hydrofeminist ideas of time [Key et al. 2025]. Lefebvre's rhythmanalysis offers a simple principle we adopt: each rhythm should be measured by its own repetition, not by an external clock [Lefebvre 2004].

Taken together, this work makes one nonhuman or slow time felt through one artifact. It does not yet tell designers how to hold several concurrent times, from seconds to years, in one structure without letting one of them become the standard.

### 2.3 Situated and Physical Data

Data physicalization moves data from screens into objects that can be touched and walked around [Jansen et al. 2015], and embedded representations place data in the environment it describes [Willett et al. 2017]. Chemicals in the Creek turned open government data on water pollution into light installations on the creek itself, designed with the local community [Perovich et al. 2021]. Textile physicalizations have become a rich strand: VISMOCK maps data to smocked fabric through visual and tactile variables [Bakhtiari et al. 2024], and Friske et al. [2020] used yarn and sound to tell interpersonal data stories.

The closest precedent to our work is A Year of Interaction Around Town [Jones et al. 2024]. A motorised sock-knitting machine knitted one row each time it sensed a person at local arts events, while the yarn colour changed monthly with the seasons of a nearby river. The resulting knit is a year-long record. Its time, however, has one rule: one row equals one detected visit, with a monthly colour change on top. Most physicalizations share this pattern, a single mapping from time to material. Our work asks how one material structure can hold many temporal mappings at once.

### 2.4 Weaving as Computation

Weaving has long been tied to computation: the punched cards of the Jacquard loom are an early form of stored instructions [Plant 1997]. In HCI, Devendorf and colleagues treat weaving as a site of design research rather than only an output. AdaCAD frames weave drafts as a parametric notation for complex structures [Devendorf et al. 2023]; double weaving supports layered smart textiles [Devendorf and Di Lauro 2019]; and Unfabricate designs woven circuits to be unravelled and reclaimed [Wu and Devendorf 2020].

We take from this work the idea that a weave draft is already a notation: a grid of rules that a machine can perform. We extend it by reading the draft as a musical score. Each pick is a beat, and the warp holds every agent in the same cloth.

### 2.5 Summary

Prior work decenters the human by changing who participates, makes slow or nonhuman time felt through one tempo, and physicalizes environmental data through one temporal mapping. No work we know of composes many intrinsic times into one perceivable structure while keeping their differences. Polyrhythm Loom addresses this gap.

## 3 Design Requirements

We did not begin with these requirements; they emerged from turns in our design process between October and November 2026. We report each requirement together with the turn that produced it, because the reasons for changing direction are part of the knowledge this work offers [Gaver 2012; Bowers 2012]. Figure 2 summarises the sequence.

[Figure 2: From design turns to requirements R1–R5.]

**R1 — Measure each agent by its own cycle.** An early test placed all agents on one shared clock, with one pick of weft equal to one hour. Across a cloth of 480 picks, the tide completed dozens of cycles while CO₂ and the spoonbill barely moved. The same length of cloth held 20 seconds of the device's time and 20 years of the spoonbill's. Slow agents were not wrong on this clock; they were simply invisible. Each agent must be measured by its own cycle.

**R2 — Share one structure, not separate zones.** Our first loom gave each agent its own band of warp. Each rhythm was legible, but faculty reviewers described the result as fragmented: the agents sat side by side without meeting. A second variant, a "time lens" that magnified one agent at a time, produced patterns we judged unconvincing as cloth, and we dropped it. In research through design, an aesthetic failure is a valid finding: the form did not carry the idea. Agents must share one structure in which they can cross and affect each other.

**R3 — Ground the agents in one shared place.** Listening Sea, our earlier probe, used a single live hydrophone stream from the Salish Sea. Its data carried a strong story, ship noise masking orca calls, but it came from far away and from one source. Our first multi-agent version then drew on scattered datasets, which read as a patchwork of unrelated frequencies. We considered replaying the time window of the 2008 Wenchuan earthquake to give the agents a shared event, but decided it was too heavy, ethically and emotionally, for an exhibition piece. We settled on the Cotai mudflat in Macau: a place we can visit, sample with our own sensors, and share with the agents we represent. The agents must share a place, and the designer must be able to reach it.

**R4 — Make the human one voice among many.** We first imagined visitors weaving cloths of their own from their own data. We then made the visitor one of seven agents weaving a shared cloth. Finally, we let the loom run on the agents' rhythms and asked visitors to step back, watch and listen, keeping a treadle as one optional human voice. The human must take part as one agent, not as the centre that drives the loom.

**R5 — Work within the limits of the booth and ethics review.** The exhibition offered a small booth and about two weeks of production time, and our course context did not allow a participant study. Weaving the final cloth on the college's electronic jacquard loom would have consumed most of that time. The system must run digitally first, with material weaving as a later step.

## 4 Polyrhythm Loom

Polyrhythm Loom is a web-based loom, a tablet installation with layered acrylic sheets, and a treadle. This section answers RQ1 and notes which requirement each part meets.

[Figure 1 (teaser): the acrylic layers seen from the front as one cloth, and from the side as separate layers.]

### 4.1 Seven Agents on the Cotai Mudflat (R3)

We classify agents by where they act rather than what they are, using the spheres of the Critical Zone, the thin living layer of the Earth from treetops to groundwater [Latour and Weibel 2020]. Each agent's data is read as one of three rhythm types: cyclic, linear or event [Lefebvre 2004; Adam 1998]. Every sphere contributes at least one agent. Humans are not a sphere; they enter as visitors. Table 1 lists the agents.

| Agent | Sphere | Data source | Period | One pick |
|---|---|---|---|---|
| CO₂ | Atmosphere | NOAA Mauna Loa, monthly | 1 year | 15 days |
| Daylight and plants | Biosphere | Macao Meteorological and Geophysical Bureau (SMG) sunshine; solar elevation | 1 day | 1 hour |
| Black-faced spoonbill | Biosphere | Hong Kong Bird Watching Society regional census; Macau counts | 1 year (winter stay) | 15 days |
| Tide | Hydrosphere | SMG tide tables | 12.42 hours | 31 minutes |
| Mud and sediment | Lithosphere | Our own sensors on site; distant earthquakes from the USGS catalogue as events | [TBD] | [TBD] |
| This device | Technosphere | Measured live on site | 1 second | 0.04 seconds |
| Visitor | — | Treadle presses; no personal data | none | 1 press |

**Table 1.** The seven agents. Except for the device and the visitor, the exhibition prototype uses modelled data to be replaced with measured data.

The spoonbill anchors the cloth locally: it winters at the Cotai ecological zone, and its stay overlaps the exhibition.

### 4.2 Equal Beats (R1)

The core rule is simple. Every agent's cycle is divided into the same number of beats, k, and one beat is one pick of weft:

$$\text{one pick} = \frac{\text{period}}{k}, \quad k = 24$$

Thus one tide cycle, one day of daylight and one year of CO₂ each take 24 picks. Event agents advance one pick per event, and the visitor advances one pick per treadle press. No agent's clock is the standard.

We chose k = 24 for four reasons. A plant pick then equals exactly one hour, a point of contact with human time. Twenty-four divides into three full repeats of an 8-end satin. It samples each cycle far above the Nyquist limit of two samples per cycle, so curves stay smooth. And a cloth of 480 picks holds 20 cycles of every agent.

### 4.3 Recompile Pipeline

Data passes through five stages (Figure 5):

1. Complex data: raw series with mixed units, sampling rates and gaps.
2. Simple data: each series decomposed into trend, cycle and residual, and scaled to 0–1.
3. Weaving data (the score): each series resampled to picks under both clocks.
4. Pixel: one row of 0s and 1s per pick, a standard weave draft.
5. Textile and screen: the same draft drives the on-screen loom and can be sent to a jacquard loom.

Each stage loses detail on purpose. We treat this loss as part of translating between species and scales, not as an error to hide, and we document what each stage drops.

### 4.4 Weave Grammar (R2)

The grammar has seven elements. Along the warp, data shapes the pattern: a ridge swings left and right with an agent's cycle; where ridges meet they form a crossing and their values sum; the ground tone follows an agent's trend; and an event appears as a single lozenge flower. Along the weft, time and colour are set: every 24 picks, two plain picks form a bar line; the weft takes one of five indigo shades according to the chord of agents at that pick; and the visitor's presses add a madder-red brocade weft.

All agents share one 8-end shaded satin ground. Tone becomes the number of raised warp points:

$$\text{warp } i \text{ is up at pick } j \iff (3i - j) \bmod 8 < n, \qquad n = \operatorname{round}(1 + 6 \cdot \text{tone})$$

At arm's length the cloth reads as smooth tone; up close it shows real interlacings. Where cycles fall into phase, ridges reinforce each other and form nodes; where they drift apart, they cross and pull against each other (Figure 6).

### 4.5 Interface

The web page has four parts: agent clocks on the left, each a dial turning by its own cycle; the loom in the centre, with jacquard head, heddles, shuttle, reed and growing cloth; body time on the right, showing what the latest pick means for each agent; and a footer with the treadle, sound and data settings. Key time points are labelled as nodes on the cloth. A data drawer accepts a two-column CSV, so modelled data can be replaced with measured data.

### 4.6 Installation (R4, R5)

A tablet runs the live page. Beside it, the agents' layers are cut as parallel acrylic sheets: seen from the front, they read as one cloth; seen from the side, they come apart as separate layers. This is the physical form of the system's logic. The loom runs on the agents' rhythms. A treadle, read by an Arduino UNO R4 WiFi, lets a visitor add one pick for every agent at once, with sound and vibration feedback. Holding a press longer than 0.6 seconds ties a knot in the cloth. The treadle is one voice of seven, not a control.

## 5 Demonstration and Analysis

This section provides the evidence for our claim and answers RQ2. We weave the same data under two clocks and compare what each makes visible.

### 5.1 Deployment

Polyrhythm Loom was shown at [exhibition name, venue] in Macau from [dates] November 2026. The booth held the tablet, the acrylic layers and the treadle in about [TBD] m². The device and visitor agents ran live; the other five ran on modelled series calibrated to their sources in Table 1. The system ran for [TBD] hours across [TBD] days. [Update after the exhibition.]

### 5.2 Two Clocks, One Data Set

We render the same data as two sections of one cloth, both ending at the same moment, the opening of the exhibition. In the common-clock section, one pick equals one hour for every agent. In the intrinsic-clock section, one cycle equals 24 picks for every agent (Figure 7). Table 2 shows how much time the same 480 picks hold under each clock.

| Agent | Common clock (1 pick = 1 h) | Intrinsic clock (1 cycle = 24 picks) |
|---|---|---|
| This device | 20 days | 20 seconds |
| Tide | 20 days | about 10 days |
| Daylight and plants | 20 days | 20 days |
| Earthquakes (events) | 20 days | about 3 years, at 1 pick per quake |
| CO₂ | 20 days | 20 years |
| Black-faced spoonbill | 20 days | 20 years |

**Table 2.** Time held by 480 picks. Under the intrinsic clock, the spans differ by about seven orders of magnitude.

**What the common clock shows, and hides.** The common clock keeps simultaneity: every pick is the same hour for every agent, so one can see, for example, which tides coincide with daylight. It also keeps human legibility, since its unit is familiar. But it erases slow agents. Over 20 days, CO₂ and the spoonbill are almost flat lines; eight treadle presses turn the tide through 0.64 of a cycle, but CO₂ through only 0.0009. Fast agents fare no better: sampling a one-second device clock once an hour turns its rhythm into noise.

**What intrinsic clocks show, and hide.** Under intrinsic clocks, every agent shows its full shape, and all seven are equally present in the cloth. Eight presses turn every dial through the same angle, a third of a cycle, but that angle means 4 months of CO₂, 8 hours of daylight, 4.1 hours of tide and 0.33 seconds of the device. Ridges cross and fall into phase, producing nodes that no single series contains. What is lost is simultaneity: a crossing between the tide ridge and the CO₂ ridge does not mean that the two happened at the same moment. There is also a risk of false equivalence, as if one tide "equalled" one year.

**Why both are needed.** Neither clock is neutral. The common clock makes difference invisible; intrinsic clocks make simultaneity invisible. Showing them as two sections of one cloth, ending together, lets each correct the other. The acrylic installation repeats this at the scale of the body: from the front, one cloth; from the side, separate layers. We return to this as separate and align in Section 6.1.

### 5.3 Process Materials

Alongside the system, we kept a build log, a record of design decisions with dates and reasons, screenshots of every discarded version, and notes from reviews with faculty, a textile artist and the college's loom technicians. Much of the code was written with an AI coding assistant (Cursor); we record which parts were generated and how they were checked. These materials support the requirements in Section 3 and are available as supplementary material [to prepare].

### 5.4 Conditions and Ethics

We collected no data about visitors. The treadle records only that a press occurred and how long it lasted. Our notes from the exhibition are first-person observations by the designer; we report them as context, not as findings about how visitors perceive time. [might Add two or three short observations after the exhibition.]

## 6 Discussion and Limitations

### 6.1 Separate and Align

We name the strategy behind Polyrhythm Loom separate and align. To separate is to measure each agent by its own cycle, so that no agent's time becomes the standard. To align is to give every cycle the same count of beats in one shared structure, so that the agents can still meet. We offer it as an intermediate-level concept [Höök and Löwgren 2012]: more general than our artifact, more specific than a theory of time.

The concept sits between two familiar defaults. A shared time axis aligns without separating: everything meets, but slow and fast agents disappear. Separate panels, or small multiples, separate without aligning: each agent keeps its shape, but relations between them are lost. Separate and align keeps both, and pairs the result with a common-clock view so that simultaneity is not lost either (Section 5.2).

Other designers can apply it in three steps: find each agent's characteristic period; choose a shared beat count that suits the medium (24 suited satin weaving; a different medium may need 12 or 60); and show a common-clock companion beside the intrinsic view. A knitted record like that of Jones et al. [2024], for example, could knit one row per river cycle rather than per visitor, beside a row-per-day section.

### 6.2 Weaving as a Relational Grammar

A chart places values at positions on axes. A cloth works differently: it accumulates pick by pick, it holds every thread in one structure, and its pattern comes from where threads cross. This suits data understood as relation rather than as representation. Weaving also offers a ready notation: the draft already used by tools such as AdaCAD [Devendorf et al. 2023] doubled as our score, so the same file drove the screen and could drive a loom. We see this as a reason for designers to consider textile structures not only as an output medium for data, but as a way of thinking about how several data series relate.

### 6.3 Decentering, and Its Limits

Polyrhythm Loom makes the human one voice among seven, and asks visitors to step back. Yet the designer remains present everywhere. We chose which agents to include, which period stands for each, the value of k and every mapping rule. The decentering happens in what the loom shows, not in who wrote it. Like Morse Things [Wakkary et al. 2017], the loom offers only partial access to its agents, and we do not claim to let them speak. Our claim is narrower: the loom makes their differences in time perceivable. We think the honest response is to make the authored rules visible, as we have done in Section 4, so that others can question and change them [Nicenboim et al. 2025].

### 6.4 Situatedness

Moving from Listening Sea to the Cotai mudflat changed our relation to the data. A public stream from a distant sea is easy to access but difficult to stand beside. Data from a place we can visit is harder to collect but grounds the work [Perovich et al. 2021; Loukissas 2019]. The place also shapes the design process itself: sampling on a mudflat must be timed to low tide, so the tide sets the fieldwork schedule as well as a ridge in the cloth. We plan to document this in the next phase.

### 6.5 Limitations and Future Work

Our claim is an existence proof, and its limits matter.

- **No participant study.** We do not yet know how visitors perceive the time-scale differences. A study under ethics review will compare the two clocks with visitors in the next phase of this work.
- **Modelled data.** Five of the seven agents ran on modelled series during the exhibition; we will replace them with measured data, including our own sensors on the mudflat.
- **Simplified periods.** The tide uses only its main lunar component, M2, although Macau's tide also includes diurnal components and a 14.8-day spring–neap cycle. The device's one-second period is the most arbitrary of our choices. We will check each period against real data by autocorrelation.
- **One place, seven agents.** The classification by spheres worked for this site; other places may need different agents or rhythm types.
- **Weaving deferred.** We have not yet woven the cloth on the college's jacquard loom or flat knitting machine. Material weaving, and letting agents mark material during an exhibition, are next steps.

## 7 Conclusion

Data about other species and earth processes usually reach us on one human clock, where slow agents vanish and fast ones blur. Polyrhythm Loom shows that this is not the only option. By measuring each of seven agents on the Cotai mudflat by its own cycle and giving every cycle the same 24 beats, it composes their intrinsic rhythms into one shared cloth. Weaving the same data under a common clock and under intrinsic clocks shows that each hides something the other reveals, which is why we keep both. We offer separate and align as a concept other designers can reuse, and we have tried to keep visible the rules through which we, as designers, still shape what the loom shows. The next step is to ask visitors what they feel when one press of a treadle is half an hour for the tide and two weeks for a spoonbill.

## References

Items marked [verify] need their details checked before submission. Convert to ACM reference format at the end.

- Barbara Adam. 1998. *Timescapes of Modernity: The Environment and Invisible Hazards*. Routledge.
- Bahare Bakhtiari, Charles Perin, and Sowmya Somanath. 2024. VISMOCK: A Programmable Smocking Technique for Creating Interactive Data Physicalization. In *Proc. DIS '24*. ACM.
- Heidi Biggs, Jeffrey Bardzell, and Shaowen Bardzell. 2021. Watching Myself Watching Birds: Abjection, Ecological Thinking, and Posthuman Design. In *Proc. CHI '21*. ACM.
- John Bowers. 2012. The Logic of Annotated Portfolios: Communicating the Value of "Research Through Design". In *Proc. DIS '12*. ACM.
- Laura Devendorf and Chris Di Lauro. 2019. Adapting Double Weaving and Yarn Plying Techniques for Smart Textiles Applications. In *Proc. TEI '19*. ACM.
- Laura Devendorf et al. 2023. AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving. In *Proc. CHI '23*. ACM. [verify author list]
- Mikhaila Friske, Jordan Wirfs-Brock, and Laura Devendorf. 2020. Entangling the Roles of Maker and Interpreter in Interpersonal Data Narratives: Explorations in Yarn and Sound. In *Proc. DIS '20*. ACM.
- William Gaver. 2012. What Should We Expect from Research Through Design? In *Proc. CHI '12*. ACM.
- Elisa Giaccardi and Johan Redström. 2020. Technology and More-Than-Human Design. *Design Issues* 36, 4.
- Elisa Giaccardi, Nazli Cila, Chris Speed, and Melissa Caldwell. 2016. Thing Ethnography: Doing Design Research with Non-Humans. In *Proc. DIS '16*. ACM.
- Lars Hallnäs and Johan Redström. 2001. Slow Technology: Designing for Reflection. *Personal and Ubiquitous Computing* 5, 3.
- Sara Heitlinger, Nick Bryan-Kinns, and Rob Comber. 2019. The Right to the Sustainable Smart City. In *Proc. CHI '19*. ACM.
- Kristina Höök and Jonas Löwgren. 2012. Strong Concepts: Intermediate-Level Knowledge in Interaction Design Research. *ACM TOCHI* 19, 3.
- Yvonne Jansen et al. 2015. Opportunities and Challenges for Data Physicalization. In *Proc. CHI '15*. ACM.
- Lee Jones, Greta Grip, Erin Kennedy, and Sara Nabil. 2024. A Year of Interaction Around Town: Gathering Traces with an Interactive Knitting Machine and Community Stitch Markers. In *Proc. DIS '24*. ACM.
- Cayla Key, Cally Gatehouse, Stevie Koepp, and Nick Taylor. 2025. Leaky Cups: Tinkering with Hydrofeminist Temporalities for HCI. In *Proc. CHI '25*. ACM.
- Bruno Latour and Peter Weibel (Eds.). 2020. *Critical Zones: The Science and Politics of Landing on Earth*. MIT Press.
- Youngsil Lee, Chris Speed, and Larissa Pschetz. 2024. Pheno-data: Knowledge from Tomatoes' Becoming with Different Ecological Worlds. In *CHI EA '24* (alt.chi). ACM.
- Henri Lefebvre. 2004. *Rhythmanalysis: Space, Time and Everyday Life*. Continuum.
- Jen Liu, Daragh Byrne, and Laura Devendorf. 2018. Design for Collaborative Survival: An Inquiry into Human-Fungi Relationships. In *Proc. CHI '18*. ACM.
- Yanni Alexander Loukissas. 2019. *All Data Are Local: Thinking Critically in a Data-Driven Society*. MIT Press.
- Iohanna Nicenboim, Doenja Oogjes, Heidi Biggs, and Seowoo Nam. 2025. Decentering Through Design: Bridging Posthuman Theory with More-than-Human Design Practices. *Human–Computer Interaction* 40, 1–4, 195–220. [verify year: published online 2023]
- William Odom, Abigail Sellen, Richard Banks, David Kirk, Tim Regan, Mark Selby, Jodi Forlizzi, and John Zimmerman. 2014. Designing for Slowness, Anticipation and Re-visitation: A Long Term Field Study of the Photobox. In *Proc. CHI '14*. ACM.
- William Odom, Ron Wakkary, Jeroen Hol, Bram Naus, Pepijn Verburg, Tal Amram, and Amy Yo Sue Chen. 2019. Investigating Slowness as a Frame to Design Longer-Term Experiences with Personal Data: A Field Study of Olly. In *Proc. CHI '19*. ACM.
- Netta Ofer and Mirela Alistar. 2024. Tracing as a Strategy for Orienting to Nonhuman Perspectives. In *Proc. DIS '24*, 1087–1100. ACM. [verify first names]
- Laura J. Perovich, Sara Ann Wylie, and Roseann Bongiovanni. 2021. Chemicals in the Creek: Designing a Situated Data Physicalization of Open Government Data with the Community. *IEEE TVCG* 27, 2.
- Sadie Plant. 1997. *Zeros + Ones: Digital Women and the New Technoculture*. Doubleday.
- Larissa Pschetz and Michelle Bastian. 2018. Temporal Design: Rethinking Time in Design. *Design Studies* 56.
- Ron Wakkary. 2021. *Things We Could Design: For More Than Human-Centered Worlds*. MIT Press.
- Ron Wakkary, Doenja Oogjes, Sabrina Hauser, Henry Lin, Cheng Cao, Leo Ma, and Tijs Duel. 2017. Morse Things: A Design Inquiry into the Gap Between Things and Us. In *Proc. DIS '17*. ACM. [verify author list]
- Wesley Willett, Yvonne Jansen, and Pierre Dragicevic. 2017. Embedded Data Representations. *IEEE TVCG* 23, 1.
- Shanel Wu and Laura Devendorf. 2020. Unfabricate: Designing Smart Textiles for Disassembly. In *Proc. CHI '20*. ACM.
- John Zimmerman, Jodi Forlizzi, and Shelley Evenson. 2007. Research Through Design as a Method for Interaction Design Research in HCI. In *Proc. CHI '07*. ACM.
