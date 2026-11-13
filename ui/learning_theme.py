
from PySide6.QtWidgets import QWidget


def apply_learning_theme(page: QWidget):
    page.setObjectName("LearningPage")

    page.setStyleSheet("""
        QWidget#LearningPage {
            background-color: #111318;
            color: #E5E7EB;
            font-family: "Segoe UI";
            font-size: 13px;
        }

        QLabel {
            color: #E5E7EB;
            background: transparent;
        }

        QLabel#Muted {
            color: #9CA3AF;
        }

        QScrollArea {
            background: transparent;
            border: none;
        }

        QScrollArea > QWidget > QWidget {
            background: transparent;
        }

        QFrame#Panel {
            background-color: #191E28;
            border: 1px solid #2B3443;
            border-radius: 12px;
        }

        QPushButton {
            background-color: #202735;
            color: #DCE7F5;
            border: 1px solid #344256;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 12px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #29384D;
            border: 1px solid #60A5FA;
            color: white;
        }

        QPushButton:pressed {
            background-color: #172B46;
        }

        QPushButton:disabled {
            background-color: #1A1E25;
            color: #626B79;
            border-color: #292D36;
        }

        QPushButton#RunButton {
            background-color: #2563EB;
            color: white;
            border: 1px solid #3B82F6;
            border-radius: 9px;
            padding: 12px 18px;
            font-weight: bold;
        }

        QPushButton#RunButton:hover {
            background-color: #3478F6;
            border-color: #60A5FA;
        }

        QPushButton#RunButton:pressed {
            background-color: #1D4ED8;
        }

        QProgressBar {
            background-color: #252C38;
            border: none;
            border-radius: 5px;
            min-height: 9px;
            max-height: 9px;
        }

        QProgressBar::chunk {
            background-color: #3B82F6;
            border-radius: 5px;
        }

        QRadioButton {
            color: #DCE7F5;
            background-color: #191E28;
            border: 1px solid #303B4C;
            border-radius: 9px;
            padding: 13px;
            spacing: 10px;
        }

        QRadioButton:hover {
            background-color: #222D3D;
            border-color: #60A5FA;
        }

        QRadioButton:checked {
            background-color: #1D2D45;
            border: 1px solid #60A5FA;
            color: white;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
        }

        QRadioButton::indicator:unchecked {
            border: 2px solid #64748B;
            border-radius: 8px;
            background: #111827;
        }

        QRadioButton::indicator:checked {
            border: 2px solid #60A5FA;
            border-radius: 8px;
            background: #3B82F6;
        }

        QScrollBar:vertical {
            background: #111318;
            width: 9px;
            margin: 2px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical {
            background: #39465A;
            min-height: 30px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical:hover {
            background: #60A5FA;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            height: 0px;
        }
    """)
