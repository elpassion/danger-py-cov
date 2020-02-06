from danger_py_cov.cobertura import CoberturaWrapper


def test_that_cobertura_wrapper_calculates_missed_and_total_branches():
    """
    Test that Cobertura report wrapper calculates missed & total branches.
    """
    report = CoberturaWrapper(
        "tests/fixtures/cov_fixture.xml", source="danger_py_cov_example/"
    )

    assert report.total_branches(filename="module_one.py") == 6
    assert report.missed_branches(filename="module_one.py") == 2
    assert report.total_branches(filename="module_two.py") == 0
    assert report.missed_branches(filename="module_two.py") == 0
    assert report.total_branches(filename="module_three.py") == 0
    assert report.missed_branches(filename="module_three.py") == 0
