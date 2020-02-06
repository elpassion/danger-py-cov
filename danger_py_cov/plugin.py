from typing import Optional

from danger_python.plugins import DangerPlugin

from danger_py_cov.report import CoverageReport, generate_report


class DangerCoverage(DangerPlugin):
    def report_coverage(
        self,
        report_path: str,
        sources_path: Optional[str] = None,
        minimum_coverage: Optional[float] = None,
    ):
        report = CoverageReport(report_path, source=sources_path)
        modified_files = self.danger.git.modified_files + self.danger.git.created_files
        rendered_report = generate_report(report, modified_files, minimum_coverage)
        self.markdown(rendered_report.markdown)

        if rendered_report.fail:
            self.fail(rendered_report.fail)
