from typing import Optional

from danger_python.plugins import DangerPlugin
from pycobertura import Cobertura


class DangerCoverage(DangerPlugin):
    def report_coverage(self, report_path: str, sources_path: Optional[str] = None):
        report = Cobertura(report_path, source=sources_path)
        line_rate_formatted = f"{report.line_rate() * 100:.2f}"
        current_coverage = f"### Current coverage is `{line_rate_formatted}%`"
        self.markdown(current_coverage)
