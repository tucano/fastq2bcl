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
from pathlib import Path

from fastq2bcl import __version__
from fastq2bcl.parser import parse_seqdesc_fields
from fastq2bcl.reader import read_first_record

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from fastq2bcl.skeleton import fib`,
# when using this Python module as a library.

def fastq2bcl(outdir, r1, r2=None, i1=None, i2=None):
    """
    fastq2bcl function call

    Args:
        outdir - output directory to create run flowcell fake dir
        r1 - R1 fastq.gz
        r2 - R2 fastq.gz
        i1 - I1 fastq.gz
        i2 - I2 fastq.gz

    Returns:
        a string report with useful info.
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
    run_id = mock_run_id(seqdesc_fields)

    # print report
    _logger.info("printing report")
    print (f"OUTDIR: {outdir.absolute()}")
    print (f"RUNID: {run_id}")
    print ("SEQDESC FIELDS:")    
    for key,val in seqdesc_fields.items():        
        val = "---" if val == None else val
        print("{:<10} {:<10}".format(key,val))

def mock_run_id(fields):
    """
    Mock the run directory id and Path
    """
    run_id = "YYMMDD_" + \
        fields['instrument'] + "_" + \
        fields['run_number'].zfill(4) + "_" + \
        fields['flowcell_id']
    return run_id

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
    parser = argparse.ArgumentParser(description="Convert fastq.gz reads and metadata in a bcl2fastq-able run directory")
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
    parser.add_argument(dest="r1", help="fastq.gz with R1 reads", metavar="R1")
    parser.add_argument(dest="r2", help="fastq.gz with R2 reads (optional)", metavar="R2", nargs='?')
    parser.add_argument(dest="i1", help="fastq.gz with I1 reads (optional)", metavar="I1", nargs='?')
    parser.add_argument(dest="i2", help="fastq.gz with I2 reads (optional)", metavar="I2", nargs='?')
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        help="Set the output directory for mocked run. default: cwd",
        default=os.getcwd()
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
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting application...")
    fastq2bcl(args.outdir, args.r1, args.r2, args.i1, args.i2)    
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
