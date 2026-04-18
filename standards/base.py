"""
Base classes for metadata standards definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class Obligation(Enum):
    MANDATORY = "Mandatory"
    CONDITIONAL = "Conditional"
    OPTIONAL = "Optional"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"
    PROHIBITED = "Prohibited"


class Cardinality(Enum):
    ONE = "One"
    MANY = "Many"


class RepresentationTerm(Enum):
    CODE = "Code"
    CONFIDENTIALITY_LABEL = "ConfidentialityLabel"
    DATETIME = "DateTime"
    GEO_REFERENCE = "GeoReference"
    IDENTIFIER = "Identifier"
    INDICATOR = "Indicator"
    NAME = "Name"
    POINT_OF_CONTACT = "PointOfContact"
    QUANTITY = "Quantity"
    TEXT = "Text"
    TIME_INTERVAL = "TimeInterval"
    CLASS = "Class"       # for standards that use OWL/RDF classes
    BOOLEAN = "Boolean"
    URI = "URI"
    ENUM = "Enum"


@dataclass
class FieldDefinition:
    name: str
    description: str
    obligation: Obligation
    cardinality: Cardinality
    representation_term: RepresentationTerm
    values: str = ""
    reference: str = ""
    comments: str = ""
    not_to_be_confused_with: str = ""
    condition: str = ""        # for CONDITIONAL fields
    layer: str = ""
    group: str = ""
    xml_element: str = ""
    namespace: str = ""


class MetadataStandard:
    id: str = ""
    name: str = ""
    full_name: str = ""
    version: str = ""
    organization: str = ""
    domain: str = ""           # "NATO", "EU", "ISO", "NIST"
    description: str = ""
    reference: str = ""
    fields: Dict[str, FieldDefinition] = {}

    def detect_score(self, metadata: Dict[str, Any]) -> float:
        """Return confidence score 0.0–1.0 for how likely metadata conforms to this standard."""
        raise NotImplementedError

    def validate(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Return {valid: bool, errors: [...], warnings: [...], score: float}"""
        raise NotImplementedError

    def generate_example(self) -> Dict[str, Any]:
        """Return example metadata dict conforming to this standard."""
        raise NotImplementedError

    def get_mandatory_fields(self) -> List[FieldDefinition]:
        return [f for f in self.fields.values() if f.obligation == Obligation.MANDATORY]

    def get_conditional_fields(self) -> List[FieldDefinition]:
        return [f for f in self.fields.values() if f.obligation == Obligation.CONDITIONAL]

    def get_optional_fields(self) -> List[FieldDefinition]:
        return [f for f in self.fields.values() if f.obligation == Obligation.OPTIONAL]

    def _score_fields(self, metadata: Dict[str, Any],
                      mandatory_weight: float = 0.6,
                      optional_weight: float = 0.4) -> float:
        """
        Generic scoring helper used by most standards.
        Counts how many mandatory/optional field names are present in *metadata*.
        Returns a 0.0–1.0 score.
        """
        mandatory = self.get_mandatory_fields()
        optional = self.get_optional_fields()
        all_keys = {k.lower() for k in metadata.keys()}

        mandatory_hits = sum(1 for f in mandatory if f.name.lower() in all_keys)
        optional_hits = sum(1 for f in optional if f.name.lower() in all_keys)

        m_score = (mandatory_hits / len(mandatory)) if mandatory else 0.0
        o_score = (optional_hits / len(optional)) if optional else 0.0

        return mandatory_weight * m_score + optional_weight * o_score
