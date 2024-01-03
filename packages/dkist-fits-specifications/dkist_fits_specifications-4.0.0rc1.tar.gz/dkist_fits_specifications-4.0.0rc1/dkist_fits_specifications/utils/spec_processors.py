import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable
from dataclasses import dataclass

logger = logging.getLogger(__name__)
from dkist_fits_specifications.utils import frozendict, schema_type_hint

# Defined as a random string so we don't accidentally confuse ourselves in tests where we want to
# use a fake instrument name
_NOT_A_DKIST_INSTRUMENT = "671976988c6c4bf78836401062757b16"


class ConditionalRequirement(ABC):
    """
    A class definition for capturing a single type of conditional requiredness.

    These classes are instantiated with a header and then can be used to check the requiredness of any key in the schema
    """

    def __init__(self, header: dict[str:Any]):
        self.header = header

    @abstractmethod
    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Given the schema for a single key, check if this key needs to be required."""
        pass


class InstrumentRequired(ConditionalRequirement):
    """
    Conditional requirement that makes all keys related to the headers "INSTRUME" required.

    spec_field:
      instrument_required: str
    """

    def __init__(self, header: dict[str, Any]):
        super().__init__(header=header)
        self.instrument = self.header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()

    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Check if the required instrument matches the instrument in the header."""
        # "False" is importantly different than _NOT_A_DKIST_INSTRUMENT
        return spec_fields.get("instrument_required", "False").casefold() == self.instrument


def _vbi_is_polarimetric(header: dict[str, Any]) -> False:
    """VBI is *always* non-polarimetric."""
    return False


def _visp_is_polarimetric(header: dict[str, Any]) -> bool:
    """Check ViSP polarimeter mode to see if dataset was polarimetric."""
    return header["VSPPOLMD"] == "observe_polarimetric"


def _cryonirsp_is_polarimetric(header: dict[str, Any]) -> bool:
    """
    Check Cryo-NIRSP headers to see if dataset was polarimetric.

    Polarimetric if there are more than 1 modstate and the modulator was in a "moving" mode.
    """
    return header["CNMODNST"] > 1 and header["CNSPINMD"] in ["Continuous", "Stepped"]


def _dlnirsp_is_polarimetric(header: dict[str, Any]) -> bool:
    """Check DL-NIRSP polarimeter mode to see if dataset was polarimetric."""
    return header["DLPOLMD"] == "Full Stokes"


def _fallback_is_polarimetric(header: dict[str, Any]) -> False:
    """
    One-stop function for when we can't figure out what to do with a particular instrument.

    Logs a warning and returns False.
    """
    instrument = header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()
    logger.warning(
        f"Checking polarimetric requiredness for instrument {instrument} is not currently supported."
    )
    return False


class PolarimetricRequired(ConditionalRequirement):

    """
    Conditional requirement that makes keys required if the dataset represents polarimetric data.

    spec_field:
      polarimetric_required: bool
    """

    instrument_to_polarimetric_func_mapping = {
        "vbi": _vbi_is_polarimetric,
        "visp": _visp_is_polarimetric,
        "cryo-nirsp": _cryonirsp_is_polarimetric,
        "dl-nirsp": _dlnirsp_is_polarimetric,
    }

    def __init__(self, header: dict[str, Any]):
        super().__init__(header=header)
        instrument = self.header.get("INSTRUME", _NOT_A_DKIST_INSTRUMENT).casefold()

        is_polarimetric_function = self.instrument_to_polarimetric_func_mapping.get(
            instrument, _fallback_is_polarimetric
        )

        try:
            self.is_polarimetric = is_polarimetric_function(self.header)
        except Exception as e:
            logger.warning(
                f"Error encountered when checking polarimetric requiredness. Error was:\n{e}"
            )
            self.is_polarimetric = False

    def check_requiredness(self, spec_fields: frozendict[str, Any]) -> bool:
        """Check if the header was from a polarimetric dataset and the key is `polarimetric_required`."""
        return self.is_polarimetric and spec_fields.get("polarimetric_required", False)


def update_schema_requiredness(
    schema: schema_type_hint, requirements: list[ConditionalRequirement]
) -> dict[str, frozendict[str, Any]]:
    """
    Modify a schema's `required` values based on conditional requirements.

    If ANY of the conditional requiredness requirements are met then the key is set to "required."
    """
    updated_schema = dict()
    for fits_keyword_name, spec_fields in schema.items():
        thawed_fields = dict(spec_fields)

        if any([requirement.check_requiredness(spec_fields) for requirement in requirements]):
            thawed_fields["required"] = True

        updated_schema[fits_keyword_name] = frozendict(thawed_fields)

    return updated_schema


@dataclass
class ExpansionIndex:
    """
    A class for defining a FITS schema expansion.

    index: the string to be substituted, omitting the surrounding '<', '>'
    size: how many (zero-padded) characters to use for the substituted integer
    values: the iterable of integers to be used as substitution for the index

    Example:
        Using the expansion of:
        ExpansionIndex(index="a", size=3, values=range(1, 6))

        on the keyword 'KEY<a>' would produce the expanded set of keys:
        ['KEY001', 'KEY002', 'KEY003', 'KEY004', 'KEY005']

    """

    index: str
    values: Iterable
    size: int = None

    def __post_init__(self):
        if len(str(max(self.values))) > self.size:
            raise ValueError(
                f"The maximum expansion value ({max(self.values)}) does not fit within the prescribed size ({self.size})."
            )

    def _expanded_keys(self, key: str) -> list[str]:
        """Generate schema entries for expanded keys."""
        return [key.replace(f"<{self.index}>", str(i).zfill(self.size)) for i in self.values]

    def generate(self, keys: list[str]) -> list[str]:
        """Generate the new keys to be added."""
        return_keys = []
        for key in keys:
            if f"<{self.index}>" in key:
                return_keys.extend(self._expanded_keys(key=key))
        long_keys = [k for k in return_keys if len(k) > 8]
        if long_keys:
            raise ValueError(
                f"FITS keywords cannot be more than 8 characters in length. {long_keys} are too long."
            )
        return return_keys


def expand_schema(
    schema: schema_type_hint, expansions: list[ExpansionIndex]
) -> dict[str, frozendict[str, Any]]:
    """Perform a schema expansion given a schema and a list of ExpansionIndexes to apply."""
    expanded_schema = dict()
    for fits_keyword_name, spec_fields in schema.items():
        if "<" not in fits_keyword_name:
            expanded_schema.update({fits_keyword_name: spec_fields})
        else:
            expanded_fits_keywords = [fits_keyword_name]
            for expansion in expansions:
                expanded_fits_keywords.extend(expansion.generate(keys=expanded_fits_keywords))
            expanded_schema.update({k: spec_fields for k in expanded_fits_keywords if "<" not in k})
    return expanded_schema
