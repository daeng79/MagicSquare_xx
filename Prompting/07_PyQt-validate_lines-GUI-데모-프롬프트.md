# PyQt validate_lines GUI 데모 — MagicSquare_xx

> `validate_lines` API가 GREEN 완료된 뒤, **PyQt 최소 GUI 시연 데모**를 추가할 때 사용한다.

---

## 프롬프트 (복사용)

```
MagicSquare_xx에 PyQt를 이용해서 validate_lines 최소 GUI 데모를 만들어줘.

SSOT:
- @docs/PRD.md (§8 validate_lines API, status·failed_lines 계약)
- @.cursorrules (ECB, 검증 순서, 솔버·UI 제품 목표 금지 — 단, 이번은 시연용 데모로 한정)
- @Report/06_validate_lines-GREEN-Golden-Master-보고서.md (Controller 구현 완료 상태)
- @Report/07_PyQt-validate_lines-GUI-데모-보고서.md (이전 산출 참고)

---

## 목표

학습·시연용 **최소** PyQt 윈도우:
- 4×4 격자 입력 (0=�빈칸, 1~16)
- [검증] 버튼 → validate_lines(grid) 호출
- status (pass/fail/incomplete) + failed_lines 표시
- 실패 선 소속 칸 시각적 하이라이트 (선택이지만 권장)

Non-Goal (구현 금지):
- 마방진 솔버·정답 자동 채우기
- diagnose / next_check
- src/ Entity·Controller 로직 변경 (호출만)
- tests/ assert 완화·skip

---

## 구현 지침

1) 패키지 위치: gui/
   - gui/__init__.py
   - gui/demo.py — MagicSquareDemoWindow, main()

2) 프레임워크: PyQt6 (pyproject.toml [project.optional-dependencies] gui = ["PyQt6>=6.5"])

3) import:
   - sys.path에 src/ 추가 (pytest pythonpath와 동일)
   - from validate_lines import validate_lines 만 사용

4) UI 최소 구성:
   - 16개 QSpinBox (0~16)
   - 버튼: 샘플 불러오기 (tests/conftest grid_g1과 동일 격자), 초기화, 검증
   - 결과: status 한글 라벨 + 색상, failed_lines 목록
   - 힌트: 검증 순서 R1→R4→C1→C4→D1→D2, 마법상수 34

5) pyproject.toml:
   - [project.scripts] magicsquare-demo = "gui.demo:main"
   - setuptools로 gui* 패키지 등록

6) 한국어 UI 라벨·코드 주석

---

## 검증

pip install -e ".[gui]"
python gui/demo.py   # 또는 magicsquare-demo
pytest tests/ -v     # 6 passed 유지 (src/ 미변경)

---

⚠️ 규칙:
- src/validate_lines.py 수정 금지 (버그가 아니면)
- git commit은 내가 요청할 때만
- 한국어 응답

완료 보고:
- 추가·변경 파일 목록
- 실행 방법
- pytest 결과

완료 후 /export 로 Report+Prompting 쌍 갱신해줘.
```

---

## 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | `gui/demo.py` + `main()` 진입점 | ☑ |
| 2 | `validate_lines`만 호출, `src/` 미수정 | ☑ |
| 3 | status 3종 + failed_lines 표시 | ☑ |
| 4 | PyQt6 optional dependency | ☑ |
| 5 | `pytest tests/` 6 passed | ☑ |
| 6 | 솔버·diagnose 미포함 | ☑ |

---

## 실행 명령 요약

```powershell
pip install -e ".[gui]"
python gui/demo.py
magicsquare-demo
pytest tests/ -v
```

---

## 연결

| 문서 | 역할 |
|---|---|
| `Report/07_PyQt-validate_lines-GUI-데모-보고서.md` | 본 세션 산출 SSOT |
| `Report/06_validate_lines-GREEN-Golden-Master-보고서.md` | API GREEN 선행 |
| `gui/demo.py` | 데모 구현 |
| `tests/conftest.py` | 샘플 격자 `grid_g1` |

---

## GUI 확장만 (복사용)

```
MagicSquare_xx PyQt 데모(gui/demo.py)에 아래만 추가해줘. src/ tests/ 변경 최소화.

SSOT: @Report/07_PyQt-validate_lines-GUI-데모-보고서.md

요청: (예: incomplete 샘플 불러오기 버튼 / 실패 선별 현재 합 표시)

규칙:
- validate_lines 호출 유지, 솔버·diagnose 금지
- pytest 6 passed 유지
- 한국어 UI

완료 후 /export report 로 Report/07 갱신.
```

---

*Prompting/07 · PyQt GUI 데모 재현용 · MagicSquare_xx (export 2026-06-10)*
