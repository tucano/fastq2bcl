import pytest
from pathlib import Path

from fastq2bcl.writer import write_run_info_xml, generate_run_info_xml

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


def test_generate_run_info_xml():
    assert (
        generate_run_info_xml(
            "YYMMDD_M11111_0222_000000000-K9H97",
            222,
            "000000000-K9H97",
            "M11111",
            110,
            None,
            None,
            None,
        )
        == excepted_xml
    )


def test_write_run_info_xml(tmpdir):
    xmlout = Path(tmpdir.join("Runinfo.xml"))
    write_run_info_xml(
        xmlout,
        "YYMMDD_M11111_0222_000000000-K9H97",
        222,
        "000000000-K9H97",
        "M11111",
        110,
    )
    assert xmlout.read_text() == excepted_xml
    pass
