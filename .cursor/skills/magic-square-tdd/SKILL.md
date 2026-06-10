---
name: magic-square-tdd
description: >-
  MagicSquare_xx Dual-Track TDD(ARRR·C2C·ECB) 워크플로를 적용한다.
  Use when Phase is red|green|refactor, or user runs Commands
  /red-test-plan, /red-skeleton, /green-minimal, /golden-master,
  /refactor-smell, /refactor-safe, or mentions TDD, RED, GREEN, REFACTOR,
  Dual-Track, C2C, pytest.fail, validate_lines, MagicSquare.
disable-model-invocation: true
---

# magic-square-tdd

MagicSquare_xx 4×4 마방진 검증 프로젝트의 **Dual-Track TDD** 단일 진실 공급원(SSOT) Skill.  
명시적 Command·Skill 호출 시에만 적용한다 (`disable-model-invocation: true`).

## SSOT (반드시 Read)

| 문서 | 역할 |
|---|---|
| `.cursorrules` | API·ECB·검증 순서·TDD 사이클·금지 |
| `docs/PRD.md` | FR-*·Invariant·Mom Test SC (없으면 `.cursorrules`+`Report/` 추론, `(추론)` 표기) |

**도메인 요약:** 4×4 `grid`, `0`=빈칸, 1~16, 마법상수 34, 10선 `R1~R4·C1~C4·D1·D2`, 검증 순서 고정.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | Command | 산출 |
|---|---|---|---|
| **Ask** | RED ③④ | `/red-test-plan` | C2C 설계표·플랜 (파일 없음) |
| **Ask** | RED ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 (`tests/`만) |
| **Respond** | GREEN | `/green-minimal` | `src/` 최소 구현 + assert PASS |
| **Respond** | GREEN+ | `/golden-master` | `tests/golden/*.approved.txt` |
| **Refine** | REFACTOR ⑦ | `/refactor-smell` | 스멜 표 (수정 없음) |
| **Refine** | REFACTOR ⑧ | `/refactor-safe` | Budget 내 리팩터 |

**한 번에 한 Phase만.** RED 중 `src/` 수정 금지. GREEN 중 REFACTOR 금지.

---

## 2. Phase 선언 (응답 첫 줄)

```
Phase: red   | Layer: {entity|boundary} | Track: {Logic|UI}
Phase: green | Layer: {entity|boundary} | Track: {Logic|UI}
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI     # smell
Phase: refactor | Layer: {entity|boundary} | Track: {Logic|UI}  # safe
```

`.cursorrules` 레거시 `Phase: RED`/`GREEN`/`REFACTOR` 대신 **Command 체인에서는 위 형식 우선**.

---

## 3. C2C Rule 1~3

| Rule | 내용 |
|---|---|
| **Rule1** | PRD FR(또는 SC) **1개** → To-Do **1개** |
| **Rule2** | To-Do 1개 = Test ID 1개 = RED 사이클 1개 |
| **Rule3** | Test ID마다 **Given / When / Then** 고정 (AAA 대응) |

**Test ID:** Logic `T-LOG-{nnn}` · UI `T-BND-{nnn}`.

---

## 4. RED 절대 금지

| 금지 | 이유 |
|---|---|
| `src/` 수정 | GREEN 전용 |
| `@pytest.mark.skip`, `xfail` | RED 회피 (E003) |
| assert 완화·테스트 삭제 | RED 회피 (E004) |
| **Logic Track Domain Mock** | Entity `patch`/`Mock` 금지 (E002) |
| 솔버·정답 채우기·범위 밖 기능 | E005 |
| `red-test-plan`에서 `tests/`·`src/` Write | ③=설계만 |

**스켈레톤 Then:** `pytest.fail("RED: {Test ID} — …")` **한 줄만** — assert 본문·통과 더미 금지.

**E001~E005 emit 금지** (플랜·스켈레톤 산출에 넣지 않음).

---

## 5. GREEN 규칙

| 규칙 | 내용 |
|---|---|
| **범위** | RED **1묶음** Test ID만 통과시키는 최소 `src/` |
| **assert** | `pytest.fail` → 설계 Then과 동등한 assert |
| **상수** | `34`/`16`/`4` 리터럴 금지 → `constants.py` SSOT (`MAGIC_CONSTANT` 등) |
| **ECB** | Entity는 Controller/Boundary import 금지 |
| **커밋** | **1커밋 = 1 RED 묶음**, 사용자 요청 시만 |
| **금지** | 묶음 외 ID 동시 해결, REFACTOR, E001~E005 |

---

## 6. REFACTOR 규칙

| 규칙 | 내용 |
|---|---|
| **smell** | 탐지만 — 수정·commit 금지 |
| **safe** | `/refactor-smell` 표에서 **스멜 1건** (RF-xxx) |
| **Change Budget** | 파일≤3 · 클래스≤1 · 메서드≤3 |
| **동작 불변** | 입출력·예외·`int[6]` 1-index·`Exxx` 의미 변경 금지 |
| **golden** | `UPDATE_GOLDEN` 없이 matched; 비의도 diff → **롤백**; 의도적 → ISS + `UPDATE_GOLDEN=1` |
| **금지** | 기능 추가·버그 수정 (별도 GREEN) |

---

## 7. Track A (UI) vs Track B (Logic)

| | **Track A — UI (Boundary)** | **Track B — Logic (Entity)** |
|---|---|---|
| Layer | `boundary` | `entity` |
| 대상 | `validate_lines(grid)` 공개 API | `src/entity/` 순수 함수 |
| 테스트 | `tests/test_validate_lines.py` | `tests/test_entity_*.py` |
| Test ID | `T-BND-{nnn}` | `T-LOG-{nnn}` |
| Act | `result = validate_lines(grid)` | Entity 함수 직접 호출 |
| Assert | `status`, `failed_lines` | 반환값·불변식 |
| Mock | Boundary는 실제 Controller 경로 | **Domain Mock 금지** |
| ECB | 공개 API만; Entity private assert 금지 | Entity만; Controller/Boundary import 금지 |

Track B 설계를 Track A에 쓸 때: `Layer: boundary`, `Track: UI`, 파일·함수만 Boundary 기준 치환.

---

## 8. Command 체인

```
/red-test-plan          → C2C 4블록, "/red-skeleton 으로 넘길 준비됐다"
/red-skeleton           → tests/ pytest.fail 스켈레톤
/green-minimal          → src/ 최소 구현 + assert PASS
/golden-master          → tests/golden/{id}.approved.txt (선택·회귀 잠금)
/refactor-smell         → 스멜 표 + RF 후보 1~3 (P0 1개 → safe)
/refactor-safe [RF-nnn] → Budget 내 리팩터 1건
```

각 Command 상세: `.cursor/commands/{name}.md`. Command 실행 시 **본 Skill 자동 따름**.

---

## 9. pytest 명령 패턴

```bash
# 전제·회귀 (smell/safe/golden 전)
python -m pytest tests/ -v

# RED 묶음·단일 Test ID
pytest tests/test_entity_line.py -v
pytest tests/test_entity_line.py::test_d_loc_01_blank_coords_row_major -v

# Boundary
pytest tests/test_validate_lines.py::test_<이름> -v

# Golden 기준 생성 (최초·ISS 후만)
UPDATE_GOLDEN=1 pytest tests/<파일>::<함수> -v

# Golden matched (UPDATE_GOLDEN 없음)
pytest tests/ -v
```

**기대:** RED=skeleton `FAILED`(fail 메시지) · GREEN/safe=전부 `PASSED` · golden=matched.

---

## 10. 완료 보고 형식

### red-test-plan

```markdown
Phase: red | Layer: entity | Track: Logic
## 1. C2C … ## 2. Track B … ## 3. 테스트 플랜 … ## 4. ECB·Mock …
/red-skeleton 으로 넘길 준비됐다
```

### red-skeleton

```markdown
Phase: red | Layer: entity | Track: Logic
| Test ID | 함수명 | FAIL 메시지 (한 줄) |
## 변경 파일 (tests/만)
```

### green-minimal

```markdown
Phase: green | Layer: entity | Track: Logic
## PASS Test ID | ## 변경 파일 | ## pytest (단일+전체) | ## 회귀
```

### golden-master

```markdown
Phase: green | Layer: entity | Track: Logic
## golden 경로 | matched: yes/no | diff 요약 (한 줄)
```

### refactor-smell

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
## pytest 전제 | ## 스멜 표 | ## /refactor-safe 후보
## 다음: P0 1개 → /refactor-safe
```

### refactor-safe

```markdown
Phase: refactor | Layer: entity | Track: Logic
## 대상 RF-xxx | ## 변경 요약 | ## Budget | ## pytest | ## golden matched
```

---

## ECB 빠른 참조

```
Entity     src/entity/     순수 함수, I/O 없음
Controller src/validate_lines.py  VERIFICATION_ORDER 고정
Boundary   tests/          공개 API만
```

검증 순서: `R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2`

---

## Golden 페이로드 (고정)

```
I:{int6 1-index, 6개, 콤마}   예: I:1,2,3,3,0,0
E:{Exxx}                      예: E:E000
```

`tests/_approval.py` → `assert_matches_golden(test_id, actual)`. 수동 편집 우회 금지.

---

## conftest·상수 (기본)

- `tests/conftest.py` — `grid_g1`: 4×4, 0 두 개, row-major
- 상수 import: `from constants import MAGIC_CONSTANT, GRID_SIZE, MAX_CELL_VALUE` (픽스처·assert만)
- SSOT: `entity/constants.py` 우선, 없으면 `src/constants.py`

---

## 소통·commit

- 사용자와 **한국어**; 코드 주석 **한국어**
- **git commit**은 사용자 명시 요청 시만
- 범위 밖(솔버, UI, DB, TDD 도구 도입) 제안·구현 금지

---

## 체크리스트 (Command 완료 시)

- [ ] SSOT Read (`.cursorrules`, `docs/PRD.md`)
- [ ] Phase 선언 첫 줄
- [ ] Track·Layer·Test ID traceability
- [ ] 해당 Phase 금지 목록 미위반
- [ ] pytest 실행·결과 보고
- [ ] 변경 파일 목록 명시
