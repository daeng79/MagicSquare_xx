# Entity — 선 합 계산 RED skeleton (assert 없음)

import pytest

from constants import MAGIC_CONSTANT
from entity.line import line_sum_matches_magic, sum_line


def test_t_log_001_sum_line_four_cells():
    """T-LOG-001: sum_line이 4칸 합을 반환한다."""
    # Given
    cells = [7, 8, 9, 10]

    # When
    result = sum_line(cells)

    # Then
    pytest.fail(
        f"RED: T-LOG-001 — sum_line(cells) 반환값 == {MAGIC_CONSTANT} 기대, got={result!r}"
    )


def test_t_log_002_line_sum_matches_magic_true():
    """T-LOG-002: line_sum_matches_magic이 합=마법상수 여부를 True로 반환한다."""
    # Given
    cells = [7, 8, 9, 10]
    magic_constant = MAGIC_CONSTANT

    # When
    result = line_sum_matches_magic(cells, magic_constant)

    # Then
    pytest.fail(
        f"RED: T-LOG-002 — line_sum_matches_magic 반환값 is True 기대, got={result!r}"
    )
