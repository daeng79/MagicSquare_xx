# Report 템플릿 — magic-square-docs SSOT

> 형식 원본: `Report/05.REPORT.md` (없으면 본 파일).  
> ARRR 1사이클·세션 N 보고서 작성 시 [SKILL.md](SKILL.md) Step C에서 사용.

---

## 파일명

```
Report/{NN}_{주제-slug}-세션보고서.md
```

- `{NN}`: 2자리 (`04`, `10` …) — `max(Report, Prompting 번호) + 1`
- slug: 한글·영문·숫자·하이픈 (기존 `Report/`와 통일)

---

## 공통 골격

```markdown
# {제목} — MagicSquare_xx 세션 {N} 보고서

## 1. 문서 목적
- ARRR {Ask|Respond|Refine} · Phase: {phase} 1사이클 산출 기록
- (한 줄: 이번 세션에서 무엇을 완료했는지)

## 2. 세션 메타
| 항목 | 값 |
|---|---|
| 세션 | N |
| Phase | {red \| green \| refactor \| repeat} |
| Layer / Track | {entity\|boundary} / {Logic\|UI\|Logic+UI} |
| Command | {/red-test-plan, /green-minimal, …} |
| Test ID | {T-LOG-001, T-BND-002, …} |
| pytest | `{실행한 명령}` → {passed}/{failed} (실측만) |
| git status | (요약: 변경 파일 N개, 브랜치) |

## 3. 근거 문서
| 문서 | 역할 |
|---|---|
| `.cursorrules` | API·ECB·TDD |
| `docs/PRD.md` | FR·SC (있으면) |
| `Prompting/{NN}_{slug}-transcript.md` | 본 세션 대화 원문 |
| `Report/05.REPORT.md` | Report 형식 SSOT |

## 4. Phase별 STEP 본문
(아래 해당 Phase 섹션만 채움 — 나머지는 `—` 또는 생략)

## 5. 변경·산출물
| 유형 | 경로 |
|---|---|
| Report | `Report/{NN}_…` |
| Transcript | `Prompting/{NN}_…-transcript.md` |
| 코드 | (해당 시 `src/`·`tests/` 목록) |

## 6. 다음 단계
- (한 줄: 다음 Command·Phase)

---
*작성 기준: MagicSquare_xx 세션 {N} · Phase {phase} · {YYYY-MM-DD}*
```

---

## Phase: RED

```markdown
### STEP RED — 설계·스켈레톤

#### RED ③ C2C (요약)
| Test ID | FR/SC | Given → Then (한 줄) |
|---|---|---|
| T-LOG-001 | SC-1 | … |

#### RED ④ 스켈레톤
| Test ID | 함수명 | FAIL 메시지 |
|---|---|---|
| T-LOG-001 | `test_…` | RED: T-LOG-001 — … |

#### pytest (RED)
- 명령: `pytest tests/… -v`
- 결과: **N failed** (스켈레톤 `pytest.fail` — 정상)

#### 금지 준수
- [ ] `src/` 미수정
- [ ] skip/xfail 없음
```

---

## Phase: GREEN

```markdown
### STEP GREEN — 최소 구현

#### PASS Test ID
| Test ID | 함수명 | 비고 |
|---|---|---|
| T-LOG-001 | `test_…` | PASSED |

#### src/ 변경 (최소)
| 파일 | 변경 요약 |
|---|---|
| `src/entity/line.py` | … |

#### tests/ 변경
| 파일 | 변경 요약 |
|---|---|
| `tests/test_entity_line.py` | pytest.fail → assert |

#### pytest (GREEN)
- 단일: `pytest tests/…::test_… -v` → 1 passed
- 전체: `pytest tests/… -v` → N passed, 0 failed

#### golden (해당 시)
- 경로: `tests/golden/T-LOG-001.approved.txt`
- matched: yes / n/a
```

---

## Phase: REFACTOR

```markdown
### STEP REFACTOR — smell · safe

#### smell (⑦)
| P | 스멜 | 위치 | RF 후보 |
|---|---|---|---|
| P0 | Magic Number | `src/…` | RF-001 |

#### safe (⑧)
| RF ID | 스멜 | 변경 요약 | Budget |
|---|---|---|---|
| RF-001 | Magic Number | constants import | 2파일·2메서드 ✓ |

#### pytest · golden
- `pytest tests/ -v` → N passed
- golden matched: yes / ISS-{nnn} 후 UPDATE_GOLDEN
```

---

## Phase: repeat

```markdown
### STEP repeat — ARRR 1사이클 요약

| 단계 | Command | 산출 | 상태 |
|---|---|---|---|
| Ask RED ③ | `/red-test-plan` | C2C 4블록 | ✓ |
| Ask RED ④ | `/red-skeleton` | pytest.fail 스켈레톤 | ✓ |
| Respond GREEN | `/green-minimal` | src 최소·PASS | ✓ |
| Respond+ | `/golden-master` | golden matched | ✓/n/a |
| Refine ⑦ | `/refactor-smell` | 스멜 표 | ✓ |
| Refine ⑧ | `/refactor-safe` | RF-001 | ✓/— |

#### 회귀
- `python -m pytest tests/ -v` → (실측)

#### 미완·차단
- (없음 / 한 줄)
```
