---
title: "Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks"
authors: "Atsushi Masumori, Norihiro Maruyama, Itsuki Doi, johnsmith, Hiroki Sato, Takashi Ikegami"
year: 2025
venue: "arXiv preprint, cs.RO"
venue_type: "web"
doi_or_url: "https://doi.org/10.48550/arXiv.2509.05338"
verified: true
stream: "personal"
topic_tags: []         # 你来填
subconversation: ""
relevance: ""          # core | adjacent | background | rejected — 你来选
date_read:
---

# Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks

## 1 · Why this paper

This ALife/robotics paper connects a living plant to a mobile robot using asynchronous LLM modules that translate environmental sensor data into coordinated behavior. It sits in an instructive contrast to *Polyrhythm Loom*: both works bridge biological processes, technical signals, and public exhibition encounters, but *Plantbot* uses **natural language** as its universal protocol, whereas I use **computational weaving** to avoid anthropomorphic translation.

## 2 · Summary

- What it talks about: Introduces **Plantbot**, a hybrid bio-robotic system pairing a potted plant (with soil moisture,temperature, pH, EC, and NPK sensors) with a mobile crawler base (webcam, mic, speaker, LiDAR) coordinated by five asynchronous LLM modules communicating via natural language over OSC.
- Main contributions: (1) A modular, asynchronous LLM agent architecture (Vision, Sensor, Chat, and two Action agents) using natural language as a cross-domain protocol; (2) real-world exhibition deployments at Ginza Skywalk (2024) and CCBT Tokyo (2025); (3) behavioral log analyses (UMAP utterance clusters, word clouds, Stop/Move state dynamics) framing the system as an embodied Artificial Life model.
- Problem & importance: Prior plant-robot hybrids relied on rigid, low-level analog mappings (e.g., voltage thresholds directly triggering wheels), limiting behavioral adaptability; meanwhile, purely digital AI agents lack intrinsic biological **normativity** (real stakes like survival or hydration).
- Innovation & benefits: Treating **natural language as a universal interface** lets heterogeneous modules (vision, soil sensing, motor control, human dialogue) coordinate flexibly without central hard-coded logic, echoing Minsky’s *Society of Mind* and Global Workspace Theory.
- Advance over prior work: Moves beyond fixed stimulus-response bio-hybrids by using LLM-mediated linguistic messaging to generate emergent, context-sensitive movement and conversation around a living organism’s needs.



## 3 · Critical thinking

- Natural language as "universal protocol" smuggles in anthropomorphism: Converting raw soil moisture into *"I'm thirsty, can I have water?"* doesn't let the plant speak—it ventriloquizes human-like emotion and conversational framing via GPT-3.5/4V. Using language as the bridge forces non-verbal, slow botanical states into human linguistic norms.
- Prompted normativity ≠ biological normativity: The authors argue that coupling a plant installs intrinsic biological normativity into the sensor-motor loop. Yet the mapping from *"dry soil"* to *"I should move"* is still mediated by human-written LLM system prompts—so the system’s goals remain designer-authored rather than purely plant-driven.
- Evaluating the AI chatter rather than the plant or visitors: Their empirical analysis (UMAP clusters, word clouds,Stop/Move durations) tracks how the *LLM modules* behaved across short 3–4 day exhibitions, offering no evidence on whether Plantbot’s autonomous wandering actually benefited the plant’s health over time, nor how visitors experienced its agency.



## 4 · Creative thinking

- Sparks: *Plantbot*’s asynchronous, decentralized module design mirrors *Polyrhythm Loom*’s **agent-specific generative rhythms**. Both reject a single master clock in favor of loosely coupled processes operating at their own tempos.
- New application: Instead of putting a plant on wheels, a modular asynchronous architecture could feed live Cotai mudflat sensor streams (salinity, tide, avian acoustics) into *Polyrhythm Loom*’s weaving grammar—where each "module" governs a distinct warp/weft thread rather than a spoken utterance.
- Alternative method: Rather than translating ecological data into *natural language* (which anthropomorphizes nonhumans), *Polyrhythm Loom* translates signals into **structural textile operations** (connection, mediation, interruption),preserving the strangeness and non-verbal character of more-than-human temporalities.



## 5 · Form — read it as a genre, not just as content

- Genre & venue style: **CS/Robotics & Artificial Life (ALife) system paper**—written as an arXiv preprint bridging hardware/software engineering with ALife philosophy (*normativity, Society of Mind, Global Workspace Theory*).
- First contribution claim (from Abstract):
  > *"We introduce Plantbot, a hybrid lifeform that connects a living plant with a mobile robot through a network of large language model (LLM) modules."*
- Artifact vs. analysis: Heavily **system-and-behavior oriented**—hardware/agent architecture + quantitative log visualizations (UMAP, state-transition durations, word clouds) rather than human-centered qualitative interviews.
- Related work: Contrasts prior bio-hybrid robots (limited to low-level analog signals) and LLM agents (lacking biological stakes) to motivate LLM-mediated bio-robotics.
- Process evidence: Public exhibition photos, hardware schematics, raw inter-agent text logs, and statistical plots of system utterances/states.
- Figures: **7 figures** documented (installation views, 5-module system diagram, hardware diagram, UMAP embedding plot,module word clouds, Stop/Move duration plots, transition word clouds).
- Voice & tense: First-person plural (*"we introduce", "we conducted"*); present tense for architecture and ALife claims, past tense for exhibition trials and log analysis.



## 6 · Venue signal

While *Plantbot* is an **ALife/Robotics (**`cs.RO`**)** preprint rather than a DIS paper, it shows a trend DIS reviewers increasingly encounter: *LLM-mediated more-than-human systems*. For **DIS**, however, an ALife log analysis alone wouldn't suffice—DIS reviewers would immediately press on *anthropomorphism* (making a plant talk like a needy chatbot) and ask for **critical reflection on human-nonhuman mediation** and **visitor encounters**. That gives *Polyrhythm Loom* a clear edge: you explicitly avoid turning mudflat processes into talking personas.

## 7 · Take-home

- Learned & new: Framing biological needs as **"normativity"** that grounds an artificial sensor-motor loop is a useful concept—even if I critique how *Plantbot* implements it through GPT dialogue.
- Application: Cite *Plantbot* in *Polyrhythm Loom*’s Related Work as a foil for **linguistic/anthropomorphic mediation** of nonhuman signals: whereas *Plantbot* uses natural language to make a plant legible to humans, *Polyrhythm Loom* uses **computational weaving** to keep relational mediation structural and non-verbal.
- Good writing sample? Good for **architecture-to-concept framing** (linking an engineering diagram to big theoretical ideas like *Society of Mind*), though for DIS you’ll want deeper reflection on design choices and exhibition encounters rather than UMAP plots of agent text.

