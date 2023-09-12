import re
import logging

_logger = logging.getLogger(__name__)


def parse_seqdesc_fields(txt):
    """
    Parse the SeqIO description field using named groups.
    """
    regxp = re.compile(
        r"(?P<instrument>[A-Za-z0-9_]+):"
        + r"(?P<run_number>[0-9]+):"
        + r"(?P<flowcell_id>[A-Za-z0-9-]+):"
        + r"(?P<lane>[0-9]+):"
        + r"(?P<tile>[0-9]+):?"
        + r"(?P<x_pos>[0-9]+)?:?"
        + r"(?P<y_pos>[0-9]+)?:?"
        + r"(?P<UMI>[A-Z-]+)?"
        + r"\s"
        + r"(?P<read>[0-9]+):"
        + r"(?P<is_filtered>[YN]+):"
        + r"(?P<control_number>[0-9]+):"
        + r"(?P<index>[0-9A-Z+]+)"
    )

    match = re.match(regxp, txt)
    if not match:
        raise ValueError(f"Sequence identifier not recognized: {txt}")

    return validate_fields(match.groupdict())


def validate_fields(fields):
    """
    Validate the fields extracted from SeqIO description
    """
    valid_keys = [
        "instrument",
        "run_number",
        "flowcell_id",
        "lane",
        "tile",
        "x_pos",
        "y_pos",
        "UMI",
        "read",
        "is_filtered",
        "control_number",
        "index",
    ]
    _logger.info(f"Verifying keys ...")

    for key in valid_keys:
        if not fields[key]:
            if key == "UMI" and fields[key] == None:
                _logger.info(f"Found None value for optional key {key}. This is ok.")
            else:
                raise ValueError(f"Requested Key {key} not Found in fastq description")

    return fields
