# entity line Dual-Track REFACTOR — MagicSquare_xx

> GREEN+Golden 완료 후 `src/entity/line.py`를 **Logic Track**·**UI Track**으로 분리하는 `/refactor-safe` 세션 재현용.

---

## 프롬프트 (복사용)

```
@src/entity/line.py 를 Dual Track TDD 기준으로 리팩터링해줘.

Track 분리
- UI Track
- Logic Track

진행 순서
- 테스트 확인
- Logic 부터 리팩토링
- 다음에 UI 리팩토링
- 리팩토링 후 다시 테스트

규칙
- UI 와 Logic 코드를 섞지 말 것
- 전체 테스트가 통과해야 완료되었다고 판단할 것

SSOT:
- @docs/PRD.md (FR-010~011, NFR-007 Change Budget)
- @.cursorrules (ECB, TDD)
- @Report/06_validate_lines-GREEN-Golden-Master-보고서.md (GREEN 선행)
- @Report/08_entity-line-Dual-Track-리팩터-보고서.md (목표 구조 참고)
- @.cursor/skills/magic-square-tdd/SKILL.md (Track B=Logic, Track A=UI)

---

Phase: refactor | Layer: entity | Track: Logic → UI

## 1. 전제

pytest tests/ -v → 전부 PASS 아니면 중단 (GREEN 먼저)

## 2. Logic Track (먼저)

신규 src/entity/line_logic.py:
- sum_line(cells) — 4칸 합
- line_sum_equals(cells, magic_constant) — 합 == 마법상수 (기본값 없음)
- constants import 금지, I/O·상태 없음

## 3. UI Track (다음)

src/entity/line.py — facade만:
- MAGIC_CONSTANT 기본값으로 line_sum_matches_magic 공개
- line_logic.line_sum_equals 위임
- sum_line re-export (__all__ 유지)
- 로직 코드 inline 금지

## 4. ECB·Budget

- validate_lines.py는 entity.line만 import (변경 최소)
- tests/ 변경 없이 동작 불변
- Change Budget: 파일≤3, 클래스≤1, 메서드≤3
- E001~E005 위반 금지, 기능 추가·버그 수정 금지

## 5. 회귀

pytest tests/ -v → 6 passed
UPDATE_GOLDEN 없이 golden matched 확인

완료 보고:
- Logic/UI 파일 역할 표
- Change Budget
- pytest·golden 결과

완료 후 /export 로 Report+Prompting 쌍 갱신해줘.
```

---

## 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | 리팩터 전 `pytest tests/ -v` PASS | ☑ |
| 2 | `line_logic.py` — constants import 없음 | ☑ |
| 3 | `line.py` — 로직 inline 없음, facade만 | ☑ |
| 4 | `from entity.line import sum_line, line_sum_matches_magic` 유지 | ☑ |
| 5 | Change Budget 준수 (파일 2) | ☑ |
| 6 | 리팩터 후 6 passed · golden matched | ☑ |

---

## pytest 명령

```powershell
pytest tests/ -v
pytest tests/test_entity_line.py -v
pytest tests/test_validate_lines.py -v
```

---

## 연결

| 문서 | 역할 |
|---|---|
| `Report/08_entity-line-Dual-Track-리팩터-보고서.md` | 본 세션 산출 SSOT |
| `Report/06_validate_lines-GREEN-Golden-Master-보고서.md` | GREEN+Golden 선행 |
| `.cursor/commands/refactor-safe.md` | Safe Refactor Command |
| `.cursor/commands/refactor-smell.md` | 후속 스멜 탐지 |

---

## REFACTOR 회귀만 재검증 (복사용)

```
MagicSquare_xx — entity line Dual-Track REFACTOR가 완료됐는지 검증해줘.

SSOT:
- @Report/08_entity-line-Dual-Track-리팩터-보고서.md
- @.cursor/commands/refactor-safe.md

확인:
1) src/entity/line_logic.py 존재 — sum_line, line_sum_equals (constants import 없음)
2) src/entity/line.py — facade만, line_logic 위임
3) pytest tests/ -v → 6 passed
4) UPDATE_GOLDEN 없이 golden matched

미완이면 위 SSOT 구조로 REFACTOR 수행.
완료면 보고만 (코드 변경 불필요 시 src/ 수정 금지).

완료 후 /export 로 Report/08·Prompting/08 갱신.
```

---

*Prompting/08 · entity line Dual-Track REFACTOR 재현용 · MagicSquare_xx (export 2026-06-11)*
