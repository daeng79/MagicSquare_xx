# GREEN Minimal — RED 1묶음 최소 구현 (ARRR R단계)

> **ARRR R단계 (Respond = GREEN)** — RED 1묶음당 `src/` **최소 구현**으로 해당 Test ID를 PASS시킨다.  
> **1커밋 = 1 RED 묶음** (사용자가 commit 요청할 때만). REFACTOR는 별도 커맨드.

---

## Skill 참조

**`magic-square-tdd` Skill이 있으면 자동 따름.**  
(import 경로·상수 SSOT·ECB·최소 구현 범위가 Skill과 충돌하면 Skill 우선)

---

## 사용법

```
/green-minimal
```

**추가 입력 없이** 동작한다. 전제: 같은 채팅·브랜치에 `/red-test-plan` 설계표 + `/red-skeleton` 스켈레톤이 있고, RED 묶음이 **FAILED** 상태다.

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **`/red-test-plan` 블록 1~3** | RED 묶음 Test ID, Given/When/Then, 대상 함수 |
| **`/red-skeleton` 산출** | `tests/` 경로, `pytest.fail` 메시지, conftest |
| **`.cursorrules`** | ECB, API 계약, TDD 사이클 |
| **`magic-square-tdd` Skill** | 있으면 최소 구현·상수 규칙 우선 |

스켈레톤·설계표가 없으면 **중단** — `/red-skeleton` 먼저 실행하라고 안내한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (설계표 Track에 맞춤):

```
Phase: green | Layer: entity | Track: Logic
```

| Track | Layer | 기본 선언 |
|---|---|---|
| Logic | `entity` | `Phase: green \| Layer: entity \| Track: Logic` |
| UI (boundary) | `boundary` | `Phase: green \| Layer: boundary \| Track: UI` |

---

## 실행 절차

1. **RED 재확인** — 이번 RED 묶음만 pytest 실행, 전부 `FAILED` + `pytest.fail("RED: …")` 인지 확인
2. **`src/` 최소 구현** — 묶음 Test ID 통과에 **필요한 코드만** 추가·수정 (여분 로직 금지)
3. **`tests/` assert 교체** — `pytest.fail` 제거, 설계표 **Then**에 맞는 `assert` 본문으로 치환
4. **PASS 확인** — 묶음 전 Test ID pytest PASS; **회귀**는 파일 전체·관련 suite로 재확인
5. **보고** — [보고 형식](#보고-형식): PASS Test ID · 변경 파일 · 회귀 결과

| 단계 | 수정 허용 | 금지 |
|---|---|---|
| RED 재확인 | — | assert·src 선행 수정 |
| 최소 구현 | `src/` (묶음 범위) | 이번 묶음 외 Test ID 동시 해결 |
| assert 교체 | `tests/` (묶음 범위) | assert 완화·skip·xfail |
| PASS 확인 | 회귀 실패 시 **즉시** 수정 | REFACTOR·구조 개편 |

**1 RED 묶음 = 설계표 `RED 묶음 범위`에 명시된 Test ID 집합** (예: `T-LOG-001~003`). 한 번의 `/green-minimal`은 **한 묶음만** 처리한다.

---

## 최소 구현 원칙

### 상수 SSOT (`constants.py`)

| 금지 | 대신 |
|---|---|
| 리터럴 `34`, `16`, `4` 하드코딩 | `constants.py` import |
| 매직넘버·중복 상수 정의 | `MAGIC_CONSTANT`, `GRID_SIZE`, `MAX_CELL_VALUE` 등 SSOT |

```python
# src/entity/line.py — 예
from constants import MAGIC_CONSTANT

def line_sum_matches_magic(cells: list[int], magic_constant: int = MAGIC_CONSTANT) -> bool:
    ...
```

SSOT: `entity/constants.py` 우선, 없으면 `src/constants.py`. 새 상수는 **이번 묶음에 필요할 때만** constants에 추가.

### ECB (계층 import)

| 계층 | 허용 import | 금지 |
|---|---|---|
| **Entity** (`src/entity/`) | `constants`, 표준 라이브러리 | `validate_lines`, `tests.*`, Boundary·Controller |
| **Controller** | `entity.*`, `constants` | `tests.*` |
| **Boundary** (`tests/`) | 공개 API (`validate_lines` 등), `constants`(픽스처만) | Entity 내부 private 우회 assert |

Entity는 **I/O·상태·Mock 없음** — 순수 함수만.

### E001~E005 (구현·테스트에서 금지)

RED 설계와 동일한 품질 게이트. **해당 패턴으로 `raise`·조기 `return`·stub 통과 금지.**

| 코드 | GREEN에서 금지 |
|---|---|
| **E001** | 묶음 밖 Test ID를 한꺼번에 맞추는 과잉 구현·범위 밖 `src/` 변경 |
| **E002** | Domain Mock / Entity `patch` |
| **E003** | `@pytest.mark.skip`, `xfail` |
| **E004** | assert 완화 (`==`→`in`, 조건 삭제), `pytest.fail` 잔존 |
| **E005** | 솔버·정답 채우기·하드코딩된 정답 반환 |

**금지 예 (통과용 치트):**

```python
# 금지 — E005/과잉 구현
def sum_line(cells): return 34

# 금지 — E004
assert result in ("pass", "fail")  # 설계 Then보다 약함

# 금지 — 묶음 밖 선행 해결
def validate_lines(grid): ...  # T-LOG-001만 GREEN인데 Controller 전체 구현
```

---

## assert 교체 (스켈레톤 → RED assert)

`/red-skeleton` Then을 설계표 Then에 맞게 교체:

```python
# Before (skeleton)
pytest.fail("RED: T-LOG-001 — sum_line이 4칸 합을 34와 비교해야 함")

# After (GREEN)
from constants import MAGIC_CONSTANT

# When
total = sum_line(cells)

# Then
assert total == 10  # Given에 맞는 기대값
assert line_sum_matches_magic(cells, MAGIC_CONSTANT) is False
```

- Test ID 주석·docstring 유지 (traceability)
- AAA 주석(`# Given` / `# When` / `# Then`) 유지

---

## Boundary Track 치환 (Track A)

| 항목 | Logic | Boundary |
|---|---|---|
| 선언 | `Layer: entity \| Track: Logic` | `Layer: boundary \| Track: UI` |
| `src/` | `src/entity/` | `src/validate_lines.py` (+ 필요 Entity) |
| assert | Entity 반환값 | `result["status"]`, `result["failed_lines"]` |
| ECB | Entity만 구현 | Controller가 Entity 호출; Boundary는 공개 API만 assert |

---

## pytest 명령 (필수 실행)

### 1) 단일 테스트 (묶음 내 1 Test ID)

```bash
pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v
```

### 2) 파일 전체 (회귀·묶음 전체)

```bash
pytest tests/test_entity_line.py -v
```

Boundary 예:

```bash
pytest tests/test_validate_lines.py::test_행1_합이_34가_아니면_failed_lines에_R1 -v
pytest tests/test_validate_lines.py -v
```

**기대:** 이번 묶음 Test ID **전부 PASSED**. 기존 통과분 **회귀 없음**.  
회귀 실패 시 보고 전에 **즉시 수정**하고 pytest 재실행.

---

## git commit

| 규칙 | 내용 |
|---|---|
| **시점** | 사용자가 **명시적으로 요청할 때만** |
| **단위** | **1커밋 = 1 RED 묶음** (해당 Test ID + 최소 `src/` + assert 교체) |
| **메시지** | 묶음 Test ID 범위 포함 (예: `green: T-LOG-001~003 sum_line 최소 구현`) |

사용자 요청 없이 `git commit` **실행하지 않는다**.

---

## 금지 (본 커맨드)

| 금지 | 이유 |
|---|---|
| 이번 RED 묶음 **외** Test ID 동시 해결 | 1묶음=1GREEN 추적성 |
| REFACTOR (중복 제거·구조 개편·이름 일괄 변경) | 별도 단계 |
| assert 완화·skip·xfail·`pytest.fail` 잔존 | RED 회피 (E003/E004) |
| 하드코딩·매직넘버 | constants SSOT |
| Entity → Controller/Boundary import | ECB 위반 |
| 솔버·정답 테이블·범위 밖 기능 | E005 |
| 사용자 미요청 `git commit` | `.cursorrules` |

---

## 보고 형식

```markdown
Phase: green | Layer: entity | Track: Logic

## PASS Test ID
| Test ID | 함수명 | 결과 |
|---|---|---|
| T-LOG-001 | `test_d_loc_01_blank_coords_row_major` | PASSED |

## 변경 파일
- `src/entity/line.py` — `sum_line` 최소 구현
- `tests/test_entity_line.py` — pytest.fail → assert 교체
- `src/constants.py` — (해당 시만) 상수 추가

## pytest 결과
- 단일: `pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v` → 1 passed
- 전체: `pytest tests/test_entity_line.py -v` → N passed, 0 failed

## 회귀
- 없음 / (있었으면) 즉시 수정 후 재실행 결과

## 다음 단계
- 다음 RED 묶음: `/red-skeleton` 또는 REFACTOR: 별도 커맨드
- commit: 사용자 요청 시 1묶음 1커밋
```

회귀가 있으면 **PASS Test ID 보고 전에** 수정·재실행 결과를 반드시 포함한다.

---

## ARRR · TDD 위치

| 단계 | 커맨드 | 산출 |
|---|---|---|
| RED ③ | `/red-test-plan` | C2C 설계표 |
| RED ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| **GREEN** | **`/green-minimal`** | **`src/` 최소 구현 + assert PASS** |
| REFACTOR | (별도) | 동작 유지 정리 |

`.cursorrules`: GREEN = `src/`만 수정; 본 커맨드는 assert 교체를 위해 **동일 묶음 `tests/`만** 함께 수정한다.

---

## 참조

| 문서 | 역할 |
|---|---|
| `.cursor/commands/red-test-plan.md` | RED 묶음·Test ID·Then |
| `.cursor/commands/red-skeleton.md` | 스켈레톤·conftest·pytest.fail |
| `.cursor/commands/tdd-red.md` | Boundary RED assert 형식 |
| `.cursorrules` | ECB·API·TDD·commit 규칙 |
| `src/constants.py` | 상수 SSOT |

### 완료 조건

- [ ] RED 묶음 전 Test ID PASSED
- [ ] `pytest.fail` 제거, 설계 Then과 동등한 assert
- [ ] 하드코딩 없음, constants SSOT
- [ ] E001~E005·ECB 위반 없음
- [ ] 파일 전체 pytest 회귀 없음 (실패 시 즉시 수정)
- [ ] commit은 사용자 요청 시만

---

*ARRR Respond: GREEN = RED 1묶음 최소 구현. 1커밋=1묶음. REFACTOR는 여기서 하지 않는다.*
