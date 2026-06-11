# Entity Logic Track — 선 합·마법상수 비교 순수 로직 (I/O·상태·상수 기본값 없음)


def sum_line(cells: list[int]) -> int:
    """4칸 선의 합을 반환한다."""
    return sum(cells)


def line_sum_equals(cells: list[int], magic_constant: int) -> bool:
    """선 합이 주어진 마법상수와 일치하는지 반환한다."""
    return sum_line(cells) == magic_constant
