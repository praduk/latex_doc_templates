# Linear Space LaTeX document templates

A clone-ready system for professional engineering documents, legal drafts,
decision memos, and dark 16:9 Beamer presentations. The document classes use
US letter paper, LuaLaTeX, modern OpenType fonts, disciplined page furniture,
and a shared metadata and marking layer. The presentation theme takes its
palette and visual rhythm from the supplied pre-seed fundraising deck without
copying that deck's content.

The repository is intentionally safe by default: the four primary templates
build as uncontrolled. Five optional marking previews deliberately exercise
corporate, export, and classification renderers using conspicuous synthetic
labels, fictional metadata, and harmless placeholder text. They contain no
controlled or classified information and are not handling or classification
authority. Controlled and classified profiles fail at compile time when
required authority fields are missing. That validation catches omissions; it
does **not** make a workstation, Git repository, PDF, person, or distribution
channel authorized.

## Choose a starting point

The commands below use the macOS/Linux wrapper. Use `scripts\build.cmd` on
Windows Command Prompt or `.\scripts\build.ps1` in PowerShell with the same
target argument.

| Target | Intended use | Source | Command | Output |
|---|---|---|---|---|
| Engineering | Analysis, design descriptions, interface documents, verification reports, manuals | `templates/engineering/main.tex` | `./scripts/build.sh engineering` | `build/engineering/engineering.pdf` |
| Legal | Counsel-reviewed agreements, formal instruments, exhibits | `templates/legal/main.tex` | `./scripts/build.sh legal` | `build/legal/legal.pdf` |
| Memo | Decisions, recommendations, approvals, short technical records | `templates/memo/main.tex` | `./scripts/build.sh memo` | `build/memo/memo.pdf` |
| Presentation | Investor, customer, program, and technical presentations | `templates/presentation/main.tex` | `./scripts/build.sh presentation` | `build/presentation/presentation.pdf` |

All three written templates are US letter. The Beamer template is 16:9.

### Synthetic marking previews

These five decks exist only to preview formatting. Their synthetic watermark,
fictional authority data, and no-controlled-or-classified-information notices
must remain visible. Never replace their placeholder text with real controlled
or classified content on an unapproved system.

| Preview | Command | Output |
|---|---|---|
| National-security Confidential (synthetic preview) | `./scripts/build.sh synthetic-confidential` | `build/marking-demos/synthetic-confidential.pdf` |
| EAR | `./scripts/build.sh synthetic-ear` | `build/marking-demos/synthetic-ear.pdf` |
| ITAR | `./scripts/build.sh synthetic-itar` | `build/marking-demos/synthetic-itar.pdf` |
| Secret | `./scripts/build.sh synthetic-secret` | `build/marking-demos/synthetic-secret.pdf` |
| Top Secret | `./scripts/build.sh synthetic-top-secret` | `build/marking-demos/synthetic-top-secret.pdf` |

`./scripts/build.sh all` builds only the four primary templates.
`./scripts/build.sh marking-demos` builds all five synthetic previews. This
separation prevents marked demonstrations from being mistaken for ordinary
project deliverables.

## Quick start

Requirements:

- Python 3.9 or newer;
- a current TeX distribution with LuaLaTeX and Biber; and
- `latexmk` (recommended; the build script has a direct LuaLaTeX fallback).

On macOS or Linux, check the installation, run the regression suite, then build
and open one example:

```sh
./scripts/build.sh --check
./scripts/build.sh --test
./scripts/build.sh engineering --open
```

On Windows Command Prompt:

```bat
scripts\build.cmd --check
scripts\build.cmd --test
scripts\build.cmd engineering --open
```

On PowerShell:

```powershell
.\scripts\build.ps1 --check
.\scripts\build.ps1 --test
.\scripts\build.ps1 engineering --open
```

Replace `engineering` with `legal`, `memo`, or `presentation`, or use `all` to
build the four primary examples. Use `marking-demos` only when you intentionally
want all five synthetic marking previews.

`make engineering`, `make legal`, `make memo`, `make presentation`, `make
marking-demos`, `make check`, `make test`, and `make clean` are available where
Make is installed. The Python entry point is the portable interface and should
be preferred in editor tasks and automation.

## Documentation

- [Public LaTeX API](docs/API.md): exact user-facing commands, arguments,
  defaults, and examples.
- [Customization guide](docs/CUSTOMIZATION.md): project-level design and
  content changes.
- [Presentation playbook](docs/PRESENTATION_PLAYBOOK.md): high-value narrative,
  screen, background, team, milestone, and visual-QA guidance.
- [Fillable forms and signatures](docs/FORMS.md): AcroForm fields, viewer tests,
  and signing workflows.
- [Markings and handling controls](docs/MARKINGS.md): proprietary, EAR/ITAR,
  CUI, classification, portion-marking, and distribution rules.
- [Asset provenance](assets/ASSET_PROVENANCE.md): source, credit, reuse, and
  owner-approval records for bundled assets.

## Install the toolchain

### macOS

Install [MacTeX](https://www.tug.org/mactex/) or BasicTeX plus the packages
reported by `scripts/build.py --check`. MacTeX already includes the required
engines and common packages. Open a new terminal after installation so the TeX
binaries are on `PATH`.

### Windows

Install [MiKTeX](https://miktex.org/download) or
[TeX Live](https://www.tug.org/texlive/), enable automatic package installation
if using MiKTeX, and install [Python](https://www.python.org/downloads/windows/).
The `build.cmd` and PowerShell wrappers locate the Windows Python launcher when
available. Restart the shell after installation.

### Linux

Install TeX Live, Biber, Latexmk, and Python through the distribution package
manager or the upstream [TeX Live installer](https://www.tug.org/texlive/).
For Debian/Ubuntu, the simplest complete installation is:

```sh
sudo apt install texlive-full biber latexmk python3
```

That package is large. A smaller installation is reasonable, but it must
contain every file listed by `./scripts/build.sh --check`.

## Create a new project from this repository

Clone to a document-specific directory and immediately update the remote so a
project document cannot accidentally push back to the template repository:

```sh
git clone git@github.com:praduk/latex_doc_templates.git my-project-document
cd my-project-document
git remote rename origin template
git remote add origin <new-project-repository-url>
```

Then:

1. Keep the repository structure intact and choose the target you need with the
   platform build wrapper. The shared setup check verifies required template,
   test, and asset inputs across the repository.
2. Replace the sample metadata and content in the selected `main.tex`.
3. Replace synthetic CSV and bibliography data under `templates/shared-data/`.
4. Build, inspect the rendered PDF page by page, and record the review.
5. Add an approved license before publishing the repository outside Linear
   Space. No rights are granted here for the supplied corporate marks.

Paths are resolved from the repository root, so builds work the same way from
an editor, terminal, or CI runner.

### Keep only the template families you need

After cloning, run the root-level selector to retain any combination of the
four primary template families and remove the others:

```sh
python3 select_templates.py
```

On Windows, use:

```bat
py -3 select_templates.py
```

The interactive selector previews every path it will delete and requires the
exact confirmation word `DELETE`. It refuses to delete uncommitted changes
under those paths unless `--force` is supplied. Use a dry run or automate a
known selection with:

```sh
python3 select_templates.py --keep engineering,presentation --dry-run
python3 select_templates.py --keep engineering,presentation --yes
```

The command writes `template-selection.json`. The normal `all`, `--check`,
`--test`, and `--clean` build operations then use only the retained families;
shared branding, mathematics, markings, assets, and tests remain wherever a
selected family still needs them. Selection is intentionally one-way because
files are physically removed. Recover a removed family with Git or start from
a fresh clone. Use `--force` only when deleting modified files is deliberate.

Each template also includes a local `latexmk` configuration for direct editor
compilation. Running `latexmk main.tex` inside a template directory writes
`main.pdf` and auxiliary files beside that source. Configure editor build tasks
to run from the repository root and call the platform wrapper with `<target>`
when you want the clean, isolated `build/<target>/<target>.pdf` layout used by
this repository.

## Common metadata

Every target uses the same block:

```tex
\LSSetup{
  title={Document title},
  subtitle={Optional subtitle},
  short-title={Short running title},
  author={Name or team},
  organization={Linear Space},
  document-id={LS-SYS-0123},
  revision={B},
  status={Released},
  date={2026-08-30},
  project={Program name},
  client={Customer name}
}
```

Use an explicit release date for controlled baselines. `\today` is convenient
for drafts but makes otherwise identical rebuilds change.

## Mathematics, units, diagrams, and plots

Every target loads the shared math package. It includes:

- `mathtools`, theorem environments, and Unicode mathematics;
- `siunitx` for quantities and uncertainty;
- TikZ with engineering-oriented libraries; and
- PGFPlots with light and dark Linear Space plot styles.

Representative helpers include `\vect{x}`, `\mat{A}`, `\transpose`,
`\norm{x}`, `\expect{x}`, `\prob{A}`, `\odv{y}{t}`, `\pdv{f}{x}`, and
`\skewmat{\omega}`. Use `\qty{3.2}{\milli\radian}` rather than manually
spacing numbers and units. The engineering and presentation examples show a
CSV-backed plot and traceable synthetic-data disclaimer.

## Markings and handling controls

Read [docs/MARKINGS.md](docs/MARKINGS.md) before changing the default
`uncontrolled` profile. The marking system keeps these concepts separate:

- proprietary information belonging to Linear Space, a partner, or multiple
  owners;
- EAR or ITAR export jurisdiction;
- CUI banners and designation information;
- Confidential, Secret, or Top Secret national-security classification; and
- DoD distribution statements and other handling notices.

They are not interchangeable and are not automatically concatenated into an
official banner. The authority supplies the banner and selects the prescribed
distribution code, categories, date, and office; the package owns the fixed
A--F sentence text. The contract, security classification guide, controlling
office, or authorized reviewer remains authoritative.

Never put classified material in this ordinary repository. Do not put CUI or
export-controlled technical data here unless the people, device, repository,
backup path, build tools, and distribution channel are all explicitly approved
for that information.

## Presentation design

The dark Beamer theme includes cover, image-divider, statement, two-column,
equation, chart, tradeoff, metric, milestone, team, acronym, reference, and
closing examples. The stock cover uses the exact owner-supplied red-and-blue
galactic-core image with a fully transparent (`0`) full-canvas overlay; title
darkening is optional and uniform. Backgrounds are cover-cropped rather than stretched. Keep
each slide to one claim and keep the image-credit slide synchronized with the
imagery actually used. See the [presentation playbook](docs/PRESENTATION_PLAYBOOK.md),
[customization guide](docs/CUSTOMIZATION.md), and
[asset provenance record](assets/ASSET_PROVENANCE.md).

## Repository map

```text
assets/                 Branding, documented defaults, and owner-supplied imagery
docs/                   API, forms, markings, presentation, and customization guidance
scripts/                Cross-platform build entry points
select_templates.py     Interactive, guarded template-family pruning tool
templates/              Four primary examples, five synthetic previews, and shared data
tex/                    Shared classes, theme, brand, math, and marking packages
build/                  Generated PDFs and intermediate files (ignored by Git)
```

## Release checklist

Before distributing a PDF:

1. Replace every bracketed placeholder and synthetic datum in a production
   deliverable. Resolve every legal drafting field; do not distribute a
   partially completed agreement as execution-ready.
2. Confirm title, identifier, revision, date, status, authorship, and PDF
   metadata.
3. Confirm all figures, equations, requirement label keys and rendered numbers,
   acronyms, references, citations, and links.
4. Run the platform wrapper with `--test`, then build from a clean checkout
   with `all` or the specific primary target. Build `marking-demos` separately
   only when those previews are intentionally part of the review.
5. Inspect every rendered page or slide at full size; compilation alone is not
   visual QA.
6. For a fillable legal PDF, verify every AcroForm widget and blank appearance,
   enter representative values, save and reopen the file, and confirm entered
   values remain visible when printed or exported. Follow
   [docs/FORMS.md](docs/FORMS.md) for signature and viewer checks.
7. Obtain counsel review for legal language and authorized security/export
   review for controlled markings. A successful build is not an authority
   determination.
8. If distributing a synthetic marking preview, confirm every slide still says
   that it is a demonstration containing no controlled or classified
   information. Never repurpose a preview as a production marked document.
9. Confirm image, font, and third-party content rights, retain visible credits
   where the source, license, or publication policy requires them, and preserve
   the project-specific provenance record.
10. If a filing or customer requires PDF/A, PDF/UA, electronic signatures, or
   another archival/accessibility standard, use a qualified downstream
   workflow. These templates produce professional PDFs but do not claim those
   certifications.

## Design decisions

- LuaLaTeX is mandatory so the same OpenType font stack works across operating
  systems.
- TeX Gyre Pagella, TeX Gyre Heros, and TeX Gyre Pagella Math are redistributable
  TeX fonts and avoid proprietary workstation dependencies.
- The presentation standardizes on TeX Gyre Heros on every platform; the
  reference PowerPoint's embedded Urbanist font was not extracted.
- Shell escape is not required.
- Two sample backgrounds have independently documented sources and reuse
  terms. Additional owner-supplied backgrounds are available for project use,
  but each selected asset still needs project-specific rights, credit, and
  provenance review before external publication.

This is a production-quality starting system, not a substitute for engineering
review, legal advice, export authorization, classification authority, or an
approved information system.
