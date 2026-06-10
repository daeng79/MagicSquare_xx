# PRD §12 Traceability RED 테스트 플랜 — MagicSquare_xx

## 1. 문서 목적

- `docs/PRD.md` §12 추적성 표(233–241행)에 정의된 **Test ID**(`T-LOG-001~002`, `T-BND-001~004`)에 대한 **Dual-Track RED 테스트 플랜**을 확정한다.
- ARRR Ask 단계(`/red-test-plan`) 산출물로, `/red-skeleton` 이전 **설계 전용** 문서이다 (`tests/`·`src/` 미작성).
- Mom Test **SC-1**(합 불일치 위치 드러내기)·**SC-2**(검증 순서·`incomplete` 규칙)를 현재 세션 `validate_lines`·Entity 범위에 매핑한다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `docs/PRD.md` | FR-*·SC-*·§12 Traceability SSOT |
| `.cursorrules` | API 계약·ECB·검증 순서·TDD 금지 |
| `Report/02_MagicSquare_1004-세션3-워크북-보고서.md` | SC-1~3·Rule·Test Loop |
| `Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md` | `validate_lines` / `diagnose` 2계층 분리 |
| `Report/04_ARRR-TDD-Command-Skill-체인-보고서.md` | `/red-test-plan`·Dual-Track 체인 |
| `Prompting/05_PRD-Traceability-RED-테스트-플랜-프롬프트.md` | 본 보고서 재생성용 프롬프트 |

---

## 3. 범위 요약

| 구분 | Test ID | 세션 | 비고 |
|---|---|---|---|
| **Track B (Logic)** | T-LOG-001, T-LOG-002 | 현재 | Entity — `sum_line`, `line_sum_matches_magic` |
| **Track A (UI / Boundary)** | T-BND-001 ~ T-BND-004 | 현재 | `validate_lines` 공개 API |
| **후속** | FR-022 (`next_check`) | 다음 세션 | `diagnose` 상위 Contract — 본 플랜 RED 대상 아님 |

**권장 RED 묶음 순서:** Logic `T-LOG-001~002` → Boundary `T-BND-001~004` (Entity 선행, Controller가 Entity 호출)

---

## 4. Track B — Logic (Entity)

**Phase:** `red` | **Layer:** `entity` | **Track:** `Logic`

### 4.1 C2C (Rule1~3)

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|---|---|---|---|---|---|---|
| Rule1 | **FR-010** — `sum_line(cells)` 한 선(4칸) 합 반환 | `sum_line`이 4개 정수 합을 반환하는 RED 테스트 작성 | T-LOG-001 | `cells = [7, 8, 9, 10]` (합 34) | `sum_line(cells)` 호출 | 반환값 `== 34` |
| Rule2 | **FR-011** — `line_sum_matches_magic(cells, magic_constant)` 합·마법상수 일치 여부 | `line_sum_matches_magic`이 합 34 여부를 bool로 반환하는 RED 테스트 작성 | T-LOG-002 | `cells = [7, 8, 9, 10]`, `magic_constant = 34` | `line_sum_matches_magic(cells, magic_constant)` 호출 | 반환값 `is True` |

> C2C Rule2 엄격 적용 시 불일치(`False`) 케이스는 **T-LOG-003**으로 분리 가능. PRD §12에는 T-LOG-002만 명시 — 1사이클 원칙 우선 시 **True 케이스만** RED.

### 4.2 RED 시나리오 명세

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---|---|---|---|---|
| T-LOG-001 | `sum_line` | `[7, 8, 9, 10]` → `34` | INV-001 마법상수 34 | stub `...` → 실패 |
| T-LOG-002 | `line_sum_matches_magic` | `[7,8,9,10]`, `magic_constant=34` → `True` | `MAGIC_CONSTANT`(34) | stub `...` → 실패 |

### 4.3 테스트 플랜

| 항목 | 내용 |
|---|---|
| **파일 경로** | `tests/test_entity_line.py` (신규) |
| **함수명** | `test_t_log_001_sum_line_four_cells` · `test_t_log_002_line_sum_matches_magic_true` |
| **conftest** | 없음 (Given은 테스트 내 리터럴) |
| **pytest** | `pytest tests/test_entity_line.py -v` |
| **RED 묶음** | `T-LOG-001`, `T-LOG-002` |

---

## 5. Track A — UI (Boundary)

**Phase:** `red` | **Layer:** `boundary` | **Track:** `UI`

### 5.1 C2C (Rule1~3)

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|---|---|---|---|---|---|---|
| Rule1 | **FR-002** — 합 ≠ 34인 선 ID를 `failed_lines`에 포함 | R1만 실패 격자로 `R1` 포함 검증 | T-BND-001 | `grid_r1_fail` | `validate_lines(grid)` | `status == "fail"`, `"R1" in failed_lines` |
| Rule2 | **FR-002** (D1) — D1 합 ≠ 34 → `failed_lines`에 `D1` | D1(↘) 실패 격자로 `D1` 포함 검증 | T-BND-002 | `grid_d1_fail` | `validate_lines(grid)` | `status == "fail"`, `"D1" in failed_lines` |
| Rule3 | **FR-006** — `incomplete`: 행·열 통과 + 대각선 실패 | 행·열 8선 OK·D1만 실패 → `incomplete` | T-BND-003 | `grid_incomplete_d1` | `validate_lines(grid)` | `status == "incomplete"`, `"D1" in failed_lines`, 행·열 ID 없음 |
| (추가) | **FR-007** — 검증 순서 고정 | 복수 선 실패 시 `failed_lines`가 `VERIFICATION_ORDER` 순 | T-BND-004 | `grid_multi_fail` | `validate_lines(grid)` | `failed_lines == ["R1", "R3", …]` 순서 준수 |

### 5.2 Given 격자 (픽스처 설계값)

**`grid_r1_fail`** — T-BND-001

```
R1 = [10, 10, 10, 10] → 합 40 ≠ 34
[
  [10, 10, 10, 10],
  [ 1,  2,  3,  4],
  [ 5,  6,  7,  8],
  [ 4,  5,  6,  7],
]
```

**`grid_d1_fail`** — T-BND-002 (D1 = (0,0)(1,1)(2,2)(3,3))

```
D1 = 10+2+7+4 = 23 ≠ 34
[
  [10,  1,  2,  3],
  [ 4,  2,  5,  6],
  [ 7,  8,  7,  9],
  [10, 11, 12,  4],
]
```

**`grid_incomplete_d1`** — T-BND-003 (행·열 8선 합 34, D1=40)

```
[
  [10, 10,  7,  7],   # R1=34
  [ 7, 10, 10,  7],   # R2=34
  [ 7,  7, 10, 10],   # R3=34
  [10,  7,  7, 10],   # R4=34 → C1~C4 각 34, D1=40, D2=34
]
```

**`grid_multi_fail`** — T-BND-004

```
R1·R3 동시 실패 (각 행 합 40)
[
  [10, 10, 10, 10],
  [ 1,  2,  3,  4],
  [10, 10, 10, 10],
  [ 4,  5,  6,  7],
]
기대 failed_lines 선두: ["R1", "R3", ...]
```

### 5.3 RED 시나리오 명세

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---|---|---|---|---|
| T-BND-001 | `validate_lines` | R1 합≠34 → `failed_lines`에 `R1` | FR-008: 빈칸 없어도 합 계산 | Controller stub `...` |
| T-BND-002 | `validate_lines` | D1 합≠34 → `failed_lines`에 `D1` | D1 = ↘ 대각선 4칸 | 동일 |
| T-BND-003 | `validate_lines` | 행·열 OK, D1 실패 → `incomplete` | INV-006 부분 만족 ≠ 완료 | 동일 |
| T-BND-004 | `validate_lines` | 복수 실패 → `failed_lines` = `VERIFICATION_ORDER` | INV-005 고정 순서 | 동일 |

### 5.4 테스트 플랜

| 항목 | 내용 |
|---|---|
| **파일 경로** | `tests/test_validate_lines.py` |
| **함수명** | `test_t_bnd_001_r1_in_failed_lines` · `test_t_bnd_002_d1_in_failed_lines` · `test_t_bnd_003_incomplete_row_col_ok_d1_fail` · `test_t_bnd_004_failed_lines_verification_order` |
| **conftest** | 신규: `grid_r1_fail`, `grid_d1_fail`, `grid_incomplete_d1`, `grid_multi_fail` |
| **pytest** | `pytest tests/test_validate_lines.py -v` |
| **RED 묶음** | `T-BND-001` ~ `T-BND-004` |

---

## 6. ECB·Mock 점검 (전 Test ID)

| 점검 항목 | Logic | Boundary |
|---|---|---|
| 계층 준수 | Entity만 직접 호출 | 공개 API만 assert |
| Domain Mock | **금지** | 실제 Controller 경로 |
| E001~E005 | **금지** (src 수정·skip·assert 완화·솔버) | 동일 |

**결과:** T-LOG-001~002, T-BND-001~004 전부 **PASS**

---

## 7. Traceability 매트릭스 (PRD §12)

| PRD 행 | SC | FR | Test ID | 본 플랜 |
|---|---|---|---|---|
| 235 | SC-1 | FR-001,002,010,011 | T-BND-001 | Boundary — R1 실패 |
| 236 | SC-1 | FR-001,002 | T-BND-002 | Boundary — D1 실패 |
| 237 | SC-2 | FR-006,007 | T-BND-003 | Boundary — `incomplete` |
| 238 | SC-2 | FR-007 | T-BND-004 | Boundary — 검증 순서 |
| 239 | SC-3 | FR-022 | (후속) | `diagnose` · `next_check` |
| 240 | SC-1 | FR-010 | T-LOG-001 | Logic — `sum_line` |
| 241 | SC-1 | FR-011 | T-LOG-002 | Logic — `line_sum_matches_magic` |

---

## 8. 실행 순서·다음 단계

```
/red-skeleton (Logic: T-LOG-001~002)
  → /green-minimal (Logic)
  → /red-skeleton (Boundary: T-BND-001~004)
  → /green-minimal (Boundary)
```

**완료 조건 (본 플랜):** `/red-skeleton 으로 넘길 준비됐다`

---

## 9. 구현 상태 (2026-06-10)

| 항목 | 상태 |
|---|---|
| `src/entity/line.py` | stub (`...`) |
| `src/validate_lines.py` | stub (`...`) |
| `tests/test_validate_lines.py` | import만 |
| `tests/test_entity_line.py` | **미생성** |
| `tests/conftest.py` | **미생성** (픽스처 설계만 확정) |

---

*작성 기준: MagicSquare_xx PRD §12 Traceability · ARRR Ask RED ③ · 2026-06-10*
