from danger_py_cov_example.module_one import incrementer


def test_incrementer_works_for_zero():
    """
    Test incrementer works for 0.
    """
    assert incrementer(0) == 1


def test_incrementer_works_for_ten():
    """
    Test incrementer works for 10.
    """
    assert incrementer(10) == 11
