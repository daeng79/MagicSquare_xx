# MagicSquare_xx — Product Requirements Document (PRD)

> **SSOT:** 본 문서는 기능 요구(FR)·성공 기준(SC)·Invariant·API 계약의 단일 진실 공급원이다.  
> `.cursorrules`·`magic-square-tdd` Skill·`/red-test-plan`이 본 PRD를 우선 참조한다.

| 항목 | 값 |
|---|---|
| 프로젝트 | MagicSquare_xx (MagicSquare_1004 세션 3+) |
| 버전 | 0.1.0-draft |
| 작성일 | 2026-06-10 |
| 저장소 | `daeng79/MagicSquare_xx` |

---

## 1. 문서 목적

4×4 부분 마방진 실습에서 **막혔을 때 판단 기준을 구조적으로 드러내는** 검증 시스템의 요구사항을 정의한다. Mom Test 증거·세션 3 워크북·`validate_lines` 계약 정합성 확인을 통합한다.

### 근거 문서

| 문서 | 역할 |
|---|---|
| `Report/01_4x4-마방진-MomTest-인터뷰-보고서.md` | Mom Test 증거·진짜 문제 |
| `Report/02_MagicSquare_1004-세션3-워크북-보고서.md` | R-G-I-O·SC-1~3·Rule |
| `Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md` | API 2계층 분리 권장 |
| `Report/04_ARRR-TDD-Command-Skill-체인-보고서.md` | Dual-Track TDD·Command 체인 |
| `.cursorrules` | ECB·TDD·검증 순서 |

---

## 2. 문제 정의 (Mom Test)

### 2.1 페르소나

4×4 **부분 마방진**(빈칸 2개)을 손으로/코드로 다루는 **학습자**. ECB·설계 연습 중 빈칸 맞추기 단계에서 **다중 제약 판단**에 어려움을 겪는다.

### 2.2 진짜 문제 (한 문장)

> 여러 제약(행·열·대각선)이 겹친 상태에서, 중간에 어디가 틀렸는지·다음에 무엇을 확인할지 판단할 수 없어 20분을 쓰고도 진행을 이어가지 못하고, 같은 유형의 과제를 다시 열지 않게 된다.

### 2.3 Mom Test 증거

| # | 과거 사실 | ID |
|---|---|---|
| ① | 대각선 합 34 맞추다 **합 불일치** → **즉시 실습 종료** | `diagonal_stall` |
| ② | **20분** 투입 후 다음 확인 단계 없이 중단 | `20min_abort` |
| ③ | 비슷한 과제 **재시도·재개 없음** | `no_retry` |

### 2.4 표면 문제 (금지 — 본 PRD 범위 밖)

- 4×4 마방진 **정답 자동 채우기 솔버**
- **대각선 검증 함수만** 따로 추가하는 것을 목표로 삼기
- TDD/pytest **도입 자체**를 제품 목표로 삼기
- UI / DB / Web 레이어
- 알고리즘 난이도·풀이 속도 개선

---

## 3. 제품 목표

| | 내용 |
|---|---|
| **Vision** | 막혔을 때 **어느 제약이 깨졌는지**와 **다음 확인 순서**를 재현 가능하게 고정한다 |
| **Goal** | "거의 맞음"과 "틀림"을 중간에 구분하고, 종료 대신 **구조적 피드백**을 반환한다 |
| **Non-Goal** | 정답 두 칸을 대신 찾아주는 것 |

---

## 4. R-G-I-O

| | 내용 |
|---|---|
| **Role** | 4×4 부분 마방진(빈칸 2개, 합 34) 실습 학습자 |
| **Goal** | 위반 위치·유형 드러내기 + 다음 확인 한 걸음 (20분 포기·재개 없음 패턴 차단) |
| **Input** | `grid: list[list[int]]` 4×4 — `0`=빈칸(정확히 2개), 채움 `1~16`, 0 제외 중복 금지 |
| **Output (전체)** | 제약별 통과/실패 + 위반 `{type, location, actual, expected}` + **다음 확인 1건** |

> **계약 분리 (Report/03):** Output 전체는 **`diagnose(grid)`** 책임. 본 세션 구현 핵심은 하위 API **`validate_lines(grid)`** (line 합 검증, SC-1).

---

## 5. 성공 기준 (SC)

| ID | 성공 기준 | Mom Test | validate_lines 단독 | 상위 diagnose |
|---|---|---|---|---|
| **SC-1** | 합 불일치 시 **어느 줄·현재 합·목표(34) 차이** 출력 | ① | ✅ 직접 | ✅ |
| **SC-2** | 검증 **순서·우선순위** 문서·Rule 고정 | ① | ⚠️ 부분 | ✅ |
| **SC-3** | 막힘 시 **종료 대신** 위반 목록 + **다음 한 걸음** | ②③ | ❌ | ✅ |

---

## 6. 기능 요구 (FR)

### 6.1 현재 세션 범위 — `validate_lines` (Track A · Boundary)

| ID | 요구 | SC | 우선순위 |
|---|---|---|---|
| **FR-001** | 4×4 `grid` 입력을 받아 **10선** 각각 합을 계산한다 | SC-1 | P0 |
| **FR-002** | 합 ≠ `MAGIC_CONSTANT`(34)인 선 ID를 `failed_lines`에 포함한다 | SC-1 | P0 |
| **FR-003** | `status`를 `pass` \| `fail` \| `incomplete` 중 하나로 반환한다 | SC-1, SC-2 | P0 |
| **FR-004** | `pass`: 10선 모두 합=34 | — | P0 |
| **FR-005** | `fail`: 하나 이상 합≠34 (빈칸 유무 무관) | SC-1 | P0 |
| **FR-006** | `incomplete`: 행·열(R1~R4,C1~C4) 통과 + 대각선(D1/D2) 중 하나 이상 실패 | SC-2 | P0 |
| **FR-007** | 검증 순서 `R1→R2→R3→R4→C1→C2→C3→C4→D1→D2` 고정 | SC-2 | P0 |
| **FR-008** | 빈칸(0)이 있어도 **합 계산 수행**; 전 선 통과 전까지 완료 아님 | SC-1 | P0 |
| **FR-009** | 공개 API 시그니처: `validate_lines(grid) -> {status, failed_lines}` | — | P0 |

### 6.2 Entity 계층 — Track B · Logic

| ID | 요구 | SC | 우선순위 |
|---|---|---|---|
| **FR-010** | `sum_line(cells)` — 한 선(4칸) 합 반환 | SC-1 | P0 |
| **FR-011** | `line_sum_matches_magic(cells, magic_constant)` — 합이 마법상수와 일치 여부 | SC-1 | P0 |
| **FR-012** | Entity는 I/O·상태·Controller/Boundary import 없음 (순수 함수) | — | P0 |

### 6.3 후속 세션 — `diagnose` (상위 Contract, 본 PRD에만 정의)

| ID | 요구 | SC | 우선순위 |
|---|---|---|---|
| **FR-020** | `diagnose(grid)` — line 위반 + 중복·범위 검증 통합 | SC-1~3 | P1 |
| **FR-021** | 위반 시 `{type, location, actual, expected}` 반환 | SC-1 | P1 |
| **FR-022** | `next_check` — 막힘 시 다음 확인 제약 1건 | SC-3 | P1 |
| **FR-023** | Rule `NO_PARTIAL_SATISFACTION` — 행·열만 OK여도 대각선 실패 시 미완료 | SC-2 | P1 |

---

## 7. Invariant (불변 조건)

| ID | Invariant | SSOT |
|---|---|---|
| **INV-001** | 마법상수 = **34** | `src/constants.py` → `MAGIC_CONSTANT` |
| **INV-002** | 격자 크기 = **4×4** | `GRID_SIZE = 4` (정의 예정) |
| **INV-003** | 셀 값: `0` 또는 **1~16** | `MAX_CELL_VALUE = 16` (정의 예정) |
| **INV-004** | 10선 ID: `R1~R4`, `C1~C4`, `D1`, `D2` | `LINE_IDS` |
| **INV-005** | 검증 순서 = `VERIFICATION_ORDER` | `constants.py` |
| **INV-006** | 부분 만족 ≠ 완료 (`incomplete` 존재) | FR-006 |
| **INV-007** | Golden 페이로드: `int[6]` **1-index** 6슬롯 + `Exxx` | `golden-master` Command |
| **INV-008** | 하드코딩 `34`/`16`/`4` 금지 — constants import | GREEN·REFACTOR |

---

## 8. API 계약 (Contract)

### 8.1 `validate_lines` (현재 구현 대상)

```python
validate_lines(grid: list[list[int]]) -> {
    "status": Literal["pass", "fail", "incomplete"],
    "failed_lines": list[str]  # 실패한 선 ID, 예: ["R1", "D1"]
}
```

| status | 조건 |
|---|---|
| `pass` | 10선 모두 합 = 34 |
| `fail` | 하나 이상 합 ≠ 34 |
| `incomplete` | R1~R4·C1~C4 통과, D1 또는 D2 실패 |

**미명시 (Contract 후속):** 빈칸 포함 줄의 합 판정 — 0을 합에 **포함**하여 계산 (`.cursorrules` 기본). 구현 시 테스트로 고정.

### 8.2 `diagnose` (후속 — 시그니처 초안)

```python
diagnose(grid: list[list[int]]) -> {
    "status": str,
    "violations": list[{ "type", "location", "actual", "expected" }],
    "next_check": str | None
}
```

---

## 9. ECB 아키텍처

| 계층 | 역할 | 위치 | 테스트 |
|---|---|---|---|
| **Entity** | 선 합 계산, 34 비교 | `src/entity/` | Track B · `tests/test_entity_*.py` |
| **Controller** | 고정 순서 검증, status·failed_lines 조립 | `src/validate_lines.py` | Controller는 Entity 단위 테스트 간접 |
| **Boundary** | 공개 API 계약 | `tests/test_validate_lines.py` | Track A |

**금지:** Entity → Controller/Boundary import · 솔버 · UI · DB

---

## 10. Dual-Track TDD

| Track | Layer | 대상 | Test ID |
|---|---|---|---|
| **A (UI)** | `boundary` | `validate_lines` | `T-BND-{nnn}` |
| **B (Logic)** | `entity` | `sum_line`, `line_sum_matches_magic` | `T-LOG-{nnn}` |

### ARRR · Command 체인

| ARRR | Command | Phase |
|---|---|---|
| Ask | `/red-test-plan`, `/red-skeleton` | RED |
| Respond | `/green-minimal`, `/golden-master` | GREEN |
| Refine | `/refactor-smell`, `/refactor-safe` | REFACTOR |

### C2C (Contract-to-Code)

| Rule | 내용 |
|---|---|
| Rule1 | FR(또는 SC) **1개** → To-Do **1개** |
| Rule2 | To-Do 1개 = Test ID 1개 = RED 1사이클 |
| Rule3 | Test ID마다 Given / When / Then 고정 |

---

## 11. Rule (도메인)

```yaml
rules:
  - id: FAIL_WITH_VIOLATION_TYPE
    when: constraint_check_fails
    then: report { type, location, actual, expected }  # FR-021

  - id: NO_PARTIAL_SATISFACTION
    when: row_col_pass AND diagonal_fail
    then: status = incomplete  # FR-006

  - id: FIXED_VERIFICATION_ORDER
    order: [R1, R2, R3, R4, C1, C2, C3, C4, D1, D2]  # FR-007

  - id: MOM_TEST_ALIGNMENT
    evidence: [diagonal_stall, 20min_abort, no_retry]
```

---

## 12. Traceability (SC → FR → Test)

| SC | FR | Test ID (예) | RED 시나리오 |
|---|---|---|---|
| SC-1 | FR-001,002,010,011 | T-BND-001 | R1 합≠34 → `failed_lines`에 `R1` |
| SC-1 | FR-001,002 | T-BND-002 | D1 합≠34 → `failed_lines`에 `D1` |
| SC-2 | FR-006,007 | T-BND-003 | 행·열 OK·D1 실패 → `incomplete` |
| SC-2 | FR-007 | T-BND-004 | 검증 순서 준수 (Controller) |
| SC-3 | FR-022 | (후속) | `next_check` 비어 있지 않음 |
| SC-1 | FR-010 | T-LOG-001 | `sum_line` 4칸 합 |
| SC-1 | FR-011 | T-LOG-002 | `line_sum_matches_magic` vs 34 |

---

## 13. 품질·프로세스 요구

| ID | 요구 |
|---|---|
| **NFR-001** | Python ≥ 3.10, pytest ≥ 8.0 |
| **NFR-002** | TDD: RED → GREEN → REFACTOR, **한 번에 한 Phase** |
| **NFR-003** | RED: `tests/`만 · GREEN: `src/` (+ 동일 묶음 assert) |
| **NFR-004** | skip/xfail·assert 완화로 RED 회피 금지 |
| **NFR-005** | 1커밋 = 1 RED 묶음 (사용자 요청 시) |
| **NFR-006** | Golden Master: `UPDATE_GOLDEN` 통제, 수동 편집 우회 금지 |
| **NFR-007** | REFACTOR Change Budget: 파일≤3, 클래스≤1, 메서드≤3 |

### E001~E005 (품질 게이트)

| 코드 | 금지 |
|---|---|
| E001 | 범위 밖 일괄 변경 |
| E002 | Domain Mock (Logic Track) |
| E003 | skip / xfail |
| E004 | assert 완화 |
| E005 | 솔버·정답 채우기·범위 밖 기능 |

---

## 14. 구현 상태 (2026-06-10)

| 항목 | 상태 |
|---|---|
| `src/constants.py` | `MAGIC_CONSTANT`, `LINE_IDS`, `VERIFICATION_ORDER` |
| `src/entity/line.py` | stub (`...`) |
| `src/validate_lines.py` | stub (`...`) |
| `tests/test_validate_lines.py` | import만 |
| FR-001~012 | **미구현** (RED/GREEN 대기) |
| FR-020~023 | **후속 세션** |
| `docs/PRD.md` | **본 문서** |

---

## 15. 용어

| 용어 | 정의 |
|---|---|
| **10선** | 행 4 + 열 4 + 대각선 2 (D1↘, D2↙) |
| **마방진** | 1~16을 한 번씩 쓰는 4×4 배치 (본 프로젝트는 부분 격자 허용) |
| **RED 묶음** | 동일 Track·Layer의 연속 Test ID 집합 |
| **Approval Test** | `tests/golden/{id}.approved.txt` golden master |

---

*PRD SSOT · MagicSquare_xx · Mom Test + 세션 3 워크북 + validate_lines 정합성 통합 · 2026-06-10*
