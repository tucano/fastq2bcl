import logging
import struct
from pathlib import Path

_logger = logging.getLogger(__name__)


def write_run_info_xml(
    rundir,
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
    xmlout = Path.joinpath(rundir, "RunInfo.xml")
    xmlout.parent.mkdir(exist_ok=True, parents=True)
    with open(xmlout, "wt") as f_out:
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


def write_filter(rundir, cluster_count):
    """
    Filter:
        The filter files can be found in the BaseCalls directory. The filter file specifies whether a cluster passed filters.
        Filter files are generated at cycle 26 using 25 cycles of data. For each tile, one filter file is generated.
        Location: Data/Intensities/BaseCalls/L001
        File format: s_[lane]_[tile].filter

        The format is described below

        - Bytes 0-3 Zero value (for backwards compatibility)
        - Bytes 4-7 Filter format version number
        - Bytes 8-11 Number of clusters
        - Bytes 12-(N+11) Where N is the cluster number
          unsigned 8-bits integer Bit 0 is pass or failed filter


    Example:
    bytes([0, 0, 0, 0])              -----> prefix 0
    bytes([3, 0, 0, 0])              -----> version 3
    struct.pack("<I", cluster_count) -----> number of cluster in little endian unsigned int
    bytes([1]*cluster_count)         -----> For each cluster an unsigned 8-bits integer
                                            Where Bit 0 is pass or failed filter

    In other words I can use bytes([1]) to set something like: 00000001 where Bit 0 is set.

    Then:
        1 == PASS FILTER
        0 == NO PASS FILTER

    In hexdump:
    BYTES 0-3      BYTES 4-7      BYTES 8-11     BYTES 12-14
    00 00 00 00    03 00 00 00    03 00 00 00    01 01 01

    At bytes 8-11 I have 3 clusters and each cluster is represented by a an unsigned 8-bit integer.

    References:
        https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq_letterbooklet_15038058brpmi.pdf
        http://support-docs.illumina.com/IN/NovaSeq6000Dx_HTML/Content/IN/NovaSeq/SequencingOutputFiles_fNV.htm
        https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/FileFormat_FASTQ-files_swBS.htm
        https://docs.python.org/3/library/struct.html
        https://docs.python.org/3/library/struct.html#format-characters
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
    Write control file:

        The X.control files are binary files containing control results

         The format is described below

        - Bytes 0-3 Zero value (for backwards compatibility)
        - Bytes 4-7 Format version number
        - Bytes 8-11 Number of clusters
        - Bytes 12-(2xN+11) Where N is the cluster number
          The bits are used as follows:
          Bit 0: always empty (0)
          Bit 1: was the read identified as a control?
          Bit 2: was the match ambiguous?
          Bit 3: did the read match the phiX tag?
          Bit 4: did the read align to match the phiX tag?
          Bit 5: did the read match the control index sequence?
          Bits 6,7: reserved for future use
          Bits 8..15: the report key for the matched record in the controls.fasta file (specified by the REPORT_KEY metadata)

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

    Positions is a List of x and y values

    The BCL to FASTQ converter can use different types of position files and will expect a type based on the version of RTA used:

    locs: the locs files can be found in the Intensities/L<lane> directories

    From mkdata.sh of bcl2fastq

    printf '0: 010000000000803f' | xxd -r -g0 > "$locs_filename"
    printf '0: %.8x' $clusters_count | sed -E 's/0: (..)(..)(..)(..)/0: \4\3\2\1/' | xxd -r -g0 >> "$locs_filename"

    So with 1 cluster count should be
    01 00 00 00    00 00 80 3f
    01 00 00 00    CDCC8C3F 9A99993F

    Source of this is bcl2fastq/src/cxx/lib/data

    struct Record
    {
        /// \brief X-coordinate.
        float x_;
        /// \brief y-coordinate.
        float y_;
    }

    """
    path = Path(outdir) / "Data/Intensities/L001/s_1_1101.locs"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as f_out:
        f_out.write(bytes([1, 0, 0, 0, 0, 0, 0x80, 0x3F]))
        f_out.write(struct.pack("<I", len(positions)))
        for position in positions:
            f_out.write(encode_loc_bytes(position[0], position[1]))


def encode_loc_bytes(x_pos, y_pos):
    x_bytes = struct.pack("<f", (int(x_pos) - 1000) / 10)
    y_bytes = struct.pack("<f", (int(y_pos) - 1000) / 10)
    return x_bytes + y_bytes
