# 공통·Boundary 픽스처 — PRD §12.4 Given 격자

import pytest


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """4×4, 0 두 개, row-major 채움 순서."""
    return [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]


@pytest.fixture
def grid_r1_fail() -> list[list[int]]:
    """T-BND-001: R1 합 40."""
    return [
        [10, 10, 10, 10],
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [4, 5, 6, 7],
    ]


@pytest.fixture
def grid_d1_fail() -> list[list[int]]:
    """T-BND-002: D1↘ 합 23."""
    return [
        [10, 1, 2, 3],
        [4, 2, 5, 6],
        [7, 8, 7, 9],
        [10, 11, 12, 4],
    ]


@pytest.fixture
def grid_incomplete_d1() -> list[list[int]]:
    """T-BND-003: 행·열 8선 합 34, D1=40."""
    return [
        [10, 10, 7, 7],
        [7, 10, 10, 7],
        [7, 7, 10, 10],
        [10, 7, 7, 10],
    ]


@pytest.fixture
def grid_multi_fail() -> list[list[int]]:
    """T-BND-004: R1·R3 각 합 40."""
    return [
        [10, 10, 10, 10],
        [1, 2, 3, 4],
        [10, 10, 10, 10],
        [4, 5, 6, 7],
    ]
