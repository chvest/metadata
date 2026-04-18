"""
ISO 23081-1:2017 — Information and Documentation — Records Management Metadata.
Part 1: Principles.

ISO 23081 defines a framework for creating, managing and using metadata for records
within or across organisations. It supports the management of records throughout
their lifecycle from creation to disposition.

Reference:
  ISO 23081-1:2017 — Records Management Metadata — Principles
  ISO 23081-2:2009 — Conceptual and Implementation Issues
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_23081 = "http://www.iso.org/ns/records-metadata/1.0"


FIELDS: Dict[str, FieldDefinition] = {

    # ── Mandatory ─────────────────────────────────────────────────────────────
    "identifier": FieldDefinition(
        name="identifier",
        description=(
            "A unique identifier for the record. Should be a persistent, "
            "unambiguous reference that enables the record to be found and "
            "distinguished from all other records."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or alphanumeric code per record series scheme",
        reference="ISO 23081-1:2017 §7.2.1",
        layer="Core",
        group="",
        xml_element="identifier",
        namespace=NS_23081,
    ),
    "title": FieldDefinition(
        name="title",
        description=(
            "The name given to the record. "
            "May be a formal title, a subject heading, or a file reference. "
            "Should be sufficient to identify the record without ambiguity."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 23081-1:2017 §7.2.2",
        layer="Core",
        group="",
        xml_element="title",
        namespace=NS_23081,
    ),
    "creator": FieldDefinition(
        name="creator",
        description=(
            "The agent (person, organisation, or system) who created the record. "
            "The creator is responsible for the intellectual content of the record."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.NAME,
        values="Agent name or URI; may include role qualifier",
        reference="ISO 23081-1:2017 §7.2.3",
        layer="Core",
        group="",
        xml_element="creator",
        namespace=NS_23081,
    ),
    "dateCreated": FieldDefinition(
        name="dateCreated",
        description=(
            "The date on which the record was created. "
            "Mandatory. Used for lifecycle management and retrieval."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime",
        reference="ISO 23081-1:2017 §7.2.4",
        layer="Core",
        group="Date",
        xml_element="dateCreated",
        namespace=NS_23081,
    ),
    "type": FieldDefinition(
        name="type",
        description=(
            "The genre or type of record. Indicates whether the record is a "
            "letter, report, contract, policy, form, etc. "
            "Should use a controlled vocabulary."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="Controlled vocabulary: letter | report | contract | policy | form | order | invoice | minutes | correspondence | other",
        reference="ISO 23081-1:2017 §7.2.5",
        layer="Core",
        group="",
        xml_element="type",
        namespace=NS_23081,
    ),
    "format": FieldDefinition(
        name="format",
        description=(
            "The physical or digital format of the record. "
            "Essential for understanding access requirements and migration planning."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="IANA MIME type or descriptive format name, e.g., PDF/A, DOCX, TIFF",
        reference="ISO 23081-1:2017 §7.2.6",
        layer="Core",
        group="",
        xml_element="format",
        namespace=NS_23081,
    ),

    # ── Date group ────────────────────────────────────────────────────────────
    "dateModified": FieldDefinition(
        name="dateModified",
        description="The date on which the record was last changed.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ISO 23081-1:2017 §7.3.1",
        layer="Core",
        group="Date",
        xml_element="dateModified",
        namespace=NS_23081,
    ),
    "dateClosed": FieldDefinition(
        name="dateClosed",
        description="The date on which the record was closed (no longer subject to active modification).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ISO 23081-1:2017 §7.3.2",
        layer="Core",
        group="Date",
        xml_element="dateClosed",
        namespace=NS_23081,
    ),

    # ── Optional ──────────────────────────────────────────────────────────────
    "aggregation": FieldDefinition(
        name="aggregation",
        description=(
            "The series, sub-series, file, or other aggregation to which the record belongs. "
            "Provides context for the record within the records system."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Series reference or file reference code",
        reference="ISO 23081-1:2017 §7.4.1",
        layer="Core",
        group="",
        xml_element="aggregation",
        namespace=NS_23081,
    ),
    "rights": FieldDefinition(
        name="rights",
        description="Information about rights held in and over the record.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Rights statement text or URI",
        reference="ISO 23081-1:2017 §7.4.2",
        layer="Core",
        group="",
        xml_element="rights",
        namespace=NS_23081,
    ),
    "access": FieldDefinition(
        name="access",
        description=(
            "Access conditions for the record. "
            "Specifies who may access the record and under what conditions."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Access conditions text; classification level; access control list",
        reference="ISO 23081-1:2017 §7.4.3",
        layer="Core",
        group="",
        xml_element="access",
        namespace=NS_23081,
    ),
    "description": FieldDefinition(
        name="description",
        description="An account of the content of the record.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 23081-1:2017 §7.4.4",
        layer="Core",
        group="",
        xml_element="description",
        namespace=NS_23081,
    ),
    "subject": FieldDefinition(
        name="subject",
        description="The topic of the record.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or controlled vocabulary term",
        reference="ISO 23081-1:2017 §7.4.5",
        layer="Core",
        group="",
        xml_element="subject",
        namespace=NS_23081,
    ),
    "language": FieldDefinition(
        name="language",
        description="A language of the record.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-2/B code",
        reference="ISO 23081-1:2017 §7.4.6",
        layer="Core",
        group="",
        xml_element="language",
        namespace=NS_23081,
    ),
    "disposition": FieldDefinition(
        name="disposition",
        description=(
            "The disposal instruction or authority governing the retention "
            "and final disposition of the record. "
            "Linked to a records authority or disposal schedule."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Disposal authority reference; retention period; final action (transfer|destroy|retain permanently)",
        reference="ISO 23081-1:2017 §7.4.7",
        layer="Core",
        group="",
        xml_element="disposition",
        namespace=NS_23081,
    ),
    "status": FieldDefinition(
        name="status",
        description="The current lifecycle status of the record.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="active | inactive | closed | transferred | destroyed | permanent",
        reference="ISO 23081-1:2017 §7.4.8",
        layer="Core",
        group="",
        xml_element="status",
        namespace=NS_23081,
    ),
    "agent": FieldDefinition(
        name="agent",
        description=(
            "An agent (person, organisation, or system) associated with the record "
            "in a role other than creator (e.g., author, addressee, authoriser)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.NAME,
        values="Agent name or URI with role qualifier",
        reference="ISO 23081-1:2017 §7.4.9",
        layer="Core",
        group="",
        xml_element="agent",
        namespace=NS_23081,
    ),
    "mandate": FieldDefinition(
        name="mandate",
        description=(
            "The legal or organisational mandate that requires the record to be created "
            "or retained. Links business activity to record keeping obligations."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Mandate reference: legislation, regulation, policy, or standard",
        reference="ISO 23081-1:2017 §7.4.10",
        layer="Core",
        group="",
        xml_element="mandate",
        namespace=NS_23081,
    ),
    "use": FieldDefinition(
        name="use",
        description=(
            "A log or description of the use of the record, including who accessed it "
            "and for what purpose."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text use log or structured audit trail",
        reference="ISO 23081-1:2017 §7.4.11",
        layer="Core",
        group="",
        xml_element="use",
        namespace=NS_23081,
    ),
}


class ISO23081Standard(MetadataStandard):
    """ISO 23081-1:2017 — Records Management Metadata."""

    id = "iso23081"
    name = "ISO 23081-1"
    full_name = "ISO 23081-1:2017 Records Management Metadata"
    version = "2017"
    organization = "ISO/TC 46/SC 11"
    domain = "ISO"
    description = (
        "ISO 23081-1 defines a framework for creating, managing and using metadata "
        "for records. It establishes principles for understanding and implementing "
        "metadata in records management systems across the full records lifecycle. "
        "It is particularly relevant for government and defence record management, "
        "providing crosswalks with Dublin Core and other metadata standards."
    )
    reference = "ISO 23081-1:2017"
    namespace = NS_23081
    fields = FIELDS

    _ns_markers = ["iso.org/ns/records", "23081", "records-metadata", "recordsmanagement"]
    _mandatory_fields = ["identifier", "title", "creator", "dateCreated", "type", "format"]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.4
                break

        mand_hits = sum(1 for f in self._mandatory_fields if f.lower() in meta_lower)
        score += (mand_hits / len(self._mandatory_fields)) * 0.4

        records_specific = ["aggregation", "disposition", "mandate", "use", "access", "agent"]
        rs_hits = sum(1 for k in records_specific if k in meta_lower)
        score += (rs_hits / len(records_specific)) * 0.2
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in self._mandatory_fields:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory element missing: {mf} (ISO 23081-1:2017 §7.2)")

        recommended = ["aggregation", "rights", "access", "language", "disposition"]
        for rf in recommended:
            if rf not in meta_lower:
                warnings.append(f"Recommended element absent: {rf}")

        found = sum(1 for f in self._mandatory_fields if f.lower() in meta_lower)
        score = found / len(self._mandatory_fields)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
