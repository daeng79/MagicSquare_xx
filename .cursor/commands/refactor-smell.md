# Refactor Smell — 코드 스멜 탐지 (ARRR R단계)

> **ARRR R단계 (Refine = ⑦)** — `src/`·`tests/` 코드 스멜을 **탐지만** 한다.  
> **수정·commit 금지.** 후보는 `/refactor-safe`로 넘긴다.

---

## Skill 참조

**`magic-square-tdd` Skill이 있으면 자동 따름.**  
(스멜 분류·ECB 기준·Change Budget이 Skill과 충돌하면 Skill 우선)

---

## 사용법

```
/refactor-smell
```

**추가 입력 없이** 동작한다. `src/`·`tests/`를 Read·분석만 한다.

| 자동 추출 소스 | 추출 항목 |
|---|---|
| **`src/`·`tests/`** | 함수·클래스 길이, 중복, 명명, 매직넘버, ECB import |
| **`.cursorrules`** | ECB 계층, constants SSOT, 검증 순서 |
| **채팅·GREEN 보고** | 최근 변경 파일·Track |
| **`magic-square-tdd` Skill** | 스멜 우선순위·금지 패턴 |

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

Logic·Boundary(UI) **모두** 스캔 대상. 한 Track만 해당되면 표에 Track 열로 구분한다.

---

## 전제 (필수) — 실패 시 중단

```bash
python -m pytest tests/ -v
```

| 결과 | 동작 |
|---|---|
| **전부 PASSED** | 스멜 탐지 진행 |
| **1개라도 FAILED** | **즉시 중단** — GREEN·golden 수정 후 재실행 안내 |

본 커맨드는 pytest를 **실행해 전제만 확인**한다. 실패를 고치지 않는다.

---

## 실행 절차

1. **pytest 전제 확인** — `python -m pytest tests/ -v` → 전부 PASS 아니면 중단
2. **`src/`·`tests/` Read** — Entity·Controller·Boundary 전 범위
3. **스멜 분류** — 아래 7종 × P0/P1/P2
4. **Change Budget 검토** — 후보별 예상 변경량이 Budget 이내인지 표기
5. **출력** — [스멜 표](#스멜-표) + `/refactor-safe` 후보 **1~3개**
6. **다음 안내** — **P0 1개만** 골라 `/refactor-safe` 실행

**코드 수정·파일 Write·`git commit` 금지.**

---

## 스멜 유형 (7종)

| 스멜 | 탐지 기준 (MagicSquare_xx) |
|---|---|
| **Long Method** | 함수·메서드 **>25줄** 또는 단일 책임 초과 (검증+조립 혼재) |
| **Duplicated Code** | 동일·유사 로직 2곳 이상 (행/열/대각선 합 계산 반복, assert 패턴 복붙) |
| **Mysterious Name** | `x`, `tmp`, `data`, `check` 등 의도 불명; 도메인 용어 미사용 (`failed_lines`·`LINE_IDS` 등 선호) |
| **Magic Number** | `34`, `16`, `4` 등 리터럴 — `constants.py` 미사용 |
| **ECB 위반** | Entity→Controller/Boundary import; Boundary→Entity private; Controller가 Boundary 참조 |
| **Feature Envy** | 한 함수가 다른 모듈/계층 데이터를 과다 조작 (Entity가 `grid` 전체 순회하며 status 조립 등) |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 의미 | 예 |
|---|---|---|
| **P0** | 테스트·계약·ECB 위험 — **즉시 `/refactor-safe` 후보** | ECB 위반, Magic Number in `src/`, Long Method in `validate_lines` |
| **P1** | 유지보수 부담 — 다음 스프린트 | Duplicated Code (Entity 내), Mysterious Name |
| **P2** | 미미·스타일 — 여유 시 | tests 주석 정리, 변수명 개선 |

P0가 여러 개면 **Change Budget**·회귀 범위가 가장 작은 것부터 후보 순위.

---

## Change Budget (`/refactor-safe` 1회 상한)

후보 제안 시 **한 번의 safe refactor**가 이 범위를 넘지 않아야 한다.

| 항목 | 상한 |
|---|---|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

Budget 초과 스멜은 표에 `OVER BUDGET` 표기 — `/refactor-safe` 후보에서 제외하거나 분할 제안.

---

## 스멜 표 (출력 필수)

응답 본문 핵심 = 아래 표 (위치·근거·등급·Budget).

| P | 스멜 | Track | 위치 (파일:함수/줄) | 근거 (한 줄) | Budget |
|---|---|---|---|---|---|
| P0 | ECB 위반 | Logic | `src/entity/line.py:…` | Entity가 `validate_lines` import | 2파일·2메서드 ✓ |
| P1 | Duplicated Code | Logic+UI | `src/validate_lines.py:…` | R/C/D 합 검사 반복 | 3파일·3메서드 ✓ |
| P2 | Mysterious Name | UI | `tests/test_validate_lines.py:…` | `result` 외 의미 불명 변수 | 1파일 ✓ |

- 스멜 **0건**이면 빈 표 대신 `스멜 없음 — /refactor-safe 불필요` 한 줄
- 각 행은 **재현 가능**하게 (파일 경로 + 함수명 또는 줄 범위)

---

## `/refactor-safe` 후보 (1~3개)

스멜 표에서 골라 **실행 가능한 refactor 단위**만 제안:

| # | 후보 ID | P | 스멜 | 제안 작업 (한 줄) | 예상 변경 | 선행 조건 |
|---|---|---|---|---|---|---|
| 1 | `RF-001` | P0 | Magic Number | `34` → `MAGIC_CONSTANT` import | 2파일·2메서드 | pytest PASS |
| 2 | `RF-002` | P0 | ECB 위반 | Entity import 제거·순수 함수 분리 | 2파일·1메서드 | pytest PASS |

- 후보 **1~3개** (P0 우선, Budget 내)
- 각 후보에 `RF-{nnn}` ID 부여 (`/refactor-safe` 인자로 사용)

---

## 다음 안내 (필수)

출력 **마지막**에 반드시:

```markdown
## 다음 단계
- **P0 1개만** 선택 (권장: RF-001 — …)
- 실행: `/refactor-safe` (후보 ID 또는 스멜 1건 지정)
- 본 커맨드에서는 코드 수정·commit 하지 않음
```

P0가 없으면: `P0 없음 — P1 후보는 필요 시 /refactor-safe` 안내.

---

## 금지 (본 커맨드)

| 금지 | 이유 |
|---|---|
| `src/`·`tests/` **수정** | Refine ⑦ = 탐지만 |
| `git commit` | `/refactor-safe`·사용자 요청 후 |
| pytest 실패 **수정** | GREEN 범위 |
| assert 완화·skip·테스트 삭제 | 품질 훼손 |
| Budget 초과 일괄 리팩터 제안 | safe refactor 위반 |
| 스멜 없는데 임의 구조 변경 제안 | YAGNI |

---

## 보고 형식 (요약)

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 전제
- `python -m pytest tests/ -v` → N passed, 0 failed

## 스멜 표
| P | 스멜 | Track | 위치 | 근거 | Budget |
| ... |

## /refactor-safe 후보
| # | 후보 ID | P | 스멜 | 제안 작업 | 예상 변경 |
| ... |

## 다음 단계
- P0 1개만 골라 `/refactor-safe` 실행 (권장: RF-001)
```

---

## ARRR · TDD 위치

| 단계 | 커맨드 | 산출 |
|---|---|---|
| GREEN | `/green-minimal` | PASS |
| Golden | `/golden-master` | approval 기준 |
| **Refine ⑦** | **`/refactor-smell`** | **스멜 표 + 후보 (수정 없음)** |
| Refine ⑧ | `/refactor-safe` | Budget 내 실제 리팩터 + pytest |

`.cursorrules`: REFACTOR = 동작 유지; 본 커맨드는 **분석만**, 실제 변경은 `/refactor-safe`.

---

## 참조

| 문서 | 역할 |
|---|---|
| `.cursor/commands/refactor-safe.md` | (다음) Budget 내 리팩터 실행 |
| `.cursor/commands/green-minimal.md` | PASS 전제 |
| `.cursorrules` | ECB·constants·TDD |
| `magic-square-tdd` Skill | 스멜·Budget 규칙 |

### 완료 조건

- [ ] `python -m pytest tests/ -v` 전부 PASS 확인 (아니면 중단)
- [ ] 스멜 표 출력 (7종 분류·P0/P1/P2)
- [ ] Change Budget 열 표기
- [ ] `/refactor-safe` 후보 1~3개
- [ ] P0 1개 선택 → `/refactor-safe` 안내
- [ ] 코드 수정·commit 없음

---

*ARRR Refine ⑦: smell only. RF-xxx 후보로 ⑧ `/refactor-safe`에 넘긴다.*
