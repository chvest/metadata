"""
DCAT-AP 2.x — EU Data Catalogue Application Profile for Data Portals in Europe.

DCAT-AP is a specification based on W3C DCAT (Data Catalog Vocabulary) for describing
public sector datasets in Europe. It enables cross-border data discovery through the
European Data Portal and national data portals.

Reference: DCAT-AP 2.1.1 (https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/dcat-application-profile-data-portals-europe)
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_DCAT = "http://www.w3.org/ns/dcat#"
NS_DCT = "http://purl.org/dc/terms/"
NS_FOAF = "http://xmlns.com/foaf/0.1/"
NS_ADMS = "http://www.w3.org/ns/adms#"


FIELDS: Dict[str, FieldDefinition] = {

    # ── dcat:Dataset — Mandatory ─────────────────────────────────────────────
    "dct:title": FieldDefinition(
        name="dct:title",
        description=(
            "A name given to the dataset. Corresponds to dcterms:title. "
            "Should be concise and distinguishable from other datasets in the catalogue."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text (may be repeated for multiple languages using xml:lang)",
        reference="DCAT-AP 2.1.1 §6.1 Dataset mandatory property",
        layer="Dataset",
        group="",
        xml_element="dct:title",
        namespace=NS_DCT,
    ),
    "dct:description": FieldDefinition(
        name="dct:description",
        description=(
            "A free-text account of the dataset. Should describe the content, "
            "purpose, and key characteristics of the dataset clearly enough for "
            "potential consumers to evaluate its relevance."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text (may be repeated per language)",
        reference="DCAT-AP 2.1.1 §6.1 Dataset mandatory property",
        layer="Dataset",
        group="",
        xml_element="dct:description",
        namespace=NS_DCT,
    ),

    # ── dcat:Dataset — Recommended ───────────────────────────────────────────
    "dcat:contactPoint": FieldDefinition(
        name="dcat:contactPoint",
        description=(
            "Relevant contact information for the catalogued resource. "
            "Links to a vCard or similar contact description resource."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="URI of a vCard instance or structured contact object",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dcat:contactPoint",
        namespace=NS_DCAT,
    ),
    "dct:publisher": FieldDefinition(
        name="dct:publisher",
        description=(
            "An entity (organisation) responsible for making the dataset available. "
            "Recommended to use a URI from an authority file (e.g., EU Publications Office NAL)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of foaf:Agent (preferably from a controlled authority)",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:publisher",
        namespace=NS_DCT,
    ),
    "dct:creator": FieldDefinition(
        name="dct:creator",
        description=(
            "An entity responsible for producing the dataset. "
            "May differ from publisher when a dataset is produced by one organisation "
            "and published by another."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of foaf:Agent",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:creator",
        namespace=NS_DCT,
    ),
    "dcat:keyword": FieldDefinition(
        name="dcat:keyword",
        description=(
            "A keyword or tag describing the dataset. "
            "Free-text keywords aid discovery via text search."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text keyword string (repeatable, multilingual)",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dcat:keyword",
        namespace=NS_DCAT,
    ),
    "dcat:theme": FieldDefinition(
        name="dcat:theme",
        description=(
            "The main category of the dataset. "
            "For DCAT-AP this should be a URI from the EU Data Theme Named Authority List "
            "(e.g., http://publications.europa.eu/resource/authority/data-theme/AGRI)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI from EU Data Theme NAL or INSPIRE theme",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dcat:theme",
        namespace=NS_DCAT,
    ),
    "dct:identifier": FieldDefinition(
        name="dct:identifier",
        description=(
            "A unique identifier of the dataset within the context of the catalogue. "
            "Should be a stable, persistent URI."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or other formal identifier string",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
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
        values="ISO 8601 date",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:issued",
        namespace=NS_DCT,
    ),
    "dct:modified": FieldDefinition(
        name="dct:modified",
        description="Most recent date on which the dataset was changed, updated or modified.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:modified",
        namespace=NS_DCT,
    ),
    "dct:language": FieldDefinition(
        name="dct:language",
        description=(
            "A language of the dataset. "
            "Use URIs from the EU Publications Office language authority list."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI, e.g., http://publications.europa.eu/resource/authority/language/ENG",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:language",
        namespace=NS_DCT,
    ),
    "dct:spatial": FieldDefinition(
        name="dct:spatial",
        description=(
            "The geographic region described by the dataset. "
            "Should reference a Named Place (URI) from GEONAMES, EU Countries NAL, etc."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a geographic location resource (GeoNames, NUTS, EU Countries NAL)",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:spatial",
        namespace=NS_DCT,
    ),
    "dct:temporal": FieldDefinition(
        name="dct:temporal",
        description="The temporal period that the dataset covers.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="dct:PeriodOfTime with dcat:startDate and dcat:endDate",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
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
        values="URI of the licence (SPDX, Creative Commons, EU Publications Office Licence NAL)",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:license",
        namespace=NS_DCT,
    ),
    "dct:accessRights": FieldDefinition(
        name="dct:accessRights",
        description=(
            "Information that indicates whether the dataset is publicly accessible, "
            "has access restrictions, or is non-public. "
            "Use EU Access Rights NAL: PUBLIC, RESTRICTED, NON_PUBLIC."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values=(
            "URI from EU Access Rights NAL: "
            "http://publications.europa.eu/resource/authority/access-right/PUBLIC | "
            "RESTRICTED | NON_PUBLIC"
        ),
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dct:accessRights",
        namespace=NS_DCT,
    ),
    "dcat:distribution": FieldDefinition(
        name="dcat:distribution",
        description="An available distribution for the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Distribution instance",
        reference="DCAT-AP 2.1.1 §6.2 Dataset recommended property",
        layer="Dataset",
        group="",
        xml_element="dcat:distribution",
        namespace=NS_DCAT,
    ),

    # ── dcat:Dataset — Optional ──────────────────────────────────────────────
    "owl:versionInfo": FieldDefinition(
        name="owl:versionInfo",
        description="A version indicator (name or identifier) of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Version string",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="owl:versionInfo",
        namespace="http://www.w3.org/2002/07/owl#",
    ),
    "adms:identifier": FieldDefinition(
        name="adms:identifier",
        description="A secondary identifier of the dataset (in a different identifier scheme).",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="adms:Identifier instance",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="adms:identifier",
        namespace=NS_ADMS,
    ),
    "dct:type": FieldDefinition(
        name="dct:type",
        description="The type of the dataset. Recommended: EU Dataset Type NAL.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI from EU Dataset Type NAL or DCMI Type vocabulary",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:type",
        namespace=NS_DCT,
    ),
    "dct:provenance": FieldDefinition(
        name="dct:provenance",
        description="A statement about the lineage of a Dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:provenance",
        namespace=NS_DCT,
    ),
    "dct:conformsTo": FieldDefinition(
        name="dct:conformsTo",
        description="An implementing rule or other specification that the dataset conforms to.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the standard/specification",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:conformsTo",
        namespace=NS_DCT,
    ),
    "dct:source": FieldDefinition(
        name="dct:source",
        description="A related dataset from which the described dataset is derived.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the source dataset",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:source",
        namespace=NS_DCT,
    ),
    "dct:hasVersion": FieldDefinition(
        name="dct:hasVersion",
        description="A related dataset that is a version, edition, or adaptation of the described dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:hasVersion",
        namespace=NS_DCT,
    ),
    "dct:isVersionOf": FieldDefinition(
        name="dct:isVersionOf",
        description="A related dataset of which the described dataset is a version, edition, or adaptation.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:isVersionOf",
        namespace=NS_DCT,
    ),
    "dct:relation": FieldDefinition(
        name="dct:relation",
        description="A resource with an unspecified relationship to the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:relation",
        namespace=NS_DCT,
    ),
    "dct:hasPart": FieldDefinition(
        name="dct:hasPart",
        description="A related resource that is included either physically or logically in the described dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:hasPart",
        namespace=NS_DCT,
    ),
    "dct:isPartOf": FieldDefinition(
        name="dct:isPartOf",
        description="A related resource in which the described dataset is physically or logically included.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:isPartOf",
        namespace=NS_DCT,
    ),
    "dcat:qualifiedRelation": FieldDefinition(
        name="dcat:qualifiedRelation",
        description="A description of a relationship with another resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Relationship instance",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dcat:qualifiedRelation",
        namespace=NS_DCAT,
    ),
    "prov:qualifiedAttribution": FieldDefinition(
        name="prov:qualifiedAttribution",
        description="An attribution that includes agent, role and other contextual information.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a prov:Attribution instance",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="prov:qualifiedAttribution",
        namespace="http://www.w3.org/ns/prov#",
    ),
    "dct:accrualPeriodicity": FieldDefinition(
        name="dct:accrualPeriodicity",
        description="The frequency at which the dataset is updated.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI from MDR Frequency NAL, e.g., .../frequency/ANNUAL",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:accrualPeriodicity",
        namespace=NS_DCT,
    ),
    "dcat:landingPage": FieldDefinition(
        name="dcat:landingPage",
        description="A Web page that can be navigated to in a Web browser to gain access to the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of the landing page",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dcat:landingPage",
        namespace=NS_DCAT,
    ),
    "dcat:spatialResolutionInMeters": FieldDefinition(
        name="dcat:spatialResolutionInMeters",
        description="The minimum spatial separation resolvable in a dataset, measured in meters.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.QUANTITY,
        values="xsd:decimal value in meters",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dcat:spatialResolutionInMeters",
        namespace=NS_DCAT,
    ),
    "dcat:temporalResolution": FieldDefinition(
        name="dcat:temporalResolution",
        description="The minimum time period resolvable in the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="xsd:duration, e.g., PT1H (1 hour), P1D (1 day)",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dcat:temporalResolution",
        namespace=NS_DCAT,
    ),
    "adms:sample": FieldDefinition(
        name="adms:sample",
        description="A sample distribution of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:Distribution instance",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="adms:sample",
        namespace=NS_ADMS,
    ),
    "dct:isReferencedBy": FieldDefinition(
        name="dct:isReferencedBy",
        description="A related resource, such as a publication, that references, cites, or otherwise points to the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="DCAT-AP 2.1.1 §6.3 Dataset optional property",
        layer="Dataset",
        group="",
        xml_element="dct:isReferencedBy",
        namespace=NS_DCT,
    ),

    # ── dcat:Distribution — Mandatory ────────────────────────────────────────
    "dcat:accessURL": FieldDefinition(
        name="dcat:accessURL",
        description=(
            "A URL of the resource that gives access to a distribution of the dataset. "
            "This is the only mandatory property for a distribution. "
            "It may link to a data file or an API endpoint."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URL of the access endpoint or download page",
        reference="DCAT-AP 2.1.1 §6.4 Distribution mandatory property",
        layer="Distribution",
        group="",
        xml_element="dcat:accessURL",
        namespace=NS_DCAT,
    ),

    # ── dcat:Distribution — Recommended/Optional ─────────────────────────────
    "dcat:downloadURL": FieldDefinition(
        name="dcat:downloadURL",
        description="The URL of the downloadable file in a given format.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="Direct download URL",
        reference="DCAT-AP 2.1.1 §6.5 Distribution recommended property",
        layer="Distribution",
        group="",
        xml_element="dcat:downloadURL",
        namespace=NS_DCAT,
    ),
    "dct:format": FieldDefinition(
        name="dct:format",
        description="The file format of the distribution. Use the MDR File Type NAL.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI from MDR File Type NAL, e.g., .../file-type/PDF",
        reference="DCAT-AP 2.1.1 §6.5 Distribution recommended property",
        layer="Distribution",
        group="",
        xml_element="dct:format",
        namespace=NS_DCT,
    ),
    "dcat:mediaType": FieldDefinition(
        name="dcat:mediaType",
        description="The media type of the distribution. Use IANA media types.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="IANA MIME type, e.g., application/json, text/csv",
        reference="DCAT-AP 2.1.1 §6.5 Distribution recommended property",
        layer="Distribution",
        group="",
        xml_element="dcat:mediaType",
        namespace=NS_DCAT,
    ),
    "dcat:byteSize": FieldDefinition(
        name="dcat:byteSize",
        description="The size of a distribution in bytes.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.QUANTITY,
        values="xsd:decimal integer (number of bytes)",
        reference="DCAT-AP 2.1.1 §6.6 Distribution optional property",
        layer="Distribution",
        group="",
        xml_element="dcat:byteSize",
        namespace=NS_DCAT,
    ),
    "odrl:hasPolicy": FieldDefinition(
        name="odrl:hasPolicy",
        description="An ODRL conformant policy expressing the rights associated with the distribution.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of an odrl:Policy instance",
        reference="DCAT-AP 2.1.1 §6.6 Distribution optional property",
        layer="Distribution",
        group="",
        xml_element="odrl:hasPolicy",
        namespace="http://www.w3.org/ns/odrl/2/",
    ),
    "adms:status": FieldDefinition(
        name="adms:status",
        description="The status of the distribution in the context of a particular workflow process.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI from ADMS status vocabulary: Completed | Deprecated | UnderDevelopment | Withdrawn",
        reference="DCAT-AP 2.1.1 §6.6 Distribution optional property",
        layer="Distribution",
        group="",
        xml_element="adms:status",
        namespace=NS_ADMS,
    ),
    "dcat:accessService": FieldDefinition(
        name="dcat:accessService",
        description="A data service that gives access to the distribution of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URI of a dcat:DataService instance",
        reference="DCAT-AP 2.1.1 §6.6 Distribution optional property",
        layer="Distribution",
        group="",
        xml_element="dcat:accessService",
        namespace=NS_DCAT,
    ),
}


class DCATAPStandard(MetadataStandard):
    """DCAT-AP 2.x — EU Data Catalogue Application Profile."""

    id = "dcat_ap"
    name = "DCAT-AP"
    full_name = "EU Data Catalogue Application Profile for Data Portals in Europe"
    version = "2.1.1"
    organization = "European Commission / SEMIC"
    domain = "EU"
    description = (
        "DCAT-AP is the European standard for describing datasets and data services "
        "in public-sector data portals. It extends W3C DCAT with European-specific "
        "requirements, particularly for linking to EU-controlled vocabularies "
        "(Named Authority Lists published by the EU Publications Office). "
        "DCAT-AP defines classes for Catalogue, Dataset, Distribution, and DataService."
    )
    reference = "DCAT-AP 2.1.1 (SEMIC/European Commission)"
    namespace = NS_DCAT
    fields = FIELDS

    _ns_markers = [NS_DCAT, "w3.org/ns/dcat", "dcat-ap", "www.w3.org/ns/dcat"]
    _mandatory_fields_lower = ["dct:title", "dct:description", "dcat:accessurl"]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.4
                break

        # Check for DCAT-specific keys (with namespace prefix)
        dcat_keys = ["dcat:keyword", "dcat:theme", "dcat:distribution", "dcat:contactpoint",
                     "dcat:accessurl", "dcat:downloadurl", "dcat:mediatype", "dcat:landingpage"]
        dct_keys = ["dct:title", "dct:description", "dct:publisher", "dct:language",
                    "dct:spatial", "dct:temporal", "dct:issued", "dct:modified"]

        dcat_hits = sum(1 for k in dcat_keys if k in meta_lower)
        dct_hits = sum(1 for k in dct_keys if k in meta_lower)

        score += (dcat_hits / len(dcat_keys)) * 0.3
        score += (dct_hits / len(dct_keys)) * 0.3
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in self._mandatory_fields_lower:
            if mf not in meta_lower:
                errors.append(f"Mandatory property missing: {mf} (DCAT-AP 2.1.1 §6.1/§6.4)")

        recommended = ["dcat:contactPoint", "dct:publisher", "dcat:keyword",
                       "dcat:theme", "dct:identifier", "dct:language"]
        for rf in recommended:
            if rf.lower() not in meta_lower:
                warnings.append(f"Recommended property absent: {rf}")

        mandatory_found = sum(1 for mf in self._mandatory_fields_lower if mf in meta_lower)
        score = mandatory_found / len(self._mandatory_fields_lower)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
