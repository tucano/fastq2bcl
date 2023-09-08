import pytest

from fastq2bcl.parser import parse_seqdesc_fields, validate_fields

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

expected_full = {
    "instrument": "M11111",
    "run_number": "222",
    "flowcell_id": "000000000-K9H97",
    "lane": "1",
    "tile": "1101",
    "x_pos": "19304",
    "y_pos": "1328",
    "UMI": "AAACGGG",
    "read": "1",
    "is_filtered": "N",
    "control_number": "0",
    "index": "1",
}

expected_no_umi = {
    "instrument": "M11111",
    "run_number": "222",
    "flowcell_id": "000000000-K9H97",
    "lane": "1",
    "tile": "1101",
    "x_pos": "19304",
    "y_pos": "1328",
    "UMI": None,
    "read": "1",
    "is_filtered": "N",
    "control_number": "0",
    "index": "1",
}

expected_missing = {
    "instrument": "M11111",
    "run_number": "222",
    "flowcell_id": "000000000-K9H97",
    "lane": "1",
    "tile": "1101",
    "x_pos": None,
    "y_pos": "1328",
    "UMI": None,
    "read": "1",
    "is_filtered": "N",
    "control_number": "0",
    "index": "1",
}


def test_parse_seqdesc_fields():
    """SeqIO description parser Tests"""
    assert (
        parse_seqdesc_fields("M11111:222:000000000-K9H97:1:1101:19304:1328 1:N:0:1")
        == expected_no_umi
    )
    assert (
        parse_seqdesc_fields(
            "M11111:222:000000000-K9H97:1:1101:19304:1328:AAACGGG 1:N:0:1"
        )
        == expected_full
    )
    with pytest.raises(ValueError):
        parse_seqdesc_fields("AAA:1:2")
        parse_seqdesc_fields("M11111:222:000000000-K9H97:1:1101:::AAACGGG 1:N:0:1")


def test_validate_fields():
    """SeqIO fields validationTests"""
    assert validate_fields(expected_full) == expected_full
    assert validate_fields(expected_no_umi) == expected_no_umi
    with pytest.raises(ValueError):
        validate_fields(expected_missing)
