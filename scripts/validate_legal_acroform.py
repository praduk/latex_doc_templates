#!/usr/bin/env python3
"""Validate the legal template's canonical AcroForm and widget appearances."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys
from typing import Any

try:
    from pypdf import PdfReader
    from pypdf.generic import DictionaryObject, IndirectObject
except ImportError as exc:  # pragma: no cover - exercised only without QA deps
    raise SystemExit(
        "pypdf is required for AcroForm QA. Install it with "
        "'python -m pip install pypdf'."
    ) from exc


CHOICE_FIELDS = {
    "agreement_party_a_entity_type",
    "agreement_party_b_entity_type",
    "agreement_party_a_signature_signing_method",
    "agreement_party_b_signature_signing_method",
}

CHECKBOX_FIELDS = {"agreement_preparation_review_complete"}

TEXT_FIELDS = {
    "agreement_party_a_legal_name",
    "agreement_party_a_formation_jurisdiction",
    "agreement_party_b_legal_name",
    "agreement_party_b_formation_jurisdiction",
    "agreement_effective_date",
    "agreement_purpose",
    "agreement_confidential_information_definition",
    "agreement_authorized_representatives",
    "agreement_standard_of_care",
    "agreement_incident_reporting",
    "agreement_required_disclosure_procedure",
    "agreement_special_rights_terms",
    "agreement_term",
    "agreement_survival_period",
    "agreement_disposition_requirements",
    "agreement_governing_law",
    "agreement_forum_venue_terms",
    "agreement_notice_delivery_methods",
    "agreement_notice_effectiveness",
    "agreement_integration_amendment_terms",
    "agreement_assignment_waiver_severability_terms",
    "agreement_party_a_signature_typed_name",
    "agreement_party_a_signature_title",
    "agreement_party_a_signature_date",
    "agreement_party_b_signature_typed_name",
    "agreement_party_b_signature_title",
    "agreement_party_b_signature_date",
    "agreement_notice_party_a_legal_name",
    "agreement_notice_party_b_legal_name",
    "agreement_notice_party_a_attention",
    "agreement_notice_party_b_attention",
    "agreement_notice_party_a_address",
    "agreement_notice_party_b_address",
    "agreement_notice_party_a_email",
    "agreement_notice_party_b_email",
    "agreement_notice_party_a_copy_to",
    "agreement_notice_party_b_copy_to",
}

EXPECTED_TYPES = {
    **{name: "/Tx" for name in TEXT_FIELDS},
    **{name: "/Ch" for name in CHOICE_FIELDS},
    **{name: "/Btn" for name in CHECKBOX_FIELDS},
}


def dereference(value: Any) -> Any:
    """Resolve an indirect PDF object while leaving direct objects unchanged."""
    return value.get_object() if isinstance(value, IndirectObject) else value


def inherited_value(widget: DictionaryObject, key: str) -> Any:
    """Read an inheritable field entry from a widget or its parent chain."""
    current: Any = widget
    while isinstance(current, DictionaryObject):
        if key in current:
            return dereference(current[key])
        parent = current.get("/Parent")
        if parent is None:
            return None
        current = dereference(parent)
    return None


def qualified_field_name(widget: DictionaryObject) -> str | None:
    """Build the fully qualified field name from /T and /Parent entries."""
    parts: list[str] = []
    current: Any = widget
    while isinstance(current, DictionaryObject):
        partial_name = current.get("/T")
        if partial_name is not None:
            parts.append(str(partial_name))
        parent = current.get("/Parent")
        if parent is None:
            break
        current = dereference(parent)
    return ".".join(reversed(parts)) if parts else None


def appearance_is_nonempty(value: Any) -> bool:
    """Require every normal-appearance leaf to be a nonempty PDF stream."""
    resolved = dereference(value)
    get_data = getattr(resolved, "get_data", None)
    if callable(get_data):
        return len(get_data()) > 0
    if isinstance(resolved, DictionaryObject):
        return bool(resolved) and all(
            appearance_is_nonempty(child) for child in resolved.values()
        )
    return False


def choice_option_values(field: DictionaryObject) -> list[str]:
    """Return the selectable export values from a PDF choice field."""
    values: list[str] = []
    for option in field.get("/Opt", []):
        resolved = dereference(option)
        if isinstance(resolved, (list, tuple)):
            if not resolved:
                raise ValueError("choice field contains an empty /Opt entry")
            values.append(str(dereference(resolved[0])))
        else:
            values.append(str(resolved))
    return values


def validate(
    pdf_path: Path,
    expected_types: dict[str, str] | None = EXPECTED_TYPES,
) -> tuple[int, int]:
    reader = PdfReader(pdf_path)
    root = dereference(reader.trailer["/Root"])
    acroform_ref = root.get("/AcroForm")
    if acroform_ref is None:
        raise ValueError("PDF catalog has no /AcroForm entry")
    acroform = dereference(acroform_ref)

    if bool(acroform.get("/NeedAppearances", False)):
        raise ValueError("/AcroForm relies on /NeedAppearances true")

    canonical_refs = list(acroform.get("/Fields", []))
    if not canonical_refs:
        raise ValueError("/AcroForm/Fields is empty")

    fields = reader.get_fields() or {}
    actual_names = set(fields)
    expected_names = set(expected_types) if expected_types is not None else set(fields)
    missing = sorted(expected_names - actual_names)
    unexpected = sorted(actual_names - expected_names)
    if missing or unexpected:
        raise ValueError(
            f"canonical field-name mismatch; missing={missing}, unexpected={unexpected}"
        )
    if len(canonical_refs) != len(expected_names):
        raise ValueError(
            f"/AcroForm/Fields has {len(canonical_refs)} entries; "
            f"expected {len(expected_names)}"
        )

    if expected_types is None:
        unsupported = {
            name: str(field.get("/FT"))
            for name, field in fields.items()
            if str(field.get("/FT")) not in {"/Tx", "/Ch", "/Btn"}
        }
        if unsupported:
            raise ValueError(f"unsupported AcroForm field types: {unsupported}")
    else:
        for name, expected_type in expected_types.items():
            actual_type = str(fields[name].get("/FT"))
            if actual_type != expected_type:
                raise ValueError(
                    f"field {name!r} has type {actual_type!r}; expected {expected_type!r}"
                )

    for name, field in fields.items():
        if str(field.get("/FT")) != "/Ch":
            continue
        option_values = choice_option_values(field)
        if not option_values:
            raise ValueError(f"choice field {name!r} has no /Opt entries")
        if len(option_values) != len(set(option_values)):
            raise ValueError(f"choice field {name!r} repeats an /Opt export value")
        for key in ("/V", "/DV"):
            initial = field.get(key)
            if initial is None:
                continue
            resolved_initial = dereference(initial)
            selected = (
                [str(dereference(item)) for item in resolved_initial]
                if isinstance(resolved_initial, (list, tuple))
                else [str(resolved_initial)]
            )
            invalid = [value for value in selected if value not in option_values]
            if invalid:
                raise ValueError(
                    f"choice field {name!r} has {key} value(s) absent from /Opt: {invalid}"
                )
            raise ValueError(
                f"choice field {name!r} has a preselected {key} value; "
                "Linear Space choice menus must start blank"
            )

    widgets_by_name: dict[str, list[DictionaryObject]] = defaultdict(list)
    for page_number, page in enumerate(reader.pages, start=1):
        for annotation_ref in page.get("/Annots", []):
            annotation = dereference(annotation_ref)
            if str(annotation.get("/Subtype")) != "/Widget":
                continue
            name = qualified_field_name(annotation)
            if name is None:
                raise ValueError(f"unnamed /Widget annotation on page {page_number}")
            widgets_by_name[name].append(annotation)

            appearance = dereference(annotation.get("/AP"))
            if not isinstance(appearance, DictionaryObject) or "/N" not in appearance:
                raise ValueError(f"widget {name!r} has no normal appearance (/AP /N)")
            if not appearance_is_nonempty(appearance["/N"]):
                raise ValueError(f"widget {name!r} has an empty normal appearance")

            if name in CHECKBOX_FIELDS or (
                expected_types is None and str(inherited_value(annotation, "/FT")) == "/Btn"
            ):
                value = inherited_value(annotation, "/V")
                state = annotation.get("/AS")
                if value is None or state is None or str(value) != str(state):
                    raise ValueError(
                        f"checkbox {name!r} has inconsistent /V={value!r} and /AS={state!r}"
                    )
                normal = dereference(appearance["/N"])
                if not isinstance(normal, DictionaryObject) or state not in normal:
                    raise ValueError(
                        f"checkbox {name!r} has no appearance for state {state!r}"
                    )

    widget_names = set(widgets_by_name)
    missing_widgets = sorted(expected_names - widget_names)
    unexpected_widgets = sorted(widget_names - expected_names)
    if missing_widgets or unexpected_widgets:
        raise ValueError(
            "widget-name mismatch; "
            f"missing={missing_widgets}, unexpected={unexpected_widgets}"
        )

    repeated = sorted(
        name for name, widgets in widgets_by_name.items() if len(widgets) != 1
    )
    if repeated:
        counts = {name: len(widgets_by_name[name]) for name in repeated}
        raise ValueError(f"field names do not map one-to-one to widgets: {counts}")

    return len(canonical_refs), sum(len(items) for items in widgets_by_name.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="legal-template PDF to validate")
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help=(
            "validate the PDF's actual field names and types without enforcing "
            "the stock legal template's exact field manifest"
        ),
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF does not exist: {args.pdf}")

    try:
        field_count, widget_count = validate(
            args.pdf,
            expected_types=None if args.structure_only else EXPECTED_TYPES,
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"AcroForm validation failed: {exc}", file=sys.stderr)
        return 1

    print(
        f"Validated {field_count} canonical AcroForm fields and "
        f"{widget_count} one-to-one /Widget annotations with nonempty appearances."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
