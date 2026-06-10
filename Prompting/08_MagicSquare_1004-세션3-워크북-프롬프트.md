# MagicSquare_1004 — 세션 3 워크북 프롬프트

> Mom Test 결과를 바탕으로 세션 3 워크북(Rule/Command/Skill/Test Loop)을 생성·갱신할 때 사용한다.

---

## 프롬프트 (복사용)

```
Mom Test 결과:
- 페르소나: 4×4 부분 마방진(빈칸 2개)을 손으로/코드로 다루는 학습자. ECB·설계 연습과 함께 빈칸 맞추기를 수행하며, 다중 제약 판단에서 어려움을 겪는다.
- 진짜 문제 (한 문장): 여러 제약(행·열·대각선)이 겹친 상태에서, 중간에 어디가 틀렸는지·다음에 무엇을 확인할지 판단할 수 없어 20분을 쓰고도 진행을 이어가지 못하고, 같은 유형의 과제를 다시 열지 않게 된다.
- Mom Test 증거 3줄:
  1) 대각선 합을 34로 맞추려다 합 불일치 → 그 순간 실습 종료
  2) 20분 투입 후에도 다음 확인 단계 없이 중단
  3) 비슷한 과제 재시도·재개 없음 ("이 문제는 나랑 안 맞다")

MagicSquare_1004 세션 3 워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop

⚠️ 규칙:
- 솔루션(솔버, TDD 도구, UI)을 주제·목표에 넣지 말 것
- 성공 기준은 Mom Test 증거 3줄과 1:1 traceability
- Contract·Component·구현 코드는 다음 세션으로 미룸
- Report/06 Mom Test 인터뷰 보고서와 정합성 유지
```

---

## 세션 3 워크북 템플릿 (빈 양식)

### Mom Test 결과

| 항목 | 내용 |
|---|---|
| 페르소나 | |
| 진짜 문제 (한 문장) | |
| Mom Test 증거 3줄 | 1) 2) 3) |

### 1) 주제 한 문장

> (솔루션 최소화 — "판단 기준 고정" 중심)

### 2) R-G-I-O

| Role | |
| Goal | |
| Input | |
| Output | |

### 3) 성공 기준 3개

| # | 성공 기준 | Mom Test 증거 |
|---|---|---|
| SC-1 | | |
| SC-2 | | |
| SC-3 | | |

### 4) 표면 문제 — 하지 않을 것

| 표면 문제 | 왜 하지 않는가 |
|---|---|
| | |

### 8계층 — 세션 3

#### Rule

```yaml
# (4개 규칙: 위반 유형 필수, 부분 만족 금지, 검증 순서 고정, Mom Test 정렬)
```

#### Command

| Command | 목적 | Mom Test 연결 |
|---|---|---|
| | | |

#### Skill (선택)

```markdown
# (constraint-diagnosis 등)
```

#### Test Loop

| 단계 | 내용 | Mom Test 매핑 |
|---|---|---|
| RED | | |
| GREEN | | |
| REFACTOR | | |

---

## 저장 지시

워크북 완료 후 아래에 저장:

- **보고서:** `Report/08_MagicSquare_1004-세션3-워크북-보고서.md`
- **프롬프트:** `Prompting/08_MagicSquare_1004-세션3-워크북-프롬프트.md` (본 파일)

---

## 관련 문서

| 파일 | 설명 |
|---|---|
| `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md` | Mom Test 인터뷰 원본·증거 |
| `Report/08_MagicSquare_1004-세션3-워크북-보고서.md` | 본 프롬프트로 생성한 세션 3 워크북 |
| `Prompting/cursor_mom_test_workbook_discussion.md` | Mom Test 워크북·인터뷰 대화 기록 |
| `Prompting/07_역할분리-MomTest-시뮬레이션-프롬프트.md` | 역할 분리 3턴 시뮬레이션 |

---

*MagicSquare_1004 · 세션 3 워크북 프롬프트 · 2026*
