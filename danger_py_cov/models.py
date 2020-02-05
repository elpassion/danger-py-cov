from dataclasses import dataclass
from typing import List


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


@dataclass
class CoverageReportOutput:
    total_coverage: float
    file_changes: List[CoverageFileChangeOutput]
