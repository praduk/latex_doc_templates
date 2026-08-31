# Customization guide

The template separates content from shared design. Edit a project `main.tex`
freely; change files under `tex/` only when the change should affect every
document cloned from that revision of the template.

See [API.md](API.md) for exact macro signatures and defaults,
[FORMS.md](FORMS.md) for interactive PDF fields and signing workflows,
[MARKINGS.md](MARKINGS.md) for handling rules, and
[PRESENTATION_PLAYBOOK.md](PRESENTATION_PLAYBOOK.md) for display and narrative
guidance.

## Branding

Shared colors, fonts, and logo paths live in `tex/linearspace-brand.sty`.
Semantic color names such as `LSInk`, `LSBlue`, `LSSlate`, and `LSRule` are
stable interfaces. Change their definitions centrally instead of replacing
colors throughout individual documents.

Override a logo for one project without editing the package:

```tex
\LSSetLogoLight{assets/branding/project-logo.png}
\LSSetLogoDark{assets/branding/project-logo-on-dark.png}
```

Use transparent PNG or PDF assets. Plain LuaLaTeX/`graphicx` does not import
SVG directly in this shell-escape-free workflow; convert an SVG to PDF before
referencing it. Verify transparency over both white and photographic
backgrounds. The stock wordmark is pixel-calibrated to the supplied 512 by 512
initial-mark artwork: its active bottom aligns with the lowercase `i`, and the
logo-to-`i` gap matches the `i`-to-`n` gap at every scale. After replacing that
artwork, remeasure both relationships in a high-resolution render.

## Engineering report

Use `linearspace-report` for analyses, design descriptions, ICDs, verification
reports, and manuals. The example includes:

- revision history, executive summary, contents, figures, and tables;
- requirements with stable source label keys and automatically rendered
  `REQ-n` numbers (visible numbers change when items are inserted or reordered);
- theorem and definition environments;
- TikZ architecture/flow graphics;
- PGFPlots reading version-controlled CSV data;
- warning and key-point callouts; and
- a Biber bibliography.

Prefer short, declarative headings. Put assumptions next to the model they
limit. Give every figure and table a caption, label, provenance, unit system,
and uncertainty statement where applicable.

## Legal document

Use `linearspace-legal` for a formal structure that counsel will review. Set
short party roles and cover metadata through `\LSLegalSetup`, use the nested
`legalclauses` list, and complete or deliberately remove every drafting field
inside the document's single `LSForm` environment. Give each AcroForm field a
unique, stable ASCII name. `\LSEnableLineNumbers` is available for filing/review
conventions.

The sample agreement is not a jurisdiction-complete contract. It deliberately
does not invent indemnity, limitation-of-liability, intellectual-property,
privacy, employment, government-contract, or export terms for an unknown
transaction.

The title's drafting note and counsel disclaimer are safe defaults. After every
form value and drafting choice is resolved and qualified counsel approves the
final form, they can be suppressed without editing the shared class:

```tex
\LSLegalSetup{
  % ...parties, date, and governing law...
  title-note={},
  counsel-disclaimer={}
}
```

## Memo

Use `linearspace-memo` for a decision record. Set the routing block through:

```tex
\LSMemoSetup{
  to={Decision authority},
  from={Responsible author},
  cc={Reviewers},
  subject={Decision in plain language},
  action-required={Owner, action, and due date.}
}
```

Lead with the recommendation, show the center view and rejected extremes, name
the evidence needed, and close with owned actions.

## Presentation

The Beamer theme is optimized for a 10 inch by 5.625 inch 16:9 canvas. Use the
same one-claim discipline as the supplied reference deck, but keep text within
the template's margins and avoid shrinking tables to compensate for excess
content. The complete background, milestone, team, acronym, reference, and
narrative-component APIs are in [API.md](API.md); practical screen and meeting
guidance is in [PRESENTATION_PLAYBOOK.md](PRESENTATION_PLAYBOOK.md).

### Background and section frames

Change the title background:

```tex
\LSTitleBackground{assets/backgrounds/approved-image-16x9.jpg}
\LSTitleBackgroundOverlay{0} % transparent default; valid range is 0 through 1
```

The title overlay, when nonzero, darkens the full canvas uniformly. It never
creates a left-side-only dark panel.

Create a cover-cropped image frame with a black overlay opacity from 0 to 1:

```tex
\begin{LSImageFrame}[0.46]{assets/backgrounds/approved-image-16x9.jpg}
  \vfill
  \LSStatement{A single claim that earns the transition.}
  \vfill
\end{LSImageFrame}
```

Or use the section helper:

```tex
\LSSectionSlide[0.42]
  {assets/backgrounds/approved-image-16x9.jpg}
  {Section 02}
  {Customer evidence changes the decision}
  [{[Sources] Background: provider/creator. See assets/ASSET_PROVENANCE.md.}]
```

Images are scaled proportionally to cover the canvas and clipped by the page;
they are never stretched. Use a crop that leaves quiet space behind text.

### Content helpers

```tex
\LSStatement{A large statement.}
\LSMetric{42\%}{Short explanation of the metric}
```

Use normal Beamer `columns`, `block`, `alertblock`, TikZ, and PGFPlots for other
layouts. The example demonstrates equations, charts, tradeoffs, and a metric
close. The `linearspace dark` PGFPlots style adapts axes and legends to the
black canvas.

### Slide typography

- Frame titles: 36 pt.
- Section statements: 38--48 pt.
- Primary body: about 18--25 pt.
- Chart labels: 12--14 pt minimum.
- Footer: 9.3 pt.

Do not solve overflow by reducing body text below readable presentation size.
Split the claim or move detail to an appendix. Test the deck on the actual
projector or conferencing pipeline; dark gradients and thin rules can collapse
under compression.

### Image credits

Record the source, creator, rights basis, adaptations, and retrieval date for
every third-party image. Retain a complete visible credit wherever the source,
license, or publication policy requires one. The sample deck keeps a final
credits slide and speaker-note source records; keep that slide synchronized
with the images actually used. The independently sourced examples and the
owner-approved background library have different provenance status. See
[`assets/ASSET_PROVENANCE.md`](../assets/ASSET_PROVENANCE.md) before external
publication.

## Plots and external data

Store small, reviewable source data under `templates/shared-data/` or a
project-specific `data/` directory. Read it directly from PGFPlots so the chart
and the reviewed values cannot drift apart:

```tex
\addplot table[x=time,y=error,col sep=comma]{data/test-run.csv};
```

State whether data are measured, simulated, estimated, or synthetic. Include
units and uncertainty. Avoid screenshots of charts when a vector plot is
possible.

## Fonts

Documents use TeX Gyre Pagella/Heros and TeX Gyre Pagella Math. The Beamer
theme uses TeX Gyre Heros on every platform so line breaks are deterministic.
Do not extract embedded fonts from the reference PowerPoint unless the font
license independently authorizes it.

## Project-level design changes

The safest extension pattern is a small project package:

```tex
% tex/project.sty
\ProvidesPackage{project}
\RequirePackage{linearspace-brand}
\definecolor{ProjectAccent}{HTML}{00A6A6}
\newcommand{\ProjectName}{Program Name}
```

Load it from `main.tex`. This keeps upstream template updates reviewable and
avoids a fork of every shared class.

## Visual QA

For each release, render and inspect every page or slide at full size. Check
page size, crop, baselines, equation breaks, table widths, footers, banners,
link targets, image resolution, and font embedding. For fillable PDFs, also
check field order, widget appearance, representative saved values, and printed
or exported values in the recipient's intended viewer. A clean compiler log is
necessary but not sufficient.
