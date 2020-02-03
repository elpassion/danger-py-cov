from danger_py_cov_example.module_three import squarer


def test_squarer_works_for_zero():
    """
    Test squarer works for 0.
    """
    assert squarer(0) == 0
