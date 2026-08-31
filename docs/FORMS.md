# Fillable PDF forms and signatures

The legal template uses native PDF AcroForm fields. They are real interactive
widgets, not pictures of blank boxes. The same controls can be loaded in an
engineering report when a report needs approvals, acknowledgements, or data
entry.

AcroForms help collect information; they do not provide legal review,
identity proofing, tamper evidence, or a certificate-backed digital signature.

## Minimal pattern

`linearspace-legal` loads the form package automatically. In another class,
load it explicitly after the document class:

```tex
\documentclass{linearspace-report}
\usepackage{linearspace-forms}

\begin{document}
\begin{LSForm}
  \LSFormTextField[required,maxlen=120]
    {reviewer_legal_name}{Reviewer legal name}
  \LSFormMultilineField[maxlen=1200]
    {reviewer_comments}{Review comments}
\end{LSForm}
\end{document}
```

Put every field in exactly one `LSForm` environment. The package deliberately
rejects fields outside that environment, nested forms, and a second form
environment. One canonical form tree is easier to validate and less likely to
break in downstream signing or document-management tools.

## Field API

Optional arguments use the applicable `hyperref` form-field options. Useful
examples include `required`, `maxlen=120`, `readonly`, and `checked` for a
checkbox. Keep the explicit field name separate from those options. Choice
menus deliberately reject `default=` and `value=`: they start blank so the
stored value and the package's viewer-independent blank appearance cannot
silently disagree.

| Interface | Arguments | Result |
|---|---|---|
| `\begin{LSForm} ... \end{LSForm}` | none | Owns the document's single canonical AcroForm. |
| `\LSFormTextField[options]{name}{label}` | optional field options; stable field name; printed label | Full-width, single-line text field. Default height is `1.70em`. |
| `\LSFormInlineTextField[options]{name}` | optional field options; stable field name | Single-line field for a table cell or a layout that already has a label. |
| `\LSFormMultilineField[options]{name}{label}` | optional field options; stable field name; printed label | Full-width multiline field. Default height is `0.82in`. |
| `\LSFormInlineMultilineField[options]{name}` | optional field options; stable field name | Multiline field for a table cell or custom layout. Default height is `0.62in`. |
| `\LSFormCheckBox[options]{name}{label}` | optional field options; stable field name; printed label | Checkbox with its label to the right. |
| `\LSFormChoiceMenu[options]{name}{label}{choices}` | optional field options; stable field name; printed label; comma-separated choices | Blank-initialized pop-down choice field. The choices follow `hyperref` syntax; `Display text=export-value` may be used when the stored value should differ. `default=` and `value=` are rejected. |
| `\LSFormSignatureBlock[width]{party-label}{prefix}` | optional width, default `0.46\textwidth`; visible party label; stable field-name prefix | Physical signature line plus signing-method, typed-name, title/capacity, and date fields. |

For example:

```tex
\LSFormChoiceMenu[required]
  {review_disposition}{Disposition}
  {Approved,Approved with comments,Rejected}

\LSFormCheckBox{review_complete}
  {I completed the document-preparation review.}
```

Field names must be unique and match this pattern:

```text
[A-Za-z][-A-Za-z0-9_]*
```

Good names are stable, descriptive identifiers such as
`agreement_effective_date` and `reviewer_legal_name`. Do not derive names from
page numbers or clause numbers that are likely to change. The package stops the
build on a blank, malformed, or duplicate name.

`\LSFormSignatureBlock{First Party}{agreement_party_a_signature}` generates
these four fields:

```text
agreement_party_a_signature_signing_method
agreement_party_a_signature_typed_name
agreement_party_a_signature_title
agreement_party_a_signature_date
```

The prefix therefore must also be unique.

## Signature workflows

For a report approval page:

```tex
\clearpage
\chapter*{Approval}
\begin{LSForm}
  \noindent
  \LSFormSignatureBlock{Prepared by}{report_preparer}
  \hfill
  \LSFormSignatureBlock{Approved by}{report_approver}
\end{LSForm}
```

Choose the execution method based on the transaction and the recipient's
requirements:

- The visible line supports printing and an ink signature.
- The typed-name field is an ordinary text field. It is not a PDF `/Sig`
  object and does not prove identity or detect later changes.
- For certificate-based PDF signatures, PAdES, qualified signatures, or an
  e-signature service, compile the final unsigned PDF first and use the
  approved downstream signing system. Do not recompile after signing; a new
  PDF invalidates the earlier signature relationship.
- Keep a controlled unsigned master, the completed signing copy, and any
  certificate/audit record required by policy. Flatten only a separate archive
  copy when the recipient or records policy requires it.

## Viewer and release checks

PDF viewers do not implement AcroForms identically. Browser viewers in
particular may display, save, print, or export values differently. Before
release, test the exact viewer and workflow the recipient will use:

1. Open the compiled PDF and confirm every field is visible.
2. Enter representative long values, accents, punctuation, and dates.
3. Save, close, reopen, and confirm values persist.
4. Print or export a copy and verify values remain visible.
5. Exercise any external signing, document-management, or ingestion system.
6. Re-run the repository's AcroForm validator on the original compiled legal
   template when its field structure changes.

Install the validator dependency into the Python environment used for the
repository, then run the exact stock-template check:

```sh
python3 -m pip install pypdf
python3 scripts/validate_legal_acroform.py build/legal/legal.pdf
```

On Windows Command Prompt or PowerShell, the equivalent Python-launcher
commands are:

```powershell
py -3 -m pip install pypdf
py -3 scripts/validate_legal_acroform.py build/legal/legal.pdf
```

The default check intentionally enforces the stock legal template's exact
field-name/type manifest in addition to the form-tree and appearance checks.
After deliberately changing, adding, or removing fields, either update
`EXPECTED_TYPES` in `scripts/validate_legal_acroform.py` as part of the reviewed
schema change, or run the generic structural check:

```sh
python3 scripts/validate_legal_acroform.py \
  --structure-only build/legal/legal.pdf
```

The structural check still requires one canonical field per widget, unique
names, supported field types, `/NeedAppearances` not true (effective false),
and a nonempty normal appearance for every widget. It also requires unique, nonempty choice
options and a blank initial choice value, preventing an invisible or malformed
preselection from passing QA. It does not enforce a project-specific field
manifest.

The template keeps `/NeedAppearances` effectively false (the catalog may omit
that optional key, whose PDF default is false) and supplies a nonempty normal
appearance for every blank widget so unfilled controls remain visible in
standards-compliant viewers. The validator rejects `/NeedAppearances true`.
A downstream editor is responsible for updating the appearance after a user
enters a value.

The `required` flag and built-in field formatting are enforced differently by
different viewers. They do not establish legal sufficiency, validate a date or
email address, verify a signer's identity, or replace downstream business-rule
validation. Treat them as interface hints and test the actual receiving
workflow.

Interactive forms and archival standards can conflict. If a filing requires
PDF/A, PDF/UA, flattened fields, or a particular signature profile, decide the
required final format with counsel or the receiving authority and use a
qualified downstream conversion and validation workflow.

Form data can itself be proprietary, export-controlled, CUI, personal, or
classified. Use only approved people, devices, repositories, viewers, signing
services, and distribution channels for the completed data.
