from danger_python.danger import Danger, Violation

from danger_py_cov import DangerCoverage


def test_plugin_appends_coverage_results_to_markdown(danger: Danger):
    """
    Test plugin appends coverage results to markdown.
    """
    plugin = DangerCoverage()
    plugin.report_coverage()

    assert danger.results.markdowns == [Violation(message="Hello world")]
