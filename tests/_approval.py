# Approval Test — golden master 비교 헬퍼

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(
    test_id: str, actual: str, *, golden_dir: Path | None = None
) -> None:
    """Approval Test: actual 문자열을 golden 파일과 비교한다."""
    base = golden_dir or GOLDEN_DIR
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{test_id}.approved.txt"
    normalized = actual.rstrip("\n") + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"golden 없음: {path} — UPDATE_GOLDEN=1 로 기준 생성")

    expected = path.read_text(encoding="utf-8")
    if expected != normalized:
        raise AssertionError(
            f"golden mismatch: {path}\n--- expected ---\n{expected}--- actual ---\n{normalized}"
        )
