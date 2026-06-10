# Boundary — validate_lines(grid) 공개 API 계약 검증 (RED skeleton)

import pytest

from constants import VERIFICATION_ORDER
from validate_lines import validate_lines


def test_t_bnd_001_r1_in_failed_lines(grid_r1_fail):
    """T-BND-001: R1 합≠34 → status fail, R1 in failed_lines."""
    # Arrange
    grid = grid_r1_fail

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R1" in result["failed_lines"]


def test_t_bnd_002_d1_in_failed_lines(grid_d1_fail):
    """T-BND-002: D1 합≠34 → status fail, D1 in failed_lines."""
    # Given
    grid = grid_d1_fail

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        f"RED: T-BND-002 — status=='fail', 'D1' in failed_lines 기대, result={result!r}"
    )


def test_t_bnd_003_incomplete_row_col_ok_d1_fail(grid_incomplete_d1):
    """T-BND-003: 행·열 OK·D1 실패 → status incomplete."""
    # Given
    grid = grid_incomplete_d1

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-BND-003 — status=='incomplete', 'D1' in failed_lines, "
        "행·열 ID 없음 기대, "
        f"result={result!r}"
    )


def test_t_bnd_004_failed_lines_verification_order(grid_multi_fail):
    """T-BND-004: 복수 실패 시 failed_lines가 VERIFICATION_ORDER 순."""
    # Given
    grid = grid_multi_fail

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        f"RED: T-BND-004 — failed_lines가 VERIFICATION_ORDER 순 기대 "
        f"(order={VERIFICATION_ORDER!r}), result={result!r}"
    )
