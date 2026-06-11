# validate_lines GREEN·Golden Master·커버리지 — MagicSquare_xx

> RED 스켈레톤 PASS 이후 **GREEN 최소 구현**, **Golden Master**, **pytest-cov 커버리지**를 한 세션에서 진행할 때 사용한다.

---

## 프롬프트 (복사용)

```
MagicSquare_xx 세션 3 — RED 스켈레톤을 GREEN 처리하고 Golden Master·커버리지까지 완료해줘.

SSOT:
- @docs/PRD.md (§6 FR, §8 API, §12 Traceability, INV-007 Golden)
- @.cursorrules (ECB, 검증 순서, TDD)
- @Report/05_PRD-Traceability-RED-테스트-플랜-보고서.md
- @Report/06_validate_lines-GREEN-Golden-Master-보고서.md (이전 산출 참고)

대상 Test ID (전부 PASS 전제):
- Track B (Logic): T-LOG-001, T-LOG-002
- Track A (Boundary): T-BND-001, T-BND-002, T-BND-003, T-BND-004

---

## 1. GREEN (/green-minimal)

Phase: green | Layer: entity+boundary | Track: Logic+UI

src/ 최소 구현만 (과잉 로직 금지):
- src/entity/line.py — sum_line, line_sum_matches_magic (MAGIC_CONSTANT SSOT)
- src/validate_lines.py — VERIFICATION_ORDER 고정, status/failed_lines 조립
  - pass: 10선 모두 34
  - incomplete: 행·열 8선 OK + D1/D2만 실패
  - fail: 그 외

tests/ — pytest.fail → PRD Then assert로 교체 (완화·skip 금지)

pytest tests/ -v → 6 passed 확인

---

## 2. 커버리지 (pytest-cov)

명령:
  pytest tests/ --cov=src --cov-report=term-missing
  pytest tests/ --cov=src --cov-report=html
  Invoke-Item .\htmlcov\index.html

htmlcov/index.html 없으면 --cov-report=html 로 재생성.
coverage 정적 파일 오류 시: pip install --force-reinstall coverage

---

## 3. Golden Master (/golden-master)

Phase: green | Layer: entity+boundary | Track: Logic+UI

1) tests/_approval.py — assert_matches_golden (없으면 생성)
2) src/entity/serialize.py — format_golden_payload, format_entity_int_golden,
   format_entity_bool_golden, format_validate_lines_golden
3) tests/golden/{TestID}.approved.txt — Test ID 1:1
4) pyproject.toml pythonpath에 tests 추가 (_approval import)

페이로드:
- Logic: I:{int6 1-index}\nE:E000\n
- Boundary: S:{status}\nF:{failed_lines}\nE:E000\n

절차:
  $env:UPDATE_GOLDEN="1"; pytest tests/ -v   # 기준 생성
  pytest tests/ -v                             # matched

golden 수동 편집 금지.

---

⚠️ 규칙:
- RED 단계에서 src/ 선행 수정 금지 (이미 GREEN이면 src/ 수정 OK)
- E001~E005 위반 금지 (과잉 구현, assert 완화, skip, 솔버)
- git commit은 내가 요청할 때만
- 한국어 주석·응답

완료 보고:
- PASS Test ID 표
- 변경 파일 목록
- pytest 결과 (6 passed)
- 커버리지 % · Missing 줄
- golden matched yes/no

완료 후 /export 로 Report+Prompting 쌍 갱신해줘.
```

---

## 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | T-LOG-001~002, T-BND-001~004 pytest PASS | ☑ |
| 2 | `pytest.fail` 잔존 없음 | ☑ |
| 3 | constants SSOT (리터럴 34 금지) | ☑ |
| 4 | ECB — Entity가 Controller import 안 함 | ☑ |
| 5 | `tests/_approval.py` + 6 golden 파일 | ☑ |
| 6 | UPDATE_GOLDEN 없이 matched | ☑ |
| 7 | 커버리지 term-missing 실행 | ☑ |

---

## pytest 명령 요약

```powershell
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing
pytest tests/ --cov=src --cov-report=html
$env:UPDATE_GOLDEN="1"; pytest tests/ -v
Invoke-Item .\htmlcov\index.html
```

---

## 연결

| 문서 | 역할 |
|---|---|
| `Report/06_validate_lines-GREEN-Golden-Master-보고서.md` | 본 세션 산출 SSOT |
| `Report/05_PRD-Traceability-RED-테스트-플랜-보고서.md` | RED 선행 |
| `.cursor/commands/green-minimal.md` | GREEN Command |
| `.cursor/commands/golden-master.md` | Golden Command |

---

## Golden PASS만 재검증 (복사용)

```
MagicSquare_xx — Golden Master · Approval Test GREEN PASS가 완료됐는지 검증해줘.

SSOT:
- @Report/06_validate_lines-GREEN-Golden-Master-보고서.md
- @.cursor/commands/golden-master.md
- @.cursorrules

확인:
1) pytest tests/ -v → 6 passed
2) UPDATE_GOLDEN 없이 tests/golden/*.approved.txt matched
3) src/entity/line.py, src/validate_lines.py, src/entity/serialize.py, tests/_approval.py 존재

미완이면 GREEN(/green-minimal) 후 Golden(/golden-master) 절차 수행.
완료면 보고만 (코드 변경 불필요 시 src/ 수정 금지).

완료 후 /export 로 Report/06·Prompting/06 갱신.
```

---

*Prompting/06 · GREEN+Golden 재현용 · MagicSquare_xx (export 갱신 2026-06-10)*
