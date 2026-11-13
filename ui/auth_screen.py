
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)

from ui.branding import create_logo_pixmap


class AuthScreen(QWidget):
    """Clean LogicFlow login and account creation interface."""

    authenticated = Signal(str)

    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager

        self.setWindowTitle("LogicFlow")
        self.setMinimumSize(520, 680)
        self.resize(540, 740)

        self.setStyleSheet("""
            QWidget {
                background-color: #10141D;
                color: #E8EDF7;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QFrame#AuthCard {
                background-color: #191F2B;
                border: 1px solid #293243;
                border-radius: 15px;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLabel#AuthTitle {
                color: #F1F5F9;
                font-size: 25px;
                font-weight: 700;
            }

            QLabel#AuthSubtitle {
                color: #8998AD;
                font-size: 12px;
            }

            QLabel#FieldLabel {
                color: #E8EDF7;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#FieldHint {
                color: #8491A5;
                font-size: 11px;
            }

            QLabel#AuthError {
                color: #F87171;
                font-size: 12px;
                padding: 2px 0;
            }

            QLineEdit {
                background-color: #17263B;
                color: #F1F5F9;
                border: 1px solid #293243;
                border-radius: 8px;
                padding: 11px 13px;
                min-height: 20px;
                selection-background-color: #2878E5;
            }

            QLineEdit:hover {
                border: 1px solid #3B506C;
            }

            QLineEdit:focus {
                border: 1px solid #2878E5;
                background-color: #192B43;
                outline: none;
            }

            QPushButton {
                outline: none;
            }

            QPushButton#PrimaryButton {
                background-color: #2878E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#PrimaryButton:hover {
                background-color: #3688F5;
            }

            QPushButton#PrimaryButton:pressed {
                background-color: #1D62C0;
            }

            QPushButton#PrimaryButton:disabled {
                background-color: #35445B;
                color: #8491A5;
            }

            QPushButton#PrimaryButton:focus {
                border: 1px solid #60A5FA;
            }

            QPushButton#SecondaryButton {
                background-color: transparent;
                color: #60A5FA;
                border: none;
                padding: 8px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#SecondaryButton:hover {
                color: #06B6D4;
            }

            QPushButton#SecondaryButton:focus {
                border: none;
            }

            QCheckBox {
                background: transparent;
                color: #8998AD;
                spacing: 9px;
                font-size: 12px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #475569;
                background-color: #17263B;
            }

            QCheckBox::indicator:checked {
                background-color: #2878E5;
                border: 1px solid #2878E5;
            }

            QCheckBox::indicator:hover {
                border: 1px solid #60A5FA;
            }

            QStackedWidget {
                background: transparent;
                border: none;
            }
        """)

        self.stack = QStackedWidget()
        self.stack.setFixedWidth(430)

        self.login_page = self.build_login_page()
        self.signup_page = self.build_signup_page()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.signup_page)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(self.stack)

        if self.auth_manager.has_accounts():
            self.stack.setCurrentWidget(self.login_page)
        else:
            self.stack.setCurrentWidget(self.signup_page)

    # ==========================================
    # SHARED COMPONENTS
    # ==========================================

    def create_card(self):
        card = QFrame()
        card.setObjectName("AuthCard")
        card.setFrameShape(QFrame.Shape.NoFrame)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 27, 32, 27)
        layout.setSpacing(11)

        return card, layout

    def add_header(self, layout, title, subtitle):
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(create_logo_pixmap(72))
        logo.setFixedHeight(76)

        title_label = QLabel(title)
        title_label.setObjectName("AuthTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("AuthSubtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)

        layout.addWidget(logo)
        layout.addSpacing(2)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(12)

    def add_field_label(self, layout, text):
        label = QLabel(text)
        label.setObjectName("FieldLabel")
        layout.addWidget(label)

    def create_text_field(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setClearButtonEnabled(False)
        field.setMinimumHeight(43)
        field.setMaxLength(128)
        return field

    def create_password_field(self, placeholder):
        field = self.create_text_field(placeholder)
        field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    def create_hint(self, text):
        label = QLabel(text)
        label.setObjectName("FieldHint")
        label.setWordWrap(True)
        return label

    def create_error_label(self):
        label = QLabel("")
        label.setObjectName("AuthError")
        label.setWordWrap(True)
        label.setMinimumHeight(19)
        return label

    def create_primary_button(self, text):
        button = QPushButton(text)
        button.setObjectName("PrimaryButton")
        button.setMinimumHeight(44)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def create_secondary_button(self, text):
        button = QPushButton(text)
        button.setObjectName("SecondaryButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    # ==========================================
    # LOGIN PAGE
    # ==========================================

    def build_login_page(self):
        card, layout = self.create_card()

        self.add_header(
            layout,
            "Welcome Back",
            "Sign in to continue your LogicFlow journey."
        )

        self.add_field_label(layout, "Username")

        self.login_username = self.create_text_field(
            "Enter your username"
        )

        self.login_username.setText(
            self.auth_manager.get_remembered_username()
        )

        layout.addWidget(self.login_username)

        layout.addSpacing(5)

        self.add_field_label(layout, "Password")

        self.login_password = self.create_password_field(
            "Enter your password"
        )

        layout.addWidget(self.login_password)

        layout.addSpacing(4)

        self.remember_checkbox = QCheckBox(
            "Remember my username"
        )

        self.remember_checkbox.setChecked(
            bool(self.auth_manager.get_remembered_username())
        )

        layout.addWidget(self.remember_checkbox)

        self.login_error = self.create_error_label()
        layout.addWidget(self.login_error)

        self.login_button = self.create_primary_button(
            "Log In"
        )

        self.login_button.clicked.connect(
            self.handle_login
        )

        layout.addWidget(self.login_button)

        layout.addSpacing(3)

        create_account_button = self.create_secondary_button(
            "New to LogicFlow?  Create an account"
        )

        create_account_button.clicked.connect(
            self.show_signup_page
        )

        layout.addWidget(create_account_button)

        footer = QLabel(
            "OFFLINE ACCOUNT  •  STORED ON THIS COMPUTER"
        )

        footer.setObjectName("AuthSubtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(8)
        layout.addWidget(footer)

        self.login_username.returnPressed.connect(
            self.login_password.setFocus
        )

        self.login_password.returnPressed.connect(
            self.handle_login
        )

        return card

    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username or not password:
            self.login_error.setText(
                "Please enter your username and password."
            )
            return

        self.login_button.setEnabled(False)
        self.login_error.setText("")

        try:
            success, message = self.auth_manager.authenticate(
                username,
                password
            )

        except Exception as error:
            success = False
            message = f"Login failed: {error}"

        finally:
            self.login_button.setEnabled(True)

        if not success:
            self.login_error.setText(message)
            return

        remembered_username = (
            message
            if self.remember_checkbox.isChecked()
            else ""
        )

        self.auth_manager.set_remembered_username(
            remembered_username
        )

        self.login_password.clear()
        self.authenticated.emit(message)

    # ==========================================
    # SIGNUP PAGE
    # ==========================================

    def build_signup_page(self):
        card, layout = self.create_card()

        self.add_header(
            layout,
            "Create Your Account",
            "Your workspace starts here."
        )

        self.add_field_label(layout, "Username")

        self.signup_username = self.create_text_field(
            "Choose a username"
        )

        self.signup_username.setMaxLength(24)
        layout.addWidget(self.signup_username)

        layout.addWidget(
            self.create_hint(
                "3–24 characters. Letters, numbers, dots, "
                "hyphens and underscores."
            )
        )

        layout.addSpacing(4)

        self.add_field_label(layout, "Password")

        self.signup_password = self.create_password_field(
            "Create a password"
        )

        layout.addWidget(self.signup_password)

        layout.addWidget(
            self.create_hint(
                "Use at least 8 characters."
            )
        )

        layout.addSpacing(4)

        self.add_field_label(layout, "Confirm Password")

        self.confirm_password = self.create_password_field(
            "Enter your password again"
        )

        layout.addWidget(self.confirm_password)

        self.signup_error = self.create_error_label()
        layout.addWidget(self.signup_error)

        self.signup_button = self.create_primary_button(
            "Create Account"
        )

        self.signup_button.clicked.connect(
            self.handle_signup
        )

        layout.addWidget(self.signup_button)

        login_button = self.create_secondary_button(
            "Already have an account?  Log in"
        )

        login_button.clicked.connect(
            self.show_login_page
        )

        layout.addWidget(login_button)

        footer = QLabel(
            "OFFLINE ACCOUNT  •  NO INTERNET REQUIRED"
        )

        footer.setObjectName("AuthSubtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5)
        layout.addWidget(footer)

        self.confirm_password.returnPressed.connect(
            self.handle_signup
        )

        return card

    def handle_signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text()
        confirmation = self.confirm_password.text()

        if not username or not password or not confirmation:
            self.signup_error.setText(
                "Please complete all fields."
            )
            return

        if password != confirmation:
            self.signup_error.setText(
                "Your passwords do not match."
            )
            return

        self.signup_button.setEnabled(False)
        self.signup_error.setText("")

        try:
            success, message = self.auth_manager.create_account(
                username,
                password
            )

        except Exception as error:
            success = False
            message = f"Account creation failed: {error}"

        finally:
            self.signup_button.setEnabled(True)

        if not success:
            self.signup_error.setText(message)
            return

        self.auth_manager.set_remembered_username(username)

        self.signup_password.clear()
        self.confirm_password.clear()

        self.authenticated.emit(username)

    # ==========================================
    # PAGE NAVIGATION
    # ==========================================

    def show_login_page(self):
        self.login_error.setText("")
        self.login_password.clear()

        self.stack.setCurrentWidget(
            self.login_page
        )

        self.login_username.setFocus()

    def show_signup_page(self):
        self.signup_error.setText("")
        self.signup_password.clear()
        self.confirm_password.clear()

        self.stack.setCurrentWidget(
            self.signup_page
        )

        self.signup_username.setFocus()
