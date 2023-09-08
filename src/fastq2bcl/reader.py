import logging
import gzip
from Bio import SeqIO

_logger = logging.getLogger(__name__)


def read_first_record(fastq_file):
    """
    Validate fastq.gz r1 file and extract first read
    """
    _logger.info(f"Opening gz file {fastq_file}")
    with gzip.open(fastq_file, "rt") as fastq_fh:
        return next(SeqIO.parse(fastq_fh, "fastq"))
