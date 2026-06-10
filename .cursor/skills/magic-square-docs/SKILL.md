---
name: magic-square-docs
description: >-
  MagicSquare_xx 세션 Report·Transcript Export(ARRR 1사이클 보고, 세션 N 보고서).
  Use when user requests Report Export, Transcript, /export-session,
  Phase repeat, ARRR cycle completion report, or session report documentation.
disable-model-invocation: true
---

# magic-square-docs

MagicSquare_xx **세션 문서화** Skill — Report + Transcript 쌍 Export, README 인덱스 갱신.  
`/export-session` 및 Report Export 요청 시 **본 Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행**.

## SSOT 형식

| 문서 | 역할 |
|---|---|
| `Report/05.REPORT.md` | Report 형식 원본 (없으면 [report-template.md](report-template.md)) |
| `Prompting/05.Export-Transcript.md` | Transcript 형식 원본 (없으면 [transcript-template.md](transcript-template.md)) |
| `.cursor/commands/export.md` | 레거시 `/export` (report+prompt 쌍) |
| `magic-square-tdd` Skill | Phase·Test ID·Command·pytest 맥락 |

**소통:** 사용자와 **한국어**.

---

## 트리거

- Report Export · Transcript · `/export-session`
- `Phase: repeat` · ARRR 1사이클 완료 보고 · 세션 N 보고서
- 명시적 `magic-square-docs` Skill 호출

---

## 워크플로 (Step A → F)

Export 요청 시 **magic-square-docs Skill 로드 후 checklist 수행** — [phase-checklist.md](phase-checklist.md) 체크박스 순서대로.

### Step A — 입력 수집

| 입력 | 수집 |
|---|---|
| **git status** | `git status -sb` 실행 |
| **pytest** | `python -m pytest tests/ -v` **실행** (결과 실측만 기록) |
| **Phase** | `red` / `green` / `refactor` / `repeat` |
| **Test ID** | `T-LOG-*`, `T-BND-*` (채팅·설계표) |
| **Command** | `/red-test-plan`, `/green-minimal`, … |
| **주제·slug** | 세션 맥락 |
| **uuid** | agent-transcripts `{uuid}.jsonl` (있으면) |

### Step B — NN 결정

```
NN = max(Report/, Prompting/ 파일명 선두 2자리 번호) + 1
```

- `05.REPORT.md`, `05.Export-Transcript.md` 등 **메타 SSOT는 번호 제외**
- Report·Transcript **동일 NN·slug**

### Step C — Report

1. Read SSOT → [report-template.md](report-template.md)
2. Phase 해당 **STEP**만 본문 작성:
   - `red` → STEP RED
   - `green` → STEP GREEN
   - `refactor` → STEP REFACTOR
   - `repeat` → STEP repeat (ARRR 1사이클 표)
3. Step A 실측(pytest·git) 반영
4. Write `Report/{NN}_{slug}-세션보고서.md`

### Step D — Transcript

1. Read SSOT → [transcript-template.md](transcript-template.md)
2. 헤더: `_Exported on … from Cursor …` · `_Source uuid: …`
3. 본문: `**User**` / `**Cursor**` 교차, `---` 구분
4. Write `Prompting/{NN}_{slug}-transcript.md`

### Step E — README 문서 표 갱신

- `README.md`에 `## 문서 인덱스` 표 유지·**행 추가**
- 없으면 루트 `README.md` 생성 후 표 삽입
- 형식: [phase-checklist.md](phase-checklist.md) Step E

### Step F — 완료 보고

**경로 2개** 반드시 표기:

```markdown
## Export-session 완료

| 항목 | 경로 |
|---|---|
| Report | `Report/{NN}_{slug}-세션보고서.md` |
| Transcript | `Prompting/{NN}_{slug}-transcript.md` |

### 요약
- Phase: … · Test ID: … · pytest: (실측 한 줄) · git: (한 줄)
```

---

## `/export-session` 연동

```
/export-session
```

| 항목 | 내용 |
|---|---|
| 동작 | magic-square-docs Skill 로드 → Step A~F |
| 산출 | Report + Transcript (경로 2개) |
| checklist | [phase-checklist.md](phase-checklist.md) |
| NN | Step B 규칙 |

`/export`(export.md)와 차이:

| | `/export-session` | `/export` |
|---|---|---|
| Skill | magic-square-docs | export.md |
| 산출 | 세션보고서 + transcript | 보고서 + 프롬프트 |
| Phase STEP | RED/GREEN/REFACTOR/repeat | 주제 자유 |
| pytest·git | Step A 필수 실측 | 선택 |

---

## Phase ↔ Report STEP

| Phase | Report 섹션 | 전형 Command |
|---|---|---|
| `red` | STEP RED | `/red-test-plan`, `/red-skeleton` |
| `green` | STEP GREEN | `/green-minimal`, `/golden-master` |
| `refactor` | STEP REFACTOR | `/refactor-smell`, `/refactor-safe` |
| `repeat` | STEP repeat | 위 1사이클 요약표 |

`repeat` = Ask(RED) → Respond(GREEN) → Refine(REFACTOR) 완료 후 **세션 마감** Export.

---

## 파일 명명

```
Report/{NN}_{slug}-세션보고서.md
Prompting/{NN}_{slug}-transcript.md
```

예: `Report/04_T-LOG-001-green-세션보고서.md` · `Prompting/04_T-LOG-001-green-transcript.md`

---

## 금지

| 금지 | |
|---|---|
| **git commit** 임의 | 사용자 명시 요청 시만 |
| **UPDATE_GOLDEN=1** 임의 | ISS·`/golden-master` 없이 |
| **채팅·터미널 없는 pytest** 결과 기재 | Step A2 미실행 금지 |
| Report 본문을 Transcript에 복붙 | 역할 분리 |
| `src/`/`tests/` 코드 export | git·TDD |
| 번호·slug 무시 임의 파일명 | 추적 불가 |

---

## 보조 템플릿

| 파일 | 용도 |
|---|---|
| [report-template.md](report-template.md) | Report 골격·Phase STEP |
| [transcript-template.md](transcript-template.md) | Transcript 헤더·발화 형식 |
| [phase-checklist.md](phase-checklist.md) | export-session 체크리스트 |

---

## magic-square-tdd 연계

TDD 세션 Export 시 parallel Read:

- Phase 선언 형식 · Test ID · Command 체인 · pytest 패턴
- Report STEP에 RED/GREEN/REFACTOR 산출 **요약만** (코드 전문은 git)

---

## 완료 조건

- [ ] Step A: git·pytest **실행**·Phase·Test ID·Command 수집
- [ ] Step B: NN 확정
- [ ] Step C: Report Write (Phase STEP)
- [ ] Step D: Transcript Write (`_Exported on`, `_Source uuid`)
- [ ] Step E: README 문서 표 갱신
- [ ] Step F: 경로 2개 보고
- [ ] 금지 목록 미위반

---

*Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행.*
