"""
Standard Suites — groups of metadata standards that work together.

Relationship types:
  requires     — the member MUST be used for the suite anchor to function correctly
                 (e.g. ADatP-4774 is required by ADatP-5636 for its Security Layer)
  extends      — the member is an application profile of or formally derived from
                 the anchor (e.g. DCAT-AP extends Dublin Core)
  complements  — commonly used alongside; neither requires the other but they
                 cover complementary concerns (e.g. ISO 23081 complements ISO 19115)
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SuiteMember:
    standard_id: str
    relationship: str          # "requires" | "extends" | "complements" | "anchor"
    role: str                  # one-sentence description of the role in the suite
    optional: bool = False     # True if the member can be omitted in some deployments


@dataclass
class StandardSuite:
    id: str
    name: str
    description: str
    anchor_id: str             # the primary / most important standard in the suite
    members: List[SuiteMember] = field(default_factory=list)
    color: str = "#003189"     # display colour (hex)

    def get_member(self, standard_id: str) -> Optional[SuiteMember]:
        for m in self.members:
            if m.standard_id == standard_id:
                return m
        return None

    def get_all_ids(self) -> List[str]:
        return [m.standard_id for m in self.members]

    def get_required_ids(self) -> List[str]:
        return [m.standard_id for m in self.members
                if m.relationship in ("anchor", "requires")]

    def get_by_relationship(self, rel: str) -> List[SuiteMember]:
        return [m for m in self.members if m.relationship == rel]


# ---------------------------------------------------------------------------
# Suite definitions
# ---------------------------------------------------------------------------

SUITES: List[StandardSuite] = [

    StandardSuite(
        id="nato_metadata_infrastructure",
        name="NATO Metadata Infrastructure",
        description=(
            "The three interlocking NATO standards that together provide a complete, "
            "secure metadata infrastructure. ADatP-5636 defines the core metadata "
            "elements across three layers (Security, Common, Information Lifecycle). "
            "Its Security Layer references confidentiality labels whose syntax is "
            "normatively defined in ADatP-4774 — without 4774, the mandatory "
            "originatorConfidentialityLabel and metadataConfidentialityLabel fields "
            "cannot be correctly populated. ADatP-4778 provides the cryptographic "
            "binding mechanism that ties the metadata record to its data object, "
            "ensuring integrity and non-repudiation. All three must be implemented "
            "together for a fully conformant NATO metadata solution."
        ),
        anchor_id="adatp5636",
        color="#003189",
        members=[
            SuiteMember(
                standard_id="adatp5636",
                relationship="anchor",
                role="Core metadata element set — defines all descriptive, administrative, "
                     "and lifecycle metadata fields.",
            ),
            SuiteMember(
                standard_id="adatp4774",
                relationship="requires",
                role="Confidentiality label syntax — normatively defines the structure of "
                     "the ConfidentialityLabel values used by ADatP-5636's mandatory "
                     "Security Layer fields (originatorConfidentialityLabel, "
                     "metadataConfidentialityLabel, alternativeConfidentialityLabel).",
            ),
            SuiteMember(
                standard_id="adatp4778",
                relationship="requires",
                role="Metadata binding mechanism — cryptographically binds the ADatP-5636 "
                     "metadata record to its data object using XML Signature/Encryption, "
                     "ensuring integrity and enabling non-repudiation.",
            ),
        ],
    ),

    StandardSuite(
        id="eu_data_catalogue",
        name="EU Data Catalogue Profile",
        description=(
            "The EU's layered approach to data catalogue metadata. Dublin Core / "
            "ISO 15836 provides the foundational 15-element vocabulary that underpins "
            "virtually all general metadata standards. DCAT-AP is the EU Application "
            "Profile of W3C DCAT, which itself reuses Dublin Core Terms extensively — "
            "understanding Dublin Core is prerequisite to working with DCAT-AP. "
            "DCAT-AP is mandatory for datasets published on the EU Open Data Portal "
            "and national data portals of EU member states."
        ),
        anchor_id="dcat_ap",
        color="#003399",
        members=[
            SuiteMember(
                standard_id="dcat_ap",
                relationship="anchor",
                role="EU Application Profile of DCAT — defines classes and properties "
                     "for cataloguing datasets, distributions, and data services across "
                     "EU member state portals.",
            ),
            SuiteMember(
                standard_id="dcat_ap_se",
                relationship="extends",
                role="Swedish national profile of DCAT-AP — adds mandatory publisher, "
                     "CC0 catalogue licence requirement, Geonames spatial URIs, "
                     "HVD category support, and a Swedish availability vocabulary.",
            ),
            SuiteMember(
                standard_id="dublin_core",
                relationship="extends",
                role="Foundational vocabulary — DCAT-AP reuses Dublin Core Terms (dct:) "
                     "for the majority of its descriptive properties (title, description, "
                     "creator, publisher, date, identifier, language, rights, etc.).",
            ),
        ],
    ),

    StandardSuite(
        id="eu_spatial_data_infrastructure",
        name="EU Spatial Data Infrastructure",
        description=(
            "The EU INSPIRE Directive mandates spatial data metadata for 34 geographic "
            "themes across all EU member states. INSPIRE's metadata specification is "
            "formally based on ISO 19115-1, which it profiles and constrains. "
            "Implementing INSPIRE without understanding ISO 19115 is impractical — "
            "ISO 19115 defines the underlying data model, XML encoding (ISO 19139), "
            "and the geographic extent, coordinate reference, and data quality elements "
            "that INSPIRE mandates."
        ),
        anchor_id="inspire",
        color="#006633",
        members=[
            SuiteMember(
                standard_id="inspire",
                relationship="anchor",
                role="EU directive metadata specification — mandates discovery metadata "
                     "for spatial datasets and services across EU member states, "
                     "covering identification, classification, geographic extent, "
                     "temporal reference, quality, conformity, and constraints.",
            ),
            SuiteMember(
                standard_id="iso19115",
                relationship="extends",
                role="Underlying geographic metadata standard — INSPIRE is formally "
                     "profiled from ISO 19115-1. Provides the complete metadata model, "
                     "XML encoding via ISO 19139, and elements beyond the INSPIRE "
                     "mandatory set.",
            ),
        ],
    ),

    StandardSuite(
        id="iso_information_management",
        name="ISO Information Management",
        description=(
            "Two complementary ISO standards addressing different dimensions of "
            "information management. ISO 19115-1 covers geographic and general-purpose "
            "resource metadata including identification, quality, spatial representation, "
            "and constraints. ISO 23081-1 covers records management metadata — the "
            "lifecycle, disposition, mandate, and agent relationships needed for "
            "managing records over time. Together they provide end-to-end coverage "
            "from resource discovery through long-term preservation."
        ),
        anchor_id="iso19115",
        color="#495057",
        members=[
            SuiteMember(
                standard_id="iso19115",
                relationship="anchor",
                role="Geographic and general resource metadata — covers identification, "
                     "data quality, spatial representation, reference systems, content, "
                     "distribution, and constraints.",
            ),
            SuiteMember(
                standard_id="iso23081",
                relationship="complements",
                role="Records management metadata — adds lifecycle, disposition authority, "
                     "agent relationships, mandates, and use history needed for long-term "
                     "records stewardship.",
            ),
        ],
    ),

    StandardSuite(
        id="nist_security_metadata",
        name="NIST Security & Identity Metadata",
        description=(
            "Two complementary NIST publications covering different aspects of security "
            "metadata. SP 800-60 provides the information-type taxonomy and impact-level "
            "categorisation framework (Confidentiality/Integrity/Availability: "
            "Low/Moderate/High) that feeds into system security planning. "
            "IR 8112 defines the attribute metadata schema that describes the "
            "identity attributes of the persons and systems involved in handling "
            "that information — enabling relying parties in federated systems to "
            "evaluate the trustworthiness, currency, and provenance of identity claims."
        ),
        anchor_id="nist_sp80060",
        color="#5c2d82",
        members=[
            SuiteMember(
                standard_id="nist_sp80060",
                relationship="anchor",
                role="Information type categorisation — maps information types to "
                     "provisional impact levels (Low/Moderate/High) per FIPS 199, "
                     "determining the overall security category of an information system.",
            ),
            SuiteMember(
                standard_id="nist_ir8112",
                relationship="complements",
                role="Attribute metadata schema — describes the properties (origin, "
                     "verification method, accuracy, expiry, provenance) of identity "
                     "attributes exchanged in federated systems that access the "
                     "categorised information.",
            ),
        ],
    ),
]

# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

_SUITE_INDEX = {s.id: s for s in SUITES}
_STANDARD_TO_SUITES: dict = {}
for _suite in SUITES:
    for _member in _suite.members:
        _STANDARD_TO_SUITES.setdefault(_member.standard_id, []).append(_suite)


def get_all_suites() -> List[StandardSuite]:
    return list(SUITES)


def get_suite(suite_id: str) -> Optional[StandardSuite]:
    return _SUITE_INDEX.get(suite_id)


def get_suites_for_standard(standard_id: str) -> List[StandardSuite]:
    """Return all suites that include this standard."""
    return _STANDARD_TO_SUITES.get(standard_id, [])


def build_pairwise_summary() -> dict:
    """
    Build an N×N dict of usage-compatibility summaries for every pair of standards.

    Each cell contains:
      category   : str  — one of: self | required | extends | complements |
                                   high | medium | low | none
      label      : str  — short human-readable label
      description: str  — one sentence explaining the relationship
      score      : float — crosswalk compatibility score 0.0–1.0 (0.0 for suite pairs)
      suite_id   : str | None — suite that defines the relationship (if any)
      suite_name : str | None
    """
    from standards.registry import get_all_standards
    from standards.crosswalk import compute_compatibility_score

    standards = get_all_standards()
    ids = [s.id for s in standards]
    names = {s.id: s.name for s in standards}

    # Build a fast lookup: (src_id, tgt_id) -> (suite, src_member, tgt_member)
    suite_pairs: dict = {}
    for suite in SUITES:
        member_ids = [m.standard_id for m in suite.members]
        for i, mid in enumerate(member_ids):
            for jid in member_ids:
                if mid == jid:
                    continue
                src_m = suite.get_member(mid)
                tgt_m = suite.get_member(jid)
                # Only record if not already recorded by a stronger relationship
                key = (mid, jid)
                if key not in suite_pairs:
                    suite_pairs[key] = (suite, src_m, tgt_m)

    result = {}
    for src_id in ids:
        result[src_id] = {}
        for tgt_id in ids:
            if src_id == tgt_id:
                result[src_id][tgt_id] = {
                    "category": "self",
                    "label": "—",
                    "description": "",
                    "score": 1.0,
                    "suite_id": None,
                    "suite_name": None,
                }
                continue

            # Check suite relationship first
            suite_key = (src_id, tgt_id)
            if suite_key in suite_pairs:
                suite, src_m, tgt_m = suite_pairs[suite_key]
                rel = tgt_m.relationship  # relationship of the TARGET in the suite

                # Determine category from the relationship of either member
                # "requires" wins over everything; anchor+requires pair = required
                all_rels = {src_m.relationship, tgt_m.relationship}
                if "requires" in all_rels or (
                        src_m.relationship == "anchor" and tgt_m.relationship == "requires") or (
                        tgt_m.relationship == "anchor" and src_m.relationship == "requires"):
                    cat = "required"
                    label = "Must use together"
                    desc = (
                        f"{names[src_id]} and {names[tgt_id]} are normatively interdependent "
                        f"within the {suite.name} suite — one cannot be fully used without the other."
                    )
                elif "extends" in all_rels:
                    cat = "extends"
                    label = "Extends / profiles"
                    desc = (
                        f"One of these standards is an application profile or formal extension of the other "
                        f"({suite.name}). They share a common vocabulary and are designed to be used together."
                    )
                else:
                    cat = "complements"
                    label = "Complements"
                    desc = (
                        f"{names[src_id]} and {names[tgt_id]} are complementary standards in the "
                        f"{suite.name} suite — they cover different aspects and are commonly used together."
                    )
                result[src_id][tgt_id] = {
                    "category": cat,
                    "label": label,
                    "description": desc,
                    "score": 0.0,
                    "suite_id": suite.id,
                    "suite_name": suite.name,
                }
                continue

            # No suite relationship — use crosswalk score
            score = compute_compatibility_score(src_id, tgt_id)
            pct = score * 100
            if pct >= 50:
                cat, label = "high", "High crosswalk"
                desc = (
                    f"{int(pct)}% of {names[src_id]} fields have defined equivalents in "
                    f"{names[tgt_id]}. These standards can be used together with good field coverage."
                )
            elif pct >= 25:
                cat, label = "medium", "Partial crosswalk"
                desc = (
                    f"{int(pct)}% of {names[src_id]} fields map to {names[tgt_id]}. "
                    f"Partial interoperability is achievable but significant gaps exist."
                )
            elif pct > 0:
                cat, label = "low", "Limited crosswalk"
                desc = (
                    f"Only {int(pct)}% of {names[src_id]} fields have equivalents in "
                    f"{names[tgt_id]}. These standards address different concerns; "
                    f"limited direct mapping is possible."
                )
            else:
                cat, label = "none", "No crosswalk"
                desc = (
                    f"No field-level mappings are defined between {names[src_id]} and "
                    f"{names[tgt_id]}. These standards operate in different domains and "
                    f"are not directly interoperable."
                )
            result[src_id][tgt_id] = {
                "category": cat,
                "label": label,
                "description": desc,
                "score": round(score, 3),
                "suite_id": None,
                "suite_name": None,
            }

    return result


def get_suite_example(suite_id: str) -> Optional[dict]:
    """Return a structured visual example for a given suite, or None."""
    return SUITE_EXAMPLES.get(suite_id)


# ---------------------------------------------------------------------------
# Visual examples — one annotated structure per suite
#
# Each example is a dict:
#   title       : str
#   description : str   — one paragraph explaining what the example illustrates
#   layout      : str   — "nested" | "columns" | "flow"
#   blocks      : list  — list of block dicts (see below)
#
# Block dict:
#   id          : str   — standard_id for colour-coding
#   label       : str   — heading shown on the box
#   color       : str   — hex background colour
#   text_color  : str   — hex text colour
#   description : str   — one sentence shown inside the box
#   fields      : list of {"name", "value", "note"}
#   children    : list of nested block dicts   (layout=nested only)
#   annotation  : str   — optional arrow/connector annotation
# ---------------------------------------------------------------------------

SUITE_EXAMPLES: dict = {

    # ── NATO Metadata Infrastructure ─────────────────────────────────────────
    "nato_metadata_infrastructure": {
        "title": "A NATO document with full metadata infrastructure",
        "description": (
            "This example shows how the three standards nest around a single data object. "
            "ADatP-4778 is the outermost envelope — it cryptographically binds everything "
            "together. Inside it sits the ADatP-5636 metadata record, whose Security Layer "
            "contains confidentiality labels whose syntax is defined by ADatP-4774. "
            "The data object itself (the PDF) sits outside the metadata but is referenced "
            "and signed by the 4778 binding."
        ),
        "layout": "nested",
        "blocks": [
            {
                "id": "adatp4778",
                "label": "ADatP-4778 — Metadata Binding Wrapper",
                "color": "#001f5e",
                "text_color": "#ffffff",
                "description": (
                    "Outer envelope. Cryptographically binds the metadata record to "
                    "the data object via XML Signature. Proves that the metadata "
                    "has not been altered since it was signed."
                ),
                "fields": [
                    {"name": "DataObjectReference",
                     "value": "sha-256: a3f9c2…",
                     "note": "Hash of the PDF — any change to the file breaks this link"},
                    {"name": "XMLSignature",
                     "value": "[RSA-SHA256, signed by HQ NATO CA]",
                     "note": "Cryptographic proof of integrity and origin"},
                ],
                "children": [
                    {
                        "id": "adatp5636",
                        "label": "ADatP-5636 — Core Metadata Record",
                        "color": "#003189",
                        "text_color": "#ffffff",
                        "description": (
                            "The metadata record itself, organised in three layers. "
                            "The Security Layer fields reference confidentiality label "
                            "structures whose syntax is defined by ADatP-4774."
                        ),
                        "fields": [],
                        "children": [
                            {
                                "id": "adatp4774",
                                "label": "Security Layer (ADatP-4774 label syntax)",
                                "color": "#c0392b",
                                "text_color": "#ffffff",
                                "description": (
                                    "Classification labels. The structure of each label "
                                    "is normatively defined by ADatP-4774, not by 5636 itself."
                                ),
                                "fields": [
                                    {"name": "originatorConfidentialityLabel",
                                     "value": "PolicyIdentifier: NATO | Classification: RESTRICTED | Category: NATO",
                                     "note": "Mandatory — set by the originator"},
                                    {"name": "metadataConfidentialityLabel",
                                     "value": "PolicyIdentifier: NATO | Classification: UNCLASSIFIED",
                                     "note": "Mandatory — labels the metadata record itself, not the resource"},
                                ],
                                "children": [],
                            },
                            {
                                "id": "adatp5636",
                                "label": "Common Layer",
                                "color": "#0044c8",
                                "text_color": "#ffffff",
                                "description": "Descriptive and administrative metadata elements.",
                                "fields": [
                                    {"name": "title",
                                     "value": "Exercise TRIDENT JUNCTURE — Final After-Action Report",
                                     "note": "Mandatory"},
                                    {"name": "creator",
                                     "value": "type=person; name=J. Smith; affiliation=HQ SACT; email=j.smith@act.nato.int",
                                     "note": "Mandatory — PointOfContact composite value"},
                                    {"name": "publisher",
                                     "value": "type=organization; name=HQ Supreme Allied Command Transformation",
                                     "note": "Mandatory"},
                                    {"name": "dateCreated",
                                     "value": "2024-11-22T14:00:00Z",
                                     "note": "Mandatory — ISO 8601"},
                                    {"name": "identifier",
                                     "value": "urn:nato:resource:2024:SACT-AAR-TJ24-001",
                                     "note": "Mandatory — NATO URN scheme"},
                                    {"name": "language",
                                     "value": "eng",
                                     "note": "Optional — ISO 639-3"},
                                    {"name": "countryCode",
                                     "value": "NOR",
                                     "note": "Optional — exercise held in Norway"},
                                ],
                                "children": [],
                            },
                            {
                                "id": "adatp5636",
                                "label": "Information Lifecycle Support Layer",
                                "color": "#1a6bbf",
                                "text_color": "#ffffff",
                                "description": "Retention, disposition and version management.",
                                "fields": [
                                    {"name": "dateDisposition",
                                     "value": "2044-11-22",
                                     "note": "Optional — 20-year retention per NATO policy"},
                                    {"name": "status",
                                     "value": "Final",
                                     "note": "Optional"},
                                    {"name": "version",
                                     "value": "1.0",
                                     "note": "Optional"},
                                ],
                                "children": [],
                            },
                        ],
                    },
                ],
                "annotation": "",
            },
            {
                "id": "data_object",
                "label": "Data Object (the resource itself)",
                "color": "#495057",
                "text_color": "#ffffff",
                "description": (
                    "The actual file or information object. It exists independently of "
                    "the metadata; the 4778 binding ties them together without embedding "
                    "one inside the other."
                ),
                "fields": [
                    {"name": "File",
                     "value": "SACT-AAR-TJ24-001.pdf  (4.2 MB)",
                     "note": "The PDF is referenced by hash in the 4778 binding, not embedded in the metadata"},
                ],
                "children": [],
                "annotation": "&#8593; bound and signed by ADatP-4778",
            },
        ],
    },

    # ── EU Data Catalogue Profile ─────────────────────────────────────────────
    "eu_data_catalogue": {
        "title": "A dataset record on an EU national data portal",
        "description": (
            "This example shows a DCAT-AP dataset record as it would appear on an EU "
            "member state open data portal. The coloured fields show which elements come "
            "from the Dublin Core vocabulary (dct: prefix, reused by DCAT-AP) and which "
            "are DCAT-AP specific (dcat: prefix). Understanding Dublin Core is essential "
            "because the majority of a DCAT-AP record is expressed in Dublin Core Terms."
        ),
        "layout": "columns",
        "blocks": [
            {
                "id": "dublin_core",
                "label": "Dublin Core Terms (dct:) — inherited by DCAT-AP",
                "color": "#003399",
                "text_color": "#ffffff",
                "description": (
                    "These fields use the dct: (Dublin Core Terms) namespace. "
                    "DCAT-AP does not redefine them — it reuses the Dublin Core "
                    "definitions directly. Any Dublin Core-aware system can read these."
                ),
                "fields": [
                    {"name": "dct:title",
                     "value": "Air Quality Monitoring Data — Oslo Region 2023",
                     "note": "Mandatory in DCAT-AP, inherited from Dublin Core"},
                    {"name": "dct:description",
                     "value": "Hourly PM2.5, PM10, NO2 and O3 measurements from 18 monitoring stations.",
                     "note": "Mandatory in DCAT-AP"},
                    {"name": "dct:publisher",
                     "value": "Norwegian Environment Agency",
                     "note": "Mandatory — foaf:Agent"},
                    {"name": "dct:identifier",
                     "value": "https://data.norge.no/datasets/air-quality-oslo-2023",
                     "note": "Mandatory"},
                    {"name": "dct:issued",
                     "value": "2024-01-15",
                     "note": "Optional — date of formal publication"},
                    {"name": "dct:modified",
                     "value": "2024-03-01",
                     "note": "Optional — date of last revision"},
                    {"name": "dct:language",
                     "value": "http://publications.europa.eu/resource/authority/language/NOR",
                     "note": "Optional — EU authority code"},
                    {"name": "dct:license",
                     "value": "https://creativecommons.org/licenses/by/4.0/",
                     "note": "Recommended — URI to licence"},
                    {"name": "dct:accrualPeriodicity",
                     "value": "http://publications.europa.eu/resource/authority/frequency/HOURLY",
                     "note": "Recommended — update frequency"},
                ],
                "children": [],
            },
            {
                "id": "dcat_ap",
                "label": "DCAT-AP specific (dcat:) — EU application profile additions",
                "color": "#0d6efd",
                "text_color": "#ffffff",
                "description": (
                    "These fields use the dcat: namespace and are specific to DCAT-AP. "
                    "They extend Dublin Core with structured distribution, theme, and "
                    "contact information that Dublin Core alone cannot express."
                ),
                "fields": [
                    {"name": "dcat:theme",
                     "value": "http://publications.europa.eu/resource/authority/data-theme/ENVI",
                     "note": "Recommended — EU Data Theme vocabulary: Environment"},
                    {"name": "dcat:keyword",
                     "value": "air quality, PM2.5, NO2, Oslo, environment",
                     "note": "Recommended — free-text keywords"},
                    {"name": "dcat:contactPoint",
                     "value": "vcard:Kind → data@environment.no",
                     "note": "Recommended — vCard contact"},
                    {"name": "dcat:spatialResolutionInMeters",
                     "value": "500.0",
                     "note": "Optional — spatial granularity of the data"},
                    {"name": "dcat:temporalResolution",
                     "value": "PT1H",
                     "note": "Optional — ISO 8601 duration: 1 hour"},
                    {"name": "dcat:distribution",
                     "value": "→ Distribution record (see below)",
                     "note": "Mandatory if data is accessible — links to download/access"},
                ],
                "children": [],
            },
            {
                "id": "dcat_ap",
                "label": "dcat:Distribution — how to access the data",
                "color": "#4dabf7",
                "text_color": "#212529",
                "description": (
                    "Each distribution describes one way to access the dataset "
                    "(e.g. CSV download, API endpoint, WMS service). A dataset "
                    "can have multiple distributions."
                ),
                "fields": [
                    {"name": "dcat:accessURL",
                     "value": "https://api.nilu.no/aqdata/oslo/2023",
                     "note": "Mandatory — URL of the access point"},
                    {"name": "dcat:downloadURL",
                     "value": "https://data.norge.no/files/air-quality-oslo-2023.csv",
                     "note": "Optional — direct download link"},
                    {"name": "dct:format",
                     "value": "http://publications.europa.eu/resource/authority/file-type/CSV",
                     "note": "Recommended — EU file type authority"},
                    {"name": "dcat:mediaType",
                     "value": "text/csv",
                     "note": "Recommended — IANA MIME type"},
                    {"name": "dct:license",
                     "value": "https://creativecommons.org/licenses/by/4.0/",
                     "note": "Recommended — may differ from dataset-level license"},
                ],
                "children": [],
            },
        ],
    },

    # ── EU Spatial Data Infrastructure ───────────────────────────────────────
    "eu_spatial_data_infrastructure": {
        "title": "A spatial dataset metadata record under the INSPIRE Directive",
        "description": (
            "INSPIRE mandates discovery metadata for spatial datasets across EU member "
            "states. Its metadata model is a constrained profile of ISO 19115-1: every "
            "INSPIRE element maps to an ISO 19115 element, but ISO 19115 defines many more "
            "elements than INSPIRE requires. This example shows an INSPIRE-compliant record "
            "and highlights which ISO 19115 structures it uses underneath."
        ),
        "layout": "columns",
        "blocks": [
            {
                "id": "inspire",
                "label": "INSPIRE — Mandatory discovery metadata",
                "color": "#006633",
                "text_color": "#ffffff",
                "description": (
                    "The elements INSPIRE requires for every spatial dataset. "
                    "These are the minimum needed for the resource to appear on "
                    "the EU INSPIRE Geoportal."
                ),
                "fields": [
                    {"name": "title",
                     "value": "Administrative Units — Norway",
                     "note": "Mandatory — maps to ISO 19115 MD_DataIdentification/citation/title"},
                    {"name": "abstract",
                     "value": "Municipal and county boundaries for Norway, updated annually from the Norwegian Mapping Authority.",
                     "note": "Mandatory"},
                    {"name": "keyword",
                     "value": "Administrative units (INSPIRE Annex I theme)",
                     "note": "Mandatory — must reference GEMET INSPIRE themes vocabulary"},
                    {"name": "geographicBoundingBox",
                     "value": "W: 4.09 | E: 31.17 | S: 57.81 | N: 71.19",
                     "note": "Mandatory — WGS84 decimal degrees"},
                    {"name": "topicCategory",
                     "value": "boundaries",
                     "note": "Mandatory for datasets — ISO 19115 MD_TopicCategoryCode"},
                    {"name": "dateOfPublication",
                     "value": "2024-01-01",
                     "note": "Mandatory — at least one date required"},
                    {"name": "lineage",
                     "value": "Derived from the Norwegian Property Register (Matrikkelen). Annual update cycle.",
                     "note": "Mandatory — data quality / provenance statement"},
                    {"name": "conditionsForAccessAndUse",
                     "value": "No conditions apply — Norwegian Open Government Data licence",
                     "note": "Mandatory — access and use constraints"},
                    {"name": "limitationsOnPublicAccess",
                     "value": "No limitations on public access",
                     "note": "Mandatory"},
                    {"name": "responsibleParty",
                     "value": "Norwegian Mapping Authority | role: pointOfContact",
                     "note": "Mandatory"},
                    {"name": "metadataLanguage",
                     "value": "nor",
                     "note": "Mandatory"},
                    {"name": "metadataDate",
                     "value": "2024-03-15",
                     "note": "Mandatory — date this metadata record was created/updated"},
                ],
                "children": [],
            },
            {
                "id": "iso19115",
                "label": "ISO 19115-1 — Full metadata model (INSPIRE profiles this)",
                "color": "#2d6a4f",
                "text_color": "#ffffff",
                "description": (
                    "ISO 19115-1 defines the full metadata model that INSPIRE is based on. "
                    "These additional elements are not required by INSPIRE but are available "
                    "for richer documentation, and many national implementations include them."
                ),
                "fields": [
                    {"name": "fileIdentifier",
                     "value": "NO-NMA-ADMIN-UNITS-2024",
                     "note": "ISO 19115 — unique ID for this metadata record"},
                    {"name": "metadataStandardName",
                     "value": "ISO 19115-1:2014 / INSPIRE Metadata Regulation",
                     "note": "ISO 19115 — identifies the standard used"},
                    {"name": "spatialRepresentationType",
                     "value": "vector",
                     "note": "ISO 19115 — not mandated by INSPIRE but commonly included"},
                    {"name": "spatialResolution (equivalentScale)",
                     "value": "1:50 000",
                     "note": "ISO 19115 — precision of the dataset"},
                    {"name": "resourceFormat",
                     "value": "GML 3.2 / ESRI Shapefile",
                     "note": "ISO 19115 MD_Format — distribution format"},
                    {"name": "referenceSystemIdentifier",
                     "value": "EPSG:25833 (ETRS89 / UTM zone 33N)",
                     "note": "ISO 19115 — coordinate reference system"},
                    {"name": "MD_SecurityConstraints / classification",
                     "value": "unclassified",
                     "note": "ISO 19115 — security classification (not in INSPIRE core)"},
                    {"name": "MD_MaintenanceInformation",
                     "value": "updateFrequency: annually | nextUpdateDate: 2025-01-01",
                     "note": "ISO 19115 — maintenance schedule beyond INSPIRE scope"},
                ],
                "children": [],
            },
        ],
    },

    # ── ISO Information Management ────────────────────────────────────────────
    "iso_information_management": {
        "title": "A government contract document across its full information lifecycle",
        "description": (
            "ISO 19115-1 describes what a resource is — its content, coverage, quality "
            "and format. ISO 23081-1 describes what happens to a resource over time — "
            "who is responsible for it, under what mandate it was created, when it must "
            "be disposed of, and whether a legal hold prevents disposal. Together they "
            "cover a record from creation to final disposition."
        ),
        "layout": "flow",
        "blocks": [
            {
                "id": "iso19115",
                "label": "ISO 19115-1 — Resource Description",
                "color": "#2d6a4f",
                "text_color": "#ffffff",
                "description": "Answers: What is this resource? What does it contain? What quality does it have?",
                "fields": [
                    {"name": "citation / title",
                     "value": "Infrastructure Survey — Eastern District Water Mains",
                     "note": "Identifies the resource"},
                    {"name": "abstract",
                     "value": "GIS survey of water main infrastructure, including pipe age, material and pressure zones.",
                     "note": "Content description"},
                    {"name": "dateStamp",
                     "value": "2019-06-14",
                     "note": "When the metadata was created"},
                    {"name": "topicCategory",
                     "value": "utilitiesCommunication",
                     "note": "ISO 19115 topic classification"},
                    {"name": "geographicBoundingBox",
                     "value": "Eastern District boundary polygon",
                     "note": "Spatial extent"},
                    {"name": "resourceFormat",
                     "value": "GeoPackage 1.2",
                     "note": "Distribution format"},
                    {"name": "lineage",
                     "value": "Field survey 2019, verified against 2018 engineering drawings.",
                     "note": "Data quality — provenance"},
                    {"name": "resourceConstraints",
                     "value": "Not for public release — internal infrastructure data",
                     "note": "Access constraints"},
                ],
                "children": [],
                "annotation": "&#8595; the same record is then managed as a record",
            },
            {
                "id": "iso23081",
                "label": "ISO 23081-1 — Records Management Metadata",
                "color": "#1b4332",
                "text_color": "#ffffff",
                "description": "Answers: Who owns it? Under what authority? When must it be disposed of? Is it on hold?",
                "fields": [
                    {"name": "agent / role: creator",
                     "value": "Infrastructure Management Dept, City of Oslo",
                     "note": "Who created the record"},
                    {"name": "agent / role: owner",
                     "value": "City Engineer's Office",
                     "note": "Who is responsible for the record"},
                    {"name": "mandate",
                     "value": "Municipal Records Act §14 — infrastructure surveys",
                     "note": "Legal authority requiring the record to exist"},
                    {"name": "dispositionAuthority",
                     "value": "City Archives Retention Schedule, Class 7.4.2",
                     "note": "The schedule that governs when/how to dispose"},
                    {"name": "retentionPeriod",
                     "value": "Permanent — transfer to City Archives after 30 years",
                     "note": "Derived from disposition authority"},
                    {"name": "dispositionDate",
                     "value": "2049-06-14",
                     "note": "Calculated: creation date + retention period"},
                    {"name": "recordsHold",
                     "value": "false",
                     "note": "No active legal hold — disposal may proceed on schedule"},
                    {"name": "status",
                     "value": "active",
                     "note": "Current lifecycle status of the record"},
                    {"name": "use / accessHistory",
                     "value": "Accessed 3 times for planning applications (2020, 2022, 2024)",
                     "note": "ISO 23081 use metadata — supports appraisal decisions"},
                ],
                "children": [],
            },
        ],
    },

    # ── NIST Security & Identity Metadata ────────────────────────────────────
    "nist_security_metadata": {
        "title": "Security categorisation feeding into federated attribute trust",
        "description": (
            "SP 800-60 categorises an information system by the sensitivity of the "
            "information it processes (Confidentiality / Integrity / Availability impact "
            "levels: Low, Moderate, or High). That categorisation then informs the trust "
            "requirements for identity attributes in IR 8112 — a system handling High "
            "confidentiality information demands attributes that are strongly verified, "
            "recently checked, and governed by a recognised trust framework."
        ),
        "layout": "flow",
        "blocks": [
            {
                "id": "nist_sp80060",
                "label": "NIST SP 800-60 — Information Type Categorisation",
                "color": "#5c2d82",
                "text_color": "#ffffff",
                "description": (
                    "Step 1: identify the information types the system processes and "
                    "assign provisional CIA impact levels. The highest impact level "
                    "across all types sets the overall security category."
                ),
                "fields": [
                    {"name": "systemName",
                     "value": "NATO Intelligence Analysis Portal",
                     "note": "The system being categorised"},
                    {"name": "informationType [1]",
                     "value": "C.3.1 — Defense and National Security / Intelligence",
                     "note": "SP 800-60 Appendix C taxonomy identifier"},
                    {"name": "confidentialityImpact",
                     "value": "High",
                     "note": "Unauthorised disclosure could cause severe damage to national security"},
                    {"name": "integrityImpact",
                     "value": "High",
                     "note": "Corrupted intelligence could lead to critically flawed decisions"},
                    {"name": "availabilityImpact",
                     "value": "Moderate",
                     "note": "Temporary unavailability is serious but not catastrophic"},
                    {"name": "systemSecurityCategory",
                     "value": "SC = {(confidentiality, High), (integrity, High), (availability, Moderate)} → Overall: HIGH",
                     "note": "FIPS 199 high-watermark: overall category = highest individual impact"},
                ],
                "children": [],
                "annotation": "&#8595; HIGH system category sets strict trust requirements for users and attributes",
            },
            {
                "id": "nist_ir8112",
                "label": "NIST IR 8112 — Attribute Metadata for Users Accessing the System",
                "color": "#7b3fa0",
                "text_color": "#ffffff",
                "description": (
                    "Step 2: because the system is categorised HIGH, the attributes "
                    "used to grant access must meet correspondingly high assurance standards. "
                    "IR 8112 metadata lets the relying party evaluate whether each "
                    "attribute meets those standards before granting access."
                ),
                "fields": [
                    {"name": "attributeName",
                     "value": "clearanceLevel",
                     "note": "The identity attribute being asserted (e.g. security clearance)"},
                    {"name": "attributeValue",
                     "value": "NATO SECRET",
                     "note": "The claimed clearance level"},
                    {"name": "attributeDataType",
                     "value": "string",
                     "note": "IR 8112 §3.3 — data type of the value"},
                    {"name": "attributeOrigin",
                     "value": "https://nspa.nato.int/personnel-security/",
                     "note": "Authoritative source — NATO Security and Personnel Agency"},
                    {"name": "attributeVerification",
                     "value": "in-person",
                     "note": "How the clearance was verified — in-person vetting required for HIGH systems"},
                    {"name": "lastVerified",
                     "value": "2024-01-10T00:00:00Z",
                     "note": "Must be recent — HIGH systems may require re-verification every 5 years"},
                    {"name": "expiryDate",
                     "value": "2029-01-10T00:00:00Z",
                     "note": "Clearance expires — system must reject access after this date"},
                    {"name": "attributeAccuracy",
                     "value": "high",
                     "note": "Confidence in the value — commensurate with in-person vetting"},
                    {"name": "policyIdentifier",
                     "value": "https://www.nato.int/cps/en/natohq/official_texts_17279.htm",
                     "note": "NATO Security Policy — the trust framework governing the clearance"},
                    {"name": "assertingParty",
                     "value": "https://idp.nspa.nato.int/",
                     "note": "The identity provider asserting the clearance in this transaction"},
                ],
                "children": [],
            },
        ],
    },
}


def get_suite_siblings(standard_id: str) -> List[dict]:
    """
    For a given standard, return the other members of every suite it belongs to,
    enriched with relationship info. Used to render 'Related Standards' panels.
    """
    result = []
    for suite in get_suites_for_standard(standard_id):
        for member in suite.members:
            if member.standard_id == standard_id:
                continue
            result.append({
                "suite_id": suite.id,
                "suite_name": suite.name,
                "standard_id": member.standard_id,
                "relationship": member.relationship,
                "role": member.role,
                "suite_color": suite.color,
            })
    return result
