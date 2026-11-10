# Claim — Listening Sea (Orcasound)

Filed 2026-11-10. The student supplied this text as the claim for the project as it stood then. The four sentences, the evidence list, the objection and the next action are theirs. Later revisions stay in this file, dated.

Two spellings were corrected on filing: a missing space in "I made Listening", and "indigeous" to "indigenous". Nothing else was rewritten.

## Version 2026-11-10

### 1 · I made

I made Listening Sea, a system that takes the Orcasound live hydrophone stream (orca calls and the ship noise that masks them) and feeds it back into human space as touch and sound. Remote listeners are connected too, so each listener's state influences the others through data. The installation is framed conceptually by tidal time and magnetic direction.

### 2 · In making it I found that

In making it I found that the stream is never one voice. It is a polyphony of orcas, ships, water and equipment, and the masking itself is the most legible narrative. Separating or "cleaning" the orca signal would erase the relation between species and industry. I also found that a single live source, far from my own situation, keeps the audience as listeners about the sea rather than participants in a shared environment. That is why I now treat it as a process piece.

### 3 · Which means that

Which means that data as relation is better served by keeping the overlap (who masks whom, and when) than by isolating a "non-human voice." Distributing listening across remote participants is one way to dissolve the central human ear. A single-agent system still limits how far that de-centring can go, and this directly motivated the multi-agent, multi-rhythm structure of *Weaving With*.

### 4 · Which is useful to

Which is useful to more-than-human and sonic-interaction designers working with live environmental audio. It suggests treating interference and masking as content rather than noise. It also offers a pattern for multi-listener systems where the human audience is plural and mutually affecting rather than one privileged observer.

## Evidence

- Working prototype in `~/Desktop/Hydrophone` (live stream ingest via Node.js + ffmpeg)
- Running process record in `docs/build-log.md`, from the Oct 28 technical setup onwards
- Recordings comparing masked and unmasked segments (ship passage vs. quiet water)
- Concept sketches for touch/sound feedback and the remote-listener network
- Journal note on the decision to reframe it as a process piece and move to *Weaving With*

Repository note, 2026-11-10: those files are in `~/Desktop/Hydrophone`, outside this repository. They were on this machine when the claim was filed. `docs/build-log.md` there begins 2026-10-26. They are not in this commit.

## Strongest objection

Translating hydrophone data into touch and sound for human comfort is still a human-centred aestheticisation of orca experience. Without any data from human participants (the course setup cannot include them for ethics reasons), the claim that remote listening "dissolves the central ego" is a design intention, not an observed effect. Also the data is simple and far away from us. The local data is much more approachable and related to audience and designer.

## Next action

Make two short audio-tactile renderings of the same 10-minute stream segment: one with the ship noise filtered out, one with the masking kept and emphasised. Compare them side by side and write down what relation each makes perceivable. This gives point 3 concrete evidence before any participant study at DIS stage. Also need to find the more suitable data which is layered and also more accessible and indigenous.
