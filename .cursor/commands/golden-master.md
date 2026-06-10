# Golden Master — Approval Test 구축·검증

> **GREEN PASS 후** 대상 Test ID의 출력을 Golden Master(Approval Test)로 고정한다.  
> 기준 파일 생성 → matched 검증. 수동 편집으로 통과 우회 금지.

---

## Skill 참조

**`magic-square-tdd` Skill이 있으면 자동 따름.**  
(golden 경로·직렬화 포맷·`UPDATE_GOLDEN` 절차가 Skill과 충돌하면 Skill 우선)

---

## 사용법

```
/golden-master
```

**추가 입력 없이** 동작한다. 전제: 대상 Test ID가 **pytest PASS** 상태 (`/green-minimal` 완료 후).

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **채팅·설계표** | Test ID, 대상 함수, `tests/` 경로 |
| **`/green-minimal` 보고** | PASS Test ID · 변경 파일 |
| **`.cursorrules`** | ECB·도메인 규칙 |
| **`magic-square-tdd` Skill** | golden 포맷·헬퍼 우선 |

대상 Test ID가 FAIL이면 **중단** — `/green-minimal` 먼저 실행하라고 안내한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: green | Layer: entity | Track: Logic
```

| Track | Layer | 기본 선언 |
|---|---|---|
| Logic | `entity` | `Phase: green \| Layer: entity \| Track: Logic` |
| UI (boundary) | `boundary` | `Phase: green \| Layer: boundary \| Track: UI` |

---

## 전제 (필수)

| 조건 | 확인 |
|---|---|
| 대상 Test ID pytest | **PASSED** |
| `src/` 구현 | GREEN 최소 구현 완료 |
| assert | `pytest.fail` 없음, 설계 Then assert 존재 |

```bash
pytest tests/<파일>::<함수> -v
# → 1 passed 필수
```

---

## 실행 절차

### 1. `tests/_approval.py` — `assert_matches_golden`

파일이 없으면 **생성**. 있으면 포맷 규칙만 준수하는지 확인.

| 항목 | 규칙 |
|---|---|
| 함수 | `assert_matches_golden(test_id: str, actual: str, *, golden_dir: Path \| None = None)` |
| golden 경로 | `tests/golden/{test_id}.approved.txt` (`test_id` = `T-LOG-001` 등) |
| `UPDATE_GOLDEN=1` | actual을 golden 파일에 **덮어쓰기** 후 `matched` 반환 |
| `UPDATE_GOLDEN` 없음 | golden 읽어 actual과 **완전 일치** 비교; 불일치 시 diff와 함께 실패 |

```python
# tests/_approval.py — 골격 (없으면 생성)
from __future__ import annotations

import os
from pathlib import Path


GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(test_id: str, actual: str, *, golden_dir: Path | None = None) -> None:
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
```

### 2. `tests/golden/{id}.approved.txt` 연결

대상 테스트 Then에 golden assert **추가** (기존 assert 유지·보강):

```python
from _approval import assert_matches_golden
from entity.serialize import format_golden_payload  # Skill·프로젝트 헬퍼


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given / When … (기존 GREEN assert 유지)
    payload = format_golden_payload(coords, error_code)  # 아래 포맷 규칙

    # Golden Master
    assert_matches_golden("T-LOG-001", payload)
```

- `{id}` = 설계표 **Test ID** (`T-LOG-001` → `tests/golden/T-LOG-001.approved.txt`)
- Test ID ↔ golden 파일 **1:1**

### 3. `UPDATE_GOLDEN=1` — 기준 파일 생성

**최초 1회** (또는 의도적 기준 갱신 시만):

```bash
UPDATE_GOLDEN=1 pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v
```

- `src/` 실행 결과를 직렬화한 `actual`이 golden에 기록됨
- 생성 후 golden 파일 **내용을 수동 편집해 통과시키지 않는다**

### 4. `UPDATE_GOLDEN` 없이 matched 확인

```bash
pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v
```

- **기대:** PASSED + golden **matched**
- 불일치 시 pytest **FAILED**, diff 메시지로 expected/actual 출력

---

## Golden 페이로드 포맷 (고정)

수동 편집·임의 포맷 금지. `format_golden_payload` (또는 동등 헬퍼)로만 생성.

### `int[6]` — 1-index

| 규칙 | 내용 |
|---|---|
| 개수 | 정수 **6개** 고정 |
| 인덱스 | **1-based** (0 금지) |
| 직렬화 | `I:` + 콤마 구분, 공백 없음 |

```
I:1,2,3,3,4,2
```

예: row-major 빈칸 좌표 `(1,2)`, `(3,3)` → `row,col,row,col,pad,pad` 등 도메인 매핑은 Entity/Skill에 정의. **6슬롯 미만·초과 금지.**

### 에러 코드 문자열

| 규칙 | 내용 |
|---|---|
| 접두 | `E:` |
| 패턴 | `E` + 3자리 숫자 (`E000` = 정상/에러 없음) |
| 예 | `E000`, `E001` … `E005` |

### 전체 레코드 (한 줄 또는 고정 2줄)

```
I:1,2,3,3,0,0
E:E000
```

- 줄바꿈: 마지막 `\n` 하나 (비교 시 `assert_matches_golden`이 정규화)
- 필드 순서·접두사 변경 금지

```python
def format_golden_payload(int6: tuple[int, int, int, int, int, int], error_code: str) -> str:
    """int[6] 1-index + 에러 코드 문자열 — golden SSOT 포맷."""
    if len(int6) != 6 or any(i < 1 for i in int6):
        raise ValueError("int6는 1-index 정수 6개")
    if not error_code.startswith("E") or len(error_code) != 4:
        raise ValueError("error_code는 Exxx 형식")
    return f"I:{','.join(str(i) for i in int6)}\nE:{error_code}\n"
```

---

## 금지

| 금지 | 이유 |
|---|---|
| golden 파일 **수동 편집**으로 pytest 통과 | Approval 우회 |
| `UPDATE_GOLDEN` 없이 golden 삭제·빈 파일 | 기준 상실 |
| 포맷 임의 변경 (`I:`/`E:` 외, 0-index) | diff 비교 무의미 |
| PASS 전 golden 생성 | 구현 미검증 기준 |
| 이번 Test ID 외 golden 일괄 갱신 | 추적성 상실 |
| `src/` 변경으로 golden만 맞추기 (테스트 의미 훼손) | GREEN 회귀 |

기준 갱신이 필요하면 **`UPDATE_GOLDEN=1` + 구현·assert 정당화** 후에만 수행.

---

## pytest 명령 요약

| 단계 | 명령 |
|---|---|
| PASS 전제 확인 | `pytest tests/<파일>::<함수> -v` |
| 기준 생성 | `UPDATE_GOLDEN=1 pytest tests/<파일>::<함수> -v` |
| matched 검증 | `pytest tests/<파일>::<함수> -v` |
| 회귀 (파일 전체) | `pytest tests/<파일> -v` |

Boundary 예:

```bash
UPDATE_GOLDEN=1 pytest tests/test_validate_lines.py::test_행1_합이_34가_아니면_failed_lines에_R1 -v
pytest tests/test_validate_lines.py::test_행1_합이_34가_아니면_failed_lines에_R1 -v
```

---

## 보고 형식

```markdown
Phase: green | Layer: entity | Track: Logic

## 대상 Test ID
- T-LOG-001 (`test_d_loc_01_blank_coords_row_major`) — PASS 전제 확인됨

## Golden
| 항목 | 값 |
|---|---|
| 경로 | `tests/golden/T-LOG-001.approved.txt` |
| matched | yes / no |
| diff 요약 | (no 시) `I:` 줄 또는 `E:` 줄 불일치 한 줄 |

## pytest
- 생성: `UPDATE_GOLDEN=1 pytest …` → passed, golden written
- 검증: `pytest …` (UPDATE_GOLDEN 없음) → passed, matched

## 변경 파일
- `tests/_approval.py` (신규 또는 유지)
- `tests/golden/T-LOG-001.approved.txt` (신규)
- `tests/test_entity_line.py` (assert_matches_golden 연결)

## 다음 단계
- 다음 Test ID golden 또는 REFACTOR
```

**diff 요약:** mismatch 시 `AssertionError`에서 `I:`/`E:` 중 달라진 **첫 줄만** 인용.

---

## Boundary Track 치환 (Track A)

| 항목 | Logic | Boundary |
|---|---|---|
| 선언 | `Layer: entity \| Track: Logic` | `Layer: boundary \| Track: UI` |
| payload | Entity 출력 직렬화 | `status` + `failed_lines` 등 API dict 직렬화 |
| golden id | `T-LOG-{nnn}` | `T-BND-{nnn}` |
| 포맷 | `I:` + `E:` (동일 규칙 적용 가능) | Skill·Contract에 따른 고정 문자열 (예: `S:fail\nF:R1,D1\nE:E000\n`) |

Boundary 전용 포맷은 Skill·PRD가 있으면 그 SSOT를 따르고, 없으면 **한 줄 키=값 고정**으로 문서화 후 동일 approval 흐름을 적용한다.

---

## ARRR · TDD 위치

| 단계 | 커맨드 | 산출 |
|---|---|---|
| GREEN | `/green-minimal` | PASS + 최소 구현 |
| **Golden Master** | **`/golden-master`** | **`tests/golden/*.approved.txt` + matched** |
| REFACTOR | (별도) | 동작 유지, golden은 UPDATE_GOLDEN으로만 갱신 |

---

## 참조

| 문서 | 역할 |
|---|---|
| `.cursor/commands/green-minimal.md` | PASS 전제·묶음 Test ID |
| `.cursor/commands/red-test-plan.md` | Test ID · Then |
| `.cursorrules` | ECB·도메인 |
| `magic-square-tdd` Skill | golden 포맷·직렬화 헬퍼 |

### 완료 조건

- [ ] 대상 Test ID PASS 전제 충족
- [ ] `tests/_approval.py` + `assert_matches_golden` 존재
- [ ] `tests/golden/{id}.approved.txt` 연결
- [ ] `UPDATE_GOLDEN=1`로 기준 생성 완료
- [ ] `UPDATE_GOLDEN` 없이 matched · pytest PASSED
- [ ] golden 수동 편집 없음
- [ ] 보고: golden 경로 · matched · diff 요약

---

*Golden Master = GREEN 이후 회귀 방지용 Approval Test. 기준은 구현 출력으로만 갱신한다.*
