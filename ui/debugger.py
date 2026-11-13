
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QDialog,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor


class DebuggerPanel(QFrame):

    start_requested = Signal()
    step_requested = Signal()
    stop_requested = Signal()
    reset_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("DebuggerPanel")

        self.setStyleSheet("""
            QFrame#DebuggerPanel {
                background-color: #181B22;
                border: 1px solid #292D36;
                border-radius: 8px;
            }

            QLabel {
                color: #E5E7EB;
            }

            QLabel#DebuggerStatus {
                font-weight: bold;
            }

            QLabel#DebuggerSteps {
                color: #9CA3AF;
            }

            QPushButton {
                background-color: #252A34;
                border: 1px solid #353B48;
                border-radius: 6px;
                padding: 7px 11px;
            }

            QPushButton:hover {
                background-color: #343B49;
            }

            QPushButton:disabled {
                color: #64748B;
                background-color: #1C2029;
            }

            QPushButton#DebugStart {
                background-color: #2563EB;
                border: none;
                font-weight: bold;
            }

            QPushButton#DebugStart:hover {
                background-color: #3B82F6;
            }

            QDialog#HistoryDialog {
                background-color: #181B22;
            }

            QListWidget {
                background-color: #111318;
                border: 1px solid #292D36;
                border-radius: 6px;
                padding: 5px;
                outline: none;
            }

            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }

            QListWidget::item:selected {
                background-color: #252A34;
            }
        """)

        self.build_interface()
        self.set_state("idle")

    def build_interface(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(8)

        title = QLabel("DEBUG")
        title.setStyleSheet(
            "color: #60A5FA; font-weight: bold;"
        )

        self.status_label = QLabel("Idle")
        self.status_label.setObjectName("DebuggerStatus")

        self.step_label = QLabel("Steps: 0")
        self.step_label.setObjectName("DebuggerSteps")

        self.start_button = QPushButton("▶ Start")
        self.start_button.setObjectName("DebugStart")

        self.step_button = QPushButton("Next Step →")
        self.stop_button = QPushButton("■ Stop")
        self.reset_button = QPushButton("↻ Reset")
        self.history_button = QPushButton("History")

        self.start_button.clicked.connect(
            self.start_requested.emit
        )

        self.step_button.clicked.connect(
            self.step_requested.emit
        )

        self.stop_button.clicked.connect(
            self.stop_requested.emit
        )

        self.reset_button.clicked.connect(
            self.reset_requested.emit
        )

        self.history_button.clicked.connect(
            self.show_history
        )

        layout.addWidget(title)
        layout.addWidget(self.status_label)
        layout.addWidget(self.step_label)
        layout.addStretch()

        layout.addWidget(self.start_button)
        layout.addWidget(self.step_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.history_button)

        # History dialog is created once and reused.
        self.history_dialog = QDialog(self)
        self.history_dialog.setObjectName("HistoryDialog")
        self.history_dialog.setWindowTitle(
            "LogicFlow - Execution History"
        )
        self.history_dialog.resize(520, 420)

        history_layout = QVBoxLayout(self.history_dialog)

        history_title = QLabel("Execution History")
        history_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.history_list = QListWidget()

        close_button = QPushButton("Close")
        close_button.clicked.connect(
            self.history_dialog.hide
        )

        history_layout.addWidget(history_title)
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(close_button)

    def show_history(self):
        self.history_dialog.show()
        self.history_dialog.raise_()
        self.history_dialog.activateWindow()

    def set_state(self, state, message=None):
        states = {
            "idle": ("Idle", "#9CA3AF"),
            "ready": ("Ready", "#60A5FA"),
            "running": ("Running", "#34D399"),
            "paused": ("Paused", "#FBBF24"),
            "completed": ("Completed", "#34D399"),
            "stopped": ("Stopped", "#9CA3AF"),
            "error": ("Error", "#F87171"),
        }

        label, color = states.get(
            state,
            ("Unknown", "#9CA3AF")
        )

        self.status_label.setText(label)
        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )

        self.start_button.setEnabled(
            state in ("idle", "completed", "stopped", "error")
        )

        self.step_button.setEnabled(
            state in ("ready", "running", "paused")
        )

        self.stop_button.setEnabled(
            state in ("ready", "running", "paused")
        )

        self.reset_button.setEnabled(
            state != "idle"
        )

    def add_history_entry(
        self,
        step_number,
        node_name,
        node_type,
        message,
        error=False
    ):
        if error:
            prefix = "✖"
            color = QColor("#F87171")
        else:
            prefix = "✓"
            color = QColor("#34D399")

        text = (
            f"{prefix} Step {step_number}: "
            f"{node_name} [{node_type}]\n"
            f"   {message}"
        )

        item = QListWidgetItem(text)
        item.setForeground(color)

        self.history_list.addItem(item)
        self.history_list.scrollToBottom()

        self.set_step_count(step_number)

    def set_step_count(self, count):
        self.step_label.setText(
            f"Steps: {count}"
        )

    def clear_history(self):
        self.history_list.clear()
        self.set_step_count(0)

    def set_message(self, message):
        # Kept for compatibility with older code.
        # The explanation is now displayed beneath the active node.
        pass
