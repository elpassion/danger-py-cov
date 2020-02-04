from typing import Iterable, List, Optional

from danger_python.plugins import DangerPlugin

from danger_py_cov.models import CoverageFile
from danger_py_cov.report import CoverageReport


class DangerCoverage(DangerPlugin):
    def report_coverage(self, report_path: str, sources_path: Optional[str] = None):
        report = CoverageReport(report_path, source=sources_path)
        report_entries = map(lambda f: entry_for_file(report, f), report.files())
        generated_report = generate_report(report_entries)

        for markdown in generated_report:
            self.markdown(markdown)


def entry_for_file(report: CoverageReport, filename: str) -> CoverageFile:
    return CoverageFile(
        name=filename,
        total_statements=report.total_statements(filename),
        missed_statements=len(report.missed_statements(filename)),
        total_branches=report.total_branches(filename),
        missed_branches=report.missed_branches(filename),
    )


def generate_report(files: Iterable[CoverageFile]) -> List[str]:
    coverage = f"{total_coverage(list(files)):.2f}%"
    return [f"### Current coverage is `{coverage}`"]


def total_coverage(files: List[CoverageFile]) -> float:
    statements = (
        "total_statements",
        "total_branches",
        "missed_statements",
        "missed_branches",
    )

    numbers = list(map(lambda s: sum(map(lambda f: getattr(f, s), files)), statements))
    hits = numbers[0] + numbers[1] - numbers[2] - numbers[3]
    total = numbers[0] + numbers[1]

    return float(hits) * 100.0 / float(total)
