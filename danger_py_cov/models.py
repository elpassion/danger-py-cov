from dataclasses import dataclass


@dataclass
class CoverageFile:
    name: str
    total_statements: int
    missed_statements: int
    total_branches: int
    missed_branches: int
