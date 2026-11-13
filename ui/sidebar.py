
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup,
)

from ui.branding import create_logo_pixmap


class Sidebar(QFrame):

    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Sidebar")
        self.setFixedWidth(235)
        self.nav_buttons = {}

        self.setStyleSheet("""
            QFrame#Sidebar {
                background-color: #111827;
                border-right: 1px solid #273449;
            }

            QLabel#BrandTitle {
                color: #F8FAFC;
                font-size: 21px;
                font-weight: bold;
            }

            QLabel#BrandSubtitle {
                color: #94A3B8;
                font-size: 10px;
            }

            QLabel#NavHeading {
                color: #64748B;
                font-size: 10px;
                font-weight: bold;
                padding-left: 10px;
            }

            QPushButton#NavButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #94A3B8;
                text-align: left;
                padding: 12px 14px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton#NavButton:hover {
                background-color: #1E293B;
                color: #F8FAFC;
            }

            QPushButton#NavButton:checked {
                background-color: #1D355B;
                color: #60A5FA;
                font-weight: bold;
                border-left: 3px solid #3B82F6;
                padding-left: 11px;
            }

            QPushButton#LogoutButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 8px;
                color: #FCA5A5;
                text-align: left;
                padding: 11px 14px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#LogoutButton:hover {
                background-color: #3B2028;
                border: 1px solid #71343F;
                color: #F87171;
            }

            QLabel#VersionLabel {
                color: #64748B;
                font-size: 10px;
            }

            QFrame#SidebarDivider {
                background-color: #273449;
                border: none;
                max-height: 1px;
            }
        """)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 22, 15, 16)
        layout.setSpacing(8)

        # BRANDING
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(10)

        logo = QLabel()
        logo.setPixmap(
            create_logo_pixmap(64).scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        logo.setFixedSize(48, 48)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(2)

        title = QLabel("LogicFlow")
        title.setObjectName("BrandTitle")

        subtitle = QLabel("VISUAL PROGRAMMING")
        subtitle.setObjectName("BrandSubtitle")

        brand_text.addWidget(title)
        brand_text.addWidget(subtitle)

        brand_layout.addWidget(logo)
        brand_layout.addLayout(brand_text)
        brand_layout.addStretch()

        layout.addLayout(brand_layout)
        layout.addSpacing(30)

        # NAVIGATION HEADING
        navigation_heading = QLabel("WORKSPACE")
        navigation_heading.setObjectName("NavHeading")

        layout.addWidget(navigation_heading)
        layout.addSpacing(5)

        # NAVIGATION BUTTONS
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        navigation_items = [
            ("Dashboard", "⌂  Dashboard"),
            ("Learn", "▤  Learn"),
            ("Logic Editor", "◇  Logic Editor"),
            ("Challenges", "✧  Challenges"),
            ("My Projects", "▣  My Projects"),
        ]

        for key, label in navigation_items:
            button = QPushButton(label)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(44)

            self.button_group.addButton(button)
            self.nav_buttons[key] = button
            layout.addWidget(button)

        self.nav_buttons["Dashboard"].setChecked(True)

        layout.addSpacing(15)

        # DIVIDER
        divider = QFrame()
        divider.setObjectName("SidebarDivider")
        layout.addWidget(divider)

        layout.addStretch()

        # LOGOUT
        self.logout_button = QPushButton("↪  Logout")
        self.logout_button.setObjectName("LogoutButton")
        self.logout_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.logout_button.setMinimumHeight(43)

        self.logout_button.clicked.connect(
            self.logout_requested.emit
        )

        layout.addWidget(self.logout_button)

        layout.addSpacing(12)

        # FOOTER
        footer = QVBoxLayout()
        footer.setSpacing(5)

        footer_title = QLabel("LOGICFLOW DESKTOP")
        footer_title.setObjectName("VersionLabel")

        footer_version = QLabel("Version 1.0")
        footer_version.setObjectName("VersionLabel")

        footer.addWidget(footer_title)
        footer.addWidget(footer_version)

        layout.addLayout(footer)

    def set_active(self, name):
        button = self.nav_buttons.get(name)

        if button is not None:
            button.setChecked(True)
