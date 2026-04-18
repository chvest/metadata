"""
DCAT-AP-SE 2.2.0 — Swedish national application profile of DCAT-AP.

DCAT-AP-SE is maintained by DIGG (Swedish Agency for Digital Government) and
extends DCAT-AP 2.x with Swedish-specific obligations, controlled vocabularies,
and requirements. It is the mandatory profile for datasets published on the
Swedish national open data portal (dataportal.se).

Key Swedish additions over DCAT-AP 2.1.1:
  - Publisher is mandatory (not just recommended)
  - Catalog license must be CC0 1.0 (Public Domain)
  - Spatial coverage should use Geonames URIs (preferred Swedish authority)
  - HVD Category (dcat:hvdCategory) for EU High-value dataset regulation
  - Applicable Legislation (dcat:applicableLegislation) added
  - Language URIs from EU Publications Office NAL (same as DCAT-AP)

Reference: DCAT-AP-SE 2.2.0 (https://docs.dataportal.se/dcat/2.2.0/en/)
           GitHub: https://github.com/diggsweden/DCAT-AP-SE
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_DCAT = "http://www.w3.org/ns/dcat#"
NS_DCT  = "http://purl.org/dc/terms/"
NS_FOAF = "http://xmlns.com/foaf/0.1/"
NS_ADMS = "http://www.w3.org/ns/adms#"
NS_PROV = "http://www.w3.org/ns/prov#"


FIELDS: Dict[str, FieldDefinition] = {

    # ── dcat:Dataset — Mandatory ─────────────────────────────────────────────

    "dct:title": FieldDefinition(
        name="dct:title",
        description=(
            "A name given to the dataset. Mandatory, repeatable for multiple languages "
            "(use xml:lang tags). Should be concise and distinguishable from other "
            "datasets in the catalogue."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged literal (e.g., 'My dataset'@sv, 'My dataset'@en)",
        reference="DCAT-AP-SE 2.2.0 §Dataset — mandatory",
        layer="Dataset",
        group="",
        xml_element="dct:title",
        namespace=NS_DCT,
    ),
    "dct:description": FieldDefinition(
        name="dct:description",
        description=(
            "A free-text account of the dataset. Mandatory, repeatable for multiple "
            "languages. Should describe content, purpose, and key characteristics "
            "clearly enough for potential consumers to evaluate relevance."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged literal",
        reference="DCAT-AP-SE 2.2.0 §Dataset — mandatory",
        layer="Dataset",
        group="",
        xml_element="dct:description",
        namespace=NS_DCT,
    ),
    "dct:publisher": FieldDefinition(
        name="dct:publisher",
        description=(
            "The entity responsible for making the dataset available. "
            "Mandatory in DCAT-AP-SE (upgraded from recommended in base DCAT-AP). "
            "Should be a URI of a foaf:Agent, preferably from an authority file. "
            "For Swedish public sector: use the organisation number URI."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of foaf:Agent, e.g., https://organization.se/org/2021002520",
        reference="DCAT-AP-SE 2.2.0 §Dataset — mandatory",
        layer="Dataset",
        group="",
        xml_element="dct:publisher",
        namespace=NS_DCT,
    ),

    # ── dcat:Dataset — Recommended ───────────────────────────────────────────

    "dct:accessRights": FieldDefinition(
        name="dct:accessRights",
        description=(
            "Information about access restrictions. Use the EU Access Rights Named "
            "Authority List: PUBLIC, RESTRICTED, or NON_PUBLIC."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values=(
            "URI from EU Access Rights NAL: "
            "http://publications.europa.eu/resource/authority/access-right/PUBLIC | "
            "RESTRICTED | NON_PUBLIC"
        ),
        reference="DCAT-AP-SE 2.2.0 §Dataset — recommended",
        layer="Dataset",
        group="",
        xml_element="dct:accessRights",
        namespace=NS_DCT,
    ),
    "dcat:contactPoint": FieldDefinition(
        name="dcat:contactPoint",
        description=(
            "Contact information for flagging errors or submitting questions about "
            "the dataset. Links to a vCard resource."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="URI of a vcard:Organization or vcard:Individual",
        reference="DCAT-AP-SE 2.2.0 §Dataset — recommended",
        layer="Dataset",
        group="",
        xml_element="dcat:contactPoint",
        namespace=NS_DCAT,
    ),
    "dcat:keyword": FieldDefinition(
        name="dcat:keyword",
        description="A keyword or tag describing the dataset. Repeatable, multilingual.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged free-text keyword string",
        reference="DCAT-AP-SE 2.2.0 §Dataset — recommended",
        layer="Dataset",
        group="",
        xml_element="dcat:keyword",
        namespace=NS_DCAT,
    ),
    "dcat:theme": FieldDefinition(
        name="dcat:theme",
        description=(
            "The main category of the dataset. Use URIs from the EU Data Theme Named "
            "Authority List or INSPIRE themes. Multiple themes allowed."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI from EU Data Theme NAL (http://publications.europa.eu/resource/authority/data-theme/...)",
        reference="DCAT-AP-SE 2.2.0 §Dataset — recommended",
        layer="Dataset",
        group="",
        xml_element="dcat:theme",
        namespace=NS_DCAT,
    ),
    "dct:spatial": FieldDefinition(
        name="dct:spatial",
        description=(
            "The geographic region described by the dataset. "
            "DCAT-AP-SE recommends Geonames URIs for Swedish localities, "
            "or EU Countries/NUTS NAL for broader regions."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI (Geonames, EU Countries NAL, NUTS) e.g., https://sws.geonames.org/2661886/ (Sweden)",
        reference="DCAT-AP-SE 2.2.0 §Dataset — recommended",
        layer="Dataset",
        group="",
        xml_element="dct:spatial",
        namespace=NS_DCT,
    ),

    # ── dcat:Dataset — Optional ──────────────────────────────────────────────

    "dct:creator": FieldDefinition(
        name="dct:creator",
        description=(
            "Entity primarily responsible for producing the dataset. "
            "May differ from publisher. Use a URI of a foaf:Agent."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of foaf:Agent",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:creator",
        namespace=NS_DCT,
    ),
    "dct:identifier": FieldDefinition(
        name="dct:identifier",
        description="A unique, stable identifier for the dataset (preferably a URI).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or persistent identifier string",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:identifier",
        namespace=NS_DCT,
    ),
    "dct:issued": FieldDefinition(
        name="dct:issued",
        description="Date of formal issuance (publication) of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date, datetime, or gYear",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:issued",
        namespace=NS_DCT,
    ),
    "dct:modified": FieldDefinition(
        name="dct:modified",
        description="Most recent date on which the dataset was changed or modified.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:modified",
        namespace=NS_DCT,
    ),
    "dct:language": FieldDefinition(
        name="dct:language",
        description=(
            "Language(s) of the dataset content. "
            "Use URIs from the EU Publications Office language authority list."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI from EU Language NAL, e.g., http://publications.europa.eu/resource/authority/language/SWE",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:language",
        namespace=NS_DCT,
    ),
    "dct:temporal": FieldDefinition(
        name="dct:temporal",
        description="The temporal period that the dataset covers.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="dct:PeriodOfTime with dcat:startDate and dcat:endDate",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:temporal",
        namespace=NS_DCT,
    ),
    "dct:license": FieldDefinition(
        name="dct:license",
        description="The licence under which the dataset is made available.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of the licence (Creative Commons, SPDX, EU Publications Office Licence NAL)",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:license",
        namespace=NS_DCT,
    ),
    "dcat:distribution": FieldDefinition(
        name="dcat:distribution",
        description="An available distribution of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Distribution instance",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dcat:distribution",
        namespace=NS_DCAT,
    ),
    "dct:accrualPeriodicity": FieldDefinition(
        name="dct:accrualPeriodicity",
        description="The frequency at which the dataset is updated.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI from MDR Frequency NAL, e.g., .../frequency/ANNUAL",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:accrualPeriodicity",
        namespace=NS_DCT,
    ),
    "dcat:landingPage": FieldDefinition(
        name="dcat:landingPage",
        description="A web page providing access to the dataset and its metadata.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the landing page",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dcat:landingPage",
        namespace=NS_DCAT,
    ),
    "dct:conformsTo": FieldDefinition(
        name="dct:conformsTo",
        description="An implementing rule or specification that the dataset conforms to.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the standard or specification",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:conformsTo",
        namespace=NS_DCT,
    ),
    "dct:type": FieldDefinition(
        name="dct:type",
        description="The type of the dataset. Use the EU Dataset Type NAL.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI from EU Dataset Type NAL or DCMI Type vocabulary",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:type",
        namespace=NS_DCT,
    ),
    "dct:provenance": FieldDefinition(
        name="dct:provenance",
        description="A statement about the lineage or origins of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or URI",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:provenance",
        namespace=NS_DCT,
    ),
    "dct:source": FieldDefinition(
        name="dct:source",
        description="A related dataset from which the described dataset is derived.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the source dataset",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:source",
        namespace=NS_DCT,
    ),
    "dct:isPartOf": FieldDefinition(
        name="dct:isPartOf",
        description="A related resource in which the described dataset is included.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:isPartOf",
        namespace=NS_DCT,
    ),
    "dct:hasVersion": FieldDefinition(
        name="dct:hasVersion",
        description="A related dataset that is a version of the described dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:hasVersion",
        namespace=NS_DCT,
    ),
    "dct:isVersionOf": FieldDefinition(
        name="dct:isVersionOf",
        description="A related dataset of which this is a version or edition.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:isVersionOf",
        namespace=NS_DCT,
    ),
    "dct:relation": FieldDefinition(
        name="dct:relation",
        description="A related resource with an unspecified relationship.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dct:relation",
        namespace=NS_DCT,
    ),
    "prov:qualifiedAttribution": FieldDefinition(
        name="prov:qualifiedAttribution",
        description="An attribution including agent, role, and other context.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a prov:Attribution instance",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="prov:qualifiedAttribution",
        namespace=NS_PROV,
    ),
    "dcat:qualifiedRelation": FieldDefinition(
        name="dcat:qualifiedRelation",
        description="A description of a typed relationship with another resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Relationship instance",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dcat:qualifiedRelation",
        namespace=NS_DCAT,
    ),
    "dcat:spatialResolutionInMeters": FieldDefinition(
        name="dcat:spatialResolutionInMeters",
        description="The minimum spatial separation resolvable in the dataset, in metres.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.QUANTITY,
        values="xsd:decimal",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dcat:spatialResolutionInMeters",
        namespace=NS_DCAT,
    ),
    "dcat:temporalResolution": FieldDefinition(
        name="dcat:temporalResolution",
        description="The minimum time period resolvable in the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="xsd:duration, e.g., PT1H (1 hour), P1D (1 day)",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="dcat:temporalResolution",
        namespace=NS_DCAT,
    ),
    "adms:identifier": FieldDefinition(
        name="adms:identifier",
        description="A secondary identifier of the dataset (alternative identifier scheme).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="adms:Identifier instance",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="adms:identifier",
        namespace=NS_ADMS,
    ),
    "adms:version": FieldDefinition(
        name="adms:version",
        description="A version number or designation of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Version string literal",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="adms:version",
        namespace=NS_ADMS,
    ),
    "adms:versionNotes": FieldDefinition(
        name="adms:versionNotes",
        description="Release notes or description of changes in this version.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged literal",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional",
        layer="Dataset",
        group="",
        xml_element="adms:versionNotes",
        namespace=NS_ADMS,
    ),

    # ── DCAT-AP-SE specific additions ────────────────────────────────────────

    "dcat:applicableLegislation": FieldDefinition(
        name="dcat:applicableLegislation",
        description=(
            "The legislation that mandates the creation or management of this dataset. "
            "Added in DCAT-AP-SE to support EU High-value dataset (HVD) regulation "
            "(Implementing Regulation (EU) 2023/138) and other legal obligations."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of legislation, e.g., http://data.europa.eu/eli/reg_impl/2023/138/oj",
        reference="DCAT-AP-SE 2.2.0 §Dataset — optional (HVD-specific)",
        layer="Dataset",
        group="",
        xml_element="dcat:applicableLegislation",
        namespace=NS_DCAT,
    ),
    "dcat:hvdCategory": FieldDefinition(
        name="dcat:hvdCategory",
        description=(
            "The High-value dataset category, if this dataset falls under the EU HVD "
            "Implementing Regulation (EU) 2023/138. Categories include: geospatial, "
            "earth observation and environment, meteorological, statistics, "
            "companies and company ownership, mobility."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values=(
            "URI from EU HVD category list, e.g., "
            "http://data.europa.eu/bna/c_164e0bf5 (Geospatial)"
        ),
        reference="DCAT-AP-SE 2.2.0 §Dataset — conditional (required if HVD)",
        layer="Dataset",
        group="",
        xml_element="dcat:hvdCategory",
        namespace=NS_DCAT,
    ),

    # ── dcat:Distribution — Mandatory ────────────────────────────────────────

    "dcat:accessURL": FieldDefinition(
        name="dcat:accessURL",
        description=(
            "A URL giving access to a distribution of the dataset. "
            "The only mandatory property for a Distribution in DCAT-AP-SE."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URL of the access endpoint or download page",
        reference="DCAT-AP-SE 2.2.0 §Distribution — mandatory",
        layer="Distribution",
        group="",
        xml_element="dcat:accessURL",
        namespace=NS_DCAT,
    ),

    # ── dcat:Distribution — Optional ─────────────────────────────────────────

    "dcat:downloadURL": FieldDefinition(
        name="dcat:downloadURL",
        description="A URL of the downloadable file in a given format.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="Direct download URL",
        reference="DCAT-AP-SE 2.2.0 §Distribution — recommended",
        layer="Distribution",
        group="",
        xml_element="dcat:downloadURL",
        namespace=NS_DCAT,
    ),
    "dcat:mediaType": FieldDefinition(
        name="dcat:mediaType",
        description="The media type of the distribution. Use IANA media types.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="IANA MIME type, e.g., application/json, text/csv",
        reference="DCAT-AP-SE 2.2.0 §Distribution — recommended",
        layer="Distribution",
        group="",
        xml_element="dcat:mediaType",
        namespace=NS_DCAT,
    ),
    "dct:format": FieldDefinition(
        name="dct:format",
        description="The file format of the distribution. Use the MDR File Type NAL.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI from MDR File Type NAL",
        reference="DCAT-AP-SE 2.2.0 §Distribution — optional",
        layer="Distribution",
        group="",
        xml_element="dct:format",
        namespace=NS_DCT,
    ),
    "dcatse:availability": FieldDefinition(
        name="dcatse:availability",
        description=(
            "The planned availability of the distribution. "
            "Swedish extension property. Indicates how long the distribution "
            "will remain available: AVAILABLE, EXPERIMENTAL, STABLE, TEMPORARY."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values=(
            "URI from DCAT-AP-SE availability vocabulary: "
            "http://dataportal.se/vocab/availability/AVAILABLE | "
            "EXPERIMENTAL | STABLE | TEMPORARY"
        ),
        reference="DCAT-AP-SE 2.2.0 §Distribution — optional (Swedish extension)",
        layer="Distribution",
        group="",
        xml_element="dcatse:availability",
        namespace="http://dataportal.se/vocab/",
    ),

    # ── dcat:Catalog — Mandatory ─────────────────────────────────────────────

    "cat:dct:title": FieldDefinition(
        name="cat:dct:title",
        description="Name of the catalogue. Mandatory, multilingual.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged literal",
        reference="DCAT-AP-SE 2.2.0 §Catalog — mandatory",
        layer="Catalog",
        group="",
        xml_element="dct:title",
        namespace=NS_DCT,
    ),
    "cat:dct:description": FieldDefinition(
        name="cat:dct:description",
        description="Free-text account of the catalogue. Mandatory, multilingual.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Language-tagged literal",
        reference="DCAT-AP-SE 2.2.0 §Catalog — mandatory",
        layer="Catalog",
        group="",
        xml_element="dct:description",
        namespace=NS_DCT,
    ),
    "cat:dct:publisher": FieldDefinition(
        name="cat:dct:publisher",
        description=(
            "Entity responsible for publishing the catalogue. "
            "Mandatory. For Swedish public sector: organisation number URI."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of foaf:Agent",
        reference="DCAT-AP-SE 2.2.0 §Catalog — mandatory",
        layer="Catalog",
        group="",
        xml_element="dct:publisher",
        namespace=NS_DCT,
    ),
    "cat:dct:license": FieldDefinition(
        name="cat:dct:license",
        description=(
            "The licence for the catalogue metadata. "
            "DCAT-AP-SE requires CC0 1.0 Universal (Public Domain Dedication) for "
            "all catalogues published on the Swedish national data portal."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="https://creativecommons.org/publicdomain/zero/1.0/ (CC0 1.0 — required in Sweden)",
        reference="DCAT-AP-SE 2.2.0 §Catalog — mandatory",
        layer="Catalog",
        group="",
        xml_element="dct:license",
        namespace=NS_DCT,
    ),
    "cat:dcat:dataset": FieldDefinition(
        name="cat:dcat:dataset",
        description="A dataset included in the catalogue. At least one required.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Dataset instance",
        reference="DCAT-AP-SE 2.2.0 §Catalog — mandatory",
        layer="Catalog",
        group="",
        xml_element="dcat:dataset",
        namespace=NS_DCAT,
    ),
}


class DCATAPSEStandard(MetadataStandard):
    """DCAT-AP-SE 2.2.0 — Swedish national application profile of DCAT-AP."""

    id = "dcat_ap_se"
    name = "DCAT-AP-SE"
    full_name = "Swedish DCAT Application Profile — DCAT-AP-SE version 2.2.0"
    version = "2.2.0"
    organization = "DIGG (Swedish Agency for Digital Government)"
    domain = "EU"
    description = (
        "DCAT-AP-SE is the Swedish national application profile of the EU's DCAT-AP standard, "
        "maintained by DIGG (Swedish Agency for Digital Government). It is mandatory for "
        "datasets published on the Swedish national open data portal (dataportal.se). "
        "Key additions over base DCAT-AP include: mandatory publisher, mandatory CC0 catalogue "
        "license, Geonames URI preference for spatial coverage, support for EU High-value "
        "dataset (HVD) categories, and a Swedish-specific distribution availability vocabulary."
    )
    reference = "DCAT-AP-SE 2.2.0 (DIGG, Sweden)"
    namespace = NS_DCAT
    fields = FIELDS

    _ns_markers = ["dataportal.se", "dcat-ap-se", "dcatse:", "dcat_ap_se"]
    _mandatory_fields_lower = [
        "dct:title", "dct:description", "dct:publisher", "dcat:accessurl",
        "cat:dct:license",
    ]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns.lower():
                score += 0.5
                break

        # Swedish-specific markers
        if "dcatse:availability" in meta_lower or "dcatse" in str(metadata):
            score += 0.3

        if "dcat:hvdcategory" in meta_lower or "dcat:applicablelegislation" in meta_lower:
            score += 0.2

        # DCAT field presence
        dcat_keys = ["dcat:keyword", "dcat:theme", "dcat:distribution", "dcat:contactpoint",
                     "dcat:accessurl", "dcat:downloadurl", "dcat:mediatype"]
        dcat_hits = sum(1 for k in dcat_keys if k in meta_lower)
        score += (dcat_hits / len(dcat_keys)) * 0.2

        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        core_mandatory = ["dct:title", "dct:description", "dct:publisher"]
        for mf in core_mandatory:
            if mf not in meta_lower:
                errors.append(f"Mandatory property missing: {mf} (DCAT-AP-SE 2.2.0 §Dataset)")

        if "dcat:accessurl" not in meta_lower:
            warnings.append(
                "dcat:accessURL missing from Distribution — mandatory if distribution present"
            )

        recommended = ["dcat:contactPoint", "dcat:keyword", "dcat:theme",
                       "dct:identifier", "dct:language", "dct:accessRights", "dct:spatial"]
        for rf in recommended:
            if rf.lower() not in meta_lower:
                warnings.append(f"Recommended property absent: {rf}")

        if "dct:license" in meta_lower:
            license_val = str(meta_lower.get("dct:license", ""))
            if "creativecommons.org/publicdomain/zero" not in license_val and "CC0" not in license_val:
                warnings.append(
                    "Catalog license should be CC0 1.0 for dataportal.se publication "
                    "(DCAT-AP-SE requirement)"
                )

        mandatory_found = sum(
            1 for mf in core_mandatory if mf in meta_lower
        )
        score = mandatory_found / len(core_mandatory)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
