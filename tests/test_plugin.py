from danger_python.danger import Danger, Violation

from danger_py_cov import DangerCoverage


def test_plugin_appends_coverage_results_to_markdown(danger: Danger):
    """
    Test plugin appends coverage results to markdown.
    """
    plugin = DangerCoverage()
    plugin.report_coverage(
        report_path="tests/fixtures/cov_fixture.xml",
        sources_path="danger_py_cov_example/",
    )

    assert danger.results.markdowns == [
        Violation(message="### Current coverage is `66.67%`")
    ]
