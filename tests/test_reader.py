import pytest

from fastq2bcl.reader import (
    read_first_record,
    read_fastq_files,
    get_mask_from_files,
)

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

expected_data_single_seq = [
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
]

expected_data_single_pos = [("21270", "1316")]

expected_data_pair_seq = [
    (
        "ACTGAACCACTACTGAGCTGGGACGGAGTATACATTAACATAAACGTATCATAGCTTAGGACACTGCTCATAGCTGAGACGGATGTCATGACTGAGTTAGGGCACCTGGGATTAGTGTTTAACACTCTTTTGATACGGTATTGCCTAGATGGTACCCCAGCCGCGCTCCGGAGTCCAATAAAGCAGGGAAATACGGTCTACAGAGTGAGCCGACGCACGCAGTCACGAATCAGCCGGGCAGCTCATGGTACTGAGGTGACCATTCCCCTTTACCCCGTAACCGTCTCTTGTCTCCCGTGGCCCGATCGAGAACTTATCTCCAAGAAGCAAACGTTGAAGCACTTGTACGCAGCAGACACCTGCTAAGCACAATAACCGCGTCGGTGCGCCTTGGGGTTACAAATAGGAAGTAGTAGAACGTTAGATAATCCCTCTCAAACAACTTTAGTACCTTCCTAAACGTTTACCCGTATAATGTGTTGCTCGCACTAACTTCTGTCGTTTGCACGAATGTATTTTCGATCGGGCCACGGGAGACAAGAGACGGTTACGGGGTAAAGGGGAATGGTCACCTCAGTACCATGAGCTGCCCGGCTGATTCGTGACTGCGTGCGTCGG",
        [40] * 618,
    )
]

expected_data_multi_samples_seq_1 = "ACTGAACCACTACTGAGCTGGGACGGAGTATACATTAACATAAACGTATCATAGCTTAGGACACTGCTCATAGCTGAGACGGATGTCATGACTGAGTTAGGGCACCTGGGATTAGTGTTTAACACTCTTTTGATACGGTATTGCCTAGATGGTACCCCAGCCGCGCTCCGGAGTCCAATAAAGCAGGGAAATACGGTCTACAGAGTGAGCCGACGCACGCAGTCACGAATCAGCCGGGCAGCTCATGGTACTGAGGTGACCATTCCCCTTTACCCCGTAACCGTCTCTTGTCTCCCAACCACTAAACCACTAGAACTTATCTCCAAGAAGCAAACGTTGAAGCACTTGTACGCAGCAGACACCTGCTAAGCACAATAACCGCGTCGGTGCGCCTTGGGGTTACAAATAGGAAGTAGTAGAACGTTAGATAATCCCTCTCAAACAACTTTAGTACCTTCCTAAACGTTTACCCGTATAATGTGTTGCTCGCACTAACTTCTGTCGTTTGCACGAATGTATTTTCGATCGGGCCACGGGAGACAAGAGACGGTTACGGGGTAAAGGGGAATGGTCACCTCAGTACCATGAGCTGCCCGGCTGATTCGTGACTGCGTGCGTCGG"

expected_data_pair_pos = [("1", "2")]
expected_data_multi_samples_pos = [("1", "2"), ("3", "4")]


def test_read_first_record():
    r = read_first_record("data/test/01_single/test_single.fastq.gz")
    assert (
        str(r.seq)
        == "CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT"
    )


def test_read_single_fastq_files():
    seq, pos = read_fastq_files(
        "data/test/01_single/test_single.fastq.gz", None, None, None, True, True
    )
    assert seq == expected_data_single_seq
    assert pos == expected_data_single_pos


def test_read_pair_fastq_files():
    seq, pos = read_fastq_files(
        "data/test/07_pair/R1.fastq.gz",
        "data/test/07_pair/R2.fastq.gz",
        None,
        None,
        True,
        True,
    )
    assert seq == expected_data_pair_seq
    assert pos == expected_data_pair_pos


def test_read_pair_with_double_index():
    seq, pos = read_fastq_files(
        "data/test/05_multi_pair_double_index/R1.fastq.gz",
        "data/test/05_multi_pair_double_index/R2.fastq.gz",
        "data/test/05_multi_pair_double_index/RIndex1.fastq.gz",
        "data/test/05_multi_pair_double_index/RIndex2.fastq.gz",
        True,
        True,
    )
    assert seq[0][0] == expected_data_multi_samples_seq_1
    assert pos == expected_data_multi_samples_pos


def test_get_mask_from_files():
    assert (
        get_mask_from_files(
            "data/test/05_multi_pair_double_index/R1.fastq.gz",
            "data/test/05_multi_pair_double_index/R2.fastq.gz",
            "data/test/05_multi_pair_double_index/RIndex1.fastq.gz",
            "data/test/05_multi_pair_double_index/RIndex2.fastq.gz",
            True,
            True,
        )
        == "296N8Y8Y309N"
    )


def test_get_mask_from_files_raise_umi_error():
    with pytest.raises(ValueError):
        get_mask_from_files(
            "data/test/03_single_with_umi/single_with_umi.fastq.gz",
            None,
            "data/test/05_multi_pair_double_index/RIndex1.fastq.gz",
            "data/test/05_multi_pair_double_index/RIndex2.fastq.gz",
            False,
            True,
        )


def test_get_mask_from_files_raise_index_error():
    with pytest.raises(ValueError):
        get_mask_from_files(
            "data/test/05_multi_pair_double_index/R1.fastq.gz",
            "data/test/05_multi_pair_double_index/R2.fastq.gz",
            "data/test/05_multi_pair_double_index/RIndex1.fastq.gz",
            "data/test/05_multi_pair_double_index/RIndex2.fastq.gz",
            True,
            False,
        )


def test_get_mask_from_file_with_umi():
    assert (
        get_mask_from_files(
            "data/test/03_single_with_umi/single_with_umi.fastq.gz",
            None,
            None,
            None,
            False,
            True,
        )
        == "110N9Y"
    )


def test_read_fastq_file_with_umi():
    seq, pos = read_fastq_files(
        "data/test/03_single_with_umi/single_with_umi.fastq.gz",
        None,
        None,
        None,
        False,
        True,
    )
    assert seq[0][0].endswith("ACGTAGTAC") == True


def test_seq_mismatch():
    with pytest.raises(ValueError):
        seq, pos = read_fastq_files(
            "data/test/01_single/test_single.fastq.gz",
            "data/test/07_pair/R2.fastq.gz",
            None,
            None,
            True,
            True,
        )
