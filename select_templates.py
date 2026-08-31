#!/usr/bin/env python3
"""Keep selected template families and remove the unselected families safely.

Run this once after cloning the template repository.  The script keeps shared
branding, mathematics, markings, build wrappers, and documentation used by the
retained templates.  Deleted tracked files remain recoverable with Git.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


if sys.version_info < (3, 9):
    raise SystemExit("Python 3.9 or newer is required.")


ROOT = Path(__file__).resolve().parent
SELECTION_FILE = ROOT / "template-selection.json"
TEMPLATE_ORDER = ("engineering", "legal", "memo", "presentation")
TEMPLATE_DESCRIPTIONS = {
    "engineering": "Engineering reports, analyses, documentation, and manuals",
    "legal": "Legal agreements and fillable AcroForm documents",
    "memo": "Professional decision and technical memoranda",
    "presentation": "Dark 16:9 Beamer presentations and synthetic marking demos",
}

# Every path is literal and repository-relative.  Shared packages and assets
# are deliberately absent from this map.
TYPE_PATHS = {
    "engineering": (
        "templates/engineering",
        "tex/linearspace-report.cls",
        "tests/corporate-smoke.tex",
        "tests/classified-export-statement-f-validation-draft.tex",
        "tests/full-combination-report-layout-draft.tex",
        "tests/multi-owner-proprietary-validation-draft.tex",
        "build/engineering",
        "build/tests/corporate-report",
        "build/tests/classified-export-statement-f-validation",
        "build/tests/full-combination-report-layout",
        "build/tests/multi-owner-proprietary-validation",
    ),
    "legal": (
        "templates/legal",
        "tex/linearspace-legal.cls",
        "tex/linearspace-forms.sty",
        "scripts/validate_legal_acroform.py",
        "tests/full-combination-legal-layout-draft.tex",
        "tests/invalid-choice-initial-value-smoke.tex",
        "build/legal",
        "build/tests/full-combination-legal-layout",
        "build/tests/invalid-choice-initial-value",
    ),
    "memo": (
        "templates/memo",
        "tex/linearspace-memo.cls",
        "tests/full-combination-memo-layout-draft.tex",
        "tests/invalid-control-smoke.tex",
        "build/memo",
        "build/tests/full-combination-memo-layout",
        "build/tests/invalid-control",
    ),
    "presentation": (
        "templates/presentation",
        "templates/marking-demos",
        "tex/beamerthemeLinearSpace.sty",
        "assets/backgrounds",
        "tests/classified-presentation-validation-draft.tex",
        "tests/corporate-presentation-smoke.tex",
        "tests/full-combination-presentation-layout-draft.tex",
        "tests/invalid-milestone-count-smoke.tex",
        "tests/invalid-slide-marking-framebreak-smoke.tex",
        "tests/invalid-slide-marking-overlays-smoke.tex",
        "tests/invalid-title-overlay-opacity-smoke.tex",
        "tests/presentation-acronyms-smoke.tex",
        "tests/presentation-components-draft.tex",
        "tests/presentation-slide-markings-draft.tex",
        "build/presentation",
        "build/marking-demos",
        "build/tests/classified-presentation-validation",
        "build/tests/corporate-presentation",
        "build/tests/full-combination-presentation-layout",
        "build/tests/invalid-milestone-count",
        "build/tests/invalid-slide-marking-framebreak",
        "build/tests/invalid-slide-marking-overlays",
        "build/tests/invalid-title-overlay-opacity",
        "build/tests/presentation-acronyms",
        "build/tests/presentation-components",
        "build/tests/presentation-slide-markings",
    ),
}

SHARED_DATA_PATHS = ("templates/shared-data",)
SHARED_DATA_USERS = frozenset(("engineering", "presentation"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keep",
        metavar="LIST",
        help=(
            "comma- or space-separated names/numbers to retain; for example "
            "--keep engineering,presentation or --keep 1,4"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show the deletion plan without changing the repository",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="apply the displayed plan without the interactive DELETE prompt",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="allow deletion of paths with uncommitted changes or use outside Git",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list selectable template families and exit",
    )
    return parser.parse_args()


def show_choices() -> None:
    print("Available template families:")
    for index, name in enumerate(TEMPLATE_ORDER, start=1):
        print(f"  {index}. {name:12} {TEMPLATE_DESCRIPTIONS[name]}")


def normalize_selection(raw: str) -> tuple[str, ...]:
    tokens = [token.lower() for token in re.split(r"[\s,]+", raw.strip()) if token]
    if not tokens:
        raise ValueError("select at least one template family")
    if tokens == ["all"]:
        return TEMPLATE_ORDER
    aliases = {str(index): name for index, name in enumerate(TEMPLATE_ORDER, start=1)}
    aliases.update({name: name for name in TEMPLATE_ORDER})
    unknown = [token for token in tokens if token not in aliases]
    if unknown:
        raise ValueError(
            "unknown selection "
            + ", ".join(repr(token) for token in unknown)
            + "; use names, numbers 1-4, or all"
        )
    selected_names = {aliases[token] for token in tokens}
    return tuple(name for name in TEMPLATE_ORDER if name in selected_names)


def current_selection() -> tuple[str, ...]:
    if not SELECTION_FILE.is_file():
        return TEMPLATE_ORDER
    try:
        payload = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))
        return normalize_selection(" ".join(payload["selected_templates"]))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"cannot read {SELECTION_FILE.name}; restore it from Git or use a fresh clone"
        ) from error


def deletion_plan(selected: tuple[str, ...]) -> tuple[Path, ...]:
    selected_set = set(selected)
    relative_paths: list[str] = []
    for name in TEMPLATE_ORDER:
        if name not in selected_set:
            relative_paths.extend(TYPE_PATHS[name])
    if not (selected_set & SHARED_DATA_USERS):
        relative_paths.extend(SHARED_DATA_PATHS)

    planned: list[Path] = []
    seen: set[Path] = set()
    for relative in relative_paths:
        candidate = ROOT / relative
        if candidate in seen or not (candidate.exists() or candidate.is_symlink()):
            continue
        seen.add(candidate)
        planned.append(candidate)
    return tuple(planned)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def verify_repository() -> bool:
    sentinels = (
        ROOT / "scripts" / "build.py",
        ROOT / "tex" / "linearspace-markings.sty",
        ROOT / "README.md",
    )
    if not all(path.is_file() for path in sentinels):
        raise RuntimeError(
            "this script is not in the root of a complete latex_doc_templates clone"
        )
    git = shutil.which("git")
    if not git:
        return False
    result = subprocess.run(
        [git, "rev-parse", "--show-toplevel"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False
    return Path(result.stdout.strip()).resolve() == ROOT


def modified_planned_paths(plan: tuple[Path, ...]) -> tuple[str, ...]:
    if not plan:
        return ()
    git = shutil.which("git")
    if not git:
        return ()
    result = subprocess.run(
        [
            git,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            *(relative(path) for path in plan),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Git could not inspect the paths scheduled for deletion")
    return tuple(line for line in result.stdout.splitlines() if line.strip())


def assert_safe_target(path: Path) -> None:
    try:
        path.relative_to(ROOT)
    except ValueError as error:
        raise RuntimeError(f"refusing to delete a path outside the repository: {path}") from error
    if path == ROOT:
        raise RuntimeError("refusing to delete the repository root")
    if path.is_symlink():
        return
    resolved = path.resolve(strict=False)
    if ROOT not in resolved.parents:
        raise RuntimeError(f"refusing to delete a path outside the repository: {path}")


def remove_path(path: Path) -> None:
    assert_safe_target(path)
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def write_selection(selected: tuple[str, ...]) -> None:
    payload = {
        "schema_version": 1,
        "selected_templates": list(selected),
    }
    temporary = ROOT / ".template-selection.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, SELECTION_FILE)


def main() -> int:
    args = parse_args()
    if args.list:
        show_choices()
        return 0

    in_git_repository = verify_repository()
    retained_before = current_selection()

    if args.keep is None:
        show_choices()
        print()
        raw = input(
            "Keep which templates? Enter names or numbers separated by commas "
            "(example: 1,4): "
        )
    else:
        raw = args.keep
    try:
        selected = normalize_selection(raw)
    except ValueError as error:
        raise RuntimeError(str(error)) from error

    unavailable = set(selected) - set(retained_before)
    if unavailable:
        raise RuntimeError(
            "cannot restore previously removed template families: "
            + ", ".join(name for name in TEMPLATE_ORDER if name in unavailable)
            + "; restore them with Git or start from a fresh clone"
        )

    plan = deletion_plan(selected)
    print()
    print("Retaining: " + ", ".join(selected))
    print("Removing: " + ", ".join(name for name in TEMPLATE_ORDER if name not in selected))
    print()
    if plan:
        print(f"Deletion plan ({len(plan)} existing paths):")
        for path in plan:
            print(f"  - {relative(path)}")
    else:
        print("Deletion plan: no remaining files need removal.")

    if args.dry_run:
        print("\nDry run only; no files were changed.")
        return 0

    if not in_git_repository and not args.force:
        raise RuntimeError(
            "Git recovery is unavailable or this is not the repository root; "
            "rerun with --force only if permanent deletion is intentional"
        )

    modified = modified_planned_paths(plan) if in_git_repository else ()
    if modified and not args.force:
        print("\nUncommitted changes exist under paths scheduled for deletion:")
        for line in modified:
            print("  " + line)
        raise RuntimeError(
            "commit/stash those changes, or rerun with --force to delete them intentionally"
        )

    if not args.yes:
        print(
            "\nThis permanently removes the listed working-tree paths. "
            "Tracked files can be recovered with Git."
        )
        confirmation = input("Type DELETE to continue: ")
        if confirmation != "DELETE":
            print("Cancelled; no files were changed.")
            return 0

    for path in plan:
        remove_path(path)
    write_selection(selected)

    print(f"\nConfiguration complete. Removed {len(plan)} paths.")
    print(f"Recorded retained templates in {SELECTION_FILE.name}.")
    print("Build all retained templates with the normal 'all' target.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EOFError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
