# MagicSquare_1004 — 세션 3 워크북 보고서

## 1. 문서 목적

- Mom Test 인터뷰 결과(`Report/06`)를 바탕으로 **세션 3 워크북**을 작성한다.
- 8계층 중 **Rule, Command, (Skill), Test Loop**만 정의하고, Contract·Component·구현은 다음 세션으로 미룬다.
- 미래 의향·솔루션 찬성이 아닌 **과거 사실·행동·손실**을 근거로 주제·성공 기준·범위를 고정한다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md` | Mom Test 인터뷰·진짜 문제·증거 |
| `Report/01` (문제 인식) | "거의 맞음" 착시, 판단 기준 재현성 |
| `Prompting/08_MagicSquare_1004-세션3-워크북-프롬프트.md` | 본 워크북 재생성용 프롬프트 |

---

## 3. Mom Test 결과 (입력)

### 페르소나

4×4 부분 마방진(빈칸 2개)을 손으로/코드로 다루는 **학습자**. ECB·설계 연습과 함께 빈칸 맞추기를 수행하며, **다중 제약 판단**에서 어려움을 겪는다.

### 진짜 문제 (한 문장)

**여러 제약(행·열·대각선)이 겹친 상태에서, 중간에 어디가 틀렸는지·다음에 무엇을 확인할지 판단할 수 없어 20분을 쓰고도 진행을 이어가지 못하고, 같은 유형의 과제를 다시 열지 않게 된다.**

### Mom Test 증거 3줄

1. 대각선 합을 34로 맞추려다 **합 불일치** → 그 순간 **실습 종료**
2. **20분** 투입 후에도 다음 확인 단계 없이 중단
3. 비슷한 과제 **재시도·재개 없음** ("이 문제는 나랑 안 맞다")

---

## 4. 세션 3 워크북

### 4.1 주제 한 문장 (Mom Test 기반, 솔루션 최소화)

> **4×4 부분 마방진에서 막혔을 때, 어느 제약이 깨졌는지와 다음에 확인할 순서를 구조적으로 드러내는 판단 기준을 고정한다.**

| 포함 | 제외 |
|---|---|
| 판단 체계, 위반 드러내기, 다음 확인 순서 | 솔버, 대각선 "기능" 추가, TDD 도구 도입 자체 |

### 4.2 R-G-I-O

| | 내용 |
|---|---|
| **Role** | 4×4 부분 마방진(빈칸 2개, 합 34) 실습 **학습자** — ECB·설계 연습 중, 빈칸 맞추기 단계에서 막힘을 경험한 사람 |
| **Goal** | "거의 맞음"과 "틀림"을 **중간에 구분**하고, 막혔을 때 **다음 확인 한 걸음**을 재현 가능하게 만든다 (20분 후 포기·재개 없음 패턴 차단) |
| **Input** | 4×4 `int[][]` (0=빈칸 정확히 2개, 값 0 또는 1~16, 0 제외 중복 금지) + Mom Test 증거 3줄 + 제약 정의(행·열·대각선 합=34) |
| **Output** | 제약별 **통과/실패** + **위반 유형·위치·값** + **다음 확인 순서** 1건 — "틀렸다"만이 아닌 구조적 피드백 |

### 4.3 성공 기준 3개 (Mom Test 증거와 연결)

| # | 성공 기준 | 연결 Mom Test 증거 |
|---|---|---|
| **SC-1** | 합 불일치 시 **어느 줄(행/열/대각선)·현재 합·목표(34) 차이**를 출력한다 | ① "합이 안 맞아 막혔지만 **어디가 틀렸는지 특정 못 함**" |
| **SC-2** | 검증 **순서·우선순위**가 문서·Rule에 고정되어 있다 (예: 행 → 열 → 대각선) | ① "대각선부터 막혀 **다음 확인 단계를 모름**" |
| **SC-3** | 막힘 상태에서도 **종료 대신** "위반 목록 + 다음 한 걸음"을 반환한다 | ② 20분 후 중단 ③ **재시도·재개 없음** |

### 4.4 표면 문제 — 이번 프로젝트에서 하지 않을 것

| 표면 문제 (금지) | 왜 하지 않는가 |
|---|---|
| 4×4 마방진 **정답 두 칸을 자동으로 채워주는 솔버** | 진짜 문제는 "정답 못 찾음"이 아니라 **판단 체계 부재** |
| **대각선 검증 함수**만 추가 | 기능 1개 ≠ 막혔을 때 **다음 행동·순서** 고정 |
| **TDD/pytest 도입**을 목표로 삼기 | 증거는 **20분 손실·포기**이지 "TDD 하면 좋겠다"가 아님 |
| 알고리즘 난이도·풀이 속도 개선 | Pain은 난이도가 아니라 **중간 판별 불가** |
| UI / DB / Web 레이어 | 세션 3 범위 밖; 순수 **판단·검증 계약**에 집중 |

---

## 5. 8계층 — 세션 3 산출물

> **전체 8계층:** Concept → Mom Test → Rule → Command → Skill → Contract → Test Loop → Component  
> **이번 세션:** Rule, Command, (Skill), Test Loop만 작성

### 5.1 Rule

```yaml
# magic-square-constraint-rules
rules:
  - id: FAIL_WITH_VIOLATION_TYPE
    # 실패 응답은 "틀렸다"만 금지 — 위반 제약 유형(행/열/대각선/중복/범위) 필수
    when: constraint_check_fails
    then: report { type, location, actual, expected }

  - id: NO_PARTIAL_SATISFACTION
    # 행·열만 맞아도 "거의 끝" 판단 금지 — 전체 제약 통과 전까지 미완료
    when: row_col_pass AND diagonal_fail
    then: status = INCOMPLETE

  - id: FIXED_VERIFICATION_ORDER
    # 구현·실습 시작 전 검증 순서 문서화 필수
    order: [row, col, main_diag, anti_diag, duplicate, range]

  - id: MOM_TEST_ALIGNMENT
    # 설계 변경 시 Mom Test 증거 3줄과 SC-1~3 정렬 점검
    evidence: [diagonal_stall, 20min_abort, no_retry]
```

### 5.2 Command

| Command | 목적 | Mom Test 연결 |
|---|---|---|
| `/diagnose-grid` | 현재 격자의 제약별 통과/실패 + 위반 상세 | SC-1 |
| `/next-check` | 막힘 시 **다음 확인할 제약 1개** 반환 | SC-2, SC-3 |
| `/verify-order` | 고정된 검증 순서 출력·준수 여부 점검 | SC-2 |
| `/mom-alignment` | Rule·Test가 Mom Test 증거·SC와 맞는지 리뷰 | 전체 정렬 |

### 5.3 Skill (선택)

```markdown
# constraint-diagnosis — 4×4 마방진 제약 진단

## When to use
- 학습자가 빈칸 맞추기에서 막혔을 때
- "합이 안 맞다"만 알고 어디가 틀렸는지 모를 때

## Steps
1. 고정 순서(행→열→대각선→중복→범위)로 검사
2. 첫 실패 지점에서 { type, location, actual, expected } 보고
3. `/next-check`로 다음 확인 제약 1건 제안
4. Mom Test SC-1~3 충족 여부 자체 점검

## Do NOT
- 정답 두 칸을 대신 채우지 않음 (솔버 금지)
- "거의 맞음" 표현 사용 금지
```

### 5.4 Test Loop

| 단계 | 내용 | Mom Test 매핑 |
|---|---|---|
| **RED** | 대각선 합≠34 → 출력에 `type=diagonal`, `actual`, `expected=34` 포함 테스트 실패 | 증거 ① |
| **RED** | 행·열 OK·대각선 FAIL → `status=INCOMPLETE`, `next=diagonal` 테스트 실패 | 증거 ① + SC-2 |
| **RED** | 막힘 격자 → `violations[]` + `next_check` 비어 있지 않음 테스트 실패 | 증거 ②③ |
| **GREEN** | 최소 `diagnose(grid)` — 위 RED 중 1개 통과 | — |
| **REFACTOR** | 행/열/대각선 검증 중복 제거, 순서 단일 모듈화 | Report/01 "검증 복붙 버그" 예방 |
| **Loop 종료** | SC-1~3 각각 대응 테스트 ≥1 통과 + Mom Test 증거 traceability 표 | — |

---

## 6. 세션 3 산출물 체크리스트

- [ ] Rule YAML/MD 초안 (4개 규칙)
- [ ] Command 4개 정의
- [ ] (선택) Skill `constraint-diagnosis` 초안
- [ ] Test Loop RED 3개 + SC↔증거 매핑표
- [ ] 표면 문제 5개 "하지 않음" 명시

---

## 7. Report/06과의 정합성

| Report/06 개념 | 세션 3 반영 |
|---|---|
| 대각선 합 불일치 → 즉시 종료 | SC-1, Rule `FAIL_WITH_VIOLATION_TYPE` |
| 다음 확인 단계 모름 | SC-2, Command `/next-check`, Rule `FIXED_VERIFICATION_ORDER` |
| 20분 + 재개 없음 | SC-3, Test Loop RED (종료 대신 `next_check`) |
| "정답 찾기" ≠ 핵심 | 표면 문제 — 솔버 금지 |

---

*작성 기준: MagicSquare_1004 세션 3 · Mom Test Report/06 (2026)*
