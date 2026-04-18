"""
Standards Registry — central registry of all supported metadata standards.
"""
from standards.nato.adatp5636 import ADatP5636Standard
from standards.nato.adatp4774_4778 import ADatP4774Standard, ADatP4778Standard
from standards.eu.dublin_core import DublinCoreStandard
from standards.eu.dcat_ap import DCATAPStandard
from standards.eu.dcat_ap_se import DCATAPSEStandard
from standards.eu.inspire import INSPIREStandard
from standards.iso.iso19115 import ISO19115Standard
from standards.iso.iso23081 import ISO23081Standard
from standards.nist.sp800 import NISTSP80060Standard, NISTIR8112Standard


# Instantiate each standard once
_STANDARDS = [
    ADatP5636Standard(),
    ADatP4774Standard(),
    ADatP4778Standard(),
    DublinCoreStandard(),
    DCATAPStandard(),
    DCATAPSEStandard(),
    INSPIREStandard(),
    ISO19115Standard(),
    ISO23081Standard(),
    NISTSP80060Standard(),
    NISTIR8112Standard(),
]

_REGISTRY = {s.id: s for s in _STANDARDS}


def get_all_standards():
    """Return all registered MetadataStandard instances."""
    return list(_REGISTRY.values())


def get_standard(standard_id: str):
    """Return a standard by its ID or None."""
    return _REGISTRY.get(standard_id)


def list_standard_ids():
    """Return a list of all registered standard IDs."""
    return list(_REGISTRY.keys())
