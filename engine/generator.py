"""
Metadata Generator.

Generates realistic example metadata records for each supported standard.
Uses Faker for realistic text data.
"""
import json
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

from faker import Faker
from standards.base import (
    MetadataStandard, FieldDefinition, Obligation, RepresentationTerm
)

fake = Faker()
Faker.seed(42)


# ---------------------------------------------------------------------------
# Value generators per RepresentationTerm
# ---------------------------------------------------------------------------

NATO_ORGS = [
    "HQ NATO", "ACO SHAPE", "ACT Norfolk", "NCI Agency", "NSPA",
    "HQ AIRCOM", "HQ LANDCOM", "HQ MARCOM", "JFC Brunssum", "JFC Naples",
    "NATO Standardization Office", "NATO HQ Brussels",
]

NATO_CLASSIFICATIONS = [
    "UNCLASSIFIED", "NATO RESTRICTED", "NATO CONFIDENTIAL", "NATO SECRET"
]

COUNTRY_CODES_EU = [
    "GB", "FR", "DE", "NL", "BE", "PL", "IT", "ES", "PT", "GR", "DK",
    "NO", "CA", "US", "TR", "CZ", "HU", "RO", "BG", "HR", "SK", "SI",
    "EE", "LV", "LT", "AL", "MK", "ME", "RS", "BA",
]

MIME_TYPES = [
    "application/pdf", "text/xml", "application/json", "text/html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg", "image/tiff", "application/gzip", "text/csv",
    "application/zip",
]

NATO_RESOURCE_TYPES = [
    "Report", "Order", "Directive", "Plan", "Message", "Record",
    "Standard", "Doctrine", "Assessment", "Policy", "Instruction",
]

TOPIC_CATEGORIES = [
    "intelligenceMilitary", "defense", "boundaries", "transportation",
    "environment", "location", "imageryBaseMapsEarthCover", "structure",
]

IMPACT_LEVELS = ["Low", "Moderate", "High"]

NIST_MISSION_AREAS = [
    "Services for Citizens", "Support Delivery of Services",
    "Management of Government Resources", "Defense / National Security",
]

NIST_INFO_TYPES = [
    "C.2.1 — Administrative Management", "C.3.1 — Defense and National Security",
    "C.5.1 — Financial Management", "C.2.2 — Human Resources",
    "C.3.2 — Intelligence", "C.4.1 — Transportation",
]

EU_THEMES = [
    "http://publications.europa.eu/resource/authority/data-theme/GOVE",
    "http://publications.europa.eu/resource/authority/data-theme/TRAN",
    "http://publications.europa.eu/resource/authority/data-theme/ENVI",
    "http://publications.europa.eu/resource/authority/data-theme/JUST",
]

LANGUAGES = ["eng", "fra", "deu", "nld", "pol", "ita", "spa", "por", "nor", "dan"]
BCP47_LANGUAGES = ["en", "fr", "de", "nl", "pl", "it", "es", "pt"]


def _rand_date(past_years: int = 5) -> str:
    start = datetime.now() - timedelta(days=past_years * 365)
    dt = start + timedelta(days=random.randint(0, past_years * 365))
    return dt.strftime("%Y-%m-%d")


def _rand_datetime(past_years: int = 5) -> str:
    start = datetime.now() - timedelta(days=past_years * 365)
    dt = start + timedelta(
        days=random.randint(0, past_years * 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _point_of_contact(role: str = "creator") -> str:
    first = fake.first_name()
    last = fake.last_name()
    org = random.choice(NATO_ORGS)
    email_domain = org.lower().replace(" ", "").replace(".", "") + ".nato.int"
    email = f"{first[0].lower()}.{last.lower()}@{email_domain}"
    phone = f"+32-2-{random.randint(100,999)}-{random.randint(1000,9999)}"
    return (
        f"type=person; name={first} {last}; "
        f"affiliation={org}; email={email}; phone={phone}; role={role}"
    )


def _nato_urn() -> str:
    year = random.randint(2018, 2024)
    doc_type = random.choice(["DOC", "REP", "MSG", "ORD", "DIR"])
    num = random.randint(1000, 99999)
    return f"urn:nato:resource:{year}:{doc_type}-{num}"


def _confidentiality_label(classification: Optional[str] = None) -> str:
    cl = classification or random.choice(NATO_CLASSIFICATIONS)
    nation = random.choice(COUNTRY_CODES_EU)
    return (
        f"PolicyIdentifier=urn:nato:policy:security; "
        f"Classification={cl}; "
        f"Category[TagName=Releasability,Type=PERMISSIVE,GenericValue={nation}]; "
        f"CreationDateTime={_rand_datetime()}"
    )


def _geo_reference() -> str:
    lat = round(random.uniform(35.0, 70.0), 4)
    lon = round(random.uniform(-10.0, 35.0), 4)
    return f"WGS84-DD; lat={lat}; lon={lon}"


def _bounding_box() -> Dict[str, float]:
    lon1 = round(random.uniform(-10.0, 30.0), 2)
    lat1 = round(random.uniform(35.0, 65.0), 2)
    lon2 = round(lon1 + random.uniform(0.5, 5.0), 2)
    lat2 = round(lat1 + random.uniform(0.5, 5.0), 2)
    return {
        "westBoundLongitude": lon1,
        "eastBoundLongitude": lon2,
        "southBoundLatitude": lat1,
        "northBoundLatitude": lat2,
    }


def _time_interval() -> str:
    start = _rand_date(3)
    from datetime import date
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = start_dt + timedelta(days=random.randint(30, 365))
    return f"start={start}; end={end_dt.strftime('%Y-%m-%d')}"


class FieldGenerator:
    """Generates realistic fake values for each RepresentationTerm."""

    def generate_value(self, field: FieldDefinition, standard_id: str = "") -> Any:
        rt = field.representation_term
        name_low = field.name.lower()

        # Special cases by field name
        if "confidentialitylabel" in name_low:
            return _confidentiality_label()
        if "policyidentifier" in name_low:
            return "urn:nato:policy:security"
        if "classification" in name_low and "system" not in name_low:
            if standard_id.startswith("adatp4774"):
                return random.choice(NATO_CLASSIFICATIONS)
            if "iso19115" in standard_id:
                return random.choice(["unclassified", "restricted", "confidential", "secret"])
            return random.choice(NATO_CLASSIFICATIONS)
        if "creationdatetime" in name_low or "datestamp" in name_low:
            return _rand_datetime()
        if "identifier" in name_low and "type" not in name_low:
            if "nist" in standard_id or "information" in name_low:
                return random.choice(NIST_INFO_TYPES).split(" — ")[0]
            if "file" in name_low:
                import uuid
                return str(uuid.uuid4())
            return _nato_urn()
        if "metadatareference" in name_low or "dataobjectreference" in name_low:
            return _nato_urn()
        if "bindingmethod" in name_low:
            return "XML_SIGNATURE"
        if "signaturevalue" in name_low:
            return "dGhpcyBpcyBhIGZha2Ugc2lnbmF0dXJlIHZhbHVl"
        if "hashvalue" in name_low:
            import hashlib
            return hashlib.sha256(fake.sentence().encode()).hexdigest()
        if "hashalgorithm" in name_low:
            return "SHA-256"

        # By RepresentationTerm
        if rt == RepresentationTerm.CONFIDENTIALITY_LABEL:
            return _confidentiality_label()

        if rt == RepresentationTerm.DATETIME:
            if "date" in name_low and any(x in name_low for x in ["stamp", "created", "modified", "issued"]):
                return _rand_datetime()
            return _rand_date()

        if rt == RepresentationTerm.POINT_OF_CONTACT:
            role = "creator"
            if "publisher" in name_low:
                role = "publisher"
            elif "contributor" in name_low:
                role = "contributor"
            elif "custodian" in name_low:
                role = "custodian"
            elif "contact" in name_low:
                role = "pointOfContact"
            elif "responsible" in name_low:
                role = "pointOfContact"
            return _point_of_contact(role)

        if rt == RepresentationTerm.IDENTIFIER:
            return _nato_urn()

        if rt == RepresentationTerm.URI:
            if "license" in name_low or "licence" in name_low:
                return "https://creativecommons.org/licenses/by/4.0/"
            if "spatial" in name_low:
                return f"http://www.geonames.org/{random.randint(1000000, 9999999)}"
            if "theme" in name_low:
                return random.choice(EU_THEMES)
            if "publisher" in name_low or "creator" in name_low:
                return f"https://publications.europa.eu/resource/authority/corporate-body/{random.choice(['NATO', 'EUROSTAT', 'EC'])}"
            if "language" in name_low:
                lang = random.choice(BCP47_LANGUAGES).upper()
                return f"http://publications.europa.eu/resource/authority/language/{lang}"
            if "accessrights" in name_low:
                return random.choice([
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
                    "http://publications.europa.eu/resource/authority/access-right/RESTRICTED",
                    "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC",
                ])
            return _nato_urn()

        if rt == RepresentationTerm.GEO_REFERENCE:
            if "bounding" in name_low:
                bb = _bounding_box()
                return str(bb)
            return _geo_reference()

        if rt == RepresentationTerm.CODE:
            if "country" in name_low:
                return random.choice(COUNTRY_CODES_EU)
            if "language" in name_low:
                return random.choice(LANGUAGES)
            if "type" in name_low and "mime" not in name_low and "media" not in name_low:
                return random.choice(NATO_RESOURCE_TYPES)
            if "format" in name_low or "media" in name_low:
                return random.choice(MIME_TYPES)
            if "topic" in name_low or "category" in name_low:
                return random.choice(TOPIC_CATEGORIES)
            if "status" in name_low:
                return random.choice(["Active", "Draft", "Superseded", "Archived"])
            if "spatial" in name_low and "representation" in name_low:
                return random.choice(["vector", "grid", "textTable"])
            if "hierarchy" in name_low:
                return random.choice(["dataset", "series", "nonGeographicDataset"])
            if "impact" in name_low or "confidentiality" in name_low or "integrity" in name_low or "availability" in name_low:
                return random.choice(IMPACT_LEVELS)
            return random.choice(["Code001", "Code002", "Code003"])

        if rt == RepresentationTerm.TEXT:
            if "title" in name_low:
                return f"{fake.catch_phrase()} — {fake.word().title()} {random.randint(2020, 2024)}"
            if "abstract" in name_low or "description" in name_low or "summary" in name_low:
                return fake.paragraph(nb_sentences=5)
            if "keyword" in name_low or "subject" in name_low:
                return fake.word().title()
            if "lineage" in name_low or "provenance" in name_low:
                return f"Data derived from {fake.company()} on {_rand_date()}. " \
                       f"Processing steps: {fake.sentence(nb_words=10)}"
            if "purpose" in name_low:
                return fake.sentence(nb_words=15)
            if "version" in name_low:
                return f"{random.randint(1, 5)}.{random.randint(0, 9)}"
            if "mandate" in name_low:
                return f"Regulation (EU) No {random.randint(100, 2000)}/{random.randint(2000, 2024)}"
            if "condition" in name_low or "access" in name_low or "rights" in name_low:
                return "No conditions apply."
            if "limitation" in name_low:
                return "No limitations on public access."
            if "toc" in name_low or "tableofcontents" in name_low:
                return "1. Introduction\n2. Background\n3. Main Content\n4. Conclusions\n5. References"
            if "extent" in name_low and "qualifier" not in name_low:
                return f"{random.randint(10, 500)} pages"
            if "disposition" in name_low:
                return f"Retain for {random.randint(5, 20)} years then destroy. Authority: DA-{random.randint(100,999)}"
            if "systemnameidentifier" in name_low or "systemname" in name_low:
                return f"{fake.company()} Information System v{random.randint(1,5)}"
            return fake.sentence(nb_words=random.randint(8, 20))

        if rt == RepresentationTerm.NAME:
            if "place" in name_low:
                return fake.city()
            if "region" in name_low:
                return fake.state()
            if "creator" in name_low or "author" in name_low or "agent" in name_low:
                return f"{fake.name()}, {random.choice(NATO_ORGS)}"
            return fake.name()

        if rt == RepresentationTerm.TIME_INTERVAL:
            return _time_interval()

        if rt == RepresentationTerm.QUANTITY:
            if "byte" in name_low:
                return str(random.randint(1024, 10 * 1024 * 1024))
            if "resolution" in name_low or "spatial" in name_low:
                return str(random.randint(10, 1000))
            if "extent" in name_low:
                return str(random.randint(1, 500))
            return str(round(random.uniform(1.0, 1000.0), 2))

        if rt == RepresentationTerm.BOOLEAN or rt == RepresentationTerm.INDICATOR:
            return random.choice(["true", "false"])

        if rt == RepresentationTerm.CLASS:
            return f"[{field.name} structure — see standard documentation]"

        if rt == RepresentationTerm.ENUM:
            if field.values:
                options = [v.strip() for v in field.values.replace("|", ",").split(",") if v.strip()]
                if options:
                    return random.choice(options)
            return "Low"

        # Fallback
        return fake.word()

    def generate_for_standard(self, std: MetadataStandard,
                               include_optional: bool = True,
                               include_conditional: bool = True) -> Dict[str, Any]:
        """Generate a full example metadata record for the given standard."""
        result: Dict[str, Any] = {}

        for field_name, field_def in std.fields.items():
            ob = field_def.obligation
            if ob == Obligation.MANDATORY:
                result[field_name] = self.generate_value(field_def, std.id)
            elif ob == Obligation.CONDITIONAL and include_conditional:
                result[field_name] = self.generate_value(field_def, std.id)
            elif ob == Obligation.OPTIONAL and include_optional:
                # Include ~60% of optional fields to keep examples manageable
                if random.random() < 0.6:
                    result[field_name] = self.generate_value(field_def, std.id)

        return result


def to_xml(metadata: Dict[str, Any], standard) -> str:
    """Convert metadata dict to XML using the standard's namespace."""
    ns = getattr(standard, 'namespace', '')
    prefix_map = {}
    if ns:
        prefix_map[None] = ns

    # Build root element
    if ns:
        root_tag = f"{{{ns}}}metadata"
    else:
        root_tag = "metadata"

    root = ET.Element(root_tag)
    if ns:
        root.set("xmlns", ns)

    for key, val in metadata.items():
        if key.startswith("@"):
            continue
        # Handle namespace-prefixed keys (DCAT-AP style)
        clean_key = key.replace(":", "_").replace(".", "_")
        child = ET.SubElement(root, clean_key)
        if isinstance(val, dict):
            for dk, dv in val.items():
                sub = ET.SubElement(child, str(dk))
                sub.text = str(dv)
        elif isinstance(val, list):
            child.text = str(val[0]) if val else ""
            for extra in val[1:]:
                extra_child = ET.SubElement(root, clean_key)
                extra_child.text = str(extra)
        else:
            child.text = str(val) if val is not None else ""

    raw = ET.tostring(root, encoding="unicode", xml_declaration=False)
    try:
        pretty = parseString(f'<?xml version="1.0"?>{raw}').toprettyxml(indent="  ")
        # Remove the XML declaration added by toprettyxml (we add our own)
        lines = pretty.split("\n")
        if lines[0].startswith("<?xml"):
            lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
        return "\n".join(lines)
    except Exception:
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{raw}'
