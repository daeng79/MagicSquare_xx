# Controller — 고정 검증 순서로 Entity 호출, status·failed_lines 조립

from typing import Literal, TypedDict

from constants import VERIFICATION_ORDER
from entity.line import line_sum_matches_magic


class ValidateLinesResult(TypedDict):
    status: Literal["pass", "fail", "incomplete"]
    failed_lines: list[str]


_ROW_COL_IDS = frozenset({"R1", "R2", "R3", "R4", "C1", "C2", "C3", "C4"})
_DIAG_IDS = frozenset({"D1", "D2"})


def _cells_for_line(grid: list[list[int]], line_id: str) -> list[int]:
    """선 ID에 해당하는 4칸 값을 반환한다."""
    size = len(grid)
    if line_id.startswith("R"):
        row = int(line_id[1]) - 1
        return grid[row]
    if line_id.startswith("C"):
        col = int(line_id[1]) - 1
        return [grid[row][col] for row in range(size)]
    if line_id == "D1":
        return [grid[i][i] for i in range(size)]
    if line_id == "D2":
        return [grid[i][size - 1 - i] for i in range(size)]
    raise ValueError(f"알 수 없는 선 ID: {line_id}")


def validate_lines(grid: list[list[int]]) -> ValidateLinesResult:
    failed_lines: list[str] = []

    for line_id in VERIFICATION_ORDER:
        if not line_sum_matches_magic(_cells_for_line(grid, line_id)):
            failed_lines.append(line_id)

    if not failed_lines:
        status: Literal["pass", "fail", "incomplete"] = "pass"
    elif not any(lid in _ROW_COL_IDS for lid in failed_lines) and any(
        lid in _DIAG_IDS for lid in failed_lines
    ):
        status = "incomplete"
    else:
        status = "fail"

    return {"status": status, "failed_lines": failed_lines}
