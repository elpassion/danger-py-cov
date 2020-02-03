from unittest.mock import patch

from danger_py_cov import DangerCoverage
from danger_python.danger import Danger, Violation


def test_plugin_appends_to_markdown(danger: Danger):
    """
    Test plugin appends to markdown.
    """
    plugin = DangerCoverage()
    plugin.report_coverage()

    assert danger.results.markdowns == [Violation(message="Hello world")]
