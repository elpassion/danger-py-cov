from danger_py_cov.calculations import calculate_coverage
from danger_py_cov.models import CoverageFile


def test_coverage_calculation_handles_empty_files_list():
    """
    Test coverage calculation handles empty files list with maximum coverage.
    """
    result = calculate_coverage([])

    assert result == 100.00


def test_coverage_calculation_handles_a_case_with_no_statements():
    """
    Test coverage calculation handles files with no statements with maximum coverage.
    """
    coverage_file = CoverageFile(
        name="some_file.py",
        total_branches=0,
        total_statements=0,
        missed_branches=0,
        missed_statements=0,
    )
    result = calculate_coverage([coverage_file])

    assert result == 100.0
