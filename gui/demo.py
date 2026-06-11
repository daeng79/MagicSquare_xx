"""PyQt 최소 GUI 데모 — 4×4 격자 입력 후 validate_lines 결과 표시."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# src 모듈 import (pytest pythonpath와 동일)
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from validate_lines import validate_lines  # noqa: E402

GRID_SIZE = 4
# 부분 마방진 샘플 (빈칸 2개)
SAMPLE_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]

_STATUS_STYLE = {
    "pass": "color: #1a7f37; font-weight: bold;",
    "fail": "color: #cf222e; font-weight: bold;",
    "incomplete": "color: #bf8700; font-weight: bold;",
}

_STATUS_LABEL = {
    "pass": "통과 — 10선 모두 합 34",
    "fail": "실패 — 합 불일치 선 있음",
    "incomplete": "미완료 — 행·열 OK, 대각선 실패",
}


class MagicSquareDemoWindow(QMainWindow):
    """4×4 격자 편집 및 validate_lines 호출 데모."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_xx — validate_lines 데모")
        self.setMinimumSize(420, 380)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addWidget(self._build_grid_group())
        root.addLayout(self._build_button_row())
        root.addWidget(self._build_result_group())

    def _build_grid_group(self) -> QGroupBox:
        group = QGroupBox("4×4 격자 (0 = 빈칸, 1~16 = 채움)")
        layout = QGridLayout(group)
        layout.setSpacing(6)

        self._cells: list[list[QSpinBox]] = []
        mono = QFont("Consolas", 14)
        mono.setStyleHint(QFont.StyleHint.Monospace)

        for row in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(0, 16)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setFont(mono)
                spin.setMinimumWidth(52)
                spin.setMinimumHeight(40)
                layout.addWidget(spin, row, col)
                row_boxes.append(spin)
            self._cells.append(row_boxes)

        return group

    def _build_button_row(self) -> QHBoxLayout:
        row = QHBoxLayout()

        load_btn = QPushButton("샘플 불러오기")
        load_btn.clicked.connect(self._load_sample)
        row.addWidget(load_btn)

        clear_btn = QPushButton("초기화")
        clear_btn.clicked.connect(self._clear_grid)
        row.addWidget(clear_btn)

        row.addStretch()

        validate_btn = QPushButton("검증")
        validate_btn.setDefault(True)
        validate_btn.clicked.connect(self._on_validate)
        row.addWidget(validate_btn)

        return row

    def _build_result_group(self) -> QGroupBox:
        group = QGroupBox("검증 결과")
        layout = QVBoxLayout(group)

        self._status_label = QLabel("검증 버튼을 눌러 주세요.")
        self._status_label.setWordWrap(True)
        layout.addWidget(self._status_label)

        self._failed_label = QLabel("")
        self._failed_label.setWordWrap(True)
        layout.addWidget(self._failed_label)

        hint = QLabel(
            "검증 순서: R1→R4 → C1→C4 → D1→D2  ·  마법상수 34"
        )
        hint.setStyleSheet("color: #656d76; font-size: 11px;")
        layout.addWidget(hint)

        return group

    def _read_grid(self) -> list[list[int]]:
        return [[box.value() for box in row] for row in self._cells]

    def _write_grid(self, grid: list[list[int]]) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setValue(grid[row][col])

    def _load_sample(self) -> None:
        self._write_grid(SAMPLE_GRID)
        self._status_label.setText("샘플 격자를 불러왔습니다. 검증을 실행해 보세요.")
        self._status_label.setStyleSheet("")
        self._failed_label.setText("")
        self._clear_highlights()

    def _clear_grid(self) -> None:
        self._write_grid([[0] * GRID_SIZE for _ in range(GRID_SIZE)])
        self._status_label.setText("격자를 초기화했습니다.")
        self._status_label.setStyleSheet("")
        self._failed_label.setText("")
        self._clear_highlights()

    def _clear_highlights(self) -> None:
        for row in self._cells:
            for box in row:
                box.setStyleSheet("")

    def _highlight_failed_lines(self, failed_lines: list[str]) -> None:
        """실패한 선에 속한 칸을 연한 빨간 배경으로 표시."""
        self._clear_highlights()
        failed = set(failed_lines)
        highlight = "background-color: #ffebe9;"

        for line_id in failed:
            for row, col in _cells_in_line(line_id):
                self._cells[row][col].setStyleSheet(highlight)

    def _on_validate(self) -> None:
        grid = self._read_grid()
        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]

        self._status_label.setText(_STATUS_LABEL[status])
        self._status_label.setStyleSheet(_STATUS_STYLE[status])

        if failed:
            self._failed_label.setText(
                f"실패 선 ({len(failed)}): {', '.join(failed)}"
            )
            self._highlight_failed_lines(failed)
        else:
            self._failed_label.setText("실패한 선 없음")
            self._clear_highlights()


def _cells_in_line(line_id: str) -> list[tuple[int, int]]:
    """선 ID에 해당하는 (행, 열) 좌표 목록."""
    if line_id.startswith("R"):
        row = int(line_id[1]) - 1
        return [(row, col) for col in range(GRID_SIZE)]
    if line_id.startswith("C"):
        col = int(line_id[1]) - 1
        return [(row, col) for row in range(GRID_SIZE)]
    if line_id == "D1":
        return [(i, i) for i in range(GRID_SIZE)]
    if line_id == "D2":
        return [(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)]
    return []


def main() -> None:
    app = QApplication(sys.argv)
    window = MagicSquareDemoWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
