from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DangerCoverageConfiguration:
    low_threshold: float = 0.25
    medium_threshold: float = 0.5
    high_threshold: float = 0.8
    none_emoji: str = ":skull:"
    low_emoji: str = ":no_entry_sign:"
    medium_emoji: str = ":warning:"
    high_emoji: str = ":white_check_mark:"


@dataclass
class CoverageFile:
    name: str
    total_statements: int
    missed_statements: int
    total_branches: int
    missed_branches: int


@dataclass
class CoverageFileChangeOutput:
    name: str
    coverage: float
    emoji: str


@dataclass
class CoverageReportOutput:
    total_coverage: float
    file_changes: List[CoverageFileChangeOutput]


@dataclass
class RenderedReport:
    markdown: str
    fail: Optional[str]
