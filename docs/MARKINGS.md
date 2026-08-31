# Markings and handling controls

This guide separates markings that look similar but have different legal and
security meanings. It was checked against the official sources linked below on
2026-08-30. The contract, security classification guide, CUI authority,
controlling DoD office, and current agency instruction always control.

## Non-negotiable boundary

This package renders labels and rejects some internally inconsistent settings.
It does **not** classify information, determine CUI, make an export
classification, grant a license, approve public release, accredit a system,
authorize a recipient, or prove compliance. Its confirmation keys are operator
attestations, not technical controls.

Do not paste, compile, preview, cache, synchronize, back up, or commit
classified content on an unclassified system. Use these sources for CUI or
export-controlled data only when every person, endpoint, repository, build
tool, intermediate file, backup, and recipient is approved for that data.

The safe default is:

```tex
\LSMarkingSetup{profile=uncontrolled,classification=none,controls={}}
```

## Independent layers

| Layer | Meaning | Configuration |
|---|---|---|
| Corporate | Proprietary/confidentiality legends for one or multiple private owners | `controls={proprietary}` and `proprietary-mode` |
| Export | EAR/ITAR jurisdiction and transaction constraints | `ear`, `itar` |
| CUI | Unclassified information controlled under an applicable authority | `cui` |
| Classification | Overall national-security classification: Confidential, Secret, or Top Secret | `classification=confidential`, `secret`, or `top-secret` |
| Distribution | DoD technical-information audience determination | `distribution-code=A` through `F` |

EAR and ITAR are not classification levels or universal page banners. CUI is
not a synonym for corporate sensitivity. A DoD distribution statement is not
a classification marking and does not replace CUI or classified markings.

Contractual or corporate use of the word “confidential” is also not the U.S.
national-security classification `CONFIDENTIAL`. Put contractual language in
the reviewed proprietary legend, agreement, or other applicable notice. Use
`classification=confidential` and an uppercase `CONFIDENTIAL` banner only for
authorized national-security information on an approved classified system.

## Profiles and banners

| Profile | Intended rule set | Banner rule enforced by this package |
|---|---|---|
| `uncontrolled` | No declared page marking | blank; no colored banner |
| `unclassified` | Positive unclassified marking, with no CUI or classified information | exactly `UNCLASSIFIED`, rendered in green |
| `corporate` | Proprietary/export workflow | single-owner proprietary: exactly `LINEAR SPACE PROPRIETARY`; multi-owner proprietary: exactly `PROPRIETARY, SEE TITLE PAGE`; otherwise blank |
| `cui-general` | 32 CFR Part 2002 and controlling-agency rules | uppercase `CUI`/`CONTROLLED` form supplied by the authority |
| `cui-dod` | Unclassified DoD CUI | exactly `CUI` |
| `classified-general` | Classified, non-DoD-specific agency rules | exact `CONFIDENTIAL`, `SECRET`, or `TOP SECRET` level prefix; CUI-bearing output must include `//CUI` |
| `classified-dod` | DoD classified rules | exact `CONFIDENTIAL`, `SECRET`, or `TOP SECRET` prefix; `CUI` is forbidden in the banner |

The accepted `classification` values are `none`, `confidential`, `secret`, and
`top-secret`. The `uncontrolled` profile deliberately stays blank; use
`unclassified` only when an exact positive `UNCLASSIFIED` marking is required
and the material contains neither CUI nor classified information.

Banner input is expanded once, trimmed, validated, and frozen. Runtime CUI
overrides must exactly equal the document's inclusive banner. Reserved
classification words are rejected in unclassified profiles. A banner that is
too wide for the physical page or slide is a fatal error; mandatory text is
never silently cropped or reduced.

The stock document and presentation renderers center the literal banner text
in the top and bottom bars. `UNCLASSIFIED` uses the package's green banner;
other colors follow the configured profile and level. Colors are visual
navigation only. They do not establish a marking, are not official
classification indicators, and never replace the centered text.

## Corporate and export examples

The default proprietary legend is Linear Space language, not government-
prescribed wording. `proprietary-notice` is customizable only after the
applicable agreement and counsel approve it.

```tex
\LSMarkingSetup{
  profile=corporate,
  classification=none,
  controls={proprietary}
}
```

### Multiple proprietary owners

Use multi-owner mode when proprietary material from two or more organizations
appears in the same document. Declare each owner and its separately reviewed
legend or disclosure in the preamble:

```tex
\LSDeclareProprietaryOwner
  {Fictional Owner Alpha}
  {Fictional Owner Alpha proprietary information; use and disclosure are
   governed by the applicable agreement.}
\LSDeclareProprietaryOwner
  {Fictional Owner Beta}
  {Fictional Owner Beta proprietary information; use and disclosure are
   governed by the applicable agreement.}

\LSMarkingSetup{
  profile=corporate,
  classification=none,
  controls={proprietary},
  proprietary-mode=multi-owner
}
```

The names above are deliberately fictional. Replace each with the reviewed
legal name and replace each legend with the text approved for that owner and
agreement. Multi-owner mode requires at least two unique declarations and
rejects declarations outside that mode. The page or slide banner is exactly
`PROPRIETARY, SEE TITLE PAGE`; the stock title-page notice pairs every owner
with its own reviewed legend.

The same declarations may accompany a CUI or classified profile when the
material also contains those owners' proprietary data. In that case, the CUI
or classified government banner remains the page or slide banner; the
corporate owner legends remain on the title page and do not replace the
government marking.

EAR/ITAR output requires a review record rather than a bare acronym:

```tex
\LSMarkingSetup{
  profile=corporate,
  classification=none,
  controls={proprietary,ear},
  operator-confirms-controlled-environment=true,
  export-jurisdiction={EAR},
  export-classification={REPLACE ME},
  export-authorization={REPLACE ME},
  export-destination={REPLACE ME},
  export-end-user={REPLACE ME},
  export-end-use={REPLACE ME},
  export-contact={REPLACE ME},
  export-review-date={REPLACE ME}
}
```

`REPLACE ME`, `TBD`, `TODO`, `YYYY-MM-DD`, and a wholly bracketed value are
rejected in required fields. The export metadata notice is a workflow aid, not
an official export determination or destination-control statement. The
separate `\LSEARDestinationControlStatement`,
`\LSITARDestinationControlStatement`, and `\LSDoDExportControlWarning` presets
must be selected only when the cited rule and transaction actually require
them.

Export fields are mandatory whenever `controls` contains `ear` or `itar`, and
forbidden otherwise. `export-jurisdiction` must exactly match the control set:
`EAR`, `ITAR`, or `EAR and ITAR`. The required reviewed fields are
classification, authorization, destination, end-user, end-use, contact, and
review date.

A DoD profile containing `ear` or `itar` requires an explicit reviewed
`dod-export-controlled-technical-information=true` or `false` determination;
the package will not infer the DoDI 5230.24 result from jurisdiction metadata
alone. The defense categories `Export Controlled`, `Critical Technology`, and
`Direct Military Support` are definitionally export-controlled and therefore
enable the path automatically; an explicit `false` then conflicts and fails.
For unclassified `cui-dod` CTI, the enabled path requires Distribution
Statement B, C, D, or E and the exact `Export Controlled` reason. `Critical
Technology` or `Direct Military Support` alone therefore fails on that path;
add `Export Controlled` only when the controlling office approved both
reasons. For `classified-dod`, the enabled path requires the controlling
office's Statement B, C, D, E, or F determination. The package does not impose
the unclassified reason rule on that classified path; Statement F has no
category field.

The title page or cover then includes the full DoDI 5230.24 export-control
warning and structured distribution statement. The stock document classes add
an immediate second page containing the complete DoDD 5230.25, Enclosure 5
release notice. In Beamer, place `\LSMarkingDisclosureFrame` immediately after
the title slide; it carries that full notice across continuation slides when
needed. The directive text contains legacy statutory citations and penalties,
so the controlling office must verify the current prescribed notice before
release; do not silently rewrite it in the template.

The unclassified B--E restriction follows the assignment rule in DoDI 5230.24
Section 3.4.i and Table 1. The classified path follows Sections 3.3.a and
4.3.e(3), which permit B--F; the controlling office still determines the
specific statement and any applicable reason.

## CUI

Only designate CUI when the information falls within the CUI Registry and a
law, regulation, government-wide policy, or controlling agreement applies.

An unclassified DoD example skeleton is:

```tex
\LSMarkingSetup{
  profile=cui-dod,
  classification=none,
  controls={cui},
  operator-confirms-controlled-environment=true,
  banner-text={CUI},
  controlled-by={REPLACE ME},       % DoD Component
  controlled-office={REPLACE ME},   % determining office
  cui-categories={REPLACE ME},
  distribution-dissemination-control={REPLACE ME},
  control-poc={REPLACE ME}
}
```

For the DoD profiles, the designation indicator uses two `Controlled By:`
lines, `CUI Category:`, and `POC:`. When a structured DoD statement is
configured, the fourth row is exactly `Distribution Statement:` followed by
the letter. Otherwise it is `Distribution/Dissemination Control:` followed by
the originator-approved dissemination value; do not infer that `NONE` applies.
For unclassified DoD CTI, `cui-categories` must include the exact delimited
token `CTI` and a structured B--F statement is mandatory; conversely, a DoD
unclassified B--F profile requires that `CTI` token. `control-poc` must be the
controlling office's phone number and/or office mailbox, not merely a person's
name.

For `cui-general`, supply the exact inclusive banner and values required by the
controlling agency. The package checks the banner's basic form and consistency,
not whether a category or limited-dissemination token is substantively valid.

## DoD Distribution Statements A--F

Use the structured API only. Raw `distribution-statement` text and the old
`\LSDistributionStatementA` through `F` constructors are fatal errors, so an
official sentence cannot be silently rewritten through an escape hatch.

Statement A requires an actual public-release approval:

```tex
\LSMarkingSetup{
  profile=uncontrolled,
  classification=none,
  controls={},
  distribution-code=A,
  public-release-approved=true,
  operator-confirms-dod-distribution-authority=true
}
```

Statements B--E require the defense-category heading, determination date, and
controlling DoD office. F requires the date and office but no category:

```tex
\LSMarkingSetup{
  % ...DoD CUI or DoD classified fields...
  distribution-code=C,
  distribution-categories={REPLACE ME},
  distribution-date={REPLACE ME},
  distribution-office={REPLACE ME},
  operator-confirms-dod-distribution-authority=true
}
```

`distribution-categories` is the preferred key. It accepts one to three unique
entries and treats `CTI` and `Controlled Technical Information` as the same
category for duplicate detection. The current consistency whitelist is:

| Accepted category | B--E codes accepted by the package |
|---|---|
| Controlled Technical Information (`CTI` alias) | B, C, D, E |
| Contractor Performance Evaluation | B, E |
| Critical Technology | B, C, D, E |
| Direct Military Support | E |
| Export Controlled | B, C, D, E |
| Foreign Government Information | B, C, D, E |
| IAs | B, C, D, E |
| Operations Security | B, E |
| Patents and Inventions | B, E |
| Proprietary Business Information | B, E |
| SBIR | B, E |
| Software Documentation | B, C, D, E |
| Test and Evaluation | B, E |
| Vulnerability Information | B, C, D, E |

Statement F has no category field in its prescribed sentence, so the package
requires `distribution-categories` to be blank for F. This whitelist only
catches structural inconsistencies; it does not make the controlling office's
substantive determination.

The package owns the fixed A--F sentence structure and substitutes only these
reviewed fields. It cannot determine the correct code, authorized audience,
defense category, date, or office. DoDI 5230.24 says the prescribed wording
may not be modified. Where its narrative and summary table differ, this
implementation follows the quoted statement in Section 4.2 and still requires
controlling-office confirmation. It also makes unclassified technical information bearing
B--F subject to DoD CUI handling; the package therefore requires
`profile=cui-dod` and `controls={cui}` for unclassified B--F output, and
`profile=classified-dod` for classified B--F output.

Statement A is rejected with any declared control or classification. The
public-release and DoD-authority booleans must be set only after the competent
authority's determination. Statement F has additional scope restrictions that
software cannot evaluate; consult the controlling office.

## Classified output and CUI commingling

The classified profiles accept `classification=confidential`,
`classification=secret`, or `classification=top-secret`. These values produce
national-security `CONFIDENTIAL`, `SECRET`, or `TOP SECRET` markings; they are
not labels for contractual or corporate confidentiality.

The following is a reference skeleton only. Never test it with real classified
content or on an ordinary workstation.

```tex
\LSMarkingSetup{
  profile=classified-dod,
  classification=secret,
  controls={},
  operator-confirms-classified-environment=true,
  banner-text={SECRET},
  authority-type=derivative,
  classified-by={REPLACE ME},
  derived-from={REPLACE ME},
  declassify-on={REPLACE ME}
}
```

Original classification instead requires `authority-type=original`,
`classification-reason`, and
`original-classification-authority-confirmed=true`; `derived-from` must then be
blank. Derivative output requires `derived-from`, while
`classification-reason` must be blank. These checks do not verify anyone's
authority or the cited source.

`classification-date` is intentionally rejected. Use `\LSSetup{date=...}` for
document metadata only. The rendered authority block contains `Classified By`,
`Reason` or `Derived From`, and `Declassify On`.

Commingling differs by profile:

- `classified-general` with `controls={cui}` requires the controlling agency's
  commingled banner containing `//CUI`.
- `classified-dod` with `controls={cui}` forbids `CUI` in the banner and permits
  only `(CUI)` for CUI-only portions. It also requires the DoD designation
  fields and `classified-cui-source`. The package generates the fixed DoDI
  5200.48 Figure 1 warning structure, inserting the configured classification
  level and source; `classified-cui-contact` is an optional reviewed POC. Raw
  `classified-cui-warning` text is disabled.

## Portion marks

Use only the typed helpers:

```tex
\LSU{Unclassified portion.}
\LSCUI{CUI portion under the configured authority.}
\LSCUI[SP-CTI]{General-profile category example only.}
\LSC{Confidential portion.}
\LSS{Secret portion.}
\LSTS{Top Secret portion.}
```

`\LSPortion` and `\LSPortionMark` are intentionally disabled. `\LSCUI`
requires CUI; `\LSC` requires Confidential, Secret, or Top Secret output;
`\LSS` requires Secret or Top Secret output; and `\LSTS` requires Top Secret.
Optional CUI category/control tokens are prohibited in DoD profiles. In a
general profile, an optional token must be uppercase, have safe syntax, and
occur as a delimited token in the validated inclusive banner.

Every content portion in a classified briefing must be portion marked,
including unclassified content with `\LSU`/`(U)`. This applies to content such
as titles, bullets, captions, tables, and graphics according to the controlling
instruction; a visually obvious classification level is not a substitute for
the required portion mark.

The package cannot discover unmarked paragraphs, captions, titles, tables,
notes, hidden slides, or attachments. A reviewer must apply every required
portion mark consistently.

## First page, slides, and runtime enforcement

The built-in document title/header macros call `\LSCompactMarkingNotices`,
which preserves the complete cover-notice text while tightening its layout.
When markings or a distribution statement require notices, the package fails
before the first page ships if that cover set has not been rendered. A custom
title may call either the compact or full renderer before first shipout.

For DoD B--F output, the stock report and legal covers place the CUI
designation indicator in the lower-right notice column and put the complete
distribution statement directly beneath it. The memo class inserts a dedicated
cover page for that profile. Custom title pages must preserve this placement.

The Linear Space Beamer theme registers its own top-and-bottom banner renderer.
It confirms banner emission at every shipout; disabling or replacing the theme
bar without an equivalent confirmation is fatal. The stock title template
renders all compact cover notices on slide 1 and uses the same lower-right DoD
placement. `\LSMarkingDisclosureFrame` is an optional readable duplicate for
ordinary profiles. It is mandatory immediately after the title slide for the
DoD export-controlled-technical-information path because it carries the full
DoDD 5230.25 release notice; the notice may continue across generated slides.

Use `\LSIfClassifiedTF{classified code}{unclassified code}` in custom layouts.
If replacing the title template, render `\LSCompactMarkingNotices` before the
first slide ships; a classification authority block alone is not the complete
cover set. Validation proves timely invocation, not substantive accuracy or
that a customized renderer preserved every physical position.

### Classified presentation slide rules

For a classified briefing, the first slide carries the overall presentation
marking. Later slides may carry that overall presentation marking or an
individual slide marking appropriate to the information on that slide, as the
controlling instruction permits. All content in the classified briefing still
requires portion markings, including `(U)` for unclassified portions. The
software does not inspect slide content or determine whether a chosen overall,
individual-slide, or portion marking is correct or missing.

Use the exact green `UNCLASSIFIED` banner only for an individually marked slide
that contains no CUI and no classified information. A CUI-only individual
slide instead uses the exact CUI or `CONTROLLED` banner authorized by the
controlling authority. Other applicable corporate, export, dissemination, and
distribution requirements still apply.

`\LSValidateCUIOnlyBanner{...}` is a narrow validation helper for that CUI-only
individual-slide case. It checks an uppercase CUI/`CONTROLLED`-only banner and
requires `controls={cui}`, but it does not draw a banner, change the overall
document banner, or decide whether the slide qualifies. The Beamer theme's
public wrapper consumes this result safely; custom presentation renderers must
consume `\LSValidatedBannerText` immediately after validation and must not save
or reuse it after another marking operation:

```tex
\LSValidateCUIOnlyBanner{CUI}
% A custom renderer must immediately draw \LSValidatedBannerText.
```

For the stock Beamer theme, prefer:

```tex
\begin{LSSlideMarking}{unclassified}
  \begin{frame}{\LSU{Unclassified title}}
    \LSU{Unclassified content.}
  \end{frame}
\end{LSSlideMarking}

\begin{LSSlideMarking}[CUI//SP-EXAMPLE]{cui}
  \begin{frame}{\LSCUI{CUI title}}
    \LSCUI{CUI content.}
  \end{frame}
\end{LSSlideMarking}
```

The optional banner is forbidden in `unclassified` mode; the exact green
`UNCLASSIFIED` marking is automatic. A blank optional banner in `cui` mode uses
`CUI`. The wrapper is available only in an overall CUI-bearing or classified
deck, cannot be used on the first slide, must contain exactly one frame or
one frame-producing Linear Space helper, and must produce exactly one physical
slide. It rejects `allowframebreaks` and restores the overall banner after the
slide. These are mechanical guards only; an authorized reviewer must determine
whether the individual marking and every portion mark are correct.

`\LSSetRunningBanner`, `\LSThisPageBanner`, and `\LSFrameBanner` validate and
store the expanded canonical value. CUI-bearing runtime overrides must exactly
match the document banner. The CUI-only helper above is the separate,
non-mutating validation path for a renderer that implements an authorized
individual-slide banner. The package does not validate speaker notes, hidden
slides, embedded files, or exported handouts. A DoD presentation derived from
multiple sources may also need the full source list on the first or last slide;
the compact authority block does not generate that list.

## What the fail-closed checks still cannot prove

The package rejects unknown controls, incompatible profiles, missing or
expanded-blank required fields, common placeholder values, stale inapplicable
structured fields, malformed/down-marked banners, unchecked raw portions, raw
official distribution text, late notices, missing registered-renderer
confirmation, and over-wide mandatory banners. Those are consistency checks
only.

LaTeX remains programmable. A user can alter package internals, replace output
routines, convert the PDF incorrectly, or lie in an attestation field. The
software cannot inspect factual authority, category eligibility, recipients,
end use, system accreditation, hidden source files, or whether a customized box
visibly overflowed. The stock layouts implement the documented DoD cover
placement, but software cannot prove that a user-modified title still does.
Treat successful compilation as the start of human review, never as a release
decision.

## Pre-release review

An authorized reviewer should verify:

1. actual national-security classification, including the distinction between
   `CONFIDENTIAL` and contractual or corporate confidentiality, the CUI
   category, and the governing authority;
2. every proprietary owner's reviewed legal name and legend, the title-page
   owner/legend pairs, and the two-or-more-owner rule when multi-owner mode is
   selected;
3. the overall marking on the first classified slide, the permitted overall or
   individual marking on every later slide, every required portion mark
   including `(U)`, and the eligibility of any CUI-only or `UNCLASSIFIED`
   individual slide;
4. exact document banners, first-page blocks, distribution text, and the
   centered top-and-bottom rendering of every required banner;
5. EAR/ITAR jurisdiction, ECCN/USML category, authorization, destination,
   end-user, and end use;
6. recipients, repository, endpoint, cache, backup, and transmission approval;
7. notes, hidden slides, attachments, source data, logs, and intermediates; and
8. the rendered PDF/handout, not only the LaTeX source.

## Official sources

- [32 CFR 2002.20, marking CUI](https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002/section-2002.20)
- [NARA CUI FAQs](https://www.archives.gov/cui/faqs.html)
- [NARA CUI Marking Handbook](https://www.archives.gov/files/cui/documents/20161206-cui-marking-handbook-v1-1-20190524.pdf)
- [NARA CUI Registry](https://www.archives.gov/cui/registry/category-list)
- [32 CFR Part 2001, Subpart C, classified marking](https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2001/subpart-C)
- [ISOO classified marking booklet](https://www.archives.gov/files/isoo/notices/marking-booklet-revision.pdf)
- [DoDM 5200.01 Volume 2](https://www.esd.whs.mil/portals/54/Documents/DD/issuances/dodm/520001m_vol2.pdf)
- [DoDI 5200.48, DoD CUI Program](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF)
- [DoDI 5230.24, distribution statements](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf)
- [DoDD 5230.25, export-controlled technical-data release notice](https://www.esd.whs.mil/portals/54/documents/dd/issuances/dodd/523025p.pdf)
- [BIS: classify your item](https://www.bis.gov/licensing/classify-your-item)
- [15 CFR 758.6, destination control statement](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-758/section-758.6)
- [22 CFR 123.9, ITAR country of ultimate destination](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-123/section-123.9)

Use the current source and controlling instruction. This guide is not legal
advice, export advice, or classification guidance.
