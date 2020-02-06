import xml.etree.ElementTree as ET
from typing import Iterator, Optional, Tuple

from pycobertura import Cobertura


class CoberturaWrapper(Cobertura):
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
