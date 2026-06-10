# validate_lines · Report/08 R-G-I-O 정합성 확인 — MagicSquare_xx

> Report/08 워크북의 R-G-I-O·성공 기준이 `validate_lines` 계약과 맞는지 **확인만** 할 때 사용한다.

---

## 프롬프트 (복사용)

```
@Report/08_MagicSquare_1004-세션3-워크북-보고서.md 의 R-G-I-O·성공 기준이 validate_lines 계약과 맞는지 ‘확인만’ 한다.

⚠️ 규칙:
- 파일은 만들지 않는다 (Ask/확인 전용). export가 필요하면 /export 로 별도 요청.
- 워크스페이스·GitHub·Contract 문서에서 validate_lines 정의를 먼저 탐색한다.
- 공식 Contract가 없으면 Report/08 Rule·Test Loop·MagicSquareJudge/isMagic 맥락에서 추론한 validate_lines와 대조한다.
- 구현·Contract 신규 작성·코드 변경은 하지 않는다.

확인 항목:
1) validate_lines 존재 여부 (코드·문서·테스트)
2) 추론한 validate_lines 계약 (입력·출력·범위)
3) R-G-I-O 4항목별 대조 (✅ / ⚠️ / ❌)
4) SC-1~3별 대조 (validate_lines 단독 충족 여부)
5) 추가 불일치·공백 (diagnose vs validate_lines 2계층, duplicate/range, 빈칸 줄 합 판정 등)
6) 종합 판정 한 줄 + Contract 세션 권장

출력 형식:
- 조사 범위 표
- 추론 validate_lines 계약 표
- R-G-I-O 대조 표
- SC 대조 표
- 종합 판정 (Input / Output / SC-1~3)
- (선택) diagnose vs validate_lines 권장 분리
```

---

## 확인 체크리스트 (에이전트 자체 점검)

| # | 항목 | 통과 기준 |
|---|---|---|
| 1 | validate_lines 탐색 | 워크스페이스 + GitHub 검색 결과 명시 |
| 2 | 대조 기준 명시 | 공식 없을 때 추론 근거(Report/08 Rule·Test Loop) 기록 |
| 3 | SC-1 | line 위치·actual·expected=34 ↔ validate_lines 핵심 |
| 4 | SC-2 | 검증 순서 — validate_lines 단독 vs Rule 전체 구분 |
| 5 | SC-3 | next_check — validate_lines 밖임을 명시 |
| 6 | 2계층 결론 | validate_lines(하위) + diagnose(상위) 권장 여부 |

---

## 저장 지시

확인 완료 후 export 시:

- **보고서:** `Report/09_validate_lines-R-G-I-O-정합성-확인-보고서.md`
- **프롬프트:** `Prompting/09_validate_lines-R-G-I-O-정합성-확인-프롬프트.md` (본 파일)

---

## 관련 문서

| 파일 | 설명 |
|---|---|
| `Report/08_MagicSquare_1004-세션3-워크북-보고서.md` | 대조 대상 — R-G-I-O, SC, Rule, Test Loop |
| `Report/09_validate_lines-R-G-I-O-정합성-확인-보고서.md` | 본 프롬프트로 생성한 정합성 확인 보고서 |
| `Report/06_4x4-마방진-MomTest-인터뷰-보고서.md` | Mom Test 증거 원본 |
| `Prompting/08_MagicSquare_1004-세션3-워크북-프롬프트.md` | 세션 3 워크북 생성 프롬프트 |

---

*MagicSquare_1004 · validate_lines 정합성 확인 프롬프트 · 2026*
