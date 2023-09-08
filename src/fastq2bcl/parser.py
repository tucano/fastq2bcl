import re
import logging

_logger = logging.getLogger(__name__)


def parse_seqdesc_fields(txt):
    """
    Parse the SeqIO description field using named groups.

    <instrument>      Instrument ID.
    <run_number>      Run number on instrument.
    <flowcell_id>     Flowcell ID
    <lane>            Lane number
    <tile>            Tile number
    <x_pos>           Position X of cluster
    <y_pos>           Position Y of cluster
    <UMI>             Optional, appears when UMI is specified in sample sheet. UMI sequences for Read 1 and Read 2, seperated by a plus [+].
    <read>            Read number. 1 can be single read or Read 2 of paired-end.
    <is_filtered>     Y if the read is filtered (did not pass), N otherwise.
    <control_number>  0 when none of the control bits are on, otherwise it is an even number.
                      On HiSeq X and NextSeq systems, control specification is not performed and this number is always 0.
    <index>           Index of the read.

    References:
        https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/FileFormat_FASTQ-files_swBS.htm
    """
    regxp = r"(?P<instrument>[A-Za-z0-9_]+):(?P<run_number>[0-9]+):(?P<flowcell_id>[A-Za-z0-9-]+):(?P<lane>[0-9]+):(?P<tile>[0-9]+):?(?P<x_pos>[0-9]+)?:?(?P<y_pos>[0-9]+)?:?(?P<UMI>[A-Z-]+)?\s(?P<read>[0-9]+):(?P<is_filtered>[YN]+):(?P<control_number>[0-9]+):(?P<index>[0-9A-Z+]+)"

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
        if fields[key]:
            _logger.info(f"Found key {key} with value {fields[key]}")
        else:
            _logger.debug(f"Key {key} is NoneType!")
            if key == "UMI" and fields[key] == None:
                _logger.info(f"Found None value for optional key {key}. This is ok.")
            else:
                raise ValueError(f"Requested Key {key} not Found")

    return fields
