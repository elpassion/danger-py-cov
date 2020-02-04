from typing import Optional

from danger_python.plugins import DangerPlugin

from danger_py_cov.report import CoverageReport, generate_report


class DangerCoverage(DangerPlugin):
    def report_coverage(self, report_path: str, sources_path: Optional[str] = None):
        report = CoverageReport(report_path, source=sources_path)
        modified_files = self.danger.git.modified_files + self.danger.git.created_files

        for markdown in generate_report(report, modified_files):
            self.markdown(markdown)
