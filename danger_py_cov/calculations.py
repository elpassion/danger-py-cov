from typing import List, Tuple

from .models import CoverageFile, DangerCoverageConfiguration


def emoji_for_coverage(
    coverage: float, configuration: DangerCoverageConfiguration
) -> str:
    if coverage >= configuration.high_threshold:
        return configuration.high_emoji
    elif coverage >= configuration.medium_threshold:
        return configuration.medium_emoji
    elif coverage >= configuration.low_threshold:
        return configuration.low_emoji
    else:
        return configuration.none_emoji


def calculate_coverage(files: List[CoverageFile]) -> float:
    default_coverage = 100.0
    if not files:
        return default_coverage

    hits, totals = zip(*map(__hits_and_totals, files))
    sum_totals = float(sum(totals))

    if sum_totals == 0:
        return default_coverage

    return float(sum(hits)) * 100.0 / sum_totals


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
