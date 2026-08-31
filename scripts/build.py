#!/usr/bin/env python3
"""Cross-platform builder for the Linear Space LaTeX templates."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import shlex
import subprocess
import sys


if sys.version_info < (3, 9):
    raise SystemExit("Python 3.9 or newer is required.")


ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = ROOT / "build"
SELECTION_FILE = ROOT / "template-selection.json"

PRIMARY_TARGET_NAMES = ("engineering", "legal", "memo", "presentation")


def load_selected_targets() -> tuple[str, ...]:
    """Return the retained template families, or all families before pruning."""
    if not SELECTION_FILE.is_file():
        return PRIMARY_TARGET_NAMES
    try:
        payload = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))
        selected = payload["selected_templates"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise RuntimeError(
            f"cannot read {SELECTION_FILE.name}; restore it or rerun "
            "select_templates.py from a clean clone"
        ) from error
    if (
        not isinstance(selected, list)
        or not selected
        or any(name not in PRIMARY_TARGET_NAMES for name in selected)
        or len(selected) != len(set(selected))
    ):
        raise RuntimeError(
            f"{SELECTION_FILE.name} must contain a nonempty, unique "
            f"selected_templates list drawn from {', '.join(PRIMARY_TARGET_NAMES)}"
        )
    return tuple(name for name in PRIMARY_TARGET_NAMES if name in selected)


SELECTED_TARGETS = load_selected_targets()

GENERATED_SUFFIXES = (
    ".acn",
    ".acr",
    ".alg",
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".dvi",
    ".fdb_latexmk",
    ".fls",
    ".glg",
    ".glo",
    ".gls",
    ".ist",
    ".loa",
    ".lof",
    ".log",
    ".lol",
    ".lot",
    ".nav",
    ".out",
    ".pdf",
    ".ps",
    ".run.xml",
    ".snm",
    ".synctex.gz",
    ".thm",
    ".toc",
    ".vrb",
    ".xdv",
    "-blx.bib",
)

ALL_TARGETS = {
    "engineering": ROOT / "templates" / "engineering" / "main.tex",
    "legal": ROOT / "templates" / "legal" / "main.tex",
    "memo": ROOT / "templates" / "memo" / "main.tex",
    "presentation": ROOT / "templates" / "presentation" / "main.tex",
}
TARGETS = {name: source for name, source in ALL_TARGETS.items() if name in SELECTED_TARGETS}

# These are intentionally excluded from the default `all` target.  They are
# synthetic visual previews, not authority to create, store, or handle actual
# controlled/classified information.
ALL_DEMO_TARGETS = {
    "synthetic-confidential": ROOT / "templates" / "marking-demos" / "synthetic-confidential-demo.tex",
    "synthetic-ear": ROOT / "templates" / "marking-demos" / "synthetic-ear-demo.tex",
    "synthetic-itar": ROOT / "templates" / "marking-demos" / "synthetic-itar-demo.tex",
    "synthetic-secret": ROOT / "templates" / "marking-demos" / "synthetic-secret-demo.tex",
    "synthetic-top-secret": ROOT / "templates" / "marking-demos" / "synthetic-top-secret-demo.tex",
}
DEMO_TARGETS = ALL_DEMO_TARGETS if "presentation" in SELECTED_TARGETS else {}

SMOKE_TARGETS = {
    "corporate-report": ROOT / "tests" / "corporate-smoke.tex",
    "corporate-presentation": ROOT / "tests" / "corporate-presentation-smoke.tex",
    "presentation-acronyms": ROOT / "tests" / "presentation-acronyms-smoke.tex",
}
_SMOKE_REQUIRED_TYPE = {
    "corporate-report": "engineering",
    "corporate-presentation": "presentation",
    "presentation-acronyms": "presentation",
}
SMOKE_TARGETS = {
    name: source
    for name, source in SMOKE_TARGETS.items()
    if _SMOKE_REQUIRED_TYPE[name] in SELECTED_TARGETS
}

DRAFT_VALIDATIONS = {
    "public-release-validation": ROOT / "tests" / "public-release-validation-draft.tex",
    "structured-distribution": ROOT / "tests" / "structured-distribution-draft.tex",
    "export-controls-validation": ROOT / "tests" / "export-controls-validation-draft.tex",
    "itar-controls-validation": ROOT / "tests" / "itar-controls-validation-draft.tex",
    "dod-export-controlled-validation": ROOT / "tests" / "dod-export-controlled-validation-draft.tex",
    "dod-export-not-applicable-validation": ROOT / "tests" / "dod-export-not-applicable-validation-draft.tex",
    "classified-dod-validation": ROOT / "tests" / "classified-dod-validation-draft.tex",
    "classified-presentation-validation": ROOT / "tests" / "classified-presentation-validation-draft.tex",
    "classified-export-statement-f-validation": ROOT / "tests" / "classified-export-statement-f-validation-draft.tex",
    "confidential-classified-validation": ROOT / "tests" / "confidential-classified-validation-draft.tex",
    "unclassified-profile-validation": ROOT / "tests" / "unclassified-profile-validation-draft.tex",
    "alternate-cui-only-banner-validation": ROOT / "tests" / "alternate-cui-only-banner-validation-draft.tex",
    "multi-owner-proprietary-validation": ROOT / "tests" / "multi-owner-proprietary-validation-draft.tex",
    "presentation-components": ROOT / "tests" / "presentation-components-draft.tex",
    "presentation-slide-markings": ROOT / "tests" / "presentation-slide-markings-draft.tex",
    "full-combination-report-layout": ROOT / "tests" / "full-combination-report-layout-draft.tex",
    "full-combination-legal-layout": ROOT / "tests" / "full-combination-legal-layout-draft.tex",
    "full-combination-memo-layout": ROOT / "tests" / "full-combination-memo-layout-draft.tex",
    "full-combination-presentation-layout": ROOT / "tests" / "full-combination-presentation-layout-draft.tex",
    **{f"{name}-demo-layout": source for name, source in DEMO_TARGETS.items()},
}
_DRAFT_REQUIRED_TYPE = {
    "classified-export-statement-f-validation": "engineering",
    "classified-presentation-validation": "presentation",
    "presentation-components": "presentation",
    "presentation-slide-markings": "presentation",
    "full-combination-report-layout": "engineering",
    "full-combination-legal-layout": "legal",
    "full-combination-memo-layout": "memo",
    "full-combination-presentation-layout": "presentation",
    "multi-owner-proprietary-validation": "engineering",
}
DRAFT_VALIDATIONS = {
    name: source
    for name, source in DRAFT_VALIDATIONS.items()
    if _DRAFT_REQUIRED_TYPE.get(name) in (None, *SELECTED_TARGETS)
}

EXPECTED_FAILURES = {
    "invalid-choice-initial-value": (
        ROOT / "tests" / "invalid-choice-initial-value-smoke.tex",
        "Choice-menu option 'default/value' is not supported",
    ),
    "invalid-title-overlay-opacity": (
        ROOT / "tests" / "invalid-title-overlay-opacity-smoke.tex",
        "Title background overlay '1.01' is outside the supported range",
    ),
    "invalid-slide-marking-framebreak": (
        ROOT / "tests" / "invalid-slide-marking-framebreak-smoke.tex",
        "LSSlideMarking cannot wrap a frame with allowframebreaks",
    ),
    "invalid-slide-marking-overlays": (
        ROOT / "tests" / "invalid-slide-marking-overlays-smoke.tex",
        "LSSlideMarking produced 2 physical slides",
    ),
    "invalid-milestone-count": (
        ROOT / "tests" / "invalid-milestone-count-smoke.tex",
        "An LSMilestoneSlide contains 11 milestones",
    ),
    "invalid-control": (
        ROOT / "tests" / "invalid-control-smoke.tex",
        "Unknown control token",
    ),
    "invalid-reserved-banner": (
        ROOT / "tests" / "invalid-reserved-banner-smoke.tex",
        "The uncontrolled profile requires",
    ),
    "invalid-raw-distribution": (
        ROOT / "tests" / "invalid-raw-distribution-smoke.tex",
        "Raw distribution-statement text is",
    ),
    "invalid-expanded-blank": (
        ROOT / "tests" / "invalid-expanded-blank-smoke.tex",
        "'distribution-office' is blank",
    ),
    "invalid-cui-banner-override": (
        ROOT / "tests" / "invalid-cui-banner-override-smoke.tex",
        "A CUI-bearing document must use",
    ),
    "invalid-raw-portion": (
        ROOT / "tests" / "invalid-raw-portion-smoke.tex",
        "Raw portion marks are disabled",
    ),
    "invalid-first-page-notices": (
        ROOT / "tests" / "invalid-first-page-notices-smoke.tex",
        "Required title-page notices",
    ),
    "invalid-banner-width": (
        ROOT / "tests" / "invalid-banner-width-smoke.tex",
        "The mandatory banner is wider than",
    ),
    "invalid-dod-commingled-banner": (
        ROOT / "tests" / "invalid-dod-commingled-banner-smoke.tex",
        "DoD classified banners must not",
    ),
    "invalid-preamble-page-override": (
        ROOT / "tests" / "invalid-preamble-page-override-smoke.tex",
        "A CUI-bearing document must use",
    ),
    "invalid-statement-a-authority": (
        ROOT / "tests" / "invalid-statement-a-authority-smoke.tex",
        "Distribution Statement A requires DoD authority confirmation",
    ),
    "invalid-dod-export-category": (
        ROOT / "tests" / "invalid-dod-export-category-smoke.tex",
        "distribution reasons must include Export Controlled",
    ),
    "invalid-export-jurisdiction": (
        ROOT / "tests" / "invalid-export-jurisdiction-smoke.tex",
        "Export jurisdiction does not match controls={ear}",
    ),
    "invalid-distribution-category-code": (
        ROOT / "tests" / "invalid-distribution-category-code-smoke.tex",
        "is not authorized for Distribution Statement C",
    ),
    "invalid-dod-cui-category": (
        ROOT / "tests" / "invalid-dod-cui-category-smoke.tex",
        "requires the CTI CUI category",
    ),
    "invalid-distribution-category-alias-duplicate": (
        ROOT / "tests" / "invalid-distribution-category-alias-duplicate-smoke.tex",
        "repeats a defense category",
    ),
    "invalid-critical-technology-without-export-reason": (
        ROOT / "tests" / "invalid-critical-technology-without-export-reason-smoke.tex",
        "distribution reasons must include Export Controlled",
    ),
    "invalid-stale-classification-attestation": (
        ROOT / "tests" / "invalid-stale-classification-attestation-smoke.tex",
        "Classified-environment confirmation does not apply",
    ),
    "invalid-confidential-banner": (
        ROOT / "tests" / "invalid-confidential-banner-smoke.tex",
        "The banner would remove CONFIDENTIAL",
    ),
    "invalid-confidential-cui-prefix": (
        ROOT / "tests" / "invalid-confidential-cui-prefix-smoke.tex",
        "The classified-general CONFIDENTIAL+CUI banner has the wrong prefix",
    ),
    "invalid-confidential-secret-portion": (
        ROOT / "tests" / "invalid-confidential-secret-portion-smoke.tex",
        "A SECRET portion mark requires SECRET or TOP SECRET output",
    ),
    "invalid-unclassified-confidential-portion": (
        ROOT / "tests" / "invalid-unclassified-confidential-portion-smoke.tex",
        "A CONFIDENTIAL portion mark requires CONFIDENTIAL, SECRET, or TOP SECRET output",
    ),
    "invalid-confidential-dod-commingled-banner": (
        ROOT / "tests" / "invalid-confidential-dod-commingled-banner-smoke.tex",
        "DoD classified banners must not contain CUI",
    ),
    "invalid-unclassified-banner": (
        ROOT / "tests" / "invalid-unclassified-banner-smoke.tex",
        "The unclassified profile requires the exact banner UNCLASSIFIED",
    ),
    "invalid-unclassified-classification": (
        ROOT / "tests" / "invalid-unclassified-classification-smoke.tex",
        "A classification level requires a classified profile",
    ),
    "invalid-unclassified-cui-control": (
        ROOT / "tests" / "invalid-unclassified-cui-control-smoke.tex",
        "CUI requires a CUI or classified profile",
    ),
    "invalid-cui-only-banner-no-control": (
        ROOT / "tests" / "invalid-cui-only-banner-no-control-smoke.tex",
        "A CUI-only slide banner requires controls={cui}",
    ),
    "invalid-cui-only-banner-case": (
        ROOT / "tests" / "invalid-cui-only-banner-case-smoke.tex",
        "Official banner text must use uppercase letters",
    ),
    "invalid-cui-only-banner-classification": (
        ROOT / "tests" / "invalid-cui-only-banner-classification-smoke.tex",
        "A CUI-only slide banner cannot contain a classification term",
    ),
    "invalid-multi-owner-blank-owner": (
        ROOT / "tests" / "invalid-multi-owner-blank-owner-smoke.tex",
        "Proprietary owner name is blank",
    ),
    "invalid-multi-owner-placeholder-owner": (
        ROOT / "tests" / "invalid-multi-owner-placeholder-owner-smoke.tex",
        "Required marking field 'proprietary-owner' contains a placeholder",
    ),
    "invalid-multi-owner-duplicate-owner": (
        ROOT / "tests" / "invalid-multi-owner-duplicate-owner-smoke.tex",
        "is declared more than once",
    ),
    "invalid-multi-owner-late-declaration": (
        ROOT / "tests" / "invalid-multi-owner-late-declaration-smoke.tex",
        "Proprietary-owner declarations are frozen",
    ),
    "invalid-multi-owner-too-few": (
        ROOT / "tests" / "invalid-multi-owner-too-few-smoke.tex",
        "Multi-owner proprietary mode requires at least two owners",
    ),
    "invalid-proprietary-owner-mode": (
        ROOT / "tests" / "invalid-proprietary-owner-mode-smoke.tex",
        "Proprietary-owner declarations require proprietary-mode=multi-owner",
    ),
    "invalid-proprietary-owner-control": (
        ROOT / "tests" / "invalid-proprietary-owner-control-smoke.tex",
        "Multi-owner proprietary mode requires controls={proprietary}",
    ),
    "invalid-multi-owner-corporate-banner": (
        ROOT / "tests" / "invalid-multi-owner-corporate-banner-smoke.tex",
        "The multi-owner corporate proprietary banner must be exact",
    ),
    "invalid-missing-dod-release-notice": (
        ROOT / "tests" / "invalid-missing-dod-release-notice-smoke.tex",
        "The required DoDD 5230.25 release notice was not rendered by page or slide 2",
    ),
    "invalid-missing-dod-export-determination": (
        ROOT / "tests" / "invalid-missing-dod-export-determination-smoke.tex",
        "requires an explicit export-controlled-technical-information determination",
    ),
    "invalid-dod-cti-without-distribution": (
        ROOT / "tests" / "invalid-dod-cti-without-distribution-smoke.tex",
        "The DoD unclassified CTI category requires a structured distribution statement",
    ),
    "invalid-unclassified-export-statement-f": (
        ROOT / "tests" / "invalid-unclassified-export-statement-f-smoke.tex",
        "Unclassified DoD export-controlled CTI requires Distribution Statement B, C, D, or E",
    ),
}
_EXPECTED_FAILURE_REQUIRED_TYPE = {
    "invalid-choice-initial-value": "legal",
    "invalid-title-overlay-opacity": "presentation",
    "invalid-slide-marking-framebreak": "presentation",
    "invalid-slide-marking-overlays": "presentation",
    "invalid-milestone-count": "presentation",
    "invalid-control": "memo",
}
EXPECTED_FAILURES = {
    name: test
    for name, test in EXPECTED_FAILURES.items()
    if _EXPECTED_FAILURE_REQUIRED_TYPE.get(name) in (None, *SELECTED_TARGETS)
}

COMMON_REQUIRED_FILES = (
    ROOT / "tex" / "linearspace-brand.sty",
    ROOT / "tex" / "linearspace-acronyms.sty",
    ROOT / "tex" / "linearspace-markings.sty",
    ROOT / "tex" / "linearspace-math.sty",
    ROOT / "assets" / "branding" / "linear-space-color.png",
    ROOT / "assets" / "branding" / "linear-space-dark-bg.png",
    ROOT / "assets" / "branding" / "linear-space-mark.svg",
    ROOT / "assets" / "branding" / "linear-space-solar-system.png",
)

TYPE_REQUIRED_FILES = {
    "engineering": (
        ROOT / "tex" / "linearspace-report.cls",
        ROOT / "templates" / "shared-data" / "estimation-error.csv",
        ROOT / "templates" / "shared-data" / "references.bib",
    ),
    "legal": (
        ROOT / "tex" / "linearspace-forms.sty",
        ROOT / "tex" / "linearspace-legal.cls",
        ROOT / "scripts" / "validate_legal_acroform.py",
    ),
    "memo": (ROOT / "tex" / "linearspace-memo.cls",),
    "presentation": (
        ROOT / "tex" / "beamerthemeLinearSpace.sty",
        ROOT / "templates" / "shared-data" / "estimation-error.csv",
        ROOT / "templates" / "shared-data" / "references.bib",
        ROOT / "assets" / "backgrounds" / "james-webb-cloudy-space-16x9.jpg",
        ROOT / "assets" / "backgrounds" / "milky-way-panorama.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "black-hole.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "explosive-galaxy.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "galaxy-explosion-render.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "james-webb-cloudy-space-original.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "jwst-jupiter-rings.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "milky-way-supplied.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "moon-from-earth.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "night-sky.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "phantom-galaxy.jpg",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "pillars-of-creation.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "tarantula-nebula-jwst.png",
        ROOT / "assets" / "backgrounds" / "user-supplied" / "red-blue-galactic-core.png",
    ),
}

REQUIRED_FILES = (
    *TARGETS.values(),
    *DEMO_TARGETS.values(),
    *SMOKE_TARGETS.values(),
    *DRAFT_VALIDATIONS.values(),
    *(source for source, _ in EXPECTED_FAILURES.values()),
    *COMMON_REQUIRED_FILES,
    *(path for name in SELECTED_TARGETS for path in TYPE_REQUIRED_FILES[name]),
)
REQUIRED_FILES = tuple(dict.fromkeys(REQUIRED_FILES))

REQUIRED_PACKAGES = (
    "amsthm.sty",
    "array.sty",
    "beamer.cls",
    "biblatex.sty",
    "booktabs.sty",
    "bookmark.sty",
    "cleveref.sty",
    "csquotes.sty",
    "enumitem.sty",
    "etoolbox.sty",
    "expl3.sty",
    "fontspec.sty",
    "geometry.sty",
    "graphicx.sty",
    "hyperref.sty",
    "iftex.sty",
    "lastpage.sty",
    "lineno.sty",
    "listings.sty",
    "longtable.sty",
    "mathtools.sty",
    "microtype.sty",
    "pgfplots.sty",
    "pdfrender.sty",
    "ragged2e.sty",
    "scrartcl.cls",
    "scrlayer-scrpage.sty",
    "scrreprt.cls",
    "setspace.sty",
    "siunitx.sty",
    "tabularx.sty",
    "tcolorbox.sty",
    "tikz.sty",
    "unicode-math.sty",
    "xcolor.sty",
    "xparse.sty",
    "xurl.sty",
    "texgyreheros-regular.otf",
    "texgyreheros-bold.otf",
    "texgyrepagella-regular.otf",
    "texgyrepagella-bold.otf",
    "texgyrepagella-math.otf",
)
_PACKAGE_REQUIRED_TYPE = {
    "beamer.cls": "presentation",
    "pdfrender.sty": "presentation",
    "scrreprt.cls": "engineering",
    "lineno.sty": "legal",
}
REQUIRED_PACKAGES = tuple(
    package
    for package in REQUIRED_PACKAGES
    if _PACKAGE_REQUIRED_TYPE.get(package) in (None, *SELECTED_TARGETS)
    and not (
        package == "scrartcl.cls"
        and not ({"legal", "memo"} & set(SELECTED_TARGETS))
    )
)


def command_path(name: str) -> str | None:
    return shutil.which(name)


def python_with_module(module: str) -> str:
    """Prefer this interpreter, then find a PATH Python with ``module``.

    Some stock macOS Python installations intentionally omit third-party
    packages even when a project-managed Python is later on PATH.  Probing
    every concrete PATH candidate keeps the test command portable without
    hard-coding a workstation-specific virtual environment.
    """
    names = ("python3.exe", "python.exe") if os.name == "nt" else ("python3", "python")
    candidates = [Path(sys.executable)]
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        for name in names:
            candidate = Path(entry) / name
            if candidate.is_file() and candidate not in candidates:
                candidates.append(candidate)
    for candidate in candidates:
        result = subprocess.run(
            [str(candidate), "-c", f"import {module}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return str(candidate)
    return sys.executable


def tex_environment() -> dict[str, str]:
    env = os.environ.copy()
    # A trailing empty component preserves TeX's normal search path.
    # The builder always runs subprocesses from ROOT.  Never add the caller's
    # working directory: doing so would allow an unrelated checkout to shadow
    # this repository's classes, assets, or bibliography files.
    tex_paths = [ROOT / "tex", ROOT / "templates", ROOT]
    bib_paths = [ROOT / "templates", ROOT]
    existing_tex = env.get("TEXINPUTS", "")
    existing_bib = env.get("BIBINPUTS", "")
    env["TEXINPUTS"] = os.pathsep.join(
        [*(str(path) for path in tex_paths), existing_tex, ""]
    )
    env["BIBINPUTS"] = os.pathsep.join(
        [*(str(path) for path in bib_paths), existing_bib, ""]
    )
    return env


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    display = subprocess.list2cmdline(command) if os.name == "nt" else shlex.join(command)
    print("+", display, flush=True)
    subprocess.run(command, cwd=cwd, env=tex_environment(), check=True)


def check_setup() -> bool:
    ok = True
    print("Retained templates")
    print("  " + ", ".join(SELECTED_TARGETS))
    print("Toolchain")
    for command in ("lualatex", "biber"):
        path = command_path(command)
        print(f"  {'OK' if path else 'MISSING':7} {command}" + (f" -> {path}" if path else ""))
        ok &= path is not None

    latexmk = command_path("latexmk")
    print(f"  {'OK' if latexmk else 'OPTIONAL':7} latexmk" + (f" -> {latexmk}" if latexmk else " (direct LuaLaTeX fallback will be used)"))

    print("Repository inputs")
    for path in REQUIRED_FILES:
        present = path.is_file()
        print(f"  {'OK' if present else 'MISSING':7} {path.relative_to(ROOT)}")
        ok &= present

    kpsewhich = command_path("kpsewhich")
    if not kpsewhich:
        print("  MISSING kpsewhich (cannot verify packages)")
        return False

    print("LaTeX packages")
    for package in REQUIRED_PACKAGES:
        result = subprocess.run(
            [kpsewhich, package],
            cwd=ROOT,
            env=tex_environment(),
            capture_output=True,
            text=True,
            check=False,
        )
        present = result.returncode == 0 and bool(result.stdout.strip())
        print(f"  {'OK' if present else 'MISSING':7} {package}")
        ok &= present

    if not ok:
        print("\nInstall the missing components before building. See README.md.")
    return ok


def compile_source(job_name: str, source: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf = output_dir / f"{job_name}.pdf"

    # Never leave a previously successful PDF looking current after a failed
    # compile.  LuaTeX can also create an incomplete PDF header before a fatal
    # pre-document validation error, so remove that partial artifact on error.
    if pdf.exists():
        pdf.unlink()

    try:
        latexmk = command_path("latexmk")
        if latexmk:
            run(
                [
                    latexmk,
                    "-lualatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-file-line-error",
                    "-recorder",
                    f"-outdir={output_dir}",
                    f"-jobname={job_name}",
                    str(source),
                ]
            )
        else:
            lualatex = command_path("lualatex")
            if not lualatex:
                raise RuntimeError("lualatex was not found; run with --check for details")
            latex_command = [
                lualatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                f"-output-directory={output_dir}",
                f"-jobname={job_name}",
                str(source),
            ]
            run(latex_command)
            bcf = output_dir / f"{job_name}.bcf"
            if bcf.exists():
                biber = command_path("biber")
                if not biber:
                    raise RuntimeError("biber is required by this document but was not found")
                run(
                    [
                        biber,
                        "--input-directory",
                        str(output_dir),
                        "--output-directory",
                        str(output_dir),
                        job_name,
                    ]
                )
            run(latex_command)
            run(latex_command)
    except (OSError, RuntimeError, subprocess.CalledProcessError):
        if pdf.exists():
            pdf.unlink()
        raise

    if not pdf.exists():
        raise RuntimeError(f"build completed without producing {pdf}")
    print(f"Built {pdf.relative_to(ROOT)}")
    return pdf


def build_target(name: str) -> Path:
    output_dir = BUILD_ROOT / name
    pdf = compile_source(name, TARGETS[name], output_dir)
    try:
        assert_clean_log(output_dir / f"{name}.log")
    except RuntimeError:
        if pdf.exists():
            pdf.unlink()
        raise
    return pdf


def build_demo_target(name: str) -> Path:
    output_dir = BUILD_ROOT / "marking-demos"
    pdf = compile_source(name, DEMO_TARGETS[name], output_dir)
    try:
        assert_clean_log(output_dir / f"{name}.log")
    except RuntimeError:
        if pdf.exists():
            pdf.unlink()
        raise
    return pdf


def assert_clean_log(log_path: Path) -> None:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    patterns = (
        r"Overfull \\hbox",
        r"Overfull \\vbox",
        r"LaTeX Warning: There were undefined references",
        r"Citation .+ undefined",
        r"Reference .+ undefined",
        r"destination with the same identifier",
        r"multiply defined",
        r"Missing character: There is no",
        r"Token not allowed in a PDF string",
        r"Please \(re\)run Biber",
        r"Rerun to get cross-references right",
        r"Label\(s\) may have changed",
    )
    issues = [line for line in text.splitlines() if any(re.search(pattern, line) for pattern in patterns)]
    if issues:
        excerpt = "\n".join(issues[:12])
        raise RuntimeError(f"quality gate failed for {log_path.relative_to(ROOT)}:\n{excerpt}")


def run_smoke_tests() -> None:
    tests_root = BUILD_ROOT / "tests"
    for job_name, source in SMOKE_TARGETS.items():
        output_dir = tests_root / job_name
        compile_source(job_name, source, output_dir)
        assert_clean_log(output_dir / f"{job_name}.log")

    if "legal" in TARGETS:
        legal_pdf = build_target("legal")
        run(
            [
                python_with_module("pypdf"),
                str(ROOT / "scripts" / "validate_legal_acroform.py"),
                str(legal_pdf),
            ]
        )

    lualatex = command_path("lualatex")
    if not lualatex:
        raise RuntimeError("lualatex is required for the expected-failure smoke test")

    for job_name, source in DRAFT_VALIDATIONS.items():
        output_dir = tests_root / job_name
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf = output_dir / f"{job_name}.pdf"
        if pdf.exists():
            pdf.unlink()
        command = [
            lualatex,
            "-draftmode",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={output_dir}",
            f"-jobname={job_name}",
            str(source),
        ]
        try:
            # Two passes make page-count/LastPage assertions deterministic
            # from a clean build while remaining PDF-free in draft mode.
            run(command)
            run(command)
            if pdf.exists() and pdf.stat().st_size:
                raise RuntimeError(
                    f"draft validation '{job_name}' unexpectedly produced a PDF"
                )
            assert_clean_log(output_dir / f"{job_name}.log")
            print(f"Passed validation-only draft '{job_name}'; no PDF retained.")
        finally:
            # A failed draft-mode TeX run can leave an empty PDF behind. Never
            # retain synthetic controlled/classified validation artifacts.
            if pdf.exists():
                pdf.unlink()

    for job_name, (source, expected_message) in EXPECTED_FAILURES.items():
        output_dir = tests_root / job_name
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf = output_dir / f"{job_name}.pdf"
        if pdf.exists():
            pdf.unlink()
        command = [
            lualatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={output_dir}",
            f"-jobname={job_name}",
            str(source),
        ]
        display = subprocess.list2cmdline(command) if os.name == "nt" else shlex.join(command)
        print("+", display, "(expected to fail)", flush=True)
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=tex_environment(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log_path = output_dir / f"{job_name}.log"
        log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
        # TeX inserts the package label again when it wraps a long diagnostic.
        # Remove that presentation-only prefix before matching the stable text.
        normalized_log = re.sub(
            r"(?m)^\((?:linearspace-markings|linearspace-forms|beamerthemeLinearSpace)\)\s*",
            "",
            log_text,
        )
        compact_log = re.sub(r"\s+", "", normalized_log)
        compact_expected = re.sub(r"\s+", "", expected_message)
        if pdf.exists():
            pdf.unlink()
        if result.returncode == 0:
            raise RuntimeError(f"{job_name} smoke test unexpectedly compiled")
        if compact_expected not in compact_log:
            raise RuntimeError(f"{job_name} smoke test failed for an unexpected reason")
        if "Output written on" in log_text:
            raise RuntimeError(f"{job_name} shipped one or more pages before failing")
        print(f"Passed expected-failure test '{job_name}'; no PDF retained.")
    print("All smoke tests passed.")


def open_file(path: Path) -> None:
    if sys.platform == "darwin":
        command = ["open", str(path)]
    elif os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
        return
    else:
        command = ["xdg-open", str(path)]
    subprocess.Popen(command, cwd=ROOT)


def clean_generated_outputs() -> None:
    removed_direct_artifacts = 0
    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)
        print(f"Removed {BUILD_ROOT.relative_to(ROOT)}")

    sources = [
        *TARGETS.values(),
        *DEMO_TARGETS.values(),
        *SMOKE_TARGETS.values(),
        *DRAFT_VALIDATIONS.values(),
        *(source for source, _ in EXPECTED_FAILURES.values()),
    ]
    stems = {
        *(path.stem for path in sources),
        *TARGETS.keys(),
        *DEMO_TARGETS.keys(),
        *SMOKE_TARGETS.keys(),
        *DRAFT_VALIDATIONS.keys(),
        *EXPECTED_FAILURES.keys(),
    }
    directories = {ROOT, *(path.parent for path in sources)}

    # Direct editor/LuaLaTeX runs can place known build products beside a
    # template or at the repository root. Limit deletion to known job stems so
    # --clean never removes an unrelated PDF or user-authored file.
    for directory in directories:
        for stem in stems:
            for suffix in GENERATED_SUFFIXES:
                artifact = directory / f"{stem}{suffix}"
                if artifact.is_file():
                    artifact.unlink()
                    removed_direct_artifacts += 1

    if removed_direct_artifacts:
        print(f"Removed {removed_direct_artifacts} direct-compilation artifacts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        choices=["all", "marking-demos", *ALL_TARGETS, *ALL_DEMO_TARGETS],
        default="all",
        help="template to build (default: all)",
    )
    parser.add_argument("--check", action="store_true", help="verify the local toolchain and exit")
    parser.add_argument("--test", action="store_true", help="run positive and expected-failure smoke tests")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove repository and direct-compilation outputs, then exit",
    )
    parser.add_argument("--open", action="store_true", help="open the generated PDF after a single-target build")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.open and args.target in ("all", "marking-demos"):
        raise RuntimeError("--open requires a single target")
    if args.check and (args.clean or args.test or args.open or args.target != "all"):
        raise RuntimeError("--check cannot be combined with a target, --clean, --test, or --open")
    if args.clean and (args.test or args.open or args.target != "all"):
        raise RuntimeError("--clean cannot be combined with a target, --test, or --open")
    if args.test and (args.open or args.target != "all"):
        raise RuntimeError("--test cannot be combined with a target or --open")

    if args.clean:
        clean_generated_outputs()
        return 0

    if args.check:
        return 0 if check_setup() else 1

    if args.test:
        run_smoke_tests()
        return 0

    if args.target == "all":
        outputs = [build_target(name) for name in TARGETS]
    elif args.target == "marking-demos":
        if not DEMO_TARGETS:
            raise RuntimeError(
                "marking demos were removed with the presentation template; "
                "restore them from Git or a fresh clone before building them"
            )
        outputs = [build_demo_target(name) for name in DEMO_TARGETS]
    elif args.target in TARGETS:
        outputs = [build_target(args.target)]
    elif args.target in DEMO_TARGETS:
        outputs = [build_demo_target(args.target)]
    else:
        raise RuntimeError(
            f"template target '{args.target}' was not retained; selected targets are "
            f"{', '.join(SELECTED_TARGETS)}"
        )
    if args.open:
        open_file(outputs[0])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
