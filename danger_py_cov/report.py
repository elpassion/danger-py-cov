import xml.etree.ElementTree as ET
from typing import Iterator, List, Optional, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape
from pycobertura import Cobertura

from .models import CoverageFile, CoverageFileChangeOutput, CoverageReportOutput


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
    template_environment = Environment(
        loader=PackageLoader("danger_py_cov", "templates"),
        autoescape=select_autoescape([]),
    )
    template = template_environment.get_template("report.md.jinja")
    report_entries = [entry_for_file(report, f) for f in report.files()]
    markdown = template.render(
        report=generate_report_for_files(report_entries, modified_files)
    )
    return list(filter(None, markdown.splitlines()))


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
) -> CoverageReportOutput:
    return CoverageReportOutput(
        total_coverage=__total_coverage(files),
        file_changes=__file_changes(files, modified_files),
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


def __file_changes(
    files: List[CoverageFile], modified_files: List[str]
) -> List[CoverageFileChangeOutput]:
    def is_modified(file: CoverageFile) -> bool:
        return any(map(lambda f: f.endswith(file.name), modified_files))

    return sorted(map(__file_output, filter(is_modified, files)), key=lambda f: f.name)


def __file_output(file: CoverageFile) -> CoverageFileChangeOutput:
    hits, totals = __hits_and_totals(file)
    coverage = float(hits) * 100.0 / float(totals)

    return CoverageFileChangeOutput(name=file.name, coverage=coverage)
