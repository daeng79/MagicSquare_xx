# Phase Checklist — export-session

> `/export-session` 또는 Report Export 요청 시 **magic-square-docs** Step A~F 순서 점검.

---

## Step A — 입력 수집

| # | 항목 | 수집 방법 | 필수 |
|---|---|---|---|
| A1 | `git status` | Shell `git status -sb` | ✓ |
| A2 | pytest | Shell `python -m pytest tests/ -v` (실패해도 실측 기록) | ✓ |
| A3 | Phase | 채팅 첫 줄·Command 맥락 (`red`/`green`/`refactor`/`repeat`) | ✓ |
| A4 | Test ID | 설계표·보고 (`T-LOG-*`, `T-BND-*`) | ✓ |
| A5 | Command | 이번 세션 Command 목록 | ✓ |
| A6 | 세션 주제·slug | 채팅·PRD·Report 맥락 | ✓ |
| A7 | transcript uuid | `agent-transcripts/{uuid}.jsonl` (있으면) | 선택 |

**금지:** A2 미실행 상태로 passed/failed **기재**.

---

## Step B — 번호 (NN)

```
NN = max(Report/{n}_, Prompting/{n}_) + 1  → 2자리 zero-pad
```

| 절차 | 내용 |
|---|---|
| B1 | Glob `Report/*.md`, `Prompting/*.md` |
| B2 | 파일명 선두 `\d{2}_` 추출, 최대값 |
| B3 | `05.REPORT.md` 등 메타 파일은 **번호에서 제외** |
| B4 | Report·Transcript **동일 NN·slug** |

갱신 vs 신규: 동일 세션·주제 파일 있으면 **갱신** (사용자 "새 번호" 시 예외).

---

## Step C — Report

- [ ] [report-template.md](report-template.md) 공통 골격
- [ ] Phase 해당 STEP만 작성 (RED / GREEN / REFACTOR / repeat)
- [ ] pytest·git status **Step A 실측** 반영
- [ ] `Prompting/{NN}_…-transcript.md` 상호 참조
- [ ] Write `Report/{NN}_{slug}-세션보고서.md`

---

## Step D — Transcript

- [ ] [transcript-template.md](transcript-template.md) 헤더 (`_Exported on`, `_Source uuid`)
- [ ] User/Cursor 교차, `---` 구분
- [ ] Phase·Command·실측 pytest 보존
- [ ] Write `Prompting/{NN}_{slug}-transcript.md`

---

## Step E — README 문서 표 갱신

`README.md` 없으면 프로젝트 루트에 **문서 인덱스 섹션** 생성.

```markdown
## 문서 인덱스

| NN | Report | Transcript / Prompting | Phase | 날짜 |
|---|---|---|---|---|
| {NN} | [세션보고서](Report/{NN}_{slug}-세션보고서.md) | [transcript](Prompting/{NN}_{slug}-transcript.md) | {phase} | {YYYY-MM-DD} |
```

- [ ] 기존 행 유지, 신규 행 **추가** (덮어쓰기 아님)
- [ ] NN 내림차순 또는 오름차순 **일관** 유지

---

## Step F — 완료 보고

```markdown
## Export-session 완료

| 항목 | 경로 |
|---|---|
| Report | `Report/{NN}_{slug}-세션보고서.md` |
| Transcript | `Prompting/{NN}_{slug}-transcript.md` |

### 요약
- Phase: {phase} · Test ID: {…} · pytest: {실측 한 줄}

### README
- 문서 표 갱신: yes
```

---

## 금지 (전 Step)

| 금지 | |
|---|---|
| `git commit` 임의 | 사용자 요청 시만 |
| `UPDATE_GOLDEN=1` 임의 | ISS·golden-master 절차 없이 |
| 채팅·터미널 없는 pytest 결과 | Step A2 필수 |
| `src/`/`tests/` export 본문 | git·TDD 흐름 |
| Report 전문을 Transcript에 중복 | 역할 분리 |

---

## Phase 빠른 매핑

| Phase | Report STEP | 필수 Command 예 |
|---|---|---|
| `red` | RED | `/red-test-plan`, `/red-skeleton` |
| `green` | GREEN | `/green-minimal`, `/golden-master` |
| `refactor` | REFACTOR | `/refactor-smell`, `/refactor-safe` |
| `repeat` | repeat | 위 전체 1사이클 요약 |
