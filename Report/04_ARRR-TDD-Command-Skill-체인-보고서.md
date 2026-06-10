# ARRR TDD Command·Skill 체인 — MagicSquare_xx

## 1. 문서 목적

- MagicSquare_xx **Dual-Track TDD** 워크플로를 Cursor **Command 6종 + Skill 2종**으로 고정한다.
- ARRR(Ask·Respond·Refine)과 RED/GREEN/REFACTOR Phase를 **한 Command 체인**으로 추적 가능하게 한다.
- 세션 3 워크북(`Report/02`)의 Test Loop·Command 계층을 **실행 가능한 `.cursor/commands/`·`.cursor/skills/`** 산출물로 구체화한다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `.cursorrules` | API·ECB·TDD 사이클·검증 순서 |
| `Report/02_MagicSquare_1004-세션3-워크북-보고서.md` | Rule·Command·Test Loop (8계층) |
| `Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md` | `validate_lines` 계약 정합성 |
| `Prompting/04_ARRR-TDD-Command-Skill-체인-프롬프트.md` | 본 보고서·체인 재생성용 프롬프트 |
| GitHub `daeng79/MagicSquare_xx` | 원격 저장소 (MCP 조회 확인) |

---

## 3. 세션 산출 요약

### 3.1 Command 체인 (`.cursor/commands/`)

| 순서 | Command | ARRR·Phase | 역할 |
|---|---|---|---|
| ① | `/red-test-plan` | Ask · RED ③ | C2C 설계표·테스트 플랜 (파일 Write 없음) |
| ② | `/red-skeleton` | Ask · RED ④ | `pytest.fail` 스켈레톤 (`tests/`만) |
| ③ | `/green-minimal` | Respond · GREEN | RED 1묶음 최소 `src/` + assert PASS |
| ④ | `/golden-master` | Respond+ | Approval Test·golden matched |
| ⑤ | `/refactor-smell` | Refine ⑦ | 스멜 탐지만 (수정 금지) |
| ⑥ | `/refactor-safe` | Refine ⑧ | RF 1건 Budget 내 리팩터 |

**기존 유지:** `/export`, `/tdd-red` (Boundary RED 실행 레거시)

### 3.2 Skill (`.cursor/skills/`)

| Skill | 역할 | `disable-model-invocation` |
|---|---|---|
| `magic-square-tdd` | Dual-Track TDD SSOT — Phase·C2C·금지·Track 표·pytest 패턴 | `true` |
| `magic-square-docs` | Report·Transcript Export — Step A~F, `/export-session` 연동 | `true` |

`magic-square-docs` 보조: `report-template.md`, `transcript-template.md`, `phase-checklist.md`

### 3.3 공통 규칙 (체인 전체)

| 항목 | 내용 |
|---|---|
| Phase 선언 | 응답 첫 줄 `Phase: red\|green\|refactor \| Layer \| Track` |
| Track B (Logic) | `entity` · `src/entity/` · Domain Mock 금지 |
| Track A (UI) | `boundary` · `validate_lines` 공개 API |
| 상수 SSOT | `constants.py` — `34`/`16`/`4` 리터럴 금지 |
| E001~E005 | RED 설계·GREEN·REFACTOR 품질 게이트 |
| git commit | 사용자 명시 요청 시만 |
| Golden | `int[6]` 1-index · `Exxx` · `UPDATE_GOLDEN` 통제 |

---

## 4. Command별 핵심 계약

### `/red-test-plan`

- 입력 없이 동작 — 채팅·PRD·`.cursorrules`에서 FR·Test ID 추출
- 출력 4블록: C2C · Track B · 테스트 플랜 · ECB·Mock 점검
- 완료: `/red-skeleton 으로 넘길 준비됐다`

### `/red-skeleton`

- Then = `pytest.fail("RED: {Test ID} — …")` 한 줄만
- `tests/conftest.py` — `grid_g1` (0 두 개, row-major)
- 완료: pytest FAILED 보고

### `/green-minimal`

- 1 RED 묶음 = 1 GREEN · 1커밋(요청 시)
- `pytest.fail` → assert 교체

### `/golden-master`

- `tests/_approval.py` · `tests/golden/{id}.approved.txt`
- `UPDATE_GOLDEN=1` 기준 생성 → 없이 matched

### `/refactor-smell` · `/refactor-safe`

- smell: 수정 금지 · RF 후보 1~3 · P0 → safe
- safe: RF 1건 · Budget(파일≤3·클래스≤1·메서드≤3) · golden 유지

---

## 5. ARRR ↔ TDD 전체 맵

```
Ask     RED ③  /red-test-plan     설계표
Ask     RED ④  /red-skeleton      pytest.fail
Respond GREEN  /green-minimal     src 최소·PASS
Respond+       /golden-master     golden
Refine  ⑦     /refactor-smell    스멜 표
Refine  ⑧     /refactor-safe     safe refactor
```

문서 Export (별도): `magic-square-docs` · `/export-session`(Command 미생성·Skill에 연동 문구만)

---

## 6. 미완·다음 세션

| 항목 | 상태 |
|---|---|
| `/export-session` Command | Skill에 연동 문구만 — **파일 미생성** |
| `docs/PRD.md` | 없음 — `.cursorrules`+Report 추론 |
| `Report/05.REPORT.md` · `Prompting/05.Export-Transcript.md` | SSOT 참조 경로 — **미생성** (Skill 템플릿 폴백) |
| TDD 체인 실제 코드 실행 | Command·Skill 정의만 — RED/GREEN 구현은 후속 |

---

## 7. 8계층 정합 (Report/02)

| 계층 | 본 세션 반영 |
|---|---|
| Rule | `.cursorrules` + Skill 금지 목록 |
| Command | 6종 신규 + export·tdd-red |
| Skill | magic-square-tdd · magic-square-docs |
| Test Loop | Command 체인으로 RED→GREEN→REFACTOR 단계 고정 |
| Contract | 다음 세션 (Report/03 권장 유지) |

---

*작성 기준: MagicSquare_xx 세션 4 · ARRR TDD Command·Skill 체인 · 2026-06-10*
