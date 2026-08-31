# Marking smoke tests

These files test package behavior with synthetic text. They do not validate a
security classification, CUI designation, export determination, distribution
decision, system, or recipient. Never substitute real controlled or classified
content into a test on an unapproved system.

Run the repository test suite on macOS or Linux with:

```sh
./scripts/build.sh --test
```

On Windows, use `scripts\build.cmd --test`; in PowerShell, use
`.\scripts\build.ps1 --test`.

The ordinary corporate report, corporate presentation, and presentation
acronym smokes produce harmless PDFs. Their automated log gate rejects
overfull boxes, unresolved citations or references, duplicate destinations,
and multiply defined labels. It does not currently reject underfull-box
diagnostics; visual QA remains separate.

Expected-failure fixtures exercise unknown controls, reserved banners, raw
official distribution text, expanded blank fields, inconsistent CUI banner
overrides, raw portion marks, late first-page notices, over-wide banners, and
the DoD classified/CUI commingling rule. They also reject Statement A without
DoD authority confirmation and a DoD export-controlled-technical-information
configuration whose distribution reasons omit the exact `Export Controlled`
category. Jurisdiction/control mismatches and invalid DoD category/statement
combinations also fail before shipout.
A setup-order regression proves that a preamble page override is checked again
against the final profile. Every one must fail for its named reason at the
intended validation boundary; the release-notice deadline fixture necessarily
reaches the second-page shipout check. The runner deletes stale or partial PDFs
so a failed build cannot leave an old success artifact looking current.

Current expected-failure coverage also includes:

- nonblank choice-menu initialization through unsupported `default=` or
  `value=` options, which could otherwise disagree with a blank appearance;
- title-background overlay opacity outside the inclusive `0` through `1`
  range;
- malformed, lowered, or profile-incompatible Confidential banners and portion
  marks, including the DoD classified/CUI rule;
- blank, placeholder, duplicate, late, or too-few multi-owner proprietary
  declarations, plus incompatible owner mode, control, and corporate banner;
- stale classification attestations and export-jurisdiction mismatches;
- invalid or duplicate DoD distribution categories and missing required export
  determinations; and
- missing release notices, CTI distribution statements, and invalid
  unclassified Statement F use.

The following positive fixtures deliberately use LuaLaTeX `-draftmode` and
contain no controlled or classified information:

- `structured-distribution-draft.tex`
- `public-release-validation-draft.tex`
- `export-controls-validation-draft.tex`
- `itar-controls-validation-draft.tex`
- `dod-export-controlled-validation-draft.tex`
- `dod-export-not-applicable-validation-draft.tex`
- `classified-dod-validation-draft.tex`
- `classified-presentation-validation-draft.tex`
- `classified-export-statement-f-validation-draft.tex`
- `confidential-classified-validation-draft.tex`
- `unclassified-profile-validation-draft.tex`
- `alternate-cui-only-banner-validation-draft.tex`
- `multi-owner-proprietary-validation-draft.tex`
- `presentation-components-draft.tex`
- `presentation-acronyms-smoke.tex`
- `presentation-slide-markings-draft.tex`
- `full-combination-report-layout-draft.tex`
- `full-combination-legal-layout-draft.tex`
- `full-combination-memo-layout-draft.tex`
- `full-combination-presentation-layout-draft.tex`

The same draft-only pass also compiles all five sources under
`templates/marking-demos/`:

- `synthetic-confidential-demo.tex`
- `synthetic-ear-demo.tex`
- `synthetic-itar-demo.tex`
- `synthetic-secret-demo.tex`
- `synthetic-top-secret-demo.tex`

They exercise rendering and validation logic without retaining PDFs. The
classified-profile fixtures are synthetic software tests only; their labels
are not classification decisions or authority records. The full-combination
document fixtures prove that each stock title flow keeps its compact, complete
notice stack on one physical cover and emits the required DoDD release notice
as page 2. The presentation fixture proves that its title remains one physical
slide, the immediately following disclosure renders the release notice, and
automatic disclosure continuation stays within an explicit six-slide cap.
The presentation-components fixture covers the reusable background, team, and
one- through ten-stage milestone layouts. Acronym pagination and slide-local
marking helpers have focused fixtures of their own; the main presentation build
covers the reference and narrative helpers. The five marking previews are
compiled in draft mode only during `--test`; use the separate
`marking-demos` build target when their synthetic PDFs are intentionally needed.
