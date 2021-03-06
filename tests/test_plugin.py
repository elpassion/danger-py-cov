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
        "| Files changed | Coverage | - |\n"
        "| ------------- | -------- | --- |\n"
        "| module_one.py | `71.43%` | :warning: |\n"
        "| module_three.py | `100.00%` | :white_check_mark: |\n"
        "| module_two.py | `0.00%` | :skull: |\n"
    )

    assert danger.results.markdowns == [Violation(message=expected_message)]
    assert danger.results.fails == []


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
    assert danger.results.fails == []


def test_plugin_does_fail_the_build_if_minimum_coverage_is_not_met(danger: Danger):
    """
    Test plugin fails the build if minimum coverage is not met.
    """
    plugin = DangerCoverage()
    plugin.report_coverage(
        report_path="tests/fixtures/cov_fixture.xml",
        sources_path="danger_py_cov_example/",
        minimum_coverage=66.70,
    )

    expected_message = (
        "### Current coverage is `66.67%`\n"
        "No source changes affecting the coverage found\n"
    )

    expected_fail = "Minimum required coverage `66.70%` not met"

    assert danger.results.markdowns == [Violation(message=expected_message)]
    assert danger.results.fails == [Violation(message=expected_fail)]
