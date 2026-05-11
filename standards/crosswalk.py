"""
Crosswalk mappings between metadata standards.

Each mapping entry defines:
  - source_standard:  standard ID of the source field
  - source_field:     field name in the source standard
  - target_standard:  standard ID of the target standard
  - target_field:     corresponding field name in the target standard (or None)
  - mapping_type:     "exact" | "similar" | "partial" | "none"
  - notes:            explanation of semantic differences/similarities

Primary crosswalk source: ADatP-5636 NCMS fields to other standards.
Additional crosswalks cover Dublin Core ↔ ISO 19115 and other pairs.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Verification sources
# ---------------------------------------------------------------------------

@dataclass
class CrosswalkSource:
    """
    A published, authoritative source that corroborates the crosswalk assessment
    for a given standard pair.

    basis:
      normative   — the mapping is defined by one of the standards themselves
                    (e.g. DCAT-AP uses dct: namespace from Dublin Core Terms)
      published   — an authoritative body has published a crosswalk document
                    (e.g. GeoDCAT-AP, INSPIRE Technical Guidelines)
      assessed    — our own field-by-field analysis; no public crosswalk exists
    """
    title: str
    url: str
    basis: str          # normative | published | assessed
    description: str
    sections: str = ""  # relevant section(s) in the source document


# Keyed by frozenset of two standard IDs (order-independent)
PAIR_SOURCES: Dict[Tuple[str, str], List[CrosswalkSource]] = {

    ("dublin_core", "dcat_ap"): [
        CrosswalkSource(
            title="DCAT-AP 2.1.1 Specification",
            url="https://semiceu.github.io/DCAT-AP/releases/2.1.1/",
            basis="normative",
            description=(
                "DCAT-AP is normatively built on Dublin Core Terms (dct:) and "
                "Dublin Core Elements (dc:). Properties such as dct:title, "
                "dct:description, dct:publisher, dct:issued, dct:language and "
                "dct:license are Dublin Core Terms properties reused directly. "
                "The mapping between the two standards is therefore inherent to "
                "the DCAT-AP specification itself."
            ),
            sections="§4 (Namespaces), §6 (Classes and properties)",
        ),
        CrosswalkSource(
            title="Dublin Core Terms (DCMI Metadata Terms)",
            url="https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            basis="normative",
            description=(
                "The authoritative definition of all Dublin Core Terms properties "
                "reused by DCAT-AP. Confirms semantic equivalence for shared properties."
            ),
        ),
    ],

    ("inspire", "iso19115"): [
        CrosswalkSource(
            title="INSPIRE Metadata Technical Guidelines v2.0.1 (TG MD)",
            url="https://knowledge-base.inspire.ec.europa.eu/publications/"
                "technical-guidance-implementation-inspire-dataset-and-service-"
                "metadata-based-isots-191392007_en",
            basis="normative",
            description=(
                "The INSPIRE Metadata Technical Guidelines are normative implementing "
                "rules under EU Directive 2007/2/EC. They explicitly map every INSPIRE "
                "metadata element to the corresponding ISO 19115 data model element, "
                "with clause-level references. INSPIRE metadata conformance is defined "
                "as a profile of ISO 19115 / ISO 19139."
            ),
            sections="Annex A (Abstract Test Suite), Annex C (Mapping tables)",
        ),
        CrosswalkSource(
            title="Commission Regulation (EC) No 1205/2008 — INSPIRE Metadata",
            url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32008R1205",
            basis="normative",
            description=(
                "The EU legal regulation defining mandatory INSPIRE metadata elements. "
                "The regulatory text cross-references ISO 19115 element names directly."
            ),
        ),
    ],

    ("dcat_ap", "inspire"): [
        CrosswalkSource(
            title="GeoDCAT-AP 2.0.0 — EU ISA² Programme",
            url="https://semiceu.github.io/GeoDCAT-AP/releases/2.0.0/",
            basis="published",
            description=(
                "GeoDCAT-AP is a published EU ISA² programme specification that "
                "provides an RDF encoding for INSPIRE and ISO 19115 metadata, "
                "enabling geospatial datasets to be published on general-purpose "
                "data portals using DCAT-AP. Appendix B contains field-level "
                "mapping tables between INSPIRE elements and DCAT-AP properties."
            ),
            sections="Appendix B (Mapping tables), §B.3–B.6",
        ),
    ],

    ("dcat_ap", "iso19115"): [
        CrosswalkSource(
            title="GeoDCAT-AP 2.0.0 — EU ISA² Programme",
            url="https://semiceu.github.io/GeoDCAT-AP/releases/2.0.0/",
            basis="published",
            description=(
                "GeoDCAT-AP maps the union of ISO 19115:2003 core profile elements "
                "and INSPIRE metadata elements to DCAT-AP properties. Appendix B "
                "gives a complete element-by-element mapping table."
            ),
            sections="Appendix B",
        ),
    ],

    ("dublin_core", "iso19115"): [
        CrosswalkSource(
            title="GeoDCAT-AP 2.0.0 — EU ISA² Programme",
            url="https://semiceu.github.io/GeoDCAT-AP/releases/2.0.0/",
            basis="published",
            description=(
                "GeoDCAT-AP implicitly covers Dublin Core ↔ ISO 19115 since "
                "DCAT-AP is built on Dublin Core Terms. The mapping can be composed "
                "from the GeoDCAT-AP ISO 19115 → DCAT-AP tables."
            ),
            sections="Appendix B",
        ),
        CrosswalkSource(
            title="DCMI / ISO TC 211 Joint Working Group — Geospatial Crosswalk",
            url="https://www.dublincore.org/groups/geospecial/",
            basis="published",
            description=(
                "The Dublin Core Metadata Initiative and ISO TC 211 have collaborated "
                "on crosswalk documentation between Dublin Core and ISO 19115 geographic "
                "metadata concepts."
            ),
        ),
    ],

    ("adatp5636", "dublin_core"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "ADatP-5636 references Dublin Core concepts in its design rationale "
                "and bibliography, but the NATO Standardization Office has not published "
                "a public crosswalk document. The field mappings in this tool represent "
                "our own analysis based on semantic alignment of field definitions. "
                "Access to the normative ADatP-5636 document requires NATO credentials."
            ),
        ),
    ],

    ("adatp5636", "dcat_ap"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "No public crosswalk between ADatP-5636 and DCAT-AP has been published. "
                "The field mappings in this tool are based on semantic analysis of both "
                "standards' field definitions. The DCAT-AP ↔ Dublin Core relationship "
                "is normative (DCAT-AP uses dct: namespace), which allows indirect "
                "corroboration for fields that map through Dublin Core."
            ),
        ),
    ],

    ("adatp5636", "inspire"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "No public crosswalk between ADatP-5636 and INSPIRE has been published. "
                "The mappings are based on our analysis. INSPIRE's basis in ISO 19115 "
                "can be used to partially corroborate via the ADatP-5636 ↔ ISO 19115 "
                "assessment and the normative INSPIRE ↔ ISO 19115 TG."
            ),
        ),
    ],

    ("adatp5636", "iso19115"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "ADatP-5636 references ISO 19115 geographic metadata concepts "
                "for spatial fields (e.g. geographicReference). No public crosswalk "
                "has been published by NATO NSO. The field mappings represent our own "
                "semantic analysis."
            ),
        ),
    ],

    ("adatp5636", "iso23081"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "ADatP-5636 covers records management concepts (recordsDisposition, "
                "dateDisposition) that align with ISO 23081 principles. No authoritative "
                "crosswalk has been published. Mappings are our own assessment."
            ),
        ),
    ],

    ("adatp5636", "nist_sp80060"): [
        CrosswalkSource(
            title="Author assessment",
            url="",
            basis="assessed",
            description=(
                "No published crosswalk exists between ADatP-5636 and NIST SP 800-60. "
                "The limited overlap (information type, sensitivity classification) is "
                "based on our semantic analysis of both standards."
            ),
        ),
    ],

    ("adatp5636", "nist_ir8112"): [
        CrosswalkSource(
            title="NIST IR 8112 — Attribute Metadata",
            url="https://csrc.nist.gov/publications/detail/ir/8112/final",
            basis="published",
            description=(
                "NIST IR 8112 defines a standard set of attribute metadata for "
                "identity and access management. Crosswalk to ADatP-5636 is our "
                "own analysis; NIST IR 8112 is publicly available and the field "
                "definitions can be directly compared."
            ),
        ),
    ],

    ("adatp5636", "dcat_ap_se"): [
        CrosswalkSource(
            title="ADatP-5636 Ed.A V1 — NCMS Metadata Standard (NATO NSO)",
            url="https://nso.nato.int/",
            basis="assessed",
            description=(
                "No public crosswalk between ADatP-5636 and DCAT-AP-SE exists. "
                "The mappings are derived from the ADatP-5636 ↔ DCAT-AP assessment "
                "(since DCAT-AP-SE reuses the same RDF properties) and augmented with "
                "SE-specific requirements from the DCAT-AP-SE 2.2.0 specification."
            ),
        ),
        CrosswalkSource(
            title="DCAT-AP-SE 2.2.0 Specification",
            url="https://docs.dataportal.se/dcat/2.2.0/en/",
            basis="normative",
            description=(
                "Used to identify DCAT-AP-SE-specific obligations and Swedish "
                "national requirements that differ from base DCAT-AP."
            ),
        ),
    ],

    ("dcat_ap_se", "dcat_ap"): [
        CrosswalkSource(
            title="DCAT-AP-SE 2.2.0 Specification",
            url="https://docs.dataportal.se/dcat/2.2.0/en/",
            basis="normative",
            description=(
                "DCAT-AP-SE is normatively defined as a constrained application profile "
                "of DCAT-AP. The specification explicitly states it extends DCAT-AP 2.x "
                "and shares the same RDF properties (dct:, dcat:, foaf: namespaces). "
                "All DCAT-AP-SE dataset and distribution properties are drawn directly "
                "from the DCAT-AP vocabulary, with Swedish-specific obligation levels "
                "and two additional SE-specific properties (dcatse:availability, "
                "dcat:hvdCategory)."
            ),
            sections="Introduction, Dataset class, Distribution class",
        ),
        CrosswalkSource(
            title="DCAT-AP-SE GitHub Repository (diggsweden/DCAT-AP-SE)",
            url="https://github.com/diggsweden/DCAT-AP-SE",
            basis="normative",
            description=(
                "Source repository for the DCAT-AP-SE specification, including the "
                "bundle.json file that defines all classes and property-level details "
                "(URIs, obligation levels, cardinality, ranges). Used as the primary "
                "technical reference for this crosswalk."
            ),
        ),
        CrosswalkSource(
            title="DCAT-AP 2.1.1 Specification",
            url="https://semiceu.github.io/DCAT-AP/releases/2.1.1/",
            basis="normative",
            description=(
                "The base EU Application Profile that DCAT-AP-SE extends. "
                "Confirms the shared property URIs and vocabulary requirements "
                "that are common to both profiles."
            ),
        ),
    ],

    ("dcat_ap_se", "dublin_core"): [
        CrosswalkSource(
            title="DCAT-AP-SE 2.2.0 Specification",
            url="https://docs.dataportal.se/dcat/2.2.0/en/",
            basis="normative",
            description=(
                "DCAT-AP-SE reuses Dublin Core Terms (dct:) properties throughout, "
                "confirming the mapping for title, description, publisher, creator, "
                "identifier, issued, modified, language, spatial, license, rights, "
                "relation, source, and type. The mapping to base Dublin Core (dc:) "
                "elements is derived from DCMI's own equivalence declarations."
            ),
        ),
        CrosswalkSource(
            title="DCMI Metadata Terms",
            url="https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            basis="normative",
            description=(
                "The authoritative definition of Dublin Core Terms (dct: namespace) "
                "used by DCAT-AP-SE. DCMI Terms are refinements or equivalents of "
                "the original 15 Dublin Core elements — the mapping is formally "
                "declared by DCMI."
            ),
        ),
    ],
}


def get_pair_sources(id_a: str, id_b: str) -> List[CrosswalkSource]:
    """Return verification sources for a standard pair (order-independent)."""
    key1 = (id_a, id_b)
    key2 = (id_b, id_a)
    return PAIR_SOURCES.get(key1) or PAIR_SOURCES.get(key2) or []


# ---------------------------------------------------------------------------
# Value-level compatibility issues
# ---------------------------------------------------------------------------

@dataclass
class FieldValueIssue:
    """
    A value-level incompatibility between two fields in a standard pair.
    Unlike CrosswalkEntry (which records whether a field has a mapping),
    FieldValueIssue records whether the *values* in a mapped field pair are
    compatible — i.e. whether an actual value from the source field would be
    accepted as-is by the target field.

    issue_type:
      vocabulary_mismatch  — same concept but incompatible controlled vocabularies
                             (e.g. NATO classification codes vs EU Access Rights NAL)
      format_change        — same data type but different encoding format
                             (e.g. ISO 639-3 alpha-3 vs BCP 47 language tags)
      structure_loss       — source is a structured compound object; target is a
                             plain string or URI (sub-fields cannot be recovered)
      collapse             — multiple source fields map to the same target field;
                             the target cannot distinguish which source field a value
                             came from
      uri_required         — target requires a URI from a specific authority; source
                             allows free text or a different URI namespace
    """
    source_standard: str
    target_standard: str
    source_field: str
    target_field: str
    issue_type: str       # see above
    severity: str         # blocking | lossy | transform_required
    title: str
    description: str
    source_vocab: str     # brief description of source vocabulary / encoding
    target_vocab: str     # brief description of target vocabulary / encoding
    example_values: list  # list of (src_val, tgt_val, note) tuples
    transform_spec: str = ""   # what transformation is needed to resolve the issue


VALUE_ISSUES: List[FieldValueIssue] = [

    # ── ADatP-5636 → Dublin Core ────────────────────────────────────────────

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dublin_core",
        source_field="language", target_field="language",
        issue_type="format_change", severity="transform_required",
        title="Language codes: ISO 639-3 alpha-3 vs BCP 47 / ISO 639-2",
        description=(
            "ADatP-5636 mandates ISO 639-3 alpha-3 codes (three-letter terminology "
            "codes). Dublin Core dc:language accepts BCP 47 tags (e.g. 'en', 'fr') "
            "or ISO 639-2/3. For major languages the codes match (ISO 639-3 'eng' "
            "equals ISO 639-2/T 'eng'), but the encoding expectation differs. "
            "A Dublin Core consumer expecting BCP 47 two-letter tags will not "
            "recognise 'eng' as valid."
        ),
        source_vocab="ISO 639-3 alpha-3 (e.g. eng, fra, deu, nld)",
        target_vocab="BCP 47 (e.g. en, fr, de, nl) or ISO 639-2/3",
        example_values=[
            ("eng", "eng / en", "ISO 639-3 matches ISO 639-2/T; BCP 47 would be 'en'"),
            ("nld", "nld / nl", "ISO 639-3 'nld' = ISO 639-2/T; BCP 47 = 'nl'"),
            ("deu", "deu / de", "ISO 639-3 'deu' = ISO 639-2/T; BCP 47 = 'de'"),
        ],
        transform_spec="Truncate to 2-char BCP 47 tag, or map ISO 639-3 → ISO 639-2/T lookup.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dublin_core",
        source_field="creator", target_field="creator",
        issue_type="structure_loss", severity="lossy",
        title="Structured PointOfContact flattened to free-text creator",
        description=(
            "ADatP-5636 creator is a structured PointOfContact compound with "
            "sub-fields for type, name, affiliation, email, phone, and role — all "
            "machine-readable. Dublin Core dc:creator is a plain text string or URI. "
            "The conversion must flatten the structure into a single string. "
            "The email address, phone number, affiliation, and role are lost as "
            "machine-actionable data and cannot be recovered from the DC record."
        ),
        source_vocab="PointOfContact: type=person|organisation; name; affiliation; email; phone; role",
        target_vocab="Free text agent name or URI",
        example_values=[
            (
                "type=person; name=Maj. Claire Dubois; affiliation=HQ AIRCOM; email=c.dubois@hqaircom.nato.int; role=author",
                "Maj. Claire Dubois (HQ AIRCOM)",
                "Email, role, and type are silently discarded",
            ),
        ],
        transform_spec="Concatenate name and affiliation into a readable string. Email and role must be discarded.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dublin_core",
        source_field="dateCreated", target_field="date",
        issue_type="collapse", severity="lossy",
        title="Three date fields collapse into a single dc:date",
        description=(
            "ADatP-5636 has distinct mandatory fields for dateCreated, dateIssued, "
            "and dateModified. Dublin Core dc:date is a single generic date element "
            "with no sub-type discriminator. All three fields map to dc:date, "
            "producing a record with up to three dc:date values that cannot be "
            "distinguished. A consumer sorting by publication date may pick the wrong "
            "value. DCTerms (dct:created, dct:issued, dct:modified) would resolve "
            "this, but plain dc:date does not."
        ),
        source_vocab="ISO 8601 datetime with semantic role (created | issued | modified)",
        target_vocab="Generic ISO 8601 date — no role discriminator in dc:date",
        example_values=[
            ("dateCreated=2024-03-15T09:00:00Z", "date=2024-03-15T09:00:00Z", "Role 'created' lost"),
            ("dateIssued=2024-03-22T14:30:00Z", "date=2024-03-22T14:30:00Z", "Role 'issued' lost — same target element"),
            ("dateModified=2024-04-01", "date=2024-04-01", "Role 'modified' lost — now ambiguous which date is which"),
        ],
        transform_spec="Use DCTerms dct:created, dct:issued, dct:modified instead of plain dc:date to preserve role semantics.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dublin_core",
        source_field="type", target_field="type",
        issue_type="vocabulary_mismatch", severity="transform_required",
        title="Resource type: NATO type codes vs DCMI Type Vocabulary",
        description=(
            "ADatP-5636 type field accepts either DCMI Type Vocabulary terms or "
            "NATO-specific resource type codes. Dublin Core dc:type expects values "
            "from the DCMI Type Vocabulary (Text, Dataset, Image, etc.). NATO-specific "
            "type codes not in the DCMI Type Vocabulary will be unrecognised by a "
            "Dublin Core consumer."
        ),
        source_vocab="DCMI Type Vocabulary OR NATO resource type code list",
        target_vocab="DCMI Type Vocabulary: Collection | Dataset | Event | Image | InteractiveResource | MovingImage | PhysicalObject | Service | Software | Sound | StillImage | Text",
        example_values=[
            ("Text", "Text", "Valid DCMI Type — no transformation needed"),
            ("Dataset", "Dataset", "Valid DCMI Type — no transformation needed"),
            ("Report", "Text", "NATO type 'Report' has no DCMI equivalent — closest is 'Text'"),
            ("TacticalPicture", None, "NATO-specific type with no DCMI equivalent — must be dropped or mapped to 'Image'"),
        ],
        transform_spec="Map NATO type codes to DCMI Type vocabulary. NATO types with no DCMI equivalent must be either dropped or mapped to the closest approximation.",
    ),

    # ── ADatP-5636 → DCAT-AP ────────────────────────────────────────────────

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap",
        source_field="language", target_field="dct:language",
        issue_type="uri_required", severity="transform_required",
        title="Language: ISO 639-3 code must become EU Languages Authority Table URI",
        description=(
            "ADatP-5636 uses ISO 639-3 alpha-3 codes as literal strings (e.g. 'eng'). "
            "DCAT-AP 2.1.1 requires dct:language to be a URI from the EU Publications "
            "Office Languages Named Authority List. An ISO 639-3 string will fail "
            "DCAT-AP validation. The transformation is well-defined but mandatory."
        ),
        source_vocab="ISO 639-3 alpha-3 literal string (e.g. eng, fra, deu)",
        target_vocab="EU Languages NAL URI (e.g. http://publications.europa.eu/resource/authority/language/ENG)",
        example_values=[
            ("eng", "http://publications.europa.eu/resource/authority/language/ENG", "Append EU NAL base URI + uppercase code"),
            ("fra", "http://publications.europa.eu/resource/authority/language/FRA", ""),
            ("deu", "http://publications.europa.eu/resource/authority/language/DEU", ""),
        ],
        transform_spec="Map: prepend 'http://publications.europa.eu/resource/authority/language/' and uppercase the code.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap",
        source_field="creator", target_field="dct:creator",
        issue_type="structure_loss", severity="lossy",
        title="Structured PointOfContact must become a foaf:Agent URI",
        description=(
            "DCAT-AP dct:creator expects a URI identifying a foaf:Agent — a "
            "resolvable identifier for a person or organisation in a controlled "
            "agent register. ADatP-5636 PointOfContact is a structured compound "
            "value (name, affiliation, email, role). No conversion from PointOfContact "
            "to a foaf:Agent URI is possible without an external agent registry. "
            "Without a URI, the field either cannot be populated (blocking) or must "
            "be represented as a blank node (non-conformant with DCAT-AP best practice)."
        ),
        source_vocab="PointOfContact: type; name; affiliation; email; phone; role",
        target_vocab="URI of foaf:Agent (e.g. from a national authority file or ORCID)",
        example_values=[
            (
                "type=organisation; name=HQ AIRCOM; affiliation=NATO Allied Air Command",
                "https://authority.example.org/agents/HQ-AIRCOM (hypothetical)",
                "Requires a resolvable URI — cannot be derived from the PointOfContact string alone",
            ),
        ],
        transform_spec="Requires an external agent registry. If none is available, represent as a blank foaf:Agent node with foaf:name populated from the PointOfContact name field.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap",
        source_field="accessRights", target_field="dct:accessRights",
        issue_type="vocabulary_mismatch", severity="transform_required",
        title="Access rights: free text / NATO URI must map to EU Access Rights NAL",
        description=(
            "DCAT-AP dct:accessRights requires a URI from the EU Access Rights "
            "Named Authority List, which has exactly three values: PUBLIC, RESTRICTED, "
            "or NON_PUBLIC. ADatP-5636 accessRights is free text or any URI. "
            "NATO access right values (e.g. 'NATO UNCLASSIFIED — Releasable to NATO') "
            "must be interpreted and mapped to one of the three EU vocabulary terms. "
            "This is a lossy transformation — the detailed releasability conditions "
            "are reduced to a coarse three-way classification."
        ),
        source_vocab="Free text or URI describing access conditions",
        target_vocab="EU Access Rights NAL: PUBLIC | RESTRICTED | NON_PUBLIC",
        example_values=[
            ("NATO UNCLASSIFIED — Releasable to NATO nations", "http://publications.europa.eu/resource/authority/access-right/RESTRICTED", "Releasable within NATO = Restricted (not fully public, not fully non-public)"),
            ("NATO UNCLASSIFIED — No limitations", "http://publications.europa.eu/resource/authority/access-right/PUBLIC", "Unrestricted = Public"),
            ("NATO SECRET", "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC", "Classified = Non-public (but security label detail is lost)"),
        ],
        transform_spec="Define a mapping table from NATO access/classification levels to the three EU Access Rights values. The mapping is inherently lossy.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap",
        source_field="originatorConfidentialityLabel", target_field="dct:accessRights",
        issue_type="vocabulary_mismatch", severity="lossy",
        title="ADatP-4774 confidentiality structure reduced to 3-value EU access right",
        description=(
            "The originatorConfidentialityLabel is a structured ADatP-4774 value "
            "encoding the NATO security policy, classification level, and releasability "
            "categories (e.g. REL TO specific nations). This rich security context "
            "is irreducibly reduced to PUBLIC / RESTRICTED / NON_PUBLIC in DCAT-AP. "
            "The releasability conditions, policy identifier, and category tags are "
            "permanently lost — a DCAT-AP consumer cannot reconstruct the original "
            "NATO access control decision from the converted record."
        ),
        source_vocab="ADatP-4774 ConfidentialityInformation: PolicyIdentifier; Classification; Category[TagName, Type, Value]",
        target_vocab="EU Access Rights NAL: PUBLIC | RESTRICTED | NON_PUBLIC",
        example_values=[
            (
                "PolicyIdentifier=urn:nato:policy:security; Classification=NATO UNCLASSIFIED; Category[TagName=Releasability,Type=PERMISSIVE,GenericValue=NATO]",
                "http://publications.europa.eu/resource/authority/access-right/RESTRICTED",
                "Full security policy context lost — only coarse access level preserved",
            ),
        ],
        transform_spec="Map NATO classification level to EU Access Right. Policy identifier and releasability categories cannot be expressed in DCAT-AP.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap",
        source_field="geographicReference", target_field="dct:spatial",
        issue_type="uri_required", severity="transform_required",
        title="Geographic reference must become a location URI (GeoNames / NUTS / EU Countries)",
        description=(
            "DCAT-AP dct:spatial expects a URI identifying a location resource, "
            "preferably from GeoNames, NUTS, or the EU Countries Named Authority List. "
            "ADatP-5636 geographicReference can be a bounding box, coordinates, or a "
            "named place identifier. Coordinate values cannot be directly expressed in "
            "dct:spatial and would require a GeoSPARQL or GeoDCAT-AP extension. "
            "Named places must be resolved to a registered authority URI."
        ),
        source_vocab="Bounding box (decimal degrees), coordinate pair, or named place identifier",
        target_vocab="URI from GeoNames, NUTS, EU Countries NAL, or GeoSPARQL geometry",
        example_values=[
            ("NORFOLKVA, USA", "http://sws.geonames.org/4776222/", "Named place → GeoNames URI (requires lookup)"),
            ("51.5°N 0.1°W (bounding box)", "GeoDCAT-AP dcat:bbox extension", "Coordinates require GeoDCAT-AP extension — not in base DCAT-AP"),
        ],
        transform_spec="Resolve named places to GeoNames or NUTS URIs. For coordinate-based references, use the GeoDCAT-AP dcat:bbox extension (not part of base DCAT-AP 2.1.1).",
    ),

    # ── ADatP-5636 → INSPIRE ────────────────────────────────────────────────

    FieldValueIssue(
        source_standard="adatp5636", target_standard="inspire",
        source_field="language", target_field="resourceLanguage",
        issue_type="format_change", severity="transform_required",
        title="Language codes: ISO 639-3 alpha-3 vs ISO 639-2/B (bibliographic)",
        description=(
            "INSPIRE requires ISO 639-2/B (bibliographic) three-letter codes. "
            "ADatP-5636 uses ISO 639-3 alpha-3 codes, which are identical to "
            "ISO 639-2/T (terminology) codes. For most languages the two variants "
            "are identical (e.g. 'eng' = 'eng'), but for some they differ — notably "
            "Dutch (ISO 639-2/T: 'nld', ISO 639-2/B: 'dut'), French ('fra' vs 'fre'), "
            "German ('deu' vs 'ger'). An INSPIRE validator will reject 'nld', 'fra', "
            "or 'deu' if it expects ISO 639-2/B."
        ),
        source_vocab="ISO 639-3 alpha-3 / ISO 639-2/T (e.g. deu, fra, nld)",
        target_vocab="ISO 639-2/B (e.g. ger, fre, dut)",
        example_values=[
            ("eng", "eng", "T and B codes identical — no change needed"),
            ("deu", "ger", "German: ISO 639-2/T 'deu' → ISO 639-2/B 'ger'"),
            ("fra", "fre", "French: ISO 639-2/T 'fra' → ISO 639-2/B 'fre'"),
            ("nld", "dut", "Dutch: ISO 639-2/T 'nld' → ISO 639-2/B 'dut'"),
            ("zho", "chi", "Chinese: ISO 639-2/T 'zho' → ISO 639-2/B 'chi'"),
        ],
        transform_spec="Apply ISO 639-2/T → ISO 639-2/B lookup table for languages where they differ. Approximately 20 languages have divergent codes.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="inspire",
        source_field="type", target_field="resourceType",
        issue_type="vocabulary_mismatch", severity="transform_required",
        title="Resource type: DCMI Type / NATO codes vs INSPIRE dataset | series | service",
        description=(
            "INSPIRE resourceType only accepts three values: 'dataset', 'series', or "
            "'service'. ADatP-5636 type accepts DCMI Type Vocabulary (12 terms) or "
            "NATO-specific codes. Most document types (Report, Plan, Assessment, Image) "
            "must be mapped to 'dataset' or dropped if the resource is neither a dataset "
            "nor a service. This is a significant semantic narrowing."
        ),
        source_vocab="DCMI Type Vocabulary (12 terms) or NATO resource type codes",
        target_vocab="dataset | series | service (INSPIRE MD_ScopeCode subset)",
        example_values=[
            ("Dataset", "dataset", "Direct match"),
            ("Service", "service", "Direct match"),
            ("Text", "dataset", "INSPIRE has no 'document' type — closest is dataset"),
            ("Report", "dataset", "NATO 'Report' has no INSPIRE equivalent — must become dataset"),
            ("Image", "dataset", "No INSPIRE image/raster type — becomes dataset"),
        ],
        transform_spec="Map: Service → service, Collection → series, all others → dataset. Semantic precision is lost for non-spatial document types.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="inspire",
        source_field="geographicReference", target_field="geographicBoundingBox",
        issue_type="format_change", severity="lossy",
        title="Geographic reference must be a WGS 84 bounding box with four decimal-degree components",
        description=(
            "INSPIRE geographicBoundingBox requires exactly four WGS 84 decimal-degree "
            "values: westBoundLongitude, eastBoundLongitude, southBoundLatitude, "
            "northBoundLatitude. ADatP-5636 geographicReference accepts bounding boxes, "
            "coordinate points, or named place identifiers. A point reference must be "
            "expanded to a bounding box (lossy — the point becomes a zero-area box). "
            "A named place identifier cannot be converted without a gazetteer lookup."
        ),
        source_vocab="Bounding box (decimal degrees) | coordinate point | named place identifier",
        target_vocab="WGS 84 bounding box: westBound, eastBound, southBound, northBound (decimal degrees)",
        example_values=[
            ("BBOX: 5.0°E 15.0°E 47.0°N 55.0°N", "W=5.0 E=15.0 S=47.0 N=55.0", "Direct mapping — bounding box already in correct format"),
            ("POINT: 10.0°E 51.0°N", "W=10.0 E=10.0 S=51.0 N=51.0", "Point → zero-area bounding box (lossy)"),
            ("NORFOLKVA, USA", None, "Named place — requires gazetteer lookup to derive coordinates"),
        ],
        transform_spec="Convert points to zero-area bounding boxes. Resolve named places via a gazetteer. Verify coordinates are in WGS 84.",
    ),

    # ── ADatP-5636 → ISO 19115 ──────────────────────────────────────────────

    FieldValueIssue(
        source_standard="adatp5636", target_standard="iso19115",
        source_field="language", target_field="dataIdentificationLanguage",
        issue_type="format_change", severity="transform_required",
        title="Language codes: ISO 639-3 alpha-3 vs ISO 639-2/B (same as INSPIRE)",
        description=(
            "ISO 19115-1:2014 specifies ISO 639-2 for language codes. As with INSPIRE, "
            "the bibliographic (B) variant is expected. For languages where ISO 639-2/T "
            "and ISO 639-2/B codes differ, the ADatP-5636 value will not conform."
        ),
        source_vocab="ISO 639-3 alpha-3 / ISO 639-2/T",
        target_vocab="ISO 639-2/B",
        example_values=[
            ("deu", "ger", "German: T→B"),
            ("fra", "fre", "French: T→B"),
            ("nld", "dut", "Dutch: T→B"),
        ],
        transform_spec="Apply ISO 639-2/T → ISO 639-2/B lookup table.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="iso19115",
        source_field="originatorConfidentialityLabel", target_field="classification",
        issue_type="vocabulary_mismatch", severity="lossy",
        title="ADatP-4774 classification structure vs ISO 19115 MD_ClassificationCode",
        description=(
            "ISO 19115 MD_ClassificationCode has a fixed vocabulary: unclassified, "
            "restricted, confidential, secret, topSecret, SBU, forOfficialUseOnly. "
            "The ADatP-4774 ConfidentialityInformation structure encodes the full "
            "NATO security policy with classification, releasability categories, and "
            "policy identifier. The releasability information (e.g. REL TO specific "
            "nations) and policy identifier are permanently lost in the conversion."
        ),
        source_vocab="ADatP-4774: PolicyIdentifier; Classification (NATO UNCLASSIFIED | RESTRICTED | CONFIDENTIAL | SECRET | COSMIC TOP SECRET); Category releasability tags",
        target_vocab="MD_ClassificationCode: unclassified | restricted | confidential | secret | topSecret | SBU | forOfficialUseOnly",
        example_values=[
            ("Classification=NATO UNCLASSIFIED; Category[TagName=Releasability,GenericValue=NATO]", "unclassified", "NATO UNCLASSIFIED → unclassified; releasability tag lost"),
            ("Classification=NATO RESTRICTED", "restricted", "Direct classification level mapping"),
            ("Classification=NATO CONFIDENTIAL; Category[GenericValue=FIN DEU GBR]", "confidential", "Nation-specific releasability (FIN, DEU, GBR) lost"),
            ("Classification=COSMIC TOP SECRET", "topSecret", "COSMIC marking lost — only topSecret level preserved"),
        ],
        transform_spec="Map NATO classification level to MD_ClassificationCode. Releasability categories and policy identifier cannot be expressed in ISO 19115 and must be discarded or placed in a free-text constraint field.",
    ),

    FieldValueIssue(
        source_standard="adatp5636", target_standard="iso19115",
        source_field="type", target_field="hierarchyLevel",
        issue_type="vocabulary_mismatch", severity="transform_required",
        title="Resource type: DCMI Type / NATO codes vs ISO 19115 MD_ScopeCode",
        description=(
            "ISO 19115 hierarchyLevel uses MD_ScopeCode, a vocabulary designed for "
            "geospatial data (dataset, series, service, tile, featureType, etc.). "
            "DCMI Type terms and NATO resource type codes do not map directly to "
            "MD_ScopeCode values. Document types like 'Text' or 'Report' have no "
            "precise MD_ScopeCode equivalent."
        ),
        source_vocab="DCMI Type Vocabulary or NATO resource type codes",
        target_vocab="MD_ScopeCode: attribute | attributeType | collectionHardware | collectionSession | dataset | series | nonGeographicDataset | dimensionGroup | feature | featureType | fieldSession | software | service | model | tile",
        example_values=[
            ("Dataset", "dataset", "Direct match"),
            ("Service", "service", "Direct match"),
            ("Text", "nonGeographicDataset", "Non-spatial document — best approximation"),
            ("Report", "nonGeographicDataset", "No scope code for documents"),
        ],
        transform_spec="Map DCMI/NATO types to MD_ScopeCode. Non-geospatial document types should use 'nonGeographicDataset'.",
    ),

    # ── ADatP-5636 → DCAT-AP-SE ─────────────────────────────────────────────

    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        source_field="language", target_field="dct:language",
        issue_type="uri_required", severity="transform_required",
        title="Language: ISO 639-3 alpha-3 codes must become EU Language NAL URIs",
        description=(
            "ADatP-5636 encodes language as an ISO 639-3 three-letter code (eng, fra, deu). "
            "DCAT-AP-SE requires a URI from the EU Publications Office language Named Authority "
            "List (e.g. http://publications.europa.eu/resource/authority/language/ENG). "
            "This is the same transform as DCAT-AP but explicitly required by the Swedish portal."
        ),
        source_vocab="ISO 639-3 alpha-3 codes (eng, fra, deu, nld, …)",
        target_vocab="EU Language NAL URIs (http://publications.europa.eu/resource/authority/language/ENG, …)",
        example_values=[
            ("eng", "http://publications.europa.eu/resource/authority/language/ENG", "Standard case"),
            ("fra", "http://publications.europa.eu/resource/authority/language/FRA", "Standard case"),
            ("swe", "http://publications.europa.eu/resource/authority/language/SWE", "Swedish — common in SE context"),
            ("deu", "http://publications.europa.eu/resource/authority/language/DEU", "Standard case"),
        ],
        transform_spec="Map ISO 639-3 to the EU Language NAL URI pattern: http://publications.europa.eu/resource/authority/language/{CODE.upper()}",
    ),
    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        source_field="publisher", target_field="dct:publisher",
        issue_type="uri_required", severity="transform_required",
        title="Publisher: free-text name must become a foaf:Agent URI",
        description=(
            "ADatP-5636 publisher is a free-text organisation name. DCAT-AP-SE requires "
            "a URI identifying a foaf:Agent — for Swedish public sector organisations this "
            "should be the organisation's URI (often based on the organisation number). "
            "Publisher is also mandatory in SE, so missing values block import entirely."
        ),
        source_vocab="Free-text organisation name",
        target_vocab="foaf:Agent URI, e.g., https://organization.digg.se/org/2021002520",
        example_values=[
            ("HQ AIRCOM", "", "No standard URI — must be manually assigned"),
            ("NATO Communications and Information Agency", "", "No Swedish org number URI"),
        ],
        transform_spec="Map each organisation to a URI in a maintained authority file. For Swedish receivers, use the Swedish organisation number URI scheme.",
    ),
    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        source_field="accessRights", target_field="dct:accessRights",
        issue_type="vocabulary_mismatch", severity="transform_required",
        title="Access rights: NATO free text vs EU Access Rights NAL URI",
        description=(
            "ADatP-5636 accessRights is a free-text field encoding NATO access policies. "
            "DCAT-AP-SE requires a URI from the EU Publications Office Access Rights NAL. "
            "NATO classification levels approximately map to the three SE values, but "
            "NATO-specific caveats (REL TO, NF, NATO CONFIDENTIAL) have no EU NAL equivalent."
        ),
        source_vocab="Free text: 'Authorised NATO personnel only', 'NATO UNCLASSIFIED', etc.",
        target_vocab="EU Access Rights NAL: PUBLIC | RESTRICTED | NON_PUBLIC",
        example_values=[
            ("NATO UNCLASSIFIED", "http://publications.europa.eu/resource/authority/access-right/PUBLIC", "Approximate mapping"),
            ("NATO RESTRICTED", "http://publications.europa.eu/resource/authority/access-right/RESTRICTED", "Approximate mapping"),
            ("NATO CONFIDENTIAL", "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC", "Classification caveats lost"),
            ("REL TO FVEY", "", "No EU NAL equivalent — releasability caveats cannot be expressed"),
        ],
        transform_spec="Map classification level to EU Access Rights URI. Accept information loss for caveats. Document the mapping policy.",
    ),
    FieldValueIssue(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        source_field="geographicReference", target_field="dct:spatial",
        issue_type="uri_required", severity="transform_required",
        title="Geographic reference: multiple NATO formats vs Geonames URI (SE preference)",
        description=(
            "ADatP-5636 geographicReference supports MGRS, UTM, WGS84-DD, WGS84-DMS, "
            "GeoJSON, WKT, and GeoNames. DCAT-AP-SE recommends Geonames URIs for "
            "Swedish localities, with EU Countries NAL / NUTS as alternatives. "
            "Only existing Geonames values transfer directly — coordinate-based formats "
            "cannot be converted to a named-place URI without reverse geocoding."
        ),
        source_vocab="MGRS, UTM, WGS84-DD, WGS84-DMS, GeoJSON, WKT, GeoNames URI",
        target_vocab="Geonames URI (preferred), EU Countries NAL, NUTS",
        example_values=[
            ("https://sws.geonames.org/2661886/", "https://sws.geonames.org/2661886/", "Already a Geonames URI — direct transfer"),
            ("59.3293N 18.0686E", "", "WGS84-DD coordinate — needs reverse geocoding to Geonames URI"),
            ("33UUP09", "", "MGRS grid reference — not convertible to Geonames URI without lookup"),
        ],
        transform_spec="If value is already a Geonames URI, transfer directly. Otherwise reverse-geocode or manually assign the nearest Geonames/NUTS URI.",
    ),
]


def get_value_issues(id_a: str, id_b: str) -> List[FieldValueIssue]:
    """Return value-level issues for both directions of a standard pair."""
    ids = {id_a, id_b}
    return [v for v in VALUE_ISSUES
            if v.source_standard in ids and v.target_standard in ids]


@dataclass
class CrosswalkEntry:
    source_standard: str
    source_field: str
    target_standard: str
    target_field: str        # empty string means no equivalent
    mapping_type: str        # exact | similar | partial | none
    notes: str = ""


@dataclass
class ConflictEntry:
    """
    A known interoperability conflict between two standards.

    conflict_type:
      mandatory_gap        — field mandatory in source, no equivalent in target;
                             a conformant source record cannot be a conformant target record
      vocabulary           — same concept but incompatible controlled vocabularies/encodings;
                             direct value transfer fails without a lookup table
      obligation_inversion — field mandatory in target but optional/absent in source;
                             source records may be missing values the target requires
      structural           — fundamental structural incompatibility (e.g. security layer
                             with no analogue in target standard)
      domain_mismatch      — fields appear to map but serve orthogonal purposes in their
                             respective domains; mapping produces misleading results

    severity:
      blocking             — prevents full interoperability; conformant records in source
                             CANNOT be made fully conformant in target without data loss
      lossy                — conversion is possible but data is degraded or partially lost
      transform_required   — interoperable only after a well-defined transformation step
    """
    source_standard: str
    target_standard: str
    conflict_type: str   # see above
    severity: str        # blocking | lossy | transform_required
    title: str
    source_field: str = ""
    target_field: str = ""
    description: str = ""


# ---------------------------------------------------------------------------
# ADatP-5636 → Dublin Core
# ---------------------------------------------------------------------------
ADATP5636_TO_DUBLIN_CORE: List[CrosswalkEntry] = [
    # ── Core descriptive fields ───────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "title", "dublin_core", "title", "exact",
                   "Both express the name of the resource. NCMS restricts to ONE title; DC allows MANY."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "dublin_core", "alternative", "exact",
                   "NCMS alternativeTitle maps directly to DCTerms:alternative (alternative name / acronym)."),
    CrosswalkEntry("adatp5636", "creator", "dublin_core", "creator", "similar",
                   "NCMS requires PointOfContact structure; DC allows free text. Semantics are equivalent."),
    CrosswalkEntry("adatp5636", "publisher", "dublin_core", "publisher", "similar",
                   "NCMS requires PointOfContact; DC allows free text. Same semantics."),
    CrosswalkEntry("adatp5636", "contributor", "dublin_core", "contributor", "similar",
                   "Both express contributing agents with secondary roles. NCMS uses PointOfContact structure."),
    CrosswalkEntry("adatp5636", "description", "dublin_core", "description", "exact",
                   "Both provide a textual account of the resource content."),
    CrosswalkEntry("adatp5636", "abstract", "dublin_core", "abstract", "exact",
                   "DCTerms:abstract is an exact equivalent for NCMS abstract (a summary of the resource)."),
    CrosswalkEntry("adatp5636", "tableOfContents", "dublin_core", "tableOfContents", "exact",
                   "DCTerms:tableOfContents is an exact match for NCMS tableOfContents."),
    CrosswalkEntry("adatp5636", "subject", "dublin_core", "subject", "exact",
                   "Both describe the topic using keywords or classification codes."),
    CrosswalkEntry("adatp5636", "keyword", "dublin_core", "subject", "similar",
                   "NCMS keyword is informal; DC subject is the combined keyword/subject element."),
    CrosswalkEntry("adatp5636", "type", "dublin_core", "type", "similar",
                   "NCMS may use NATO-specific type codes; DC recommends DCMI Type Vocabulary."),
    # ── Identification ────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "identifier", "dublin_core", "identifier", "exact",
                   "Both express a unique identifier; NCMS recommends NATO URN scheme."),
    CrosswalkEntry("adatp5636", "language", "dublin_core", "language", "exact",
                   "Both reference ISO 639 language codes."),
    # ── Format ───────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "mediaFormat", "dublin_core", "format", "exact",
                   "NCMS mediaFormat = MIME type; DC format = file format. Semantically equivalent."),
    CrosswalkEntry("adatp5636", "extent", "dublin_core", "extent", "exact",
                   "DCTerms:extent is an exact match — size or duration of the resource."),
    CrosswalkEntry("adatp5636", "medium", "dublin_core", "medium", "exact",
                   "DCTerms:medium is an exact match — physical medium or material carrier."),
    CrosswalkEntry("adatp5636", "hasFormat", "dublin_core", "hasFormat", "exact",
                   "DCTerms:hasFormat is identical — a related resource in another format."),
    CrosswalkEntry("adatp5636", "isFormatOf", "dublin_core", "isFormatOf", "exact",
                   "DCTerms:isFormatOf is identical — inverse of hasFormat."),
    # ── Dates ─────────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "dateCreated", "dublin_core", "created", "exact",
                   "DCTerms:created is the exact equivalent for the date of resource creation."),
    CrosswalkEntry("adatp5636", "dateIssued", "dublin_core", "issued", "exact",
                   "DCTerms:issued is the exact equivalent for the formal publication date."),
    CrosswalkEntry("adatp5636", "dateModified", "dublin_core", "modified", "exact",
                   "DCTerms:modified is the exact equivalent for the last modification date."),
    CrosswalkEntry("adatp5636", "dateAccepted", "dublin_core", "dateAccepted", "exact",
                   "DCTerms:dateAccepted is an exact match — date of formal acceptance."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "dublin_core", "dateCopyrighted", "exact",
                   "DCTerms:dateCopyrighted is an exact match — year of copyright assertion."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "dublin_core", "dateSubmitted", "exact",
                   "DCTerms:dateSubmitted is an exact match — date submitted for review."),
    # ── Rights ───────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "rights", "dublin_core", "rights", "exact",
                   "Both express rights information over the resource."),
    CrosswalkEntry("adatp5636", "accessRights", "dublin_core", "accessRights", "exact",
                   "DCTerms:accessRights is an exact match — information about access restrictions."),
    CrosswalkEntry("adatp5636", "license", "dublin_core", "license", "exact",
                   "DCTerms:license is an exact match — a legal document giving access permissions."),
    CrosswalkEntry("adatp5636", "rightsHolder", "dublin_core", "rightsHolder", "exact",
                   "DCTerms:rightsHolder is an exact match — person or organisation owning rights."),
    # ── Provenance & standards compliance ────────────────────────────────────
    CrosswalkEntry("adatp5636", "provenance", "dublin_core", "provenance", "exact",
                   "DCTerms:provenance is an exact match — statement of changes in ownership/custody."),
    CrosswalkEntry("adatp5636", "conformsTo", "dublin_core", "conformsTo", "exact",
                   "DCTerms:conformsTo is an exact match — an established standard the resource conforms to."),
    CrosswalkEntry("adatp5636", "source", "dublin_core", "source", "exact",
                   "Both indicate a source resource from which this is derived."),
    # ── Coverage ─────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "geographicReference", "dublin_core", "coverage", "partial",
                   "NCMS geographicReference is structured (with encoding scheme); DC coverage is free text."),
    CrosswalkEntry("adatp5636", "timePeriod", "dublin_core", "coverage", "partial",
                   "NCMS timePeriod uses DCMI Period format; DC coverage includes both spatial and temporal."),
    # ── Generic relation ─────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "relation", "dublin_core", "relation", "exact",
                   "Both express a generic relationship to another resource."),
    # ── Specific relations (DCTerms refinements — all exact matches) ─────────
    CrosswalkEntry("adatp5636", "hasPart", "dublin_core", "hasPart", "exact",
                   "DCTerms:hasPart is identical — a resource included in this one."),
    CrosswalkEntry("adatp5636", "isPartOf", "dublin_core", "isPartOf", "exact",
                   "DCTerms:isPartOf is identical — a resource in which this is included."),
    CrosswalkEntry("adatp5636", "hasVersion", "dublin_core", "hasVersion", "exact",
                   "DCTerms:hasVersion is identical — a version, edition, or adaptation."),
    CrosswalkEntry("adatp5636", "isVersionOf", "dublin_core", "isVersionOf", "exact",
                   "DCTerms:isVersionOf is identical — the resource this is a version of."),
    CrosswalkEntry("adatp5636", "references", "dublin_core", "references", "exact",
                   "DCTerms:references is identical — a resource referenced, cited, or pointed to."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "dublin_core", "isReferencedBy", "exact",
                   "DCTerms:isReferencedBy is identical — a resource that references this one."),
    CrosswalkEntry("adatp5636", "replaces", "dublin_core", "replaces", "exact",
                   "DCTerms:replaces is identical — a resource this one supplants or supersedes."),
    CrosswalkEntry("adatp5636", "requires", "dublin_core", "requires", "exact",
                   "DCTerms:requires is identical — a resource required by this one."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "dublin_core", "isRequiredBy", "exact",
                   "DCTerms:isRequiredBy is identical — a resource that requires this one."),
    # ── Security / classification (no DC equivalent) ─────────────────────────
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "dublin_core", "", "none",
                   "No Dublin Core equivalent. DC has no security classification concept."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "dublin_core", "", "none",
                   "No Dublin Core equivalent. DC has no metadata-level security label concept."),
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "dublin_core", "", "none",
                   "No Dublin Core equivalent. DC has no security classification concept."),
    # ── Records management (no DC equivalent) ────────────────────────────────
    CrosswalkEntry("adatp5636", "recordsDisposition", "dublin_core", "", "none",
                   "Records management concept not present in Dublin Core."),
    CrosswalkEntry("adatp5636", "dateDisposition", "dublin_core", "", "none",
                   "Records management concept not present in Dublin Core."),
    CrosswalkEntry("adatp5636", "version", "dublin_core", "", "none",
                   "No dc: or dcterms: version element; use hasVersion/isVersionOf for resource relations."),
    # ── NATO-specific operational context (no DC equivalent) ─────────────────
    CrosswalkEntry("adatp5636", "contextActivity", "dublin_core", "", "none",
                   "NATO operational/exercise/project context; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "custodian", "dublin_core", "", "none",
                   "NATO records custodian concept; no direct Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "countryCode", "dublin_core", "", "none",
                   "ISO 3166 country code; DC coverage may capture this loosely but no exact equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction", "dublin_core", "", "none",
                   "Redaction metadata concept; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "dublin_core", "", "none",
                   "Redaction metadata concept; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "dublin_core", "", "none",
                   "Redaction metadata concept; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "recordsHold", "dublin_core", "", "none",
                   "Legal hold / litigation hold concept; no Dublin Core equivalent."),
    # ── Additional fields with DCTerms equivalents ────────────────────────────
    CrosswalkEntry("adatp5636", "dateValid", "dublin_core", "valid", "exact",
                   "DCTerms:valid is an exact match — date (often a range) during which the resource is valid."),
    CrosswalkEntry("adatp5636", "dateAvailable", "dublin_core", "available", "exact",
                   "DCTerms:available is an exact match — date the resource became or will become available."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "dublin_core", "accrualPeriodicity", "exact",
                   "DCTerms:accrualPeriodicity is an exact match — the frequency at which the resource is updated."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "dublin_core", "identifier", "similar",
                   "Dublin Core allows multiple identifiers in different schemes; "
                   "an external identifier is a valid dc:identifier value."),
    CrosswalkEntry("adatp5636", "copyright", "dublin_core", "rights", "similar",
                   "A copyright statement is a form of rights information; dc:rights or dcterms:rights is the target."),
    CrosswalkEntry("adatp5636", "subjectCategory", "dublin_core", "subject", "similar",
                   "A formal subject classification category maps to dc:subject / dcterms:subject."),
    CrosswalkEntry("adatp5636", "subtitle", "dublin_core", "alternative", "partial",
                   "A subtitle is a form of alternative title; DCTerms:alternative is the closest match."),
    CrosswalkEntry("adatp5636", "placeName", "dublin_core", "spatial", "partial",
                   "A named place maps to DCTerms:spatial (a spatial characteristic of the resource)."),
    CrosswalkEntry("adatp5636", "region", "dublin_core", "spatial", "partial",
                   "A named region maps to DCTerms:spatial."),
    # ── Remaining fields with no Dublin Core equivalent ───────────────────────
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "dublin_core", "", "none",
                   "Encoding scheme qualifier for geographic reference; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "dateAcquired", "dublin_core", "", "none",
                   "Acquisition date; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "dateClosed", "dublin_core", "", "none",
                   "Record closure date; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "dateCutOff", "dublin_core", "", "none",
                   "Information cut-off date; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "dateDeclared", "dublin_core", "", "none",
                   "Declaration date; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "dublin_core", "", "none",
                   "Planned next-version date; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "extentQualifier", "dublin_core", "", "none",
                   "Extent unit qualifier; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "authorizes", "dublin_core", "", "none",
                   "Authorization relation; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "dublin_core", "", "none",
                   "Authorization relation; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "dublin_core", "", "none",
                   "Definitional relation; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "dublin_core", "relation", "partial",
                   "DCTerms does not include isReplacedBy; the generic dcterms:relation is the closest option."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "dublin_core", "", "none",
                   "Definitional relation; no Dublin Core equivalent."),
    CrosswalkEntry("adatp5636", "status", "dublin_core", "", "none",
                   "Resource lifecycle status; no Dublin Core equivalent."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → DCAT-AP
# ---------------------------------------------------------------------------
ADATP5636_TO_DCAT_AP: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "title", "dcat_ap", "dct:title", "exact",
                   "Both mandatory; DCAT-AP uses DCTerms namespace prefix."),
    CrosswalkEntry("adatp5636", "creator", "dcat_ap", "dct:creator", "similar",
                   "NCMS PointOfContact structure; DCAT-AP uses foaf:Agent URI. Semantics equivalent."),
    CrosswalkEntry("adatp5636", "publisher", "dcat_ap", "dct:publisher", "similar",
                   "NCMS PointOfContact; DCAT-AP recommends URI from authority file."),
    CrosswalkEntry("adatp5636", "dateCreated", "dcat_ap", "dct:issued", "partial",
                   "DCAT-AP dct:issued corresponds to publication/issuance. "
                   "dateCreated is closer to creation date (no direct equivalent in DCAT-AP)."),
    CrosswalkEntry("adatp5636", "dateIssued", "dcat_ap", "dct:issued", "exact",
                   "Both express the formal publication date."),
    CrosswalkEntry("adatp5636", "dateModified", "dcat_ap", "dct:modified", "exact",
                   "Both express the date of last modification."),
    CrosswalkEntry("adatp5636", "description", "dcat_ap", "dct:description", "exact",
                   "Both mandatory in their respective standards; semantically equivalent."),
    CrosswalkEntry("adatp5636", "keyword", "dcat_ap", "dcat:keyword", "exact",
                   "DCAT-AP has a dedicated keyword property; NCMS keyword maps exactly."),
    CrosswalkEntry("adatp5636", "subject", "dcat_ap", "dcat:keyword", "similar",
                   "NCMS subject uses controlled vocabulary; DCAT-AP keyword is free text or theme URI."),
    CrosswalkEntry("adatp5636", "language", "dcat_ap", "dct:language", "similar",
                   "NCMS uses ISO 639-3; DCAT-AP recommends EU Language NAL URI."),
    CrosswalkEntry("adatp5636", "identifier", "dcat_ap", "dct:identifier", "exact",
                   "Both express a persistent identifier."),
    CrosswalkEntry("adatp5636", "type", "dcat_ap", "dct:type", "similar",
                   "NCMS uses NATO type codes; DCAT-AP recommends EU Dataset Type NAL URI."),
    CrosswalkEntry("adatp5636", "mediaFormat", "dcat_ap", "dcat:mediaType", "exact",
                   "Both express IANA media types (MIME types)."),
    CrosswalkEntry("adatp5636", "rights", "dcat_ap", "dct:rights", "exact",
                   "Both express general rights information."),
    CrosswalkEntry("adatp5636", "accessRights", "dcat_ap", "dct:accessRights", "similar",
                   "NCMS free text; DCAT-AP requires URI from EU Access Rights NAL."),
    CrosswalkEntry("adatp5636", "contributor", "dcat_ap", "dct:contributor", "exact",
                   "Same semantics; format differs (PointOfContact vs URI)."),
    CrosswalkEntry("adatp5636", "source", "dcat_ap", "dct:source", "exact",
                   "Both indicate a source dataset."),
    CrosswalkEntry("adatp5636", "relation", "dcat_ap", "dct:relation", "exact",
                   "Generic relationship; same semantics."),
    CrosswalkEntry("adatp5636", "provenance", "dcat_ap", "dct:provenance", "exact",
                   "Both describe the lineage/provenance of the resource."),
    CrosswalkEntry("adatp5636", "geographicReference", "dcat_ap", "dct:spatial", "similar",
                   "NCMS structured geo reference; DCAT-AP uses URI (GeoNames/NUTS/EU Countries NAL)."),
    CrosswalkEntry("adatp5636", "license", "dcat_ap", "dct:license", "exact",
                   "Both express a licence URI."),
    CrosswalkEntry("adatp5636", "conformsTo", "dcat_ap", "dct:conformsTo", "exact",
                   "Both indicate a standard/specification the resource conforms to."),
    CrosswalkEntry("adatp5636", "hasVersion", "dcat_ap", "dct:hasVersion", "exact",
                   "Both indicate a version of the resource."),
    CrosswalkEntry("adatp5636", "isVersionOf", "dcat_ap", "dct:isVersionOf", "exact",
                   "Both indicate the resource is a version of another."),
    CrosswalkEntry("adatp5636", "hasPart", "dcat_ap", "dct:hasPart", "exact",
                   "Both indicate a part of the resource."),
    CrosswalkEntry("adatp5636", "isPartOf", "dcat_ap", "dct:isPartOf", "exact",
                   "Both indicate the resource is part of another."),
    CrosswalkEntry("adatp5636", "version", "dcat_ap", "owl:versionInfo", "similar",
                   "NCMS version string; DCAT-AP owl:versionInfo. Similar semantics."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "dcat_ap", "dct:accessRights", "partial",
                   "NCMS has structured confidentiality label (ADatP-4774); DCAT-AP has URI-based access rights. "
                   "Only a partial mapping — classification level can inform access rights category."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "dcat_ap", "", "none",
                   "No DCAT-AP equivalent; DCAT-AP does not have a metadata-level security label."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "dcat_ap", "", "none",
                   "Records management concept; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateDisposition", "dcat_ap", "", "none",
                   "Records management concept; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "timePeriod", "dcat_ap", "dct:temporal", "similar",
                   "NCMS DCMI Period notation; DCAT-AP dct:PeriodOfTime with startDate/endDate."),
    CrosswalkEntry("adatp5636", "accrualPeriodicity", "dcat_ap", "dct:accrualPeriodicity", "exact",
                   "Both express update frequency."),
    # ── Additional descriptive fields ─────────────────────────────────────────
    CrosswalkEntry("adatp5636", "abstract", "dcat_ap", "dct:description", "similar",
                   "DCAT-AP has no dedicated abstract field; dct:description is the closest element."),
    CrosswalkEntry("adatp5636", "tableOfContents", "dcat_ap", "dct:description", "partial",
                   "No dedicated tableOfContents in DCAT-AP; content can be added to dct:description."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "dcat_ap", "dct:title", "partial",
                   "DCAT-AP allows repeatable dct:title; an alternative title can be expressed as "
                   "an additional title with a language tag or role annotation."),
    CrosswalkEntry("adatp5636", "subtitle", "dcat_ap", "dct:title", "partial",
                   "No dedicated subtitle field; subtitle can be appended to the primary title."),
    CrosswalkEntry("adatp5636", "subjectCategory", "dcat_ap", "dcat:theme", "similar",
                   "NCMS subjectCategory (classification scheme controlled vocabulary) maps to "
                   "DCAT-AP dcat:theme (EU Data Theme or other controlled vocabulary URI)."),
    # ── External identification ───────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "externalIdentifier", "dcat_ap", "adms:identifier", "exact",
                   "ADMS:identifier is specifically designed for secondary or external identifiers "
                   "in other naming schemes — an exact match for NCMS externalIdentifier."),
    # ── Relations ────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "isReferencedBy", "dcat_ap", "dct:isReferencedBy", "exact",
                   "DCAT-AP explicitly includes dct:isReferencedBy; exact match."),
    CrosswalkEntry("adatp5636", "references", "dcat_ap", "dct:relation", "partial",
                   "DCAT-AP has no specific dct:references property; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "replaces", "dcat_ap", "dct:relation", "partial",
                   "DCAT-AP has no dct:replaces property; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "dcat_ap", "dct:relation", "partial",
                   "DCAT-AP has no dct:isReplacedBy property; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "requires", "dcat_ap", "dct:relation", "partial",
                   "DCAT-AP has no dct:requires property; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "dcat_ap", "dct:relation", "partial",
                   "DCAT-AP has no dct:isRequiredBy property; dct:relation is the closest generic equivalent."),
    # ── Rights ───────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "copyright", "dcat_ap", "dct:rights", "similar",
                   "NCMS copyright statement maps to the general dct:rights field."),
    CrosswalkEntry("adatp5636", "rightsHolder", "dcat_ap", "", "none",
                   "DCAT-AP 2.1.1 does not include a dedicated dct:rightsHolder property at dataset level."),
    # ── Spatial ──────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "countryCode", "dcat_ap", "dct:spatial", "partial",
                   "An ISO 3166 country code is a valid value for dct:spatial; "
                   "DCAT-AP recommends GeoNames or EU Countries Named Authority List URIs."),
    CrosswalkEntry("adatp5636", "placeName", "dcat_ap", "dct:spatial", "partial",
                   "A named place can be expressed as a dct:spatial value using a GeoNames URI."),
    CrosswalkEntry("adatp5636", "region", "dcat_ap", "dct:spatial", "partial",
                   "A named administrative region can be expressed as a dct:spatial value using "
                   "a GeoNames or NUTS URI."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "dcat_ap", "", "none",
                   "Encoding scheme qualifier for geographic reference; no DCAT-AP equivalent."),
    # ── Dates ────────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "dateAvailable", "dcat_ap", "dct:issued", "partial",
                   "Availability date is closest to dct:issued (formal publication/issuance date)."),
    CrosswalkEntry("adatp5636", "dateValid", "dcat_ap", "dct:temporal", "partial",
                   "A validity period can be expressed as a temporal coverage (dct:PeriodOfTime)."),
    CrosswalkEntry("adatp5636", "dateAccepted", "dcat_ap", "", "none",
                   "No DCAT-AP equivalent for formal acceptance date."),
    CrosswalkEntry("adatp5636", "dateAcquired", "dcat_ap", "", "none",
                   "Acquisition date is a records management concept; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateClosed", "dcat_ap", "", "none",
                   "Record closure date; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "dcat_ap", "", "none",
                   "Copyright year is implicit in dct:rights; DCAT-AP has no dedicated field."),
    CrosswalkEntry("adatp5636", "dateCutOff", "dcat_ap", "", "none",
                   "Information cut-off date is a NATO-specific concept; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateDeclared", "dcat_ap", "", "none",
                   "Declaration date is a NATO records concept; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "dcat_ap", "", "none",
                   "Planned next-version date; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "dcat_ap", "", "none",
                   "Submission date is a records management concept; no DCAT-AP equivalent."),
    # ── Physical format ───────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "extent", "dcat_ap", "dcat:byteSize", "partial",
                   "Digital extent (file size) can be expressed as dcat:byteSize on a distribution. "
                   "Non-digital extent (page count, duration) has no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "extentQualifier", "dcat_ap", "", "none",
                   "Extent unit qualifier; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "medium", "dcat_ap", "", "none",
                   "Physical carrier medium; DCAT-AP focuses on digital datasets and has no medium field."),
    CrosswalkEntry("adatp5636", "hasFormat", "dcat_ap", "", "none",
                   "DCAT-AP models format variants through dcat:distribution with dct:format — "
                   "a different approach; there is no dct:hasFormat relation at dataset level."),
    CrosswalkEntry("adatp5636", "isFormatOf", "dcat_ap", "", "none",
                   "No dct:isFormatOf at dataset level in DCAT-AP; format variants are distributions."),
    # ── Status / lifecycle ────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "updatingFrequency", "dcat_ap", "dct:accrualPeriodicity", "exact",
                   "Both express the periodicity of resource updates using frequency vocabularies."),
    CrosswalkEntry("adatp5636", "status", "dcat_ap", "adms:status", "similar",
                   "NCMS lifecycle status maps to adms:status; DCAT-AP uses this at distribution level "
                   "but it can represent dataset lifecycle status as well."),
    # ── NATO/security-specific — no DCAT-AP equivalent ────────────────────────
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "dcat_ap", "", "none",
                   "NATO-specific security label; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "custodian", "dcat_ap", "", "none",
                   "Records custodian role; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "contextActivity", "dcat_ap", "", "none",
                   "NATO operational/exercise/project context; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "authorizes", "dcat_ap", "", "none",
                   "Authorization relation; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "dcat_ap", "", "none",
                   "Authorization relation; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "dcat_ap", "", "none",
                   "Definitional relation to a standard; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "dcat_ap", "", "none",
                   "Definitional relation; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction", "dcat_ap", "", "none",
                   "Redaction metadata; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "dcat_ap", "", "none",
                   "Redaction metadata; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "dcat_ap", "", "none",
                   "Redaction metadata; no DCAT-AP equivalent."),
    CrosswalkEntry("adatp5636", "recordsHold", "dcat_ap", "", "none",
                   "Legal/litigation hold; no DCAT-AP equivalent."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → ISO 19115-1
# ---------------------------------------------------------------------------
ADATP5636_TO_ISO19115: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "title", "iso19115", "citationTitle", "exact",
                   "Both mandatory expressions of the resource name."),
    CrosswalkEntry("adatp5636", "creator", "iso19115", "pointOfContact", "similar",
                   "NCMS creator = CI_ResponsibleParty with role=originator. ISO 19115 uses pointOfContact."),
    CrosswalkEntry("adatp5636", "publisher", "iso19115", "pointOfContact", "similar",
                   "NCMS publisher = CI_ResponsibleParty with role=publisher. ISO 19115 uses pointOfContact."),
    CrosswalkEntry("adatp5636", "dateCreated", "iso19115", "citationDate", "similar",
                   "ISO 19115 CI_Citation.date with dateType=creation. Semantically equivalent."),
    CrosswalkEntry("adatp5636", "dateIssued", "iso19115", "citationDate", "similar",
                   "ISO 19115 CI_Citation.date with dateType=publication."),
    CrosswalkEntry("adatp5636", "dateModified", "iso19115", "citationDate", "similar",
                   "ISO 19115 CI_Citation.date with dateType=revision."),
    CrosswalkEntry("adatp5636", "abstract", "iso19115", "abstract", "exact",
                   "Both mandatory summaries of the resource content."),
    CrosswalkEntry("adatp5636", "description", "iso19115", "abstract", "partial",
                   "NCMS description is broader; ISO 19115 abstract is the primary narrative field."),
    CrosswalkEntry("adatp5636", "keyword", "iso19115", "descriptiveKeywords", "similar",
                   "NCMS keyword maps to ISO 19115 MD_Keywords.keyword within descriptiveKeywords element."),
    CrosswalkEntry("adatp5636", "subject", "iso19115", "descriptiveKeywords", "partial",
                   "NCMS subject uses classification scheme; ISO 19115 descriptiveKeywords includes type=theme."),
    CrosswalkEntry("adatp5636", "language", "iso19115", "dataIdentificationLanguage", "exact",
                   "Both mandatory language fields using ISO 639 codes."),
    CrosswalkEntry("adatp5636", "identifier", "iso19115", "fileIdentifier", "similar",
                   "Both identify the record; ISO 19115 fileIdentifier is for the metadata record, "
                   "citationIdentifier is for the resource itself."),
    CrosswalkEntry("adatp5636", "type", "iso19115", "hierarchyLevel", "similar",
                   "NCMS type describes resource genre; ISO 19115 hierarchyLevel uses MD_ScopeCode."),
    CrosswalkEntry("adatp5636", "mediaFormat", "iso19115", "resourceFormat", "partial",
                   "NCMS MIME type; ISO 19115 MD_Format includes name, version, specification."),
    CrosswalkEntry("adatp5636", "rights", "iso19115", "resourceConstraints", "partial",
                   "NCMS rights free text; ISO 19115 uses MD_Constraints/MD_LegalConstraints structure."),
    CrosswalkEntry("adatp5636", "accessRights", "iso19115", "accessConstraints", "similar",
                   "NCMS accessRights; ISO 19115 MD_LegalConstraints.accessConstraints with MD_RestrictionCode."),
    CrosswalkEntry("adatp5636", "contributor", "iso19115", "pointOfContact", "partial",
                   "NCMS contributor = CI_ResponsibleParty with role=collaborator/contributor."),
    CrosswalkEntry("adatp5636", "relation", "iso19115", "aggregationInfo", "partial",
                   "NCMS relation; ISO 19115 MD_AggregateInformation with associationType."),
    CrosswalkEntry("adatp5636", "provenance", "iso19115", "lineage", "similar",
                   "NCMS provenance; ISO 19115 LI_Lineage.statement. Similar concepts."),
    CrosswalkEntry("adatp5636", "geographicReference", "iso19115", "extent", "similar",
                   "NCMS geographicReference; ISO 19115 EX_GeographicBoundingBox or EX_GeographicDescription."),
    CrosswalkEntry("adatp5636", "timePeriod", "iso19115", "extent", "similar",
                   "NCMS timePeriod; ISO 19115 EX_TemporalExtent within extent element."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "iso19115", "classification", "partial",
                   "NCMS structured ADatP-4774 label; ISO 19115 MD_SecurityConstraints.classification "
                   "uses MD_ClassificationCode. Only the classification level maps directly."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "iso19115", "", "none",
                   "ISO 19115 does not have a metadata-record confidentiality label concept."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "iso19115", "", "none",
                   "Records management concept not covered in ISO 19115."),
    CrosswalkEntry("adatp5636", "conformsTo", "iso19115", "", "none",
                   "No direct ISO 19115 equivalent; DQ_ConformanceResult covers conformance testing, not declaration."),
    CrosswalkEntry("adatp5636", "version", "iso19115", "", "none",
                   "No direct ISO 19115 equivalent; version may appear in citationIdentifier or metadataStandardVersion."),
    CrosswalkEntry("adatp5636", "license", "iso19115", "resourceConstraints", "partial",
                   "NCMS license URI; ISO 19115 MD_LegalConstraints uses MD_RestrictionCode."),
    CrosswalkEntry("adatp5636", "topicCategory", "iso19115", "topicCategory", "exact",
                   "Both use ISO 19115 MD_TopicCategoryCode values."),
    CrosswalkEntry("adatp5636", "spatialResolution", "iso19115", "spatialResolution", "exact",
                   "Same MD_Resolution structure."),
    # ── Additional descriptive and identification ──────────────────────────────
    CrosswalkEntry("adatp5636", "alternativeTitle", "iso19115", "alternateTitle", "exact",
                   "ISO 19115 CI_Citation.alternateTitle is an exact match for an alternative name."),
    CrosswalkEntry("adatp5636", "subtitle", "iso19115", "alternateTitle", "partial",
                   "Subtitle can be expressed as an alternateTitle with an appropriate qualifier."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "iso19115", "citationIdentifier", "similar",
                   "ISO 19115 CI_Citation.identifier captures external identifiers in other schemes; "
                   "semantically equivalent to NCMS externalIdentifier."),
    CrosswalkEntry("adatp5636", "subjectCategory", "iso19115", "topicCategory", "similar",
                   "NCMS subjectCategory (formal classification scheme) maps to ISO 19115 "
                   "topicCategory (MD_TopicCategoryCode) when the source vocabulary aligns."),
    # ── Lifecycle and maintenance ─────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "status", "iso19115", "status", "exact",
                   "ISO 19115 MD_Identification.status uses MD_ProgressCode; "
                   "NCMS status uses a similar lifecycle vocabulary. Exact conceptual match."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "iso19115", "resourceMaintenance", "similar",
                   "NCMS updatingFrequency maps to ISO 19115 MD_MaintenanceInformation."
                   "maintenanceAndUpdateFrequency (MD_MaintenanceFrequencyCode)."),
    # ── Provenance and source ─────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "source", "iso19115", "lineage", "similar",
                   "Data source information belongs in ISO 19115 LI_Lineage.source "
                   "(LI_Source with sourceDescription and sourceCitation)."),
    # ── Rights ───────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "copyright", "iso19115", "resourceConstraints", "partial",
                   "Copyright statement is expressed in MD_LegalConstraints.otherConstraints."),
    CrosswalkEntry("adatp5636", "rightsHolder", "iso19115", "pointOfContact", "partial",
                   "Rights holder can be expressed as a CI_ResponsibleParty with "
                   "role=owner within resourceConstraints/MD_LegalConstraints."),
    # ── Spatial ──────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "countryCode", "iso19115", "extent", "partial",
                   "A country code can be expressed as EX_GeographicDescription.geographicIdentifier "
                   "or as part of EX_GeographicBoundingBox within the extent element."),
    CrosswalkEntry("adatp5636", "placeName", "iso19115", "extent", "partial",
                   "A place name is expressed as EX_GeographicDescription.geographicIdentifier."),
    CrosswalkEntry("adatp5636", "region", "iso19115", "extent", "partial",
                   "A named region is expressed as EX_GeographicDescription.geographicIdentifier."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "iso19115", "extent", "partial",
                   "Encoding scheme qualifier for geographic reference; can annotate the reference "
                   "system within EX_GeographicDescription."),
    # ── Temporal ─────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "dateValid", "iso19115", "extent", "partial",
                   "Validity period maps to EX_TemporalExtent within the extent element."),
    CrosswalkEntry("adatp5636", "dateAvailable", "iso19115", "citationDate", "partial",
                   "Date the resource became available maps to CI_Date with dateType=available."),
    CrosswalkEntry("adatp5636", "dateAccepted", "iso19115", "citationDate", "partial",
                   "Formal acceptance date maps to CI_Date with an appropriate dateType code."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "iso19115", "citationDate", "partial",
                   "Copyright year maps to CI_Date with dateType=notKnown or a custom extension."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "iso19115", "citationDate", "partial",
                   "Submission date maps to CI_Date with an appropriate dateType code."),
    # ── Resource relations ────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "hasPart", "iso19115", "aggregationInfo", "partial",
                   "Part-whole relation captured in MD_AggregateInformation with "
                   "associationType=largerWorkCitation."),
    CrosswalkEntry("adatp5636", "isPartOf", "iso19115", "aggregationInfo", "partial",
                   "Part-of relation captured in MD_AggregateInformation with "
                   "associationType=partOfSeamlessDatabase or largerWorkCitation."),
    CrosswalkEntry("adatp5636", "hasVersion", "iso19115", "aggregationInfo", "partial",
                   "Version relation captured in MD_AggregateInformation with "
                   "associationType=revisionOf or series."),
    CrosswalkEntry("adatp5636", "isVersionOf", "iso19115", "aggregationInfo", "partial",
                   "Version-of relation captured in MD_AggregateInformation."),
    CrosswalkEntry("adatp5636", "references", "iso19115", "aggregationInfo", "partial",
                   "References relation captured in MD_AggregateInformation with "
                   "associationType=crossReference."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "iso19115", "aggregationInfo", "partial",
                   "IsReferencedBy relation captured in MD_AggregateInformation with "
                   "associationType=crossReference (inverse)."),
    CrosswalkEntry("adatp5636", "replaces", "iso19115", "aggregationInfo", "partial",
                   "Replaces relation captured in MD_AggregateInformation with "
                   "associationType=revisionOf."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "iso19115", "aggregationInfo", "partial",
                   "IsReplacedBy relation captured in MD_AggregateInformation."),
    CrosswalkEntry("adatp5636", "requires", "iso19115", "aggregationInfo", "partial",
                   "Dependency relation captured in MD_AggregateInformation with "
                   "associationType=dependency."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "iso19115", "aggregationInfo", "partial",
                   "IsRequiredBy relation captured in MD_AggregateInformation."),
    # ── Physical format ───────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "medium", "iso19115", "resourceFormat", "partial",
                   "Physical carrier medium is conceptually related to MD_Format; "
                   "ISO 19115 MD_Format covers format specification including medium."),
    CrosswalkEntry("adatp5636", "hasFormat", "iso19115", "aggregationInfo", "partial",
                   "Format variant relation captured in MD_AggregateInformation with "
                   "associationType=isComposedOf or similar."),
    CrosswalkEntry("adatp5636", "isFormatOf", "iso19115", "aggregationInfo", "partial",
                   "Inverse format variant relation in MD_AggregateInformation."),
    # ── No ISO 19115 equivalent ───────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "tableOfContents", "iso19115", "abstract", "partial",
                   "No dedicated tableOfContents element; content can be appended to the abstract."),
    CrosswalkEntry("adatp5636", "extentQualifier", "iso19115", "", "none",
                   "Extent unit qualifier has no direct ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "extent", "iso19115", "", "none",
                   "NCMS extent = file size / duration; ISO 19115 extent = spatial/temporal coverage. "
                   "Different concepts — no equivalent for file size in ISO 19115 core."),
    CrosswalkEntry("adatp5636", "dateAcquired", "iso19115", "", "none",
                   "Acquisition date is a records management concept; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "dateClosed", "iso19115", "", "none",
                   "Record closure date; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "dateCutOff", "iso19115", "", "none",
                   "Information cut-off date; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "dateDeclared", "iso19115", "", "none",
                   "Declaration date; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "iso19115", "", "none",
                   "Planned next-version date; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "dateDisposition", "iso19115", "", "none",
                   "Records disposal date; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "iso19115", "", "none",
                   "NATO-specific security label; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "custodian", "iso19115", "", "none",
                   "Records custodian role; ISO 19115 CI_RoleCode does not include a custodian role."),
    CrosswalkEntry("adatp5636", "contextActivity", "iso19115", "", "none",
                   "NATO operational context; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "authorizes", "iso19115", "", "none",
                   "Authorization relation; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "iso19115", "", "none",
                   "Authorization relation; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "iso19115", "", "none",
                   "Definitional relation; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "iso19115", "", "none",
                   "Definitional relation; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction", "iso19115", "", "none",
                   "Redaction metadata; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "iso19115", "", "none",
                   "Redaction metadata; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "iso19115", "", "none",
                   "Redaction metadata; no ISO 19115 equivalent."),
    CrosswalkEntry("adatp5636", "recordsHold", "iso19115", "", "none",
                   "Legal hold; no ISO 19115 equivalent."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → ISO 23081-1
# ---------------------------------------------------------------------------
ADATP5636_TO_ISO23081: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "title", "iso23081", "title", "exact",
                   "Both mandatory; ISO 23081 also allows subject headings as title."),
    CrosswalkEntry("adatp5636", "creator", "iso23081", "creator", "similar",
                   "Both mandatory; NCMS uses PointOfContact; ISO 23081 allows agent name or URI."),
    CrosswalkEntry("adatp5636", "dateCreated", "iso23081", "dateCreated", "exact",
                   "Both mandatory creation date fields; same ISO 8601 format."),
    CrosswalkEntry("adatp5636", "identifier", "iso23081", "identifier", "exact",
                   "Both mandatory unique identifiers."),
    CrosswalkEntry("adatp5636", "type", "iso23081", "type", "similar",
                   "Both mandatory type fields; ISO 23081 uses records-specific vocabulary."),
    CrosswalkEntry("adatp5636", "mediaFormat", "iso23081", "format", "exact",
                   "Both use MIME types or format descriptions."),
    CrosswalkEntry("adatp5636", "description", "iso23081", "description", "exact",
                   "Both optional descriptions of the resource."),
    CrosswalkEntry("adatp5636", "subject", "iso23081", "subject", "exact",
                   "Both describe the topic."),
    CrosswalkEntry("adatp5636", "language", "iso23081", "language", "exact",
                   "Both use ISO 639 codes."),
    CrosswalkEntry("adatp5636", "rights", "iso23081", "rights", "exact",
                   "Both express rights information."),
    CrosswalkEntry("adatp5636", "accessRights", "iso23081", "access", "similar",
                   "NCMS accessRights = ISO 23081 access. ISO 23081 access is more records-specific."),
    CrosswalkEntry("adatp5636", "dateModified", "iso23081", "dateModified", "exact",
                   "Same semantics; same ISO 8601 format."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "iso23081", "disposition", "similar",
                   "NCMS ILS layer recordsDisposition; ISO 23081 disposition. Very close semantics."),
    CrosswalkEntry("adatp5636", "dateDisposition", "iso23081", "disposition", "partial",
                   "NCMS dateDisposition is the date; ISO 23081 disposition includes both instruction and date."),
    CrosswalkEntry("adatp5636", "status", "iso23081", "status", "similar",
                   "Both optional status fields; ISO 23081 uses records lifecycle vocabulary."),
    CrosswalkEntry("adatp5636", "relation", "iso23081", "aggregation", "partial",
                   "NCMS relation is generic; ISO 23081 aggregation is specifically about records series/file context."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "iso23081", "", "none",
                   "ISO 23081 does not have a structured confidentiality label mechanism."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "iso23081", "", "none",
                   "No records metadata equivalent; ISO 23081 does not distinguish metadata-level labels."),
    CrosswalkEntry("adatp5636", "provenance", "iso23081", "", "none",
                   "ISO 23081 agent/mandate fields partially cover provenance but no direct equivalent."),
    CrosswalkEntry("adatp5636", "contextActivity", "iso23081", "mandate", "partial",
                   "NCMS contextActivity (mission/operation context); ISO 23081 mandate (legal/organisational mandate). "
                   "Related but not equivalent."),
    # ── Additional mappings ───────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "contributor", "iso23081", "agent", "similar",
                   "ISO 23081 agent covers all parties associated with the record; "
                   "contributor maps to agent with an appropriate relationship role."),
    CrosswalkEntry("adatp5636", "abstract", "iso23081", "description", "similar",
                   "ISO 23081 description captures a textual account of the record; "
                   "an abstract is a type of description."),
    CrosswalkEntry("adatp5636", "keyword", "iso23081", "subject", "similar",
                   "ISO 23081 subject describes the topic of the record; keywords are a form of subject."),
    CrosswalkEntry("adatp5636", "subjectCategory", "iso23081", "subject", "partial",
                   "A formal subject classification category maps to ISO 23081 subject."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "iso23081", "title", "partial",
                   "ISO 23081 title allows alternative names; an alternative title is a variant title."),
    CrosswalkEntry("adatp5636", "dateIssued", "iso23081", "dateCreated", "partial",
                   "Issuance date is related to record creation but distinct; dateCreated is the closest "
                   "ISO 23081 date field."),
    CrosswalkEntry("adatp5636", "dateClosed", "iso23081", "dateClosed", "exact",
                   "ISO 23081 dateClosed is an exact match — the date the record was closed."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "iso23081", "identifier", "similar",
                   "ISO 23081 identifier is used for all record identifiers including external ones."),
    CrosswalkEntry("adatp5636", "copyright", "iso23081", "rights", "similar",
                   "A copyright statement is a form of rights information over the record."),
    CrosswalkEntry("adatp5636", "license", "iso23081", "rights", "partial",
                   "A licence is one aspect of rights; ISO 23081 rights covers all rights information."),
    CrosswalkEntry("adatp5636", "rightsHolder", "iso23081", "agent", "partial",
                   "Rights holder can be expressed as an ISO 23081 agent with relationship=owner."),
    CrosswalkEntry("adatp5636", "conformsTo", "iso23081", "mandate", "partial",
                   "Conformance to a standard is related to the mandate (legal/organisational basis) "
                   "for the record, but the semantics differ."),
    CrosswalkEntry("adatp5636", "medium", "iso23081", "format", "partial",
                   "Physical carrier medium is related to format; ISO 23081 format covers both "
                   "digital and physical formats."),
    CrosswalkEntry("adatp5636", "hasPart", "iso23081", "aggregation", "partial",
                   "Part-whole relationships are expressed through ISO 23081 aggregation "
                   "(series/file/record relationships)."),
    CrosswalkEntry("adatp5636", "isPartOf", "iso23081", "aggregation", "partial",
                   "Part-of relationships expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "hasVersion", "iso23081", "aggregation", "partial",
                   "Version relationships can be expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "isVersionOf", "iso23081", "aggregation", "partial",
                   "Version-of relationships expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "references", "iso23081", "aggregation", "partial",
                   "Reference relationships expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "replaces", "iso23081", "aggregation", "partial",
                   "Supersession relationships expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "requires", "iso23081", "aggregation", "partial",
                   "Dependency relationships expressed through ISO 23081 aggregation."),
    CrosswalkEntry("adatp5636", "recordsHold", "iso23081", "disposition", "partial",
                   "A legal/litigation hold suspends normal disposition; it is a disposition-related concept."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "iso23081", "", "none",
                   "Update frequency is not a standard ISO 23081 metadata element."),
    CrosswalkEntry("adatp5636", "version", "iso23081", "", "none",
                   "Version string is not a dedicated ISO 23081 field; use aggregation for version relationships."),
    CrosswalkEntry("adatp5636", "tableOfContents", "iso23081", "", "none",
                   "Table of contents is not a standard ISO 23081 element."),
    CrosswalkEntry("adatp5636", "extent", "iso23081", "", "none",
                   "File size / duration is not a standard ISO 23081 metadata element."),
    CrosswalkEntry("adatp5636", "extentQualifier", "iso23081", "", "none",
                   "Extent qualifier; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "subtitle", "iso23081", "", "none",
                   "Subtitle is not a dedicated ISO 23081 field."),
    CrosswalkEntry("adatp5636", "publisher", "iso23081", "", "none",
                   "Publisher is not a standard ISO 23081 element; use agent with role=publisher if needed."),
    CrosswalkEntry("adatp5636", "source", "iso23081", "", "none",
                   "Data source provenance is not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "geographicReference", "iso23081", "", "none",
                   "Geographic coverage is not a standard ISO 23081 metadata element."),
    CrosswalkEntry("adatp5636", "timePeriod", "iso23081", "", "none",
                   "Temporal coverage is not a standard ISO 23081 metadata element."),
    # ── Date fields with no ISO 23081 equivalent ──────────────────────────────
    CrosswalkEntry("adatp5636", "dateAccepted", "iso23081", "", "none",
                   "Acceptance date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateAcquired", "iso23081", "", "none",
                   "Acquisition date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateAvailable", "iso23081", "", "none",
                   "Availability date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "iso23081", "", "none",
                   "Copyright year not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateCutOff", "iso23081", "", "none",
                   "Cut-off date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateDeclared", "iso23081", "", "none",
                   "Declaration date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "iso23081", "", "none",
                   "Next-version date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "iso23081", "", "none",
                   "Submission date not a standard ISO 23081 field."),
    CrosswalkEntry("adatp5636", "dateValid", "iso23081", "", "none",
                   "Validity period not a standard ISO 23081 field."),
    # ── NATO/security-specific ────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "iso23081", "", "none",
                   "NATO-specific security label; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "custodian", "iso23081", "", "none",
                   "NCMS custodian is a records management role; ISO 23081 agent partially covers this "
                   "but without a dedicated field."),
    CrosswalkEntry("adatp5636", "countryCode", "iso23081", "", "none",
                   "Country code; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "iso23081", "", "none",
                   "Geographic encoding scheme; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "placeName", "iso23081", "", "none",
                   "Place name; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "region", "iso23081", "", "none",
                   "Region; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "authorizes", "iso23081", "", "none",
                   "Authorization relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "iso23081", "", "none",
                   "Authorization relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "iso23081", "", "none",
                   "Definitional relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "iso23081", "", "none",
                   "Definitional relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "hasFormat", "iso23081", "", "none",
                   "Format variant relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isFormatOf", "iso23081", "", "none",
                   "Format variant relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "iso23081", "", "none",
                   "Referenced-by relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "iso23081", "", "none",
                   "Required-by relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "iso23081", "", "none",
                   "Replaced-by relation; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction", "iso23081", "", "none",
                   "Redaction metadata; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "iso23081", "", "none",
                   "Redaction metadata; no ISO 23081 equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "iso23081", "", "none",
                   "Redaction metadata; no ISO 23081 equivalent."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → INSPIRE
# ---------------------------------------------------------------------------
ADATP5636_TO_INSPIRE: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "title", "inspire", "title", "exact",
                   "Both mandatory; same free-text title concept."),
    CrosswalkEntry("adatp5636", "creator", "inspire", "responsibleParty", "similar",
                   "NCMS creator maps to INSPIRE responsibleParty with role=originator."),
    CrosswalkEntry("adatp5636", "publisher", "inspire", "responsibleParty", "similar",
                   "NCMS publisher maps to INSPIRE responsibleParty with role=publisher."),
    CrosswalkEntry("adatp5636", "dateCreated", "inspire", "dateOfCreation", "exact",
                   "Both express the creation date."),
    CrosswalkEntry("adatp5636", "dateIssued", "inspire", "dateOfPublication", "exact",
                   "Both express the publication/issuance date."),
    CrosswalkEntry("adatp5636", "dateModified", "inspire", "dateOfLastRevision", "exact",
                   "Both express the last revision/modification date."),
    CrosswalkEntry("adatp5636", "abstract", "inspire", "abstract", "exact",
                   "Both mandatory summaries of the resource."),
    CrosswalkEntry("adatp5636", "description", "inspire", "abstract", "partial",
                   "NCMS description broader; INSPIRE abstract is the primary narrative field."),
    CrosswalkEntry("adatp5636", "keyword", "inspire", "keyword", "similar",
                   "NCMS free-text keyword; INSPIRE keyword should reference GEMET or other controlled thesaurus."),
    CrosswalkEntry("adatp5636", "subject", "inspire", "keyword", "partial",
                   "NCMS subject uses classification code; INSPIRE keyword with originatingControlledVocabulary."),
    CrosswalkEntry("adatp5636", "language", "inspire", "resourceLanguage", "exact",
                   "Both use ISO 639-2/B codes."),
    CrosswalkEntry("adatp5636", "identifier", "inspire", "uniqueResourceIdentifier", "exact",
                   "Both express a persistent unique identifier for the resource."),
    CrosswalkEntry("adatp5636", "type", "inspire", "resourceType", "similar",
                   "NCMS NATO resource type; INSPIRE resourceType uses MD_ScopeCode (dataset|series|service)."),
    CrosswalkEntry("adatp5636", "rights", "inspire", "conditionsForAccessAndUse", "partial",
                   "NCMS rights free text; INSPIRE conditionsForAccessAndUse is mandatory and more specific."),
    CrosswalkEntry("adatp5636", "accessRights", "inspire", "limitationsOnPublicAccess", "similar",
                   "NCMS accessRights; INSPIRE limitationsOnPublicAccess is mandatory."),
    CrosswalkEntry("adatp5636", "license", "inspire", "conditionsForAccessAndUse", "partial",
                   "NCMS licence URI; INSPIRE conditions include both licence and access conditions."),
    CrosswalkEntry("adatp5636", "geographicReference", "inspire", "geographicBoundingBox", "similar",
                   "NCMS uses various encoding schemes; INSPIRE requires WGS84 bounding box."),
    CrosswalkEntry("adatp5636", "provenance", "inspire", "lineage", "similar",
                   "Both describe the history/provenance of the resource. INSPIRE lineage is mandatory."),
    CrosswalkEntry("adatp5636", "conformsTo", "inspire", "specification", "similar",
                   "NCMS conformsTo URI; INSPIRE specification is a citation to the implementing rule."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "inspire", "limitationsOnPublicAccess", "partial",
                   "Classification level informs access limitations; INSPIRE limitations reference INSPIRE exceptions."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "inspire", "", "none",
                   "INSPIRE has no metadata-level security classification concept."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "inspire", "", "none",
                   "Records management concept; outside INSPIRE scope."),
    CrosswalkEntry("adatp5636", "topicCategory", "inspire", "topicCategory", "exact",
                   "Both use identical ISO 19115 MD_TopicCategoryCode values."),
    CrosswalkEntry("adatp5636", "timePeriod", "inspire", "temporalExtent", "similar",
                   "NCMS DCMI Period format; INSPIRE ISO 19115 EX_TemporalExtent."),
    # ── Additional mappings ───────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "contributor", "inspire", "responsibleParty", "similar",
                   "INSPIRE responsibleParty with roleCode=collaborator captures contributors."),
    CrosswalkEntry("adatp5636", "source", "inspire", "lineage", "partial",
                   "Data source is part of the lineage statement in INSPIRE."),
    CrosswalkEntry("adatp5636", "subjectCategory", "inspire", "topicCategory", "similar",
                   "NCMS subjectCategory maps to INSPIRE topicCategory (ISO 19115 MD_TopicCategoryCode) "
                   "when the subject vocabulary aligns with ISO 19115 topic categories."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "inspire", "title", "partial",
                   "INSPIRE has no dedicated alternative title element; an alternative title "
                   "can be expressed as an additional title instance."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "inspire", "uniqueResourceIdentifier", "similar",
                   "INSPIRE uniqueResourceIdentifier is designed for persistent, externally resolvable "
                   "identifiers — equivalent to NCMS externalIdentifier."),
    CrosswalkEntry("adatp5636", "copyright", "inspire", "conditionsForAccessAndUse", "partial",
                   "Copyright conditions belong in INSPIRE conditionsForAccessAndUse."),
    CrosswalkEntry("adatp5636", "rightsHolder", "inspire", "responsibleParty", "partial",
                   "Rights holder expressed as INSPIRE responsibleParty with roleCode=owner."),
    CrosswalkEntry("adatp5636", "status", "inspire", "responsibleParty", "partial",
                   "INSPIRE captures resource status through resourceMaintenance within the "
                   "identification info — no direct status element; responsibleParty is the closest "
                   "contextual element."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "inspire", "responsibleParty", "partial",
                   "Update frequency is part of INSPIRE resource maintenance metadata; "
                   "no dedicated top-level element in the core INSPIRE metadata profile."),
    CrosswalkEntry("adatp5636", "countryCode", "inspire", "geographicDescription", "partial",
                   "An ISO 3166 country code can be expressed as an INSPIRE geographicDescription."),
    CrosswalkEntry("adatp5636", "placeName", "inspire", "geographicDescription", "partial",
                   "A place name maps to INSPIRE geographicDescription (free-text geographic extent)."),
    CrosswalkEntry("adatp5636", "region", "inspire", "geographicDescription", "partial",
                   "A named region maps to INSPIRE geographicDescription."),
    CrosswalkEntry("adatp5636", "dateValid", "inspire", "temporalExtent", "partial",
                   "Validity period maps to INSPIRE temporalExtent (EX_TemporalExtent)."),
    CrosswalkEntry("adatp5636", "mediaFormat", "inspire", "", "none",
                   "INSPIRE focuses on spatial data services and datasets; "
                   "there is no mandatory mediaFormat element in the INSPIRE metadata profile."),
    CrosswalkEntry("adatp5636", "version", "inspire", "", "none",
                   "No dedicated version element in INSPIRE core metadata."),
    # ── Relation fields — no INSPIRE equivalent ───────────────────────────────
    CrosswalkEntry("adatp5636", "hasPart", "inspire", "", "none",
                   "Part-whole relations are not modelled in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isPartOf", "inspire", "", "none",
                   "Part-of relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "hasVersion", "inspire", "", "none",
                   "Version relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isVersionOf", "inspire", "", "none",
                   "Version-of relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "references", "inspire", "", "none",
                   "Reference relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "inspire", "", "none",
                   "Referenced-by relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "replaces", "inspire", "", "none",
                   "Supersession relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "inspire", "", "none",
                   "Replaced-by relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "requires", "inspire", "", "none",
                   "Dependency relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "inspire", "", "none",
                   "Required-by relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "hasFormat", "inspire", "", "none",
                   "Format variant relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "isFormatOf", "inspire", "", "none",
                   "Format variant relations not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "relation", "inspire", "", "none",
                   "Generic relation not in INSPIRE core metadata."),
    # ── Date fields with no INSPIRE equivalent ────────────────────────────────
    CrosswalkEntry("adatp5636", "dateAccepted", "inspire", "", "none",
                   "Acceptance date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateAcquired", "inspire", "", "none",
                   "Acquisition date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateAvailable", "inspire", "", "none",
                   "Availability date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateClosed", "inspire", "", "none",
                   "Closure date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "inspire", "", "none",
                   "Copyright year not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateCutOff", "inspire", "", "none",
                   "Cut-off date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateDeclared", "inspire", "", "none",
                   "Declaration date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "inspire", "", "none",
                   "Next-version date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "inspire", "", "none",
                   "Submission date not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "dateDisposition", "inspire", "", "none",
                   "Disposal date not in INSPIRE core metadata."),
    # ── Physical / format ─────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "extent", "inspire", "", "none",
                   "File size / duration not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "extentQualifier", "inspire", "", "none",
                   "Extent qualifier not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "medium", "inspire", "", "none",
                   "Physical medium not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "tableOfContents", "inspire", "", "none",
                   "Table of contents not in INSPIRE core metadata."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "inspire", "", "none",
                   "Encoding scheme qualifier not in INSPIRE core metadata."),
    # ── NATO/security-specific ────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "inspire", "", "none",
                   "NATO-specific security label; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "custodian", "inspire", "", "none",
                   "Records custodian role; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "contextActivity", "inspire", "", "none",
                   "NATO operational context; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "authorizes", "inspire", "", "none",
                   "Authorization relation; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "inspire", "", "none",
                   "Authorization relation; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "inspire", "", "none",
                   "Definitional relation; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "inspire", "", "none",
                   "Definitional relation; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction", "inspire", "", "none",
                   "Redaction metadata; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "inspire", "", "none",
                   "Redaction metadata; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "inspire", "", "none",
                   "Redaction metadata; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "inspire", "", "none",
                   "Records disposal; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "recordsHold", "inspire", "", "none",
                   "Legal hold; no INSPIRE equivalent."),
    CrosswalkEntry("adatp5636", "subtitle", "inspire", "", "none",
                   "Subtitle; no dedicated INSPIRE element."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "inspire", "", "none",
                   "Update frequency is captured in INSPIRE resourceMaintenance but has no dedicated "
                   "top-level element in the core INSPIRE profile."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → NIST SP 800-60
# ---------------------------------------------------------------------------
ADATP5636_TO_NIST: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "nist_sp80060", "systemSecurityCategory", "partial",
                   "NCMS confidentiality label (classification level) partially maps to NIST security category. "
                   "NATO classification levels (UNCLASSIFIED/RESTRICTED/CONFIDENTIAL/SECRET) can inform "
                   "NIST impact levels (Low/Moderate/High) but the frameworks are not directly equivalent."),
    CrosswalkEntry("adatp5636", "identifier", "nist_sp80060", "informationTypeIdentifier", "partial",
                   "NCMS identifier is for the resource; NIST identifier is for the information type category. "
                   "Both are persistent identifiers but for different concepts."),
    CrosswalkEntry("adatp5636", "type", "nist_sp80060", "informationType", "partial",
                   "NCMS resource type (genre); NIST informationType (data category for security classification). "
                   "Different vocabularies and purposes."),
    CrosswalkEntry("adatp5636", "title", "nist_sp80060", "systemName", "none",
                   "NCMS title is the resource title; NIST systemName is the system name. "
                   "Only coincidentally similar for systems described as resources."),
    CrosswalkEntry("adatp5636", "accessRights", "nist_sp80060", "", "none",
                   "NCMS accessRights defines access conditions on the resource; NIST SP 800-60 does not "
                   "model per-resource access rights — it categorises information types system-wide."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "nist_sp80060", "", "none",
                   "NIST SP 800-60 does not have a metadata-level classification label concept."),
    # ── Remaining ADatP-5636 fields — no SP 800-60 equivalent ────────────────
    # SP 800-60 is a security-categorisation framework with 11 fields; most
    # resource-metadata fields from NATO have no counterpart.
    CrosswalkEntry("adatp5636", "abstract", "nist_sp80060", "", "none",
                   "Resource abstract; SP 800-60 has no description/abstract field."),
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "nist_sp80060", "", "none",
                   "Alternative classification label; SP 800-60 uses systemSecurityCategory, not labels."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "nist_sp80060", "", "none",
                   "Alternative title; SP 800-60 has no title fields."),
    CrosswalkEntry("adatp5636", "authorizes", "nist_sp80060", "", "none",
                   "Authorization relation; SP 800-60 has no authorization relation field."),
    CrosswalkEntry("adatp5636", "conformsTo", "nist_sp80060", "", "none",
                   "Conformance declaration; SP 800-60 has no conformance field."),
    CrosswalkEntry("adatp5636", "contextActivity", "nist_sp80060", "", "none",
                   "NATO operational context; SP 800-60 missionArea is conceptually related "
                   "but covers US federal mission functions, not NATO operational contexts."),
    CrosswalkEntry("adatp5636", "contributor", "nist_sp80060", "", "none",
                   "Contributing entity; SP 800-60 has no contributor field."),
    CrosswalkEntry("adatp5636", "copyright", "nist_sp80060", "", "none",
                   "Copyright notice; SP 800-60 has no copyright field."),
    CrosswalkEntry("adatp5636", "countryCode", "nist_sp80060", "", "none",
                   "Country code; SP 800-60 has no geographic fields."),
    CrosswalkEntry("adatp5636", "creator", "nist_sp80060", "", "none",
                   "Resource creator; SP 800-60 has no creator field."),
    CrosswalkEntry("adatp5636", "custodian", "nist_sp80060", "", "none",
                   "Data custodian; SP 800-60 has no custodian field."),
    CrosswalkEntry("adatp5636", "dateAccepted", "nist_sp80060", "", "none",
                   "Formal acceptance date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateAcquired", "nist_sp80060", "", "none",
                   "Acquisition date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateAvailable", "nist_sp80060", "", "none",
                   "Availability date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateClosed", "nist_sp80060", "", "none",
                   "Record closure date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "nist_sp80060", "", "none",
                   "Copyright date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateCreated", "nist_sp80060", "", "none",
                   "Creation date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateCutOff", "nist_sp80060", "", "none",
                   "Information cut-off date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateDeclared", "nist_sp80060", "", "none",
                   "Declaration date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateDisposition", "nist_sp80060", "", "none",
                   "Disposition date; SP 800-60 has no records management fields."),
    CrosswalkEntry("adatp5636", "dateIssued", "nist_sp80060", "", "none",
                   "Publication date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateModified", "nist_sp80060", "", "none",
                   "Modification date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "nist_sp80060", "", "none",
                   "Next version planned date; SP 800-60 has no versioning fields."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "nist_sp80060", "", "none",
                   "Submission date; SP 800-60 has no date fields."),
    CrosswalkEntry("adatp5636", "dateValid", "nist_sp80060", "", "none",
                   "Validity period; SP 800-60 has no validity date concept."),
    CrosswalkEntry("adatp5636", "description", "nist_sp80060", "", "none",
                   "Resource description; SP 800-60 has no description field."),
    CrosswalkEntry("adatp5636", "extent", "nist_sp80060", "", "none",
                   "Resource size/extent; SP 800-60 has no extent field."),
    CrosswalkEntry("adatp5636", "extentQualifier", "nist_sp80060", "", "none",
                   "Extent unit qualifier; SP 800-60 has no extent concept."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "nist_sp80060", "", "none",
                   "External identifier (ISBN, DOI, etc.); SP 800-60 has no external identifier field."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "nist_sp80060", "", "none",
                   "Geographic encoding qualifier; SP 800-60 has no geographic fields."),
    CrosswalkEntry("adatp5636", "geographicReference", "nist_sp80060", "", "none",
                   "Geographic coverage; SP 800-60 has no geographic fields."),
    CrosswalkEntry("adatp5636", "hasFormat", "nist_sp80060", "", "none",
                   "Format variant relation; SP 800-60 has no format relations."),
    CrosswalkEntry("adatp5636", "hasPart", "nist_sp80060", "", "none",
                   "Component part relation; SP 800-60 has no part/whole relations."),
    CrosswalkEntry("adatp5636", "hasRedaction", "nist_sp80060", "", "none",
                   "Redaction version relation; SP 800-60 has no redaction concept."),
    CrosswalkEntry("adatp5636", "hasVersion", "nist_sp80060", "", "none",
                   "Version relation; SP 800-60 has no version concept."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "nist_sp80060", "", "none",
                   "Inverse authorization relation; SP 800-60 has no authorization relation."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "nist_sp80060", "", "none",
                   "Definitional relation; SP 800-60 has no definitional relation."),
    CrosswalkEntry("adatp5636", "isFormatOf", "nist_sp80060", "", "none",
                   "Inverse format relation; SP 800-60 has no format relations."),
    CrosswalkEntry("adatp5636", "isPartOf", "nist_sp80060", "", "none",
                   "Container relation; SP 800-60 has no part/whole relations."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "nist_sp80060", "", "none",
                   "Inverse redaction relation; SP 800-60 has no redaction concept."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "nist_sp80060", "", "none",
                   "Inverse of references; SP 800-60 has no bibliographic relation."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "nist_sp80060", "", "none",
                   "Successor resource; SP 800-60 has no versioning relations."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "nist_sp80060", "", "none",
                   "Inverse of requires; SP 800-60 has no dependency relation."),
    CrosswalkEntry("adatp5636", "isVersionOf", "nist_sp80060", "", "none",
                   "Version relation; SP 800-60 has no version concept."),
    CrosswalkEntry("adatp5636", "keyword", "nist_sp80060", "", "none",
                   "Free-text keywords; SP 800-60 has no keyword field."),
    CrosswalkEntry("adatp5636", "language", "nist_sp80060", "", "none",
                   "Language of the resource; SP 800-60 has no language field."),
    CrosswalkEntry("adatp5636", "license", "nist_sp80060", "", "none",
                   "License URI; SP 800-60 has no license field."),
    CrosswalkEntry("adatp5636", "mediaFormat", "nist_sp80060", "", "none",
                   "MIME type; SP 800-60 has no media format field."),
    CrosswalkEntry("adatp5636", "medium", "nist_sp80060", "", "none",
                   "Physical medium; SP 800-60 has no medium field."),
    CrosswalkEntry("adatp5636", "placeName", "nist_sp80060", "", "none",
                   "Place name; SP 800-60 has no geographic fields."),
    CrosswalkEntry("adatp5636", "provenance", "nist_sp80060", "", "none",
                   "Provenance statement; SP 800-60 has no provenance field."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "nist_sp80060", "", "none",
                   "Inverse definitional relation; SP 800-60 has no definitional relation."),
    CrosswalkEntry("adatp5636", "publisher", "nist_sp80060", "", "none",
                   "Publishing organisation; SP 800-60 has no publisher field."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "nist_sp80060", "", "none",
                   "Redaction justification; SP 800-60 has no redaction concept."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "nist_sp80060", "", "none",
                   "Records management disposition; SP 800-60 does not model records management."),
    CrosswalkEntry("adatp5636", "recordsHold", "nist_sp80060", "", "none",
                   "Legal hold flag; SP 800-60 does not model legal holds."),
    CrosswalkEntry("adatp5636", "references", "nist_sp80060", "", "none",
                   "Cited resource reference; SP 800-60 has no bibliographic reference field."),
    CrosswalkEntry("adatp5636", "region", "nist_sp80060", "", "none",
                   "Region name; SP 800-60 has no geographic fields."),
    CrosswalkEntry("adatp5636", "relation", "nist_sp80060", "", "none",
                   "Generic relation to another resource; SP 800-60 has no relation field."),
    CrosswalkEntry("adatp5636", "replaces", "nist_sp80060", "", "none",
                   "Predecessor resource; SP 800-60 has no versioning relations."),
    CrosswalkEntry("adatp5636", "requires", "nist_sp80060", "", "none",
                   "Dependency resource; SP 800-60 has no dependency relation."),
    CrosswalkEntry("adatp5636", "rights", "nist_sp80060", "", "none",
                   "Rights statement; SP 800-60 has no rights field."),
    CrosswalkEntry("adatp5636", "rightsHolder", "nist_sp80060", "", "none",
                   "Rights holder; SP 800-60 has no rights holder field."),
    CrosswalkEntry("adatp5636", "source", "nist_sp80060", "", "none",
                   "Source resource reference; SP 800-60 has no source/derivation field."),
    CrosswalkEntry("adatp5636", "status", "nist_sp80060", "", "none",
                   "Resource lifecycle status; SP 800-60 has no status field for resources."),
    CrosswalkEntry("adatp5636", "subject", "nist_sp80060", "", "none",
                   "Controlled subject vocabulary; SP 800-60 informationType covers security-relevant "
                   "categories only, not general subject classification."),
    CrosswalkEntry("adatp5636", "subjectCategory", "nist_sp80060", "", "none",
                   "NATO subject category; SP 800-60 missionArea covers US federal mission functions, "
                   "not NATO subject categories."),
    CrosswalkEntry("adatp5636", "subtitle", "nist_sp80060", "", "none",
                   "Subtitle; SP 800-60 has no title fields."),
    CrosswalkEntry("adatp5636", "tableOfContents", "nist_sp80060", "", "none",
                   "Table of contents; SP 800-60 has no document structure fields."),
    CrosswalkEntry("adatp5636", "timePeriod", "nist_sp80060", "", "none",
                   "Temporal coverage; SP 800-60 has no temporal coverage fields."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "nist_sp80060", "", "none",
                   "Update frequency; SP 800-60 has no update frequency concept."),
    CrosswalkEntry("adatp5636", "version", "nist_sp80060", "", "none",
                   "Version number/label; SP 800-60 has no version field."),
    # NCMS → NIST IR 8112
    CrosswalkEntry("adatp5636", "creator", "nist_ir8112", "attributeOrigin", "partial",
                   "NCMS creator is the entity that created the resource (PointOfContact structure); "
                   "IR 8112 attributeOrigin is the authoritative source of an attribute value (URI). "
                   "Both identify an originating authority but serve different scopes."),
    CrosswalkEntry("adatp5636", "publisher", "nist_ir8112", "assertingParty", "partial",
                   "NCMS publisher is the entity making the resource officially available; "
                   "IR 8112 assertingParty is the entity asserting an attribute in a federated transaction. "
                   "The roles are analogous in a data-sharing context."),
    CrosswalkEntry("adatp5636", "identifier", "nist_ir8112", "attributeName", "none",
                   "NCMS identifier is a unique resource identifier (URI/string); "
                   "IR 8112 attributeName names the attribute type, not the resource. "
                   "Fundamentally different concepts."),
    CrosswalkEntry("adatp5636", "dateCreated", "nist_ir8112", "lastVerified", "none",
                   "NCMS dateCreated records when the resource was created; "
                   "IR 8112 lastVerified records when an attribute value was last confirmed accurate. "
                   "Different lifecycle events — no semantic equivalence."),
    CrosswalkEntry("adatp5636", "dateValid", "nist_ir8112", "expiryDate", "similar",
                   "NCMS dateValid expresses a validity period for the resource (DCMI Period); "
                   "IR 8112 expiryDate is a single point after which the attribute is no longer valid. "
                   "Both express temporal validity but with different granularity and structure."),
    CrosswalkEntry("adatp5636", "accessRights", "nist_ir8112", "policyIdentifier", "partial",
                   "NCMS accessRights states conditions for accessing the resource; "
                   "IR 8112 policyIdentifier is a URI to the trust framework governing the attribute. "
                   "Both reference a policy that governs use, but at different levels of specificity."),
    CrosswalkEntry("adatp5636", "provenance", "nist_ir8112", "attributeProvenance", "similar",
                   "NCMS provenance is a free-text statement of custody and change history for the resource; "
                   "IR 8112 attributeProvenance describes the chain of custody and transformation of an "
                   "attribute value. Semantically very close; IR 8112 is more narrowly scoped to attributes."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "nist_ir8112", "", "none",
                   "IR 8112 has no concept of a security classification label. "
                   "Attribute sensitivity in IR 8112 is implied by the policyIdentifier and relyingParty scope."),
    CrosswalkEntry("adatp5636", "rightsHolder", "nist_ir8112", "assertingParty", "partial",
                   "NCMS rightsHolder is the person or organisation owning rights over the resource; "
                   "IR 8112 assertingParty is the entity asserting the attribute. "
                   "Analogous in data governance terms but different in federated identity context."),
    # ── Remaining ADatP-5636 fields — no IR 8112 equivalent ──────────────────
    # IR 8112 is a federated-identity attribute schema; most resource-metadata
    # fields from NATO simply have no counterpart.
    CrosswalkEntry("adatp5636", "title", "nist_ir8112", "", "none",
                   "Resource title; IR 8112 has no title field for resource metadata."),
    CrosswalkEntry("adatp5636", "description", "nist_ir8112", "", "none",
                   "Resource description; IR 8112 has no description field."),
    CrosswalkEntry("adatp5636", "abstract", "nist_ir8112", "", "none",
                   "Resource abstract; IR 8112 has no abstract field."),
    CrosswalkEntry("adatp5636", "subject", "nist_ir8112", "", "none",
                   "Controlled subject vocabulary; IR 8112 has no subject classification concept."),
    CrosswalkEntry("adatp5636", "subjectCategory", "nist_ir8112", "", "none",
                   "NATO subject category code; no IR 8112 equivalent."),
    CrosswalkEntry("adatp5636", "keyword", "nist_ir8112", "", "none",
                   "Free-text keywords; IR 8112 has no keyword field."),
    CrosswalkEntry("adatp5636", "type", "nist_ir8112", "", "none",
                   "Resource genre/type; IR 8112 has no resource type field."),
    CrosswalkEntry("adatp5636", "language", "nist_ir8112", "", "none",
                   "Language of the resource; IR 8112 has no language field."),
    CrosswalkEntry("adatp5636", "publisher", "nist_ir8112", "", "none",
                   "Publishing organisation; IR 8112 has no publisher concept."),
    CrosswalkEntry("adatp5636", "contributor", "nist_ir8112", "", "none",
                   "Contributing entity; IR 8112 has no contributor field."),
    CrosswalkEntry("adatp5636", "custodian", "nist_ir8112", "", "none",
                   "Data custodian; IR 8112 does not model custodianship."),
    CrosswalkEntry("adatp5636", "rights", "nist_ir8112", "", "none",
                   "Rights statement; IR 8112 has no generic rights field."),
    CrosswalkEntry("adatp5636", "license", "nist_ir8112", "", "none",
                   "License URI; IR 8112 has no license field."),
    CrosswalkEntry("adatp5636", "copyright", "nist_ir8112", "", "none",
                   "Copyright notice; IR 8112 has no copyright field."),
    CrosswalkEntry("adatp5636", "identifier", "nist_ir8112", "", "none",
                   "NCMS resource identifier; IR 8112 attributeName names attribute types, not resources."),
    CrosswalkEntry("adatp5636", "externalIdentifier", "nist_ir8112", "", "none",
                   "External identifier (ISBN, DOI, etc.); no IR 8112 equivalent."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "nist_ir8112", "", "none",
                   "Alternative title; IR 8112 has no title fields."),
    CrosswalkEntry("adatp5636", "subtitle", "nist_ir8112", "", "none",
                   "Subtitle; IR 8112 has no subtitle field."),
    CrosswalkEntry("adatp5636", "tableOfContents", "nist_ir8112", "", "none",
                   "Table of contents; IR 8112 has no document structure fields."),
    CrosswalkEntry("adatp5636", "source", "nist_ir8112", "", "none",
                   "Source resource reference; IR 8112 has no source/derivation field."),
    CrosswalkEntry("adatp5636", "relation", "nist_ir8112", "", "none",
                   "Generic relation to another resource; IR 8112 has no relation field."),
    CrosswalkEntry("adatp5636", "references", "nist_ir8112", "", "none",
                   "Cited resource reference; IR 8112 has no bibliographic reference field."),
    CrosswalkEntry("adatp5636", "isReferencedBy", "nist_ir8112", "", "none",
                   "Inverse of references; IR 8112 has no bibliographic relation."),
    CrosswalkEntry("adatp5636", "replaces", "nist_ir8112", "", "none",
                   "Predecessor resource; IR 8112 has no versioning relations."),
    CrosswalkEntry("adatp5636", "isReplacedBy", "nist_ir8112", "", "none",
                   "Successor resource; IR 8112 has no versioning relations."),
    CrosswalkEntry("adatp5636", "requires", "nist_ir8112", "", "none",
                   "Dependency resource; IR 8112 has no dependency relation."),
    CrosswalkEntry("adatp5636", "isRequiredBy", "nist_ir8112", "", "none",
                   "Inverse of requires; IR 8112 has no dependency relation."),
    CrosswalkEntry("adatp5636", "conformsTo", "nist_ir8112", "", "none",
                   "Conformance declaration; IR 8112 has no conformance field."),
    CrosswalkEntry("adatp5636", "hasVersion", "nist_ir8112", "", "none",
                   "Version relation; IR 8112 has no version concept for resources."),
    CrosswalkEntry("adatp5636", "isVersionOf", "nist_ir8112", "", "none",
                   "Version relation; IR 8112 has no version concept for resources."),
    CrosswalkEntry("adatp5636", "hasPart", "nist_ir8112", "", "none",
                   "Component part relation; IR 8112 has no part/whole relations."),
    CrosswalkEntry("adatp5636", "isPartOf", "nist_ir8112", "", "none",
                   "Container relation; IR 8112 has no part/whole relations."),
    CrosswalkEntry("adatp5636", "hasFormat", "nist_ir8112", "", "none",
                   "Format variant relation; IR 8112 has no format relation."),
    CrosswalkEntry("adatp5636", "isFormatOf", "nist_ir8112", "", "none",
                   "Inverse format relation; IR 8112 has no format relation."),
    CrosswalkEntry("adatp5636", "authorizes", "nist_ir8112", "", "none",
                   "Authorization relation; IR 8112 has no authorization relation field."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy", "nist_ir8112", "", "none",
                   "Inverse authorization relation; IR 8112 has no authorization relation."),
    CrosswalkEntry("adatp5636", "isDefinedBy", "nist_ir8112", "", "none",
                   "Definitional relation; IR 8112 has no definitional relation."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf", "nist_ir8112", "", "none",
                   "Inverse definitional relation; IR 8112 has no definitional relation."),
    CrosswalkEntry("adatp5636", "hasRedaction", "nist_ir8112", "", "none",
                   "Redaction version relation; IR 8112 has no redaction concept."),
    CrosswalkEntry("adatp5636", "isRedactionOf", "nist_ir8112", "", "none",
                   "Inverse redaction relation; IR 8112 has no redaction concept."),
    CrosswalkEntry("adatp5636", "reasonForRedaction", "nist_ir8112", "", "none",
                   "Redaction justification; IR 8112 has no redaction concept."),
    CrosswalkEntry("adatp5636", "format", "nist_ir8112", "", "none",
                   "File format description; IR 8112 has no format field."),
    CrosswalkEntry("adatp5636", "mediaFormat", "nist_ir8112", "", "none",
                   "MIME type; IR 8112 has no media format field."),
    CrosswalkEntry("adatp5636", "medium", "nist_ir8112", "", "none",
                   "Physical medium; IR 8112 has no medium field."),
    CrosswalkEntry("adatp5636", "extent", "nist_ir8112", "", "none",
                   "Resource size/extent; IR 8112 has no extent field."),
    CrosswalkEntry("adatp5636", "extentQualifier", "nist_ir8112", "", "none",
                   "Extent unit qualifier; IR 8112 has no extent concept."),
    CrosswalkEntry("adatp5636", "geographicReference", "nist_ir8112", "", "none",
                   "Geographic coverage; IR 8112 has no geographic fields."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme", "nist_ir8112", "", "none",
                   "Geographic encoding qualifier; IR 8112 has no geographic fields."),
    CrosswalkEntry("adatp5636", "placeName", "nist_ir8112", "", "none",
                   "Place name; IR 8112 has no geographic fields."),
    CrosswalkEntry("adatp5636", "countryCode", "nist_ir8112", "", "none",
                   "Country code; IR 8112 has no geographic fields."),
    CrosswalkEntry("adatp5636", "region", "nist_ir8112", "", "none",
                   "Region name; IR 8112 has no geographic fields."),
    CrosswalkEntry("adatp5636", "timePeriod", "nist_ir8112", "", "none",
                   "Temporal coverage; IR 8112 has no temporal coverage fields."),
    CrosswalkEntry("adatp5636", "contextActivity", "nist_ir8112", "", "none",
                   "NATO operational context; IR 8112 has no operational context concept."),
    CrosswalkEntry("adatp5636", "dateIssued", "nist_ir8112", "", "none",
                   "Publication date; IR 8112 has no publication date field."),
    CrosswalkEntry("adatp5636", "dateModified", "nist_ir8112", "", "none",
                   "Modification date; IR 8112 has no modification date for resources."),
    CrosswalkEntry("adatp5636", "dateAccepted", "nist_ir8112", "", "none",
                   "Formal acceptance date; IR 8112 has no acceptance date concept."),
    CrosswalkEntry("adatp5636", "dateSubmitted", "nist_ir8112", "", "none",
                   "Submission date; IR 8112 has no submission date concept."),
    CrosswalkEntry("adatp5636", "dateCopyrighted", "nist_ir8112", "", "none",
                   "Copyright date; IR 8112 has no copyright concept."),
    CrosswalkEntry("adatp5636", "dateAcquired", "nist_ir8112", "", "none",
                   "Acquisition date; IR 8112 has no acquisition date concept."),
    CrosswalkEntry("adatp5636", "dateAvailable", "nist_ir8112", "", "none",
                   "Availability date; IR 8112 has no availability date concept."),
    CrosswalkEntry("adatp5636", "dateClosed", "nist_ir8112", "", "none",
                   "Record closure date; IR 8112 has no closure date concept."),
    CrosswalkEntry("adatp5636", "dateCutOff", "nist_ir8112", "", "none",
                   "Information cut-off date; IR 8112 has no cut-off date concept."),
    CrosswalkEntry("adatp5636", "dateDeclared", "nist_ir8112", "", "none",
                   "Declaration date; IR 8112 has no declaration date concept."),
    CrosswalkEntry("adatp5636", "dateDisposition", "nist_ir8112", "", "none",
                   "Disposition date; IR 8112 has no records disposition concept."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue", "nist_ir8112", "", "none",
                   "Next version planned date; IR 8112 has no versioning dates."),
    CrosswalkEntry("adatp5636", "updatingFrequency", "nist_ir8112", "", "none",
                   "Update frequency; IR 8112 has no update frequency concept."),
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel", "nist_ir8112", "", "none",
                   "Alternative classification label; IR 8112 has no classification label concept."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "nist_ir8112", "", "none",
                   "Metadata-level classification label; IR 8112 has no classification concept."),
    CrosswalkEntry("adatp5636", "status", "nist_ir8112", "", "none",
                   "Resource lifecycle status; IR 8112 has no resource status concept."),
    CrosswalkEntry("adatp5636", "version", "nist_ir8112", "", "none",
                   "Version number/label; IR 8112 has no version field for resources."),
    CrosswalkEntry("adatp5636", "recordsDisposition", "nist_ir8112", "", "none",
                   "Records management disposition; IR 8112 has no records management concept."),
    CrosswalkEntry("adatp5636", "recordsHold", "nist_ir8112", "", "none",
                   "Legal hold flag; IR 8112 has no records hold concept."),
]

# ---------------------------------------------------------------------------
# NIST IR 8112 → other standards (attribute metadata perspective)
# ---------------------------------------------------------------------------
NISTIR8112_TO_NCMS: List[CrosswalkEntry] = [
    CrosswalkEntry("nist_ir8112", "attributeOrigin", "adatp5636", "creator", "partial",
                   "IR 8112 attributeOrigin (URI of issuing authority) partially maps to NCMS creator "
                   "(PointOfContact of resource creator). Both identify an originating entity."),
    CrosswalkEntry("nist_ir8112", "assertingParty", "adatp5636", "publisher", "partial",
                   "IR 8112 assertingParty (entity making the attribute assertion) maps partially to "
                   "NCMS publisher (entity making the resource available). Analogous roles."),
    CrosswalkEntry("nist_ir8112", "expiryDate", "adatp5636", "dateValid", "similar",
                   "IR 8112 expiryDate maps to NCMS dateValid (end of validity period). "
                   "IR 8112 uses a single datetime; NCMS uses DCMI Period with start/end."),
    CrosswalkEntry("nist_ir8112", "lastVerified", "adatp5636", "dateModified", "partial",
                   "IR 8112 lastVerified (date attribute was last confirmed) is loosely analogous to "
                   "NCMS dateModified (date resource was last changed). Different semantics."),
    CrosswalkEntry("nist_ir8112", "attributeProvenance", "adatp5636", "provenance", "similar",
                   "IR 8112 attributeProvenance maps closely to NCMS provenance. "
                   "Both are free-text custody descriptions."),
    CrosswalkEntry("nist_ir8112", "policyIdentifier", "adatp5636", "accessRights", "partial",
                   "IR 8112 policyIdentifier (trust framework URI) partially maps to NCMS accessRights. "
                   "Both reference a governance policy."),
    CrosswalkEntry("nist_ir8112", "attributeName", "adatp5636", "", "none",
                   "No NCMS equivalent. IR 8112 attributeName names the attribute type itself, "
                   "which has no direct counterpart in a resource-centric metadata model."),
    CrosswalkEntry("nist_ir8112", "attributeValue", "adatp5636", "", "none",
                   "No NCMS equivalent. IR 8112 attributeValue is the actual asserted value of an "
                   "identity attribute — a concept absent from resource metadata."),
    CrosswalkEntry("nist_ir8112", "attributeDataType", "adatp5636", "", "none",
                   "No NCMS equivalent. IR 8112 attributeDataType specifies the data type of an "
                   "attribute value; NCMS uses representationTerm for this at schema level only."),
    CrosswalkEntry("nist_ir8112", "attributeVerification", "adatp5636", "", "none",
                   "No NCMS equivalent. IR 8112 attributeVerification describes how an identity "
                   "attribute was verified — a federated identity concept with no resource metadata counterpart."),
    CrosswalkEntry("nist_ir8112", "attributeAccuracy", "adatp5636", "", "none",
                   "No NCMS equivalent. Data quality metadata for identity attributes has no "
                   "direct counterpart in NCMS resource metadata."),
    CrosswalkEntry("nist_ir8112", "attributeConsistency", "adatp5636", "", "none",
                   "No NCMS equivalent. Cross-provider consistency checking is specific to "
                   "federated identity management."),
    CrosswalkEntry("nist_ir8112", "relyingParty", "adatp5636", "", "none",
                   "No NCMS equivalent. Relying party scoping is a federated identity concept; "
                   "NCMS manages access through accessRights and the confidentiality label."),
]

# ---------------------------------------------------------------------------
# Dublin Core → ISO 19115 (supplementary)
# ---------------------------------------------------------------------------
DC_TO_ISO19115: List[CrosswalkEntry] = [
    CrosswalkEntry("dublin_core", "title", "iso19115", "citationTitle", "exact", ""),
    CrosswalkEntry("dublin_core", "creator", "iso19115", "pointOfContact", "partial", ""),
    CrosswalkEntry("dublin_core", "subject", "iso19115", "descriptiveKeywords", "partial", ""),
    CrosswalkEntry("dublin_core", "description", "iso19115", "abstract", "similar", ""),
    CrosswalkEntry("dublin_core", "date", "iso19115", "citationDate", "partial", "DC date is generic; ISO 19115 uses typed dates."),
    CrosswalkEntry("dublin_core", "language", "iso19115", "dataIdentificationLanguage", "exact", ""),
    CrosswalkEntry("dublin_core", "identifier", "iso19115", "fileIdentifier", "similar", ""),
    CrosswalkEntry("dublin_core", "rights", "iso19115", "resourceConstraints", "partial", ""),
    CrosswalkEntry("dublin_core", "format", "iso19115", "resourceFormat", "partial", ""),
    CrosswalkEntry("dublin_core", "coverage", "iso19115", "extent", "partial", "DC coverage is text; ISO 19115 extent is structured."),
]

# ---------------------------------------------------------------------------
# ADatP-5636 → DCAT-AP-SE
# (same field coverage as DCAT-AP plus SE-specific requirements)
# ---------------------------------------------------------------------------
ADATP5636_TO_DCAT_AP_SE: List[CrosswalkEntry] = [
    CrosswalkEntry("adatp5636", "title",            "dcat_ap_se", "dct:title",       "exact",
                   "Both mandatory. Direct transfer."),
    CrosswalkEntry("adatp5636", "description",       "dcat_ap_se", "dct:description", "exact",
                   "Optional in ADatP-5636, mandatory in DCAT-AP-SE — same conflict as DCAT-AP."),
    CrosswalkEntry("adatp5636", "publisher",         "dcat_ap_se", "dct:publisher",   "similar",
                   "NCMS publisher is a free-text string; SE requires a foaf:Agent URI. "
                   "Mandatory in SE — NATO records without publisher will fail SE validation."),
    CrosswalkEntry("adatp5636", "creator",           "dcat_ap_se", "dct:creator",     "similar",
                   "NCMS creator is a PointOfContact struct; SE requires a foaf:Agent URI."),
    CrosswalkEntry("adatp5636", "dateCreated",       "dcat_ap_se", "dct:issued",      "partial",
                   "dateCreated is a creation date; issued is formal publication date."),
    CrosswalkEntry("adatp5636", "dateIssued",        "dcat_ap_se", "dct:issued",      "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "dateModified",      "dcat_ap_se", "dct:modified",    "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "keyword",           "dcat_ap_se", "dcat:keyword",    "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "subject",           "dcat_ap_se", "dcat:keyword",    "similar",
                   "NCMS subject (classification scheme) maps partially to SE keyword."),
    CrosswalkEntry("adatp5636", "language",          "dcat_ap_se", "dct:language",    "similar",
                   "SE requires EU Language NAL URI; NCMS uses ISO 639-3 alpha-3 codes. "
                   "Transform required (same as DCAT-AP)."),
    CrosswalkEntry("adatp5636", "identifier",        "dcat_ap_se", "dct:identifier",  "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "type",              "dcat_ap_se", "dct:type",        "similar",
                   "NCMS type maps to SE dct:type; vocabulary differs."),
    CrosswalkEntry("adatp5636", "mediaFormat",       "dcat_ap_se", "dcat:mediaType",  "exact",
                   "Direct transfer — IANA MIME types."),
    CrosswalkEntry("adatp5636", "rights",            "dcat_ap_se", "dct:license",     "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "accessRights",      "dcat_ap_se", "dct:accessRights","similar",
                   "SE requires EU Access Rights NAL URI; NATO accessRights is free text. "
                   "Same transform required as DCAT-AP."),
    CrosswalkEntry("adatp5636", "contributor",       "dcat_ap_se", "dct:creator",     "partial",
                   "Contributor maps approximately to creator/attribution in SE."),
    CrosswalkEntry("adatp5636", "source",            "dcat_ap_se", "dct:source",      "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "relation",          "dcat_ap_se", "dct:relation",    "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "provenance",        "dcat_ap_se", "dct:provenance",  "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "geographicReference","dcat_ap_se","dct:spatial",     "similar",
                   "SE recommends Geonames URIs; NCMS geographicReference supports multiple "
                   "formats. Geonames values transfer directly; other formats need transform."),
    CrosswalkEntry("adatp5636", "license",           "dcat_ap_se", "dct:license",     "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "conformsTo",        "dcat_ap_se", "dct:conformsTo",  "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "hasVersion",        "dcat_ap_se", "dct:hasVersion",  "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "isVersionOf",       "dcat_ap_se", "dct:isVersionOf", "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "hasPart",           "dcat_ap_se", "dct:relation",    "partial",
                   "DCAT-AP-SE does not include dct:hasPart; dct:relation is the closest "
                   "generic equivalent (hasPart and isPartOf are inverse relations — do not conflate)."),
    CrosswalkEntry("adatp5636", "isPartOf",          "dcat_ap_se", "dct:isPartOf",    "exact",
                   "Direct transfer."),
    CrosswalkEntry("adatp5636", "version",           "dcat_ap_se", "adms:version",    "similar",
                   "SE uses adms:version; NCMS version is a free-text string. Similar semantics."),
    CrosswalkEntry("adatp5636", "originatorConfidentialityLabel", "dcat_ap_se", "dct:accessRights", "partial",
                   "NCMS classification label maps only partially to SE's EU Access Rights URI. "
                   "Classification level can inform the PUBLIC/RESTRICTED/NON_PUBLIC choice, "
                   "but releasability caveats and compartments are lost."),
    CrosswalkEntry("adatp5636", "metadataConfidentialityLabel", "dcat_ap_se", "", "none",
                   "No equivalent in DCAT-AP-SE. SE has no metadata-level security model."),
    CrosswalkEntry("adatp5636", "recordsDisposition","dcat_ap_se", "",               "none",
                   "Records management concept; no SE equivalent."),
    CrosswalkEntry("adatp5636", "dateDisposition",   "dcat_ap_se", "",               "none",
                   "Records management concept; no SE equivalent."),
    CrosswalkEntry("adatp5636", "timePeriod",        "dcat_ap_se", "dct:temporal",   "similar",
                   "NCMS DCMI Period notation maps to SE dct:PeriodOfTime with startDate/endDate."),
    CrosswalkEntry("adatp5636", "accrualPeriodicity","dcat_ap_se", "dct:accrualPeriodicity", "exact",
                   "Direct transfer."),
    # ── Additional descriptive fields ─────────────────────────────────────────
    CrosswalkEntry("adatp5636", "abstract",         "dcat_ap_se", "dct:description", "similar",
                   "DCAT-AP-SE has no dedicated abstract; dct:description is the closest element."),
    CrosswalkEntry("adatp5636", "tableOfContents",  "dcat_ap_se", "dct:description", "partial",
                   "No dedicated tableOfContents; content can be added to dct:description."),
    CrosswalkEntry("adatp5636", "alternativeTitle", "dcat_ap_se", "dct:title", "partial",
                   "DCAT-AP-SE allows repeatable dct:title; alternative title expressed as additional title."),
    CrosswalkEntry("adatp5636", "subtitle",         "dcat_ap_se", "dct:title", "partial",
                   "No dedicated subtitle; can be appended to the primary title."),
    CrosswalkEntry("adatp5636", "subjectCategory",  "dcat_ap_se", "dcat:theme", "similar",
                   "NCMS subjectCategory maps to SE dcat:theme (EU Data Theme or other vocabulary URI)."),
    # ── External identification ───────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "externalIdentifier","dcat_ap_se","adms:identifier", "exact",
                   "ADMS:identifier is designed for secondary/external identifiers; exact match."),
    # ── Relations ────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "isPartOf",         "dcat_ap_se", "dct:isPartOf",   "exact",
                   "Direct transfer — dct:isPartOf is in the DCAT-AP-SE profile."),
    CrosswalkEntry("adatp5636", "references",       "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:references in SE; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "isReferencedBy",   "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:isReferencedBy in SE; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "replaces",         "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:replaces in SE; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "isReplacedBy",     "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:isReplacedBy in SE; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "requires",         "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:requires in SE; dct:relation is the closest generic equivalent."),
    CrosswalkEntry("adatp5636", "isRequiredBy",     "dcat_ap_se", "dct:relation",   "partial",
                   "No specific dct:isRequiredBy in SE; dct:relation is the closest generic equivalent."),
    # ── Rights ───────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "copyright",        "dcat_ap_se", "dct:license",    "partial",
                   "Copyright statement is partially captured by the licence field in DCAT-AP-SE."),
    CrosswalkEntry("adatp5636", "rightsHolder",     "dcat_ap_se", "",               "none",
                   "DCAT-AP-SE does not include a dedicated dct:rightsHolder at dataset level."),
    # ── Spatial ──────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "countryCode",      "dcat_ap_se", "dct:spatial",    "partial",
                   "Country code expressed as dct:spatial using EU Countries NAL or GeoNames URI."),
    CrosswalkEntry("adatp5636", "placeName",        "dcat_ap_se", "dct:spatial",    "partial",
                   "Place name expressed as dct:spatial using a GeoNames URI."),
    CrosswalkEntry("adatp5636", "region",           "dcat_ap_se", "dct:spatial",    "partial",
                   "Region expressed as dct:spatial using a GeoNames or NUTS URI."),
    CrosswalkEntry("adatp5636", "geographicEncodingScheme","dcat_ap_se","",          "none",
                   "Encoding scheme qualifier; no DCAT-AP-SE equivalent."),
    # ── Dates ────────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "dateAvailable",    "dcat_ap_se", "dct:issued",     "partial",
                   "Availability date is closest to dct:issued (formal issuance date)."),
    CrosswalkEntry("adatp5636", "dateValid",        "dcat_ap_se", "dct:temporal",   "partial",
                   "Validity period expressed as dct:PeriodOfTime within dct:temporal."),
    CrosswalkEntry("adatp5636", "dateAccepted",     "dcat_ap_se", "",               "none",
                   "Acceptance date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateAcquired",     "dcat_ap_se", "",               "none",
                   "Acquisition date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateClosed",       "dcat_ap_se", "",               "none",
                   "Closure date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateCopyrighted",  "dcat_ap_se", "",               "none",
                   "Copyright year; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateCutOff",       "dcat_ap_se", "",               "none",
                   "Cut-off date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateDeclared",     "dcat_ap_se", "",               "none",
                   "Declaration date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateNextVersionDue","dcat_ap_se","",               "none",
                   "Next-version date; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "dateSubmitted",    "dcat_ap_se", "",               "none",
                   "Submission date; no DCAT-AP-SE equivalent."),
    # ── Physical format ───────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "extent",           "dcat_ap_se", "",               "none",
                   "File size / duration; no DCAT-AP-SE equivalent at dataset level."),
    CrosswalkEntry("adatp5636", "extentQualifier",  "dcat_ap_se", "",               "none",
                   "Extent qualifier; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "medium",           "dcat_ap_se", "",               "none",
                   "Physical carrier medium; DCAT-AP-SE focuses on digital datasets."),
    CrosswalkEntry("adatp5636", "hasFormat",        "dcat_ap_se", "",               "none",
                   "DCAT-AP-SE models format variants through distributions; no dct:hasFormat relation."),
    CrosswalkEntry("adatp5636", "isFormatOf",       "dcat_ap_se", "",               "none",
                   "No isFormatOf at dataset level in DCAT-AP-SE."),
    # ── Lifecycle ────────────────────────────────────────────────────────────
    CrosswalkEntry("adatp5636", "updatingFrequency","dcat_ap_se", "dct:accrualPeriodicity", "exact",
                   "Both express the periodicity of resource updates."),
    CrosswalkEntry("adatp5636", "status",           "dcat_ap_se", "adms:version",   "none",
                   "DCAT-AP-SE uses adms:version for version tracking; there is no lifecycle "
                   "status element equivalent to NCMS status in the SE profile."),
    # ── NATO/security-specific — no DCAT-AP-SE equivalent ────────────────────
    CrosswalkEntry("adatp5636", "alternativeConfidentialityLabel","dcat_ap_se","",  "none",
                   "NATO-specific security label; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "custodian",        "dcat_ap_se", "",               "none",
                   "Records custodian; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "contextActivity",  "dcat_ap_se", "",               "none",
                   "NATO operational context; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "authorizes",       "dcat_ap_se", "",               "none",
                   "Authorization relation; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "isAuthorizedBy",   "dcat_ap_se", "",               "none",
                   "Authorization relation; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "isDefinedBy",      "dcat_ap_se", "",               "none",
                   "Definitional relation; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "providesDefinitionOf","dcat_ap_se","",             "none",
                   "Definitional relation; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "hasRedaction",     "dcat_ap_se", "",               "none",
                   "Redaction metadata; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "isRedactionOf",    "dcat_ap_se", "",               "none",
                   "Redaction metadata; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "reasonForRedaction","dcat_ap_se","",               "none",
                   "Redaction metadata; no DCAT-AP-SE equivalent."),
    CrosswalkEntry("adatp5636", "recordsHold",      "dcat_ap_se", "",               "none",
                   "Legal hold; no DCAT-AP-SE equivalent."),
]

# ---------------------------------------------------------------------------
# DCAT-AP-SE ↔ DCAT-AP (normative — SE is a constrained profile of DCAT-AP)
# ---------------------------------------------------------------------------
DCAT_AP_SE_TO_DCAT_AP: List[CrosswalkEntry] = [
    # Core dataset fields — exact matches (same URI, same namespace)
    CrosswalkEntry("dcat_ap_se", "dct:title",       "dcat_ap", "dct:title",       "exact",
                   "Identical property — both use dcterms:title with multilingual literals."),
    CrosswalkEntry("dcat_ap_se", "dct:description",  "dcat_ap", "dct:description",  "exact",
                   "Identical property — both use dcterms:description."),
    CrosswalkEntry("dcat_ap_se", "dct:publisher",    "dcat_ap", "dct:publisher",    "similar",
                   "Same URI; SE makes it mandatory (DCAT-AP only recommends it)."),
    CrosswalkEntry("dcat_ap_se", "dct:creator",      "dcat_ap", "dct:creator",      "exact",
                   "Identical optional property in both profiles."),
    CrosswalkEntry("dcat_ap_se", "dcat:contactPoint","dcat_ap", "dcat:contactPoint","exact",
                   "Identical property — vCard contact point."),
    CrosswalkEntry("dcat_ap_se", "dcat:keyword",     "dcat_ap", "dcat:keyword",     "exact",
                   "Identical property — free-text keyword tags."),
    CrosswalkEntry("dcat_ap_se", "dcat:theme",       "dcat_ap", "dcat:theme",       "exact",
                   "Same URI and vocabulary (EU Data Theme NAL)."),
    CrosswalkEntry("dcat_ap_se", "dct:identifier",   "dcat_ap", "dct:identifier",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:issued",       "dcat_ap", "dct:issued",       "exact",
                   "Identical property — ISO 8601 date."),
    CrosswalkEntry("dcat_ap_se", "dct:modified",     "dcat_ap", "dct:modified",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:language",     "dcat_ap", "dct:language",     "exact",
                   "Same URI; both require EU Publications Office language URIs."),
    CrosswalkEntry("dcat_ap_se", "dct:spatial",      "dcat_ap", "dct:spatial",      "similar",
                   "Same URI; SE prefers Geonames URIs while DCAT-AP accepts GeoNames, "
                   "EU Countries NAL, or NUTS. Values interoperable if Geonames/EU NAL used."),
    CrosswalkEntry("dcat_ap_se", "dct:temporal",     "dcat_ap", "dct:temporal",     "exact",
                   "Identical property — dct:PeriodOfTime with startDate/endDate."),
    CrosswalkEntry("dcat_ap_se", "dct:license",      "dcat_ap", "dct:license",      "similar",
                   "Same URI; SE requires CC0 for catalogues (DCAT-AP allows any licence). "
                   "Dataset-level licence is unrestricted in both."),
    CrosswalkEntry("dcat_ap_se", "dct:accessRights", "dcat_ap", "dct:accessRights", "exact",
                   "Identical property — both use EU Access Rights NAL URIs."),
    CrosswalkEntry("dcat_ap_se", "dcat:distribution","dcat_ap", "dcat:distribution","exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:accrualPeriodicity", "dcat_ap", "dct:accrualPeriodicity", "exact",
                   "Identical property — MDR Frequency NAL."),
    CrosswalkEntry("dcat_ap_se", "dcat:landingPage", "dcat_ap", "dcat:landingPage", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:conformsTo",   "dcat_ap", "dct:conformsTo",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:type",         "dcat_ap", "dct:type",         "exact",
                   "Identical property — EU Dataset Type NAL."),
    CrosswalkEntry("dcat_ap_se", "dct:provenance",   "dcat_ap", "dct:provenance",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:source",       "dcat_ap", "dct:source",       "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:isPartOf",     "dcat_ap", "dct:isPartOf",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:hasVersion",   "dcat_ap", "dct:hasVersion",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:isVersionOf",  "dcat_ap", "dct:isVersionOf",  "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dct:relation",     "dcat_ap", "dct:relation",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "prov:qualifiedAttribution", "dcat_ap", "prov:qualifiedAttribution", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dcat:qualifiedRelation", "dcat_ap", "dcat:qualifiedRelation", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dcat:spatialResolutionInMeters", "dcat_ap", "dcat:spatialResolutionInMeters", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dcat:temporalResolution", "dcat_ap", "dcat:temporalResolution", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "adms:identifier",  "dcat_ap", "adms:identifier",  "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "adms:version",     "dcat_ap", "owl:versionInfo",  "similar",
                   "adms:version (SE) and owl:versionInfo (DCAT-AP) serve the same purpose; "
                   "values transfer but namespace differs."),
    CrosswalkEntry("dcat_ap_se", "adms:versionNotes","dcat_ap", "",                 "none",
                   "adms:versionNotes has no direct equivalent in DCAT-AP 2.1.1."),
    # Distribution
    CrosswalkEntry("dcat_ap_se", "dcat:accessURL",   "dcat_ap", "dcat:accessURL",   "exact",
                   "Identical mandatory distribution property."),
    CrosswalkEntry("dcat_ap_se", "dcat:downloadURL", "dcat_ap", "dcat:downloadURL", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap_se", "dcat:mediaType",   "dcat_ap", "dcat:mediaType",   "exact",
                   "Identical property — IANA MIME types."),
    CrosswalkEntry("dcat_ap_se", "dct:format",       "dcat_ap", "dct:format",       "exact",
                   "Identical property — MDR File Type NAL."),
    # SE-specific properties without DCAT-AP equivalent
    CrosswalkEntry("dcat_ap_se", "dcatse:availability", "dcat_ap", "", "none",
                   "Swedish-specific distribution availability vocabulary has no equivalent "
                   "in base DCAT-AP 2.1.1. Information is lost on conversion."),
    CrosswalkEntry("dcat_ap_se", "dcat:applicableLegislation", "dcat_ap", "dct:conformsTo", "partial",
                   "applicableLegislation (SE) identifies mandating law by URI; DCAT-AP's "
                   "conformsTo is the closest match but semantically broader."),
    CrosswalkEntry("dcat_ap_se", "dcat:hvdCategory", "dcat_ap", "", "none",
                   "HVD category is a DCAT-AP-SE / DCAT-AP 3.x concept; not present in "
                   "DCAT-AP 2.1.1. Lost on conversion to 2.1.1."),
    # Catalog
    CrosswalkEntry("dcat_ap_se", "cat:dct:title",    "dcat_ap", "dct:title",        "exact",
                   "Catalogue title — identical property."),
    CrosswalkEntry("dcat_ap_se", "cat:dct:description", "dcat_ap", "dct:description","exact",
                   "Catalogue description — identical property."),
    CrosswalkEntry("dcat_ap_se", "cat:dct:publisher","dcat_ap", "dct:publisher",     "similar",
                   "Same URI; SE requires publisher on Catalog (DCAT-AP recommends it)."),
    CrosswalkEntry("dcat_ap_se", "cat:dct:license",  "dcat_ap", "dct:license",       "similar",
                   "Same URI; SE mandates CC0 1.0 — a DCAT-AP receiver with a different "
                   "licence will technically be valid but violates Swedish policy."),
    CrosswalkEntry("dcat_ap_se", "cat:dcat:dataset", "dcat_ap", "dcat:distribution", "similar",
                   "Catalog-level dataset reference maps to DCAT-AP's dataset/distribution "
                   "linkage; semantically equivalent."),
]

# ---------------------------------------------------------------------------
# DCAT-AP-SE → Dublin Core
# ---------------------------------------------------------------------------
DCAT_AP_SE_TO_DUBLIN_CORE: List[CrosswalkEntry] = [
    CrosswalkEntry("dcat_ap_se", "dct:title",       "dublin_core", "title",       "exact",
                   "dcterms:title = dc:title (DCMI Terms is a refinement of Dublin Core)."),
    CrosswalkEntry("dcat_ap_se", "dct:description",  "dublin_core", "description", "exact",
                   "Identical semantic."),
    CrosswalkEntry("dcat_ap_se", "dct:publisher",    "dublin_core", "publisher",   "similar",
                   "SE uses a URI; Dublin Core publisher is typically free text. Value degrades."),
    CrosswalkEntry("dcat_ap_se", "dct:creator",      "dublin_core", "creator",     "similar",
                   "SE uses foaf:Agent URI; DC creator is free text. Structure is lost."),
    CrosswalkEntry("dcat_ap_se", "dcat:keyword",     "dublin_core", "subject",     "partial",
                   "DCAT keywords map partially to DC subject; DC subject can also carry "
                   "classification codes whereas DCAT keywords are free text only."),
    CrosswalkEntry("dcat_ap_se", "dct:identifier",   "dublin_core", "identifier",  "exact",
                   "Identical semantic."),
    CrosswalkEntry("dcat_ap_se", "dct:issued",       "dublin_core", "date",        "partial",
                   "DC date is generic; SE issued is specifically the publication date."),
    CrosswalkEntry("dcat_ap_se", "dct:modified",     "dublin_core", "date",        "partial",
                   "DC date is generic; modified is a typed sub-property."),
    CrosswalkEntry("dcat_ap_se", "dct:language",     "dublin_core", "language",    "partial",
                   "SE uses EU NAL URIs; DC language is typically a string tag (BCP 47 / ISO 639)."),
    CrosswalkEntry("dcat_ap_se", "dct:spatial",      "dublin_core", "coverage",    "partial",
                   "Geonames URI maps partially to DC coverage text field."),
    CrosswalkEntry("dcat_ap_se", "dct:license",      "dublin_core", "rights",      "partial",
                   "SE licence URI maps partially to DC rights free text."),
    CrosswalkEntry("dcat_ap_se", "dct:accessRights", "dublin_core", "rights",      "partial",
                   "SE access rights URI collapses with licence into generic DC rights."),
    CrosswalkEntry("dcat_ap_se", "dct:conformsTo",   "dublin_core", "relation",    "partial",
                   "conformsTo maps loosely to DC relation; semantics differ."),
    CrosswalkEntry("dcat_ap_se", "dct:temporal",     "dublin_core", "coverage",    "partial",
                   "Temporal extent maps to DC coverage text; structure is lost."),
    CrosswalkEntry("dcat_ap_se", "dct:source",       "dublin_core", "source",      "exact",
                   "Identical semantic."),
    CrosswalkEntry("dcat_ap_se", "dct:relation",     "dublin_core", "relation",    "exact",
                   "Identical semantic."),
    CrosswalkEntry("dcat_ap_se", "dct:type",         "dublin_core", "type",        "similar",
                   "SE uses EU Dataset Type NAL URIs; DC type uses DCMI Type vocabulary."),
    CrosswalkEntry("dcat_ap_se", "dct:provenance",   "dublin_core", "", "none",
                   "DC has no provenance property."),
    CrosswalkEntry("dcat_ap_se", "dcat:contactPoint","dublin_core", "", "none",
                   "No contact point concept in Dublin Core."),
    CrosswalkEntry("dcat_ap_se", "dcat:theme",       "dublin_core", "subject",     "partial",
                   "EU Data Theme URI maps loosely to DC subject; vocabulary differs."),
    CrosswalkEntry("dcat_ap_se", "dcat:distribution","dublin_core", "format",      "partial",
                   "Distribution URL maps loosely to DC format/relation; structure is lost."),
    CrosswalkEntry("dcat_ap_se", "dcat:accessURL",   "dublin_core", "identifier",  "partial",
                   "Access URL carries similar semantics to a DC identifier (the resource locator)."),
    CrosswalkEntry("dcat_ap_se", "dcat:applicableLegislation", "dublin_core", "", "none",
                   "No equivalent in Dublin Core."),
    CrosswalkEntry("dcat_ap_se", "dcat:hvdCategory", "dublin_core", "", "none",
                   "No equivalent in Dublin Core."),
    CrosswalkEntry("dcat_ap_se", "dcatse:availability", "dublin_core", "", "none",
                   "No equivalent in Dublin Core."),
]

# ---------------------------------------------------------------------------
# DCAT-AP → DCAT-AP-SE (reverse profile direction)
# ---------------------------------------------------------------------------
DCAT_AP_TO_DCAT_AP_SE: List[CrosswalkEntry] = [
    CrosswalkEntry("dcat_ap", "dct:title",       "dcat_ap_se", "dct:title",       "exact",
                   "Identical property — transfers directly."),
    CrosswalkEntry("dcat_ap", "dct:description",  "dcat_ap_se", "dct:description",  "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:publisher",    "dcat_ap_se", "dct:publisher",    "similar",
                   "Transfers as-is; DCAT-AP-SE requires this field — DCAT-AP records "
                   "without a publisher will be invalid in SE."),
    CrosswalkEntry("dcat_ap", "dct:creator",      "dcat_ap_se", "dct:creator",      "exact",
                   "Identical optional property."),
    CrosswalkEntry("dcat_ap", "dcat:contactPoint","dcat_ap_se", "dcat:contactPoint","exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:keyword",     "dcat_ap_se", "dcat:keyword",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:theme",       "dcat_ap_se", "dcat:theme",       "exact",
                   "Same URI and vocabulary."),
    CrosswalkEntry("dcat_ap", "dct:identifier",   "dcat_ap_se", "dct:identifier",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:issued",       "dcat_ap_se", "dct:issued",       "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:modified",     "dcat_ap_se", "dct:modified",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:language",     "dcat_ap_se", "dct:language",     "exact",
                   "Same URI and vocabulary (EU Publications Office language URIs)."),
    CrosswalkEntry("dcat_ap", "dct:spatial",      "dcat_ap_se", "dct:spatial",      "similar",
                   "Transfers as-is if using Geonames or EU NAL URIs; other authority "
                   "file URIs may not align with SE Geonames preference."),
    CrosswalkEntry("dcat_ap", "dct:temporal",     "dcat_ap_se", "dct:temporal",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:license",      "dcat_ap_se", "dct:license",      "similar",
                   "Transfers; SE requires CC0 for Catalog — dataset licence is unconstrained."),
    CrosswalkEntry("dcat_ap", "dct:accessRights", "dcat_ap_se", "dct:accessRights", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:distribution","dcat_ap_se", "dcat:distribution","exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:accrualPeriodicity", "dcat_ap_se", "dct:accrualPeriodicity", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:landingPage", "dcat_ap_se", "dcat:landingPage", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:conformsTo",   "dcat_ap_se", "dct:conformsTo",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:type",         "dcat_ap_se", "dct:type",         "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:provenance",   "dcat_ap_se", "dct:provenance",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:source",       "dcat_ap_se", "dct:source",       "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:isPartOf",     "dcat_ap_se", "dct:isPartOf",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:hasVersion",   "dcat_ap_se", "dct:hasVersion",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:isVersionOf",  "dcat_ap_se", "dct:isVersionOf",  "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:relation",     "dcat_ap_se", "dct:relation",     "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "prov:qualifiedAttribution", "dcat_ap_se", "prov:qualifiedAttribution", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:qualifiedRelation", "dcat_ap_se", "dcat:qualifiedRelation", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:spatialResolutionInMeters", "dcat_ap_se", "dcat:spatialResolutionInMeters", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:temporalResolution", "dcat_ap_se", "dcat:temporalResolution", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "adms:identifier",  "dcat_ap_se", "adms:identifier",  "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "owl:versionInfo",  "dcat_ap_se", "adms:version",     "similar",
                   "Functionally equivalent; SE uses adms:version, DCAT-AP uses owl:versionInfo."),
    CrosswalkEntry("dcat_ap", "dcat:accessURL",   "dcat_ap_se", "dcat:accessURL",   "exact",
                   "Identical mandatory distribution property."),
    CrosswalkEntry("dcat_ap", "dcat:downloadURL", "dcat_ap_se", "dcat:downloadURL", "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dcat:mediaType",   "dcat_ap_se", "dcat:mediaType",   "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "dct:format",       "dcat_ap_se", "dct:format",       "exact",
                   "Identical property."),
    CrosswalkEntry("dcat_ap", "adms:status",      "dcat_ap_se", "",                 "none",
                   "adms:status is defined in DCAT-AP but not included in DCAT-AP-SE 2.2.0."),
    CrosswalkEntry("dcat_ap", "odrl:hasPolicy",   "dcat_ap_se", "",                 "none",
                   "ODRL policy has no direct equivalent in DCAT-AP-SE 2.2.0."),
    CrosswalkEntry("dcat_ap", "dcat:accessService","dcat_ap_se","",                 "none",
                   "accessService not defined in DCAT-AP-SE 2.2.0 Distribution class."),
    CrosswalkEntry("dcat_ap", "adms:sample",      "dcat_ap_se", "",                 "none",
                   "adms:sample not defined in DCAT-AP-SE 2.2.0."),
    CrosswalkEntry("dcat_ap", "dct:isReferencedBy","dcat_ap_se","",                 "none",
                   "Not included in DCAT-AP-SE 2.2.0."),
    CrosswalkEntry("dcat_ap", "dcat:byteSize",    "dcat_ap_se", "",                 "none",
                   "Distribution byte size not included in DCAT-AP-SE 2.2.0 fields."),
]

# ---------------------------------------------------------------------------
# All crosswalk entries combined
# ---------------------------------------------------------------------------
ALL_CROSSWALKS: List[CrosswalkEntry] = (
    ADATP5636_TO_DUBLIN_CORE
    + ADATP5636_TO_DCAT_AP
    + ADATP5636_TO_ISO19115
    + ADATP5636_TO_ISO23081
    + ADATP5636_TO_INSPIRE
    + ADATP5636_TO_NIST
    + NISTIR8112_TO_NCMS
    + DC_TO_ISO19115
    + ADATP5636_TO_DCAT_AP_SE
    + DCAT_AP_SE_TO_DCAT_AP
    + DCAT_AP_SE_TO_DUBLIN_CORE
    + DCAT_AP_TO_DCAT_AP_SE
)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------
def get_crosswalks_from(source_standard: str) -> List[CrosswalkEntry]:
    """Return all crosswalk entries where source_standard matches."""
    return [e for e in ALL_CROSSWALKS if e.source_standard == source_standard]


def get_crosswalks_to(target_standard: str) -> List[CrosswalkEntry]:
    """Return all crosswalk entries where target_standard matches."""
    return [e for e in ALL_CROSSWALKS if e.target_standard == target_standard]


def get_crosswalk(source_standard: str, source_field: str, target_standard: str):
    """Return the crosswalk entry for a specific source field → target standard mapping."""
    for e in ALL_CROSSWALKS:
        if (e.source_standard == source_standard
                and e.source_field.lower() == source_field.lower()
                and e.target_standard == target_standard):
            return e
    return None


def compute_compatibility_score(source_standard_id: str, target_standard_id: str) -> float:
    """
    Compute a 0.0–1.0 compatibility score between two standards.
    Score = proportion of source fields that have a non-'none' mapping in the target.
    """
    from standards.registry import get_standard
    src = get_standard(source_standard_id)
    if src is None:
        return 0.0

    source_fields = list(src.fields.keys())
    if not source_fields:
        return 0.0

    crosswalks = {e.source_field.lower(): e
                  for e in ALL_CROSSWALKS
                  if e.source_standard == source_standard_id
                  and e.target_standard == target_standard_id}

    mapped = 0
    for sf in source_fields:
        entry = crosswalks.get(sf.lower())
        if entry and entry.mapping_type != "none":
            mapped += 1

    return mapped / len(source_fields)


def build_compatibility_matrix() -> Dict[str, Dict[str, float]]:
    """Build a full N×N compatibility matrix across all registered standards."""
    from standards.registry import get_all_standards
    standards = get_all_standards()
    ids = [s.id for s in standards]
    matrix: Dict[str, Dict[str, float]] = {}
    for src_id in ids:
        matrix[src_id] = {}
        for tgt_id in ids:
            if src_id == tgt_id:
                matrix[src_id][tgt_id] = 1.0
            else:
                matrix[src_id][tgt_id] = compute_compatibility_score(src_id, tgt_id)
    return matrix


# ---------------------------------------------------------------------------
# Known structural conflicts
# ---------------------------------------------------------------------------

KNOWN_CONFLICTS: List[ConflictEntry] = [

    # ── ADatP-5636 security layer — no equivalent anywhere outside NATO ──────

    ConflictEntry(
        source_standard="adatp5636", target_standard="dublin_core",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="metadataConfidentialityLabel",
        title="Metadata-level security label has no Dublin Core equivalent",
        description=(
            "ADatP-5636 mandates a metadataConfidentialityLabel — an ADatP-4774 "
            "structured label that classifies the metadata record itself (separate "
            "from the resource it describes). Dublin Core has no security model "
            "whatsoever. Any ADatP-5636 record exported to Dublin Core permanently "
            "loses the access controls governing who may read the metadata, making "
            "the export non-conformant with the source standard."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dublin_core",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="originatorConfidentialityLabel",
        title="Resource classification label cannot be expressed in Dublin Core",
        description=(
            "ADatP-5636 mandates an originatorConfidentialityLabel using ADatP-4774 "
            "syntax, which encodes PolicyIdentifier, Classification level, releasability "
            "caveats, and compartments. Dublin Core has no concept for security "
            "classification. Exporting to Dublin Core silently discards all security "
            "constraints on the resource itself."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="metadataConfidentialityLabel",
        title="Metadata-level security label has no DCAT-AP equivalent",
        description=(
            "Same as the Dublin Core conflict: DCAT-AP inherits Dublin Core's lack "
            "of a security model. The mandatory ADatP-4774 metadata label cannot be "
            "represented and is lost on export."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="originatorConfidentialityLabel",
        title="Resource classification label cannot be expressed in DCAT-AP",
        description=(
            "DCAT-AP has no field for security classification. The full ADatP-4774 "
            "label structure (classification level, caveats, compartments) is discarded "
            "on export."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="iso19115",
        conflict_type="mandatory_gap", severity="lossy",
        source_field="originatorConfidentialityLabel",
        title="ADatP-4774 label structure only partially maps to ISO 19115 classification",
        description=(
            "ISO 19115 supports MD_SecurityConstraints with a classification code "
            "(unclassified / restricted / confidential / secret / topSecret), but "
            "this captures only the classification level. The ADatP-4774 label also "
            "encodes releasability (e.g. REL TO FVEY), handling caveats, and "
            "compartment markings — none of which ISO 19115 can represent. "
            "Conversion is possible but degrades a rich security label to a single code."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="inspire",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="metadataConfidentialityLabel",
        title="Metadata-level security label has no INSPIRE equivalent",
        description=(
            "INSPIRE metadata is designed for public open-data discovery. It has no "
            "mechanism for classifying the metadata record itself. The mandatory "
            "ADatP-4774 label is lost on export."
        ),
    ),

    # ── Obligation inversions ────────────────────────────────────────────────

    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap",
        conflict_type="obligation_inversion", severity="lossy",
        source_field="description", target_field="dct:description",
        title="Description is optional in ADatP-5636 but mandatory in DCAT-AP",
        description=(
            "DCAT-AP mandates dct:description for every dataset. ADatP-5636 makes "
            "description optional. NATO metadata records without a description field "
            "cannot be imported into a DCAT-AP compliant system without either "
            "synthesising a description from other fields or failing validation."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="iso19115",
        conflict_type="obligation_inversion", severity="transform_required",
        source_field="language", target_field="language",
        title="Language is optional in ADatP-5636 but mandatory in ISO 19115",
        description=(
            "ISO 19115 requires the metadata language to be explicitly stated "
            "(ISO 639-2/B code). ADatP-5636 treats language as optional. Records "
            "without a language field cannot be valid ISO 19115 without inference "
            "or manual augmentation."
        ),
    ),

    # ── Vocabulary / encoding incompatibilities ──────────────────────────────

    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap",
        conflict_type="vocabulary", severity="transform_required",
        source_field="accessRights", target_field="dct:accessRights",
        title="Access rights use incompatible encodings",
        description=(
            "ADatP-5636 accessRights is free text (e.g. 'Authorised NATO personnel only'). "
            "DCAT-AP dct:accessRights requires a URI from the EU Publications Office "
            "Access Rights Named Authority List "
            "(e.g. http://publications.europa.eu/resource/authority/access-right/RESTRICTED). "
            "NATO-specific access policies have no EU NAL equivalent, so direct conversion "
            "fails. A custom mapping table is required, and NATO-specific caveats are lost."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="inspire",
        conflict_type="vocabulary", severity="transform_required",
        source_field="geographicReference",
        title="Geographic encoding: multiple NATO schemes vs. WGS84-only INSPIRE requirement",
        description=(
            "ADatP-5636 geographicReference supports MGRS, UTM, WGS84-DD, WGS84-DMS, "
            "GeoJSON, WKT, and GeoNames. INSPIRE requires geographic extent as a WGS84 "
            "bounding box. Military grid references (MGRS, UTM) must be transformed to "
            "WGS84 — a lossy conversion for some representations — and point references "
            "must be expanded to bounding boxes, which may not always be meaningful."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="iso19115",
        conflict_type="vocabulary", severity="transform_required",
        source_field="geographicReference",
        title="Geographic encoding: multiple NATO schemes vs. ISO 19115 bounding box",
        description=(
            "Same core issue as INSPIRE: ISO 19115 EX_GeographicBoundingBox expects "
            "WGS84 decimal degrees. MGRS and UTM references require coordinate "
            "transformation before they can populate ISO 19115 geographic extent fields."
        ),
    ),

    # ── Orthogonal domain mismatch ───────────────────────────────────────────

    ConflictEntry(
        source_standard="adatp5636", target_standard="nist_ir8112",
        conflict_type="domain_mismatch", severity="blocking",
        title="ADatP-5636 and NIST IR 8112 operate in orthogonal domains",
        description=(
            "ADatP-5636 describes information resources (documents, datasets, files). "
            "NIST IR 8112 describes identity attributes of persons and systems in "
            "federated authentication scenarios. The standards share almost no semantic "
            "overlap. Attempting to merge or convert between them produces records that "
            "are either invalid or semantically misleading. The only meaningful "
            "relationship is that IR 8112 attribute metadata can describe the identity "
            "of the persons recorded in ADatP-5636 creator/publisher fields — but this "
            "is a reference relationship, not a field-level mapping."
        ),
    ),
    ConflictEntry(
        source_standard="nist_ir8112", target_standard="adatp5636",
        conflict_type="domain_mismatch", severity="blocking",
        title="NIST IR 8112 identity attribute fields have no resource metadata equivalents",
        description=(
            "NIST IR 8112 fields such as attributeValue, attributeVerification, "
            "attributeAccuracy, attributeConsistency, and relyingParty describe the "
            "data quality and provenance of identity claims in federated systems. "
            "ADatP-5636 has no fields for these concepts because it describes resources, "
            "not identity attributes. Conversion in this direction destroys all the "
            "specific meaning that IR 8112 encodes."
        ),
    ),

    # ── Records management absence ───────────────────────────────────────────

    ConflictEntry(
        source_standard="adatp5636", target_standard="dublin_core",
        conflict_type="structural", severity="lossy",
        source_field="recordsDisposition",
        title="Records disposition has no equivalent in Dublin Core",
        description=(
            "NATO information objects are official records subject to retention and "
            "disposition schedules. ADatP-5636 includes recordsDisposition and "
            "dateDisposition for this purpose. Dublin Core has no records management "
            "model. Exporting NATO records to Dublin Core silently loses all lifecycle "
            "management instructions."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap",
        conflict_type="structural", severity="lossy",
        source_field="recordsDisposition",
        title="Records disposition has no equivalent in DCAT-AP",
        description=(
            "Same as Dublin Core: DCAT-AP models open datasets for discovery and access, "
            "not records subject to formal retention policies. Disposition instructions "
            "are lost on export."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="iso19115",
        conflict_type="structural", severity="lossy",
        source_field="recordsDisposition",
        title="Records disposition has no equivalent in ISO 19115",
        description=(
            "ISO 19115 covers geographic information discovery metadata, not records "
            "management. Disposition schedules for NATO geospatial records cannot be "
            "carried into ISO 19115; ISO 23081 would be required as a complementary standard."
        ),
    ),

    # ── ADatP-5636 → DCAT-AP-SE ─────────────────────────────────────────────

    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="metadataConfidentialityLabel",
        title="Metadata-level security label has no DCAT-AP-SE equivalent",
        description=(
            "DCAT-AP-SE inherits DCAT-AP's lack of a security model. The mandatory "
            "ADatP-4774 metadata confidentiality label — which classifies the metadata "
            "record itself — cannot be expressed and is permanently lost on export. "
            "Any ADatP-5636 record is non-conformant with SE once this label is removed."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="mandatory_gap", severity="blocking",
        source_field="originatorConfidentialityLabel",
        title="Resource classification label cannot be expressed in DCAT-AP-SE",
        description=(
            "DCAT-AP-SE has no field for NATO security classification. The full ADatP-4774 "
            "label structure (classification level, releasability caveats, compartments) "
            "is discarded on export. A partial mapping to dct:accessRights is possible "
            "for the top-level classification (PUBLIC / RESTRICTED / NON_PUBLIC), but "
            "all NATO-specific caveats (e.g. REL TO FVEY, NF) are lost."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="obligation_inversion", severity="blocking",
        source_field="publisher", target_field="dct:publisher",
        title="Publisher is optional in ADatP-5636 but mandatory in DCAT-AP-SE",
        description=(
            "DCAT-AP-SE elevates publisher to mandatory (unlike base DCAT-AP where it "
            "is only recommended). NATO ADatP-5636 treats publisher as optional. Records "
            "without a publisher field cannot be imported into a DCAT-AP-SE compliant "
            "Swedish data portal without augmentation. Note: the publisher value must also "
            "be a URI (foaf:Agent) — a plain text organisation name is not valid in SE."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="obligation_inversion", severity="lossy",
        source_field="description", target_field="dct:description",
        title="Description is optional in ADatP-5636 but mandatory in DCAT-AP-SE",
        description=(
            "DCAT-AP-SE mandates dct:description for every dataset (inherited from DCAT-AP). "
            "ADatP-5636 treats description as optional. NATO records without a description "
            "cannot pass SE validation without synthesising one from other fields."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="vocabulary", severity="transform_required",
        source_field="accessRights", target_field="dct:accessRights",
        title="Access rights use incompatible encodings",
        description=(
            "ADatP-5636 accessRights is free text (e.g. 'Authorised NATO personnel only'). "
            "DCAT-AP-SE dct:accessRights requires a URI from the EU Publications Office "
            "Access Rights NAL (PUBLIC / RESTRICTED / NON_PUBLIC). "
            "NATO-specific access policies have no direct EU NAL equivalent — a mapping "
            "table is required, and NATO-specific caveats are lost."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="vocabulary", severity="transform_required",
        source_field="language", target_field="dct:language",
        title="Language codes: ISO 639-3 alpha-3 vs EU Language NAL URI",
        description=(
            "ADatP-5636 language uses ISO 639-3 alpha-3 codes (eng, fra, deu). "
            "DCAT-AP-SE requires a URI from the EU Publications Office language NAL "
            "(e.g. http://publications.europa.eu/resource/authority/language/ENG). "
            "Values must be converted to URIs before SE import; codes not in the EU "
            "language NAL have no valid target."
        ),
    ),
    ConflictEntry(
        source_standard="adatp5636", target_standard="dcat_ap_se",
        conflict_type="structural", severity="lossy",
        source_field="recordsDisposition",
        title="Records disposition has no equivalent in DCAT-AP-SE",
        description=(
            "DCAT-AP-SE models open datasets for discovery and access, not records "
            "subject to formal NATO retention and disposition policies. Disposition "
            "instructions are lost on export."
        ),
    ),
]


def compute_conversion_paths(id_a: str, id_c: str) -> dict:
    """
    Find all conversion paths from standard A to standard C up to 2 hops.

    A "hop" exists between two standards when there is at least one non-none
    crosswalk entry between them. The score for a hop is the compatibility
    score (fraction of source fields with a non-none mapping). The path score
    is the minimum leg score (weakest link).

    Returns a dict with:
      direct   : path dict or None  (A→C direct)
      via_one  : list of path dicts (A→B→C, sorted by path_score desc)

    Each path dict has:
      steps        : list of standard IDs  e.g. ['adatp5636','dublin_core','iso19115']
      leg_scores   : list of floats, one per leg
      path_score   : float — min(leg_scores)
      leg_labels   : list of "source → target" strings
      quality      : "good" | "fair" | "poor"
    """
    from standards.registry import get_all_standards, get_standard

    all_stds = [s.id for s in get_all_standards()]

    # Build crosswalk graph: node→node with score
    def _score(src: str, tgt: str) -> float:
        return compute_compatibility_score(src, tgt)

    def _has_crosswalk(src: str, tgt: str) -> bool:
        return any(
            e for e in ALL_CROSSWALKS
            if e.source_standard == src and e.target_standard == tgt
            and e.mapping_type != "none"
        )

    def _make_path(steps: list) -> dict:
        leg_scores = [_score(steps[i], steps[i + 1]) for i in range(len(steps) - 1)]
        path_score = min(leg_scores) if leg_scores else 0.0
        leg_labels = [f"{get_standard(steps[i]).name} → {get_standard(steps[i+1]).name}"
                      for i in range(len(steps) - 1)]
        quality = "good" if path_score >= 0.40 else ("fair" if path_score >= 0.20 else "poor")
        return {
            "steps": steps,
            "step_names": [get_standard(s).name for s in steps],
            "leg_scores": leg_scores,
            "path_score": path_score,
            "leg_labels": leg_labels,
            "quality": quality,
        }

    # Direct path
    direct = None
    if _has_crosswalk(id_a, id_c):
        direct = _make_path([id_a, id_c])

    # One-intermediate paths
    via_one = []
    for mid in all_stds:
        if mid in (id_a, id_c):
            continue
        if _has_crosswalk(id_a, mid) and _has_crosswalk(mid, id_c):
            via_one.append(_make_path([id_a, mid, id_c]))

    via_one.sort(key=lambda p: p["path_score"], reverse=True)

    return {
        "direct": direct,
        "via_one": via_one,
    }


def compute_roundtrip(id_a: str, id_b: str) -> dict:
    """
    Simulate an A→B→A round-trip conversion for every field in standard A.

    For each field in A:
      1. Find the A→B crosswalk entry (leg 1)
      2. If leg 1 maps to a B field, find the B→A crosswalk entry for that field (leg 2)
      3. Classify the round-trip outcome:
           survives  — both legs are exact or similar; field comes back intact
           degraded  — at least one leg is partial; value may be approximate
           lost      — leg 1 is none/missing OR leg 2 is none/missing

    Returns a dict with:
      fields   : list of dicts, one per field in A, sorted by status then name
      summary  : {survives, degraded, lost, total}
    """
    # Build lookup dicts for both directions
    ab_index: Dict[str, CrosswalkEntry] = {
        e.source_field.lower(): e
        for e in ALL_CROSSWALKS
        if e.source_standard == id_a and e.target_standard == id_b
    }
    # Explicit B→A entries
    ba_index: Dict[str, CrosswalkEntry] = {
        e.source_field.lower(): e
        for e in ALL_CROSSWALKS
        if e.source_standard == id_b and e.target_standard == id_a
    }
    # Infer reverse leg from A→B entries when no explicit B→A exists.
    # If A.x maps to B.y (leg 1), and there is no B.y→A entry, synthesise one
    # with the same mapping_type. This lets round-trip work even for
    # one-directional crosswalk data.
    for e in ALL_CROSSWALKS:
        if e.source_standard != id_a or e.target_standard != id_b:
            continue
        if not e.target_field:
            continue
        key = e.target_field.lower()
        if key not in ba_index:
            ba_index[key] = CrosswalkEntry(
                source_standard=id_b,
                source_field=e.target_field,
                target_standard=id_a,
                target_field=e.source_field,
                mapping_type=e.mapping_type,
                notes="(inferred reverse)",
            )

    from standards.registry import get_standard
    src = get_standard(id_a)
    if src is None:
        return {"fields": [], "summary": {"survives": 0, "degraded": 0, "lost": 0, "total": 0}}

    _GOOD = {"exact", "similar"}
    _PARTIAL = {"partial"}

    rows = []
    for fname, fdef in src.fields.items():
        leg1 = ab_index.get(fname.lower())

        if leg1 is None or leg1.mapping_type == "none" or not leg1.target_field:
            status = "lost"
            leg2 = None
        else:
            leg2 = ba_index.get(leg1.target_field.lower())
            if leg2 is None or leg2.mapping_type == "none":
                status = "lost"
            elif leg1.mapping_type in _GOOD and leg2.mapping_type in _GOOD:
                status = "survives"
            else:
                status = "degraded"

        rows.append({
            "field": fname,
            "obligation": fdef.obligation.value if hasattr(fdef.obligation, "value") else str(fdef.obligation),
            "description": fdef.description,
            "status": status,
            "leg1_field": leg1.target_field if leg1 else None,
            "leg1_type": leg1.mapping_type if leg1 else None,
            "leg1_notes": leg1.notes if leg1 else "",
            "leg2_field": leg2.source_field if leg2 else None,
            "leg2_type": leg2.mapping_type if leg2 else None,
            "leg2_notes": leg2.notes if leg2 else "",
        })

    order = {"survives": 0, "degraded": 1, "lost": 2}
    rows.sort(key=lambda r: (order[r["status"]], r["field"]))

    summary = {
        "survives": sum(1 for r in rows if r["status"] == "survives"),
        "degraded": sum(1 for r in rows if r["status"] == "degraded"),
        "lost":     sum(1 for r in rows if r["status"] == "lost"),
        "total":    len(rows),
    }
    return {"fields": rows, "summary": summary}


def compute_verdict(
    score_ab: float,
    score_ba: float,
    conflicts_ab: list,
    conflicts_ba: list,
    same_suite: bool,
) -> dict:
    """
    Synthesise a single interoperability verdict for a standard pair.

    Returns a dict with:
      label       : short human label
      sublabel    : one-sentence explanation
      level       : "suite" | "high" | "medium" | "partial" | "low"
      color       : hex colour for the badge
    """
    all_conflicts = conflicts_ab + conflicts_ba
    has_blocking = any(c["severity"] == "blocking" for c in all_conflicts)
    has_lossy    = any(c["severity"] == "lossy"    for c in all_conflicts)
    has_transform = any(c["severity"] == "transform_required" for c in all_conflicts)
    min_score = min(score_ab, score_ba)
    max_score = max(score_ab, score_ba)

    if same_suite:
        return {
            "label": "Designed to work together",
            "sublabel": "These standards are part of the same suite and are explicitly designed to interoperate.",
            "level": "suite",
            "color": "#003189",
        }

    if not has_blocking and not has_lossy and min_score >= 0.50:
        return {
            "label": "Highly interoperable",
            "sublabel": "Both standards share strong bidirectional field coverage with no blocking or data-loss conflicts.",
            "level": "high",
            "color": "#198754",
        }

    if not has_blocking and not has_lossy and (has_transform or min_score >= 0.25):
        return {
            "label": "Interoperable with transformation",
            "sublabel": "Conversion is possible but requires a defined transformation step; no data is permanently lost.",
            "level": "medium",
            "color": "#0d6efd",
        }

    if has_lossy and not has_blocking:
        return {
            "label": "Partial data loss",
            "sublabel": "Conversion loses some information; records may not be fully conformant after translation.",
            "level": "partial",
            "color": "#fd7e14",
        }

    if has_blocking or max_score < 0.25:
        return {
            "label": "Not fully interoperable",
            "sublabel": "Blocking conflicts or very low field coverage prevent full bidirectional conversion.",
            "level": "low",
            "color": "#dc3545",
        }

    # Fallback for mixed / edge cases
    return {
        "label": "Limited interoperability",
        "sublabel": "Some fields can be mapped but significant gaps or conflicts remain.",
        "level": "partial",
        "color": "#fd7e14",
    }


def build_pairwise_data(id_a: str, id_b: str) -> dict:
    """
    Build a complete comparison dict for a pair of standards.

    Returns:
      std_a / std_b          : standard objects
      score_ab / score_ba    : float 0-1 directional scores
      suite                  : StandardSuite | None  (shared suite if any)
      relationship_ab        : str | None  (relationship of b in the shared suite, from a's perspective)
      conflicts_ab           : list[dict]  (build_conflicts a→b)
      conflicts_ba           : list[dict]  (build_conflicts b→a)
      mappings_ab            : list[CrosswalkEntry]  (a→b entries, non-none only)
      mappings_ba            : list[CrosswalkEntry]  (b→a entries, non-none only)
      all_mappings_ab        : list[CrosswalkEntry]  (all a→b including none)
      all_mappings_ba        : list[CrosswalkEntry]  (all b→a including none)
    """
    from standards.registry import get_standard
    from standards.suites import get_suites_for_standard

    std_a = get_standard(id_a)
    std_b = get_standard(id_b)

    score_ab = compute_compatibility_score(id_a, id_b)
    score_ba = compute_compatibility_score(id_b, id_a)

    # Find a shared suite
    suites_a = {s.id: s for s in get_suites_for_standard(id_a)}
    suites_b = {s.id: s for s in get_suites_for_standard(id_b)}
    shared_suite = None
    rel_ab = None   # relationship of B as seen from the shared suite
    rel_ba = None
    for sid in suites_a:
        if sid in suites_b:
            shared_suite = suites_a[sid]
            mem_a = shared_suite.get_member(id_a)
            mem_b = shared_suite.get_member(id_b)
            rel_ab = mem_b.relationship if mem_b else None
            rel_ba = mem_a.relationship if mem_a else None
            break

    all_ab = [e for e in ALL_CROSSWALKS if e.source_standard == id_a and e.target_standard == id_b]
    all_ba = [e for e in ALL_CROSSWALKS if e.source_standard == id_b and e.target_standard == id_a]

    def _enrich(entries, src_std, tgt_std):
        """Return list of dicts adding source_ref / target_ref to each crosswalk entry."""
        result = []
        for e in entries:
            src_ref = ""
            tgt_ref = ""
            if src_std and e.source_field in src_std.fields:
                src_ref = src_std.fields[e.source_field].reference
            if tgt_std and e.target_field and e.target_field in tgt_std.fields:
                tgt_ref = tgt_std.fields[e.target_field].reference
            result.append({
                "source_field": e.source_field,
                "target_field": e.target_field,
                "mapping_type": e.mapping_type,
                "notes": e.notes,
                "source_ref": src_ref,
                "target_ref": tgt_ref,
            })
        return result

    enriched_ab = _enrich(all_ab, std_a, std_b)
    enriched_ba = _enrich(all_ba, std_b, std_a)

    def _build_full_fields(enriched_entries, src_std, tgt_std):
        """Unified field coverage list for one direction.

        Produces rows for:
        - Every source field: with its crosswalk entry (if one exists) or a
          synthetic 'no entry' row (row_type='source_only')
        - Every target field that receives no mapping from the source
          (row_type='target_only')

        This lets the UI show the complete picture of which fields are covered,
        partially covered, or not covered at all in either direction.
        """
        cw_index = {e["source_field"]: e for e in enriched_entries}
        mapped_tgt = {e["target_field"] for e in enriched_entries if e["target_field"]}
        rows = []

        # ── All source fields ──────────────────────────────────────────────
        if src_std:
            for fname, fdef in src_std.fields.items():
                if fname in cw_index:
                    e = cw_index[fname]
                    tgt_obl = ""
                    if tgt_std and e["target_field"] and e["target_field"] in tgt_std.fields:
                        tgt_obl = tgt_std.fields[e["target_field"]].obligation.value
                    rows.append({
                        "row_type": "mapped",
                        "source_field": fname,
                        "source_ref": e["source_ref"],
                        "source_obligation": fdef.obligation.value,
                        "target_field": e["target_field"],
                        "target_ref": e["target_ref"],
                        "target_obligation": tgt_obl,
                        "mapping_type": e["mapping_type"],
                        "notes": e["notes"],
                    })
                else:
                    # Source field exists but has no crosswalk entry at all
                    rows.append({
                        "row_type": "source_only",
                        "source_field": fname,
                        "source_ref": fdef.reference,
                        "source_obligation": fdef.obligation.value,
                        "target_field": None,
                        "target_ref": "",
                        "target_obligation": "",
                        "mapping_type": "-",
                        "notes": "No crosswalk entry defined",
                    })

        # ── Target fields that receive no mapping from source ──────────────
        if tgt_std:
            for fname, fdef in tgt_std.fields.items():
                if fname not in mapped_tgt:
                    rows.append({
                        "row_type": "target_only",
                        "source_field": None,
                        "source_ref": "",
                        "source_obligation": "",
                        "target_field": fname,
                        "target_ref": fdef.reference,
                        "target_obligation": fdef.obligation.value,
                        "mapping_type": "-",
                        "notes": "No source mapping defined",
                    })

        return rows

    full_fields_ab = _build_full_fields(enriched_ab, std_a, std_b)
    full_fields_ba = _build_full_fields(enriched_ba, std_b, std_a)

    conflicts_ab = build_conflicts(id_a, id_b)
    conflicts_ba = build_conflicts(id_b, id_a)

    verdict = compute_verdict(
        score_ab=score_ab,
        score_ba=score_ba,
        conflicts_ab=conflicts_ab,
        conflicts_ba=conflicts_ba,
        same_suite=shared_suite is not None,
    )

    return {
        "std_a": std_a,
        "std_b": std_b,
        "score_ab": score_ab,
        "score_ba": score_ba,
        "suite": shared_suite,
        "relationship_ab": rel_ab,
        "relationship_ba": rel_ba,
        "conflicts_ab": conflicts_ab,
        "conflicts_ba": conflicts_ba,
        "mappings_ab": [e for e in enriched_ab if e["mapping_type"] != "none"],
        "mappings_ba": [e for e in enriched_ba if e["mapping_type"] != "none"],
        "all_mappings_ab": enriched_ab,
        "all_mappings_ba": enriched_ba,
        "full_fields_ab": full_fields_ab,
        "full_fields_ba": full_fields_ba,
        "verdict": verdict,
        "roundtrip_ab": compute_roundtrip(id_a, id_b),
        "roundtrip_ba": compute_roundtrip(id_b, id_a),
        "paths_ab": compute_conversion_paths(id_a, id_b),
        "paths_ba": compute_conversion_paths(id_b, id_a),
        "sources": get_pair_sources(id_a, id_b),
        "value_issues": get_value_issues(id_a, id_b),
    }


def get_conflicts(source_standard: str, target_standard: str) -> List[ConflictEntry]:
    """Return all known conflicts for a given standard pair (directional)."""
    return [
        c for c in KNOWN_CONFLICTS
        if c.source_standard == source_standard and c.target_standard == target_standard
    ]


def build_conflicts(source_standard_id: str, target_standard_id: str) -> List[Dict]:
    """
    Return a combined list of conflict dicts for a source→target pair.

    Each dict has:
      source        : str
      target        : str
      conflict_type : str
      severity      : str
      title         : str
      source_field  : str
      target_field  : str
      description   : str
      auto_detected : bool  — True for gaps derived from crosswalk data
    """
    from standards.registry import get_standard
    from standards.base import Obligation

    results = []

    # 1. Known structural conflicts
    for c in get_conflicts(source_standard_id, target_standard_id):
        results.append({
            "source": c.source_standard,
            "target": c.target_standard,
            "conflict_type": c.conflict_type,
            "severity": c.severity,
            "title": c.title,
            "source_field": c.source_field,
            "target_field": c.target_field,
            "description": c.description,
            "auto_detected": False,
        })

    known_fields = {c.source_field for c in get_conflicts(source_standard_id, target_standard_id)}

    # 2. Auto-detect mandatory gaps not already covered by known conflicts
    src = get_standard(source_standard_id)
    if src:
        crosswalk_index = {
            e.source_field.lower(): e
            for e in ALL_CROSSWALKS
            if e.source_standard == source_standard_id
            and e.target_standard == target_standard_id
        }
        for fname, fdef in src.fields.items():
            if fdef.obligation != Obligation.MANDATORY:
                continue
            if fname in known_fields:
                continue
            entry = crosswalk_index.get(fname.lower())
            if entry is None or entry.mapping_type == "none":
                tgt_name = get_standard(target_standard_id)
                tgt_label = tgt_name.name if tgt_name else target_standard_id
                results.append({
                    "source": source_standard_id,
                    "target": target_standard_id,
                    "conflict_type": "mandatory_gap",
                    "severity": "blocking",
                    "title": f"Mandatory field '{fname}' has no equivalent in {tgt_label}",
                    "source_field": fname,
                    "target_field": "",
                    "description": (
                        f"'{fname}' is mandatory in {src.name} but has no defined mapping "
                        f"to {tgt_label}. A fully conformant {src.name} record cannot be "
                        f"converted to a fully conformant {tgt_label} record without "
                        f"discarding this required field."
                    ),
                    "auto_detected": True,
                })

    return results
