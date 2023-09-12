import logging
import gzip
from fastq2bcl.parser import parse_seqdesc_fields
from Bio import SeqIO

_logger = logging.getLogger(__name__)


def read_first_record(fastq_file):
    """
    Validate fastq.gz r1 file and extract first read
    """
    _logger.info(f"Opening gz file {fastq_file}")
    with gzip.open(fastq_file, "rt") as fastq_fh:
        return next(SeqIO.parse(fastq_fh, "fastq"))


def read_fastq_files(r1, r2, i1, i2):
    """
    Read fastq files R1-R2 with I1 and I2 and return only the data we need
    """
    # test only R1 FIXME

    # return a list of tuple with seq, qual
    # and a list of tuple for pos with x and y
    sequences = []
    positions = []
    with gzip.open(r1, "rt") as r1_h:
        for record in SeqIO.parse(r1_h, "fastq"):
            _logger.debug(f"Parsed sequence object with header {record.description}")
            sequences.append(
                (str(record.seq), record.letter_annotations["phred_quality"])
            )
            seqdesc_fields = parse_seqdesc_fields(record.description)
            positions.append((seqdesc_fields["x_pos"], seqdesc_fields["y_pos"]))

    return {"sequences": sequences, "positions": positions}
