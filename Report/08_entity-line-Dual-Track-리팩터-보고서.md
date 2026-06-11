# entity line Dual-Track REFACTOR — MagicSquare_xx

## 1. 문서 목적

- `src/entity/line.py`를 **Dual-Track TDD** 기준으로 **Logic Track**·**UI Track**으로 분리한 REFACTOR 세션 산출을 기록한다.
- ARRR Refine 단계(`/refactor-safe`) 완료 상태·pytest·golden matched 결과를 SSOT로 남긴다.
- 후속 Entity/Controller REFACTOR(`/refactor-smell` → `/refactor-safe`) 시 Track 분리 패턴 참조용.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `docs/PRD.md` | FR-010~011·§12 Traceability·NFR-007 Change Budget |
| `.cursorrules` | ECB·TDD·검증 순서 |
| `Report/06_validate_lines-GREEN-Golden-Master-보고서.md` | GREEN+Golden 선행 (line.py 단일 파일) |
| `Report/04_ARRR-TDD-Command-Skill-체인-보고서.md` | Dual-Track·`/refactor-safe` 체인 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | Track B(Logic)·Track A(UI) 표·Budget |
| `Prompting/08_entity-line-Dual-Track-리팩터-프롬프트.md` | 본 보고서 재생성용 프롬프트 |

---

## 3. 세션 요약

| 단계 | Track | 산출 | 결과 |
|---|---|---|---|
| 전제 | Logic+UI | `pytest tests/ -v` | 6 passed |
| REFACTOR 1 | **Logic** | `src/entity/line_logic.py` 신규 | 순수 함수 추출 |
| REFACTOR 2 | **UI** | `src/entity/line.py` facade | constants·공개 API만 |
| 회귀 | Logic+UI | `pytest tests/ -v` | 6 passed · golden matched |

**Phase 선언:** `Phase: refactor | Layer: entity | Track: Logic` → `Phase: refactor | Layer: entity | Track: UI`

---

## 4. Track 분리 설계

### 4.1 Logic Track — `src/entity/line_logic.py`

| 함수 | 역할 | 제약 |
|---|---|---|
| `sum_line(cells)` | 4칸 선 합 | `sum(cells)` |
| `line_sum_equals(cells, magic_constant)` | 합 == 마법상수 여부 | **기본값 없음**, `constants` import **금지** |

- I/O·상태 없음 (Entity 순수 함수)
- Controller/Boundary import **없음**

### 4.2 UI Track — `src/entity/line.py`

| 항목 | 역할 |
|---|---|
| `line_sum_matches_magic(cells, magic_constant=MAGIC_CONSTANT)` | 공개 API — `line_logic.line_sum_equals` 위임 |
| `sum_line` re-export | 기존 import 경로 유지 (`from entity.line import sum_line`) |
| `__all__` | `["sum_line", "line_sum_matches_magic"]` |

- `constants.MAGIC_CONSTANT` 연결만 담당
- **로직 코드 없음** — Logic Track에 위임

### 4.3 ECB 정합

```
Logic Track   entity/line_logic.py   sum_line, line_sum_equals
UI Track      entity/line.py         공개 API + constants 연결
Controller    validate_lines.py      entity.line만 import (변경 없음)
Boundary      tests/test_entity_line.py, test_validate_lines.py  (변경 없음)
```

---

## 5. 변경 파일

| 경로 | 변경 | Track |
|---|---|---|
| `src/entity/line_logic.py` | **신규** — 순수 로직 | Logic |
| `src/entity/line.py` | facade로 축소 | UI |
| `src/validate_lines.py` | 변경 없음 | — |
| `tests/` | 변경 없음 | — |

---

## 6. Change Budget

| 항목 | 사용량 | 상한 | 판정 |
|---|---|---|---|
| 파일 | 2 | ≤ 3 | ✓ |
| 클래스 | 0 | ≤ 1 | ✓ |
| 메서드 | 3 | ≤ 3 | ✓ |

동작 불변: 공개 함수 시그니처·반환값·`validate_lines` 계약 유지.

---

## 7. pytest·golden

### 7.1 리팩터 전

```powershell
pytest tests/ -v
# → 6 passed
```

### 7.2 리팩터 후

```powershell
pytest tests/ -v
# → 6 passed
```

| Test ID | Track | 결과 |
|---|---|---|
| T-LOG-001 | Logic | PASS |
| T-LOG-002 | Logic | PASS |
| T-BND-001~004 | UI (Boundary) | PASS |

- golden: `UPDATE_GOLDEN` **없이** 6/6 matched
- ISS·golden 갱신: **불필요**

---

## 8. 금지 준수 (E001~E005)

| 코드 | 본 세션 |
|---|---|
| E001 | Budget 내 2파일만 변경 |
| E002 | Domain Mock 없음 |
| E003 | skip/xfail 없음 |
| E004 | assert 완화·테스트 삭제 없음 |
| E005 | 기능 추가·솔버 없음 |

---

## 9. 미완·후속

| 항목 | 상태 | 제안 |
|---|---|---|
| `validate_lines.py` REFACTOR | 미실행 | `/refactor-smell` → P0 1건 → `/refactor-safe` |
| `serialize.py` Track 분리 | 미실행 | golden 직렬화는 별 RF |
| `status == "pass"` 케이스 | 미테스트 | RED 1건 → GREEN (Report/06 후속) |
| git commit | 미실행 | 사용자 요청 시 |

---

## 10. ARRR · TDD 위치

| ARRR | Command | 본 세션 |
|---|---|---|
| Ask | `/red-test-plan` | Report/05 (선행) |
| Respond | `/green-minimal`, `/golden-master` | Report/06 (선행) |
| **Refine** | **`/refactor-safe`** | **§3~§7 완료** |

---

*작성 기준: MagicSquare_xx 세션 3 · entity line Dual-Track REFACTOR · 2026-06-11*
