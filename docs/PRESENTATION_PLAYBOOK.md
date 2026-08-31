# Presentation playbook

The Linear Space Beamer theme is designed for investor, customer, program, and
technical reviews on 16:9 monitors and televisions. The PDF canvas is vector;
text, equations, TikZ diagrams, and PGFPlots remain sharp at 1080p, 1440p, and
4K. Raster photographs are limited by their source resolution.

The macro signatures are in [API.md](API.md). This guide explains how to use
them well.

## Build an argument, not an illustrated report

A strong decision deck normally follows this sequence:

1. State the decision or opening question.
2. Establish the customer, mission, or business consequence.
3. Show the smallest amount of evidence needed to support the claim.
4. Make uncertainty, assumptions, and alternatives visible.
5. Show the credible execution path and accountable team.
6. End with one requested decision, owner, and date.

Use one claim per slide. A title should state that claim, not merely name a
topic. “Qualification closes the remaining launch risk” is stronger than
“Qualification.”

A 20-minute external meeting rarely benefits from 40 dense slides. Keep
decision-driving evidence in the main narrative and move traceability,
derivations, secondary charts, and detailed references to an appendix.

## Typography and density

The theme uses a 36 pt content-slide title and an 18–25 pt primary body range.
These sizes are chosen for conference-room displays, not laptop-only reading.

- Keep content titles to one line whenever possible.
- Use three to five top-level bullets. A bullet should normally fit on one line.
- Use no more than two bullet levels.
- Prefer a direct label next to a chart or diagram over a distant legend.
- Keep chart labels at 12–14 pt or larger.
- Put full contractual, legal, export, CUI, or classification notices in the
  required notice area; never shrink mandatory text to make decorative content
  fit.
- Split a slide before reducing the body below a readable size.

The footer is intentionally quiet. Navigation ornaments are disabled, and the
top-right green arrow/circle decoration from the reference deck is not part of
this custom theme.

## Backgrounds and contrast

Every image frame uses a proportional cover crop. Adjust the crop with
`focal-x` and `focal-y`; never distort the image to fill 16:9.

```tex
\begin{LSBackgroundFrame}[
  opacity=0.64,
  focal-x=-0.30in,
  focal-y=0.10in
]{pillars-of-creation}
  \vfill
  \LSStatement{The mission closes a capability gap that customers already fund.}
  \vfill
\end{LSBackgroundFrame}
```

The black overlay is a design and legibility control:

- `0.35–0.48`: quiet image with large, short white text.
- `0.52–0.68`: normal content over an image.
- `0.70–0.82`: detailed cards, milestones, or small labels.
- Above `0.85`: use a black slide unless the image is intentionally only
  texture.

Inspect the actual crop. A mathematically high overlay cannot fix bright detail
directly behind a thin label. Move the focal point, add a local panel, or select
a quieter image.

The stock title uses the exact owner-supplied `red-blue-galactic-core` image
with `\LSTitleBackgroundOverlay{0}`: no part of the image is dimmed. The title
overlay remains configurable from `0` through `1` and, when nonzero, covers the
whole canvas uniformly rather than darkening one side. Milestone slides also
default to `overlay=0`; set a nonzero value explicitly only after checking the
actual image and text contrast.

## Raster resolution

For native full-screen imagery, target at least the display resolution after
the 16:9 crop:

| Display | Preferred 16:9 source |
|---|---:|
| 1080p | 1920 × 1080 |
| 1440p | 2560 × 1440 |
| 4K UHD | 3840 × 2160 |

The bundled source dimensions are:

| Registered background | Source pixels | Practical note |
|---|---:|---|
| `webb-clouds` | 2560 × 1440 | Native 1440p; acceptable upscaling on 4K at normal viewing distance. |
| `milky-way-panorama` | 4000 × 2000 | Wide and close to 4K after crop, but slightly short vertically. |
| `black-hole` | 1040 × 580 | Accent/divider use; not a native 1080p or 4K full bleed. |
| `explosive-galaxy` | 5292 × 3240 | Suitable for a 4K cover crop. |
| `galaxy-explosion-render` | 1672 × 941 | Below native 1080p. |
| `webb-clouds-original` | 6000 × 2947 | Suitable for a 4K cover crop. |
| `jupiter-rings` | 3283 × 2829 | Strong portrait crop; below native 4K when widened to 16:9. |
| `milky-way-supplied` | 1280 × 640 | Accent/divider use; below native 1080p. |
| `moon-from-earth` | 1672 × 941 | Below native 1080p. |
| `night-sky` | 1920 × 1279 | Native 1080p width with vertical crop. |
| `phantom-galaxy` | 1977 × 1130 | Approximately native 1080p. |
| `pillars-of-creation` | 1280 × 741 | Accent/divider use; below native 1080p. |
| `tarantula-nebula` | 2000 × 1157 | Approximately native 1080p. |
| `red-blue-galactic-core` | 1672 × 941 | Exact owner-supplied title image; below native 1080p. |

Upscaling does not create detail. For a flagship 4K presentation, replace
lower-resolution assets with verified higher-resolution originals when the
license and provenance permit it.

## Milestones

The component supports one to ten milestones. Three to five usually tell the
clearest executive story; use six to ten only when the audience needs the
complete gate sequence. Each item needs a state, outcome, and date—not a
task-list fragment.

- `completed`: reserve for accepted evidence or an actually closed gate.
- `in-progress`: use for the single gate currently consuming execution focus.
- `upcoming`: use for future commitments.
- Keep descriptions parallel: all outcomes or all acceptance criteria.
- Dates should use one convention across the slide: month/year, quarter/year,
  or an explicit calendar date.
- Keep a title to two lines and the description to three lines at most. The
  reserved slots preserve date alignment and the clear connector channel.
- If every milestone is “in progress,” the states are not communicating useful
  information.

The completed circle, outlined in-progress marker, and restrained upcoming
square intentionally match the reading language of the supplied milestone
reference while using stronger text/background contrast.

One to five gates form one centered row. Six to ten use five gates on the top
row and a centered lower row. The dotted connector leaves gate 5 to the right,
runs through protected side gutters and the clear channel between rows, then
enters gate 6 from the left; do not place custom annotations in that channel.

## Team

Use two to four accountable people on a team slide. A strong card contains:

- an authorized, consistently cropped portrait;
- verified name and role;
- one sentence explaining why this person can deliver the plan.

Do not repeat a résumé. Put detailed experience in speaker notes or an appendix.
If a portrait is not cleared, use the initials placeholder. The optional media
panel is best for one product, facility, or mission image that supports the
team's credibility.

## Metrics, charts, and technical evidence

Use `\LSMetric` only for a number that materially changes the decision. Always
state the unit, time basis, population, and source close to the metric.

Prefer PGFPlots and version-controlled CSV data to chart screenshots. For every
plot:

- identify measured, simulated, estimated, or synthetic data;
- show units on axes;
- show requirement/decision thresholds;
- include uncertainty when it affects the conclusion;
- use direct labels or a compact legend;
- cite the source and date.

Equations should earn their space. Define the variables and state the
interpretation or limitation in the same slide. A customer or investor should
not need to reverse-engineer why an equation changes the decision.

## Acronyms and references

Declare acronyms in the preamble and use `\LSAcronym{key}` in content. The
first use expands by default, and `\LSAcronymFrame` prints only entries that
were actually used.

Keep references separate with `\LSReferencesFrame`. Cite a claim on the slide
with `\autocite{key}`; do not rely on an unseen bibliography to indicate which
source supports which statement.

Acronym and reference slides usually belong in the appendix immediately after
the decision close, unless the audience needs them earlier.

## Markings

The title slide renders required compact notices. Every marked slide repeats
the validated banner in centered top and bottom colored bands. A dedicated
`\LSMarkingDisclosureFrame` is useful when the audience needs to read the
full notice and is mandatory for the configured DoD release-notice path.

Corporate confidentiality, proprietary ownership, EAR/ITAR jurisdiction, CUI,
and national-security classification are different concepts. Do not invent a
combined banner. For multiple proprietary owners, use the multi-owner registry;
the corporate banner becomes “PROPRIETARY, SEE TITLE PAGE,” and the title
notice lists each owner-specific legend.

Never use the synthetic Confidential, EAR, ITAR, Secret, or Top Secret demo
decks as authority. They contain fictional metadata and harmless placeholder
content solely to preview the renderer.

For an authorized individual UNCLASSIFIED or CUI-only slide inside an overall
CUI-bearing or classified deck, use the one-frame `LSSlideMarking` wrapper from
[API.md](API.md). It rejects slide 1, multiple physical slides, and
`allowframebreaks`, then restores the overall banner automatically. It cannot
decide whether the slide qualifies; every classified-briefing content portion,
including titles and unclassified text, still needs the reviewed portion mark.

## Screen and meeting QA

Before a high-value presentation:

1. Build from a clean checkout and reject all overfull boxes, missing
   references, and unresolved citations.
2. Inspect every slide at full size.
3. Test at 1920 × 1080 and at the highest target display resolution.
4. Test the real conferencing or room path; video compression can erase thin
   rules and subtle dark gradients.
5. Confirm that every chart remains understandable in grayscale and for common
   color-vision deficiencies.
6. Verify image crop, focal point, resolution, credit, and reuse terms.
7. Confirm names, roles, customer statements, financial values, dates, and
   citations with the responsible owner.
8. Confirm every proprietary, export, CUI, distribution, and classification
   marking with the authorized reviewer.
9. Keep a PDF fallback and test the exact display machine before the meeting.
10. Present from the released PDF; do not depend on workstation-specific fonts,
    animations, or network content.

For a multi-million-dollar external deck, visual polish is the last gate—not
the first. Unsupported claims, ambiguous asks, unreadable evidence, and stale
numbers are more damaging than an imperfect decorative detail.
