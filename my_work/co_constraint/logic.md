# Co-Constraint — logic & interface (v1)

Scaffold for the course proposal in `my_work/topic.md`.  
Open: `my_work/tools/co_constraint.html`

---

## Interface (3 columns)

| Column | Role |
|---|---|
| **Left** | Human protocol + mapping + simulated nonhuman source |
| **Centre** | Raw signal strip + generative drawing |
| **Right** | AI → human prompts + hard refusals |

Colour coding: **teal** = nonhuman channel · **warm gold** = AI-to-human · **light** = human protocol.

---

## Logic

```text
signal ∈ [0,1]     ← simulated now; later: real external data
humanBase          ← sliders you set
mapped?            ← checkboxes (density / step / turn / band)
influence ∈ [0,1]

if mapped:
  live = lerp(humanBase, signalShaped, influence)
else:
  live = humanBase

drawing uses live only (no manual override of live values while running)
```

AI (v1) is **scripted**, watching:

- mappedCount == 0 → extractive / no encounter  
- only density mapped → decorative use of signal  
- influence very low → token share  
- high human density while signal low and density unmapped → beautify / compensate  
- otherwise periodic decentering questions  

AI **never** interprets the signal as language or species emotion.

---

## Replace later

1. Simulated source → real channel + site (your decision).  
2. Scripted AI → optional constrained LLM with the same refusals.  
3. Screen → optional SVG plotter print as evidence.
