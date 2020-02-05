import pytest
from danger_python.danger import Danger, Violation

from danger_py_cov import DangerCoverage


@pytest.mark.parametrize(
    "modified_files",
    [["danger_py_cov_example/module_one.py", "danger_py_cov_example/module_two.py"]],
)
@pytest.mark.parametrize("created_files", [["danger_py_cov_example/module_three.py"]])
def test_plugin_appends_coverage_results_to_markdown(danger: Danger):
    """
    Test plugin appends coverage results to markdown.
    """
    plugin = DangerCoverage()
    plugin.report_coverage(
        report_path="tests/fixtures/cov_fixture.xml",
        sources_path="danger_py_cov_example/",
    )

    expected_message = (
        "### Current coverage is `66.67%`\n"
        "| Files changed | Coverage |\n"
        "| ------------- | -------- |\n"
        "| module_one.py | 71.43% |\n"
        "| module_three.py | 100.00% |\n"
        "| module_two.py | 0.00% |\n"
    )

    assert danger.results.markdowns == [Violation(message=expected_message)]


def test_plugin_does_not_print_table_if_there_are_no_changed_files(danger: Danger):
    """
    Test plugin does not print coverage table if there are no changed and/or
    created files.
    """
    plugin = DangerCoverage()
    plugin.report_coverage(
        report_path="tests/fixtures/cov_fixture.xml",
        sources_path="danger_py_cov_example/",
    )

    expected_message = (
        "### Current coverage is `66.67%`\n"
        "No source changes affecting the coverage found\n"
    )

    assert danger.results.markdowns == [Violation(message=expected_message)]
