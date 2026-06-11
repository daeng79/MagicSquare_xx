# Entity UI Track — 공개 API·constants 연결 (로직은 line_logic에 위임)

from constants import MAGIC_CONSTANT
from entity.line_logic import line_sum_equals, sum_line

__all__ = ["sum_line", "line_sum_matches_magic"]


def line_sum_matches_magic(cells: list[int], magic_constant: int = MAGIC_CONSTANT) -> bool:
    """선 합이 마법상수와 일치하는지 반환한다."""
    return line_sum_equals(cells, magic_constant)
