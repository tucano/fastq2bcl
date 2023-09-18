import pytest
import struct

from fastq2bcl.writer import (
    write_run_info_xml,
    generate_run_info_xml,
    write_filter,
    write_control,
    encode_loc_bytes,
    write_locs,
    encode_cluster_byte,
    write_bcls_and_stats,
)

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

excepted_xml = """<?xml version="1.0"?>
<RunInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2">
    <Run Id="YYMMDD_M11111_0222_000000000-K9H97" Number="222">
        <Flowcell>000000000-K9H97</Flowcell>
        <Instrument>M11111</Instrument>
        <Date>YYMMDD</Date>
        <Reads>
            <Read NumCycles="110" Number="1" IsIndexedRead="N" />
        </Reads>
        <FlowcellLayout LaneCount="1" SurfaceCount="1" SwathCount="1" TileCount="1" />
    </Run>
</RunInfo>
"""

expected_filter = b"\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x01"
expected_control = b"\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00"
expected_locs = (
    b"\x01\x00\x00\x00\x00\x00\x80?\x01\x00\x00\x00\xcd\xcc\xc7\xc2\xcd\xcc\xc7\xc2"
)
expected_bcl = b"\x01\x00\x00\x00\x05"
expected_stats = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

test_sequences = [(["C"], [1])]

test_mask = [{"cycles": 110, "index": "N", "id": 1}]


def test_generate_run_info_xml():
    assert (
        generate_run_info_xml(
            "YYMMDD_M11111_0222_000000000-K9H97",
            222,
            "000000000-K9H97",
            "M11111",
            test_mask,
        )
        == excepted_xml
    )


def test_write_run_info_xml(tmp_path):
    xmlout = tmp_path / "RunInfo.xml"
    write_run_info_xml(
        tmp_path,
        "YYMMDD_M11111_0222_000000000-K9H97",
        222,
        "000000000-K9H97",
        "M11111",
        test_mask,
    )
    assert xmlout.read_text() == excepted_xml


def test_encode_loc_bytes():
    assert encode_loc_bytes(1, 1) == b"\xcd\xcc\xc7\xc2\xcd\xcc\xc7\xc2"


def test_write_filter(tmp_path):
    binaryout = tmp_path / "Data/Intensities/BaseCalls/L001/s_1_1101.filter"
    write_filter(tmp_path, 1)
    with open(binaryout, "rb") as binfile:
        binary_content = binfile.read()
        assert binary_content == expected_filter


def test_write_control(tmp_path):
    binaryout = tmp_path / "Data/Intensities/BaseCalls/L001/s_1_1101.control"
    write_control(tmp_path, 1)
    with open(binaryout, "rb") as binfile:
        binary_content = binfile.read()
        assert binary_content == expected_control


def test_write_locs(tmp_path):
    binaryout = tmp_path / "Data/Intensities/L001/s_1_1101.locs"
    write_locs(tmp_path, [(1, 1)])
    with open(binaryout, "rb") as binfile:
        binary_content = binfile.read()
        assert binary_content == expected_locs


def test_encode_cluster_byte():
    assert encode_cluster_byte("A", 1) == b"\x04"


def test_encode_cluster_byte_null():
    assert encode_cluster_byte("N", 1) == b"\x00"


def test_write_bcls_and_stats(tmp_path):
    binaryout = tmp_path / "Data/Intensities/BaseCalls/L001/C1.1/s_1_1101.bcl"
    statsout = tmp_path / "Data/Intensities/BaseCalls/L001/C1.1/s_1_1101.stats"
    write_bcls_and_stats(tmp_path, test_sequences)
    with open(binaryout, "rb") as binfile:
        binary_content = binfile.read()
        assert binary_content == expected_bcl
    with open(statsout, "rb") as binfile:
        binary_content = binfile.read()
        assert binary_content == expected_stats
