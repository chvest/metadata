"""
NATO Metadata Standards Comparison Tool
Flask Web Application — localhost:5000

Routes:
  GET  /               → index.html (landing page)
  GET/POST /detect     → detect.html (upload/paste metadata, show results)
  GET/POST /generate   → generate.html (select standard, generate example)
  GET  /compare        → compare.html (compatibility matrix heatmap)
  GET  /report/<id>    → HTML compatibility report
  GET  /report/<id>/pdf → PDF compatibility report
  POST /api/detect     → JSON API: detect standard from metadata
  POST /api/generate   → JSON API: generate example metadata
"""
import io
import json
import os
import sys

from flask import (
    Flask, render_template, request, jsonify,
    send_file, abort, Response, redirect, url_for,
)

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB upload limit


# ---------------------------------------------------------------------------
# Lazy imports (so we don't slow down startup if a module is unavailable)
# ---------------------------------------------------------------------------

def _get_registry():
    from standards.registry import get_all_standards, get_standard, list_standard_ids
    return get_all_standards, get_standard, list_standard_ids


def _get_detector():
    from engine.detector import detect_from_string, detect, get_field_analysis, parse_metadata
    return detect_from_string, detect, get_field_analysis, parse_metadata


def _get_generator():
    from engine.generator import FieldGenerator, to_xml
    return FieldGenerator, to_xml


def _get_reporter():
    from engine.reporter import generate_html_report, generate_pdf_report, heatmap_html
    return generate_html_report, generate_pdf_report, heatmap_html


# ---------------------------------------------------------------------------
# Context processor — inject standards list into all templates
# ---------------------------------------------------------------------------

@app.context_processor
def inject_standards():
    from standards.suites import get_all_suites
    get_all_standards, _, _ = _get_registry()
    standards = get_all_standards()
    return dict(
        all_standards=standards,
        standards_by_domain={
            domain: [s for s in standards if s.domain == domain]
            for domain in ["NATO", "EU", "ISO", "NIST"]
        },
        all_suites=get_all_suites(),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    get_all_standards, _, _ = _get_registry()
    standards = get_all_standards()
    domain_counts = {}
    for s in standards:
        domain_counts[s.domain] = domain_counts.get(s.domain, 0) + 1
    return render_template("index.html", domain_counts=domain_counts)


@app.route("/detect", methods=["GET", "POST"])
def detect_view():
    get_all_standards, get_standard, _ = _get_registry()
    detect_from_string, detect, get_field_analysis, parse_metadata = _get_detector()

    result = None
    raw_input = ""
    error = None
    field_analysis = None

    if request.method == "POST":
        # Handle file upload
        if "metadata_file" in request.files and request.files["metadata_file"].filename:
            f = request.files["metadata_file"]
            raw_input = f.read().decode("utf-8", errors="replace")
        else:
            raw_input = request.form.get("metadata_text", "").strip()

        if raw_input:
            result = detect_from_string(raw_input)
            if result["success"] and result["results"]:
                top_id = result["top_match"]["standard_id"]
                parsed_meta, _, _ = parse_metadata(raw_input)
                if parsed_meta:
                    field_analysis = get_field_analysis(parsed_meta, top_id)
        else:
            error = "No input provided. Please upload a file or paste metadata text."

    return render_template(
        "detect.html",
        result=result,
        raw_input=raw_input,
        error=error,
        field_analysis=field_analysis,
    )


@app.route("/generate", methods=["GET", "POST"])
def generate_view():
    get_all_standards, get_standard, _ = _get_registry()
    FieldGenerator, to_xml = _get_generator()

    generated_json = None
    generated_xml = None
    selected_standard = None
    error = None
    include_optional = True
    include_conditional = True

    if request.method == "POST":
        std_id = request.form.get("standard_id", "")
        include_optional = request.form.get("include_optional") == "on"
        include_conditional = request.form.get("include_conditional") == "on"

        std = get_standard(std_id)
        if std is None:
            error = f"Unknown standard: {std_id}"
        else:
            selected_standard = std
            gen = FieldGenerator()
            metadata = gen.generate_for_standard(
                std,
                include_optional=include_optional,
                include_conditional=include_conditional,
            )
            generated_json = json.dumps(metadata, indent=2, ensure_ascii=False)
            generated_xml = to_xml(metadata, std)

    from standards.suites import get_suites_for_standard
    selected_suites = get_suites_for_standard(selected_standard.id) if selected_standard else []
    return render_template(
        "generate.html",
        generated_json=generated_json,
        generated_xml=generated_xml,
        selected_standard=selected_standard,
        selected_suites=selected_suites,
        include_optional=include_optional,
        include_conditional=include_conditional,
        error=error,
    )


@app.route("/compare")
def compare_view():
    from engine.reporter import heatmap_html as _heatmap_html
    from standards.crosswalk import build_compatibility_matrix
    from standards.suites import build_pairwise_summary
    get_all_standards, _, _ = _get_registry()

    hmap = _heatmap_html()
    matrix = build_compatibility_matrix()
    standards = get_all_standards()
    pairwise = build_pairwise_summary()

    return render_template(
        "compare.html",
        heatmap_html=hmap,
        matrix=matrix,
        standards=standards,
        pairwise=pairwise,
    )


@app.route("/suite/<suite_id>")
def suite_view(suite_id: str):
    from standards.suites import get_suite, get_all_suites, get_suite_example
    _, get_standard, _ = _get_registry()
    suite = get_suite(suite_id)
    if suite is None:
        abort(404)
    # Enrich members with their standard objects
    enriched = []
    for member in suite.members:
        std = get_standard(member.standard_id)
        enriched.append({"member": member, "standard": std})
    example = get_suite_example(suite_id)
    return render_template("suite.html", suite=suite, enriched_members=enriched,
                           all_suites=get_all_suites(), example=example)


@app.route("/pairwise", methods=["GET"])
def pairwise_select():
    """Selector page — redirects to /pairwise/<a>/<b> once two standards are chosen."""
    get_all_standards, _, _ = _get_registry()
    id_a = request.args.get("a", "")
    id_b = request.args.get("b", "")
    if id_a and id_b and id_a != id_b:
        return redirect(url_for("pairwise_view", id_a=id_a, id_b=id_b))
    return render_template("pairwise.html", id_a=id_a, id_b=id_b, data=None)


@app.route("/pairwise/<id_a>/<id_b>")
def pairwise_view(id_a: str, id_b: str):
    from standards.crosswalk import build_pairwise_data
    _, get_standard, _ = _get_registry()
    if get_standard(id_a) is None or get_standard(id_b) is None:
        abort(404)
    data = build_pairwise_data(id_a, id_b)
    return render_template("pairwise.html", id_a=id_a, id_b=id_b, data=data)


@app.route("/methodology")
def methodology_view():
    from standards.crosswalk import ALL_CROSSWALKS, KNOWN_CONFLICTS
    from standards.registry import get_all_standards
    from collections import Counter
    stats = {
        "n_standards": len(get_all_standards()),
        "n_crosswalk_entries": len(ALL_CROSSWALKS),
        "n_manual_conflicts": len(KNOWN_CONFLICTS),
        "mapping_counts": dict(Counter(e.mapping_type for e in ALL_CROSSWALKS)),
        "conflict_type_counts": dict(Counter(c.conflict_type for c in KNOWN_CONFLICTS)),
        "conflict_sev_counts": dict(Counter(c.severity for c in KNOWN_CONFLICTS)),
        "n_directed_pairs": len(set((e.source_standard, e.target_standard) for e in ALL_CROSSWALKS)),
    }
    return render_template("methodology.html", stats=stats)


@app.route("/tutorial")
def tutorial_view():
    from engine.generator import FieldGenerator
    from standards.crosswalk import ALL_CROSSWALKS, build_conflicts
    from standards.base import Obligation

    _, get_standard, _ = _get_registry()
    FieldGenerator, to_xml = _get_generator()

    src_id = "adatp5636"
    tgt_id = "dublin_core"
    src_std = get_standard(src_id)
    tgt_std = get_standard(tgt_id)

    # Generate a fixed, realistic source record
    import random
    from faker import Faker
    fake = Faker()
    Faker.seed(99)
    random.seed(99)

    doc = {
        "title": "Allied Ground Surveillance — Interoperability Assessment Report 2024",
        "identifier": "urn:nato:resource:2024:REP-AGS-0047",
        "creator": "type=person; name=Maj. Claire Dubois; affiliation=HQ AIRCOM Ramstein; "
                   "email=c.dubois@hqaircom.nato.int; role=author",
        "publisher": "type=organisation; name=HQ AIRCOM; affiliation=NATO Allied Air Command",
        "dateCreated": "2024-03-15T09:00:00Z",
        "dateIssued": "2024-03-22T14:30:00Z",
        "description": "Assessment of interoperability gaps between AGS sensor networks and "
                       "national C2 systems across Allied nations. Covers data link standards, "
                       "metadata exchange protocols, and recommended mitigation actions.",
        "subject": "Allied Ground Surveillance; Interoperability; C2 Systems; NATO Standards",
        "language": "eng",
        "type": "Report",
        "mediaFormat": "application/pdf",
        "metadataConfidentialityLabel": "PolicyIdentifier=urn:nato:policy:security; "
                                        "Classification=NATO UNCLASSIFIED; "
                                        "Category[TagName=Releasability,Type=PERMISSIVE,GenericValue=NATO]",
        "originatorConfidentialityLabel": "PolicyIdentifier=urn:nato:policy:security; "
                                          "Classification=NATO UNCLASSIFIED; "
                                          "Category[TagName=Releasability,Type=PERMISSIVE,GenericValue=NATO]",
        "rights": "© 2024 NATO Allied Air Command. All rights reserved.",
        "accessRights": "NATO UNCLASSIFIED — Releasable to NATO nations",
        "recordsDisposition": "Retain 5 years; review 2029-03-22",
        "version": "1.2",
    }

    # Build the converted Dublin Core record by applying crosswalk rules
    crosswalk_ab = {e.source_field: e for e in ALL_CROSSWALKS
                    if e.source_standard == src_id and e.target_standard == tgt_id}

    converted = {}
    field_trace = []   # [{src_field, src_value, tgt_field, mapping_type, outcome, notes}]

    for fname, fvalue in doc.items():
        entry = crosswalk_ab.get(fname)
        if entry is None:
            field_trace.append({"src_field": fname, "src_value": fvalue,
                                 "tgt_field": None, "mapping_type": "none",
                                 "outcome": "lost", "notes": "No crosswalk entry"})
            continue
        if entry.mapping_type == "none" or not entry.target_field:
            field_trace.append({"src_field": fname, "src_value": fvalue,
                                 "tgt_field": None, "mapping_type": "none",
                                 "outcome": "lost", "notes": entry.notes})
            continue

        tgt_field = entry.target_field
        outcome = "exact" if entry.mapping_type == "exact" else \
                  "similar" if entry.mapping_type == "similar" else "degraded"

        # Simulate value transformation for notable fields
        tgt_value = fvalue
        if fname == "creator":
            tgt_value = "Maj. Claire Dubois (HQ AIRCOM Ramstein)"
        elif fname == "publisher":
            tgt_value = "HQ AIRCOM — NATO Allied Air Command"
        elif fname in ("dateCreated", "dateIssued"):
            tgt_value = fvalue[:10]   # trim to date-only (ISO 8601 date)
        elif fname == "accessRights":
            tgt_value = "NATO UNCLASSIFIED — Releasable to NATO nations"

        # Dublin Core allows multiple values for some fields — merge into existing
        if tgt_field in converted:
            if not isinstance(converted[tgt_field], list):
                converted[tgt_field] = [converted[tgt_field]]
            converted[tgt_field].append(tgt_value)
        else:
            converted[tgt_field] = tgt_value

        field_trace.append({"src_field": fname, "src_value": fvalue,
                             "tgt_field": tgt_field, "tgt_value": tgt_value,
                             "mapping_type": entry.mapping_type,
                             "outcome": outcome, "notes": entry.notes})

    conflicts = build_conflicts(src_id, tgt_id)
    # Only keep the non-auto-detected ones for the tutorial to keep it concise
    key_conflicts = [c for c in conflicts if not c["auto_detected"]]

    return render_template(
        "tutorial.html",
        src_std=src_std,
        tgt_std=tgt_std,
        doc=doc,
        converted=converted,
        field_trace=field_trace,
        conflicts=conflicts,
        key_conflicts=key_conflicts,
    )


@app.route("/report/<standard_id>")
def report_view(standard_id: str):
    generate_html_report, _, _ = _get_reporter()
    _, get_standard, _ = _get_registry()

    from standards.suites import get_suites_for_standard, get_suite_siblings
    std = get_standard(standard_id)
    if std is None:
        abort(404)

    html_content = generate_html_report(standard_id)
    # Inject suite info into a wrapper page rather than the standalone report HTML
    suites = get_suites_for_standard(standard_id)
    siblings = get_suite_siblings(standard_id)
    return render_template(
        "report.html",
        std=std,
        report_html=html_content,
        suites=suites,
        siblings=siblings,
    )


@app.route("/report/<standard_id>/pdf")
def report_pdf(standard_id: str):
    _, generate_pdf_report, _ = _get_reporter()
    _, get_standard, _ = _get_registry()

    std = get_standard(standard_id)
    if std is None:
        abort(404)

    try:
        pdf_bytes = generate_pdf_report(standard_id)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"compatibility_report_{standard_id}.pdf",
        )
    except Exception as e:
        return Response(
            f"<h3>PDF generation error</h3><pre>{str(e)}</pre>",
            mimetype="text/html",
            status=500,
        )


# ---------------------------------------------------------------------------
# Download routes for generated metadata
# ---------------------------------------------------------------------------

@app.route("/download/json", methods=["POST"])
def download_json():
    data = request.form.get("json_content", "{}")
    std_id = request.form.get("standard_id", "metadata")
    return send_file(
        io.BytesIO(data.encode("utf-8")),
        mimetype="application/json",
        as_attachment=True,
        download_name=f"example_{std_id}.json",
    )


@app.route("/download/xml", methods=["POST"])
def download_xml():
    data = request.form.get("xml_content", "<metadata/>")
    std_id = request.form.get("standard_id", "metadata")
    return send_file(
        io.BytesIO(data.encode("utf-8")),
        mimetype="application/xml",
        as_attachment=True,
        download_name=f"example_{std_id}.xml",
    )


# ---------------------------------------------------------------------------
# JSON API endpoints
# ---------------------------------------------------------------------------

@app.route("/api/detect", methods=["POST"])
def api_detect():
    detect_from_string, _, _, _ = _get_detector()

    if request.is_json:
        payload = request.get_json(force=True)
        raw = payload.get("metadata", "") if isinstance(payload, dict) else str(payload)
    else:
        raw = request.get_data(as_text=True)

    if not raw:
        return jsonify({"error": "No metadata provided"}), 400

    result = detect_from_string(raw)
    return jsonify(result)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    FieldGenerator, to_xml = _get_generator()
    _, get_standard, _ = _get_registry()

    if request.is_json:
        payload = request.get_json(force=True) or {}
    else:
        payload = {}

    std_id = payload.get("standard_id", "adatp5636")
    include_optional = payload.get("include_optional", True)
    include_conditional = payload.get("include_conditional", True)
    output_format = payload.get("format", "json").lower()

    std = get_standard(std_id)
    if std is None:
        return jsonify({"error": f"Unknown standard: {std_id}"}), 400

    gen = FieldGenerator()
    metadata = gen.generate_for_standard(
        std,
        include_optional=bool(include_optional),
        include_conditional=bool(include_conditional),
    )

    if output_format == "xml":
        xml_str = to_xml(metadata, std)
        return Response(xml_str, mimetype="application/xml")

    return jsonify({"standard_id": std_id, "metadata": metadata})


@app.route("/api/crosswalk/<source_id>/<target_id>")
def api_crosswalk(source_id: str, target_id: str):
    from standards.crosswalk import get_crosswalks_from
    _, get_standard, _ = _get_registry()
    crosswalks = get_crosswalks_from(source_id)
    src_std = get_standard(source_id)
    tgt_std = get_standard(target_id)
    filtered = []
    for e in crosswalks:
        if e.target_standard != target_id:
            continue
        src_desc = ""
        tgt_desc = ""
        if src_std and e.source_field in src_std.fields:
            src_desc = src_std.fields[e.source_field].description
        if tgt_std and e.target_field and e.target_field in tgt_std.fields:
            tgt_desc = tgt_std.fields[e.target_field].description
        filtered.append({
            "source_field": e.source_field,
            "source_description": src_desc,
            "target_field": e.target_field,
            "target_description": tgt_desc,
            "mapping_type": e.mapping_type,
            "notes": e.notes,
        })
    return jsonify({
        "source": source_id,
        "target": target_id,
        "mappings": filtered,
    })


@app.route("/api/suites")
def api_suites():
    from standards.suites import get_all_suites
    suites = get_all_suites()
    return jsonify([{
        "id": s.id, "name": s.name, "description": s.description,
        "anchor_id": s.anchor_id, "color": s.color,
        "members": [{"standard_id": m.standard_id, "relationship": m.relationship,
                     "role": m.role} for m in s.members],
    } for s in suites])


@app.route("/api/matrix")
def api_matrix():
    from standards.crosswalk import build_compatibility_matrix
    matrix = build_compatibility_matrix()
    return jsonify(matrix)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("base.html"), 404


@app.errorhandler(500)
def server_error(e):
    return f"<h3>Server Error</h3><pre>{str(e)}</pre>", 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print(" NATO Metadata Standards Comparison Tool")
    print(" http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
