from typing import Optional

from danger_python.plugins import DangerPlugin

from danger_py_cov.report import CoverageReport, generate_report


class DangerCoverage(DangerPlugin):
    def report_coverage(self, report_path: str, sources_path: Optional[str] = None):
        report = CoverageReport(report_path, source=sources_path)

        for markdown in generate_report(report):
            self.markdown(markdown)
