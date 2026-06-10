# PRD §12 Traceability RED 테스트 플랜 — MagicSquare_xx

> `docs/PRD.md` §12 추적성 표의 Test ID에 대해 **Dual-Track RED 테스트 플랜**(C2C 4블록)을 작성할 때 사용한다.  
> `/red-test-plan` Command와 동일 산출물. **파일 Write 없음** — 설계만.

---

## 프롬프트 (복사용)

```
MagicSquare_xx PRD §12 Traceability에 해당하는 RED 테스트 플랜을 작성해줘.

SSOT:
- @docs/PRD.md (특히 §6 FR, §8 API, §12 Traceability 233–241행)
- @.cursorrules
- @Report/05_PRD-Traceability-RED-테스트-플랜-보고서.md (이전 산출 참고)

대상 Test ID:
- Track B (Logic): T-LOG-001, T-LOG-002
- Track A (Boundary): T-BND-001, T-BND-002, T-BND-003, T-BND-004
- 후속 제외: FR-022 / next_check (diagnose)

⚠️ 규칙:
- Phase: red — tests/·src/ 파일 생성·수정 금지 (설계만)
- C2C Rule1~3: FR 1개 → To-Do 1개 → Test ID 1개 → Given/When/Then
- Dual-Track: Logic(entity) 묶음 먼저, Boundary(validate_lines) 묶음 다음
- Domain Mock 금지 (E002)
- skip/xfail·assert 완화 금지 (E003/E004)
- 솔버·정답 채우기·UI·DB 금지 (E005)
- git commit은 내가 요청할 때만

출력 형식 (4블록):
1. C2C 표 — Rule1~3, Given/When/Then
2. Track B 표 — RED 시나리오, Invariant, Expected RED Failure
3. 테스트 플랜 — 파일 경로, 함수명, conftest 픽스처, pytest 명령, RED 묶음 범위
4. ECB·Mock 점검 — 전 Test ID PASS 확인

격자 픽스처 (Boundary):
- grid_r1_fail: R1 합 40
- grid_d1_fail: D1(↘) 합 ≠ 34
- grid_incomplete_d1: 행·열 8선 합 34, D1=40 → incomplete
- grid_multi_fail: R1·R3 동시 실패 → failed_lines 순서 검증

마지막 줄: /red-skeleton 으로 넘길 준비됐다

완료 후 /export 로 Report+Prompting 쌍 갱신해줘.
```

---

## 체크리스트 (에이전트 자체 점검)

| # | 항목 | 확인 |
|---|---|---|
| 1 | PRD §12 모든 Test ID 매핑 (후속 FR-022 제외 명시) | ☐ |
| 2 | Logic·Boundary RED 묶음 분리 | ☐ |
| 3 | Given 격자 수치 검증 (행·열·D1 합) | ☐ |
| 4 | T-BND-003 `incomplete` vs T-BND-001/002 `fail` 구분 | ☐ |
| 5 | T-BND-004 `VERIFICATION_ORDER` 순서 assert | ☐ |
| 6 | ECB 점검 전부 PASS | ☐ |
| 7 | src/·tests/ Write 없음 | ☐ |

---

## 저장 지시

```
/export
```

- Report: `Report/05_PRD-Traceability-RED-테스트-플랜-보고서.md`
- Prompting: `Prompting/05_PRD-Traceability-RED-테스트-플랜-프롬프트.md` (본 파일)

---

## 선택 후속

| Command | 대상 |
|---|---|
| `/red-skeleton` | Logic 묶음 `T-LOG-001~002` → `tests/test_entity_line.py` |
| `/green-minimal` | `src/entity/line.py` 최소 구현 |
| `/red-skeleton` | Boundary 묶음 `T-BND-001~004` → `tests/test_validate_lines.py` + conftest |
| `/green-minimal` | `src/validate_lines.py` 최소 구현 |

---

*MagicSquare_xx · PRD Traceability RED 테스트 플랜 · 2026-06-10*
