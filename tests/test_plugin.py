from danger_py_cov import DangerCoverage


def test_plugin_appends_to_markdown():
    """
    Test plugin appends to markdown.
    """
    plugin = DangerCoverage()

    plugin.report_coverage()
