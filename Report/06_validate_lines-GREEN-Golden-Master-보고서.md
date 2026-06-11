# validate_lines GREEN·Golden Master·커버리지 — MagicSquare_xx

## 1. 문서 목적

- RED 스켈레톤(`T-LOG-001~002`, `T-BND-001~004`)에 대한 **GREEN 최소 구현**·**Golden Master(Approval Test)** 구축·**pytest-cov 커버리지** 절차를 세션 3 산출물로 기록한다.
- ARRR Respond 단계(`/green-minimal`, `/golden-master`) 완료 상태와 pytest·golden matched 결과를 SSOT로 남긴다.
- 후속 REFACTOR(`/refactor-smell`, `/refactor-safe`) 및 `pass` 케이스 RED 추가 시 참조한다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `docs/PRD.md` | FR-003~009·§8 API·§12 Traceability·INV-007 Golden |
| `.cursorrules` | ECB·검증 순서·TDD 사이클 |
| `Report/05_PRD-Traceability-RED-테스트-플랜-보고서.md` | Test ID·Given 격자·RED 묶음 |
| `Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md` | `validate_lines` / `diagnose` 2계층 |
| `Report/04_ARRR-TDD-Command-Skill-체인-보고서.md` | `/green-minimal`·`/golden-master` 체인 |
| `Prompting/06_validate_lines-GREEN-Golden-Master-프롬프트.md` | 본 보고서 재생성용 프롬프트 |

---

## 3. 세션 요약

| 단계 | Command | 산출 | 결과 |
|---|---|---|---|
| GREEN | `/green-minimal` | `src/` 최소 구현 + assert PASS | 6 passed |
| 커버리지 | (pytest-cov) | term-missing · html | 95% (40 stmts, 2 miss) |
| Golden | `/golden-master` | `tests/golden/*.approved.txt` | 6 matched |
| 검증 (export) | `/golden-master` 재확인 | `UPDATE_GOLDEN` 없이 전체 스위트 | 6 passed · diff 없음 |

**Phase 선언:** `Phase: green | Layer: entity+boundary | Track: Logic+UI`

---

## 4. GREEN 최소 구현

### 4.1 Entity (`src/entity/line.py`)

| 함수 | 역할 |
|---|---|
| `sum_line(cells)` | 4칸 합 `sum(cells)` |
| `line_sum_matches_magic(cells, magic_constant=MAGIC_CONSTANT)` | 합 == 마법상수 여부 |

### 4.2 Controller (`src/validate_lines.py`)

| 항목 | 구현 |
|---|---|
| 검증 순서 | `VERIFICATION_ORDER` 고정 (`R1→…→D2`) |
| 선 추출 | `_cells_for_line(grid, line_id)` — 행·열·D1↘·D2↙ |
| `failed_lines` | 순서대로 실패 선 ID 수집 |
| `status` | 10선 통과 → `pass` · 행·열 OK + 대 diagonal선만 실패 → `incomplete` · 그 외 → `fail` |

### 4.3 PASS Test ID

| Test ID | Track | 함수 | Then (요약) |
|---|---|---|---|
| T-LOG-001 | Logic | `test_t_log_001_sum_line_four_cells` | `sum_line([7,8,9,10]) == 34` |
| T-LOG-002 | Logic | `test_t_log_002_line_sum_matches_magic_true` | `line_sum_matches_magic(...) is True` |
| T-BND-001 | UI | `test_t_bnd_001_r1_in_failed_lines` | `status=="fail"`, `"R1" in failed_lines` |
| T-BND-002 | UI | `test_t_bnd_002_d1_in_failed_lines` | `status=="fail"`, `"D1" in failed_lines` |
| T-BND-003 | UI | `test_t_bnd_003_incomplete_row_col_ok_d1_fail` | `status=="incomplete"`, D1만, 행·열 ID 없음 |
| T-BND-004 | UI | `test_t_bnd_004_failed_lines_verification_order` | `failed_lines`가 `VERIFICATION_ORDER` 순 |

```bash
pytest tests/ -v   # → 6 passed
```

---

## 5. 커버리지 (pytest-cov)

### 5.1 명령

```powershell
# 터미널 요약 (미커버 줄 표시)
pytest tests/ --cov=src --cov-report=term-missing

# HTML 리포트 생성
pytest tests/ --cov=src --cov-report=html

# 둘 다
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# 브라우저 열기 (PowerShell)
Invoke-Item .\htmlcov\index.html
```

### 5.2 측정 결과 (GREEN 직후)

| 파일 | Cover | Missing |
|---|---|---|
| `src/constants.py` | 100% | — |
| `src/entity/line.py` | 100% | — |
| `src/validate_lines.py` | 94% | 31, 42행 |
| **TOTAL** | **95%** | 2 stmts |

**미커버 분기:**
- **31행** — 알 수 없는 `line_id` → `ValueError` (비정상 입력)
- **42행** — 10선 모두 통과 → `status = "pass"` (`pass` 케이스 테스트 미작성)

### 5.3 HTML 생성 이슈

- `--cov-report=term-missing`만 실행하면 `htmlcov/index.html`이 **생성되지 않음**.
- `htmlcov/`에 CSS/JS만 있고 `index.html` 없을 때 → `pytest tests/ --cov=src --cov-report=html` 재실행.
- `coverage` 패키지 정적 파일 누락(`keybd_closed.png`) 시: `pip install --force-reinstall coverage` 후 재생성.

---

## 6. Golden Master (Approval Test)

### 6.1 인프라

| 파일 | 역할 |
|---|---|
| `tests/_approval.py` | `assert_matches_golden(test_id, actual)` |
| `src/entity/serialize.py` | `I:/E:` · `S:/F:/E:` 직렬화 SSOT |
| `tests/golden/{TestID}.approved.txt` | golden 기준 (6개) |
| `pyproject.toml` | `pythonpath = ["src", "tests"]` (`_approval` import) |

### 6.2 페이로드 포맷

**Logic (Entity):**
```
I:{int6 1-index 6개}
E:E000
```
- 정수 결과: `format_entity_int_golden(value)` → `I:34,1,1,1,1,1`
- 불리언: `format_entity_bool_golden(True)` → `I:1,1,1,1,1,1` (1=True, 2=False)

**Boundary (`validate_lines`):**
```
S:{status}
F:{failed_lines 콤마 구분}
E:E000
```

### 6.3 golden 기준 예시

**T-BND-003** (`grid_incomplete_d1`):
```
S:incomplete
F:D1
E:E000
```
※ D2는 합 34로 통과 — `failed_lines`에 D1만 포함 (의도적).

**T-BND-004** (`grid_multi_fail`):
```
S:fail
F:R1,R2,R3,R4,C1,C2,C3,C4,D1,D2
E:E000
```

### 6.4 절차

```powershell
# 기준 생성 (최초·ISS 후만)
$env:UPDATE_GOLDEN="1"; pytest tests/ -v

# matched 검증
pytest tests/ -v
```

| Test ID | golden 경로 | matched |
|---|---|---|
| T-LOG-001 | `tests/golden/T-LOG-001.approved.txt` | yes |
| T-LOG-002 | `tests/golden/T-LOG-002.approved.txt` | yes |
| T-BND-001 | `tests/golden/T-BND-001.approved.txt` | yes |
| T-BND-002 | `tests/golden/T-BND-002.approved.txt` | yes |
| T-BND-003 | `tests/golden/T-BND-003.approved.txt` | yes |
| T-BND-004 | `tests/golden/T-BND-004.approved.txt` | yes |

**금지:** golden 파일 수동 편집으로 pytest 통과 우회.

---

## 7. 변경 파일 목록

| 경로 | 변경 |
|---|---|
| `src/entity/line.py` | GREEN — Entity 최소 구현 |
| `src/validate_lines.py` | GREEN — Controller 최소 구현 |
| `src/entity/serialize.py` | Golden — 직렬화 헬퍼 |
| `tests/test_entity_line.py` | GREEN assert + golden 연결 |
| `tests/test_validate_lines.py` | GREEN assert + golden 연결 |
| `tests/_approval.py` | Golden — approval 헬퍼 |
| `tests/golden/*.approved.txt` | Golden — 6개 기준 |
| `tests/conftest.py` | (RED) 4 픽스처 |
| `pyproject.toml` | `pythonpath`에 `tests` 추가 |

---

## 8. ECB·TDD 정합

```
Entity     src/entity/line.py, serialize.py   순수 함수
Controller src/validate_lines.py              VERIFICATION_ORDER 고정
Boundary   tests/test_*.py                     공개 API + golden
```

- Entity → Controller/Boundary import **없음** (serialize는 테스트·golden용으로 tests에서 import)
- 상수 SSOT: `MAGIC_CONSTANT` 등 `constants.py` import
- RED 묶음 6 Test ID 전부 PASS + golden matched

---

## 9. 미완·후속

| 항목 | 상태 | 제안 |
|---|---|---|
| `status == "pass"` 케이스 | 미테스트 | RED 1건 추가 → GREEN → golden |
| `ValueError` (잘못된 line_id) | 미커버 (31행) | Entity/Controller 단위 또는 Boundary 예외 정책 확정 후 |
| REFACTOR | 미실행 | `/refactor-smell` → P0 1건 → `/refactor-safe` |
| `diagnose` / FR-022 | 후속 세션 | Report/03 참조 |

---

## 10. ARRR · TDD 위치

| ARRR | Command | 본 세션 |
|---|---|---|
| Ask | `/red-test-plan`, `/red-skeleton` | Report/05 (선행) |
| **Respond** | **`/green-minimal`** | **§4 완료** |
| **Respond+** | **`/golden-master`** | **§6 완료** |
| Refine | `/refactor-smell`, `/refactor-safe` | 다음 |

---

## 11. 본 export 세션 검증 (2026-06-10)

사용자 요청: **Golden Master · Approval Test GREEN PASS 완료**.

| 점검 | 결과 |
|---|---|
| `pytest tests/ -v` | **6 passed** (0.05s) |
| `UPDATE_GOLDEN` 없이 golden | **6/6 matched** |
| `src/` 추가 수정 | **불필요** (이미 GREEN+Golden 완료 상태) |
| golden diff | 없음 |

**결론:** Respond(`/green-minimal`) + Respond+(`/golden-master`) 완료. 다음 단계는 Refine — `/refactor-smell` → `/refactor-safe`.

---

*작성 기준: MagicSquare_xx 세션 3 · GREEN+Golden Master · 2026-06-10 (export 갱신)*
