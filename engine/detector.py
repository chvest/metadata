"""
Metadata Standard Detector.

Accepts a parsed metadata dict (from JSON or XML) and returns a ranked list
of (standard_id, score, details) tuples.

Detection algorithm per standard:
  1. Namespace/prefix check (high weight)
  2. Mandatory field presence (high weight)
  3. Optional/specific field presence (medium weight)
  4. Value format conformance (low weight)
"""
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from lxml import etree

from standards.registry import get_all_standards


def parse_metadata(raw: str) -> Tuple[Optional[Dict[str, Any]], str, str]:
    """
    Parse raw string as JSON or XML.
    Returns (parsed_dict, format_str, error_str).
    format_str: "json" | "xml" | "unknown"
    """
    raw = raw.strip()
    if not raw:
        return None, "unknown", "Empty input"

    # Try JSON first
    if raw.startswith("{") or raw.startswith("["):
        try:
            data = json.loads(raw)
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            return data, "json", ""
        except json.JSONDecodeError as e:
            return None, "json", str(e)

    # Try XML
    try:
        root = etree.fromstring(raw.encode("utf-8") if isinstance(raw, str) else raw)
        data = _xml_to_dict(root)
        return data, "xml", ""
    except etree.XMLSyntaxError as e:
        pass

    # Try JSON again (malformed check)
    try:
        data = json.loads(raw)
        return data, "json", ""
    except Exception:
        pass

    return None, "unknown", "Could not parse as JSON or XML"


def _xml_to_dict(root: etree._Element) -> Dict[str, Any]:
    """Convert an lxml Element tree to a flat dict, stripping namespaces."""
    result: Dict[str, Any] = {}

    # Capture namespace
    ns = root.nsmap.get(None, "") or root.nsmap.get(list(root.nsmap.keys())[0], "") if root.nsmap else ""
    if ns:
        result["@namespace"] = ns

    def _local(tag: str) -> str:
        """Strip namespace from tag."""
        if tag.startswith("{"):
            return tag.split("}", 1)[1]
        return tag

    def _process(element: etree._Element, d: dict):
        tag = _local(element.tag)
        # Capture namespace hint from element
        ns_hint = element.nsmap.get(None, "") or ""
        if ns_hint and "@namespace" not in d:
            d["@namespace"] = ns_hint

        children = list(element)
        text = (element.text or "").strip()
        attrs = dict(element.attrib)

        if children:
            child_dict: Dict[str, Any] = {}
            for child in children:
                _process(child, child_dict)
            val = child_dict
        elif attrs:
            val = {**attrs, "#text": text} if text else attrs
        else:
            val = text or None

        if tag in d:
            existing = d[tag]
            if isinstance(existing, list):
                existing.append(val)
            else:
                d[tag] = [existing, val]
        else:
            d[tag] = val

    for child in root:
        _process(child, result)

    # Also add root element's own children directly processed
    root_tag = _local(root.tag)
    root_text = (root.text or "").strip()
    if root_text and root_tag not in result:
        result[root_tag] = root_text

    # Add all root-level attributes
    for k, v in root.attrib.items():
        result[f"@{_local(k)}"] = v

    return result


def detect(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Score all registered standards against the metadata dict.
    Returns a sorted list (highest score first) of:
      {
        standard_id, standard_name, score,
        matched_mandatory, missing_mandatory,
        matched_optional, matched_specific,
        details
      }
    """
    standards = get_all_standards()
    results = []

    meta_lower = {k.lower(): v for k, v in metadata.items()}

    for std in standards:
        try:
            score = std.detect_score(metadata)
        except Exception:
            score = 0.0

        # Detailed field analysis
        mandatory_fields = std.get_mandatory_fields()
        optional_fields = std.get_optional_fields()

        matched_m = [f.name for f in mandatory_fields if f.name.lower() in meta_lower]
        missing_m = [f.name for f in mandatory_fields if f.name.lower() not in meta_lower]
        matched_o = [f.name for f in optional_fields if f.name.lower() in meta_lower]

        # Build explanation
        explanation_parts = []
        if matched_m:
            explanation_parts.append(
                f"Matched {len(matched_m)}/{len(mandatory_fields)} mandatory fields: "
                f"{', '.join(matched_m[:5])}{'...' if len(matched_m) > 5 else ''}"
            )
        if missing_m:
            explanation_parts.append(
                f"Missing mandatory fields: "
                f"{', '.join(missing_m[:5])}{'...' if len(missing_m) > 5 else ''}"
            )
        if matched_o:
            explanation_parts.append(
                f"Matched {len(matched_o)} optional/specific fields"
            )

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        if ns and hasattr(std, '_ns_markers'):
            for marker in std._ns_markers:
                if marker in ns:
                    explanation_parts.append(f"Namespace match: '{marker}'")
                    break

        results.append({
            "standard_id": std.id,
            "standard_name": std.name,
            "standard_full_name": std.full_name,
            "domain": std.domain,
            "score": round(score, 4),
            "matched_mandatory": matched_m,
            "missing_mandatory": missing_m,
            "matched_optional": matched_o,
            "explanation": "; ".join(explanation_parts) if explanation_parts else "No significant matches found",
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def detect_from_string(raw: str) -> Dict[str, Any]:
    """
    Parse raw input and run detection.
    Returns full result dict.
    """
    metadata, fmt, parse_error = parse_metadata(raw)
    if metadata is None:
        return {
            "success": False,
            "error": f"Parse failed ({fmt}): {parse_error}",
            "format": fmt,
            "results": [],
        }

    results = detect(metadata)

    top = results[0] if results else None
    return {
        "success": True,
        "format": fmt,
        "parsed_fields": list(metadata.keys()),
        "top_match": top,
        "results": results,
    }


def get_field_analysis(metadata: Dict[str, Any], standard_id: str) -> Dict[str, Any]:
    """
    For a specific standard, analyse the metadata field by field:
    - Which mandatory fields are present/missing
    - Which optional fields are present
    - Which fields are unknown to this standard
    - Crosswalk info for each present field
    """
    from standards.registry import get_standard
    from standards.crosswalk import get_crosswalks_from

    std = get_standard(standard_id)
    if std is None:
        return {"error": f"Unknown standard: {standard_id}"}

    meta_lower = {k.lower(): v for k, v in metadata.items()}
    known_lower = {f.name.lower(): f for f in std.fields.values()}

    present_fields = []
    for name_low, field_def in known_lower.items():
        if name_low in meta_lower:
            crosswalks = get_crosswalks_from(standard_id)
            cw = [e for e in crosswalks if e.source_field.lower() == name_low]
            present_fields.append({
                "name": field_def.name,
                "obligation": field_def.obligation.value,
                "group": field_def.group,
                "layer": field_def.layer,
                "value": str(meta_lower[name_low])[:200],
                "crosswalks": [
                    {"target": e.target_standard, "target_field": e.target_field,
                     "mapping_type": e.mapping_type, "notes": e.notes}
                    for e in cw
                ],
            })

    missing_mandatory = [
        {"name": f.name, "description": f.description, "reference": f.reference}
        for f in std.get_mandatory_fields()
        if f.name.lower() not in meta_lower
    ]

    unknown_fields = [
        k for k in metadata.keys()
        if not k.startswith("@") and k.lower() not in known_lower
    ]

    return {
        "standard_id": standard_id,
        "present_fields": present_fields,
        "missing_mandatory": missing_mandatory,
        "unknown_fields": unknown_fields,
    }
