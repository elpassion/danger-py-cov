from typing import Optional

from danger_python.plugins import DangerPlugin

from danger_py_cov.cobertura import CoberturaWrapper
from danger_py_cov.models import DangerCoverageConfiguration
from danger_py_cov.report import generate_report


class DangerCoverage(DangerPlugin):
    def report_coverage(
        self,
        report_path: str,
        sources_path: Optional[str] = None,
        minimum_coverage: Optional[float] = None,
        configuration: Optional[DangerCoverageConfiguration] = None,
    ):
        report = CoberturaWrapper(report_path, source=sources_path)
        modified_files = self.danger.git.modified_files + self.danger.git.created_files

        rendered_report = generate_report(
            report,
            modified_files,
            minimum_coverage,
            configuration if configuration else DangerCoverageConfiguration(),
        )
        self.markdown(rendered_report.markdown)

        if rendered_report.fail:
            self.fail(rendered_report.fail)
