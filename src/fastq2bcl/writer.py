import logging

_logger = logging.getLogger(__name__)


def write_run_info_xml(
    xml_out,
    run_id,
    run_number,
    flowcell_id,
    instrument,
    cycles_r1,
    cycles_i1=None,
    cycles_r2=None,
    cycles_i2=None,
):
    """
    Write RunInfo.xml
    """

    runinfo = generate_run_info_xml(
        run_id,
        run_number,
        flowcell_id,
        instrument,
        cycles_r1,
        cycles_i1,
        cycles_r2,
        cycles_i2,
    )
    _logger.info(f"RunInfo.xml:\n{runinfo}")

    # Create directory and write file
    xml_out.parent.mkdir(exist_ok=True, parents=True)
    with open(xml_out, "wt") as f_out:
        f_out.write(runinfo)


def generate_run_info_xml(
    run_id,
    run_number,
    flowcell_id,
    instrument,
    cycles_r1,
    cycles_i1,
    cycles_r2,
    cycles_i2,
):
    """
    Generate a valid Runindo xml file.
    """
    return f"""<?xml version="1.0"?>
<RunInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2">
    <Run Id="{run_id}" Number="{run_number}">
        <Flowcell>{flowcell_id}</Flowcell>
        <Instrument>{instrument}</Instrument>
        <Date>YYMMDD</Date>
        <Reads>
            <Read NumCycles="{cycles_r1}" Number="1" IsIndexedRead="N" />
        </Reads>
        <FlowcellLayout LaneCount="1" SurfaceCount="1" SwathCount="1" TileCount="1" />
    </Run>
</RunInfo>
"""
