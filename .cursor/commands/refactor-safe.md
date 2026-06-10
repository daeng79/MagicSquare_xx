# Refactor Safe — 스멜 1건 Safe Refactor (ARRR R단계)

> **ARRR R단계 (Refine = ⑧)** — `/refactor-smell` 표에서 **선택한 스멜 1개만** Budget 내에서 리팩터한다.  
> **동작 유지** — 기능 추가·버그 수정 금지 (별도 GREEN).

---

## Skill 참조

**`magic-square-tdd` Skill이 있으면 자동 따름.**  
(Budget·ECB·golden·E001~E005가 Skill과 충돌하면 Skill 우선)

---

## 사용법

```
/refactor-safe
/refactor-safe RF-001
```

| 인자 | 동작 |
|---|---|
| **(없음)** | 채팅 내 직전 `/refactor-smell` **P0 권장 후보 1개** 자동 선택 |
| `RF-{nnn}` | 해당 후보 ID 1건만 실행 |

**한 번에 스멜 1개만.** 여러 RF 동시 처리 금지.

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **`/refactor-smell` 보고** | RF ID, 스멜 유형, 위치, 제안 작업, Budget |
| **`.cursorrules`** | ECB, REFACTOR = 동작 유지 |
| **`magic-square-tdd` Skill** | Safe refactor 패턴·금지 목록 |

`/refactor-smell` 산출이 없으면 **중단** — smell 탐지 먼저 실행하라고 안내한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (후보 Track에 맞춤):

```
Phase: refactor | Layer: entity | Track: Logic
```

| Track | Layer | 선언 |
|---|---|---|
| Logic | `entity` | `Phase: refactor \| Layer: entity \| Track: Logic` |
| UI (boundary) | `boundary` | `Phase: refactor \| Layer: boundary \| Track: UI` |

---

## 전제 (필수)

```bash
python -m pytest tests/ -v
```

| 조건 | 미충족 시 |
|---|---|
| pytest **전부 PASS** | **중단** — GREEN 후 재실행 |
| `/refactor-smell` 후보·RF ID | 없으면 `/refactor-smell` 먼저 |
| Change Budget | 후보가 `OVER BUDGET`이면 **중단** |

---

## Safe Refactor 원칙

### 동작 불변 (하드 제약)

| 항목 | 규칙 |
|---|---|
| **입출력** | 공개 함수 시그니처·반환값·의미 **변경 금지** |
| **예외** | raise 타입·조건·메시지 의미 **변경 금지** |
| **`int[6]` 1-index** | golden·직렬화 6슬롯·1-based 규칙 **변경 금지** |
| **에러 코드** | `Exxx` 문자열 의미 **변경 금지** |
| **API 계약** | `validate_lines` status·`failed_lines` 의미 유지 |

리팩터는 **구조·이름·중복 제거·상수 추출**만. 관찰 가능한 동작이 달라지면 **롤백**.

### E001~E005 (emit·도입 금지)

| 코드 | REFACTOR에서 금지 |
|---|---|
| **E001** | Budget 초과·묶음 밖 파일 일괄 변경 |
| **E002** | Domain Mock / Entity `patch` |
| **E003** | `@pytest.mark.skip`, `xfail` |
| **E004** | assert 완화·테스트 삭제 |
| **E005** | 솔버·기능 추가·버그 수정·하드코딩 정답 |

**버그를 발견해도** 본 커맨드에서 고치지 않는다 → 별도 **GREEN** 이슈로 기록.

### Change Budget (1회 상한 — 반드시 준수)

| 항목 | 상한 |
|---|---|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

초과 시 작업 **분할** — 이번 실행은 Budget 내에서 **중단·보고**.

### ECB

| 계층 | REFACTOR 허용 | 금지 |
|---|---|---|
| Entity | 순수 함수 추출·rename·상수 import | Controller/Boundary import 추가 |
| Controller | Entity 호출 정리·순서 유지 | Boundary import |
| Boundary (`tests/`) | 이름·헬퍼 정리 (동작 동일) | Entity private 직접 검증 추가 |

---

## 실행 절차

1. **대상 확정** — RF ID 또는 P0 스멜 **1건** (위치·제안 작업 명시)
2. **pytest 전제** — `python -m pytest tests/ -v` PASS 확인
3. **Budget 확인** — 예상 변경이 파일≤3·클래스≤1·메서드≤3
4. **리팩터 실행** — `src/`·필요 시 `tests/` (동작 동일한 구조 변경만)
5. **pytest 회귀** — `pytest tests/ -v` → 전부 PASS
6. **golden matched** — `UPDATE_GOLDEN` **없이** golden 연결 테스트 PASS
7. **golden diff 처리** — [golden diff 정책](#golden-diff-정책)
8. **보고** — 변경 요약 · pytest · golden matched

---

## golden diff 정책

리팩터 후 golden assert가 실패할 수 있다. **의도 여부**로 분기:

| 경우 | 조건 | 조치 |
|---|---|---|
| **비의도** | 입출력·`int[6]`·`Exxx`가 리팩터 목표와 무관하게 변경 | **즉시 롤백** → pytest·golden 재확인 |
| **의도적** | 직렬화 경로만 바뀌었으나 **관찰 결과는 동일**해야 함 (실제로는 비의도면 롤백) | 관찰 결과 동일함을 증명 후 **ISS 문서화** + `UPDATE_GOLDEN=1` |

### ISS 문서화 (의도적 golden 갱신 시만)

`Report/` 또는 `docs/issues/`에 한 줄 이상:

```markdown
## ISS-{nnn}: golden 갱신 (RF-001)
- 리팩터: (한 줄)
- golden: `tests/golden/T-LOG-001.approved.txt`
- 사유: 직렬화 경로 변경, 관찰값 동일 확인 방법: (pytest 로그·수동 대조)
- 갱신: `UPDATE_GOLDEN=1 pytest tests/...::... -v`
```

**golden 수동 편집으로 통과 우회 금지** — `UPDATE_GOLDEN=1`은 ISS 기록 **후**에만.

### golden 검증 명령

```bash
# matched 확인 (UPDATE_GOLDEN 없음)
pytest tests/ -v

# 의도적 갱신 (ISS 후)
UPDATE_GOLDEN=1 pytest tests/<golden_연결_파일>::<함수> -v
pytest tests/ -v
```

golden 파일이 없으면 본 커맨드에서 **생략** 가능 — 있으면 **반드시** matched 확인.

---

## 스멜 유형별 허용 작업 (1건)

| 스멜 | Safe 작업 예 | 금지 |
|---|---|---|
| **Long Method** | private 헬퍼 추출 (동일 계층) | 새 공개 API·로직 추가 |
| **Duplicated Code** | 공통 함수 1개 추출 | 검증 순서 변경 |
| **Mysterious Name** | 도메인 rename | 공개 시그니처 breaking rename |
| **Magic Number** | `constants.py` import | 상수 **값** 변경 |
| **ECB 위반** | import 제거·계층 이동 | 역방향 의존 추가 |
| **Feature Envy** | 메서드 이동 (올바른 계층으로) | status 조립을 Entity로 이동 |

---

## 금지 (본 커맨드)

| 금지 | 이유 |
|---|---|
| 스멜 **2건 이상** 동시 처리 | 1 RF = 1 smell |
| 기능 추가·버그 수정 | GREEN 전용 |
| 입출력·예외·`int[6]`·`Exxx` 의미 변경 | Safe refactor 위반 |
| Budget 초과 | `/refactor-smell` 분할 후보 |
| E001~E005 패턴 | 품질 게이트 |
| golden 수동 편집 | Approval 우회 |
| 비의도 golden diff 방치 | 롤백 필수 |
| `git commit` (사용자 미요청) | `.cursorrules` |

---

## git commit

| 규칙 | 내용 |
|---|---|
| **시점** | 사용자 **명시 요청 시만** |
| **단위** | **1커밋 = 1 RF (스멜 1건)** |
| **메시지** | `refactor: RF-001 Magic Number — MAGIC_CONSTANT import` |

---

## 보고 형식

```markdown
Phase: refactor | Layer: entity | Track: Logic

## 대상
- RF-001 | P0 | Magic Number | `src/entity/line.py:line_sum_matches_magic`

## 변경 요약
- `src/entity/line.py` — 리터럴 34 → `MAGIC_CONSTANT` import
- (해당 시) `tests/…` — import 경로만

## Change Budget
- 파일 2 / 클래스 0 / 메서드 2 — ✓ 준수

## pytest
- `pytest tests/ -v` → N passed, 0 failed

## golden
- matched: yes / n/a (golden 미구축) / ISS-001 후 UPDATE_GOLDEN 갱신 완료
- (no 시) diff 한 줄 + 롤백 여부

## 다음 단계
- 추가 스멜: `/refactor-smell` 재실행 또는 RF-002 → `/refactor-safe RF-002`
- commit: 사용자 요청 시
```

---

## ARRR · TDD 위치

| 단계 | 커맨드 | 산출 |
|---|---|---|
| Refine ⑦ | `/refactor-smell` | 스멜 표 + RF 후보 |
| **Refine ⑧** | **`/refactor-safe`** | **Budget 내 리팩터 + pytest + golden** |
| 버그·기능 | `/green-minimal` | 별도 GREEN |

`.cursorrules`: REFACTOR = 동작 유지, 중복·순서 로직 정리.

---

## 참조

| 문서 | 역할 |
|---|---|
| `.cursor/commands/refactor-smell.md` | RF 후보·Budget·P0 선택 |
| `.cursor/commands/golden-master.md` | golden·UPDATE_GOLDEN·포맷 |
| `.cursor/commands/green-minimal.md` | 버그 수정은 여기 |
| `.cursorrules` | ECB·TDD·commit |

### 완료 조건

- [ ] 스멜 **1건**만 처리 (RF ID 명시)
- [ ] Change Budget 준수
- [ ] 입출력·예외·`int[6]` 1-index 불변
- [ ] E001~E005 없음, 기능 추가·버그 수정 없음
- [ ] `pytest tests/ -v` 전부 PASS
- [ ] golden 있으면 matched (`UPDATE_GOLDEN` 없음) 또는 ISS+갱신
- [ ] 비의도 golden diff 시 롤백 완료
- [ ] 보고: 변경 요약 · pytest · golden matched

---

*ARRR Refine ⑧: RF-xxx 1건, 동작 유지, golden으로 회귀 잠금.*
