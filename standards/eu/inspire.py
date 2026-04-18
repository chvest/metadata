"""
INSPIRE Metadata Directive — EU Spatial Data Infrastructure.

INSPIRE (Infrastructure for Spatial Information in the European Community)
Directive 2007/2/EC establishes a spatial data infrastructure in the EU.
The INSPIRE Metadata Regulation (EC 1205/2008) and associated Technical
Guidelines define metadata requirements for spatial datasets and services.

Reference:
  INSPIRE Metadata Regulation EC 1205/2008
  INSPIRE Technical Guidelines for implementing dataset and service metadata
  https://inspire.ec.europa.eu/metadata/
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_INSPIRE = "http://inspire.ec.europa.eu/schemas/common/1.0"


FIELDS: Dict[str, FieldDefinition] = {

    # ── Identification ───────────────────────────────────────────────────────
    "title": FieldDefinition(
        name="title",
        description=(
            "A characteristic, and often unique, name by which the resource is known. "
            "Corresponds to ISO 19115 MD_DataIdentification.citation.title."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="INSPIRE Metadata Regulation §2.2.1 / ISO 19115 §B.3.2",
        layer="Identification",
        group="",
        xml_element="title",
        namespace=NS_INSPIRE,
    ),
    "abstract": FieldDefinition(
        name="abstract",
        description=(
            "A brief narrative summary of the content of the resource. "
            "Should clearly describe the scope, content and intended use of the dataset."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text (minimum 200 characters recommended)",
        reference="INSPIRE Metadata Regulation §2.2.2 / ISO 19115 §B.3.2",
        layer="Identification",
        group="",
        xml_element="abstract",
        namespace=NS_INSPIRE,
    ),
    "resourceType": FieldDefinition(
        name="resourceType",
        description=(
            "The type of resource being described. "
            "Possible values: dataset, series, service."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="dataset | series | service",
        reference="INSPIRE Metadata Regulation §2.2 / ISO 19115 MD_ScopeCode",
        layer="Identification",
        group="",
        xml_element="resourceType",
        namespace=NS_INSPIRE,
    ),
    "uniqueResourceIdentifier": FieldDefinition(
        name="uniqueResourceIdentifier",
        description=(
            "A value uniquely identifying the resource. Recommended as a URL "
            "or other persistent identifier. "
            "Corresponds to ISO 19115 MD_DataIdentification.citation.identifier."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI or code with optional codespace attribute",
        reference="INSPIRE Metadata Regulation §2.2.3 / ISO 19115 §B.3.2",
        layer="Identification",
        group="",
        xml_element="uniqueResourceIdentifier",
        namespace=NS_INSPIRE,
    ),
    "resourceLocator": FieldDefinition(
        name="resourceLocator",
        description=(
            "Location (address) for online access to the resource. "
            "Should be a URL for downloading or viewing the resource."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="URL",
        reference="INSPIRE Metadata Regulation §2.2.4 / ISO 19115 §B.3.2",
        layer="Identification",
        group="",
        xml_element="resourceLocator",
        namespace=NS_INSPIRE,
    ),
    "coupledResource": FieldDefinition(
        name="coupledResource",
        description=(
            "The identifier of datasets the service operates on "
            "(only for spatial data services)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI reference to the coupled dataset",
        reference="INSPIRE Metadata Regulation §2.2.5",
        layer="Identification",
        group="",
        xml_element="coupledResource",
        namespace=NS_INSPIRE,
    ),
    "resourceLanguage": FieldDefinition(
        name="resourceLanguage",
        description=(
            "The language(s) used within the resource. "
            "Mandatory for datasets and dataset series if they contain textual information. "
            "Use ISO 639-2/B three-letter codes."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-2/B language code, e.g., eng, fra, deu, nld",
        reference="INSPIRE Metadata Regulation §2.2.7 / ISO 19115 MD_DataIdentification.language",
        layer="Identification",
        group="",
        xml_element="resourceLanguage",
        namespace=NS_INSPIRE,
    ),
    "topicCategory": FieldDefinition(
        name="topicCategory",
        description=(
            "The main theme(s) of the dataset. "
            "Mandatory for spatial datasets and dataset series. "
            "Values drawn from MD_TopicCategoryCode."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values=(
            "farming | biota | boundaries | climatologyMeteorologyAtmosphere | economy | "
            "elevation | environment | geoscientificInformation | health | imageryBaseMapsEarthCover | "
            "intelligenceMilitary | inlandWaters | location | oceans | planningCadastre | "
            "society | structure | transportation | utilitiesCommunication | extraTerrestrial | "
            "disaster"
        ),
        reference="INSPIRE Metadata Regulation §2.2.8 / ISO 19115 MD_TopicCategoryCode",
        layer="Identification",
        group="",
        xml_element="topicCategory",
        namespace=NS_INSPIRE,
    ),
    "serviceType": FieldDefinition(
        name="serviceType",
        description="A service type name as defined in the INSPIRE Service Types Register.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="discovery | view | download | transformation | invoke | other",
        reference="INSPIRE Metadata Regulation §2.2.9",
        layer="Identification",
        group="",
        xml_element="serviceType",
        namespace=NS_INSPIRE,
    ),

    # ── Classification ───────────────────────────────────────────────────────
    "keyword": FieldDefinition(
        name="keyword",
        description=(
            "A commonly used word, formalised word or phrase used to describe the subject. "
            "At least one keyword from the GEMET INSPIRE themes thesaurus is mandatory."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Keyword value; if from thesaurus, specify originatingControlledVocabulary",
        reference="INSPIRE Metadata Regulation §2.3.1 / ISO 19115 MD_Keywords.keyword",
        layer="Classification",
        group="",
        xml_element="keyword",
        namespace=NS_INSPIRE,
    ),
    "originatingControlledVocabulary": FieldDefinition(
        name="originatingControlledVocabulary",
        description=(
            "The name and optionally the edition of the formally registered thesaurus "
            "or a similar authoritative source of keywords."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Thesaurus name with date/edition, e.g., GEMET - INSPIRE themes, version 1.0 (2008-06-01)",
        reference="INSPIRE Metadata Regulation §2.3.2 / ISO 19115 MD_Keywords.thesaurusName",
        layer="Classification",
        group="",
        xml_element="originatingControlledVocabulary",
        namespace=NS_INSPIRE,
    ),

    # ── Geographic ───────────────────────────────────────────────────────────
    "geographicBoundingBox": FieldDefinition(
        name="geographicBoundingBox",
        description=(
            "The spatial extent of the resource as a geographic bounding box "
            "defined by west, east, south and north latitude/longitude in decimal degrees. "
            "Mandatory for spatial datasets, dataset series, and services with a geographic extent."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.GEO_REFERENCE,
        values="WGS 84 decimal degrees: westBoundLongitude, eastBoundLongitude, southBoundLatitude, northBoundLatitude",
        reference="INSPIRE Metadata Regulation §2.4.1 / ISO 19115 EX_GeographicBoundingBox",
        layer="Geographic",
        group="",
        xml_element="geographicBoundingBox",
        namespace=NS_INSPIRE,
    ),
    "geographicDescription": FieldDefinition(
        name="geographicDescription",
        description="A description of the spatial extent of the resource as a character string.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or code identifying a named area",
        reference="INSPIRE Metadata Regulation §2.4.2 / ISO 19115 EX_GeographicDescription",
        layer="Geographic",
        group="",
        xml_element="geographicDescription",
        namespace=NS_INSPIRE,
    ),
    "spatialRepresentationType": FieldDefinition(
        name="spatialRepresentationType",
        description="The method used to spatially represent geographic information.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="vector | grid | textTable | tin | stereoModel | video",
        reference="INSPIRE Metadata Regulation §2.4 / ISO 19115 MD_SpatialRepresentationTypeCode",
        layer="Geographic",
        group="",
        xml_element="spatialRepresentationType",
        namespace=NS_INSPIRE,
    ),
    "spatialResolution": FieldDefinition(
        name="spatialResolution",
        description=(
            "The level of detail in the resource, expressed as an equivalent scale "
            "or a ground sample distance (in metres)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.QUANTITY,
        values="Equivalent scale (e.g., 1:50000) or ground sample distance in metres",
        reference="INSPIRE Metadata Regulation §2.4.3 / ISO 19115 MD_Resolution",
        layer="Geographic",
        group="",
        xml_element="spatialResolution",
        namespace=NS_INSPIRE,
    ),

    # ── Temporal ─────────────────────────────────────────────────────────────
    "temporalExtent": FieldDefinition(
        name="temporalExtent",
        description=(
            "The time period covered by the content of the resource. "
            "Expressed as a time instant or time period."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TIME_INTERVAL,
        values="ISO 8601 time instant or period (beginPosition/endPosition)",
        reference="INSPIRE Metadata Regulation §2.5.1 / ISO 19115 EX_TemporalExtent",
        layer="Temporal",
        group="",
        xml_element="temporalExtent",
        namespace=NS_INSPIRE,
    ),
    "dateOfPublication": FieldDefinition(
        name="dateOfPublication",
        description="Date of publication of the resource. At least one date (publication, last revision, or creation) is required.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="INSPIRE Metadata Regulation §2.5.2 / ISO 19115 CI_Citation.date (publication)",
        layer="Temporal",
        group="",
        xml_element="dateOfPublication",
        namespace=NS_INSPIRE,
    ),
    "dateOfLastRevision": FieldDefinition(
        name="dateOfLastRevision",
        description="Date of last revision of the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="INSPIRE Metadata Regulation §2.5.3 / ISO 19115 CI_Citation.date (revision)",
        layer="Temporal",
        group="",
        xml_element="dateOfLastRevision",
        namespace=NS_INSPIRE,
    ),
    "dateOfCreation": FieldDefinition(
        name="dateOfCreation",
        description="Date of creation of the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="INSPIRE Metadata Regulation §2.5.4 / ISO 19115 CI_Citation.date (creation)",
        layer="Temporal",
        group="",
        xml_element="dateOfCreation",
        namespace=NS_INSPIRE,
    ),

    # ── Quality ──────────────────────────────────────────────────────────────
    "lineage": FieldDefinition(
        name="lineage",
        description=(
            "General explanation of the data producer's knowledge about the lineage of a dataset. "
            "Describes the history of the dataset (sources, processing steps, methods)."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="INSPIRE Metadata Regulation §2.6.1 / ISO 19115 LI_Lineage.statement",
        layer="Quality",
        group="",
        xml_element="lineage",
        namespace=NS_INSPIRE,
    ),

    # ── Conformity ───────────────────────────────────────────────────────────
    "specification": FieldDefinition(
        name="specification",
        description=(
            "The specification (often an INSPIRE implementing rule or a standard) "
            "to which the resource conforms or was evaluated against."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Citation to a standard or specification document",
        reference="INSPIRE Metadata Regulation §2.7 / ISO 19115 DQ_ConformanceResult.specification",
        layer="Conformity",
        group="",
        xml_element="specification",
        namespace=NS_INSPIRE,
    ),
    "degree": FieldDefinition(
        name="degree",
        description="The degree of conformity of the resource with the implementing rule or specification.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="true (conformant) | false (non-conformant) | null (not evaluated)",
        reference="INSPIRE Metadata Regulation §2.7 / ISO 19115 DQ_ConformanceResult.pass",
        layer="Conformity",
        group="",
        xml_element="degree",
        namespace=NS_INSPIRE,
    ),

    # ── Constraints ──────────────────────────────────────────────────────────
    "conditionsForAccessAndUse": FieldDefinition(
        name="conditionsForAccessAndUse",
        description=(
            "Conditions applying to access and use of the resource. "
            "Mandatory; if no conditions apply, state 'no conditions apply'. "
            "If unknown, state 'conditions unknown'."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text or URI to license/rights document",
        reference="INSPIRE Metadata Regulation §2.8.1 / ISO 19115 MD_LegalConstraints",
        layer="Constraints",
        group="",
        xml_element="conditionsForAccessAndUse",
        namespace=NS_INSPIRE,
    ),
    "limitationsOnPublicAccess": FieldDefinition(
        name="limitationsOnPublicAccess",
        description=(
            "Limitations on public access to the resource and the reasons for such limitations. "
            "Mandatory. If no limitations apply, state this explicitly."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text referencing EC 2003/98/EC or INSPIRE exception codes",
        reference="INSPIRE Metadata Regulation §2.8.2 / ISO 19115 MD_SecurityConstraints",
        layer="Constraints",
        group="",
        xml_element="limitationsOnPublicAccess",
        namespace=NS_INSPIRE,
    ),

    # ── Responsible Party ────────────────────────────────────────────────────
    "responsibleParty": FieldDefinition(
        name="responsibleParty",
        description=(
            "Identification of, and means of communication with, person(s) and organisations(s) "
            "associated with the resource. Mandatory. "
            "Corresponds to ISO 19115 CI_ResponsibleParty."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="CI_ResponsibleParty: organisationName, contactInfo (email, address), role",
        reference="INSPIRE Metadata Regulation §2.9.1 / ISO 19115 CI_ResponsibleParty",
        layer="ResponsibleParty",
        group="",
        xml_element="responsibleParty",
        namespace=NS_INSPIRE,
    ),
    "roleCode": FieldDefinition(
        name="roleCode",
        description="The role of the responsible party for the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="resourceProvider | custodian | owner | user | distributor | originator | pointOfContact | principalInvestigator | processor | publisher | author",
        reference="INSPIRE Metadata Regulation §2.9.2 / ISO 19115 CI_RoleCode",
        layer="ResponsibleParty",
        group="",
        xml_element="roleCode",
        namespace=NS_INSPIRE,
    ),

    # ── Metadata ─────────────────────────────────────────────────────────────
    "metadataLanguage": FieldDefinition(
        name="metadataLanguage",
        description=(
            "The language in which the metadata elements are expressed. "
            "Mandatory. Use ISO 639-2/B three-letter codes."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-2/B code, e.g., eng, fra",
        reference="INSPIRE Metadata Regulation §2.10.1 / ISO 19115 MD_Metadata.language",
        layer="Metadata",
        group="",
        xml_element="metadataLanguage",
        namespace=NS_INSPIRE,
    ),
    "metadataDate": FieldDefinition(
        name="metadataDate",
        description=(
            "The date on which the metadata record was created or most recently updated. "
            "Mandatory."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date",
        reference="INSPIRE Metadata Regulation §2.10.2 / ISO 19115 MD_Metadata.dateStamp",
        layer="Metadata",
        group="",
        xml_element="metadataDate",
        namespace=NS_INSPIRE,
    ),
    "metadataPointOfContact": FieldDefinition(
        name="metadataPointOfContact",
        description=(
            "The organisation responsible for the creation and maintenance of the metadata record. "
            "Mandatory. Distinct from responsibleParty (which is for the resource)."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="CI_ResponsibleParty: organisationName, email (mandatory), role=pointOfContact",
        reference="INSPIRE Metadata Regulation §2.10.3 / ISO 19115 MD_Metadata.contact",
        layer="Metadata",
        group="",
        xml_element="metadataPointOfContact",
        namespace=NS_INSPIRE,
    ),
}


class INSPIREStandard(MetadataStandard):
    """INSPIRE Metadata Directive — EU Spatial Data Infrastructure."""

    id = "inspire"
    name = "INSPIRE"
    full_name = "INSPIRE Metadata Directive (EC 1205/2008)"
    version = "INSPIRE Technical Guidelines v2.0"
    organization = "European Commission"
    domain = "EU"
    description = (
        "INSPIRE defines metadata requirements for spatial datasets and services "
        "under EU Directive 2007/2/EC. The metadata regulation (EC 1205/2008) "
        "specifies mandatory and conditional elements derived from ISO 19115. "
        "INSPIRE metadata is widely used by national mapping agencies and public "
        "sector bodies across EU member states for spatial data discovery."
    )
    reference = "INSPIRE Metadata Regulation EC 1205/2008 / INSPIRE Technical Guidelines v2.0"
    namespace = NS_INSPIRE
    fields = FIELDS

    _ns_markers = ["inspire.ec.europa.eu", "inspire", "gmx:", "gmd:", "csw:Record"]
    _mandatory_fields = [
        "title", "abstract", "topicCategory", "keyword",
        "geographicBoundingBox", "lineage",
        "conditionsForAccessAndUse", "limitationsOnPublicAccess",
        "responsibleParty", "metadataLanguage", "metadataDate", "metadataPointOfContact",
    ]

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

        inspire_specific = [
            "topiccategory", "geographicboundingbox", "lineage",
            "conditionsforaccessanduse", "limitationsonpublicaccess",
            "metadatalanguage", "metadatadate", "metadatapointofcontact",
        ]
        hits = sum(1 for k in inspire_specific if k in meta_lower)
        score += (hits / len(inspire_specific)) * 0.2
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in self._mandatory_fields:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory element missing: {mf} (INSPIRE Metadata Regulation §2)")

        # Date check — at least one date type
        date_fields = ["dateofpublication", "dateoflastrevision", "dateofcreation"]
        if not any(d in meta_lower for d in date_fields):
            errors.append(
                "At least one date (dateOfPublication, dateOfLastRevision, or dateOfCreation) "
                "is required (INSPIRE Metadata Regulation §2.5)"
            )

        found = sum(1 for mf in self._mandatory_fields if mf.lower() in meta_lower)
        score = found / len(self._mandatory_fields)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
