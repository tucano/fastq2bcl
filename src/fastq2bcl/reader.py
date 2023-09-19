import logging
import gzip
from fastq2bcl.parser import parse_seqdesc_fields
from Bio import SeqIO
from rich import print
import sys

_logger = logging.getLogger(__name__)


def read_first_record(fastq_file):
    """
    Validate fastq.gz r1 file and extract first read
    """
    _logger.info(f"Opening gz file {fastq_file}")
    with gzip.open(fastq_file, "rt") as fastq_fh:
        return next(SeqIO.parse(fastq_fh, "fastq"))


def get_file_handlers(r1, r2, i1, i2):
    """
    Return list of FH
    """
    files_fh = [gzip.open(r1, "rt")]
    if not i1 == None:
        files_fh.append(gzip.open(i1, "rt"))
    if not i2 == None:
        files_fh.append(gzip.open(i2, "rt"))
    if not r2 == None:
        files_fh.append(gzip.open(r2, "rt"))

    return files_fh


def get_mask_from_files(r1, r2, i1, i2):
    """
    Build a mask string using seq length
    """
    record_1 = read_first_record(r1)
    mask = f"{len(record_1.seq)}N"
    if not i1 == None:
        index_1 = read_first_record(i1)
        mask += f"{len(index_1.seq)}Y"
    if not i2 == None:
        index_2 = read_first_record(i2)
        mask += f"{len(index_2.seq)}Y"
    if not r2 == None:
        record_2 = read_first_record(r2)
        mask += f"{len(record_2.seq)}N"
    return mask


def read_fastq_files(r1, r2, i1, i2):
    """
    Read fastq files R1-R2 with I1 and I2 and return only the data we need
    """
    # return a list of tuple with seq, qual
    # and a list of tuple for pos with x and y
    # SINGLE R1
    # sequences = [('AAAA',1111)]
    # positions = [(1,1)]
    #
    # in case of multiple files R1-R2:
    # PAIR R1-R2
    # sequences = [('AAAABBBB',11111111)]
    # positions = [(1,1)]
    #
    # I need way to handle multiple files and merge them in a single with exitstack
    # Ref https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack

    # build a list of iterators
    file_handlers = get_file_handlers(r1, r2, i1, i2)
    seq_iterators = [SeqIO.parse(fh, "fastq") for fh in file_handlers]

    # output Lists
    sequences = []
    positions = []

    try:
        # iterate over the R1 iterator
        for r1_record in seq_iterators[0]:
            # call next in additional iterators
            opt_data = [next(iterator) for iterator in seq_iterators[1:]]
            # store R1 data
            record_fields = parse_seqdesc_fields(r1_record.description)
            record_id = r1_record.id
            record_seq = str(r1_record.seq)
            record_qual = r1_record.letter_annotations["phred_quality"]
            for opt_record in opt_data:
                if opt_record.id != record_id:
                    raise ValueError(
                        f"Seq ID mismatch for record {opt_record.id} R1 is {record_id}"
                    )
                record_seq += str(opt_record.seq)
                record_qual += opt_record.letter_annotations["phred_quality"]
            # append cluster position
            positions.append((record_fields["x_pos"], record_fields["y_pos"]))
            # append sequence and qual
            sequences.append((record_seq, record_qual))
    finally:
        # close all files
        for file_fh in file_handlers:
            file_fh.close()

    return (sequences, positions)
