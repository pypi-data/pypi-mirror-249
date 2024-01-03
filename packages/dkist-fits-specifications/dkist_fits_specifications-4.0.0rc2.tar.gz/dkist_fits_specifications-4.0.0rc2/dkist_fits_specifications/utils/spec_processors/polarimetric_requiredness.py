import logging
from typing import Any

from dkist_fits_specifications.utils import frozendict
from dkist_fits_specifications.utils.spec_processors.requiredness_base import (
    _NOT_A_DKIST_INSTRUMENT,
    ConditionalRequirement,
)

logger = logging.getLogger(__name__)


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
