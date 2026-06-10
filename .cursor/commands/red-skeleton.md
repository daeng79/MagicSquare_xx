# RED Skeleton — pytest.fail 스켈레톤 (ARRR A단계)

> **ARRR A단계 (Ask = RED ④)** — `/red-test-plan` 설계표를 `tests/` **pytest.fail 스켈레톤**으로 옮긴다.  
> `assert` 본문·통과 더미 없음. `src/` 수정 금지. 다음 단계: 실제 RED assert 또는 GREEN.

---

## Skill 참조

**`magic-square-tdd` Skill이 있으면 자동 따름.**  
(`.cursor/skills/` 또는 프로젝트 Skill 경로에 존재 시 — 픽스처 명명·import 경로·AAA 주석·금지 목록을 Skill이 우선한다.)

---

## 사용법

```
/red-skeleton
```

**추가 입력 없이** 동작한다. 전제: 같은 채팅에 `/red-test-plan` 4블록(또는 동등 설계표)이 이미 있다.

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **직전 `/red-test-plan` 출력** | Test ID, 대상 함수, Given/When/Then, 파일 경로, RED 묶음 범위 |
| **블록 3 테스트 플랜** | `tests/test_*.py`, conftest 픽스처, pytest 명령 |
| **`.cursorrules`** | ECB 계층, 금지 항목 |
| **`magic-square-tdd` Skill** | 있으면 import·픽스처·명명 규칙 우선 |

설계표가 없으면 **중단**하고 `/red-test-plan` 먼저 실행하라고 안내한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (설계표 Track에 맞춤):

```
Phase: red | Layer: entity | Track: Logic
```

| Track | Layer | 기본 선언 |
|---|---|---|
| Logic | `entity` | `Phase: red \| Layer: entity \| Track: Logic` |
| UI (boundary) | `boundary` | `Phase: red \| Layer: boundary \| Track: UI` |

---

## 실행 절차

1. **설계표 Read** — 채팅 내 `/red-test-plan` 블록 1~3 (Test ID·파일·픽스처)
2. **`tests/`만 Write** — RED 묶음 범위의 스켈레톤 함수 추가 (또는 `conftest.py` 신규)
3. **AAA 주석** — `# Given` / `# When` / `# Then` (Arrange·Act·Assert 대응)
4. **Then 한 줄** — `pytest.fail("RED: {Test ID} — …")` 만 (assert 본문 금지)
5. **pytest 실행** — 플랜의 명령으로 전체 RED 묶음 실행
6. **보고** — [보고 형식](#보고-형식): Test ID · FAIL 한 줄 · 변경 파일(`tests/`만)

한 스켈레톤 = **Test ID 1개** = **테스트 함수 1개**.

---

## 스켈레톤 규칙

### AAA (Given / When / Then)

| 주석 | 단계 | 내용 |
|---|---|---|
| `# Given` | Arrange | 픽스처·격자·입력 데이터 준비 |
| `# When` | Act | 대상 함수 호출 (stub이면 호출만; 결과는 Then에서 fail) |
| `# Then` | Assert | **`pytest.fail(...)` 한 줄만** |

### Then (필수 형식)

```python
pytest.fail("RED: T-LOG-001 — sum_line이 4칸 합을 반환해야 함")
```

| 허용 | 금지 |
|---|---|
| `pytest.fail("RED: {Test ID} — {Then 요약}")` | `assert …` 본문 |
| When에서 Act 호출 (결과 미검증) | `pass`, `return`, 통과 더미 |
| Given에서 픽스처·리터럴 데이터 | `@pytest.mark.skip`, `xfail` |
| | `src/` 수정 |

메시지는 설계표 **Then** 열과 1:1 대응. Test ID는 설계표 ID 그대로.

### 상수 import (픽스처·Given 데이터만)

격자 크기·마법상수·셀 범위 리터럴 `34`/`16`/`4` **직접 쓰지 않는다.** 테스트·conftest의 **픽스처 데이터**에서만 import:

```python
from constants import MAGIC_CONSTANT, GRID_SIZE, MAX_CELL_VALUE
```

| 상수 | 의미 | SSOT |
|---|---|---|
| `MAGIC_CONSTANT` | 34 | `entity/constants.py` (없으면 `src/constants.py`) |
| `GRID_SIZE` | 4 | 동일 |
| `MAX_CELL_VALUE` | 16 | 동일 |

`entity/constants.py`가 없으면 `src/constants.py`에 동일 이름으로 추가는 **GREEN/REFACTOR** — skeleton 단계에서는 기존 `MAGIC_CONSTANT`만 import하고 `GRID_SIZE`/`MAX_CELL_VALUE`는 설계표·Skill 지시가 있을 때만 리터럴 대신 import 시도.

### conftest (기본 픽스처)

`tests/conftest.py`에 공통 격자 픽스처를 둔다:

| 픽스처 | 역할 |
|---|---|
| `grid_g1` | 4×4 격자, **빈칸(0) 정확히 2개**, **row-major** 순서로 값 배치 |

```python
# tests/conftest.py — 스켈레톤 단계 예시
import pytest

from constants import MAGIC_CONSTANT, GRID_SIZE  # entity/constants.py SSOT


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """4×4, 0 두 개, row-major 채움 순서."""
    return [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]
```

설계표에 다른 픽스처가 명시되면 **추가**하되 `grid_g1`은 유지·공유.

---

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

Logic Track · Entity · 설계표 `T-LOG-001` 대응 예:

```python
# tests/test_entity_line.py — RED skeleton (assert 없음)

import pytest

from constants import GRID_SIZE


def test_d_loc_01_blank_coords_row_major(grid_g1):
    """T-LOG-001: 빈칸 좌표를 row-major 순으로 반환한다."""
    # Given
    grid = grid_g1
    blank_count = sum(cell == 0 for row in grid for cell in row)

    # When
    # blank_coords = locate_blanks_row_major(grid)  # GREEN 전까지 미구현

    # Then
    pytest.fail(
        "RED: T-LOG-001 — row-major 빈칸 좌표 2건 [(1,2),(3,3)] 기대, "
        f"Given grid_g1 blank_count={blank_count}, GRID_SIZE={GRID_SIZE}"
    )
```

- 함수명 `test_d_loc_01_blank_coords_row_major` ↔ Test ID 1:1 (설계표 함수명 우선)
- When에 실제 호출이 있어도 **Then은 fail 한 줄만**
- Boundary Track이면 `validate_lines(grid)` Act + 동일 fail 패턴

---

## Boundary Track 치환 (Track A)

Logic 템플릿과 동일하되:

| 항목 | Logic | Boundary |
|---|---|---|
| 선언 | `Layer: entity \| Track: Logic` | `Layer: boundary \| Track: UI` |
| 파일 | `tests/test_entity_*.py` | `tests/test_validate_lines.py` |
| When | Entity 함수 | `result = validate_lines(grid)` |
| Then | `pytest.fail("RED: T-BND-…")` | 동일 (assert 대신 fail) |

---

## 금지 (본 커맨드)

| 금지 | 이유 |
|---|---|
| `src/` 수정 | GREEN 전용 |
| `assert` 본문 (Then) | 스켈레톤 단계 — fail만 |
| `pass` / 통과 더미 / 빈 Then | RED 회피 |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| GREEN / REFACTOR | 범위 밖 |
| 설계표 없이 임의 테스트 추가 | C2C 추적성 상실 |
| Domain Mock (`patch` on Entity) | ECB 위반 |

---

## pytest 실행 (필수)

스켈레톤 Write 직후 **반드시** 실행:

```bash
pytest tests/<플랜_파일> -v
```

또는 묶음 단위:

```bash
pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v
```

**기대 결과:** 묶음 내 **전부 FAILED** — `pytest.fail` 메시지에 `RED: {Test ID}` 포함.  
하나라도 PASSED면 스켈레톤 규칙 위반 → 수정 후 재실행.

---

## 보고 형식

```markdown
Phase: red | Layer: entity | Track: Logic

## 스켈레톤 추가
| Test ID | 함수명 | FAIL 메시지 (한 줄) |
|---|---|---|
| T-LOG-001 | `test_d_loc_01_blank_coords_row_major` | RED: T-LOG-001 — row-major 빈칸 좌표 … |

## pytest 결과
- 명령: `pytest tests/test_entity_line.py -v`
- 결과: N failed, 0 passed

## 변경 파일 (tests/만)
- `tests/conftest.py` (신규 또는 grid_g1 추가)
- `tests/test_entity_line.py` (스켈레톤 N개)

## 다음 단계
- RED assert 치환 또는 GREEN: `src/entity/` 최소 구현
```

보고 표의 **FAIL 메시지**는 pytest 출력에서 **한 줄**만 인용한다.

---

## ARRR 위치

| 단계 | 커맨드 | 산출 |
|---|---|---|
| RED ③ | `/red-test-plan` | C2C 설계표·플랜 (파일 없음) |
| **RED ④** | **`/red-skeleton`** | **`tests/` pytest.fail 스켈레톤** |
| RED ⑤ / GREEN | `/tdd-red` 또는 assert 치환 | 실패 assert·GREEN 구현 |

---

## 참조

| 문서 | 역할 |
|---|---|
| `.cursor/commands/red-test-plan.md` | 앞단 설계표·RED 묶음·Test ID |
| `.cursor/commands/tdd-red.md` | Boundary RED assert·AAA·Mom Test 보고 |
| `.cursorrules` | ECB·API·검증 순서 |
| `magic-square-tdd` Skill | 있으면 **자동 따름** (import·픽스처·명명) |

### 완료 조건

- [ ] 설계표 RED 묶음 전 Test ID에 스켈레톤 1:1 존재
- [ ] Then = `pytest.fail("RED: …")` 만
- [ ] `tests/`만 변경
- [ ] pytest 전부 FAILED 확인
- [ ] 보고에 Test ID · FAIL 한 줄 · 변경 파일 명시

---

*ARRR Ask: RED ④ = 설계표 → pytest.fail 골격. assert·구현은 다음 단계.*
