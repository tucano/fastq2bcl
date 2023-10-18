import logging
import struct
from pathlib import Path

_logger = logging.getLogger(__name__)


def write_run_info_xml(rundir, run_id, run_number, flowcell_id, instrument, mask):
    """
    Write RunInfo.xml
    """

    runinfo = generate_run_info_xml(run_id, run_number, flowcell_id, instrument, mask)
    _logger.info(f"RunInfo.xml:\n{runinfo}")

    # Create directory and write file
    xmlout = Path.joinpath(rundir, "RunInfo.xml")
    xmlout.parent.mkdir(exist_ok=True, parents=True)
    with open(xmlout, "wt") as f_out:
        f_out.write(runinfo)

    return runinfo


def generate_run_info_xml(run_id, run_number, flowcell_id, instrument, mask):
    """
    Generate a valid Runinfo xml file.
    """

    # check mask and write mask
    xml_mask = ""
    for m in mask:
        xml_mask += f"""<Read NumCycles="{m['cycles']}" Number="{m['id']}" IsIndexedRead="{m['index']}" />"""

    xml = f"""<?xml version="1.0"?>
<RunInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2">
    <Run Id="{run_id}" Number="{run_number}">
        <Flowcell>{flowcell_id}</Flowcell>
        <Instrument>{instrument}</Instrument>
        <Date>YYMMDD</Date>
        <Reads>
            { xml_mask }
        </Reads>
        <FlowcellLayout LaneCount="1" SurfaceCount="1" SwathCount="1" TileCount="1" />
    </Run>
</RunInfo>
"""
    return xml


def write_filter(rundir, cluster_count):
    """
    Write filter
    """
    path = rundir / "Data/Intensities/BaseCalls/L001/s_1_1101.filter"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as f_out:
        f_out.write(bytes([0, 0, 0, 0]))
        f_out.write(bytes([3, 0, 0, 0]))
        f_out.write(struct.pack("<I", cluster_count))
        f_out.write(bytes([1] * cluster_count))


def write_control(rundir, cluster_count):
    """
    Write control file
    """
    path = rundir / "Data/Intensities/BaseCalls/L001/s_1_1101.control"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as f_out:
        f_out.write(bytes([0, 0, 0, 0]))  # "Zero value (for backwards compatibility)"
        f_out.write(bytes([2, 0, 0, 0]))  # "Format version number"
        f_out.write(struct.pack("<I", cluster_count))  # "Number of clusters"
        f_out.write(bytes([0, 0] * cluster_count))  # two bytes for each cluster


def write_locs(outdir, positions):
    """
    Write locations.

    Args:
        Positions (List(tuple)): is a List of tuple with x and y values
    """
    # From mkdata.sh of bcl2fastq

    # printf '0: 010000000000803f' | xxd -r -g0 > "$locs_filename"
    # printf '0: %.8x' $clusters_count | sed -E 's/0: (..)(..)(..)(..)/0: \4\3\2\1/' | xxd -r -g0 >> "$locs_filename"

    # So with 1 cluster count should be
    # 01 00 00 00    00 00 80 3f
    # 01 00 00 00    CDCC8C3F 9A99993F

    # Source of this is bcl2fastq/src/cxx/lib/data

    # struct Record
    # {
    #     /// \brief X-coordinate.
    #     float x_;
    #     /// \brief y-coordinate.
    #     float y_;
    # }
    path = Path(outdir) / "Data/Intensities/L001/s_1_1101.locs"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as f_out:
        f_out.write(bytes([1, 0, 0, 0, 0, 0, 0x80, 0x3F]))
        f_out.write(struct.pack("<I", len(positions)))
        for position in positions:
            f_out.write(encode_loc_bytes(position[0], position[1]))


def encode_loc_bytes(x_pos, y_pos):
    """
    Encode x and y positon.
    FIXME this is not the correct formul according to the bcl2fastq source code.
    """
    x_bytes = struct.pack("<f", (int(x_pos) - 1000) / 10)
    y_bytes = struct.pack("<f", (int(y_pos) - 1000) / 10)
    return x_bytes + y_bytes


def encode_cluster_byte(base, qual):
    """
    Encode cluster byte.
    Bits 0-1 are the bases, respectively [A, C, G, T]
    for [0, 1, 2, 3]:
    bits 2-7 are shifted by two bits and contain the quality score.
    All bits 0 in a byte is reserved for no-call.
    """
    if base == "N":
        return bytes([0])  # no call
    qual = qual << 2
    base = ["A", "C", "G", "T"].index(base)
    return bytes([qual | base])


def init_bcl_and_write_cluster_counts(cycledir, cluster_count, filename="s_1_1101.bcl"):
    """
    Create bcl file and write cluster count
    """
    with open(cycledir / filename, "wb") as f_out:
        f_out.write(struct.pack("<I", cluster_count))


def write_cycle(context, progress, task_id):
    """
    Write a cycle file with a thread. with progress, task_id and exit event
    context: tuple with (cycle, cluster_count, outdir, data)
    data: tuple (base, quality) for a cluster
    """
    cycle, cluster_count, outdir, data = context
    cycledir = get_cycle_dir(outdir, cycle)
    _logger.info(
        f"Writing {cluster_count} clusters for cycle: {cycle+1} to dir {cycledir}"
    )

    init_bcl_and_write_cluster_counts(cycledir, cluster_count)

    # write data
    sequences_written = 0
    for base, quality in data:
        _logger.debug(f"Appending seq: {base}")
        filename = cycledir / "s_1_1101.bcl"
        append_data_to_bcl(base, quality, filename)
        sequences_written += 1
        progress[task_id] = {"progress": sequences_written, "total": len(data)}

    # write stats
    write_stat_file(cycledir / "s_1_1101.stats")


def write_bcl_and_stats(cycle, cluster_count, outdir, sequences):
    """
    Single process mode to write bcls
    """
    cycledir = get_cycle_dir(outdir, cycle)
    filename = cycledir / "s_1_1101.bcl"
    init_bcl_and_write_cluster_counts(cycledir, cluster_count)
    # write data
    for basecalls, qualscores in sequences:
        if cycle >= len(basecalls):
            _logger.info(f"Sequence is shorter than expected, adding N")
            append_data_to_bcl("N", 0, filename)
        else:
            append_data_to_bcl(basecalls[cycle], qualscores[cycle], filename)
            _logger.debug(
                f"Appending basecall: {basecalls[cycle]} to bcl for cycle {cycle+1} lenght sequence {len(basecalls)}"
            )

    # write stats
    write_stat_file(cycledir / "s_1_1101.stats")


def write_stat_file(filename):
    with open(filename, "wb") as f_out:
        # can I get away with this?
        f_out.write(bytes([0] * 108))


def append_data_to_bcl(base, quality, filename):
    bcl_byte = encode_cluster_byte(base, quality)
    with open(filename, "ab") as f_out:
        f_out.write(bcl_byte)


def get_cycle_dir(outdir, cycle, lane="L001"):
    cycledir = outdir / f"Data/Intensities/BaseCalls/{lane}/C{cycle+1}.1"
    cycledir.mkdir(exist_ok=True, parents=True)
    return cycledir
