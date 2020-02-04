import xml.etree.ElementTree as ET
from typing import Iterator, List, Optional, Tuple

from pycobertura import Cobertura

from .models import CoverageFile


class CoverageReport(Cobertura):
    def total_branches(self, filename: str) -> int:
        branch_info = self._get_branch_info(filename)
        return sum(map(lambda b: b[1], branch_info))

    def missed_branches(self, filename: str) -> int:
        branch_info = self._get_branch_info(filename)
        return sum(map(lambda b: b[1] - b[0], branch_info))

    def _get_branch_info(self, filename: str) -> Iterator[Tuple[int, int]]:
        lines = self._get_lines_by_filename(filename)
        return filter(None, map(self._get_branch_info_for_line, lines))

    def _get_branch_info_for_line(self, line: ET.Element) -> Optional[Tuple[int, int]]:
        if "condition-coverage" not in line.attrib:
            return None

        coverage = line.attrib["condition-coverage"]
        covered_branches = coverage.split("(")[-1][:-1].split("/")
        return (int(covered_branches[0]), int(covered_branches[1]))


def generate_report(report: CoverageReport) -> List[str]:
    report_entries = [entry_for_file(report, f) for f in report.files()]
    return generate_report_for_files(report_entries)


def entry_for_file(report: CoverageReport, filename: str) -> CoverageFile:
    return CoverageFile(
        name=filename,
        total_statements=report.total_statements(filename),
        missed_statements=len(report.missed_statements(filename)),
        total_branches=report.total_branches(filename),
        missed_branches=report.missed_branches(filename),
    )


def generate_report_for_files(files: List[CoverageFile]) -> List[str]:
    coverage = f"{total_coverage(files):.2f}%"
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
