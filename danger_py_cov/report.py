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


def generate_report(report: CoverageReport, modified_files: List[str]) -> List[str]:
    report_entries = [entry_for_file(report, f) for f in report.files()]
    return generate_report_for_files(report_entries, modified_files)


def entry_for_file(report: CoverageReport, filename: str) -> CoverageFile:
    return CoverageFile(
        name=filename,
        total_statements=report.total_statements(filename),
        missed_statements=len(report.missed_statements(filename)),
        total_branches=report.total_branches(filename),
        missed_branches=report.missed_branches(filename),
    )


def generate_report_for_files(
    files: List[CoverageFile], modified_files: List[str]
) -> List[str]:
    coverage = f"{__total_coverage(files):.2f}%"
    return [f"### Current coverage is `{coverage}`"] + __markdown_table(
        files, modified_files
    )


def __total_coverage(files: List[CoverageFile]) -> float:
    hits, totals = zip(*map(__hits_and_totals, files))
    return float(sum(hits)) * 100.0 / float(sum(totals))


def __hits_and_totals(file: CoverageFile) -> Tuple[int, int]:
    statements = (
        "total_statements",
        "total_branches",
        "missed_statements",
        "missed_branches",
    )

    numbers = list(map(lambda s: getattr(file, s), statements))
    hits = numbers[0] + numbers[1] - numbers[2] - numbers[3]
    total = numbers[0] + numbers[1]
    return hits, total


def __markdown_table(files: List[CoverageFile], modified_files: List[str]) -> List[str]:
    def is_modified(file: CoverageFile) -> bool:
        return any(map(lambda f: f.endswith(file.name), modified_files))

    filtered_files = sorted(list(filter(is_modified, files)), key=lambda f: f.name)

    if not filtered_files:
        return ["No source changes affecting the coverage found"]

    return ["| Files changed | Coverage |", "| --- | --- |"] + list(
        map(__format_coverage, filtered_files)
    )


def __format_coverage(file: CoverageFile) -> str:
    hits, totals = __hits_and_totals(file)
    coverage = float(hits) * 100.0 / float(totals)

    return f"| {file.name} | {coverage:.2f}% |"
