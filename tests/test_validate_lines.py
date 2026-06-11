# Boundary — validate_lines(grid) 공개 API 계약 검증 (RED skeleton)

from _approval import assert_matches_golden
from constants import VERIFICATION_ORDER
from entity.serialize import format_validate_lines_golden
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
    assert_matches_golden(
        "T-BND-001",
        format_validate_lines_golden(result["status"], result["failed_lines"]),
    )


def test_t_bnd_002_d1_in_failed_lines(grid_d1_fail):
    """T-BND-002: D1 합≠34 → status fail, D1 in failed_lines."""
    # Given
    grid = grid_d1_fail

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]
    assert_matches_golden(
        "T-BND-002",
        format_validate_lines_golden(result["status"], result["failed_lines"]),
    )


def test_t_bnd_003_incomplete_row_col_ok_d1_fail(grid_incomplete_d1):
    """T-BND-003: 행·열 OK·D1 실패 → status incomplete."""
    # Given
    grid = grid_incomplete_d1

    # When
    result = validate_lines(grid)

    # Then
    row_col_ids = {"R1", "R2", "R3", "R4", "C1", "C2", "C3", "C4"}
    assert result["status"] == "incomplete"
    assert "D1" in result["failed_lines"]
    assert not any(line_id in result["failed_lines"] for line_id in row_col_ids)
    assert_matches_golden(
        "T-BND-003",
        format_validate_lines_golden(result["status"], result["failed_lines"]),
    )


def test_t_bnd_004_failed_lines_verification_order(grid_multi_fail):
    """T-BND-004: 복수 실패 시 failed_lines가 VERIFICATION_ORDER 순."""
    # Given
    grid = grid_multi_fail

    # When
    result = validate_lines(grid)

    # Then
    assert "R1" in result["failed_lines"]
    assert "R3" in result["failed_lines"]
    assert result["failed_lines"] == [
        line_id for line_id in VERIFICATION_ORDER if line_id in result["failed_lines"]
    ]
    assert_matches_golden(
        "T-BND-004",
        format_validate_lines_golden(result["status"], result["failed_lines"]),
    )
