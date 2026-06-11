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

*작성 기준: MagicSquare_xx 세션 3 · GREEN+Golden Master · 2026-06-10 (export 갱신)*
