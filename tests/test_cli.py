import pytest
import sys

from fastq2bcl.cli import main, mock_run_id, fastq2bcl, set_mask, run

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

expected_mask_110N = [{"cycles": "110", "index": "N", "id": "1"}]
expected_mask_110N10Y10Y110N = [
    {"cycles": "110", "index": "N", "id": "1"},
    {"cycles": "10", "index": "Y", "id": "2"},
    {"cycles": "10", "index": "Y", "id": "3"},
    {"cycles": "110", "index": "N", "id": "4"},
]


def test_run(capsys):
    """run CLI test"""
    with pytest.raises(SystemExit):
        run()


def test_main_usage(capsys, tmpdir):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-o", str(tmpdir), "data/test/single/test_single.fastq.gz"])
    captured = capsys.readouterr()
    assert "YYMMDD_M11111_0222_000000000-K9H97" in captured.out


def test_mock_run_id():
    """Mock run id Tests"""
    assert mock_run_id(test_fields) == "YYMMDD_M11111_0222_000000000-K9H97"


def test_fastq2bcl(tmpdir):
    """Fastq2bcl main function Tests"""
    run_id, rundir, seqdesc_fields, mask_string = fastq2bcl(
        str(tmpdir), "data/test/single/test_single.fastq.gz"
    )
    assert seqdesc_fields["flowcell_id"] == "000000000-K9H97"
    assert run_id == "YYMMDD_M11111_0222_000000000-K9H97"
    assert mask_string == "110N"


def test_fastq2bcl_with_mask(tmpdir):
    """Fastq2bcl main function Tests"""
    run_id, rundir, seqdesc_fields, mask_string = fastq2bcl(
        str(tmpdir),
        "data/test/pair/R1.fastq.gz",
        "data/test/pair/R2.fastq.gz",
        mask_string="309N309N",
    )
    assert seqdesc_fields["flowcell_id"] == "ABCD"
    assert run_id == "YYMMDD_run_0001_ABCD"
    assert mask_string == "309N309N"


def test_set_mask():
    """Test mask generation"""
    assert set_mask("110N") == expected_mask_110N
    assert set_mask("110N10Y10Y110N") == expected_mask_110N10Y10Y110N
    with pytest.raises(ValueError):
        set_mask(None)
    with pytest.raises(ValueError):
        set_mask("100")
