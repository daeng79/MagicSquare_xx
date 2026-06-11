# Entity — 선 합 계산 RED skeleton (assert 없음)

from _approval import assert_matches_golden
from constants import MAGIC_CONSTANT
from entity.line import line_sum_matches_magic, sum_line
from entity.serialize import format_entity_bool_golden, format_entity_int_golden


def test_t_log_001_sum_line_four_cells():
    """T-LOG-001: sum_line이 4칸 합을 반환한다."""
    # Given
    cells = [7, 8, 9, 10]

    # When
    result = sum_line(cells)

    # Then
    assert result == MAGIC_CONSTANT
    assert_matches_golden("T-LOG-001", format_entity_int_golden(result))


def test_t_log_002_line_sum_matches_magic_true():
    """T-LOG-002: line_sum_matches_magic이 합=마법상수 여부를 True로 반환한다."""
    # Given
    cells = [7, 8, 9, 10]
    magic_constant = MAGIC_CONSTANT

    # When
    result = line_sum_matches_magic(cells, magic_constant)

    # Then
    assert result is True
    assert_matches_golden("T-LOG-002", format_entity_bool_golden(result))
