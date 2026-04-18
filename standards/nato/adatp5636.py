"""
ADatP-5636 (NATO Core Metadata Specification, NCMS) — Ed. A V1
NATO Standardization Agreement for information resource metadata.

Reference: ADatP-5636 Ed. A V1
XML Namespace: urn:nato:stanag:5636:A:1:elements
"""
from typing import Any, Dict, List
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NAMESPACE = "urn:nato:stanag:5636:A:1:elements"

# ---------------------------------------------------------------------------
# Field catalogue
# ---------------------------------------------------------------------------
FIELDS: Dict[str, FieldDefinition] = {

    # ── Security layer ──────────────────────────────────────────────────────
    "metadataConfidentialityLabel": FieldDefinition(
        name="metadataConfidentialityLabel",
        description=(
            "The confidentiality label applied to the metadata record itself, "
            "expressed as a structured ADatP-4774 label. Governs access to the "
            "metadata rather than the information resource it describes."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CONFIDENTIALITY_LABEL,
        values="ADatP-4774 ConfidentialityInformation structure",
        reference="ADatP-5636 Ed.A V1 §3.2.1",
        comments=(
            "Must be an ADatP-4774 compliant label. "
            "The label applies to the metadata record, not the resource."
        ),
        layer="Security",
        group="",
        xml_element="metadataConfidentialityLabel",
        namespace=NAMESPACE,
    ),
    "originatorConfidentialityLabel": FieldDefinition(
        name="originatorConfidentialityLabel",
        description=(
            "The confidentiality label assigned by the originator to the "
            "information resource being described. This is the classification "
            "marking of the actual resource content."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CONFIDENTIALITY_LABEL,
        values="ADatP-4774 ConfidentialityInformation structure",
        reference="ADatP-5636 Ed.A V1 §3.2.2",
        comments=(
            "Must comply with ADatP-4774. "
            "Highest classification of the resource."
        ),
        layer="Security",
        group="",
        xml_element="originatorConfidentialityLabel",
        namespace=NAMESPACE,
    ),
    "alternativeConfidentialityLabel": FieldDefinition(
        name="alternativeConfidentialityLabel",
        description=(
            "An alternative confidentiality label for the information resource, "
            "typically used when the resource will be shared in a different "
            "security domain or releasability context."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CONFIDENTIALITY_LABEL,
        values="ADatP-4774 ConfidentialityInformation structure",
        reference="ADatP-5636 Ed.A V1 §3.2.3",
        comments="May appear multiple times for different releasability scenarios.",
        layer="Security",
        group="Security",
        xml_element="alternativeConfidentialityLabel",
        namespace=NAMESPACE,
    ),

    # ── Common layer — ungrouped mandatory ─────────────────────────────────
    "creator": FieldDefinition(
        name="creator",
        description=(
            "The entity primarily responsible for making the information resource. "
            "For NATO resources this is typically a NATO body, command, agency or "
            "a member nation organisation. Corresponds to DCTERMS:creator."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="PointOfContact with type, name, affiliation, email, phone",
        reference="ADatP-5636 Ed.A V1 §4.2.1",
        not_to_be_confused_with=(
            "contributor — contributor had a lesser or supportive role; "
            "publisher — publisher makes the resource available."
        ),
        layer="Common",
        group="",
        xml_element="creator",
        namespace=NAMESPACE,
    ),
    "publisher": FieldDefinition(
        name="publisher",
        description=(
            "The entity responsible for making the information resource available. "
            "For many NATO documents this will be the same NATO body as the creator, "
            "but may differ when a resource is published by a different authority."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="PointOfContact with type, name, affiliation, email, phone",
        reference="ADatP-5636 Ed.A V1 §4.2.2",
        not_to_be_confused_with="creator — creator authored the content; publisher distributes it.",
        layer="Common",
        group="",
        xml_element="publisher",
        namespace=NAMESPACE,
    ),
    "dateCreated": FieldDefinition(
        name="dateCreated",
        description=(
            "The date (and optionally time) on which the information resource "
            "was originally created. This is distinct from dateIssued (publication "
            "date) and dateModified (last-updated date)."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime, e.g., 2024-03-15 or 2024-03-15T09:30:00Z",
        reference="ADatP-5636 Ed.A V1 §4.2.3",
        not_to_be_confused_with="dateIssued — date of official publication/issue.",
        layer="Common",
        group="",
        xml_element="dateCreated",
        namespace=NAMESPACE,
    ),
    "identifier": FieldDefinition(
        name="identifier",
        description=(
            "An unambiguous reference to the information resource within a given "
            "context. Recommended best practice is to use a URI. For NATO resources "
            "this is typically a URN following the NATO URI scheme."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI (recommended: NATO URN scheme urn:nato:...)",
        reference="ADatP-5636 Ed.A V1 §4.2.4",
        not_to_be_confused_with="externalIdentifier — identifier in an external system.",
        layer="Common",
        group="",
        xml_element="identifier",
        namespace=NAMESPACE,
    ),
    "title": FieldDefinition(
        name="title",
        description=(
            "The official name given to the information resource. The title should "
            "be concise yet sufficiently descriptive to identify the resource "
            "unambiguously within the NATO information environment."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text; natural language string",
        reference="ADatP-5636 Ed.A V1 §4.2.5",
        not_to_be_confused_with="alternativeTitle — secondary/abbreviated title.",
        layer="Common",
        group="",
        xml_element="title",
        namespace=NAMESPACE,
    ),

    # ── Common layer — ungrouped optional ──────────────────────────────────
    "contributor": FieldDefinition(
        name="contributor",
        description=(
            "An entity that made a contribution to the information resource but "
            "whose role was secondary to the creator. Includes editors, translators, "
            "illustrators, or technical reviewers."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="PointOfContact with type, name, affiliation, email",
        reference="ADatP-5636 Ed.A V1 §4.3.1",
        not_to_be_confused_with="creator — creator has primary intellectual responsibility.",
        layer="Common",
        group="",
        xml_element="contributor",
        namespace=NAMESPACE,
    ),
    "custodian": FieldDefinition(
        name="custodian",
        description=(
            "The entity responsible for managing and maintaining the information "
            "resource on behalf of the owner. The custodian ensures availability "
            "and integrity but may not own the resource."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="PointOfContact with type, name, affiliation, email",
        reference="ADatP-5636 Ed.A V1 §4.3.2",
        layer="Common",
        group="",
        xml_element="custodian",
        namespace=NAMESPACE,
    ),
    "language": FieldDefinition(
        name="language",
        description=(
            "The natural language or languages used in the information resource. "
            "The two NATO official languages are English (eng) and French (fra). "
            "Use IETF BCP 47 / ISO 639-3 codes."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-3 alpha-3 language code, e.g., eng, fra, deu",
        reference="ADatP-5636 Ed.A V1 §4.3.3",
        layer="Common",
        group="",
        xml_element="language",
        namespace=NAMESPACE,
    ),
    "contextActivity": FieldDefinition(
        name="contextActivity",
        description=(
            "The NATO operational, exercise, programme or project context within "
            "which the information resource was created or is relevant. "
            "Provides mission/operation context."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or structured reference to NATO activity/operation",
        reference="ADatP-5636 Ed.A V1 §4.3.4",
        layer="Common",
        group="",
        xml_element="contextActivity",
        namespace=NAMESPACE,
    ),
    "provenance": FieldDefinition(
        name="provenance",
        description=(
            "A statement of any changes in ownership and custody of the information "
            "resource since its creation that are significant for its authenticity, "
            "integrity and interpretation."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text description of provenance chain",
        reference="ADatP-5636 Ed.A V1 §4.3.5",
        layer="Common",
        group="",
        xml_element="provenance",
        namespace=NAMESPACE,
    ),
    "source": FieldDefinition(
        name="source",
        description=(
            "A related resource from which the described resource is derived. "
            "The described resource may be derived from the related resource in "
            "whole or in part."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="URI or text description of source resource",
        reference="ADatP-5636 Ed.A V1 §4.3.6",
        not_to_be_confused_with="relation — generic relationship; source implies derivation.",
        layer="Common",
        group="",
        xml_element="source",
        namespace=NAMESPACE,
    ),
    "type": FieldDefinition(
        name="type",
        description=(
            "The nature or genre of the information resource. Recommended values "
            "are drawn from the DCMI Type Vocabulary or a NATO-specific controlled "
            "vocabulary (e.g., Report, Order, Directive, Plan, Record)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="DCMI Type Vocabulary or NATO resource type code list",
        reference="ADatP-5636 Ed.A V1 §4.3.7",
        layer="Common",
        group="",
        xml_element="type",
        namespace=NAMESPACE,
    ),

    # ── Coverage group ──────────────────────────────────────────────────────
    "countryCode": FieldDefinition(
        name="countryCode",
        description=(
            "An ISO 3166-1 alpha-2 country code identifying the country or "
            "countries associated with or covered by the information resource."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="ISO 3166-1 alpha-2, e.g., GB, FR, DE, US",
        reference="ADatP-5636 Ed.A V1 §4.4.1",
        layer="Common",
        group="Coverage",
        xml_element="countryCode",
        namespace=NAMESPACE,
    ),
    "geographicReference": FieldDefinition(
        name="geographicReference",
        description=(
            "A spatial region or named place covered by the information resource. "
            "The encoding scheme must be specified using geographicEncodingScheme "
            "whenever this element is used."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.GEO_REFERENCE,
        values="Geographic coordinate, bounding box, or named place identifier",
        reference="ADatP-5636 Ed.A V1 §4.4.2",
        layer="Common",
        group="Coverage",
        xml_element="geographicReference",
        namespace=NAMESPACE,
    ),
    "geographicEncodingScheme": FieldDefinition(
        name="geographicEncodingScheme",
        description=(
            "The encoding scheme used for geographic references in the "
            "geographicReference element. Required whenever geographicReference "
            "is present."
        ),
        obligation=Obligation.CONDITIONAL,
        condition="Required if geographicReference is used (ADatP-5636 §4.4.3)",
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="MGRS, UTM, WGS84-DD, WGS84-DMS, GeoJSON, WKT, GeoNames",
        reference="ADatP-5636 Ed.A V1 §4.4.3",
        layer="Common",
        group="Coverage",
        xml_element="geographicEncodingScheme",
        namespace=NAMESPACE,
    ),
    "placeName": FieldDefinition(
        name="placeName",
        description=(
            "The name of a place associated with or covered by the information "
            "resource. Use standardised NATO place names where available (STANAG 2211)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.NAME,
        values="Standardised place name string",
        reference="ADatP-5636 Ed.A V1 §4.4.4",
        layer="Common",
        group="Coverage",
        xml_element="placeName",
        namespace=NAMESPACE,
    ),
    "region": FieldDefinition(
        name="region",
        description=(
            "A named administrative or geographic region associated with the "
            "information resource. May be a NATO AOR (Area of Responsibility) "
            "designation or a standard regional code."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Region name or code, e.g., NATO AOR designator",
        reference="ADatP-5636 Ed.A V1 §4.4.5",
        layer="Common",
        group="Coverage",
        xml_element="region",
        namespace=NAMESPACE,
    ),
    "timePeriod": FieldDefinition(
        name="timePeriod",
        description=(
            "The temporal period that the information resource covers. "
            "Expressed using DCMI Period notation: start/end dates or named period."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="DCMI Period: 'start=YYYY-MM-DD; end=YYYY-MM-DD; name=...'",
        reference="ADatP-5636 Ed.A V1 §4.4.6",
        layer="Common",
        group="Coverage",
        xml_element="timePeriod",
        namespace=NAMESPACE,
    ),

    # ── Date group ──────────────────────────────────────────────────────────
    "dateAccepted": FieldDefinition(
        name="dateAccepted",
        description="Date of formal acceptance of the information resource (e.g., by a review board).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.1",
        layer="Common",
        group="Date",
        xml_element="dateAccepted",
        namespace=NAMESPACE,
    ),
    "dateAcquired": FieldDefinition(
        name="dateAcquired",
        description="Date the information resource was acquired by or transferred to the current holding entity.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.2",
        layer="Common",
        group="Date",
        xml_element="dateAcquired",
        namespace=NAMESPACE,
    ),
    "dateAvailable": FieldDefinition(
        name="dateAvailable",
        description="Date the information resource becomes or became available for access or distribution.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.3",
        layer="Common",
        group="Date",
        xml_element="dateAvailable",
        namespace=NAMESPACE,
    ),
    "dateClosed": FieldDefinition(
        name="dateClosed",
        description="Date the information resource was closed, archived, or its active maintenance ceased.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.4",
        layer="Common",
        group="Date",
        xml_element="dateClosed",
        namespace=NAMESPACE,
    ),
    "dateCopyrighted": FieldDefinition(
        name="dateCopyrighted",
        description="Year of copyright assertion. Required if the copyright element is populated.",
        obligation=Obligation.CONDITIONAL,
        condition="Required if copyright element is used (ADatP-5636 §4.5.5)",
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 year or date, e.g., 2024",
        reference="ADatP-5636 Ed.A V1 §4.5.5",
        layer="Common",
        group="Date",
        xml_element="dateCopyrighted",
        namespace=NAMESPACE,
    ),
    "dateCutOff": FieldDefinition(
        name="dateCutOff",
        description="The cut-off date for information included in the resource (e.g., intelligence reporting up to a specific date).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.6",
        layer="Common",
        group="Date",
        xml_element="dateCutOff",
        namespace=NAMESPACE,
    ),
    "dateDeclared": FieldDefinition(
        name="dateDeclared",
        description="Date the information resource was officially declared (e.g., declared as a record in a records management system).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.7",
        layer="Common",
        group="Date",
        xml_element="dateDeclared",
        namespace=NAMESPACE,
    ),
    "dateDisposition": FieldDefinition(
        name="dateDisposition",
        description="The date on which the records disposition action (destruction, transfer, permanent retention) is scheduled or was performed.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.8",
        layer="Common",
        group="Date",
        xml_element="dateDisposition",
        namespace=NAMESPACE,
    ),
    "dateIssued": FieldDefinition(
        name="dateIssued",
        description="Date of formal issuance or publication of the information resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.9",
        not_to_be_confused_with="dateCreated — creation precedes issuance.",
        layer="Common",
        group="Date",
        xml_element="dateIssued",
        namespace=NAMESPACE,
    ),
    "dateModified": FieldDefinition(
        name="dateModified",
        description="Date on which the information resource was most recently changed or updated.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime",
        reference="ADatP-5636 Ed.A V1 §4.5.10",
        layer="Common",
        group="Date",
        xml_element="dateModified",
        namespace=NAMESPACE,
    ),
    "dateNextVersionDue": FieldDefinition(
        name="dateNextVersionDue",
        description="Planned date for the next version or update of the information resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.11",
        layer="Common",
        group="Date",
        xml_element="dateNextVersionDue",
        namespace=NAMESPACE,
    ),
    "dateSubmitted": FieldDefinition(
        name="dateSubmitted",
        description="Date the information resource was submitted for review, approval or archival.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="ADatP-5636 Ed.A V1 §4.5.12",
        layer="Common",
        group="Date",
        xml_element="dateSubmitted",
        namespace=NAMESPACE,
    ),
    "dateValid": FieldDefinition(
        name="dateValid",
        description="Date (range) during which the information resource is or was valid.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or DCMI Period",
        reference="ADatP-5636 Ed.A V1 §4.5.13",
        layer="Common",
        group="Date",
        xml_element="dateValid",
        namespace=NAMESPACE,
    ),

    # ── Description group ───────────────────────────────────────────────────
    "abstract": FieldDefinition(
        name="abstract",
        description=(
            "A summary of the information resource content. "
            "Should be sufficient for a reader to assess relevance without "
            "accessing the full resource. NATO abstracts are typically 100–500 words."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ADatP-5636 Ed.A V1 §4.6.1",
        not_to_be_confused_with="description — description may be shorter/broader.",
        layer="Common",
        group="Description",
        xml_element="abstract",
        namespace=NAMESPACE,
    ),
    "description": FieldDefinition(
        name="description",
        description=(
            "An account of the information resource. May include an abstract, "
            "table of contents, graphical representation, or free-text account "
            "of the resource content."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ADatP-5636 Ed.A V1 §4.6.2",
        layer="Common",
        group="Description",
        xml_element="description",
        namespace=NAMESPACE,
    ),
    "tableOfContents": FieldDefinition(
        name="tableOfContents",
        description="A list of sections or parts with their page locations as they appear in the information resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or structured TOC",
        reference="ADatP-5636 Ed.A V1 §4.6.3",
        layer="Common",
        group="Description",
        xml_element="tableOfContents",
        namespace=NAMESPACE,
    ),

    # ── Format group ────────────────────────────────────────────────────────
    "extent": FieldDefinition(
        name="extent",
        description=(
            "The size or duration of the information resource. "
            "For documents: page count; for files: byte size; for audio/video: duration."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.QUANTITY,
        values="Numeric value with unit, e.g., '42 pages', '2.5 MB', '00:45:00'",
        reference="ADatP-5636 Ed.A V1 §4.7.1",
        layer="Common",
        group="Format",
        xml_element="extent",
        namespace=NAMESPACE,
    ),
    "extentQualifier": FieldDefinition(
        name="extentQualifier",
        description="Qualifier specifying the unit or type of extent measurement. Required if extent is present.",
        obligation=Obligation.CONDITIONAL,
        condition="Required if extent element is used (ADatP-5636 §4.7.2)",
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="pages, bytes, kilobytes, megabytes, gigabytes, seconds, minutes, hours",
        reference="ADatP-5636 Ed.A V1 §4.7.2",
        layer="Common",
        group="Format",
        xml_element="extentQualifier",
        namespace=NAMESPACE,
    ),
    "mediaFormat": FieldDefinition(
        name="mediaFormat",
        description=(
            "The file format, physical medium, or dimensions of the resource. "
            "Use IANA Media Types (MIME types) for digital resources."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="IANA MIME type, e.g., application/pdf, text/xml, image/jpeg",
        reference="ADatP-5636 Ed.A V1 §4.7.3",
        layer="Common",
        group="Format",
        xml_element="mediaFormat",
        namespace=NAMESPACE,
    ),
    "medium": FieldDefinition(
        name="medium",
        description="The material or physical carrier of the resource (e.g., CD-ROM, USB, paper).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or controlled vocabulary term",
        reference="ADatP-5636 Ed.A V1 §4.7.4",
        layer="Common",
        group="Format",
        xml_element="medium",
        namespace=NAMESPACE,
    ),

    # ── Identifier group ────────────────────────────────────────────────────
    "externalIdentifier": FieldDefinition(
        name="externalIdentifier",
        description=(
            "An identifier for the resource in an external system (e.g., "
            "ISADG reference code, national library catalogue number, "
            "commercial ISBN/ISSN)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or string with scheme prefix, e.g., ISBN:978-..., ISSN:...",
        reference="ADatP-5636 Ed.A V1 §4.8.2",
        not_to_be_confused_with="identifier — identifier is the primary NATO identifier.",
        layer="Common",
        group="Identifier",
        xml_element="externalIdentifier",
        namespace=NAMESPACE,
    ),

    # ── Relation group ──────────────────────────────────────────────────────
    "authorizes": FieldDefinition(
        name="authorizes",
        description="This resource authorizes or gives authority to another resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or identifier of the authorized resource",
        reference="ADatP-5636 Ed.A V1 §4.9.1",
        layer="Common",
        group="Relation",
        xml_element="authorizes",
        namespace=NAMESPACE,
    ),
    "conformsTo": FieldDefinition(
        name="conformsTo",
        description="An established standard to which the information resource conforms.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the standard or policy document",
        reference="ADatP-5636 Ed.A V1 §4.9.2",
        layer="Common",
        group="Relation",
        xml_element="conformsTo",
        namespace=NAMESPACE,
    ),
    "hasFormat": FieldDefinition(
        name="hasFormat",
        description="A related resource that is substantially the same as this resource, but in another format.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the related resource",
        reference="ADatP-5636 Ed.A V1 §4.9.3",
        layer="Common",
        group="Relation",
        xml_element="hasFormat",
        namespace=NAMESPACE,
    ),
    "hasPart": FieldDefinition(
        name="hasPart",
        description="A related resource that is included either physically or logically in this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the part resource",
        reference="ADatP-5636 Ed.A V1 §4.9.4",
        layer="Common",
        group="Relation",
        xml_element="hasPart",
        namespace=NAMESPACE,
    ),
    "hasRedaction": FieldDefinition(
        name="hasRedaction",
        description="A related resource that is a redacted version of this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the redacted resource",
        reference="ADatP-5636 Ed.A V1 §4.9.5",
        layer="Common",
        group="Relation",
        xml_element="hasRedaction",
        namespace=NAMESPACE,
    ),
    "hasVersion": FieldDefinition(
        name="hasVersion",
        description="A related resource that is a version, edition, or adaptation of this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the version resource",
        reference="ADatP-5636 Ed.A V1 §4.9.6",
        layer="Common",
        group="Relation",
        xml_element="hasVersion",
        namespace=NAMESPACE,
    ),
    "isAuthorizedBy": FieldDefinition(
        name="isAuthorizedBy",
        description="A related resource that authorises this resource (inverse of authorizes).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the authorizing resource",
        reference="ADatP-5636 Ed.A V1 §4.9.7",
        layer="Common",
        group="Relation",
        xml_element="isAuthorizedBy",
        namespace=NAMESPACE,
    ),
    "isDefinedBy": FieldDefinition(
        name="isDefinedBy",
        description="A resource that defines concepts, terms or standards used by this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the defining resource",
        reference="ADatP-5636 Ed.A V1 §4.9.8",
        layer="Common",
        group="Relation",
        xml_element="isDefinedBy",
        namespace=NAMESPACE,
    ),
    "isFormatOf": FieldDefinition(
        name="isFormatOf",
        description="A related resource that is substantially the same as this resource, but in a different format.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the source format resource",
        reference="ADatP-5636 Ed.A V1 §4.9.9",
        layer="Common",
        group="Relation",
        xml_element="isFormatOf",
        namespace=NAMESPACE,
    ),
    "isPartOf": FieldDefinition(
        name="isPartOf",
        description="A related resource in which this resource is physically or logically included.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the parent resource",
        reference="ADatP-5636 Ed.A V1 §4.9.10",
        layer="Common",
        group="Relation",
        xml_element="isPartOf",
        namespace=NAMESPACE,
    ),
    "isReferencedBy": FieldDefinition(
        name="isReferencedBy",
        description="A related resource that references, cites or points to this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the referencing resource",
        reference="ADatP-5636 Ed.A V1 §4.9.11",
        layer="Common",
        group="Relation",
        xml_element="isReferencedBy",
        namespace=NAMESPACE,
    ),
    "isRequiredBy": FieldDefinition(
        name="isRequiredBy",
        description="A related resource that requires this resource for its function or use.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the requiring resource",
        reference="ADatP-5636 Ed.A V1 §4.9.12",
        layer="Common",
        group="Relation",
        xml_element="isRequiredBy",
        namespace=NAMESPACE,
    ),
    "isReplacedBy": FieldDefinition(
        name="isReplacedBy",
        description="A related resource that supplants, displaces or supersedes this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the replacing resource",
        reference="ADatP-5636 Ed.A V1 §4.9.13",
        layer="Common",
        group="Relation",
        xml_element="isReplacedBy",
        namespace=NAMESPACE,
    ),
    "isVersionOf": FieldDefinition(
        name="isVersionOf",
        description="A related resource of which this resource is a version, edition, or adaptation.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the parent version resource",
        reference="ADatP-5636 Ed.A V1 §4.9.14",
        layer="Common",
        group="Relation",
        xml_element="isVersionOf",
        namespace=NAMESPACE,
    ),
    "isRedactionOf": FieldDefinition(
        name="isRedactionOf",
        description="Identifies the source resource of which this is a redacted version.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the original full resource",
        reference="ADatP-5636 Ed.A V1 §4.9.15",
        layer="Common",
        group="Relation",
        xml_element="isRedactionOf",
        namespace=NAMESPACE,
    ),
    "providesDefinitionOf": FieldDefinition(
        name="providesDefinitionOf",
        description="A resource for which this resource provides a definition (inverse of isDefinedBy).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the defined resource",
        reference="ADatP-5636 Ed.A V1 §4.9.16",
        layer="Common",
        group="Relation",
        xml_element="providesDefinitionOf",
        namespace=NAMESPACE,
    ),
    "reasonForRedaction": FieldDefinition(
        name="reasonForRedaction",
        description="Explanation of why content has been redacted from this resource. Required if isRedactionOf is used.",
        obligation=Obligation.CONDITIONAL,
        condition="Required if isRedactionOf (or isRedaction) is used (ADatP-5636 §4.9.17)",
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text justification referencing security/legal basis",
        reference="ADatP-5636 Ed.A V1 §4.9.17",
        layer="Common",
        group="Relation",
        xml_element="reasonForRedaction",
        namespace=NAMESPACE,
    ),
    "references": FieldDefinition(
        name="references",
        description="A related resource that is referenced, cited or pointed to by this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the referenced resource",
        reference="ADatP-5636 Ed.A V1 §4.9.18",
        layer="Common",
        group="Relation",
        xml_element="references",
        namespace=NAMESPACE,
    ),
    "replaces": FieldDefinition(
        name="replaces",
        description="A related resource that is supplanted, displaced or superseded by this resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the superseded resource",
        reference="ADatP-5636 Ed.A V1 §4.9.19",
        layer="Common",
        group="Relation",
        xml_element="replaces",
        namespace=NAMESPACE,
    ),
    "requires": FieldDefinition(
        name="requires",
        description="A related resource that is required by this resource to function or be understood.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the required resource",
        reference="ADatP-5636 Ed.A V1 §4.9.20",
        layer="Common",
        group="Relation",
        xml_element="requires",
        namespace=NAMESPACE,
    ),
    "relation": FieldDefinition(
        name="relation",
        description="A related resource. Use a more specific sub-property when possible.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI of the related resource",
        reference="ADatP-5636 Ed.A V1 §4.9",
        layer="Common",
        group="Relation",
        xml_element="relation",
        namespace=NAMESPACE,
    ),

    # ── Rights group ────────────────────────────────────────────────────────
    "accessRights": FieldDefinition(
        name="accessRights",
        description=(
            "Information about who can access the resource or an indication of "
            "its security status. This complements the confidentiality label and "
            "may reference access control policies or distribution lists."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or URI to access rights policy",
        reference="ADatP-5636 Ed.A V1 §4.10.1",
        layer="Common",
        group="Rights",
        xml_element="accessRights",
        namespace=NAMESPACE,
    ),
    "copyright": FieldDefinition(
        name="copyright",
        description="A copyright statement. When present, dateCopyrighted must also be provided.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Copyright statement string, e.g., '© 2024 NATO/OTAN'",
        reference="ADatP-5636 Ed.A V1 §4.10.2",
        layer="Common",
        group="Rights",
        xml_element="copyright",
        namespace=NAMESPACE,
    ),
    "license": FieldDefinition(
        name="license",
        description="A legal document giving official permission to use the resource under defined conditions.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the license document, e.g., Creative Commons URI or NATO ISAF licence URI",
        reference="ADatP-5636 Ed.A V1 §4.10.3",
        layer="Common",
        group="Rights",
        xml_element="license",
        namespace=NAMESPACE,
    ),
    "rights": FieldDefinition(
        name="rights",
        description="Information about rights held in and over the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text rights statement",
        reference="ADatP-5636 Ed.A V1 §4.10.4",
        layer="Common",
        group="Rights",
        xml_element="rights",
        namespace=NAMESPACE,
    ),
    "rightsHolder": FieldDefinition(
        name="rightsHolder",
        description="A person or organisation owning or managing rights over the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="PointOfContact or URI to agent description",
        reference="ADatP-5636 Ed.A V1 §4.10.5",
        layer="Common",
        group="Rights",
        xml_element="rightsHolder",
        namespace=NAMESPACE,
    ),

    # ── Subject group ───────────────────────────────────────────────────────
    "keyword": FieldDefinition(
        name="keyword",
        description=(
            "A word or phrase describing the content of the resource. "
            "Keywords may be free text or drawn from a controlled vocabulary. "
            "STANAG 6001 NATO subject codes should be used where applicable."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or controlled vocabulary term",
        reference="ADatP-5636 Ed.A V1 §4.11.1",
        layer="Common",
        group="Subject",
        xml_element="keyword",
        namespace=NAMESPACE,
    ),
    "subject": FieldDefinition(
        name="subject",
        description=(
            "The topic of the resource. Subject is broader and more formal than keyword. "
            "Use a subject classification scheme (e.g., DDC, UDC, NATO subject categories)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Subject term or classification code",
        reference="ADatP-5636 Ed.A V1 §4.11.2",
        not_to_be_confused_with="keyword — keyword is informal; subject uses a classification scheme.",
        layer="Common",
        group="Subject",
        xml_element="subject",
        namespace=NAMESPACE,
    ),
    "subjectCategory": FieldDefinition(
        name="subjectCategory",
        description="A formal category from a controlled subject classification scheme applied to the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="Code from NATO subject category list or DDC/UDC",
        reference="ADatP-5636 Ed.A V1 §4.11.3",
        layer="Common",
        group="Subject",
        xml_element="subjectCategory",
        namespace=NAMESPACE,
    ),

    # ── Title group ─────────────────────────────────────────────────────────
    "alternativeTitle": FieldDefinition(
        name="alternativeTitle",
        description=(
            "An alternative name for the resource (e.g., acronym, short title, "
            "translated title, or former title)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ADatP-5636 Ed.A V1 §4.12.1",
        layer="Common",
        group="Title",
        xml_element="alternativeTitle",
        namespace=NAMESPACE,
    ),
    "subtitle": FieldDefinition(
        name="subtitle",
        description="A subordinate part of the title that provides additional descriptive information.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ADatP-5636 Ed.A V1 §4.12.2",
        layer="Common",
        group="Title",
        xml_element="subtitle",
        namespace=NAMESPACE,
    ),

    # ── ILS (Information Lifecycle Support) layer ───────────────────────────
    "recordsDisposition": FieldDefinition(
        name="recordsDisposition",
        description=(
            "The records disposition instruction or authority applicable to "
            "the information resource. Specifies what will happen to the record "
            "at the end of its retention period (transfer, destruction, permanent retention)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Disposition authority reference or instructions",
        reference="ADatP-5636 Ed.A V1 §5.2.1",
        layer="ILS",
        group="",
        xml_element="recordsDisposition",
        namespace=NAMESPACE,
    ),
    "recordsHold": FieldDefinition(
        name="recordsHold",
        description=(
            "Indicates that a records hold (litigation hold / legal hold) is in "
            "place for this resource, suspending normal disposition schedules."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.INDICATOR,
        values="true | false",
        reference="ADatP-5636 Ed.A V1 §5.2.2",
        layer="ILS",
        group="",
        xml_element="recordsHold",
        namespace=NAMESPACE,
    ),
    "updatingFrequency": FieldDefinition(
        name="updatingFrequency",
        description="The established frequency at which the resource is updated or reviewed.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="ISO 8601 duration or descriptive term: daily, weekly, monthly, annually, as-needed",
        reference="ADatP-5636 Ed.A V1 §5.2.3",
        layer="ILS",
        group="",
        xml_element="updatingFrequency",
        namespace=NAMESPACE,
    ),
    "version": FieldDefinition(
        name="version",
        description=(
            "The version identifier of the information resource. "
            "For NATO documents typically uses the EDITION/VERSION scheme."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Version string, e.g., '1.0', 'Ed.A V1', 'Draft v3'",
        reference="ADatP-5636 Ed.A V1 §5.2.4",
        layer="ILS",
        group="",
        xml_element="version",
        namespace=NAMESPACE,
    ),
    "status": FieldDefinition(
        name="status",
        description="The current lifecycle status of the information resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="Draft | Proposed | Active | Superseded | Withdrawn | Archived",
        reference="ADatP-5636 Ed.A V1 §5.2.5",
        layer="ILS",
        group="",
        xml_element="status",
        namespace=NAMESPACE,
    ),
}


class ADatP5636Standard(MetadataStandard):
    """ADatP-5636 Ed.A V1 — NATO Core Metadata Specification (NCMS)."""

    id = "adatp5636"
    name = "ADatP-5636"
    full_name = "NATO Core Metadata Specification (NCMS)"
    version = "Ed. A V1"
    organization = "NATO"
    domain = "NATO"
    description = (
        "ADatP-5636 defines the core metadata elements required to describe "
        "information resources within the NATO information environment. It is "
        "structured in three layers: Security, Common, and Information Lifecycle "
        "Support (ILS). The Security layer ensures that every metadata record "
        "carries a confidentiality label for both the record itself and the resource "
        "it describes. The Common layer provides discovery and management metadata. "
        "The ILS layer supports records management obligations."
    )
    reference = "ADatP-5636 Ed. A V1"
    namespace = NAMESPACE
    fields = FIELDS

    # namespace markers used for detection
    _ns_markers = [NAMESPACE, "stanag:5636", "nato:stanag", "ncms"]
    _key_fields = [
        "metadataConfidentialityLabel", "originatorConfidentialityLabel",
        "contextActivity", "recordsDisposition", "recordsHold",
        "updatingFrequency", "externalIdentifier", "subjectCategory",
        "geographicEncodingScheme", "dateDisposition", "dateCutOff",
        "dateNextVersionDue", "dateDeclared",
    ]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        # namespace check
        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.4
                break

        # mandatory fields
        mandatory = ["metadataconfidentialitylabel", "originatorconfidentialitylabel",
                     "creator", "publisher", "datecreated", "identifier", "title"]
        hits = sum(1 for f in mandatory if f in meta_lower)
        score += (hits / len(mandatory)) * 0.4

        # NATO-specific optional field presence
        nato_hits = sum(1 for f in self._key_fields if f.lower() in meta_lower)
        score += (nato_hits / len(self._key_fields)) * 0.2

        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        # Mandatory checks
        mandatory_fields = [
            "metadataConfidentialityLabel", "originatorConfidentialityLabel",
            "creator", "publisher", "dateCreated", "identifier", "title",
        ]
        for mf in mandatory_fields:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory field missing: {mf} (ADatP-5636 §{_field_ref(mf)})")

        # Conditional checks
        if "geographicreference" in meta_lower and "geographicencodingscheme" not in meta_lower:
            errors.append(
                "Conditional field missing: geographicEncodingScheme is required "
                "when geographicReference is present (ADatP-5636 §4.4.3)"
            )
        if "copyright" in meta_lower and "datecopyrighted" not in meta_lower:
            errors.append(
                "Conditional field missing: dateCopyrighted is required "
                "when copyright is present (ADatP-5636 §4.5.5)"
            )
        if "extent" in meta_lower and "extentqualifier" not in meta_lower:
            errors.append(
                "Conditional field missing: extentQualifier is required "
                "when extent is present (ADatP-5636 §4.7.2)"
            )
        if ("isredactionof" in meta_lower or "isredaction" in meta_lower) \
                and "reasonforredaction" not in meta_lower:
            errors.append(
                "Conditional field missing: reasonForRedaction is required "
                "when isRedactionOf is present (ADatP-5636 §4.9.17)"
            )

        # Warnings for recommended fields
        recommended = ["language", "description", "keyword", "type", "dateIssued"]
        for rf in recommended:
            if rf.lower() not in meta_lower:
                warnings.append(f"Recommended field absent: {rf}")

        total = len(mandatory_fields)
        found = sum(1 for mf in mandatory_fields if mf.lower() in meta_lower)
        score = found / total if total > 0 else 0.0

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "score": score,
        }

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)


def _field_ref(field_name: str) -> str:
    """Return the section reference for a given field name."""
    f = FIELDS.get(field_name)
    if f and f.reference:
        parts = f.reference.split("§")
        if len(parts) > 1:
            return parts[1].strip()
    return "4.x"
