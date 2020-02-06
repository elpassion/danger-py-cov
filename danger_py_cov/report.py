import functools
from typing import List, Optional, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape

from .calculations import emoji_for_coverage
from .cobertura import CoberturaWrapper
from .models import (
    CoverageFile,
    CoverageFileChangeOutput,
    CoverageReportOutput,
    DangerCoverageConfiguration,
    RenderedReport,
)


def generate_report(
    report: CoberturaWrapper,
    modified_files: List[str],
    minimum_coverage: Optional[float],
    configuration: DangerCoverageConfiguration,
) -> RenderedReport:
    template_environment = Environment(
        loader=PackageLoader("danger_py_cov", "templates"),
        autoescape=select_autoescape([]),
    )
    template = template_environment.get_template("report.md.jinja")
    report_entries = [entry_for_file(report, f) for f in report.files()]
    output = generate_report_for_files(report_entries, modified_files, configuration)
    markdown = template.render(report=output)
    fail = __fail(output, minimum_coverage)

    return RenderedReport(markdown=markdown, fail=fail)


def entry_for_file(report: CoberturaWrapper, filename: str) -> CoverageFile:
    return CoverageFile(
        name=filename,
        total_statements=report.total_statements(filename),
        missed_statements=len(report.missed_statements(filename)),
        total_branches=report.total_branches(filename),
        missed_branches=report.missed_branches(filename),
    )


def generate_report_for_files(
    files: List[CoverageFile],
    modified_files: List[str],
    configuration: DangerCoverageConfiguration,
) -> CoverageReportOutput:
    return CoverageReportOutput(
        total_coverage=__total_coverage(files),
        file_changes=__file_changes(files, modified_files, configuration),
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
    files: List[CoverageFile],
    modified_files: List[str],
    configuration: DangerCoverageConfiguration,
) -> List[CoverageFileChangeOutput]:
    def is_modified(file: CoverageFile) -> bool:
        return any(map(lambda f: f.endswith(file.name), modified_files))

    file_output = functools.partial(__file_output, configuration)
    return sorted(map(file_output, filter(is_modified, files)), key=lambda f: f.name)


def __file_output(
    configuration: DangerCoverageConfiguration, file: CoverageFile
) -> CoverageFileChangeOutput:
    hits, totals = __hits_and_totals(file)
    coverage = float(hits) * 100.0 / float(totals)
    emoji = emoji_for_coverage(coverage, configuration)

    return CoverageFileChangeOutput(name=file.name, coverage=coverage, emoji=emoji)


def __fail(
    output: CoverageReportOutput, minimum_coverage: Optional[float]
) -> Optional[str]:
    if not minimum_coverage or output.total_coverage >= minimum_coverage:
        return None

    return f"Minimum required coverage `{minimum_coverage:.2f}%` not met"
