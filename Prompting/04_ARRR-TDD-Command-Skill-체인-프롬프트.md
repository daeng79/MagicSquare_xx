# ARRR TDD Command·Skill 체인 — MagicSquare_xx

> MagicSquare_xx Dual-Track TDD용 **Command 6종 + Skill 2종**을 생성·갱신할 때 사용한다.

---

## 프롬프트 (복사용)

```
MagicSquare_xx ARRR Dual-Track TDD Command·Skill 체인을 구축·갱신해줘.

SSOT:
- @.cursorrules
- @docs/PRD.md (없으면 Report/02 워크북·Report/03 정합성 보고)
- @Report/02_MagicSquare_1004-세션3-워크북-보고서.md

⚠️ 규칙:
- TDD 한 번에 한 Phase만 (RED 중 src/ 금지, GREEN 중 REFACTOR 금지)
- git commit은 내가 요청할 때만
- 솔버·UI·DB·범위 밖 기능 금지
- Command 본문은 기존 .cursor/commands/export.md·tdd-red.md 형식 따름
- Skill은 create-skill 가이드, 500줄 이하, disable-model-invocation: true

생성·갱신 대상:

【Command 6종】
1) .cursor/commands/red-test-plan.md — ARRR Ask RED③, C2C 4블록, 파일 Write 금지
2) .cursor/commands/red-skeleton.md — RED④, pytest.fail 스켈레톤, grid_g1 conftest
3) .cursor/commands/green-minimal.md — GREEN, 1묶음=1커밋, constants SSOT
4) .cursor/commands/golden-master.md — golden, UPDATE_GOLDEN, int[6] 1-index
5) .cursor/commands/refactor-smell.md — Refine⑦, 스멜만, RF 후보
6) .cursor/commands/refactor-safe.md — Refine⑧, RF 1건, Change Budget

【Skill 2종】
A) .cursor/skills/magic-square-tdd/SKILL.md — TDD SSOT, Command 체인, Track A/B
B) .cursor/skills/magic-square-docs/ — SKILL.md + report-template + transcript-template + phase-checklist
   (/export-session 연동, Step A~F)

Command 체인 순서:
red-test-plan → red-skeleton → green-minimal → golden-master → refactor-smell → refactor-safe

각 Command에 "magic-square-tdd Skill이 있으면 자동 따름" 문구 포함.

완료 후 /export 로 Report+Prompting 쌍 저장해줘.
```

---

## Command 체크리스트 (에이전트 자체 점검)

| # | Command | 필수 포함 |
|---|---|---|
| 1 | red-test-plan | Phase 선언, C2C Rule1~3, 4블록, E001~E005, /red-skeleton 완료 한 줄 |
| 2 | red-skeleton | pytest.fail only, AAA, grid_g1, Skill 참조 |
| 3 | green-minimal | 1묶음, constants, assert 교체, pytest 2종 |
| 4 | golden-master | assert_matches_golden, I:/E: 포맷 |
| 5 | refactor-smell | pytest 전제, P0/P1/P2, Budget, 수정 금지 |
| 6 | refactor-safe | RF 1건, golden diff 정책, 롤백 |

| # | Skill | 필수 포함 |
|---|---|---|
| 1 | magic-square-tdd | ARRR 매핑, Track 표, 금지, pytest 패턴 |
| 2 | magic-square-docs | Step A~F, NN 규칙, transcript uuid, 금지 |

---

## 저장 지시

```
/export
```

- Report: `Report/{NN}_ARRR-TDD-Command-Skill-체인-보고서.md`
- Prompting: `Report/{NN}_ARRR-TDD-Command-Skill-체인-프롬프트.md` (본 파일 갱신)
- NN = max(Report, Prompting) + 1

---

## 선택 후속

| 요청 | 프롬프트 한 줄 |
|---|---|
| export-session Command | `.cursor/commands/export-session.md` — magic-square-docs Skill checklist 연동 |
| SSOT 05 파일 | `Report/05.REPORT.md`, `Prompting/05.Export-Transcript.md` 형식 원본 |
| 첫 RED 실행 | `/red-test-plan` → `/red-skeleton` (Track B Logic) |
