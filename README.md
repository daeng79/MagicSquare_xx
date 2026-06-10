# MagicSquare_xx

4×4 부분 마방진 실습에서 **막혔을 때 어느 제약이 깨졌는지**를 구조적으로 드러내는 검증 프로젝트입니다.  
정답을 대신 찾아주는 솔버가 아니라, **판단 기준·위반 위치·검증 순서**를 고정하는 것이 목표입니다.

| | |
|---|---|
| 저장소 | [daeng79/MagicSquare_xx](https://github.com/daeng79/MagicSquare_xx) |
| 요구사항 SSOT | [`docs/PRD.md`](docs/PRD.md) |
| 도메인·TDD 규칙 | [`.cursorrules`](.cursorrules) |

---

## 진짜 문제 (Mom Test)

> 여러 제약(행·열·대각선)이 겹친 상태에서, 중간에 어디가 틀렸는지·다음에 무엇을 확인할지 판단할 수 없어 20분을 쓰고도 진행을 이어가지 못하고, 같은 유형의 과제를 다시 열지 않게 된다.

| 증거 | 내용 |
|---|---|
| ① | 대각선 합 34 맞추다 불일치 → **즉시 실습 종료** |
| ② | **20분** 후 다음 확인 단계 없이 중단 |
| ③ | 비슷한 과제 **재시도 없음** |

---

## 제품 목표

| | |
|---|---|
| **Vision** | 막힘 시 **어느 제약이 깨졌는지**·**다음 확인 순서**를 재현 가능하게 고정 |
| **Non-Goal** | 빈칸 두 칸 정답 자동 채우기, UI/DB, 솔버 |

### 성공 기준 (요약)

| SC | 내용 | 현재 API |
|---|---|---|
| SC-1 | 합 불일치 시 **어느 줄·현재 합·34와의 차이** | `validate_lines` ✅ |
| SC-2 | 검증 **순서** 문서·Rule 고정 | `validate_lines` ⚠️ 부분 |
| SC-3 | 종료 대신 **위반 목록 + 다음 한 걸음** | `diagnose` (후속) |

상세: [`docs/PRD.md` §5](docs/PRD.md)

---

## 공개 API

현재 구현 대상은 **10선 합 검증** API입니다.

```python
validate_lines(grid: list[list[int]]) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": ["R1", "C3", "D1", ...]
}
```

| `status` | 조건 |
|---|---|
| `pass` | 10선 모두 합 = 34 |
| `fail` | 하나 이상 합 ≠ 34 |
| `incomplete` | 행·열 통과, 대각선(D1/D2) 실패 |

**10선:** `R1~R4` · `C1~C4` · `D1`(↘) · `D2`(↙)  
**검증 순서:** `R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2`

후속 상위 API `diagnose(grid)` — SC-2·SC-3·`next_check` (PRD FR-020~023).

---

## 도메인 규칙

- 4×4 정수 격자 `grid`, `0` = 빈칸, 채움 `1~16`
- 마법상수 **34** (`MAGIC_CONSTANT`)
- 빈칸이 있어도 합 계산 수행
- 부분 만족(행·열만 OK) ≠ 완료

---

## 프로젝트 구조

```
MagicSquare_xx/
├── docs/
│   └── PRD.md              # FR·SC·Invariant·Contract SSOT
├── src/
│   ├── constants.py        # MAGIC_CONSTANT, LINE_IDS, VERIFICATION_ORDER
│   ├── entity/
│   │   └── line.py         # sum_line, line_sum_matches_magic (Entity)
│   └── validate_lines.py   # Controller — 공개 API
├── tests/
│   └── test_validate_lines.py   # Boundary
├── .cursor/
│   ├── commands/           # TDD Command 체인 (red-test-plan … refactor-safe)
│   └── skills/             # magic-square-tdd, magic-square-docs
├── Report/                 # 세션·Mom Test 보고서
├── Prompting/              # 재사용 프롬프트·transcript
├── .cursorrules
└── pyproject.toml
```

### ECB

| 계층 | 역할 | 위치 |
|---|---|---|
| **Entity** | 선 합 계산, 34 비교 | `src/entity/` |
| **Controller** | 고정 순서 검증, status 조립 | `src/validate_lines.py` |
| **Boundary** | 공개 API 계약 테스트 | `tests/` |

---

## 시작하기

**요구:** Python ≥ 3.10

```bash
# 개발 의존성 (pytest)
pip install -e ".[dev]"

# 테스트
python -m pytest tests/ -v
```

> 현재 `src/`·`tests/`는 **stub** 상태입니다. TDD RED/GREEN으로 FR-001~012를 순차 구현합니다.

---

## Dual-Track TDD

| Track | Layer | 대상 | Test ID |
|---|---|---|---|
| **A (UI)** | boundary | `validate_lines` | `T-BND-{nnn}` |
| **B (Logic)** | entity | `sum_line`, `line_sum_matches_magic` | `T-LOG-{nnn}` |

### Command 체인 (Cursor)

```
/red-test-plan → /red-skeleton → /green-minimal → /golden-master
→ /refactor-smell → /refactor-safe
```

| Phase | Command | 산출 |
|---|---|---|
| RED | `red-test-plan`, `red-skeleton` | C2C 설계표, pytest.fail 스켈레톤 |
| GREEN | `green-minimal`, `golden-master` | 최소 구현, golden |
| REFACTOR | `refactor-smell`, `refactor-safe` | 스멜 탐지, safe refactor |

Skill: `.cursor/skills/magic-square-tdd/` · 문서 Export: `magic-square-docs`

사이클: **RED → GREEN → REFACTOR** (한 번에 한 Phase). 상세는 [`docs/PRD.md` §10](docs/PRD.md).

---

## 구현 상태

| 항목 | 상태 |
|---|---|
| PRD·Command·Skill | ✅ 정의 완료 |
| `constants.py` | ✅ |
| `validate_lines` / Entity | 🔲 stub — RED/GREEN 대기 |
| `diagnose` | 🔲 후속 세션 |

---

## 범위 밖 (하지 않음)

- 마방진 **솔버**·정답 자동 채우기
- UI / DB / Web
- TDD 도구 도입을 **제품 목표**로 삼기
- 대각선 함수만 따로 추가하는 식의 기능 나열

---

## 문서 인덱스

| NN | Report | Prompting | 주제 |
|---|---|---|---|
| 01 | [MomTest 인터뷰](Report/01_4x4-마방진-MomTest-인터뷰-보고서.md) | — | Mom Test |
| 01 | [역할분리 시뮬레이션](Report/01_역할분리-MomTest-시뮬레이션-보고서.md) | [프롬프트](Prompting/01_역할분리-MomTest-시뮬레이션-프롬프트.md) | Mom Test |
| 02 | [세션3 워크북](Report/02_MagicSquare_1004-세션3-워크북-보고서.md) | [프롬프트](Prompting/02_MagicSquare_1004-세션3-워크북-프롬프트.md) | 8계층 |
| 03 | [validate_lines 정합성](Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md) | [프롬프트](Prompting/03_validate_lines-R-G-I-O-정합성-확인-프롬프트.md) | Contract |
| 04 | [ARRR TDD 체인](Report/04_ARRR-TDD-Command-Skill-체인-보고서.md) | [프롬프트](Prompting/04_ARRR-TDD-Command-Skill-체인-프롬프트.md) | Command·Skill |

| 문서 | 설명 |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | FR·SC·Invariant·API Contract |
| [`Prompting/cursor_mom_test_workbook_discussion.md`](Prompting/cursor_mom_test_workbook_discussion.md) | 대화 아카이브 |

---

## 참고

- 작성자: 배대웅 · 리뷰어: 홍길동 (저장소 설명)
- MagicSquare_1004 · 세션 3+ · 2026
