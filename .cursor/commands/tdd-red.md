# TDD RED — validate_lines

> `validate_lines(grid)` 공개 API에 대한 **RED 단계 전용** 커맨드.  
> 실패하는 테스트를 `tests/`에 먼저 작성한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: RED
```

---

## RED 절차

1. **대상 확인** — `.cursorrules` API·status 정의·10선(R1~R4·C1~C4·D1·D2) 준수
2. **테스트 1개 작성** — `tests/test_validate_lines.py` (또는 동일 Boundary)에 추가
3. **실행** — `pytest tests/test_validate_lines.py -v`
4. **실패 확인** — `FAILED` 또는 assertion error (구현 없음·`...` stub이면 정상)
5. **보고** — 아래 [보고 형식](#보고-형식)으로 결과 전달

한 RED 사이클 = **테스트 1개** (여러 시나리오를 한 함수에 몰아넣지 않음).

---

## AAA 절차

각 테스트 함수는 **Arrange → Act → Assert** 순서를 주석으로 구분한다.

| 단계 | 내용 |
|---|---|
| **Arrange** | 4×4 `grid` 준비 (`0`=빈칸, 1~16). Mom Test·SC에 맞는 시나리오 |
| **Act** | `result = validate_lines(grid)` |
| **Assert** | `result["status"]`, `result["failed_lines"]`를 계약대로 검증 |

```python
def test_행1_합이_34가_아니면_failed_lines에_R1():
    # Arrange
    grid = [
        [1, 2, 3, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R1" in result["failed_lines"]
```

---

## pytest 예시 (RED 시나리오)

### SC-1 — 합 불일치 시 어느 선인지 드러냄

```python
def test_대각선_D1_합이_34가_아니면_failed_lines에_D1():
    # Arrange — 행·열은 통과, D1만 실패하는 격자
    grid = [ ... ]  # 4×4, D1 합 ≠ 34

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] in ("fail", "incomplete")
    assert "D1" in result["failed_lines"]
```

### SC-2 — 행·열 OK + 대각선 FAIL → incomplete

```python
def test_행열_통과_대각선_실패면_status_incomplete():
    # Arrange — R1~R4·C1~C4 합=34, D1 또는 D2 실패
    grid = [ ... ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert any(line in result["failed_lines"] for line in ("D1", "D2"))
```

### SC-3 — 막힘 상태에서 failed_lines 비어 있지 않음

```python
def test_막힘_격자는_failed_lines가_비어있지_않다():
    # Arrange — 최소 1선 실패 격자
    grid = [ ... ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert len(result["failed_lines"]) >= 1
```

### pass — 10선 모두 34 (GREEN 준비용, RED에서는 선택)

```python
def test_10선_모두_34이면_status_pass():
    # Arrange — 완성 4×4 마방진
    grid = [ ... ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

기대 RED 결과: `1 failed` (또는 N failed) — **구현 전이므로 실패가 정상**.

---

## 금지 (RED)

| 금지 | 이유 |
|---|---|
| `src/` 수정 | GREEN 단계 전용 |
| assert 완화 (`==` → `in`, 조건 삭제 등) | RED 회피 |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| 실패 테스트 삭제·주석 처리 | RED 회피 |
| 솔버·정답 채우기·Entity 직접 테스트 | Boundary는 공개 API만 |

---

## 보고 형식

RED 완료 시 아래 템플릿으로 보고:

```markdown
Phase: RED

## 추가한 테스트
- `test_<이름>` — (한 줄: 무엇을 검증하는지)

## Arrange 요약
- 격자 특성: (예: R1 합=30, D1 합=32, 빈칸 2개)

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py::test_<이름> -v`
- 결과: FAILED — (assertion 메시지 한 줄)

## Mom Test / SC 연결
- SC-? / 증거 ①|②|③

## 다음 단계
- GREEN: `src/validate_lines.py`(및 Entity) 최소 구현으로 위 테스트 통과
```

---

## 참조

- API: `validate_lines(grid) -> {status: pass|fail|incomplete, failed_lines: [...]}`
- 검증 순서: `R1 → R2 → R3 → R4 → C1 → C2 → C3 → C4 → D1 → D2`
- Boundary: `tests/test_validate_lines.py`
