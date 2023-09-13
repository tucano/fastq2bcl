import pytest

from fastq2bcl.cli import main, mock_run_id, fastq2bcl

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

test_fields = {
    "instrument": "M11111",
    "run_number": "222",
    "flowcell_id": "000000000-K9H97",
    "lane": "1",
    "tile": "1101",
    "x_pos": "19304",
    "y_pos": "1328",
    "UMI": "AAACGGG",
    "read": "1",
    "is_filtered": "N",
    "control_number": "0",
    "index": "1",
}


def test_main_usage(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["data/test/single/test_single.fastq.gz"])
    captured = capsys.readouterr()
    assert "YYMMDD_M11111_0222_000000000-K9H97" in captured.out


def test_mock_run_id():
    """Mock run id Tests"""
    assert mock_run_id(test_fields) == "YYMMDD_M11111_0222_000000000-K9H97"
    pass


def test_fastq2bcl():
    """Fastq2bcl main function Tests"""
    report = fastq2bcl(".", "data/test/single/test_single.fastq.gz")
    assert report["seqdesc_fields"]["flowcell_id"] == "000000000-K9H97"
    assert report["run_id"] == "YYMMDD_M11111_0222_000000000-K9H97"
    pass
