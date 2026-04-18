"""
ISO 19115-1:2014 — Geographic Information — Metadata — Part 1: Fundamentals.

ISO 19115-1 defines the schema required for describing geographic information
and services by means of metadata. It provides information about the identification,
extent, quality, spatial and temporal aspects, content, spatial reference, portrayal,
distribution, and other properties of digital geographic data and services.

Reference:
  ISO 19115-1:2014 Geographic Information — Metadata — Part 1: Fundamentals
  ISO 19115-2:2019 Geographic Information — Metadata — Part 2: Extensions for acquisition and processing
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_GMD = "http://www.isotc211.org/2005/gmd"
NS_GCO = "http://www.isotc211.org/2005/gco"


FIELDS: Dict[str, FieldDefinition] = {

    # ── MD_Metadata root ─────────────────────────────────────────────────────
    "fileIdentifier": FieldDefinition(
        name="fileIdentifier",
        description=(
            "Unique identifier for this metadata record. "
            "Should be a UUID or persistent URI."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="UUID or URI string",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.fileIdentifier",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:fileIdentifier",
        namespace=NS_GMD,
    ),
    "language": FieldDefinition(
        name="language",
        description=(
            "Language used for documenting the metadata. "
            "Mandatory. ISO 639-2/B three-letter code."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-2/B code, e.g., eng, fra, deu",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.language",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:language",
        namespace=NS_GMD,
    ),
    "characterSet": FieldDefinition(
        name="characterSet",
        description=(
            "Full name of the character coding standard used for the metadata set. "
            "Defaults to UTF-8."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="MD_CharacterSetCode: utf8 | ucs2 | ucs4 | utf7 | utf16 | 8859part1..15 | jis",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.characterSet",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:characterSet",
        namespace=NS_GMD,
    ),
    "hierarchyLevel": FieldDefinition(
        name="hierarchyLevel",
        description=(
            "Scope to which the metadata applies. "
            "Required if not a dataset. "
            "Corresponds to ISO 19115 MD_ScopeCode."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values=(
            "attribute | attributeType | collectionHardware | collectionSession | "
            "dataset | series | nonGeographicDataset | dimensionGroup | feature | "
            "featureType | propertyType | fieldSession | software | service | model | tile"
        ),
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.hierarchyLevel",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:hierarchyLevel",
        namespace=NS_GMD,
    ),
    "hierarchyLevelName": FieldDefinition(
        name="hierarchyLevelName",
        description="Name of the hierarchy level for which the metadata is provided.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.hierarchyLevelName",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:hierarchyLevelName",
        namespace=NS_GMD,
    ),
    "contact": FieldDefinition(
        name="contact",
        description=(
            "Party responsible for the metadata information. "
            "Mandatory. Expressed as CI_ResponsibleParty."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="CI_ResponsibleParty: individualName/organisationName, contactInfo, role",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.contact",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:contact",
        namespace=NS_GMD,
    ),
    "dateStamp": FieldDefinition(
        name="dateStamp",
        description=(
            "Date that the metadata was created or last updated. "
            "Mandatory."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 date or datetime",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.dateStamp",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:dateStamp",
        namespace=NS_GMD,
    ),
    "metadataStandardName": FieldDefinition(
        name="metadataStandardName",
        description="Name of the metadata standard used to document the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="e.g., 'ISO 19115', 'INSPIRE Metadata', 'GEMINI 2.3'",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.metadataStandardName",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:metadataStandardName",
        namespace=NS_GMD,
    ),
    "metadataStandardVersion": FieldDefinition(
        name="metadataStandardVersion",
        description="Version of the metadata standard used.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Version string, e.g., '2014'",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.metadataStandardVersion",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:metadataStandardVersion",
        namespace=NS_GMD,
    ),
    "dataSetURI": FieldDefinition(
        name="dataSetURI",
        description="Universally Unique Identifier (UUID) for the dataset described.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.dataSetURI",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:dataSetURI",
        namespace=NS_GMD,
    ),
    "referenceSystemInfo": FieldDefinition(
        name="referenceSystemInfo",
        description="Description of the spatial and temporal reference systems used in the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="MD_ReferenceSystem: RS_Identifier (code, codespace, authority)",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.referenceSystemInfo",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:referenceSystemInfo",
        namespace=NS_GMD,
    ),
    "identificationInfo": FieldDefinition(
        name="identificationInfo",
        description=(
            "Basic information required to uniquely identify a resource. "
            "Mandatory. Contains MD_DataIdentification or SV_ServiceIdentification."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CLASS,
        values="MD_DataIdentification or SV_ServiceIdentification class",
        reference="ISO 19115-1:2014 §B.3.1 MD_Metadata.identificationInfo",
        layer="MD_Metadata",
        group="",
        xml_element="gmd:identificationInfo",
        namespace=NS_GMD,
    ),

    # ── MD_DataIdentification ─────────────────────────────────────────────────
    "citation": FieldDefinition(
        name="citation",
        description=(
            "Citation data for the resource. Mandatory. "
            "Contains CI_Citation with title (mandatory), alternateTitle, "
            "date (mandatory), identifier, citedResponsibleParty, presentationForm."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CLASS,
        values="CI_Citation: title(M), alternateTitle, date(M), identifier, citedResponsibleParty",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.citation",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:citation",
        namespace=NS_GMD,
    ),
    "citationTitle": FieldDefinition(
        name="citationTitle",
        description="The name by which the cited resource is known. Mandatory within CI_Citation.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.4 CI_Citation.title",
        layer="MD_DataIdentification",
        group="Citation",
        xml_element="gmd:title",
        namespace=NS_GMD,
    ),
    "citationDate": FieldDefinition(
        name="citationDate",
        description="Reference date for the cited resource. Mandatory within CI_Citation.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.DATETIME,
        values="CI_Date: date (ISO 8601) + dateType (creation|publication|revision)",
        reference="ISO 19115-1:2014 §B.3.4 CI_Citation.date",
        layer="MD_DataIdentification",
        group="Citation",
        xml_element="gmd:date",
        namespace=NS_GMD,
    ),
    "alternateTitle": FieldDefinition(
        name="alternateTitle",
        description="Short name or other language name by which the cited information is known.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.4 CI_Citation.alternateTitle",
        layer="MD_DataIdentification",
        group="Citation",
        xml_element="gmd:alternateTitle",
        namespace=NS_GMD,
    ),
    "citationIdentifier": FieldDefinition(
        name="citationIdentifier",
        description="Value uniquely identifying the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="RS_Identifier or MD_Identifier",
        reference="ISO 19115-1:2014 §B.3.4 CI_Citation.identifier",
        layer="MD_DataIdentification",
        group="Citation",
        xml_element="gmd:identifier",
        namespace=NS_GMD,
    ),
    "abstract": FieldDefinition(
        name="abstract",
        description="Brief narrative summary of the content of the resource. Mandatory.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.abstract",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:abstract",
        namespace=NS_GMD,
    ),
    "purpose": FieldDefinition(
        name="purpose",
        description="Summary of the intentions with which the resource was developed.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.purpose",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:purpose",
        namespace=NS_GMD,
    ),
    "status": FieldDefinition(
        name="status",
        description="Status of the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="completed | historicalArchive | obsolete | onGoing | planned | required | underDevelopment",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.status (MD_ProgressCode)",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:status",
        namespace=NS_GMD,
    ),
    "pointOfContact": FieldDefinition(
        name="pointOfContact",
        description="Identification of, and means of communication with, person(s) and organisation(s) associated with the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.POINT_OF_CONTACT,
        values="CI_ResponsibleParty: individualName/organisationName, contactInfo, role",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.pointOfContact",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:pointOfContact",
        namespace=NS_GMD,
    ),
    "resourceMaintenance": FieldDefinition(
        name="resourceMaintenance",
        description="Information about the frequency of resource updates, and the scope of those updates.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_MaintenanceInformation: maintenanceAndUpdateFrequency, maintenanceNote",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.resourceMaintenance",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:resourceMaintenance",
        namespace=NS_GMD,
    ),
    "graphicOverview": FieldDefinition(
        name="graphicOverview",
        description="Graphic that provides an illustration of the dataset.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.URI,
        values="MD_BrowseGraphic: fileName, fileDescription, fileType",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.graphicOverview",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:graphicOverview",
        namespace=NS_GMD,
    ),
    "resourceFormat": FieldDefinition(
        name="resourceFormat",
        description="Description of the format of the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_Format: name, version, amendmentNumber",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.resourceFormat",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:resourceFormat",
        namespace=NS_GMD,
    ),
    "descriptiveKeywords": FieldDefinition(
        name="descriptiveKeywords",
        description="Category keywords, their type, and reference source.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_Keywords: keyword (MANY), type (MD_KeywordTypeCode), thesaurusName",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.descriptiveKeywords",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:descriptiveKeywords",
        namespace=NS_GMD,
    ),
    "resourceSpecificUsage": FieldDefinition(
        name="resourceSpecificUsage",
        description="Description of the specific ways the resource is being used by different users.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_Usage: specificUsage, usageDateTime, userDeterminedLimitations, userContactInfo",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.resourceSpecificUsage",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:resourceSpecificUsage",
        namespace=NS_GMD,
    ),
    "resourceConstraints": FieldDefinition(
        name="resourceConstraints",
        description=(
            "Restrictions on the access and use of a resource or metadata. "
            "May be MD_Constraints, MD_LegalConstraints, or MD_SecurityConstraints."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_Constraints, MD_LegalConstraints, or MD_SecurityConstraints",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.resourceConstraints",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:resourceConstraints",
        namespace=NS_GMD,
    ),
    "aggregationInfo": FieldDefinition(
        name="aggregationInfo",
        description="Provides information about the association between resources.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="MD_AggregateInformation: aggregateDataSetName, aggregateDataSetIdentifier, associationType, initiativeType",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.aggregationInfo",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:aggregationInfo",
        namespace=NS_GMD,
    ),
    "spatialRepresentationType": FieldDefinition(
        name="spatialRepresentationType",
        description="Method used to spatially represent geographic information.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="vector | grid | textTable | tin | stereoModel | video",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.spatialRepresentationType",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:spatialRepresentationType",
        namespace=NS_GMD,
    ),
    "spatialResolution": FieldDefinition(
        name="spatialResolution",
        description="Level of detail expressed as a scale factor, a ground distance, or an angle.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.QUANTITY,
        values="MD_Resolution: equivalentScale (MD_RepresentativeFraction) or distance (Length)",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.spatialResolution",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:spatialResolution",
        namespace=NS_GMD,
    ),
    "dataIdentificationLanguage": FieldDefinition(
        name="dataIdentificationLanguage",
        description="Language(s) used within the dataset. Mandatory for datasets.",
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="ISO 639-2/B code, e.g., eng",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.language",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:language",
        namespace=NS_GMD,
    ),
    "topicCategory": FieldDefinition(
        name="topicCategory",
        description=(
            "Main theme(s) of the dataset. "
            "Required for spatial datasets. ISO 19115 MD_TopicCategoryCode."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="MD_TopicCategoryCode: farming | biota | boundaries | climatology... (same as INSPIRE)",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.topicCategory",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:topicCategory",
        namespace=NS_GMD,
    ),
    "extent": FieldDefinition(
        name="extent",
        description=(
            "Spatial and temporal extent of the dataset. "
            "Contains EX_Extent with geographicElement and/or temporalElement."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CLASS,
        values="EX_Extent: description, geographicElement (EX_GeographicBoundingBox), temporalElement (EX_TemporalExtent)",
        reference="ISO 19115-1:2014 §B.3.2 MD_DataIdentification.extent",
        layer="MD_DataIdentification",
        group="",
        xml_element="gmd:extent",
        namespace=NS_GMD,
    ),

    # ── Constraints ──────────────────────────────────────────────────────────
    "useLimitation": FieldDefinition(
        name="useLimitation",
        description="Limitation affecting the fitness for use of the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.3 MD_Constraints.useLimitation",
        layer="Constraints",
        group="",
        xml_element="gmd:useLimitation",
        namespace=NS_GMD,
    ),
    "accessConstraints": FieldDefinition(
        name="accessConstraints",
        description="Access constraints applied to assure protection of privacy or intellectual property.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="MD_RestrictionCode: copyright | patent | patentPending | trademark | license | intellectualPropertyRights | restricted | otherRestrictions",
        reference="ISO 19115-1:2014 §B.3.3 MD_LegalConstraints.accessConstraints",
        layer="Constraints",
        group="LegalConstraints",
        xml_element="gmd:accessConstraints",
        namespace=NS_GMD,
    ),
    "useConstraints": FieldDefinition(
        name="useConstraints",
        description="Constraints applied to assure the protection of privacy or intellectual property, and any special restrictions or limitations on obtaining the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.CODE,
        values="MD_RestrictionCode: (same as accessConstraints)",
        reference="ISO 19115-1:2014 §B.3.3 MD_LegalConstraints.useConstraints",
        layer="Constraints",
        group="LegalConstraints",
        xml_element="gmd:useConstraints",
        namespace=NS_GMD,
    ),
    "otherConstraints": FieldDefinition(
        name="otherConstraints",
        description="Other restrictions and legal prerequisites for accessing and using the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.3 MD_LegalConstraints.otherConstraints",
        layer="Constraints",
        group="LegalConstraints",
        xml_element="gmd:otherConstraints",
        namespace=NS_GMD,
    ),
    "classification": FieldDefinition(
        name="classification",
        description="Name of the handling restrictions on the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="unclassified | restricted | confidential | secret | topSecret | SBU | forOfficialUseOnly | protected | limitedDistribution",
        reference="ISO 19115-1:2014 §B.3.3 MD_SecurityConstraints.classification",
        layer="Constraints",
        group="SecurityConstraints",
        xml_element="gmd:classification",
        namespace=NS_GMD,
    ),
    "userNote": FieldDefinition(
        name="userNote",
        description="Explanation of the application of the legal constraints or other restrictions.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.3 MD_SecurityConstraints.userNote",
        layer="Constraints",
        group="SecurityConstraints",
        xml_element="gmd:userNote",
        namespace=NS_GMD,
    ),
    "classificationSystem": FieldDefinition(
        name="classificationSystem",
        description="Name of the classification system.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text, e.g., 'NATO STANAG 4774', 'US IC Policy'",
        reference="ISO 19115-1:2014 §B.3.3 MD_SecurityConstraints.classificationSystem",
        layer="Constraints",
        group="SecurityConstraints",
        xml_element="gmd:classificationSystem",
        namespace=NS_GMD,
    ),
    "handlingDescription": FieldDefinition(
        name="handlingDescription",
        description="Additional information about the restrictions on handling the resource.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Free text",
        reference="ISO 19115-1:2014 §B.3.3 MD_SecurityConstraints.handlingDescription",
        layer="Constraints",
        group="SecurityConstraints",
        xml_element="gmd:handlingDescription",
        namespace=NS_GMD,
    ),

    # ── Data Quality ──────────────────────────────────────────────────────────
    "scope": FieldDefinition(
        name="scope",
        description="The specific data to which the data quality information applies.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="DQ_Scope: level (MD_ScopeCode), extent, levelDescription",
        reference="ISO 19115-1:2014 §B.3.5 DQ_DataQuality.scope",
        layer="DataQuality",
        group="",
        xml_element="gmd:scope",
        namespace=NS_GMD,
    ),
    "report": FieldDefinition(
        name="report",
        description="Quantitative quality information for the data specified by the scope.",
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="DQ_Element subtype with measureIdentification, result (DQ_ConformanceResult or DQ_QuantitativeResult)",
        reference="ISO 19115-1:2014 §B.3.5 DQ_DataQuality.report",
        layer="DataQuality",
        group="",
        xml_element="gmd:report",
        namespace=NS_GMD,
    ),
    "lineage": FieldDefinition(
        name="lineage",
        description=(
            "Non-quantitative quality information about the lineage of the data "
            "(history, provenance, processing steps)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="LI_Lineage: statement (free text), processStep, source",
        reference="ISO 19115-1:2014 §B.3.5 DQ_DataQuality.lineage / LI_Lineage.statement",
        layer="DataQuality",
        group="",
        xml_element="gmd:lineage",
        namespace=NS_GMD,
    ),
}


class ISO19115Standard(MetadataStandard):
    """ISO 19115-1:2014 — Geographic Information Metadata."""

    id = "iso19115"
    name = "ISO 19115-1"
    full_name = "ISO 19115-1:2014 Geographic Information — Metadata"
    version = "2014"
    organization = "ISO/TC 211"
    domain = "ISO"
    description = (
        "ISO 19115-1:2014 defines the schema required for describing geographic "
        "information and services by means of metadata. It provides a common framework "
        "for describing geospatial data and services used by mapping agencies, "
        "environmental organisations, military organisations, and government bodies "
        "worldwide. It is the foundation for INSPIRE metadata in the EU."
    )
    reference = "ISO 19115-1:2014"
    namespace = NS_GMD
    fields = FIELDS

    _ns_markers = [NS_GMD, "isotc211.org/2005/gmd", "gmd:", "iso19115", "ISO19115"]
    _mandatory_fields = [
        "language", "contact", "dateStamp", "identificationInfo",
        "citation", "citationTitle", "citationDate", "abstract",
        "dataIdentificationLanguage",
    ]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.4
                break

        # Check for ISO-specific field names
        iso_keys = [
            "datestamp", "fileidentifier", "hierarchylevel", "identificationinfo",
            "citation", "mdmetadata", "gmd", "dataidentification",
            "abstractmd", "lineage", "accessconstraints", "useconstraints",
        ]
        hits = sum(1 for k in iso_keys if k in meta_lower)
        score += (hits / len(iso_keys)) * 0.3

        mand_lower = ["language", "contact", "datestamp", "identificationinfo"]
        mand_hits = sum(1 for m in mand_lower if m in meta_lower)
        score += (mand_hits / len(mand_lower)) * 0.3
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in ["language", "contact", "dateStamp", "identificationInfo"]:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory element missing: {mf} (ISO 19115-1:2014 §B.3.1)")

        if "identificationInfo" in meta_lower or "identificationinfo" in meta_lower:
            for mf in ["abstract"]:
                if mf.lower() not in meta_lower:
                    warnings.append(f"Required within identificationInfo: {mf}")

        found = sum(1 for f in ["language", "contact", "datestamp", "identificationinfo"]
                    if f in meta_lower)
        score = found / 4
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
