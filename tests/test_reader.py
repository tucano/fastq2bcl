import pytest

from fastq2bcl.reader import read_first_record

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"


def test_read_first_record():
    r = read_first_record("data/test/single/test_single.fastq.gz")
    assert (
        str(r.seq)
        == "CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT"
    )
