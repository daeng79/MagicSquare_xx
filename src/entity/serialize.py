# Entity — golden master 직렬화 (I:/E: · S:/F:/E: SSOT)


def format_golden_payload(
    int6: tuple[int, int, int, int, int, int], error_code: str
) -> str:
    """int[6] 1-index + 에러 코드 문자열 — golden SSOT 포맷."""
    if len(int6) != 6 or any(i < 1 for i in int6):
        raise ValueError("int6는 1-index 정수 6개")
    if not error_code.startswith("E") or len(error_code) != 4:
        raise ValueError("error_code는 Exxx 형식")
    return f"I:{','.join(str(i) for i in int6)}\nE:{error_code}\n"


def format_entity_int_golden(value: int, error_code: str = "E000") -> str:
    """Entity 정수 결과 golden 페이로드."""
    return format_golden_payload((value, 1, 1, 1, 1, 1), error_code)


def format_entity_bool_golden(value: bool, error_code: str = "E000") -> str:
    """Entity 불리언 결과 golden 페이로드 (1=True, 2=False)."""
    flag = 1 if value else 2
    return format_golden_payload((flag, 1, 1, 1, 1, 1), error_code)


def format_validate_lines_golden(
    status: str, failed_lines: list[str], error_code: str = "E000"
) -> str:
    """validate_lines API 결과 golden 페이로드."""
    if not error_code.startswith("E") or len(error_code) != 4:
        raise ValueError("error_code는 Exxx 형식")
    failed = ",".join(failed_lines)
    return f"S:{status}\nF:{failed}\nE:{error_code}\n"
