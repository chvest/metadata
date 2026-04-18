"""
ADatP-4774 (Confidentiality Metadata Label Syntax) and
ADatP-4778 (Metadata Binding Mechanism) — NATO STANAGs.

ADatP-4774 defines the XML structure for expressing confidentiality labels
on NATO information resources, enabling NATO-wide interoperability of
access-control metadata.

ADatP-4778 defines the binding mechanism that attaches confidentiality labels
(ADatP-4774) to information objects using XML Signatures.

References:
  ADatP-4774 Ed. A V1  — Confidentiality Metadata Label Syntax
  ADatP-4778 Ed. A V1  — Metadata Binding Mechanism
"""
from typing import Any, Dict
from standards.base import (
    FieldDefinition, MetadataStandard,
    Obligation, Cardinality, RepresentationTerm
)

NS_4774 = "urn:nato:stanag:4774:confidentialitymetadatalabel:1:0"
NS_4778 = "urn:nato:stanag:4778:bindinginformation:1:0"


# ── ADatP-4774 field catalogue ──────────────────────────────────────────────
FIELDS_4774: Dict[str, FieldDefinition] = {
    "PolicyIdentifier": FieldDefinition(
        name="PolicyIdentifier",
        description=(
            "Identifies the security policy under which the confidentiality label "
            "was created. For NATO use this is typically the NATO Security Policy "
            "identifier URI, e.g., urn:nato:policy:security. Each participating "
            "nation or organisation defines its own policy URI."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI, e.g., urn:nato:policy:security, urn:us:policy:gov:ic:ism",
        reference="ADatP-4774 Ed.A V1 §3.2.1",
        layer="Label",
        group="ConfidentialityInformation",
        xml_element="PolicyIdentifier",
        namespace=NS_4774,
    ),
    "Classification": FieldDefinition(
        name="Classification",
        description=(
            "The classification level assigned to the resource under the referenced "
            "security policy. NATO classification levels in ascending order: "
            "UNCLASSIFIED, NATO RESTRICTED, NATO CONFIDENTIAL, NATO SECRET, "
            "COSMIC TOP SECRET."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values=(
            "UNCLASSIFIED | NATO RESTRICTED | NATO CONFIDENTIAL | "
            "NATO SECRET | COSMIC TOP SECRET"
        ),
        reference="ADatP-4774 Ed.A V1 §3.2.2",
        layer="Label",
        group="ConfidentialityInformation",
        xml_element="Classification",
        namespace=NS_4774,
    ),
    "CategoryTagName": FieldDefinition(
        name="CategoryTagName",
        description=(
            "The name of an additional access-control category applied to the "
            "resource. Categories supplement the base classification level. "
            "Examples: ATOMAL, CRYPTO, releasability caveats."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.NAME,
        values="Controlled vocabulary of category tag names per policy",
        reference="ADatP-4774 Ed.A V1 §3.2.3",
        layer="Label",
        group="Category",
        xml_element="TagName",
        namespace=NS_4774,
    ),
    "CategoryType": FieldDefinition(
        name="CategoryType",
        description=(
            "The type or nature of the category (e.g., PERMISSIVE or RESTRICTIVE). "
            "PERMISSIVE categories expand access (e.g., REL TO); "
            "RESTRICTIVE categories further restrict access (e.g., SCI compartments)."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.ENUM,
        values="PERMISSIVE | RESTRICTIVE | INFORMATIVE",
        reference="ADatP-4774 Ed.A V1 §3.2.4",
        layer="Label",
        group="Category",
        xml_element="Type",
        namespace=NS_4774,
    ),
    "CategoryGenericValue": FieldDefinition(
        name="CategoryGenericValue",
        description=(
            "The value associated with a category tag. For releasability tags "
            "this would be the country trigraphs (e.g., GBR, FRA, DEU). "
            "For compartments it would be the compartment name."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.MANY,
        representation_term=RepresentationTerm.TEXT,
        values="Policy-defined values; for releasability: ISO 3166-1 alpha-3 country codes",
        reference="ADatP-4774 Ed.A V1 §3.2.5",
        layer="Label",
        group="Category",
        xml_element="GenericValue",
        namespace=NS_4774,
    ),
    "CreationDateTime": FieldDefinition(
        name="CreationDateTime",
        description=(
            "The date and time at which the confidentiality label was created or "
            "last modified. Enables detection of stale labels and supports audit "
            "trails for label changes."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.DATETIME,
        values="ISO 8601 datetime with timezone, e.g., 2024-03-15T09:30:00Z",
        reference="ADatP-4774 Ed.A V1 §3.3",
        layer="Label",
        group="",
        xml_element="CreationDateTime",
        namespace=NS_4774,
    ),
}


# ── ADatP-4778 field catalogue ──────────────────────────────────────────────
FIELDS_4778: Dict[str, FieldDefinition] = {
    "MetadataReference": FieldDefinition(
        name="MetadataReference",
        description=(
            "A reference (URI) to the metadata or label being bound to the "
            "data object. Ensures the binding is unambiguous and the metadata "
            "can be independently retrieved and verified."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI referencing the metadata document or label",
        reference="ADatP-4778 Ed.A V1 §3.2.1",
        layer="Binding",
        group="BindingInformation",
        xml_element="MetadataReference",
        namespace=NS_4778,
    ),
    "DataObjectReference": FieldDefinition(
        name="DataObjectReference",
        description=(
            "A reference (URI) to the data object to which the metadata/label "
            "is being bound. Allows systems to locate and verify the resource "
            "that the binding applies to."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.URI,
        values="URI of the data object (file, message, dataset)",
        reference="ADatP-4778 Ed.A V1 §3.2.2",
        layer="Binding",
        group="BindingInformation",
        xml_element="DataObjectReference",
        namespace=NS_4778,
    ),
    "BindingMethod": FieldDefinition(
        name="BindingMethod",
        description=(
            "The cryptographic or structural method used to bind the metadata "
            "to the data object. The primary method defined by ADatP-4778 is "
            "W3C XML Signature (xmldsig), providing integrity protection."
        ),
        obligation=Obligation.MANDATORY,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="XML_SIGNATURE | HASH | REFERENCE_ONLY",
        reference="ADatP-4778 Ed.A V1 §3.2.3",
        comments=(
            "XML Signature (http://www.w3.org/2000/09/xmldsig#) is the preferred "
            "method for cryptographic binding."
        ),
        layer="Binding",
        group="BindingInformation",
        xml_element="BindingMethod",
        namespace=NS_4778,
    ),
    "SignatureValue": FieldDefinition(
        name="SignatureValue",
        description=(
            "The base64-encoded cryptographic signature value that binds the "
            "metadata to the data object. Present when BindingMethod is XML_SIGNATURE."
        ),
        obligation=Obligation.CONDITIONAL,
        condition="Required when BindingMethod = XML_SIGNATURE",
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Base64-encoded XML Signature value",
        reference="ADatP-4778 Ed.A V1 §3.2.4",
        layer="Binding",
        group="BindingInformation",
        xml_element="SignatureValue",
        namespace=NS_4778,
    ),
    "HashValue": FieldDefinition(
        name="HashValue",
        description=(
            "A cryptographic hash of the bound data object. Used for integrity "
            "verification in conjunction with or as an alternative to XML Signature."
        ),
        obligation=Obligation.OPTIONAL,
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.TEXT,
        values="Hex-encoded or base64-encoded hash; algorithm specified separately",
        reference="ADatP-4778 Ed.A V1 §3.2.5",
        layer="Binding",
        group="BindingInformation",
        xml_element="HashValue",
        namespace=NS_4778,
    ),
    "HashAlgorithm": FieldDefinition(
        name="HashAlgorithm",
        description=(
            "The algorithm used to compute the HashValue. "
            "SHA-256 is the minimum recommended algorithm for NATO use."
        ),
        obligation=Obligation.CONDITIONAL,
        condition="Required when HashValue is present",
        cardinality=Cardinality.ONE,
        representation_term=RepresentationTerm.CODE,
        values="SHA-256 | SHA-384 | SHA-512",
        reference="ADatP-4778 Ed.A V1 §3.2.6",
        layer="Binding",
        group="BindingInformation",
        xml_element="HashAlgorithm",
        namespace=NS_4778,
    ),
}


class ADatP4774Standard(MetadataStandard):
    """ADatP-4774 — Confidentiality Metadata Label Syntax."""

    id = "adatp4774"
    name = "ADatP-4774"
    full_name = "Confidentiality Metadata Label Syntax"
    version = "Ed. A V1"
    organization = "NATO"
    domain = "NATO"
    description = (
        "ADatP-4774 defines the XML syntax for expressing confidentiality labels "
        "on NATO information resources. A label is a structured XML element "
        "(ConfidentialityInformation) containing a PolicyIdentifier, a Classification "
        "level, zero or more Categories, and a CreationDateTime. Labels are used "
        "by ADatP-5636 (field originatorConfidentialityLabel) and bound to resources "
        "by ADatP-4778."
    )
    reference = "ADatP-4774 Ed. A V1"
    namespace = NS_4774
    fields = FIELDS_4774

    _ns_markers = [NS_4774, "stanag:4774", "confidentialitymetadatalabel"]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.5
                break

        mandatory_lower = ["policyidentifier", "classification", "creationdatetime"]
        hits = sum(1 for f in mandatory_lower if f in meta_lower)
        score += (hits / len(mandatory_lower)) * 0.5
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in ["PolicyIdentifier", "Classification", "CreationDateTime"]:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory field missing: {mf} (ADatP-4774 §3.2)")

        # Check classification value
        cl = str(meta_lower.get("classification", "")).upper()
        valid_cl = {"UNCLASSIFIED", "NATO RESTRICTED", "NATO CONFIDENTIAL",
                    "NATO SECRET", "COSMIC TOP SECRET"}
        if cl and cl not in valid_cl:
            warnings.append(f"Classification value '{cl}' not in standard NATO classification levels")

        score = sum(1 for f in ["policyidentifier", "classification", "creationdatetime"]
                    if f in meta_lower) / 3
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)


class ADatP4778Standard(MetadataStandard):
    """ADatP-4778 — Metadata Binding Mechanism."""

    id = "adatp4778"
    name = "ADatP-4778"
    full_name = "Metadata Binding Mechanism"
    version = "Ed. A V1"
    organization = "NATO"
    domain = "NATO"
    description = (
        "ADatP-4778 defines the mechanism for binding confidentiality metadata "
        "(ADatP-4774 labels) to information objects using XML Signatures. "
        "The BindingInformation element contains references to both the metadata "
        "and the data object, along with the binding method and optionally a "
        "cryptographic hash for integrity verification."
    )
    reference = "ADatP-4778 Ed. A V1"
    namespace = NS_4778
    fields = FIELDS_4778

    _ns_markers = [NS_4778, "stanag:4778", "bindinginformation"]

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        score = 0.0

        ns = str(metadata.get("@namespace", "") or metadata.get("namespace", ""))
        for marker in self._ns_markers:
            if marker in ns:
                score += 0.5
                break

        for f in ["metadatareference", "dataobjectreference", "bindingmethod"]:
            if f in meta_lower:
                score += 0.15
        return min(score, 1.0)

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        meta_lower = {k.lower(): v for k, v in metadata.items()}
        errors, warnings = [], []

        for mf in ["MetadataReference", "DataObjectReference", "BindingMethod"]:
            if mf.lower() not in meta_lower:
                errors.append(f"Mandatory field missing: {mf} (ADatP-4778 §3.2)")

        bm = str(meta_lower.get("bindingmethod", "")).upper()
        if bm == "XML_SIGNATURE" and "signaturevalue" not in meta_lower:
            errors.append("SignatureValue required when BindingMethod = XML_SIGNATURE (ADatP-4778 §3.2.4)")
        if "hashvalue" in meta_lower and "hashalgorithm" not in meta_lower:
            errors.append("HashAlgorithm required when HashValue is present (ADatP-4778 §3.2.6)")

        score = sum(1 for f in ["metadatareference", "dataobjectreference", "bindingmethod"]
                    if f in meta_lower) / 3
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "score": score}

    def generate_example(self) -> Dict[str, Any]:
        from engine.generator import FieldGenerator
        gen = FieldGenerator()
        return gen.generate_for_standard(self)
