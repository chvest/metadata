"""
Report Generator.

Produces:
1. HTML report with Plotly heatmap of field coverage
2. PDF report using ReportLab

For the compatibility matrix Plotly chart:
  fig.to_html(full_html=False, include_plotlyjs='cdn')
"""
import io
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import plotly.graph_objects as go

from standards.registry import get_all_standards, get_standard
from standards.crosswalk import (
    build_compatibility_matrix, get_crosswalks_from, ALL_CROSSWALKS, build_conflicts,
    get_pair_sources, get_value_issues
)


# ---------------------------------------------------------------------------
# Plotly helpers
# ---------------------------------------------------------------------------

def build_heatmap_fig() -> go.Figure:
    """Build the N×N compatibility matrix heatmap as a Plotly Figure."""
    matrix = build_compatibility_matrix()
    standards = get_all_standards()

    ids = [s.id for s in standards]
    names = [s.name for s in standards]

    z = []
    text = []
    for src_id in ids:
        row_z = []
        row_t = []
        for tgt_id in ids:
            val = matrix.get(src_id, {}).get(tgt_id, 0.0)
            row_z.append(round(val * 100, 1))
            row_t.append(f"{round(val * 100, 1)}%")
        z.append(row_z)
        text.append(row_t)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=names,
        y=names,
        text=text,
        texttemplate="%{text}",
        colorscale=[
            [0.0, "#2d1b69"],
            [0.2, "#5e2d91"],
            [0.4, "#9b4dca"],
            [0.6, "#3a86ff"],
            [0.8, "#48cae4"],
            [1.0, "#06d6a0"],
        ],
        zmin=0,
        zmax=100,
        colorbar=dict(title="Compatibility %"),
        hovertemplate=(
            "<b>Source: %{y}</b><br>"
            "<b>Target: %{x}</b><br>"
            "Compatibility: %{text}<extra></extra>"
        ),
    ))
    fig.update_layout(
        title="Metadata Standards Compatibility Matrix",
        xaxis=dict(title="Target Standard", tickangle=-45),
        yaxis=dict(title="Source Standard"),
        margin=dict(l=150, r=50, t=80, b=150),
        height=600,
        font=dict(family="Segoe UI, Arial, sans-serif", size=12),
        paper_bgcolor="#f8f9fa",
        plot_bgcolor="#f8f9fa",
    )
    return fig


def heatmap_html() -> str:
    """Return the heatmap as an HTML div (no full page, CDN plotly.js)."""
    fig = build_heatmap_fig()
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def build_single_standard_coverage_fig(standard_id: str) -> Optional[go.Figure]:
    """Bar chart: field coverage of source standard across all other standards."""
    src = get_standard(standard_id)
    if src is None:
        return None

    all_stds = [s for s in get_all_standards() if s.id != standard_id]
    names = [s.name for s in all_stds]
    ids = [s.id for s in all_stds]

    crosswalks = get_crosswalks_from(standard_id)

    def _pct(tgt_id: str) -> float:
        src_fields = list(src.fields.keys())
        if not src_fields:
            return 0.0
        mapped = sum(
            1 for e in crosswalks
            if e.target_standard == tgt_id and e.mapping_type != "none"
        )
        return round((mapped / len(src_fields)) * 100, 1)

    pcts = [_pct(tid) for tid in ids]

    colors = ["#3a86ff" if p >= 50 else "#9b4dca" if p >= 25 else "#e63946"
              for p in pcts]

    fig = go.Figure(data=go.Bar(
        x=names, y=pcts,
        marker_color=colors,
        text=[f"{p}%" for p in pcts],
        textposition="outside",
        hovertemplate="%{x}: %{y}%<extra></extra>",
    ))
    fig.update_layout(
        title=f"Field Coverage of {src.name} in Other Standards",
        xaxis=dict(title="Target Standard", tickangle=-30),
        yaxis=dict(title="% Fields Mapped", range=[0, 110]),
        height=400,
        paper_bgcolor="#f8f9fa",
        plot_bgcolor="#f8f9fa",
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )
    return fig


# ---------------------------------------------------------------------------
# Field value comparison helper
# ---------------------------------------------------------------------------

def _build_value_comparison_html(std, groups, matrix, standard_id: str, domain_color: dict) -> str:
    """
    Build an HTML section comparing allowed values for fields that have a
    non-'none' crosswalk mapping. Groups cards by target standard.
    """
    from collections import OrderedDict

    mapping_border = {
        "exact": "#198754",   # green
        "similar": "#0d6efd", # blue
        "partial": "#fd7e14", # orange
    }
    mapping_label = {
        "exact": ("Exact match", "#198754"),
        "similar": ("Similar — minor differences", "#0d6efd"),
        "partial": ("Partial — significant differences", "#fd7e14"),
    }

    sections = []
    total_mapped = 0

    for tgt_id, entries in groups.items():
        mapped = [e for e in entries if e.mapping_type != "none"]
        if not mapped:
            continue
        total_mapped += len(mapped)

        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        tgt_domain = tgt.domain if tgt else ""
        dcol = domain_color.get(tgt_domain, "#495057")

        cards = []
        for entry in mapped:
            src_field = std.fields.get(entry.source_field)
            tgt_field = tgt.fields.get(entry.target_field) if (tgt and entry.target_field) else None

            border = mapping_border.get(entry.mapping_type, "#6c757d")
            mlabel, mcolor = mapping_label.get(entry.mapping_type, ("Unknown", "#6c757d"))

            # Auto-generate compatibility flags
            flags = []
            if src_field and tgt_field:
                if src_field.representation_term != tgt_field.representation_term:
                    flags.append(
                        f'<span class="badge" style="background:#fff3cd;color:#664d03;border:1px solid #ffc107;">'
                        f'Type mismatch: {src_field.representation_term.value} vs {tgt_field.representation_term.value}</span>'
                    )
                if src_field.cardinality != tgt_field.cardinality:
                    flags.append(
                        f'<span class="badge" style="background:#fff3cd;color:#664d03;border:1px solid #ffc107;">'
                        f'Cardinality differs: {src_field.cardinality.value} vs {tgt_field.cardinality.value}</span>'
                    )
            elif src_field and not tgt_field:
                flags.append(
                    '<span class="badge" style="background:#f8d7da;color:#842029;border:1px solid #f5c2c7;">'
                    'Target field definition not found</span>'
                )

            def _field_col(f, label):
                if f is None:
                    return f'<div class="p-2 text-muted" style="font-size:0.8rem;"><em>No definition available</em></div>'
                values_html = f'<div style="font-size:0.78rem;color:#495057;margin-top:0.3rem;">{f.values}</div>' if f.values else ""
                condition_html = (
                    f'<div style="font-size:0.75rem;color:#6c757d;font-style:italic;margin-top:0.2rem;">'
                    f'Condition: {f.condition}</div>'
                ) if f.condition else ""
                ref_html = (
                    f'<div style="font-size:0.72rem;color:#6c757d;margin-top:0.25rem;">'
                    f'<span title="Standard reference">&#128209;</span> {f.reference}</div>'
                ) if f.reference else ""
                return f"""
                  <div style="font-size:0.8rem;">
                    <div>
                      <span style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;
                                   color:#6c757d;font-weight:600;">{label}</span>
                    </div>
                    <code style="font-size:0.8rem;font-weight:700;">{f.name}</code>
                    <div style="margin-top:0.3rem;">
                      <span class="badge bg-light text-dark border" style="font-size:0.68rem;">
                        {f.representation_term.value}
                      </span>
                      <span class="badge bg-light text-dark border ms-1" style="font-size:0.68rem;">
                        {f.cardinality.value}
                      </span>
                      <span class="badge {'bg-danger' if f.obligation.value == 'mandatory' else 'bg-secondary'} ms-1"
                            style="font-size:0.68rem;">
                        {f.obligation.value}
                      </span>
                    </div>
                    {ref_html}
                    {values_html}
                    {condition_html}
                  </div>"""

            flags_html = (
                f'<div class="d-flex flex-wrap gap-1 mb-2">{" ".join(flags)}</div>' if flags else ""
            )
            notes_html = (
                f'<div style="font-size:0.78rem;color:#495057;border-top:1px solid #dee2e6;'
                f'padding-top:0.4rem;margin-top:0.4rem;">'
                f'<strong>Notes:</strong> {entry.notes}</div>'
            ) if entry.notes else ""

            cards.append(f"""
            <div style="border:1px solid {border};border-left:4px solid {border};
                        border-radius:6px;padding:0.75rem;margin-bottom:0.6rem;background:#fff;">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span style="font-weight:700;font-size:0.8rem;color:{mcolor};">{mlabel}</span>
                <span style="font-size:0.72rem;color:#6c757d;">
                  {entry.source_field} → {entry.target_field or '—'}
                </span>
              </div>
              {flags_html}
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;">
                <div style="background:#f8f9fa;border-radius:4px;padding:0.5rem;">
                  {_field_col(src_field, "Source — " + std.name)}
                </div>
                <div style="background:#f8f9fa;border-radius:4px;padding:0.5rem;">
                  {_field_col(tgt_field, "Target — " + tgt_name)}
                </div>
              </div>
              {notes_html}
            </div>""")

        sections.append(f"""
        <div class="mb-4">
          <div style="background:#f0f4ff;border-left:4px solid {dcol};padding:0.6rem 1rem;
                      border-radius:0 6px 6px 0;margin-bottom:0.75rem;
                      display:flex;align-items:center;gap:0.75rem;">
            <strong style="color:{dcol};font-size:0.9rem;">{tgt_name}</strong>
            <span class="badge" style="background:{dcol};color:#fff;font-size:0.7rem;">{tgt_domain}</span>
            <span style="font-size:0.8rem;color:#6c757d;">{len(mapped)} mapped field{'s' if len(mapped) != 1 else ''}</span>
          </div>
          {''.join(cards)}
        </div>""")

    if not sections:
        return ""

    return f"""
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-valcomp"
         aria-expanded="false" aria-controls="sec-valcomp"
         style="cursor:pointer;user-select:none;">
      <h5 class="mb-0">Field Value Comparison
        <span class="badge bg-secondary ms-2" style="font-size:0.75rem;">{total_mapped} mapped fields</span>
      </h5>
      <span class="sec-chevron" style="font-size:0.9rem;color:#6c757d;transition:transform 0.2s;">&#9660;</span>
    </div>
    <div id="sec-valcomp" class="collapse">
      <div class="card-body">
        <p class="text-muted small mb-3">
          Side-by-side comparison of how mapped fields differ in type, cardinality, and
          allowed values. Warnings are shown where the fields are compatible in name but
          differ in how values must be expressed.
        </p>
        {''.join(sections)}
      </div>
    </div>
  </div>"""


# ---------------------------------------------------------------------------
# Interoperability conflicts helper
# ---------------------------------------------------------------------------

def _build_conflicts_html(source_standard_id: str, groups: dict, domain_color: dict) -> str:
    """
    Build an HTML section listing interoperability conflicts for every target
    standard that appears in the crosswalk groups.
    """
    severity_cfg = {
        "blocking": {
            "label": "Blocking",
            "bg": "#f8d7da", "border": "#dc3545", "text": "#842029",
            "icon": "&#9940;",  # 🚫
            "badge": "background:#dc3545;color:#fff;",
        },
        "lossy": {
            "label": "Data loss",
            "bg": "#fff3cd", "border": "#ffc107", "text": "#664d03",
            "icon": "&#9888;",  # ⚠
            "badge": "background:#ffc107;color:#664d03;",
        },
        "transform_required": {
            "label": "Transform required",
            "bg": "#cff4fc", "border": "#0dcaf0", "text": "#055160",
            "icon": "&#8635;",  # ↻
            "badge": "background:#0dcaf0;color:#055160;",
        },
    }
    type_labels = {
        "mandatory_gap": "Mandatory gap",
        "vocabulary": "Vocabulary conflict",
        "obligation_inversion": "Obligation inversion",
        "structural": "Structural absence",
        "domain_mismatch": "Domain mismatch",
    }

    sections = []
    total_conflicts = 0

    for tgt_id in groups:
        conflicts = build_conflicts(source_standard_id, tgt_id)
        if not conflicts:
            continue

        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        tgt_domain = tgt.domain if tgt else ""
        dcol = domain_color.get(tgt_domain, "#495057")
        total_conflicts += len(conflicts)

        blocking = [c for c in conflicts if c["severity"] == "blocking"]
        lossy    = [c for c in conflicts if c["severity"] == "lossy"]
        tranform = [c for c in conflicts if c["severity"] == "transform_required"]

        summary_badges = ""
        if blocking:
            summary_badges += (f'<span class="badge me-1" style="background:#dc3545;color:#fff;">'
                               f'{len(blocking)} blocking</span>')
        if lossy:
            summary_badges += (f'<span class="badge me-1" style="background:#ffc107;color:#664d03;">'
                               f'{len(lossy)} data loss</span>')
        if tranform:
            summary_badges += (f'<span class="badge me-1" style="background:#0dcaf0;color:#055160;">'
                               f'{len(tranform)} transform required</span>')

        src_std = get_standard(source_standard_id)
        cards = []
        for c in conflicts:
            cfg = severity_cfg.get(c["severity"], severity_cfg["lossy"])
            type_label = type_labels.get(c["conflict_type"], c["conflict_type"])
            field_hint = ""
            src_ref_html = ""
            tgt_ref_html = ""
            if c["source_field"]:
                field_hint = (
                    f'<code style="font-size:0.75rem;background:rgba(0,0,0,0.08);'
                    f'padding:1px 5px;border-radius:3px;">{c["source_field"]}</code>'
                )
                # Source field reference
                if src_std and c["source_field"] in src_std.fields:
                    src_fdef = src_std.fields[c["source_field"]]
                    if src_fdef.reference:
                        src_ref_html = (
                            f'<span style="font-size:0.7rem;color:#6c757d;margin-left:6px;">'
                            f'&#128209; {src_fdef.reference}</span>'
                        )
                if c["target_field"]:
                    field_hint += (
                        f' → <code style="font-size:0.75rem;background:rgba(0,0,0,0.08);'
                        f'padding:1px 5px;border-radius:3px;">{c["target_field"]}</code>'
                    )
                    # Target field reference
                    if tgt and c["target_field"] in tgt.fields:
                        tgt_fdef = tgt.fields[c["target_field"]]
                        if tgt_fdef.reference:
                            tgt_ref_html = (
                                f'<span style="font-size:0.7rem;color:#6c757d;margin-left:6px;">'
                                f'&#128209; {tgt_fdef.reference}</span>'
                            )
            auto_badge = (
                '<span style="font-size:0.65rem;background:#e9ecef;color:#495057;'
                'padding:1px 5px;border-radius:3px;margin-left:4px;">auto-detected</span>'
                if c["auto_detected"] else ""
            )
            refs_html = ""
            if src_ref_html or tgt_ref_html:
                refs_html = (
                    f'<div style="font-size:0.72rem;color:#6c757d;margin-top:0.3rem;">'
                    + (src_ref_html or "")
                    + ((" &nbsp;·&nbsp; " + tgt_ref_html) if src_ref_html and tgt_ref_html else tgt_ref_html)
                    + "</div>"
                )
            cards.append(f"""
            <div style="border:1px solid {cfg['border']};border-left:4px solid {cfg['border']};
                        border-radius:6px;padding:0.75rem;margin-bottom:0.6rem;
                        background:{cfg['bg']};">
              <div class="d-flex justify-content-between align-items-start mb-1 flex-wrap gap-1">
                <div style="font-weight:700;font-size:0.85rem;color:{cfg['text']};">
                  {cfg['icon']} {c['title']}
                </div>
                <div class="d-flex gap-1 flex-wrap">
                  <span class="badge" style="{cfg['badge']}">{cfg['label']}</span>
                  <span class="badge" style="background:#6c757d;color:#fff;font-size:0.68rem;">
                    {type_label}
                  </span>
                  {auto_badge}
                </div>
              </div>
              {f'<div class="mb-1">{field_hint}{refs_html}</div>' if field_hint else ''}
              <p style="font-size:0.8rem;color:#212529;margin:0;">{c['description']}</p>
            </div>""")

        sections.append(f"""
        <div class="mb-4">
          <div style="background:#f0f4ff;border-left:4px solid {dcol};padding:0.6rem 1rem;
                      border-radius:0 6px 6px 0;margin-bottom:0.75rem;
                      display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
            <strong style="color:{dcol};font-size:0.9rem;">{tgt_name}</strong>
            <span class="badge" style="background:{dcol};color:#fff;font-size:0.7rem;">{tgt_domain}</span>
            {summary_badges}
          </div>
          {''.join(cards)}
        </div>""")

    if not sections:
        return ""

    legend_parts = []
    for sev, cfg in severity_cfg.items():
        badge_style = cfg["badge"] + "padding:1px 6px;border-radius:3px;"
        legend_parts.append(
            f'<span class="me-3" style="font-size:0.8rem;">'
            f'<span style="{badge_style}">{cfg["icon"]} {cfg["label"]}</span>'
            f'</span>'
        )
    severity_legend = "".join(legend_parts)

    return f"""
  <div class="card mb-4" style="border-top:3px solid #dc3545;">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center flex-wrap gap-2"
         data-bs-toggle="collapse" data-bs-target="#sec-conflicts"
         aria-expanded="true" aria-controls="sec-conflicts"
         style="cursor:pointer;user-select:none;">
      <h5 class="mb-0">&#9940; Interoperability Conflicts
        <span class="badge ms-2" style="background:#dc3545;color:#fff;font-size:0.75rem;">{total_conflicts}</span>
      </h5>
      <div class="d-flex align-items-center gap-2">
        <div>{severity_legend}</div>
        <span class="sec-chevron" style="font-size:0.9rem;color:#6c757d;transition:transform 0.2s;">&#9660;</span>
      </div>
    </div>
    <div id="sec-conflicts" class="collapse show">
      <div class="card-body">
        <div class="row g-3 mb-4">
          <div class="col-md-4">
            <div class="rounded p-3 h-100" style="background:#fde8ea;border-left:4px solid #dc3545;">
              <div style="font-weight:700;font-size:0.85rem;color:#842029;margin-bottom:0.35rem;">&#9940; Blocking</div>
              <p style="font-size:0.8rem;margin-bottom:0.3rem;">A conformant record in this standard <strong>cannot be made fully conformant</strong> in the target without discarding a mandatory field or fabricating a value.</p>
              <p style="font-size:0.78rem;color:#6c757d;margin:0;">The receiver may still parse the file, but it will <strong>fail validation</strong> against the target standard. Round-trips are not safe without human review.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="rounded p-3 h-100" style="background:#fff8e1;border-left:4px solid #ffc107;">
              <div style="font-weight:700;font-size:0.85rem;color:#664d03;margin-bottom:0.35rem;">&#9888; Lossy</div>
              <p style="font-size:0.8rem;margin-bottom:0.3rem;">Conversion is possible and the record will <strong>pass target validation</strong>, but <strong>some information is permanently degraded</strong>.</p>
              <p style="font-size:0.78rem;color:#6c757d;margin:0;">Example: a structured PointOfContact (name, role, email as sub-fields) mapped to a free-text field — the value transfers but internal structure is lost and cannot be recovered.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="rounded p-3 h-100" style="background:#e0f4fb;border-left:4px solid #0dcaf0;">
              <div style="font-weight:700;font-size:0.85rem;color:#055160;margin-bottom:0.35rem;">&#8635; Transform required</div>
              <p style="font-size:0.8rem;margin-bottom:0.3rem;">Fully interoperable, but only <strong>after a specific, well-defined transformation is applied</strong>. No information is permanently lost.</p>
              <p style="font-size:0.78rem;color:#6c757d;margin:0;">Examples: vocabulary mapping (NATO classifications → DC rights), date format conversion, or splitting one field into two. The transformation must be explicitly defined and consistently applied.</p>
            </div>
          </div>
        </div>
        <p class="text-muted small mb-3">Auto-detected entries are derived from mandatory fields with no crosswalk mapping to the target standard.</p>
        {''.join(sections)}
      </div>
    </div>
  </div>"""


# ---------------------------------------------------------------------------
# Value-level issues HTML section
# ---------------------------------------------------------------------------

def _build_value_issues_html(source_standard_id: str, groups: dict, domain_color: dict) -> str:
    """
    Build a collapsible HTML section showing value-level incompatibilities between
    source_standard and every target standard that has defined value issues.
    Only rendered when get_value_issues() returns entries for this standard as source.
    """
    sev_cfg = {
        "blocking":         {"bg": "#fde8ea", "border": "#dc3545", "text": "#842029",
                             "badge": "background:#dc3545;color:#fff;", "label": "Blocking"},
        "lossy":            {"bg": "#fff3cd", "border": "#ffc107", "text": "#664d03",
                             "badge": "background:#ffc107;color:#664d03;", "label": "Lossy"},
        "transform_required": {"bg": "#cff4fc", "border": "#0dcaf0", "text": "#055160",
                               "badge": "background:#0dcaf0;color:#055160;", "label": "Transform required"},
    }
    type_labels = {
        "vocabulary_mismatch": "Vocabulary mismatch",
        "format_change":       "Format change",
        "structure_loss":      "Structure loss",
        "collapse":            "Field collapse",
        "uri_required":        "URI required",
    }

    # Collect all issues where this standard is the source, across all known targets
    seen: set = set()
    all_issues = []
    for tgt_id in groups:
        for v in get_value_issues(source_standard_id, tgt_id):
            key = (v.source_field, v.target_field, v.target_standard)
            if key not in seen and v.source_standard == source_standard_id:
                seen.add(key)
                all_issues.append(v)

    if not all_issues:
        return ""

    # Group by target standard
    by_target: dict = {}
    for v in all_issues:
        by_target.setdefault(v.target_standard, []).append(v)

    sections = []
    total = len(all_issues)

    for tgt_id, issues in by_target.items():
        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        tgt_domain = tgt.domain if tgt else ""
        dcol = domain_color.get(tgt_domain, "#495057")

        cards = []
        for v in issues:
            cfg = sev_cfg.get(v.severity, sev_cfg["lossy"])
            type_label = type_labels.get(v.issue_type, v.issue_type)

            # Example values table
            ex_html = ""
            if v.example_values:
                ex_rows = "".join(
                    f'<tr>'
                    f'<td style="padding:3px 8px;font-family:monospace;font-size:0.78rem;">{sv}</td>'
                    f'<td style="padding:3px 8px;font-family:monospace;font-size:0.78rem;">{tv if tv else "—"}</td>'
                    f'<td style="padding:3px 8px;font-size:0.75rem;color:#6c757d;">{note}</td>'
                    f'</tr>'
                    for sv, tv, note in v.example_values
                )
                ex_html = (
                    f'<div style="font-size:0.8rem;font-weight:600;color:#495057;margin-bottom:0.25rem;">'
                    f'Example conversions</div>'
                    f'<table style="width:100%;border-collapse:collapse;font-size:0.8rem;'
                    f'background:#fff;border:1px solid #dee2e6;border-radius:4px;margin-bottom:0.5rem;">'
                    f'<thead style="background:#f8f9fa;">'
                    f'<tr>'
                    f'<th style="padding:4px 8px;border-bottom:1px solid #dee2e6;">Source value</th>'
                    f'<th style="padding:4px 8px;border-bottom:1px solid #dee2e6;">Target value</th>'
                    f'<th style="padding:4px 8px;border-bottom:1px solid #dee2e6;">Note</th>'
                    f'</tr></thead>'
                    f'<tbody>{ex_rows}</tbody>'
                    f'</table>'
                )

            # Vocab side-by-side
            vocab_html = ""
            if v.source_vocab or v.target_vocab:
                sv_box = (f'<div style="flex:1;border:1px solid #dee2e6;border-radius:4px;'
                          f'padding:0.4rem 0.6rem;background:#fff;font-size:0.78rem;">'
                          f'<div style="font-size:0.72rem;color:#6c757d;margin-bottom:2px;">Source vocabulary</div>'
                          f'{v.source_vocab}</div>') if v.source_vocab else ""
                tv_box = (f'<div style="flex:1;border:1px solid #dee2e6;border-radius:4px;'
                          f'padding:0.4rem 0.6rem;background:#fff;font-size:0.78rem;">'
                          f'<div style="font-size:0.72rem;color:#6c757d;margin-bottom:2px;">Target vocabulary</div>'
                          f'{v.target_vocab}</div>') if v.target_vocab else ""
                vocab_html = f'<div style="display:flex;gap:0.5rem;margin-bottom:0.5rem;">{sv_box}{tv_box}</div>'

            # Transform spec
            ts_html = ""
            if v.transform_spec:
                ts_html = (f'<div style="margin-top:0.4rem;padding:0.4rem 0.6rem;border-radius:4px;'
                           f'background:#f8f9fa;border:1px solid #dee2e6;font-size:0.78rem;">'
                           f'<strong>&#128295; Transform:</strong> {v.transform_spec}</div>')

            cards.append(f"""
            <div style="border:1px solid {cfg['border']};border-left:4px solid {cfg['border']};
                        border-radius:6px;padding:0.75rem;margin-bottom:0.6rem;background:{cfg['bg']};">
              <div style="display:flex;flex-wrap:wrap;gap:0.4rem;align-items:center;margin-bottom:0.4rem;">
                <strong style="font-size:0.85rem;"><code>{v.source_field}</code> → <code>{v.target_field}</code></strong>
                <span style="{cfg['badge']}padding:1px 7px;border-radius:3px;font-size:0.72rem;">{cfg['label']}</span>
                <span style="background:#6c757d;color:#fff;padding:1px 7px;border-radius:3px;font-size:0.7rem;">{type_label}</span>
              </div>
              <div style="font-weight:600;font-size:0.83rem;color:{cfg['text']};margin-bottom:0.3rem;">{v.title}</div>
              <p style="font-size:0.8rem;color:#212529;margin-bottom:0.5rem;">{v.description}</p>
              {vocab_html}
              {ex_html}
              {ts_html}
            </div>""")

        sections.append(f"""
        <div class="mb-4">
          <div style="background:#f0f4ff;border-left:4px solid {dcol};padding:0.6rem 1rem;
                      border-radius:0 6px 6px 0;margin-bottom:0.75rem;
                      display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
            <strong style="color:{dcol};font-size:0.9rem;">{tgt_name}</strong>
            <span style="background:{dcol};color:#fff;padding:1px 6px;border-radius:3px;font-size:0.7rem;">{tgt_domain}</span>
            <span style="background:#6c757d;color:#fff;padding:1px 6px;border-radius:3px;font-size:0.72rem;">
              {len(issues)} value issue{'s' if len(issues) != 1 else ''}
            </span>
          </div>
          {''.join(cards)}
        </div>""")

    return f"""
  <div class="card mb-4" style="border-top:3px solid #fd7e14;">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center flex-wrap gap-2"
         data-bs-toggle="collapse" data-bs-target="#sec-valueissues"
         aria-expanded="false" aria-controls="sec-valueissues"
         style="cursor:pointer;user-select:none;">
      <h5 class="mb-0">&#9881; Value-level Compatibility
        <span class="badge ms-2" style="background:#fd7e14;color:#fff;font-size:0.75rem;">{total}</span>
      </h5>
      <span class="sec-chevron" style="font-size:0.9rem;color:#6c757d;transform:rotate(-90deg);transition:transform 0.2s;">&#9660;</span>
    </div>
    <div id="sec-valueissues" class="collapse">
      <div class="card-body">
        <p class="text-muted small mb-3">
          Structural field mappings may exist even when the <em>values</em> themselves are
          incompatible — different vocabularies, formats, or cardinality. These issues describe
          concrete value-level transformations required when converting from this standard.
          A field can map structurally but still cause data quality or validation failures if
          values are not transformed.
        </p>
        {''.join(sections)}
      </div>
    </div>
  </div>"""


# ---------------------------------------------------------------------------
# HTML report
# ---------------------------------------------------------------------------

def generate_html_report(standard_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a full-page HTML compatibility report for a given standard.
    Optionally includes analysis of a specific metadata record.
    """
    std = get_standard(standard_id)
    if std is None:
        return f"<p>Unknown standard: {standard_id}</p>"

    all_stds = get_all_standards()
    crosswalks = get_crosswalks_from(standard_id)
    matrix = build_compatibility_matrix()

    bar_fig = build_single_standard_coverage_fig(standard_id)
    bar_html = bar_fig.to_html(full_html=False, include_plotlyjs="cdn") if bar_fig else ""
    hmap_html = heatmap_html()

    # Build crosswalk table rows — grouped by target standard
    target_stds = [s for s in all_stds if s.id != standard_id]

    badge_class_map = {
        "exact": "badge bg-success",
        "similar": "badge bg-primary",
        "partial": "badge bg-warning text-dark",
        "none": "badge bg-secondary",
    }
    domain_color = {
        "NATO": "#003189", "EU": "#003399", "ISO": "#006633", "NIST": "#5c2d82",
    }

    # Group by target standard, preserving order
    from collections import OrderedDict
    groups: OrderedDict = OrderedDict()
    for entry in crosswalks:
        groups.setdefault(entry.target_standard, []).append(entry)

    xwalk_rows = []
    for tgt_id, entries in groups.items():
        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        tgt_domain = tgt.domain if tgt else ""
        score = matrix.get(standard_id, {}).get(tgt_id, 0.0)
        pct = round(score * 100, 1)
        bar_color = "#06d6a0" if pct >= 60 else "#3a86ff" if pct >= 30 else "#e63946"
        dcol = domain_color.get(tgt_domain, "#495057")
        mapped_count = sum(1 for e in entries if e.mapping_type != "none")

        # Group header row
        xwalk_rows.append(f"""
        <tr style="background:#f0f4ff; border-top:2px solid {dcol};">
          <td colspan="4" style="padding:0.6rem 0.75rem;">
            <div class="d-flex align-items-center gap-3 flex-wrap">
              <span style="font-weight:700; font-size:0.9rem; color:{dcol};">{tgt_name}</span>
              <span class="badge" style="background:{dcol};color:#fff;font-size:0.7rem;">{tgt_domain}</span>
              <span class="text-muted" style="font-size:0.8rem;">{mapped_count} of {len(entries)} fields mapped</span>
              <div class="progress flex-grow-1" style="height:8px;max-width:120px;">
                <div class="progress-bar" style="width:{max(int(pct),2)}%;background:{bar_color};"></div>
              </div>
              <span style="font-size:0.8rem;color:{bar_color};font-weight:600;">{pct}%</span>
            </div>
          </td>
          <td style="padding:0.6rem 0.75rem; text-align:right;">
            <a href="/report/{tgt_id}" class="btn btn-sm btn-outline-secondary py-0" style="font-size:0.75rem;">View report</a>
          </td>
        </tr>""")

        # Field rows for this target
        for entry in entries:
            bc = badge_class_map.get(entry.mapping_type, "badge bg-secondary")
            xwalk_rows.append(f"""
        <tr>
          <td style="padding-left:1.5rem;"><code>{entry.source_field}</code></td>
          <td style="color:#6c757d;font-size:0.82rem;">{entry.target_field or '—'}</td>
          <td><span class="{bc}">{entry.mapping_type}</span></td>
          <td colspan="2"><small class="text-muted">{entry.notes}</small></td>
        </tr>""")

    # Field value comparison cards — only for non-"none" mapped fields
    value_comparison_html = _build_value_comparison_html(std, groups, matrix, standard_id, domain_color)

    # Interoperability conflicts section
    conflicts_html = _build_conflicts_html(standard_id, groups, domain_color)

    # Value-level compatibility section
    value_issues_html = _build_value_issues_html(standard_id, groups, domain_color)

    # Mandatory fields table
    mand_rows = []
    for f in std.get_mandatory_fields():
        mand_rows.append(f"""
        <tr>
          <td><strong>{f.name}</strong></td>
          <td>{f.description[:200]}{'...' if len(f.description) > 200 else ''}</td>
          <td><code>{f.representation_term.value}</code></td>
          <td><small>{f.reference}</small></td>
        </tr>""")

    # Compatibility summary — split suite members from external standards
    from standards.suites import get_suites_for_standard

    my_suites = get_suites_for_standard(standard_id)
    suite_peer_ids = set()
    for s in my_suites:
        for m in s.members:
            if m.standard_id != standard_id:
                suite_peer_ids.add(m.standard_id)

    # Build a lookup: peer_id -> (suite, member)
    suite_peer_info = {}
    for s in my_suites:
        for m in s.members:
            if m.standard_id != standard_id:
                suite_peer_info[m.standard_id] = (s, m)

    rel_colors = {
        "anchor": "#003189", "requires": "#dc3545",
        "extends": "#0d6efd", "complements": "#198754",
    }
    rel_labels = {
        "anchor": "Anchor", "requires": "Must use together",
        "extends": "Extends / profiles", "complements": "Complements",
    }

    suite_cards = []
    for tgt in target_stds:
        if tgt.id not in suite_peer_info:
            continue
        suite, member = suite_peer_info[tgt.id]
        rcol = rel_colors.get(member.relationship, "#495057")
        rlabel = rel_labels.get(member.relationship, member.relationship)
        suite_cards.append(f"""
        <div style="border:1px solid {rcol};border-left:4px solid {rcol};
                    border-radius:6px;padding:0.65rem 0.85rem;background:#fff;
                    display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
          <div style="flex:1;min-width:180px;">
            <strong style="font-size:0.88rem;">{tgt.name}</strong>
            <span class="badge ms-2" style="background:{rcol};color:#fff;font-size:0.68rem;">{rlabel}</span>
            <div style="font-size:0.78rem;color:#6c757d;margin-top:0.15rem;">{member.role}</div>
          </div>
          <div style="display:flex;gap:0.5rem;flex-shrink:0;">
            <a href="/suite/{suite.id}" class="btn btn-sm btn-outline-secondary" style="font-size:0.75rem;">
              Suite: {suite.name}
            </a>
            <a href="/report/{tgt.id}" class="btn btn-sm btn-outline-secondary" style="font-size:0.75rem;">
              View report
            </a>
          </div>
        </div>""")

    suite_section = ""
    if suite_cards:
        suite_section = f"""
        <div class="mb-3">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span style="font-size:0.8rem;font-weight:600;text-transform:uppercase;
                         letter-spacing:0.05em;color:#6c757d;">Used in combination</span>
            <span class="badge bg-secondary">{len(suite_cards)}</span>
          </div>
          <div style="display:flex;flex-direction:column;gap:0.5rem;">
            {''.join(suite_cards)}
          </div>
        </div>
        <hr class="my-3">"""

    compat_rows = []
    for tgt in target_stds:
        if tgt.id in suite_peer_info:
            continue  # shown in suite section above

        score = matrix.get(standard_id, {}).get(tgt.id, 0.0)
        pct = round(score * 100, 1)
        bar_width = max(int(pct), 2)
        bar_color = "#06d6a0" if pct >= 60 else "#3a86ff" if pct >= 30 else "#e63946"

        conflicts = build_conflicts(standard_id, tgt.id)
        n_blocking = sum(1 for c in conflicts if c["severity"] == "blocking")
        n_lossy    = sum(1 for c in conflicts if c["severity"] == "lossy")
        n_transform= sum(1 for c in conflicts if c["severity"] == "transform_required")

        conflict_badges = ""
        if n_blocking:
            conflict_badges += (f'<span class="badge me-1" title="Conflicts that prevent full interoperability" '
                                f'style="background:#dc3545;color:#fff;">&#9940; {n_blocking} blocking</span>')
        if n_lossy:
            conflict_badges += (f'<span class="badge me-1" title="Conversion causes data loss" '
                                f'style="background:#ffc107;color:#664d03;">&#9888; {n_lossy} lossy</span>')
        if n_transform:
            conflict_badges += (f'<span class="badge me-1" title="Requires transformation step" '
                                f'style="background:#0dcaf0;color:#055160;">&#8635; {n_transform} transform</span>')
        if not conflicts:
            conflict_badges = '<span class="text-muted" style="font-size:0.8rem;">None identified</span>'

        compat_rows.append(f"""
        <tr>
          <td>{tgt.name}<br><small class="text-muted">{tgt.domain}</small></td>
          <td>
            <div class="progress" style="height:18px;min-width:80px;">
              <div class="progress-bar" role="progressbar"
                   style="width:{bar_width}%; background-color:{bar_color};">
                {pct}%
              </div>
            </div>
          </td>
          <td>{conflict_badges}</td>
          <td><a href="/report/{tgt.id}" class="btn btn-sm btn-outline-secondary">View</a></td>
        </tr>""")

    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Metadata analysis section
    meta_section = ""
    if metadata:
        from engine.detector import get_field_analysis
        analysis = get_field_analysis(metadata, standard_id)
        pf_rows = "".join(f"""
        <tr>
          <td><code>{pf['name']}</code></td>
          <td><span class="badge bg-info text-dark">{pf['obligation']}</span></td>
          <td><code>{pf['value'][:100]}</code></td>
          <td>{pf['layer']}/{pf['group'] or '—'}</td>
        </tr>""" for pf in analysis.get("present_fields", []))
        mm_rows = "".join(f"""
        <tr class="table-danger">
          <td><code>{mf['name']}</code></td>
          <td><small>{mf['description'][:150]}</small></td>
          <td><small>{mf['reference']}</small></td>
        </tr>""" for mf in analysis.get("missing_mandatory", []))
        meta_section = f"""
        <div class="card mb-4">
          <div class="card-header"><h5>Metadata Record Analysis</h5></div>
          <div class="card-body">
            <h6>Present Fields ({len(analysis.get('present_fields', []))})</h6>
            <div class="table-responsive">
            <table class="table table-sm table-striped">
              <thead><tr><th>Field</th><th>Obligation</th><th>Value (truncated)</th><th>Layer/Group</th></tr></thead>
              <tbody>{pf_rows}</tbody>
            </table>
            </div>
            <h6 class="mt-3">Missing Mandatory Fields ({len(analysis.get('missing_mandatory', []))})</h6>
            <div class="table-responsive">
            <table class="table table-sm table-danger">
              <thead><tr><th>Field</th><th>Description</th><th>Reference</th></tr></thead>
              <tbody>{mm_rows if mm_rows else '<tr><td colspan="3" class="text-success">All mandatory fields present</td></tr>'}</tbody>
            </table>
            </div>
          </div>
        </div>"""

    # Build per-pair sources summary for this standard
    all_pair_sources_html = []
    for other in target_stds:
        srcs = get_pair_sources(standard_id, other.id)
        if not srcs:
            continue
        basis_vals = [s.basis for s in srcs]
        has_norm = "normative" in basis_vals
        has_pub  = "published" in basis_vals
        badge_col   = "#198754" if has_norm else ("#0d6efd" if has_pub else "#6c757d")
        badge_label = "Normative" if has_norm else ("Published" if has_pub else "Assessment")
        def _src_item(s, col):
            b_label = "Normative" if s.basis == "normative" else ("Published" if s.basis == "published" else "Assessment")
            sec_div = (f'<div style="font-size:0.75rem;color:#6c757d;">Sections: {s.sections}</div>'
                       if s.sections else "")
            link = (f'<a href="{s.url}" target="_blank" rel="noopener" style="font-size:0.82rem;">{s.title}</a>'
                    if s.url else f'<span style="font-size:0.82rem;">{s.title}</span>')
            return (f'<li class="mb-1">{link}'
                    f'<span class="badge ms-2" style="background:{col};color:#fff;font-size:0.65rem;">{b_label}</span>'
                    f'<div style="font-size:0.78rem;color:#6c757d;">{s.description}</div>'
                    f'{sec_div}</li>')

        src_items = "".join(_src_item(s, badge_col) for s in srcs)
        dcol = domain_color.get(other.domain, "#495057")
        all_pair_sources_html.append(f"""
        <div class="mb-3">
          <div style="background:#f0f4ff;border-left:4px solid {dcol};padding:0.5rem 1rem;
                      border-radius:0 6px 6px 0;margin-bottom:0.5rem;">
            <strong style="color:{dcol};font-size:0.88rem;">{other.name}</strong>
            <span class="badge ms-2" style="background:{badge_col};color:#fff;font-size:0.68rem;">{badge_label}</span>
          </div>
          <ul class="mb-0 ps-3">{src_items}</ul>
        </div>""")

    sources_section = ""
    if all_pair_sources_html:
        sources_section = f"""
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-sources"
         aria-expanded="false" aria-controls="sec-sources"
         style="cursor:pointer;user-select:none;">
      <h5 class="mb-0">&#128214; Sources &amp; Verification</h5>
      <span class="sec-chevron" style="font-size:0.9rem;color:#6c757d;transform:rotate(-90deg);transition:transform 0.2s;">&#9660;</span>
    </div>
    <div id="sec-sources" class="collapse">
      <div class="card-body">
        <p class="text-muted small mb-3">
          Evidence basis for the crosswalk assessments in this report.
          <strong style="color:#198754;">Normative</strong> = defined by the standard itself.
          <strong style="color:#0d6efd;">Published</strong> = authoritative body crosswalk document.
          <strong style="color:#6c757d;">Assessment</strong> = our semantic analysis; no public crosswalk exists.
        </p>
        {''.join(all_pair_sources_html)}
      </div>
    </div>
  </div>"""

    html = f"""<div class="report-body pb-4">

  <!-- Description — open by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-description"
         aria-expanded="true" aria-controls="sec-description">
      <h5 class="mb-0">Standard Description</h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-description" class="collapse show">
      <div class="card-body"><p class="mb-0">{std.description}</p></div>
    </div>
  </div>

  {sources_section}

  {meta_section}

  <!-- Compatibility Summary — open by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-compat"
         aria-expanded="true" aria-controls="sec-compat">
      <h5 class="mb-0">Compatibility with Other Standards</h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-compat" class="collapse show">
      <div class="card-body">
        {suite_section}
        {'<p class="text-muted small mb-2">Field-level crosswalk coverage and known conflicts against external standards.</p>' if suite_section else ''}
        <div class="table-responsive">
        <table class="table table-sm table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>Target Standard</th>
              <th style="min-width:130px;">Field Coverage</th>
              <th>Conflicts</th>
              <th>Report</th>
            </tr>
          </thead>
          <tbody>{''.join(compat_rows) if compat_rows else '<tr><td colspan="4" class="text-muted">No external standards to compare</td></tr>'}</tbody>
        </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Bar chart — open by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-barchart"
         aria-expanded="true" aria-controls="sec-barchart">
      <h5 class="mb-0">Field Coverage Chart</h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-barchart" class="collapse show">
      <div class="card-body">{bar_html}</div>
    </div>
  </div>

  <!-- Mandatory Fields — collapsed by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-mandatory"
         aria-expanded="false" aria-controls="sec-mandatory">
      <h5 class="mb-0">Mandatory Fields <span class="badge bg-secondary ms-2" style="font-size:0.75rem;">{len(std.get_mandatory_fields())}</span></h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-mandatory" class="collapse">
      <div class="card-body">
        <div class="table-responsive">
        <table class="table table-sm table-striped table-hover">
          <thead class="table-dark">
            <tr><th>Field Name</th><th>Description</th><th>Type</th><th>Reference</th></tr>
          </thead>
          <tbody>{''.join(mand_rows) if mand_rows else '<tr><td colspan="4">No mandatory fields defined</td></tr>'}</tbody>
        </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Crosswalk table — collapsed by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-crosswalk"
         aria-expanded="false" aria-controls="sec-crosswalk">
      <h5 class="mb-0">Detailed Crosswalk Mappings
        <span class="badge bg-secondary ms-2" style="font-size:0.75rem;">{len(crosswalks)} across {len(groups)} standards</span>
      </h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-crosswalk" class="collapse">
      <div class="card-body p-0">
        <div class="table-responsive">
        <table class="table table-sm table-hover mb-0" style="border-collapse:collapse;">
          <thead class="table-dark">
            <tr>
              <th style="width:26%">Source Field</th>
              <th style="width:22%">Target Field</th>
              <th style="width:12%">Mapping</th>
              <th colspan="2">Notes</th>
            </tr>
          </thead>
          <tbody>{''.join(xwalk_rows) if xwalk_rows else '<tr><td colspan="5">No crosswalk mappings defined</td></tr>'}</tbody>
        </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Field Value Comparison — collapsed by default -->
  {value_comparison_html}

  <!-- Interoperability Conflicts — open by default -->
  {conflicts_html}

  <!-- Value-level Compatibility — collapsed by default -->
  {value_issues_html}

  <!-- Full Compatibility Heatmap — collapsed by default -->
  <div class="card mb-4">
    <div class="card-header sec-toggle d-flex justify-content-between align-items-center"
         data-bs-toggle="collapse" data-bs-target="#sec-heatmap"
         aria-expanded="false" aria-controls="sec-heatmap">
      <h5 class="mb-0">Full Compatibility Matrix Heatmap</h5>
      <span class="sec-chevron">&#9660;</span>
    </div>
    <div id="sec-heatmap" class="collapse">
      <div class="card-body">{hmap_html}</div>
    </div>
  </div>

  <footer class="text-center text-muted mt-4 pt-3 border-top">
    <small>NATO Metadata Standards Comparison Tool &mdash;
    ADatP-5636 Ed.A V1 | Dublin Core | DCAT-AP | ISO 19115 | ISO 23081 | NIST SP 800-60/53</small>
  </footer>
</div>"""
    return html


# ---------------------------------------------------------------------------
# PDF report with ReportLab
# ---------------------------------------------------------------------------

def generate_pdf_report(standard_id: str, metadata: Optional[Dict[str, Any]] = None) -> bytes:
    """Generate a PDF report using ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, PageBreak,
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    std = get_standard(standard_id)
    if std is None:
        return b""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Compatibility Report — {std.name}",
    )

    styles = getSampleStyleSheet()
    NATO_BLUE = colors.HexColor("#1a1a2e")
    LIGHT_BLUE = colors.HexColor("#3a86ff")
    GREEN = colors.HexColor("#06d6a0")
    YELLOW = colors.HexColor("#ffbe0b")
    RED = colors.HexColor("#e63946")
    GREY = colors.HexColor("#6c757d")

    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=20, textColor=NATO_BLUE, spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=11, textColor=GREY, spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"],
        fontSize=13, textColor=NATO_BLUE, spaceBefore=16, spaceAfter=6,
    )
    h3_style = ParagraphStyle(
        "H3", parent=styles["Heading3"],
        fontSize=10, textColor=NATO_BLUE, spaceBefore=8, spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=9, spaceAfter=4, leading=14,
    )
    code_style = ParagraphStyle(
        "Code",
        fontSize=8, spaceAfter=3, fontName="Courier",
        leftIndent=0, rightIndent=0, firstLineIndent=0, leading=10,
    )
    caption_style = ParagraphStyle(
        "Caption", parent=styles["Normal"],
        fontSize=8, textColor=GREY,
    )

    story = []

    # Header
    story.append(Paragraph(f"Compatibility Report", title_style))
    story.append(Paragraph(f"{std.full_name}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NATO_BLUE))
    story.append(Spacer(1, 0.3 * cm))

    # Metadata block
    meta_data = [
        ["Standard:", std.name],
        ["Full Name:", std.full_name],
        ["Version:", std.version],
        ["Organization:", std.organization],
        ["Domain:", std.domain],
        ["Reference:", std.reference],
        ["Report Date:", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")],
    ]
    meta_table = Table(meta_data, colWidths=[3.5 * cm, 13 * cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), NATO_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.5 * cm))

    from standards.suites import get_suites_for_standard

    BLOCKING = colors.HexColor("#dc3545")
    LOSSY    = colors.HexColor("#e8a000")   # amber, readable on white
    TRANSFORM= colors.HexColor("#0077aa")   # darker cyan, readable on white
    BLOCKING_BG  = colors.HexColor("#fde8ea")
    LOSSY_BG     = colors.HexColor("#fff8e1")
    TRANSFORM_BG = colors.HexColor("#e0f4fb")

    severity_color = {"blocking": BLOCKING, "lossy": LOSSY, "transform_required": TRANSFORM}
    severity_bg    = {"blocking": BLOCKING_BG, "lossy": LOSSY_BG, "transform_required": TRANSFORM_BG}
    severity_label = {"blocking": "Blocking", "lossy": "Data loss", "transform_required": "Transform req."}
    type_label_pdf = {
        "mandatory_gap": "Mandatory gap", "vocabulary": "Vocabulary",
        "obligation_inversion": "Obligation inv.", "structural": "Structural",
        "domain_mismatch": "Domain mismatch",
    }

    tbl_style_base = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NATO_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ])

    # ── Description ──────────────────────────────────────────────────────────
    story.append(Paragraph("Description", h2_style))
    story.append(Paragraph(std.description, body_style))
    story.append(Spacer(1, 0.3 * cm))

    # ── Sources & Verification ────────────────────────────────────────────────
    all_stds_for_sources = get_all_standards()
    basis_color = {"normative": GREEN, "published": LIGHT_BLUE, "assessed": GREY}
    basis_label = {"normative": "Normative", "published": "Published crosswalk",
                   "assessed": "Author assessment"}

    src_rows_pdf = []
    for other in all_stds_for_sources:
        if other.id == standard_id:
            continue
        pair_srcs = get_pair_sources(standard_id, other.id)
        if not pair_srcs:
            continue
        for s in pair_srcs:
            bc = basis_color.get(s.basis, GREY)
            bl = basis_label.get(s.basis, s.basis)
            src_rows_pdf.append([
                Paragraph(other.name, body_style),
                Paragraph(
                    f"<font color='{bc.hexval()}'><b>{bl}</b></font>",
                    caption_style,
                ),
                Paragraph(
                    f"<b>{s.title}</b><br/>{s.description}"
                    + (f"<br/><i>Sections: {s.sections}</i>" if s.sections else ""),
                    caption_style,
                ),
            ])

    if src_rows_pdf:
        story.append(Paragraph("Sources & Verification", h2_style))
        story.append(Paragraph(
            "Evidence basis for the crosswalk assessments in this report. "
            "Normative = defined by the standard itself. "
            "Published = authoritative crosswalk document. "
            "Author assessment = semantic analysis; no public crosswalk exists.",
            body_style,
        ))
        story.append(Spacer(1, 0.2 * cm))
        src_table = Table(
            [["Against standard", "Basis", "Source / Notes"]] + src_rows_pdf,
            colWidths=[3.5 * cm, 3 * cm, 10 * cm],
            repeatRows=1,   # repeat header on each page if table spans pages
            splitByRow=True, # allow rows to split across page breaks
        )
        src_table.setStyle(tbl_style_base)
        story.append(src_table)
        story.append(Spacer(1, 0.3 * cm))

    # ── Suite membership ─────────────────────────────────────────────────────
    my_suites = get_suites_for_standard(standard_id)
    if my_suites:
        story.append(Paragraph("Suite Membership", h2_style))
        story.append(Paragraph(
            "This standard is part of one or more suites and is designed to be used "
            "in combination with the following standards.",
            body_style,
        ))
        story.append(Spacer(1, 0.2 * cm))
        for suite in my_suites:
            suite_hdr_style = ParagraphStyle(
                f"SuiteHdr_{suite.id}", parent=styles["Normal"],
                fontSize=9, fontName="Helvetica-Bold",
                textColor=colors.HexColor(suite.color),
                spaceBefore=6, spaceAfter=3,
            )
            story.append(Paragraph(suite.name, suite_hdr_style))
            suite_data = [["Standard", "Relationship", "Role in suite"]]
            for m in suite.members:
                peer = get_standard(m.standard_id)
                peer_name = peer.name if peer else m.standard_id
                marker = ">> " if m.standard_id == standard_id else ""
                suite_data.append([
                    Paragraph(f"{marker}<b>{peer_name}</b>" if m.standard_id == standard_id
                              else peer_name, body_style),
                    m.relationship,
                    Paragraph(m.role, caption_style),
                ])
            st = Table(suite_data, colWidths=[3.5 * cm, 2.5 * cm, 10.5 * cm])
            st.setStyle(tbl_style_base)
            story.append(st)
        story.append(Spacer(1, 0.3 * cm))

    # ── Mandatory fields ─────────────────────────────────────────────────────
    story.append(Paragraph(f"Mandatory Fields ({len(std.get_mandatory_fields())})", h2_style))
    mand_rows_pdf = [["Field Name", "Description", "Type", "Reference"]]
    for f in std.get_mandatory_fields():
        mand_rows_pdf.append([
            Paragraph(f"<b>{f.name}</b>", code_style),
            Paragraph(f.description[:200], body_style),
            Paragraph(f.representation_term.value, caption_style),
            Paragraph(f.reference, caption_style),
        ])
    if len(mand_rows_pdf) > 1:
        mt = Table(mand_rows_pdf, colWidths=[4 * cm, 7 * cm, 2.5 * cm, 3 * cm])
        mt.setStyle(tbl_style_base)
        story.append(mt)
    story.append(Spacer(1, 0.3 * cm))

    # ── Compatibility summary ─────────────────────────────────────────────────
    story.append(Paragraph("Compatibility with Other Standards", h2_style))
    matrix = build_compatibility_matrix()
    all_stds = get_all_standards()

    suite_peer_ids = {
        m.standard_id
        for s in my_suites
        for m in s.members
        if m.standard_id != standard_id
    }

    # Suite peers sub-section
    if suite_peer_ids:
        story.append(Paragraph("Used in combination (same suite)", h3_style
                               if 'h3_style' in dir() else body_style))
        suite_peer_data = [["Standard", "Relationship", "Role"]]
        for s in my_suites:
            for m in s.members:
                if m.standard_id == standard_id:
                    continue
                peer = get_standard(m.standard_id)
                rel_color = {"requires": BLOCKING, "extends": LIGHT_BLUE,
                             "complements": GREEN, "anchor": NATO_BLUE}.get(m.relationship, GREY)
                suite_peer_data.append([
                    peer.name if peer else m.standard_id,
                    Paragraph(f"<font color='{rel_color.hexval()}'><b>{m.relationship}</b></font>",
                              body_style),
                    Paragraph(m.role, caption_style),
                ])
        spt = Table(suite_peer_data, colWidths=[4 * cm, 2.5 * cm, 10 * cm])
        spt.setStyle(tbl_style_base)
        story.append(spt)
        story.append(Spacer(1, 0.2 * cm))

    # External standards table
    story.append(Paragraph("Crosswalk compatibility with external standards", caption_style))
    story.append(Spacer(1, 0.1 * cm))
    compat_rows_pdf = [["Target Standard", "Domain", "Coverage", "Conflicts"]]
    for tgt in all_stds:
        if tgt.id == standard_id or tgt.id in suite_peer_ids:
            continue
        score = matrix.get(standard_id, {}).get(tgt.id, 0.0)
        pct = round(score * 100, 1)
        q_color = GREEN if pct >= 60 else YELLOW if pct >= 30 else RED

        conflicts = build_conflicts(standard_id, tgt.id)
        n_bl = sum(1 for c in conflicts if c["severity"] == "blocking")
        n_lo = sum(1 for c in conflicts if c["severity"] == "lossy")
        n_tr = sum(1 for c in conflicts if c["severity"] == "transform_required")
        conflict_parts = []
        if n_bl: conflict_parts.append(
            f"<font color='{BLOCKING.hexval()}'>{n_bl} blocking</font>")
        if n_lo: conflict_parts.append(
            f"<font color='{LOSSY.hexval()}'>{n_lo} lossy</font>")
        if n_tr: conflict_parts.append(
            f"<font color='{TRANSFORM.hexval()}'>{n_tr} transform</font>")
        conflict_cell = Paragraph(", ".join(conflict_parts) if conflict_parts else "None", body_style)

        compat_rows_pdf.append([
            tgt.name,
            tgt.domain,
            Paragraph(f"<font color='{q_color.hexval()}'><b>{pct}%</b></font>", body_style),
            conflict_cell,
        ])

    ct = Table(compat_rows_pdf, colWidths=[5.5 * cm, 2 * cm, 2 * cm, 7 * cm])
    ct.setStyle(tbl_style_base)
    story.append(ct)
    story.append(Spacer(1, 0.3 * cm))

    # ── Crosswalk mappings ────────────────────────────────────────────────────
    story.append(PageBreak())
    crosswalks = get_crosswalks_from(standard_id)
    story.append(Paragraph(f"Detailed Crosswalk Mappings ({len(crosswalks)})", h2_style))
    story.append(Paragraph(
        "Grouped by target standard. Mapping types: exact (green), similar (blue), "
        "partial (amber), none (grey).",
        caption_style,
    ))
    story.append(Spacer(1, 0.2 * cm))

    from collections import OrderedDict as _OD
    cw_groups: _OD = _OD()
    for e in crosswalks:
        cw_groups.setdefault(e.target_standard, []).append(e)

    type_colors_pdf = {"exact": GREEN, "similar": LIGHT_BLUE, "partial": YELLOW, "none": GREY}

    for tgt_id, entries in cw_groups.items():
        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        # Target standard subheader
        story.append(Paragraph(tgt_name, ParagraphStyle(
            f"tgt_{tgt_id}", parent=styles["Normal"],
            fontSize=8, fontName="Helvetica-Bold", textColor=NATO_BLUE,
            spaceBefore=8, spaceAfter=2,
        )))
        cw_data = [["Source Field", "Target Field", "Type", "Notes"]]
        for e in entries:
            tc = type_colors_pdf.get(e.mapping_type, GREY)
            cw_data.append([
                Paragraph(f"<b>{e.source_field}</b>", code_style),
                Paragraph(e.target_field or "—", code_style),
                Paragraph(f"<font color='{tc.hexval()}'>{e.mapping_type}</font>", body_style),
                Paragraph(e.notes[:140] if e.notes else "", caption_style),
            ])
        cw_table = Table(cw_data, colWidths=[3.5 * cm, 3 * cm, 1.8 * cm, 8.2 * cm])
        cw_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaf6")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(cw_table)
    story.append(Spacer(1, 0.3 * cm))

    # ── Field value comparison ────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Field Value Comparison", h2_style))
    story.append(Paragraph(
        "Side-by-side comparison of type, cardinality, and allowed values for fields "
        "that have a defined (non-none) crosswalk mapping.",
        body_style,
    ))
    story.append(Spacer(1, 0.2 * cm))

    for tgt_id, entries in cw_groups.items():
        mapped = [e for e in entries if e.mapping_type != "none"]
        if not mapped:
            continue
        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        story.append(Paragraph(tgt_name, ParagraphStyle(
            f"vc_{tgt_id}", parent=styles["Normal"],
            fontSize=9, fontName="Helvetica-Bold", textColor=NATO_BLUE,
            spaceBefore=10, spaceAfter=3,
        )))
        vc_data = [["Source field", "Src type", "Src values",
                    "Target field", "Tgt type", "Tgt values", "Notes"]]
        for e in mapped:
            sf = std.fields.get(e.source_field)
            tf = tgt.fields.get(e.target_field) if (tgt and e.target_field) else None
            src_type = sf.representation_term.value if sf else "—"
            tgt_type = tf.representation_term.value if tf else "—"
            src_card = sf.cardinality.value if sf else ""
            tgt_card = tf.cardinality.value if tf else ""
            src_vals = (sf.values[:80] if sf and sf.values else "")
            tgt_vals = (tf.values[:80] if tf and tf.values else "")
            # Flag mismatches in the type cell
            type_mismatch = (sf and tf and sf.representation_term != tf.representation_term)
            card_mismatch  = (sf and tf and sf.cardinality != tf.cardinality)
            src_type_cell = Paragraph(
                f"<font color='{RED.hexval() if type_mismatch else colors.black.hexval()}'>"
                f"{src_type}</font><br/><font size='6' color='grey'>{src_card}</font>",
                caption_style,
            )
            tgt_type_cell = Paragraph(
                f"<font color='{RED.hexval() if type_mismatch else colors.black.hexval()}'>"
                f"{tgt_type}</font><br/><font size='6' color='{RED.hexval() if card_mismatch else 'grey'}'>"
                f"{tgt_card}</font>",
                caption_style,
            )
            vc_data.append([
                Paragraph(f"<b>{e.source_field}</b>", code_style),
                src_type_cell,
                Paragraph(src_vals, caption_style),
                Paragraph(e.target_field or "—", code_style),
                tgt_type_cell,
                Paragraph(tgt_vals, caption_style),
                Paragraph(e.notes[:100] if e.notes else "", caption_style),
            ])
        vc_table = Table(vc_data, colWidths=[2.8*cm, 1.6*cm, 2.6*cm, 2.8*cm, 1.6*cm, 2.6*cm, 2.5*cm])
        vc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaf6")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            # Vertical divider between source and target halves
            ("LINEAFTER", (2, 0), (2, -1), 1, colors.HexColor("#aaaacc")),
        ]))
        story.append(vc_table)

    # ── Interoperability conflicts ─────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Interoperability Conflicts", h2_style))

    sev_legend_data = [
        [
            Paragraph("<b>Blocking</b>", ParagraphStyle(
                "SevHdr1", parent=styles["Normal"], fontSize=8,
                textColor=BLOCKING, fontName="Helvetica-Bold")),
            Paragraph("<b>Lossy</b>", ParagraphStyle(
                "SevHdr2", parent=styles["Normal"], fontSize=8,
                textColor=LOSSY, fontName="Helvetica-Bold")),
            Paragraph("<b>Transform required</b>", ParagraphStyle(
                "SevHdr3", parent=styles["Normal"], fontSize=8,
                textColor=TRANSFORM, fontName="Helvetica-Bold")),
        ],
        [
            Paragraph(
                "A conformant source record cannot be made fully conformant in the "
                "target without discarding a mandatory field or fabricating a value. "
                "The receiver may parse the file but it will fail target validation.",
                caption_style),
            Paragraph(
                "Conversion is possible and the record will pass target validation, "
                "but some information is permanently degraded — e.g. a structured "
                "PointOfContact flattened to free text.",
                caption_style),
            Paragraph(
                "Fully interoperable once a specific, well-defined transformation "
                "is applied (e.g. vocabulary mapping, date format conversion). "
                "No information is permanently lost.",
                caption_style),
        ],
    ]
    sev_table = Table(sev_legend_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    sev_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#fde8ea")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#fff8e1")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#e0f4fb")),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(sev_table)
    story.append(Spacer(1, 0.3 * cm))

    any_conflicts = False
    for tgt_id in cw_groups:
        conflicts = build_conflicts(standard_id, tgt_id)
        if not conflicts:
            continue
        any_conflicts = True
        tgt = get_standard(tgt_id)
        tgt_name = tgt.name if tgt else tgt_id
        story.append(Paragraph(tgt_name, ParagraphStyle(
            f"cf_{tgt_id}", parent=styles["Normal"],
            fontSize=9, fontName="Helvetica-Bold", textColor=NATO_BLUE,
            spaceBefore=10, spaceAfter=3,
        )))
        cf_data = [["Severity", "Type", "Title", "Description"]]
        for c in conflicts:
            sev_col  = severity_color.get(c["severity"], GREY)
            sev_lbl  = severity_label.get(c["severity"], c["severity"])
            type_lbl = type_label_pdf.get(c["conflict_type"], c["conflict_type"])
            cf_data.append([
                Paragraph(f"<font color='{sev_col.hexval()}'><b>{sev_lbl}</b></font>", caption_style),
                Paragraph(type_lbl, caption_style),
                Paragraph(c["title"], body_style),
                Paragraph(c["description"][:250], caption_style),
            ])
        cf_table = Table(cf_data, colWidths=[2.2*cm, 2.5*cm, 4.8*cm, 7*cm])
        # Row-level background tinting by severity
        cf_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaf6")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
        for i, c in enumerate(conflicts, start=1):
            bg = severity_bg.get(c["severity"], colors.white)
            cf_style.add("BACKGROUND", (0, i), (-1, i), bg)
        cf_table.setStyle(cf_style)
        story.append(cf_table)

    if not any_conflicts:
        story.append(Paragraph("No interoperability conflicts identified.", caption_style))

    # ── Value-level compatibility ──────────────────────────────────────────────
    _vi_domain_colors = {
        "NATO": "#003189", "EU": "#003399", "ISO": "#006633", "NIST": "#5c2d82",
    }
    value_issues_by_tgt: dict = {}
    for tgt_id in cw_groups:
        for vi in get_value_issues(standard_id, tgt_id):
            if vi.source_standard == standard_id:
                value_issues_by_tgt.setdefault(tgt_id, []).append(vi)

    if value_issues_by_tgt:
        story.append(PageBreak())
        story.append(Paragraph("Value-level Compatibility", h2_style))
        story.append(Paragraph(
            "These issues describe concrete value-level transformations required when converting "
            "from this standard. A field can map structurally but still cause data quality or "
            "validation failures if values are not transformed.",
            body_style,
        ))
        story.append(Spacer(1, 0.2 * cm))

        vi_type_labels = {
            "vocabulary_mismatch": "Vocabulary mismatch",
            "format_change":       "Format change",
            "structure_loss":      "Structure loss",
            "collapse":            "Field collapse",
            "uri_required":        "URI required",
        }
        vi_sev_colors = {
            "blocking":           colors.HexColor("#dc3545"),
            "lossy":              colors.HexColor("#ffc107"),
            "transform_required": colors.HexColor("#0dcaf0"),
        }

        for tgt_id, vi_list in value_issues_by_tgt.items():
            tgt_obj = get_standard(tgt_id)
            tgt_name_vi = tgt_obj.name if tgt_obj else tgt_id
            tgt_domain_vi = tgt_obj.domain if tgt_obj else ""
            dcol_vi = colors.HexColor(_vi_domain_colors.get(tgt_domain_vi, "#495057"))

            story.append(Paragraph(tgt_name_vi, ParagraphStyle(
                "TgtHead", parent=styles["Normal"],
                fontSize=10, textColor=dcol_vi, fontName="Helvetica-Bold",
                spaceBefore=10, spaceAfter=4,
            )))

            vi_data = [[
                Paragraph("<b>Source field → Target field</b>", caption_style),
                Paragraph("<b>Severity</b>", caption_style),
                Paragraph("<b>Type</b>", caption_style),
                Paragraph("<b>Title &amp; Description</b>", caption_style),
            ]]
            vi_bg_map = {}
            vi_sev_bg = {
                "blocking":           colors.HexColor("#fde8ea"),
                "lossy":              colors.HexColor("#fff3cd"),
                "transform_required": colors.HexColor("#cff4fc"),
            }
            for row_i, vi in enumerate(vi_list, start=1):
                sev_col = vi_sev_colors.get(vi.severity, GREY)
                sev_lbl = vi.severity.replace("_", " ").title()
                type_lbl = vi_type_labels.get(vi.issue_type, vi.issue_type)
                fields_cell = Paragraph(
                    f"<font name='Courier'>{vi.source_field}</font>"
                    f" → <font name='Courier'>{vi.target_field}</font>",
                    code_style,
                )
                title_desc = Paragraph(
                    f"<b>{vi.title}</b><br/>{vi.description[:220]}",
                    body_style,
                )
                vi_data.append([
                    fields_cell,
                    Paragraph(f"<font color='{sev_col.hexval()}'><b>{sev_lbl}</b></font>", caption_style),
                    Paragraph(type_lbl, caption_style),
                    title_desc,
                ])
                vi_bg_map[row_i] = vi_sev_bg.get(vi.severity, colors.white)

            vi_table = Table(vi_data, colWidths=[4.5 * cm, 2.5 * cm, 3 * cm, None],
                             repeatRows=1, splitByRow=True)
            vi_style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
                ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                ("FONTSIZE",   (0, 0), (-1, 0), 8),
                ("FONTSIZE",   (0, 1), (-1, -1), 8),
                ("VALIGN",     (0, 0), (-1, -1), "TOP"),
                ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#dee2e6")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white]),
                ("LEFTPADDING",  (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING",   (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
            for row_i, bg in vi_bg_map.items():
                vi_style.add("BACKGROUND", (0, row_i), (-1, row_i), bg)
            vi_table.setStyle(vi_style)
            story.append(vi_table)
            story.append(Spacer(1, 0.3 * cm))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GREY))
    story.append(Paragraph(
        "NATO Metadata Standards Comparison Tool — "
        "ADatP-5636 Ed.A V1 | Dublin Core | DCAT-AP | ISO 19115 | ISO 23081 | NIST SP 800-60/53",
        caption_style,
    ))

    doc.build(story)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes
