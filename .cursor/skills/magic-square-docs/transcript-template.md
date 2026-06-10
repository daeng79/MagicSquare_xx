# Transcript 템플릿 — magic-square-docs SSOT

> 형식 원본: `Prompting/05.Export-Transcript.md` (없으면 본 파일).  
> [SKILL.md](SKILL.md) Step D에서 사용.

---

## 파일명

```
Prompting/{NN}_{주제-slug}-transcript.md
```

- Report와 **동일 `{NN}`·slug** (쌍 추적)
- discussion 아카이브: `Prompting/cursor_{slug}_discussion.md` (번호 없음, 별도 규칙)

---

## 헤더 (필수)

```markdown
# {주제} — 세션 {N} transcript
_Exported on {YYYY-MM-DD} at {HH:MM:SS} {TZ} from Cursor ({version})_
_Source uuid: {uuid}_

---
```

| 필드 | 규칙 |
|---|---|
| `_Exported on` | export 실행 시각 (로컬 TZ) |
| `_Source uuid` | agent-transcripts JSONL 파일명(uuid, `.jsonl` 제외) 또는 채팅 세션 ID; 없으면 `unknown` + 주석 |
| Cursor 버전 | 알 수 있으면 괄호에 기록 |

---

## 본문 형식

```markdown
**User**

{사용자 메시지 원문 — 요약 금지, export 구간 전체}

---

**Cursor**

{어시스턴트 응답 원문 — 도구 출력은 핵심만, Phase 선언·pytest 실측·파일 경로 유지}

---

**User**

…
```

### 규칙

| 항목 | 내용 |
|---|---|
| 발화자 | `**User**` / `**Cursor**` 만 (역할 분리 Mom Test 등 예외는 섹션 제목으로 명시) |
| 구분선 | 발화 블록 사이 `---` |
| 코드·명령 | fenced block 유지 |
| pytest | **채팅·터미널에 실제 있던** 결과만; 없으면 `(미실행)` |
| Phase 선언 | `Phase: red \| …` 줄 보존 |
| Command | `/red-test-plan` 등 호출 기록 보존 |

---

## 메타 푸터 (선택)

```markdown
---

## Export 메타
| 항목 | 값 |
|---|---|
| Command | /export-session |
| Phase | {phase} |
| Test ID | {목록} |
| Report 쌍 | `Report/{NN}_{slug}-세션보고서.md` |
| Skill | magic-square-docs |
```

---

## 금지

- 채팅에 없는 User/Cursor 대화 **창작**
- pytest 결과 **조작·추정**
- Report 본문 전체 **복붙** (transcript는 대화 원문, report는 구조화 요약)
