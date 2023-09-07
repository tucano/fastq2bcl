import pytest

from fastq2bcl.cli import main, mock_run_id, fastq2bcl

__author__ = "Davide Rambaldi"
__copyright__ = "Davide Rambaldi"
__license__ = "MIT"

def test_main_usage(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["data/flowcell_example/Sample1_S1_L001_R1_001.fastq.gz"])
    captured = capsys.readouterr()
    assert "RUNID: YYMMDD_M11111_0222_000000000-K9H97" in captured.out

def test_mock_run_id():
    """Mock run id Tests"""
    pass

def test_fastq2bcl():
    """Fastq2bcl main function Tests"""
    pass