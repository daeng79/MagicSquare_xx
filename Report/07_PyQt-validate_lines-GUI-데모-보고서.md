# PyQt validate_lines GUI 데모 — MagicSquare_xx

## 1. 문서 목적

- `validate_lines` 공개 API를 **PyQt6 최소 GUI**로 시각화하는 데모 세션 산출물을 기록한다.
- PRD Non-Goal(UI/DB/Web)과 별도로, **학습·시연용 프레젠테이션 레이어**로 `gui/` 패키지를 추가한 범위·구조·실행 방법을 SSOT로 남긴다.
- 후속 `diagnose`·SC-3(`next_check`) UI 확장 시 참조한다.

## 2. 근거 문서

| 문서 | 역할 |
|---|---|
| `docs/PRD.md` | §2.4 Non-Goal(UI)·§8 `validate_lines` API·SC-1 |
| `.cursorrules` | ECB·검증 순서·도메인 규칙 |
| `Report/06_validate_lines-GREEN-Golden-Master-보고서.md` | GREEN 완료·`validate_lines` 구현 SSOT |
| `Report/03_validate_lines-R-G-I-O-정합성-확인-보고서.md` | Controller/Entity 분리 |
| `tests/conftest.py` | 샘플 격자 `grid_g1` (GUI SAMPLE_GRID와 동일) |
| `Prompting/07_PyQt-validate_lines-GUI-데모-프롬프트.md` | 본 보고서 재생성용 프롬프트 |

---

## 3. 세션 요약

| 항목 | 내용 |
|---|---|
| 사용자 요청 | MagicSquare_xx에 **PyQt 최소 GUI 데모** 구현 |
| 프레임워크 | **PyQt6** ≥ 6.5 |
| ECB 위치 | **프레젠테이션** — `src/` Entity·Controller **미수정** |
| 검증 | `pytest tests/ -q` → **6 passed** (기존 Boundary 회귀 없음) |
| 범위 | 솔버·정답 채우기·`diagnose`·입력 유효성 검사 **미포함** |

---

## 4. 산출물

### 4.1 파일 구조

```
MagicSquare_xx/
├── gui/
│   ├── __init__.py          # 패키지 마커
│   └── demo.py              # MagicSquareDemoWindow · main()
└── pyproject.toml           # [gui] 옵션 · magicsquare-demo 스크립트
```

### 4.2 `gui/demo.py` — 주요 구성

| 구성 요소 | 역할 |
|---|---|
| `MagicSquareDemoWindow` | `QMainWindow` — 4×4 `QSpinBox` 격자 |
| `_read_grid` / `_write_grid` | UI ↔ `list[list[int]]` 변환 |
| `_on_validate` | `validate_lines(grid)` 호출·결과 표시 |
| `_highlight_failed_lines` | 실패 선 소속 칸 연한 빨간 배경 |
| `_cells_in_line` | 선 ID → (행, 열) 좌표 (UI 전용) |
| `SAMPLE_GRID` | `conftest.grid_g1`과 동일한 부분 마방진 |
| `main()` | `QApplication` 진입점 |

### 4.3 UI 기능

| 기능 | 설명 |
|---|---|
| 4×4 스핀박스 | 값 범위 0(빈칸)~16, 등폭 모노스페이스 폰트 |
| 샘플 불러오기 | `SAMPLE_GRID` 로드 |
| 초기화 | 전 칸 0 |
| 검증 | `validate_lines` 호출 (기본 버튼) |
| 결과 표시 | `status` 한글 라벨 + 색상 (`pass`/`fail`/`incomplete`) |
| 실패 선 목록 | `failed_lines` ID를 검증 순서대로 나열 |
| 하이라이트 | 실패 선에 속한 칸 `#ffebe9` 배경 |
| 힌트 | 검증 순서·마법상수 34 안내 |

### 4.4 `status` 표시 매핑

| API `status` | UI 라벨 (요약) | 색상 |
|---|---|---|
| `pass` | 통과 — 10선 모두 합 34 | 녹색 |
| `fail` | 실패 — 합 불일치 선 있음 | 빨간색 |
| `incomplete` | 미완료 — 행·열 OK, 대각선 실패 | 주황색 |

### 4.5 `pyproject.toml` 변경

| 항목 | 내용 |
|---|---|
| `[build-system]` | setuptools 백엔드 (패키지·스크립트 등록) |
| `[tool.setuptools.packages.find]` | `gui*` 패키지 탐색 |
| `[project.optional-dependencies] gui` | `PyQt6>=6.5` |
| `[project.scripts]` | `magicsquare-demo = "gui.demo:main"` |

---

## 5. ECB·계약 준수

| 계층 | 본 세션 | 비고 |
|---|---|---|
| Entity | 변경 없음 | `src/entity/line.py` |
| Controller | 변경 없음 | `src/validate_lines.py` — GUI가 **유일 호출자**(런타임) |
| Boundary | 변경 없음 | `tests/test_validate_lines.py` |
| Presentation | **신규** | `gui/demo.py` — I/O·Qt 위젯만 |

- GUI는 `sys.path`에 `src/`를 추가해 `validate_lines`만 import한다.
- `_cells_in_line`은 **표시용**이며 Controller의 `_cells_for_line`과 역할이 겹치나, ECB 분리를 위해 `src/`에 역방향 의존을 두지 않았다.
- 솔버·자동 채우기·격자 유효성(중복·빈칸 개수) 검사는 **의도적 미구현**.

---

## 6. PRD와의 관계

| PRD | 본 데모 |
|---|---|
| §2.4 Non-Goal: UI/DB/Web | 제품 목표 범위 밖 — **시연·학습용 데모**로 한정 |
| SC-1: 합 불일치 시 어느 줄 | `failed_lines` ID 목록 + 칸 하이라이트 (**현재 합·차이 수치는 미표시**) |
| SC-2: 검증 순서 고정 | 힌트 라벨·`failed_lines` 순서(API 보장) |
| SC-3: `next_check` | 미구현 — `diagnose` 후속 |

---

## 7. 실행 방법

```powershell
# 의존성 (개발 + GUI)
pip install -e ".[dev,gui]"

# 데모 실행 (택 1)
python gui/demo.py
magicsquare-demo

# 회귀 테스트
pytest tests/ -v
```

**요구:** Python ≥ 3.10 · PyQt6 (GUI 옵션)

---

## 8. 검증 결과

| 검사 | 결과 |
|---|---|
| `from gui.demo import MagicSquareDemoWindow` | import OK |
| `pytest tests/ -q` | 6 passed |
| `src/` 수정 | 없음 |
| Golden / Approval | 변경 없음 |

---

## 9. 한계·후속 (범위 밖)

| 항목 | 상태 |
|---|---|
| 격자 입력 검증 (0 두 개·1~16 중복) | 미구현 |
| 선별 **현재 합·34와의 차이** 표시 (SC-1 완전 충족) | 미구현 |
| `incomplete` 전용 샘플 버튼 | 미구현 |
| `diagnose`·`next_check` UI | 후속 세션 |
| GUI 자동 테스트 (pytest-qt 등) | 미도입 |
| README GUI 섹션 | 미갱신 (필요 시 별도) |

---

## 10. 변경 파일 목록

| 파일 | 동작 |
|---|---|
| `gui/__init__.py` | 신규 |
| `gui/demo.py` | 신규 |
| `pyproject.toml` | gui 의존성·스크립트·setuptools 설정 추가 |

---

*작성 기준: MagicSquare_1004 세션 3+ · PyQt GUI 데모 · 2026-06-10*
