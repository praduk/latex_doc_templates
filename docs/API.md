# Public LaTeX API

This is the reference for commands intended to be used in cloned document
repositories. Braces are required arguments; brackets are optional arguments.
Configuration commands belong in the preamble unless a section explicitly says
otherwise.

All stock targets require LuaLaTeX. The shared classes and Beamer theme load
the brand, math, and marking packages automatically.

## Document metadata

### `\LSSetup{key=value,...}`

Sets metadata shared by every class and the presentation theme.

| Key | Meaning | Default |
|---|---|---|
| `title` | Full title used on the cover and in PDF metadata. | `Untitled Document` |
| `subtitle` | Optional explanatory subtitle. | blank |
| `short-title` | Running header/footer title. Keep it short. | `Untitled Document` |
| `author` | Person, team, or responsible organization. | `Author` |
| `organization` | Owning/publishing organization. | `Linear Space` |
| `document-id` | Controlled identifier. | `LS-DOC-0000` |
| `revision` | Revision identifier. | `A` |
| `status` | Draft/review/released status. | `Draft` |
| `date` | Explicit issue date is preferred for baselines. | `\today` |
| `project` | Optional project/program name. | blank |
| `client` | Optional customer/recipient. | blank |

Example:

```tex
\LSSetup{
  title={Optical Navigation Performance Analysis},
  subtitle={Qualification configuration},
  short-title={Navigation Performance},
  author={Guidance, Navigation, and Control Team},
  organization={Linear Space},
  document-id={LS-ENG-0042},
  revision={B},
  status={Released},
  date={2026-08-31},
  project={Example Spacecraft},
  client={Example Customer}
}
```

Read-only accessors are `\LSTitle`, `\LSSubtitle`, `\LSShortTitle`,
`\LSAuthor`, `\LSOrganization`, `\LSDocumentID`, `\LSRevision`,
`\LSStatus`, `\LSDate`, `\LSProject`, and `\LSClient`.

### `\LSIfBlankTF{value}{blank-code}{nonblank-code}`

Expands `blank-code` when `value` is empty and `nonblank-code` otherwise.
It is useful in project-specific cover layouts.

## Branding

The website-style wordmark is the official L artwork followed immediately by
typeset “inear Space.” The logo and text share one baseline and cannot break
across a line. The stock artwork is pixel-calibrated so its bottom-most active
pixel aligns with the bottom of the lowercase `i`, and the visible
logo-to-`i` gap equals the `i`-to-`n` gap at every supported scale.

| Command | Arguments | Purpose |
|---|---|---|
| `\LSWordmark[height]` | optional mark height, default `1.05in` | Dark text for a light background. |
| `\LSWordmarkDark[height]` | optional mark height, default `1.05in` | White text for a dark or photographic background. |
| `\LSWordmarkOnLight[height]` | optional height, default `1.05in` | Backward-compatible alias for `\LSWordmark`. |
| `\LSWordmarkOnDark[height]` | optional height, default `1.05in` | Backward-compatible alias for `\LSWordmarkDark`. |
| `\LSLogoOnLight[width]` | optional width, default `1.65in` | Raw configured logo artwork on a light background. |
| `\LSLogoOnDark[width]` | optional width, default `1.65in` | Raw configured logo artwork on a dark background. |
| `\LSLogoSolar[width]` | optional width, default `1.65in` | Raw optional solar-system logo artwork. |
| `\LSSetLogoLight{path}` | image path | Replaces the light-background logo asset for this project. |
| `\LSSetLogoDark{path}` | image path | Replaces the dark-background logo asset for this project. |
| `\LSSetLogoSolar{path}` | image path | Replaces the optional solar-system logo asset. |

Use transparent PNG or PDF artwork. The shell-escape-free build does not import
SVG directly; convert a project SVG to PDF first.

## Mathematics, units, diagrams, and plots

The classes and theme load `linearspace-math`, including `mathtools`,
`unicode-math`, `siunitx`, TikZ, and PGFPlots.

| Command | Result |
|---|---|
| `\vect{x}` | Bold vector. |
| `\mat{A}` | Bold matrix. |
| `\unitvect{e}` | Bold unit vector with a hat. |
| `\norm{x}` | Automatically sized norm. |
| `\abs{x}` | Automatically sized absolute value. |
| `\inner{x}{y}` | Inner product. |
| `\expect{x}` | Expectation. |
| `\prob{A}` | Probability. |
| `\odv{y}{t}` | First ordinary derivative. |
| `\odv[n]{y}{t}` | Ordinary derivative of order `n`. |
| `\pdv{f}{x}` | First partial derivative. |
| `\pdv[n]{f}{x}` | Partial derivative of order `n`. |
| `\skewmat{\omega}` | Cross-product/skew-matrix notation. |
| `\evalat{f(x)}{x=0}` | Evaluation bar. |

Sets are `\Rset`, `\Cset`, `\Nset`, `\Zset`, `\Qset`, and
`\Hset`. Other helpers include `\Identity`, `\transpose`, `\rank`,
`\trace`, `\diag`, `\Cov`, `\Var`, `\SO`, `\SE`, and `\GL`.

Use `\qty{3.2}{\milli\radian}` for values with units. Apply the PGFPlots
style `linearspace` in documents and `linearspace dark` in presentations.

## Markings and handling

### `\LSMarkingSetup{key=value,...}`

Configures independent corporate, export, CUI, classification, and DoD
distribution layers. The safe default is:

```tex
\LSMarkingSetup{
  profile=uncontrolled,
  classification=none,
  controls={}
}
```

The configuration freezes when the document begins. A controlled or classified
setting that lacks required reviewed fields fails the build. Validation detects
some inconsistencies; it does not determine a classification, export
jurisdiction, CUI status, authorized audience, or approved system.

Core keys:

| Key | Accepted value |
|---|---|
| `profile` | `uncontrolled`, `unclassified`, `corporate`, `cui-general`, `cui-dod`, `classified-general`, or `classified-dod`. |
| `classification` | `none`, `confidential`, `secret`, or `top-secret`. |
| `controls` | Comma list drawn from `proprietary`, `ear`, `itar`, and `cui`. |
| `banner-text` | Exact reviewed uppercase banner when the selected profile requires one. Corporate proprietary defaults are supplied automatically. |
| `render-page-banners` | `true` or `false`; keep enabled unless a registered theme renders the banner. |
| `custom-notice` | Additional reviewed handling text rendered on the cover/title page. |

Export-control keys used when `controls` contains `ear` or `itar`:

- `operator-confirms-controlled-environment=true`
- `export-jurisdiction={EAR}`, `{ITAR}`, or `{EAR and ITAR}`
- `export-classification={reviewed value}`
- `export-authorization={reviewed value}`
- `export-destination={reviewed value}`
- `export-end-user={reviewed value}`
- `export-end-use={reviewed value}`
- `export-contact={reviewed contact}`
- `export-review-date={reviewed date}`
- optional `export-notice={reviewed workflow notice}`

CUI keys:

- `operator-confirms-controlled-environment=true`
- `controlled-by`
- `controlled-office` for DoD profiles
- `cui-categories`
- `distribution-dissemination-control`
- `control-poc`

Classification-authority keys:

- `operator-confirms-classified-environment=true`
- `authority-type=original` or `derivative`
- `classified-by`
- `classification-reason` for original classification
- `derived-from` for derivative classification
- `declassify-on`
- `original-classification-authority-confirmed=true` only for an authorized
  original-classification decision
- `classified-cui-source` and optional `classified-cui-contact` when the
  selected DoD classified/CUI rules require them

Structured DoD distribution keys:

- `distribution-code=A` through `F`
- `distribution-categories={reviewed category list}` for B through E
- `distribution-date={reviewed determination date}`
- `distribution-office={controlling DoD office}`
- `operator-confirms-dod-distribution-authority=true`
- `public-release-approved=true` for Statement A
- `dod-export-controlled-technical-information=true` or `false` when a DoD
  export-control determination is required

The exact validation rules, profile combinations, and official-source links are
in [MARKINGS.md](MARKINGS.md).

`profile=uncontrolled` means no banner. `profile=unclassified` is a deliberate
visible marking that automatically produces exact `UNCLASSIFIED` text in dark
green top and bottom bands; it requires `classification=none` and no CUI or
classified content. National-security `classification=confidential` is a real
classification setting and is distinct from contractual or corporate use of
the ordinary word “confidential.”

### Single-owner proprietary data

```tex
\LSMarkingSetup{
  profile=corporate,
  classification=none,
  controls={proprietary}
}
```

The running banner is exactly `LINEAR SPACE PROPRIETARY`. Override
`proprietary-notice={...}` only with counsel-approved Linear Space language.

### Multiple proprietary owners

Use `proprietary-mode=multi-owner` and declare every owner with its own
reviewed legend:

```tex
\LSMarkingSetup{
  profile=corporate,
  classification=none,
  controls={proprietary},
  proprietary-mode=multi-owner
}
\LSDeclareProprietaryOwner
  {Example Prime}
  {Example Prime proprietary information. Use and disclosure are limited by
   the applicable written agreement.}
\LSDeclareProprietaryOwner
  {Example Partner}
  {Example Partner proprietary information. Apply the legend and permissions
   approved by Example Partner.}
```

The names above are fictional placeholders for API illustration. Replace both
names and both legends with the reviewed values for the actual owners.

The corporate running banner becomes exactly
`PROPRIETARY, SEE TITLE PAGE`. The cover notice pairs each owner with its
legend. At least two owners are required. Owner names are matched
case-insensitively for duplicate detection; blank, placeholder, duplicate, or
late declarations fail the build.

For a CUI or classified profile, the applicable inclusive government banner
still controls the page edge. The multi-owner proprietary disclosure remains
on the title page; it is not concatenated into the CUI or classification
banner.

### Portion marks

| Command | Meaning and gate |
|---|---|
| `\LSU{text}` | Renders `(U) text`. |
| `\LSCUI{text}` | Renders `(CUI) text`; requires `controls={cui}`. |
| `\LSCUI[token]{text}` | General-profile CUI category/control token; the validated inclusive banner must contain it. |
| `\LSC{text}` | Renders `(C) text`; requires Confidential, Secret, or Top Secret output. |
| `\LSS{text}` | Renders `(S) text`; requires Secret or Top Secret output. |
| `\LSTS{text}` | Renders `(TS) text`; requires Top Secret output. |

Raw `\LSPortion` and `\LSPortionMark` calls are intentionally disabled.

### Advanced banner and layout hooks

| Interface | Purpose |
|---|---|
| `\LSSetRunningBanner{exact-text}` | Revalidates and changes the running document banner. It cannot weaken the configured profile. |
| `\LSThisPageBanner{exact-text}` | Applies one validated document-page override; it resets after shipout. |
| `\LSDisablePageBanners` / `\LSEnablePageBanners` | Renderer controls for custom classes. Required UNCLASSIFIED, controlled, CUI, or classified banners cannot be disabled unless a registered alternate renderer takes responsibility. |
| `\LSValidateBanner{exact-text}` | Validates a candidate against the complete configured profile. Read the canonical result immediately from `\LSValidatedBannerText`. |
| `\LSValidateCUIOnlyBanner{exact-text}` | Validates a literal uppercase `CUI`/`CONTROLLED` individual-slide banner, requires `controls={cui}`, rejects classification terms, and leaves the overall banner unchanged. Read `\LSValidatedBannerText` immediately. |
| `\LSIfControlTF{token}{true-code}{false-code}` | Branches on one configured control token. |
| `\LSIfClassifiedTF{true-code}{false-code}` | Branches on whether a classified profile is active. |

The Beamer theme's one-slide marking wrapper is the preferred presentation
interface; do not manually combine the low-level validator with a frame banner.
Class/theme registration and render-confirmation commands are implementation
hooks, not normal document-authoring APIs.

### Notice renderers

Stock title commands call the correct compact renderer automatically.

| Command | Purpose |
|---|---|
| `\LSMarkingNotices` | Full-size applicable notice set. |
| `\LSCompactMarkingNotices` | Compact cover/title-page notice set. |
| `\LSProprietaryNotice` | Applicable single- or multi-owner proprietary notice. |
| `\LSCUIDesignationIndicator` | Structured CUI designation block. |
| `\LSExportControlMetadata` | Reviewed export metadata block. |
| `\LSClassificationAuthorityBlock` | Full authority block. |
| `\LSCompactClassificationAuthorityBlock` | Compact authority block. |
| `\LSDistributionNotice` | Structured DoD distribution statement. |
| `\LSDoDReleaseNotice` | Prescribed release notice when configured. |
| `\LSDoDReleaseNoticePage` | Dedicated document page for that notice when required. |
| `\LSNoticeBox{heading}{body}` | Generic styled notice; it does not bypass any required structured notice. |

The exact EAR/ITAR destination-control presets are
`\LSEARDestinationControlStatement` and
`\LSITARDestinationControlStatement`. Use them only when the reviewed
transaction and current rule require that exact preset. Direct
`\LSDistributionStatementA` through `\LSDistributionStatementF`
constructors are disabled; configure structured distribution keys instead.

## Engineering report

Load the class with:

```tex
\documentclass{linearspace-report}
```

| Interface | Arguments | Purpose |
|---|---|---|
| `\LSMakeReportTitle` | none | Cover plus any mandatory release-notice page. |
| `\LSMakeReportFrontMatter` | none | Roman-numbered cover and contents, then Arabic page numbering. |
| `\begin{LSRevisionHistory} ... \end{LSRevisionHistory}` | table rows | Styled revision-history long table. Supply four cells per row: revision, date, author, description. |
| `\begin{LSRequirements} ... \end{LSRequirements}` | `\item` entries | Numbered requirements. Use stable `\label{...}` keys; visible `REQ-n` numbers change when items are inserted or reordered. |
| `\begin{LSKeyPoint}[title] ...` | optional title | Blue engineering callout. |
| `\begin{LSWarning}[title] ...` | optional title | Amber caution callout. |

The class also defines `Y`, `C`, and `R` stretchable table-column types
and the `linearspace` listings style.

## Legal document

Load the class with:

```tex
\documentclass{linearspace-legal}
```

### `\LSLegalSetup{key=value,...}`

| Key | Meaning | Default |
|---|---|---|
| `party-a`, `party-b` | Short role names used in prose and headings. Full legal names belong in form fields. | `First Party`, `Second Party` |
| `effective-date` | Cover text; the sample points to Document Details. | `See Document Details` |
| `governing-law` | Prose accessor; the sample points to the governing-law form field. | `See Governing Law field` |
| `title-note` | Drafting instruction on the cover; set to empty only after review. | Built-in form-completion and legal-review warning. |
| `counsel-disclaimer` | Counsel disclaimer on the cover; set to empty only after review. | Built-in qualified-counsel warning. |

Read accessors are `\LSPartyA`, `\LSPartyB`, `\LSEffectiveDate`,
`\LSGoverningLaw`, `\LSLegalTitleNote`, and
`\LSLegalCounselDisclaimer`.

| Interface | Arguments | Purpose |
|---|---|---|
| `\LSMakeLegalTitle` | none | Legal cover and required notice flow. |
| `\begin{legalclauses} ...` | `\item` entries; three nesting levels | Article-aware clause numbering. |
| `\DefinedTerm{term}` | term | Bold quoted defined term. |
| `\LSEnableLineNumbers` / `\LSDisableLineNumbers` | none | Turn review line numbers on/off. |
| `\LSExhibit{letter}{title}` | exhibit label and title | Starts and registers an exhibit. |
| `\LSSignatureBlock{party}{name}{title}` | three strings | Print-only signature block. Prefer the fillable form block when interactivity is required. |

The fillable API is documented in [FORMS.md](FORMS.md).

## Memo

Load the class with:

```tex
\documentclass{linearspace-memo}
```

### `\LSMemoSetup{key=value,...}`

| Key | Meaning | Default |
|---|---|---|
| `to` | Decision authority or recipients. | `[Recipient]` |
| `from` | Responsible author. | `[Author]` |
| `cc` | Optional copied reviewers. | blank |
| `subject` | Decision-oriented subject. | `[Decision or subject]` |
| `action-required` | Optional owner/action/date callout. | blank |

Read accessors are `\LSMemoTo`, `\LSMemoFrom`, `\LSMemoCC`,
`\LSMemoSubject`, and `\LSMemoAction`.

Call `\LSMakeMemoHeader` once at the start. The normal letterhead contains
only the centered website-style Linear Space wordmark. Identifier, revision,
and status remain in the running header.

## Fillable AcroForms

The complete field reference, viewer checks, report approval example, and
signature guidance are in [FORMS.md](FORMS.md). The principal interfaces are:

- `\begin{LSForm} ... \end{LSForm}`
- `\LSFormTextField[options]{name}{label}`
- `\LSFormInlineTextField[options]{name}`
- `\LSFormMultilineField[options]{name}{label}`
- `\LSFormInlineMultilineField[options]{name}`
- `\LSFormCheckBox[options]{name}{label}`
- `\LSFormChoiceMenu[options]{name}{label}{choices}`
- `\LSFormSignatureBlock[width]{party-label}{field-prefix}`

## Acronyms

The Beamer theme loads `linearspace-acronyms` automatically. A document may
load it explicitly with `\usepackage{linearspace-acronyms}`.

### Declaration and use

```tex
\LSDeclareAcronym{gnc}{GNC}{guidance, navigation, and control}
\LSDeclareAcronym{ekf}{EKF}{extended Kalman filter}

The \LSAcronym{gnc} design uses an \LSAcronym{ekf}.
Later, \LSAcronym{gnc} emits only the short form.
```

| Command | Behavior |
|---|---|
| `\LSDeclareAcronym{key}{short}{long}` | Declares one unique nonblank entry. |
| `\LSAcronym{key}` | Records use; emits `long (short)` on first use and `short` thereafter by default. |
| `\LSAcronym*{key}` | Records use and emits only the short form. |
| `\LSAcronymShort{key}` | Records use/seen and emits only the short form. |
| `\LSAcronymLong{key}` | Records use and emits only the long form; does not mark the short form as introduced. |
| `\LSAcronymFull{key}` | Records use/seen and always emits `long (short)`. |
| `\LSResetAcronym{key}` | Makes the next normal use expand again. |
| `\LSResetAllAcronyms` | Resets first-use state for every declaration. |
| `\LSClearUsedAcronyms` | Clears the used-entry list without deleting declarations. |
| `\LSPrintAcronyms` | Prints only acronyms recorded as used, in declaration order. |
| `\LSAcronymSetup{expand-first-use=false}` | Globally disables automatic first-use expansion; the default is `true`. |

An undeclared, duplicate, or blank acronym is a fatal error. No index,
makeglossaries, shell escape, or extra glossary pass is required.

Resetting first-use state does not remove an acronym from the used-entry list.
Conversely, `\LSClearUsedAcronyms` does not make a previously introduced
acronym expand again. Call both operations when starting a logically separate
deck section that needs a fresh first-use policy and a fresh printed table.

## Beamer presentation

Start with:

```tex
\documentclass[aspectratio=169,professionalfonts]{beamer}
\usetheme{LinearSpace}
```

The canvas is 10 by 5.625 inches (16:9). Frame titles are 36 pt; normal
presentation text is designed around 18–25 pt. Do not shrink dense content to
fit.

### Background registry and cover crop

`\LSDeclareBackground{name}{path}` registers a project-specific short name.
Every background-taking interface accepts either that name or a direct image
path. Missing files fail the build.

Built-in names:

| Name | Path |
|---|---|
| `webb-clouds` | `assets/backgrounds/james-webb-cloudy-space-16x9.jpg` |
| `milky-way-panorama` | `assets/backgrounds/milky-way-panorama.jpg` |
| `black-hole` | `assets/backgrounds/user-supplied/black-hole.png` |
| `explosive-galaxy` | `assets/backgrounds/user-supplied/explosive-galaxy.jpg` |
| `galaxy-explosion-render` | `assets/backgrounds/user-supplied/galaxy-explosion-render.png` |
| `webb-clouds-original` | `assets/backgrounds/user-supplied/james-webb-cloudy-space-original.png` |
| `jupiter-rings` | `assets/backgrounds/user-supplied/jwst-jupiter-rings.jpg` |
| `milky-way-supplied` | `assets/backgrounds/user-supplied/milky-way-supplied.jpg` |
| `moon-from-earth` | `assets/backgrounds/user-supplied/moon-from-earth.png` |
| `night-sky` | `assets/backgrounds/user-supplied/night-sky.jpg` |
| `phantom-galaxy` | `assets/backgrounds/user-supplied/phantom-galaxy.jpg` |
| `pillars-of-creation` | `assets/backgrounds/user-supplied/pillars-of-creation.png` |
| `tarantula-nebula` | `assets/backgrounds/user-supplied/tarantula-nebula-jwst.png` |
| `red-blue-galactic-core` | `assets/backgrounds/user-supplied/red-blue-galactic-core.png` |

The two backgrounds outside `user-supplied/` have independently documented
sources and reuse terms. The owner-approved supplied library remains subject to
project-specific source, rights, and credit review before external publication;
see [ASSET_PROVENANCE.md](../assets/ASSET_PROVENANCE.md).

`\LSBackgroundPath{name-or-path}` expands a registered name to its path.

| Interface | Arguments |
|---|---|
| `\LSSetTitleBackground{name-or-path}` | Sets title image. `\LSTitleBackground{...}` is an equivalent spelling. |
| `\LSTitleBackgroundFocus{x-shift}{y-shift}` | Moves the cover-cropped title image without stretching it. |
| `\LSTitleBackgroundOverlay{opacity}` | Sets a full-canvas black title overlay from `0` through `1`; default `0` is completely transparent. |
| `\LSTitleBackgroundCredit{text}` | Adds a concise visible title-image credit/source line; default is blank. |
| `\begin{LSImageFrame}[opacity]{name-or-path} ...` | Legacy image frame; overlay default is `0.42`, focal shift is zero. |
| `\begin{LSBackgroundFrame}[keys]{name-or-path} ...` | Image frame with `opacity`, `focal-x`, and `focal-y` keys. |

Opacity is from 0 (no black overlay) to 1 (solid black). Backgrounds are scaled
proportionally to cover the canvas and clipped; they are never stretched.
The stock title uses `red-blue-galactic-core` full bleed with no darkening
overlay. `\LSSetTitleBackground` changes the image but does not add an overlay;
call `\LSTitleBackgroundOverlay{...}` explicitly only when a different title
image needs uniform darkening. The title overlay always covers the full canvas,
not one side of the image.

### General narrative components

| Interface | Arguments |
|---|---|
| `\LSSectionSlide[opacity]{background}{eyebrow}{statement}[speaker-note]` | Full-image section divider. Default opacity is `0.40`. |
| `\LSStatement{text}` | Large 34 pt decision statement inside a frame. |
| `\LSMetric{value}{caption}` | One metric tile; three fit naturally across a slide. |
| `\begin{LSBullets}[item-separation] ...` | 18 pt premium bullet list. Default separation is `0.13in`. |
| `\LSDecisionSlide{title}{left-heading}{left-body}{right-heading}{right-body}{center-view}` | Two-sided tradeoff plus a concluding center view. |
| `\LSQuoteSlide[background]{quote}{attribution}{role-or-source}` | Quote slide; omit the background for black. |
| `\LSClosingSlide[background]{closing-statement}{call-to-action}{contact}` | Full-image close. Default background is `webb-clouds`. |

### Team slide

```tex
\begin{LSTeamSlide}[
  background=red-blue-galactic-core,
  overlay=0.72,
  eyebrow={Leadership}
]{The team built to execute}
  \LSTeamMember[P1]{}
    {Replace with verified name}{Verified role}
    {Replace with one verified, decision-relevant proof point.}
  \LSTeamMember[P2]{}
    {Replace with verified name}{Verified role}
    {Replace with one verified, decision-relevant proof point.}
\end{LSTeamSlide}
```

`\LSTeamSlide[keys]{frame-title}` accepts two to four
`\LSTeamMember` calls. Keys are `background`, `overlay`, `focal-x`,
`focal-y`, `eyebrow`, `media`, and `media-side=left|right`.
`\LSTeamMember[initials]{photo-path}{name}{role}{proof-point}` uses a rounded
cover-cropped photo. Leave `photo-path` empty to show the initials
placeholder. The command fails outside a team-slide environment.

Team-slide key defaults are `background=` (blank), `overlay=0.52`,
`focal-x=0in`, `focal-y=0in`, `eyebrow=Team`, `media=` (blank), and
`media-side=left`. Member initials default to `LS`; pass explicit initials for
an intentional placeholder. A media path, when supplied, is resolved through
the same background registry and placed on the selected side.

Use real names, roles, portraits, and claims only after authorization and
verification. Do not invent credentials to make a layout look complete.

### Milestone slide

```tex
\begin{LSMilestoneSlide}[
  background=milky-way-panorama,
  overlay=0.72,
  focal-x=0in,
  focal-y=0in,
  eyebrow={Execution plan}
]{Milestones}
  \LSMilestone[status=completed]{1}{Prototype}
    {Dominant technical risk retired.}{MAR 2026}
  \LSMilestone[status=in-progress]{2}{Qualification}
    {Environmental evidence is being collected.}{AUG 2026}
  \LSMilestone[status=upcoming]{3}{Pilot}
    {Validate operations with the launch customer.}{Q4 2026}
\end{LSMilestoneSlide}
```

`\LSMilestoneSlide[keys]{frame-title}` accepts one to ten milestones.
Slide keys are `background`, `overlay`, `focal-x`, `focal-y`, and
`eyebrow`. Defaults are `background=` (the normal black canvas), `overlay=0`,
`focal-x=0in`, `focal-y=0in`, and `eyebrow=Roadmap`.

`\LSMilestone[options]{number}{title}{body}{date}` accepts:

| Option | Values | Default |
|---|---|---|
| `status` | `completed`, `in-progress`, or `upcoming` | `upcoming` |
| `accent` | Any defined LaTeX color | `LSDeckLime` |

Completed items use a filled circular marker and a high-contrast filled date
bar. In-progress items use a strongly outlined square, activity dot, and
outlined status/date bar. Upcoming items use restrained charcoal markers and
date bars. One to five milestones occupy one centered row. Six to ten occupy
two row-major rows with no more than five per row; a shorter second row is
centered. Titles are sized for up to two lines and descriptions for up to three
lines of normal presentation copy. The dotted sequence leaves gate 5 from its
right edge, uses protected side gutters and a clear horizontal channel between
the rows, and joins gate 6 at its left edge without crossing milestone text or
date bars.

### Acronym and reference slides

`\LSAcronymFrame[title]` prints the used-acronym table; the default title is
“Acronyms and abbreviations.”

Load `biblatex`, add a resource, cite normally, and call
`\LSReferencesFrame[title]`. The default title is “References,” and long
bibliographies continue automatically:

```tex
\usepackage[backend=biber,style=ieee,sorting=none]{biblatex}
\addbibresource{templates/shared-data/references.bib}

% in slide content
Result interpretation follows \autocite{maybeck1979}.

% near the end
\LSAcronymFrame
\LSReferencesFrame
```

### Marking disclosure slide

The title slide already renders every required compact cover notice.
`\LSMarkingDisclosureFrame` creates a readable expanded duplicate. It is
mandatory immediately after the title when the configured DoD
export-controlled-technical-information path requires the full release notice.

`\LSFrameBanner{exact-banner}` is an advanced preamble override. It is
validated against the selected profile; it cannot be used to weaken a CUI or
classification banner.

### One-slide UNCLASSIFIED and CUI markings

Within an overall CUI-bearing or classified presentation, wrap exactly one
later frame (or one Linear Space helper that produces one frame) when the
authorized individual-slide marking differs from the overall deck banner:

```tex
\begin{LSSlideMarking}{unclassified}
  \begin{frame}{\LSU{Public interface}}
    \LSU{Every content portion on this slide is unclassified.}
  \end{frame}
\end{LSSlideMarking}

\begin{LSSlideMarking}[CUI//SP-EXAMPLE]{cui}
  \begin{LSMilestoneSlide}[eyebrow={\LSCUI{Roadmap}}]
    {\LSCUI{Controlled execution plan}}
    \LSMilestone{1}{\LSCUI{Gate}}{\LSCUI{Reviewed CUI content.}}{\LSCUI{Q1}}
  \end{LSMilestoneSlide}
\end{LSSlideMarking}
```

The environment signature is
`\begin{LSSlideMarking}[exact-CUI-banner]{unclassified|cui}`. In
`unclassified` mode the optional argument must be blank and the green exact
`UNCLASSIFIED` banner is automatic. In `cui` mode a blank optional argument
uses `CUI`; otherwise the supplied uppercase `CUI`/`CONTROLLED`-only banner is
validated. The scope restores the overall banner automatically.

This wrapper is prohibited on slide 1 and in uncontrolled, corporate-only, or
already-unclassified decks. It fails if it contains zero or multiple frames,
uses `allowframebreaks`, or produces more than one physical slide. It validates
banner mechanics, not whether the slide content is actually eligible for the
selected individual marking. Portion-mark every title, paragraph, list item,
caption, table, and graphic annotation as the controlling instruction requires.

`\LSEnableSyntheticDemoWatermark` adds
“SYNTHETIC DEMONSTRATION — NOT CLASSIFIED” to every slide. It is for the
bundled harmless marking previews, not for production decks.

## Stability and extension

Treat commands documented here as the public layer. Commands containing
`@`, expl3 names containing `_`, and internal `ls...` environments are
implementation details.

For project-specific styling, add a small package such as `tex/project.sty`
rather than editing every class. Keep source data, bibliography files, image
credits, and verification evidence under version control with the document.
