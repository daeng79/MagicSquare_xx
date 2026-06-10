# RED Test Plan — C2C 설계표·테스트 플랜 (ARRR A단계)

> **ARRR A단계 (Ask = RED ③)** — C2C 설계표와 테스트 플랜만 작성한다.  
> 실제 `tests/`·`src/` 파일은 **생성·수정하지 않는다**. 다음 단계 `/red-skeleton`으로 넘긴다.

---

## 사용법

```
/red-test-plan
```

**추가 입력 없이** 위 커맨드만으로 동작한다.

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **현재 채팅** | 세션 주제, 논의 중인 함수·API, Mom Test SC·증거, 이미 언급된 Test ID |
| **`docs/PRD.md`** | FR-* 기능 요구, Invariant, Dual-Track 범위, 금지 항목 |
| **`.cursorrules`** | API 계약, ECB 계층, 검증 순서, TDD 금지 규칙 |
| **`tests/`·`src/` Glob** | 기존 테스트·모듈 경로 (파일 **수정은 하지 않음**) |

`docs/PRD.md`가 없으면 `.cursorrules` + 채팅 맥락 + `Report/` 워크북(SC-1~3)으로 FR을 **추론**하고, 추론임을 표에 명시한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}
```

| Track | Layer | 대상 | 기본 테스트 위치 |
|---|---|---|---|
| **Logic** | `entity` | `src/entity/` 순수 함수 | `tests/test_entity_*.py` |
| **UI** (Boundary) | `boundary` | 공개 API (`validate_lines` 등) | `tests/test_validate_lines.py` |

> **Track A(boundary) 재사용:** Logic Track용 본문을 그대로 쓰되, 선언의 `Layer`만 `boundary`로, `Track`만 `UI`로 바꾸면 Track A에 재사용 가능하다. C2C·플랜 표의 대상 함수·파일 경로만 Boundary 기준으로 치환한다.

---

## 실행 절차

1. **SSOT Read** — `.cursorrules`, `docs/PRD.md`(있으면), 채팅·Report 맥락
2. **세션 주제·Track 결정** — Logic(entity) vs UI(boundary); 모호하면 채팅 최근 맥락 우선
3. **FR → To-Do → Test ID** — C2C Rule1~3에 따라 1 FR당 To-Do 1개, RED 1사이클 = Test ID 1개
4. **4블록 출력** — 아래 [출력 형식](#출력-형식) 표만 작성 (코드·파일 Write 금지)
5. **ECB·Mock 점검** — Logic Track 시 Domain Mock 금지, E001~E005 emit 금지 확인
6. **완료 한 줄** — `"/red-skeleton 으로 넘길 준비됐다"`

---

## C2C Rule1~3 (설계 규칙)

| Rule | 내용 |
|---|---|
| **Rule1** | PRD FR(또는 SC) **1개**를 인용하고, 구현 To-Do **1개**만 대응시킨다 |
| **Rule2** | To-Do 1개 = Test ID **1개** = RED 사이클 **1개** (한 테스트에 여러 FR 몰아넣기 금지) |
| **Rule3** | 각 Test ID에 **Given / When / Then**을 표로 고정한다 (Arrange·Act·Assert 대응) |

### Test ID 명명 (자동 부여)

| Track | 패턴 | 예 |
|---|---|---|
| Logic | `T-LOG-{nnn}` | `T-LOG-001` |
| UI (boundary) | `T-BND-{nnn}` | `T-BND-001` |

채팅·PRD에 이미 ID가 있으면 **그 ID를 우선** 사용한다.

---

## 출력 형식

응답 본문은 **아래 4블록 표**만 포함한다. (서론·코드 블록·파일 Write 없음)

### 블록 1 — C2C (Rule1~3)

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|---|---|---|---|---|---|---|
| Rule1 | `FR-…` 또는 `SC-…` 원문 인용 | (한 줄 actionable) | `T-…-001` | (전제 격자·입력) | (호출·행위) | (기대 결과·Invariant) |
| Rule2 | … | … | `T-…-002` | … | … | … |
| Rule3 | … | … | `T-…-003` | … | … | … |

- FR 인용은 `docs/PRD.md` 절·ID를 붙인다. 없으면 `.cursorrules` API 조항 + `(추론)` 표기.
- Logic Track 예: `sum_line`, `line_sum_matches_magic` 대상.
- UI Track 예: `validate_lines(grid)` → `status`, `failed_lines` 계약.

### 블록 2 — Track B 표 (RED 시나리오 명세)

> Logic Track = Entity RED 명세. UI Track = Boundary RED 명세 (동일 표 구조).

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---|---|---|---|---|
| `T-…-001` | `함수명` | Given: … → Then: … | (불변 조건 1줄) | `AssertionError` / `FAILED` — (stub·미구현으로 실패할 이유) |
| `T-…-002` | … | … | … | … |

**Invariant 예 (MagicSquare_xx):**

- 마법상수 = 34
- 검증 순서: `R1→R4→C1→C4→D1→D2`
- `incomplete`: 행·열 통과 + 대각선(D1/D2) 실패
- 빈칸(0) 있어도 합 계산 수행

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|---|---|
| **파일 경로** | (예) `tests/test_entity_line.py` 또는 `tests/test_validate_lines.py` |
| **함수명** | `test_<시나리오_한글_또는_영문>` — Test ID와 1:1 매핑 |
| **conftest 픽스처** | 필요 시 이름·역할 (예: `grid_r1_fail` — R1 합≠34 격자). 없으면 `없음` 또는 `신규: fixture명 (역할)` |
| **pytest 명령** | `pytest <파일경로> -v` 또는 `pytest <파일>::<함수> -v` |
| **RED 묶음 범위** | 이번 플랜에 포함된 Test ID 목록 (예: `T-LOG-001~003`) |

한 RED 묶음 = **동일 Track·동일 Layer** 내 연속 skeleton 작성 단위. `/red-skeleton`은 이 묶음을 한 번에 옮긴다.

### 블록 4 — ECB·Mock 점검

| 점검 항목 | Logic Track | UI (boundary) Track |
|---|---|---|
| **계층 준수** | Entity만 대상; Controller·Boundary 직접 테스트 금지 | 공개 API만; Entity 내부 직접 assert 금지 |
| **Domain Mock** | **금지** — 순수 함수에 Mock/patch 금지 | Boundary는 실제 Controller 경로 (Entity stub은 GREEN 이후) |
| **I/O·상태** | Entity에 파일·DB·UI 호출 없음 | 입력 `grid`·출력 `dict` 계약만 |
| **E001~E005 emit** | **금지** — 아래 코드를 플랜·산출에 넣지 않음 | 동일 |

**E001~E005 (emit 금지 — 플랜에 포함하지 말 것):**

| 코드 | 의미 |
|---|---|
| E001 | `src/` 수정·구현 제안 |
| E002 | Domain Mock / `unittest.mock.patch` on Entity |
| E003 | `@pytest.mark.skip` / `xfail` |
| E004 | assert 완화·테스트 삭제로 RED 회피 |
| E005 | 솔버·정답 채우기·범위 밖 기능 |

점검 결과 열: 각 Test ID 행마다 `PASS` 또는 위반 시 `FAIL (E00x)` — **전부 PASS일 때만** 완료 한 줄 출력.

---

## 금지 (본 커맨드)

| 금지 | 이유 |
|---|---|
| `src/` 수정 | GREEN 단계 전용 |
| GREEN / REFACTOR 진행 | RED ③ 설계만 |
| `tests/`·`src/` 파일 생성·Write | `/red-skeleton` 전용 |
| `@pytest.mark.skip`, `xfail` | RED 회피 (E003) |
| assert 완화·실패 테스트 삭제 | RED 회피 (E004) |
| 솔버·정답 채우기·UI·DB | `.cursorrules` 범위 밖 |
| 사용자에게 Track/Layer/FR 수동 입력 요구 | 자동 추출이 기본 |

---

## 완료 한 줄 (필수)

4블록 표와 ECB 점검 **전부 PASS** 후, 응답 **마지막 줄**:

```
/red-skeleton 으로 넘길 준비됐다
```

ECB 점검에 `FAIL`이 있으면 위 문장을 출력하지 않고, 위반 항목만 수정한 플랜을 다시 표기한다.

---

## 참조 (SSOT)

| 문서 | 역할 |
|---|---|
| `.cursorrules` | API `validate_lines`, status 3종, ECB, 검증 순서, TDD 사이클 |
| `docs/PRD.md` | FR-*, Invariant, Dual-Track, Mom Test SC traceability |
| `.cursor/commands/tdd-red.md` | Boundary RED 실행 형식 (AAA·pytest·보고) — **본 커맨드는 그 이전 설계 단계** |
| `.cursor/commands/red-skeleton.md` | (다음 단계) 플랜 → `tests/` skeleton 작성 |

### MagicSquare_xx 기본 맥락 (자동 추출 실패 시 폴백)

| 항목 | 값 |
|---|---|
| 공개 API | `validate_lines(grid) -> {status, failed_lines}` |
| Entity | `sum_line`, `line_sum_matches_magic` (`src/entity/line.py`) |
| Controller | `validate_lines` (`src/validate_lines.py`) |
| Boundary | `tests/test_validate_lines.py` |
| 검증 순서 | `R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2` |

---

## 출력 예시 (요약 — Logic Track)

```markdown
Phase: red | Layer: entity | Track: Logic

## 1. C2C (Rule1~3)
| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
| ... |

## 2. Track B 표
| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
| ... |

## 3. 테스트 플랜
| 항목 | 내용 |
| ... |

## 4. ECB·Mock 점검
| 점검 항목 | Logic Track | ... |
| ... |

/red-skeleton 으로 넘길 준비됐다
```

---

*ARRR: Ask(본 커맨드) → Review → Refine → Run — RED ③ = 설계표·플랜만, 구현·skeleton은 다음 커맨드.*
