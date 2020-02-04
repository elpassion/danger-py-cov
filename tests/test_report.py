from danger_py_cov.report import CoverageReport


def test_that_report_calculates_total_branches():
    """
    Test that report calculates total branches.
    """
    report = CoverageReport(
        "tests/fixtures/cov_fixture.xml", source="danger_py_cov_example/"
    )

    assert report.total_branches(filename="module_one.py") == 6
    assert report.missed_branches(filename="module_one.py") == 2
    assert report.total_branches(filename="module_two.py") == 0
    assert report.missed_branches(filename="module_two.py") == 0
    assert report.total_branches(filename="module_three.py") == 0
    assert report.missed_branches(filename="module_three.py") == 0
