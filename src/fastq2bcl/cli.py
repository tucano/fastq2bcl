"""
CLI for fastq2bcl app

``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
        fastq2bcl = fastq2bcl.cli:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fastq2bcl`` inside your current environment.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import os
import re
from pathlib import Path
from rich import print, pretty

from fastq2bcl import __version__
from fastq2bcl.parser import parse_seqdesc_fields
from fastq2bcl.reader import read_first_record, read_fastq_files, get_mask_from_files
from fastq2bcl.writer import (
    write_run_info_xml,
    write_filter,
    write_control,
    write_locs,
    write_bcls_and_stats,
)

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from fastq2bcl.skeleton import fib`,
# when using this Python module as a library.


def fastq2bcl(outdir, r1, r2=None, i1=None, i2=None, mask_string=None):
    """fastq2bcl function call

    :param outdir: output directory to create run flowcell fake dir
    :param r1: R1 fastq.gz
    :param r2: R2 fastq.gz
    :param i1: I1 fastq.gz
    :param i2: I2 fastq.gz

    Content of returned tuple:

    rundir: final absolute path od created rundir
    run_id: generated mock run_id
    seq_fields: fields parsed and validated from first R1 record
    mask_string: mask used to generate RunInfo.xml

    :rtype: tuple
    """

    # First validate outdir
    outdir = Path(outdir).absolute()
    assert outdir.is_dir()
    assert os.access(outdir, os.W_OK)

    _logger.info(f"Output directory: {outdir}")

    # Validate R1 and extract first read
    r1 = Path(r1)
    assert r1.is_file()
    first_record = read_first_record(r1)
    seqdesc_fields = parse_seqdesc_fields(first_record.description)
    _logger.info(f"first record seqdesc fields: {seqdesc_fields}")

    # RUNDIR
    run_id = mock_run_id(seqdesc_fields)
    rundir = Path.joinpath(outdir, run_id)

    print(f"[green]RUNDIR[/green]: {rundir}")

    # MASK STRING
    if not mask_string:
        # get cycles string from files
        mask_string = get_mask_from_files(r1, r2, i1, i2)
        _logger.info(f"mask string from files: {mask_string}")

    print(f"[green]MASK[/green]: {mask_string}")

    # READ DATA {"sequences": sequences, "positions": positions}
    sequences, positions = read_fastq_files(r1, r2, i1, i2)

    # SET MASK FROM STRING
    mask = set_mask(mask_string)

    # WRITE RUN INFO
    _logger.info(f"Writing RunInfo.mxl to dir: {rundir}")
    run_info = write_run_info_xml(
        rundir,
        run_id,
        seqdesc_fields["run_number"],
        seqdesc_fields["flowcell_id"],
        seqdesc_fields["instrument"],
        mask,
    )

    print(f"[green]RunInfo.xml:[/green]:\n", run_info)

    # WRITE FILTER
    print(f"[bold magenta]Writing filter file [/bold magenta]")
    _logger.info(f"Writing filter file to dir: {rundir}")
    write_filter(rundir, len(sequences[0]))

    # WRITE CONTROL
    print(f"[bold magenta]Writing control file [/bold magenta]")
    _logger.info(f"Writing control file to dir: {rundir}")
    write_control(rundir, len(sequences[0]))

    # WRITE LOCATIONS
    print(f"[bold magenta]Writing location file [/bold magenta]")
    _logger.info(f"Writing {len(positions)} locations to dir: {rundir}")
    write_locs(rundir, positions)

    # WRITE BCL AND STATS
    print(f"[bold magenta]Writing cycles files [/bold magenta]")
    _logger.info(f"Writing {len(sequences)} sequences bcl and stats to dir: {rundir}")

    write_bcls_and_stats(rundir, sequences)

    return (run_id, rundir, seqdesc_fields, mask_string)


def mock_run_id(fields):
    """
    Mock the run directory id and Path
    """
    run_id = (
        "YYMMDD_"
        + fields["instrument"]
        + "_"
        + fields["run_number"].zfill(4)
        + "_"
        + fields["flowcell_id"]
    )
    return run_id


def set_mask(mask_string):
    if mask_string:
        mask = []
        regexp_mask = r"([0-9]+[NY])([0-9]+[NY])?([0-9]+[NY])?([0-9]+[NY])?"
        m = re.match(regexp_mask, mask_string)
        if not m:
            raise ValueError(f"Incorrect mask parse: {mask_string}")
        reads = [g for g in m.groups() if g != None]
        for g_idx in range(len(reads)):
            read = re.match(r"([0-9]+)([YN])", reads[g_idx])
            mask.append(
                {
                    "cycles": read.groups()[0],
                    "index": read.groups()[1],
                    "id": str(g_idx + 1),
                }
            )
        return mask
    else:
        raise ValueError(f"Incorrect mask string: {mask_string}")


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Convert fastq.gz reads and metadata in a bcl2fastq-able run directory"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"fastq2bcl {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-m", "--mask", dest="mask", help="define mask in format 110N10Y10Y110N"
    )
    parser.add_argument(dest="r1", help="fastq.gz with R1 reads", metavar="R1")
    parser.add_argument(
        dest="r2", help="fastq.gz with R2 reads (optional)", metavar="R2", nargs="?"
    )
    parser.add_argument(
        dest="i1", help="fastq.gz with I1 reads (optional)", metavar="I1", nargs="?"
    )
    parser.add_argument(
        dest="i2", help="fastq.gz with I2 reads (optional)", metavar="I2", nargs="?"
    )
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        help="Set the output directory for mocked run. default: cwd",
        default=os.getcwd(),
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fastq2bcl` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fastq2bcl`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    pretty.install()

    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting application...")
    _logger.info(f"User defined mask: {args.mask}")
    _logger.info(f"Input files: R1={args.r1} R2={args.r2} I1={args.i1} I2={args.i2}")

    print("[bold green]fastq2bcl[/bold green]")
    print("Args:", args)

    # call fastq2bcl
    run_id, rundir, seqdesc_fields, mask_string = fastq2bcl(
        args.outdir, args.r1, args.r2, args.i1, args.i2, args.mask
    )

    # print report

    # print(f"RUNDIR: {rundir}")
    # print(f"RUNID:  {run_id}")
    # print(f"MASK    :{mask_string}")
    # print("SEQDESC FIELDS:")
    # for key, val in seqdesc_fields.items():
    #     val = "---" if val == None else val
    #     print("{:<10} {:<10}".format(key, val))

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m fastq2bcl.skeleton 42
    #
    run()
