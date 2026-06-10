# Controller — 고정 검증 순서로 Entity 호출, status·failed_lines 조립

from typing import Literal, TypedDict

from constants import VERIFICATION_ORDER
from entity.line import line_sum_matches_magic, sum_line


class ValidateLinesResult(TypedDict):
    status: Literal["pass", "fail", "incomplete"]
    failed_lines: list[str]


def validate_lines(grid: list[list[int]]) -> ValidateLinesResult:
    ...
