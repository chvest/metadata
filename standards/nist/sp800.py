"""
NIST SP 800-60 Vol. 1 Rev. 1 — Guide for Mapping Types of Information and
Information Systems to Security Categories.

NIST IR 8112 — Attribute Metadata: A Proposed Schema for Evaluating Federated
Attributes (2016).

References:
  NIST SP 800-60 Vol. 1 Rev. 1 (2008)
  NIST IR 8112 (2016) — https://doi.org/10.6028/NIST.IR.8112
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_SP800 = "http://csrc.nist.gov/ns/sp800/1.0"


# ── NIST SP 800-60 fields ───────────────────────────────────────────────────
FIELDS_SP80060: Dict[str, FieldDefinition] = {
    "informationTypeIdentifier": FieldDefinition(
        name="informationTypeIdentifier",
        description=(
            "A unique identifier for the information type as defined in "
            "NIST SP 800-60 Appendix C. "
            "Format: C.x.y where x is the mission area and y is the information type number."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="C.x.y format, e.g., C.2.1 (Administrative Management), C.3.1 (Defense and National Security)",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.1",
        layer="SecurityCategorization",
        group="",
        xml_element="informationTypeIdentifier",
        namespace=NS_SP800,
    ),
    "systemName": FieldDefinition(
        name="systemName",
        description=(
            "The official name of the information system being categorised. "
            "Must match the system name in the system security plan (SSP)."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Official system name string",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.2",
        layer="SecurityCategorization",
        group="",
        xml_element="systemName",
        namespace=NS_SP800,
    ),
    "missionArea": FieldDefinition(
        name="missionArea",
        description=(
            "The mission area from the Federal Enterprise Architecture (FEA) "
            "Business Reference Model to which the information type belongs. "
            "Examples: Services for Citizens, Support Delivery of Services, "
            "Management of Government Resources."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values=(
            "Services for Citizens | Support Delivery of Services | "
            "Management of Government Resources | Defense / National Security / "
            "Foreign Affairs | Intelligence | Intra-Government Services"
        ),
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.1 / Appendix C",
        layer="SecurityCategorization",
        group="",
        xml_element="missionArea",
        namespace=NS_SP800,
    ),
    "informationType": FieldDefinition(
        name="informationType",
        description=(
            "The type of information processed, stored, or transmitted by the "
            "information system, drawn from the NIST SP 800-60 information type taxonomy. "
            "Examples: Financial Management, Personnel Records, Intelligence."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Information type name from NIST SP 800-60 Appendix C taxonomy",
        reference="NIST SP 800-60 Vol.1 Rev.1 Appendix C",
        layer="SecurityCategorization",
        group="",
        xml_element="informationType",
        namespace=NS_SP800,
    ),
    "confidentialityImpact": FieldDefinition(
        name="confidentialityImpact",
        description=(
            "The provisional impact level for the confidentiality of this information type. "
            "Low: limited adverse effect; Moderate: serious adverse effect; "
            "High: severe or catastrophic adverse effect on operations, assets, or individuals."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.ENUM,
        values="Low | Moderate | High",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.3 / FIPS 199",
        layer="SecurityCategorization",
        group="ImpactLevels",
        xml_element="confidentialityImpact",
        namespace=NS_SP800,
    ),
    "integrityImpact": FieldDefinition(
        name="integrityImpact",
        description=(
            "The provisional impact level for the integrity of this information type. "
            "Low: limited adverse effect; Moderate: serious adverse effect; "
            "High: severe or catastrophic adverse effect."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.ENUM,
        values="Low | Moderate | High",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.3 / FIPS 199",
        layer="SecurityCategorization",
        group="ImpactLevels",
        xml_element="integrityImpact",
        namespace=NS_SP800,
    ),
    "availabilityImpact": FieldDefinition(
        name="availabilityImpact",
        description=(
            "The provisional impact level for the availability of this information type. "
            "Low: limited adverse effect; Moderate: serious adverse effect; "
            "High: severe or catastrophic adverse effect."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.ENUM,
        values="Low | Moderate | High",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.3 / FIPS 199",
        layer="SecurityCategorization",
        group="ImpactLevels",
        xml_element="availabilityImpact",
        namespace=NS_SP800,
    ),
    "systemSecurityCategory": FieldDefinition(
        name="systemSecurityCategory",
        description=(
            "The overall security category of the information system, derived by "
            "applying the high-watermark principle across all information types "
            "for each security objective (confidentiality, integrity, availability). "
            "Expressed using FIPS 199 notation: SC system = {(confidentiality, impact), "
            "(integrity, impact), (availability, impact)}."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="FIPS 199 notation, e.g., SC = {(C,High),(I,Moderate),(A,Low)} → Overall: High",
        reference="NIST SP 800-60 Vol.1 Rev.1 §2.4 / FIPS 199",
        layer="SecurityCategorization",
        group="",
        xml_element="systemSecurityCategory",
        namespace=NS_SP800,
    ),
    "privacyDesignation": FieldDefinition(
        name="privacyDesignation",
        description=(
            "Indicates whether the information system processes Personally Identifiable "
            "Information (PII) or other privacy-sensitive information requiring "
            "Privacy Act compliance."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.BOOLEAN,
        values="true | false",
        reference="NIST SP 800-60 Vol.1 Rev.1 §3.3",
        layer="SecurityCategorization",
        group="Privacy",
        xml_element="privacyDesignation",
        namespace=NS_SP800,
    ),
    "sornRequired": FieldDefinition(
        name="sornRequired",
        description=(
            "Whether a System of Records Notice (SORN) under the Privacy Act (5 U.S.C. §552a) "
            "is required for this system. Required when the system contains a 'system of records' "
            "as defined by the Privacy Act."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.BOOLEAN,
        values="true | false",
        reference="NIST SP 800-60 Vol.1 Rev.1 §3.3 / Privacy Act",
        layer="SecurityCategorization",
        group="Privacy",
        xml_element="sornRequired",
        namespace=NS_SP800,
    ),
    "piaRequired": FieldDefinition(
        name="piaRequired",
        description=(
            "Whether a Privacy Impact Assessment (PIA) is required under "
            "E-Government Act of 2002 §208. Required when a system collects, "
            "maintains, or disseminates information in identifiable form."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.BOOLEAN,
        values="true | false",
        reference="NIST SP 800-60 Vol.1 Rev.1 §3.3 / E-Government Act §208",
        layer="SecurityCategorization",
        group="Privacy",
        xml_element="piaRequired",
        namespace=NS_SP800,
    ),
}

NS_IR8112 = "http://csrc.nist.gov/ns/ir8112/1.0"


# ── NIST IR 8112 — Attribute Metadata Schema ───────────────────────────────
FIELDS_IR8112: Dict[str, FieldDefinition] = {
    "attributeName": FieldDefinition(
        name="attributeName",
        description=(
            "A human-readable identifier for the attribute, unique within the scope of "
            "the attribute provider. The attribute name should be drawn from an "
            "agreed vocabulary or namespace wherever possible. "
            "Example: 'givenName', 'employeeNumber', 'clearanceLevel'."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.NAME,
        values="String; recommend URI-based name for federated contexts",
        reference="NIST IR 8112 §3.1",
        layer="AttributeDescription",
        group="",
        xml_element="attributeName",
        namespace=NS_IR8112,
    ),
    "attributeValue": FieldDefinition(
        name="attributeValue",
        description=(
            "The value of the attribute for a specific subject at a specific point in time. "
            "The format of the value is determined by the attributeDataType. "
            "A single attribute may have multiple values (e.g., multiple roles)."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Any; constrained by attributeDataType",
        reference="NIST IR 8112 §3.2",
        layer="AttributeDescription",
        group="",
        xml_element="attributeValue",
        namespace=NS_IR8112,
    ),
    "attributeDataType": FieldDefinition(
        name="attributeDataType",
        description=(
            "The data type of the attribute value, specifying the format and "
            "constraints applicable to the value. Enables consuming parties to "
            "correctly parse and validate the attribute value."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="string | integer | boolean | dateTime | URI | base64Binary | custom",
        reference="NIST IR 8112 §3.3",
        layer="AttributeDescription",
        group="",
        xml_element="attributeDataType",
        namespace=NS_IR8112,
    ),
    "attributeOrigin": FieldDefinition(
        name="attributeOrigin",
        description=(
            "The authoritative source of the attribute value — i.e., the organisation "
            "or system that asserted or issued the attribute. "
            "Relying parties use this to assess trustworthiness."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI identifying the attribute provider or issuing authority",
        reference="NIST IR 8112 §3.4",
        layer="Provenance",
        group="",
        xml_element="attributeOrigin",
        namespace=NS_IR8112,
    ),
    "attributeVerification": FieldDefinition(
        name="attributeVerification",
        description=(
            "The method(s) by which the attribute value was verified against "
            "authoritative sources. Describes the level of assurance associated "
            "with the attribute value."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="in-person | remote | self-asserted | document-check | biometric | none",
        reference="NIST IR 8112 §3.5",
        layer="Provenance",
        group="",
        xml_element="attributeVerification",
        namespace=NS_IR8112,
    ),
    "lastVerified": FieldDefinition(
        name="lastVerified",
        description=(
            "The date and time at which the attribute value was most recently verified "
            "against an authoritative source. Used by relying parties to assess "
            "the currency of the attribute."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 dateTime, e.g., 2024-03-15T09:30:00Z",
        reference="NIST IR 8112 §3.6",
        layer="Provenance",
        group="",
        xml_element="lastVerified",
        namespace=NS_IR8112,
    ),
    "expiryDate": FieldDefinition(
        name="expiryDate",
        description=(
            "The date and time after which the attribute value should no longer be "
            "considered valid. Relying parties must not accept attribute values "
            "past their expiry date."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 dateTime",
        reference="NIST IR 8112 §3.7",
        layer="Validity",
        group="",
        xml_element="expiryDate",
        namespace=NS_IR8112,
    ),
    "attributeAccuracy": FieldDefinition(
        name="attributeAccuracy",
        description=(
            "An indication of the accuracy or confidence level of the attribute value, "
            "based on the verification method used and the trustworthiness of the source. "
            "May be expressed as a percentage, level, or qualitative descriptor."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="high | medium | low | percentage (0-100)",
        reference="NIST IR 8112 §3.8",
        layer="Quality",
        group="",
        xml_element="attributeAccuracy",
        namespace=NS_IR8112,
    ),
    "attributeConsistency": FieldDefinition(
        name="attributeConsistency",
        description=(
            "Indicates whether the attribute value is consistent across multiple "
            "authoritative sources or identity providers. Inconsistency may signal "
            "data quality issues or identity conflicts requiring resolution."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.BOOLEAN,
        values="true | false",
        reference="NIST IR 8112 §3.9",
        layer="Quality",
        group="",
        xml_element="attributeConsistency",
        namespace=NS_IR8112,
    ),
    "attributeProvenance": FieldDefinition(
        name="attributeProvenance",
        description=(
            "A description of the chain of custody and transformation history of the "
            "attribute value from its origin to the current assertion. "
            "Documents any aggregation, derivation, or transformation applied."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Free text description of provenance chain",
        reference="NIST IR 8112 §3.10",
        layer="Provenance",
        group="",
        xml_element="attributeProvenance",
        namespace=NS_IR8112,
    ),
    "policyIdentifier": FieldDefinition(
        name="policyIdentifier",
        description=(
            "A URI identifying the policy or trust framework under which the attribute "
            "was issued and is governed. Relying parties use this to determine whether "
            "the attribute was issued under a compatible trust framework."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI, e.g., http://idmanagement.gov/ns/trustmark/1.0/",
        reference="NIST IR 8112 §3.11",
        layer="Trust",
        group="",
        xml_element="policyIdentifier",
        namespace=NS_IR8112,
    ),
    "assertingParty": FieldDefinition(
        name="assertingParty",
        description=(
            "The entity (identity provider or attribute provider) that is asserting "
            "the attribute value in the current transaction. May differ from the "
            "attributeOrigin if the attribute has been re-asserted or proxied."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI identifying the asserting party",
        reference="NIST IR 8112 §3.12",
        layer="Trust",
        group="",
        xml_element="assertingParty",
        namespace=NS_IR8112,
    ),
    "relyingParty": FieldDefinition(
        name="relyingParty",
        description=(
            "The entity that is consuming and relying upon the attribute value for an "
            "access control or identity decision. Scoping the attribute to a relying "
            "party limits its use to the intended transaction."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.IDENTIFIER,
        values="URI identifying the relying party",
        reference="NIST IR 8112 §3.13",
        layer="Trust",
        group="",
        xml_element="relyingParty",
        namespace=NS_IR8112,
    ),
}

ALL_FIELDS = {**FIELDS_SP80060, **FIELDS_IR8112}


class NISTSP80060Standard(MetadataStandard):
    """NIST SP 800-60 Vol. 1 Rev. 1 — Security Categorization."""

    id = "nist_sp80060"
    name = "NIST SP 800-60"
    full_name = "NIST SP 800-60 Vol. 1 Rev. 1 — Guide for Mapping Information Types to Security Categories"
    version = "Rev. 1 (2008)"
    organization = "NIST"
    domain = "NIST"
    description = (
        "NIST SP 800-60 provides guidance for identifying the types of information "
        "processed by federal information systems and mapping those information types "
        "to appropriate security categories (based on FIPS 199). "
        "Security categories drive the selection of security controls from "
        "NIST SP 800-53."
    )
    reference = "NIST SP 800-60 Vol. 1 Rev. 1 (NIST, 2008)"
    namespace = NS_SP800
    fields = FIELDS_SP80060

    _ns_markers = [NS_SP800, "csrc.nist.gov", "nist.gov/sp800", "fips199"]
    _mandatory_fields = [
        "informationTypeIdentifier", "systemName", "missionArea",
        "informationType", "confidentialityImpact", "integrityImpact",
        "availabilityImpact", "systemSecurityCategory",
    ]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.3
                break

        nist_keys = [
            "informationtypeidentifier", "systemname", "missionarea", "informationtype",
            "confidentialityimpact", "integrityimpact", "availabilityimpact",
            "systemsecuritycategory", "privacydesignation", "sornrequired", "piarequired",
        ]
        hits = sum(1 for k in nist_keys if k in meta_lower)
        score += (hits / len(nist_keys)) * 0.7
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in self._mandatory_fields:
            if mf.lower() not in meta_lower:
                errors.append(f"Required element missing: {mf} (NIST SP 800-60 §2)")

        # Validate impact levels
        for impact_field in ["confidentialityimpact", "integrityimpact", "availabilityimpact"]:
            val = str(meta_lower.get(impact_field, "")).title()
            if val and val not in {"Low", "Moderate", "High"}:
                errors.append(f"{impact_field} must be Low, Moderate, or High (FIPS 199)")

        found = sum(1 for f in self._mandatory_fields if f.lower() in meta_lower)
        score = found / len(self._mandatory_fields)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)


class NISTIR8112Standard(MetadataStandard):
    """NIST IR 8112 — Attribute Metadata Schema for federated identity attributes."""

    id = "nist_ir8112"
    name = "NIST IR 8112"
    full_name = "NIST IR 8112 — Attribute Metadata: A Proposed Schema for Evaluating Federated Attributes"
    version = "2016"
    organization = "NIST"
    domain = "NIST"
    description = (
        "NIST IR 8112 defines a metadata schema for describing the properties of "
        "identity attributes exchanged in federated identity systems. It enables "
        "relying parties to evaluate the trustworthiness, accuracy, currency, and "
        "provenance of attribute values asserted by identity providers. "
        "Key metadata properties include the attribute's origin, verification method, "
        "accuracy, consistency, expiry, and the policy framework under which it was issued. "
        "It is designed to complement SAML, OpenID Connect, and similar federation protocols."
    )
    reference = "NIST IR 8112 (NIST, 2016) — https://doi.org/10.6028/NIST.IR.8112"
    namespace = NS_IR8112
    fields = FIELDS_IR8112

    _ns_markers = [NS_IR8112, "csrc.nist.gov/ns/ir8112", "ir8112", "nist.gov/ir8112"]
    _mandatory_fields = ["attributeName", "attributeValue", "attributeDataType", "attributeOrigin"]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.3
                break

        key_fields = [
            "attributename", "attributevalue", "attributedatatype", "attributeorigin",
            "attributeverification", "lastverified", "expirydate", "attributeaccuracy",
            "attributeconsistency", "attributeprovenance", "policyidentifier",
            "assertingparty", "relyingparty",
        ]
        hits = sum(1 for k in key_fields if k in meta_lower)
        score += (hits / len(key_fields)) * 0.7
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in self._mandatory_fields:
            if mf.lower() not in meta_lower:
                errors.append(f"Required element missing: {mf} (NIST IR 8112 §3)")

        # Validate attributeDataType if present
        valid_types = {"string", "integer", "boolean", "datetime", "uri", "base64binary", "custom"}
        dt = str(meta_lower.get("attributedatatype", "")).lower()
        if dt and dt not in valid_types:
            warnings.append(f"attributeDataType '{dt}' is not a recognised value (NIST IR 8112 §3.3)")

        found = sum(1 for f in self._mandatory_fields if f.lower() in meta_lower)
        score = found / len(self._mandatory_fields)
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
