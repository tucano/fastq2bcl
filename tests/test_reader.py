import pytest

from fastq2bcl.reader import read_first_record, read_fastq_files

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

expected_data_single = {
    "sequences": [
        (
            "CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT",
            [
                34,
                34,
                34,
                34,
                34,
                37,
                32,
                11,
                11,
                11,
                11,
                34,
                24,
                34,
                21,
                36,
                12,
                25,
                34,
                24,
                11,
                34,
                11,
                34,
                10,
                11,
                25,
                36,
                34,
                24,
                11,
                34,
                37,
                35,
                36,
                11,
                31,
                10,
                21,
                10,
                26,
                11,
                11,
                11,
                34,
                11,
                34,
                37,
                22,
                11,
                31,
                24,
                36,
                11,
                11,
                11,
                34,
                27,
                11,
                11,
                11,
                26,
                27,
                34,
                11,
                11,
                21,
                11,
                11,
                25,
                34,
                31,
                11,
                11,
                11,
                11,
                25,
                27,
                27,
                31,
                11,
                11,
                11,
                20,
                28,
                32,
                11,
                27,
                11,
                11,
                11,
                19,
                11,
                24,
                28,
                25,
                31,
                27,
                30,
                11,
                11,
                11,
                11,
                24,
                34,
                11,
                11,
                24,
                11,
                11,
            ],
        )
    ],
    "positions": [("21270", "1316")],
}

expected_data_pair = {
    "sequences": [
        (
            "ACTGAACCACTACTGAGCTGGGACGGAGTATACATTAACATAAACGTATCATAGCTTAGGACACTGCTCATAGCTGAGACGGATGTCATGACTGAGTTAGGGCACCTGGGATTAGTGTTTAACACTCTTTTGATACGGTATTGCCTAGATGGTACCCCAGCCGCGCTCCGGAGTCCAATAAAGCAGGGAAATACGGTCTACAGAGTGAGCCGACGCACGCAGTCACGAATCAGCCGGGCAGCTCATGGTACTGAGGTGACCATTCCCCTTTACCCCGTAACCGTCTCTTGTCTCCCGTGGCCCGATCGAGAACTTATCTCCAAGAAGCAAACGTTGAAGCACTTGTACGCAGCAGACACCTGCTAAGCACAATAACCGCGTCGGTGCGCCTTGGGGTTACAAATAGGAAGTAGTAGAACGTTAGATAATCCCTCTCAAACAACTTTAGTACCTTCCTAAACGTTTACCCGTATAATGTGTTGCTCGCACTAACTTCTGTCGTTTGCACGAATGTATTTTCGATCGGGCCACGGGAGACAAGAGACGGTTACGGGGTAAAGGGGAATGGTCACCTCAGTACCATGAGCTGCCCGGCTGATTCGTGACTGCGTGCGTCGG",
            [40] * 618,
        )
    ],
    "positions": [("1", "2")],
}


def test_read_first_record():
    r = read_first_record("data/test/single/test_single.fastq.gz")
    assert (
        str(r.seq)
        == "CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT"
    )


def test_read_single_fastq_files():
    assert (
        read_fastq_files("data/test/single/test_single.fastq.gz", None, None, None)
        == expected_data_single
    )


def test_read_pair_fastq_files():
    assert (
        read_fastq_files(
            "data/test/pair/R1.fastq.gz", "data/test/pair/R2.fastq.gz", None, None
        )
        == expected_data_pair
    )
