# Export — Report / Prompting 저장

> 이번 대화(또는 지정 구간)의 산출물을 `Report/`·`Prompting/`에 저장한다.  
> `@Report/...` `@Prompting/...` 를 매번 붙이지 않아도 되도록 **한 번에 export** 한다.

---

## 사용법

```
/export                  ← report + prompt 둘 다 (기본)
/export report           ← report만
/export prompt           ← prompt만
/export discussion       ← 대화 아카이브만
```

| 인자 | 동작 | 저장 위치 |
|---|---|---|
| **(없음)** | **report + prompt 쌍 동시 export** | `Report/` + `Prompting/` |
| `report` | 보고서만 | `Report/` |
| `prompt` | 프롬프트만 | `Prompting/` |
| `discussion` | 대화 아카이브만 | `Prompting/` |

### `/export` 기본 동작 (필수)

인자 없이 `/export`만 입력하면 **반드시 아래 2개 파일을 모두** Write한다.

1. `Report/{NN}_{주제-slug}-보고서.md`
2. `Prompting/{NN}_{주제-slug}-프롬프트.md`

- **같은 `{NN}`·같은 slug** — Report↔Prompting 쌍으로 추적
- report만 만들고 prompt를 생략하지 **않음**
- prompt 본문은 report를 **복붙하지 않음** — [템플릿](#템플릿)대로 **재사용 프롬프트**(복사용 블록)만 작성
- report의 `## 2. 근거 문서` 표에 방금 저장한 Prompting 경로를 **상호 참조**로 넣음

---

## Export 절차

1. **유형 확인**
   - 인자 없음 → **`report` + `prompt` 둘 다** (기본)
   - `report` / `prompt` / `discussion` → 해당 유형만
2. **기존 파일 스캔** — `Report/`, `Prompting/` 목록을 Read·Glob으로 확인
3. **번호·파일명 결정** — [명명 규칙](#명명-규칙) 적용 (쌍 export 시 **동일 NN·slug**)
4. **근거 문서 Read**
   - Mom Test: `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md`
   - 직전 세션 Report·Prompting 쌍 (예: 08 워크북 ↔ Prompting/08)
   - `.cursorrules` (코드·TDD 작업과 연결 시)
5. **본문 작성** — [템플릿](#템플릿)에 맞춰 **완성본** (채팅 요약만 넣지 않음)
   - 쌍 export: report 먼저 작성 → prompt는 **복사용 프롬프트 블록** + (선택) 빈 양식
6. **파일 Write**
   - `/export` → Report **1개** + Prompting **1개** (총 2파일, 순서: report → prompt)
   - `/export report` 또는 `/export prompt` → 해당 1개만
7. **보고** — [보고 형식](#보고-형식)으로 경로·요약 전달 (쌍 export 시 **두 경로 모두** 표기)

### 갱신 vs 신규

| 상황 | 동작 |
|---|---|
| 같은 세션·주제 파일이 **이미 있음** | 기존 파일 **갱신** (사용자가 "새 번호"라고 하면 예외) |
| 새 세션·새 주제 | 다음 **2자리 번호** (`06`→`07`→`08`→`09`…) 로 **신규** |
| discussion | 번호 없이 `cursor_<주제>_discussion.md` 또는 타임스탬프 접미 |

---

## 명명 규칙

### Report

```
Report/{NN}_{주제-slug}-보고서.md
```

예:

- `Report/08_MagicSquare_1004-세션3-워크북-보고서.md`
- `Report/07_역할분리-MomTest-시뮬레이션-보고서.md`

### Prompting

```
Prompting/{NN}_{주제-slug}-프롬프트.md
```

예:

- `Prompting/08_MagicSquare_1004-세션3-워크북-프롬프트.md`

- `{NN}`: Report와 **같은 세션 번호**를 쓰면 쌍으로 추적하기 쉬움
- slug: 한글·영문·숫자·하이픈 (`MagicSquare_1004`, `4x4-마방진` 등 기존 파일과 통일)

### Discussion (대화 아카이브)

```
Prompting/cursor_{주제-slug}_discussion.md
```

- 파일 상단에 export 시각·Cursor 버전(알 수 있으면) 기록
- 기존 `cursor_mom_test_workbook_discussion.md` 형식 따름

---

## 템플릿

### Report (`-보고서.md`)

```markdown
# {제목} — MagicSquare_xx

## 1. 문서 목적
- (한두 문장)

## 2. 근거 문서
| 문서 | 역할 |
|---|---|
| `Report/06_...` | Mom Test |
| `Prompting/{NN}_...` | 재생성 프롬프트 |

## 3. (본문 섹션 — 주제에 맞게)
...

---
*작성 기준: MagicSquare_1004 세션 N · (날짜)*
```

### Prompt (`-프롬프트.md`)

```markdown
# {제목} — MagicSquare_xx

> (한 줄: 언제 쓰는 프롬프트인지)

---

## 프롬프트 (복사용)

\```
(에이전트·Cursor에 붙여 넣을 **완전한** 프롬프트 블록)
\```

---

## (선택) 템플릿 / 체크리스트
...
```

### Discussion

```markdown
# {주제} discussion
_Exported on {날짜} from Cursor_

---

**User**
...

**Cursor**
...
```

---

## 보고 형식

export 완료 시:

```markdown
## Export 완료

| 항목 | 내용 |
|---|---|
| 유형 | both (report+prompt) / report / prompt / discussion |
| Report | `Report/{NN}_...-보고서.md` — 신규 / 갱신 |
| Prompting | `Prompting/{NN}_...-프롬프트.md` — 신규 / 갱신 / (해당 없음) |
| 연결 | (Mom Test SC, Report↔Prompting 상호 참조) |

### 파일 요약
- Report: (한 줄)
- Prompting: (한 줄) — `/export` 기본 시 **반드시** 포함

### 다음에 쓸 때
- `/export` — report + prompt 쌍 동시 갱신
- `/export report` 또는 `/export prompt` — 한쪽만 갱신
- 채팅에서 `@` 없이 "Report/08 기준으로 RED" — 번호로 참조 가능
```

---

## 금지

| 금지 | 이유 |
|---|---|
| `src/`, `tests/` 를 export 대상으로 저장 | 코드는 git·TDD 흐름 |
| Report 본문 전체를 Prompting에 **복붙** | 역할 분리 (prompt는 복사용 블록만) |
| `/export` 시 **report만** 저장하고 prompt 생략 | 기본 동작 위반 |
| 번호·slug 무시한 임의 파일명 | 추적 불가 |
| 사용자 확인 없이 **기존 파일 덮어쓰기** (주제가 다를 때) | 데이터 손실 |
| git commit | 사용자 요청 시만 |

---

## 참조 (현재 프로젝트 인덱스)

| 번호 | Report | Prompting |
|---|---|---|
| 06 | `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md` | — |
| 07 | `Report/07_역할분리-MomTest-시뮬레이션-보고서.md` | `Prompting/07_역할분리-MomTest-시뮬레이션-프롬프트.md` |
| 08 | `Report/08_MagicSquare_1004-세션3-워크북-보고서.md` | `Prompting/08_MagicSquare_1004-세션3-워크북-프롬프트.md` |
| 09 | `Report/09_validate_lines-R-G-I-O-정합성-확인-보고서.md` | `Prompting/09_validate_lines-R-G-I-O-정합성-확인-프롬프트.md` |

**다음 신규 번호:** `10` (폴더 스캔 후 최대값+1로 재확인)

대화 아카이브: `Prompting/cursor_mom_test_workbook_discussion.md`
