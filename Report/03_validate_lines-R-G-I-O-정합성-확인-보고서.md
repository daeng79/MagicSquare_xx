# validate_lines · Report/08 R-G-I-O 정합성 확인 — MagicSquare_xx

## 1. 문서 목적

- `Report/08_MagicSquare_1004-세션3-워크북-보고서.md`의 **R-G-I-O·성공 기준(SC-1~3)** 이 `validate_lines` 계약과 맞는지 **확인만** 수행한 결과를 기록한다.
- 구현·Contract 문서 신규 작성은 범위 밖이며, 다음 세션(Contract 계층) 설계 시 참조용이다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `Report/08_MagicSquare_1004-세션3-워크북-보고서.md` | 대조 대상 — R-G-I-O, SC-1~3, Rule, Test Loop |
| `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md` | Mom Test 증거 원본 |
| `Prompting/09_validate_lines-R-G-I-O-정합성-확인-프롬프트.md` | 본 보고서 재생성·재확인용 프롬프트 |
| Dual-Track 설계 캔버스 (`MagicSquareJudge` / `isMagic`) | 기존 line 검증 API( boolean ) 참고 |

---

## 3. 조사 범위

| 항목 | 결과 |
|---|---|
| 워크스페이스 `validate_lines` | **없음** (코드·Contract 문서·테스트) |
| GitHub `daeng79/MagicSquare_xx` | **없음** |
| Report/08 | Contract 계층은 **다음 세션**으로 미룸 (§1, §5) |

→ 공식 `validate_lines` Contract가 없으므로, Report/08 Rule·Test Loop·기존 `MagicSquareJudge` 맥락에서 **추론한 계약**과 대조했다.

---

## 4. 추론한 `validate_lines` 계약 (대조 기준)

| 항목 | 내용 |
|---|---|
| **역할** | 행·열·주대각선·부대각선 **합=34** 검증 (line 단위) |
| **입력** | `4×4 int[][]` (0=빈칸 2개, 0 또는 1~16, 0 제외 중복 금지) |
| **출력** | 줄별 통과/실패 + `{ type, location, actual, expected=34 }` |
| **범위 밖** | 중복·범위 검증, `next_check`, `status=INCOMPLETE` (상위 `diagnose` 책임) |

Report/08 Rule `FIXED_VERIFICATION_ORDER`의 `row, col, main_diag, anti_diag` 4종과 Test Loop RED의 `type=diagonal, actual, expected=34`에 맞춘 정의이다.

---

## 5. R-G-I-O 대조

| R-G-I-O | Report/08 | `validate_lines`와의 관계 | 판정 |
|---|---|---|---|
| **Role** | 학습자 맥락 | API 계약 범위 밖 | ✅ 충돌 없음 |
| **Goal** | "거의 맞음" 구분 + **다음 한 걸음** | line 검증만으로 Goal 전체 충족 불가 | ⚠️ 부분 |
| **Input** | 격자 스펙 + Mom Test + 제약 정의 | 격자 스펙만 일치; Mom Test는 워크북 입력 | ✅ |
| **Output** | 제약별 통과/실패 + 위반 상세 + **다음 확인 1건** | line 위반만; `next_check` 없음 | ⚠️ 부분 |

**Input**은 격자 조건 기준 **일치**. **Output·Goal**은 `validate_lines` 단독으로는 **부족**하며, Report/08의 `diagnose(grid)` / `/next-check` 조합이 필요하다.

---

## 6. 성공 기준(SC) 대조

| SC | Report/08 | `validate_lines`만으로 충족? | 판정 |
|---|---|---|---|
| **SC-1** | 줄(행/열/대각선)·현재 합·34와의 차이 | 핵심 책임과 **직접 일치** | ✅ |
| **SC-2** | 검증 순서·우선순위 문서·Rule 고정 | line 결과 순서 ≠ 프로세스 순서; `duplicate`·`range`는 범위 밖 | ⚠️ |
| **SC-3** | 종료 대신 `violations[]` + `next_check` | line 위반 목록은 가능, **`next_check` 없음** | ❌ |

---

## 7. 추가 불일치·공백

| # | 항목 | 내용 |
|---|---|---|
| 1 | **이름 불일치** | Test Loop GREEN은 `diagnose(grid)`; `validate_lines`는 Report/08에 미언급 → **2계층 분리**(`validate_lines` 하위 + `diagnose` 상위)가 자연스럽다 |
| 2 | **제약 범위** | R-G-I-O Output·Rule은 `duplicate`, `range` 포함; `validate_lines`는 **line 합만** |
| 3 | **부분 격자** | Mom Test 시나리오(빈칸 2개)인데, 빈칸 포함 줄의 합 판정 규칙 **미명시** → SC-1 구현 시 해석 갈림 가능 |
| 4 | **기존 API** | `isMagic(matrix) → boolean`은 SC-1(위치·actual·expected)과 **불일치**; `validate_lines`는 Report/08 방향과 더 잘 맞으나 아직 Contract 미고정 |
| 5 | **세션 범위** | Report/08은 Contract를 다음 세션으로 미룸 → R-G-I-O Output이 **아직 Contract에 매핑되지 않은 상태** |

---

## 8. 종합 판정

| 구분 | 판정 |
|---|---|
| R-G-I-O **Input**(격자) | ✅ **맞음** |
| R-G-I-O **Output** 전체 | ⚠️ **`validate_lines`만으로는 부분 일치** |
| **SC-1** | ✅ **맞음** |
| **SC-2** | ⚠️ **부분** (순서·duplicate/range는 상위/별도 계약 필요) |
| **SC-3** | ❌ **불일치** (`next_check`는 `validate_lines` 밖) |

### 한 줄 결론

Report/08의 R-G-I-O·성공 기준은 **`validate_lines`와 SC-1·Input 수준에서 정렬**되어 있으나, **Output 전체와 SC-2·SC-3까지 `validate_lines` 하나로는 맞지 않는다.** Report/08이 기대하는 것은 `validate_lines` + (중복/범위 검증) + `next_check`를 묶는 **`diagnose` 계약**에 가깝다.

---

## 9. 다음 세션(Contract) 시 권장

| 권장 | 이유 |
|---|---|
| `validate_lines(grid)` — line 합 전용 Contract 명시 | SC-1 직접 충족, `MagicSquareJudge`/`isMagic` 대체 |
| `diagnose(grid)` — 상위 Contract | SC-2·SC-3, Rule `NO_PARTIAL_SATISFACTION`, Test Loop GREEN |
| 빈칸 포함 줄의 합 판정 규칙 Contract에 고정 | Mom Test 부분 격자 시나리오 모호성 제거 |
| Report/08 Test Loop RED ↔ Contract 시그니처 traceability 표 | 8계층 Contract 계층 완성 시 |

---

*작성 기준: MagicSquare_1004 · Report/08 R-G-I-O vs validate_lines 정합성 확인 · 2026-06-10*
