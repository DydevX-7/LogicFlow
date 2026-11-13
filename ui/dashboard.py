
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QGridLayout,
)


class DashboardPage(QWidget):

    continue_requested = Signal()
    new_project_requested = Signal()
    learn_requested = Signal()
    challenges_requested = Signal()
    projects_requested = Signal()
    open_project_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("DashboardPage")
        self.build_ui()

    def build_ui(self):

        self.setStyleSheet("""
            QWidget#DashboardPage {
                background-color: #10141D;
                color: #E8EDF7;
                font-family: "Segoe UI";
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QWidget#DashboardContent {
                background: transparent;
            }

            QLabel {
                background: transparent;
            }

            QLabel#PageTitle {
                color: #F1F5F9;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#PageSubtitle {
                color: #8491A5;
                font-size: 12px;
            }

            QLabel#SectionTitle {
                color: #E8EDF7;
                font-size: 17px;
                font-weight: 700;
            }

            QLabel#SectionSubtitle {
                color: #8491A5;
                font-size: 11px;
            }

            QFrame#Hero {
                background-color: #17263B;
                border: 1px solid #29466A;
                border-radius: 15px;
            }

            QLabel#HeroEyebrow {
                color: #60A5FA;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#HeroTitle {
                color: #FFFFFF;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#HeroDescription {
                color: #A9BBD2;
                font-size: 12px;
                line-height: 1.5;
            }

            QFrame#StatCard {
                background-color: #191F2B;
                border: 1px solid #293243;
                border-radius: 12px;
            }

            QFrame#StatCard:hover {
                border-color: #3B82F6;
                background-color: #1C2533;
            }

            QLabel#StatLabel {
                color: #91A0B5;
                font-size: 11px;
                font-weight: 600;
            }

            QLabel#StatValue {
                color: #69B4FF;
                font-size: 27px;
                font-weight: 700;
            }

            QLabel#StatAccent {
                color: #53647C;
                font-size: 10px;
            }

            QFrame#ActionCard {
                background-color: #191F2B;
                border: 1px solid #293243;
                border-radius: 12px;
            }

            QFrame#ActionCard:hover {
                border-color: #3B82F6;
                background-color: #1C2533;
            }

            QLabel#ActionTitle {
                color: #EAF1FC;
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#ActionDescription {
                color: #8998AD;
                font-size: 11px;
            }

            QFrame#RecentCard {
                background-color: #191F2B;
                border: 1px solid #293243;
                border-radius: 12px;
            }

            QLabel#Muted {
                color: #8998AD;
                font-size: 11px;
            }

            QPushButton {
                background-color: #242D3B;
                color: #DCE7F7;
                border: 1px solid #344258;
                border-radius: 8px;
                padding: 9px 14px;
                font-size: 11px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #303E53;
                border-color: #60A5FA;
            }

            QPushButton:pressed {
                background-color: #1C2B40;
            }

            QPushButton#Primary {
                background-color: #2878E5;
                color: white;
                border: 1px solid #3989F5;
                padding: 11px 17px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton#Primary:hover {
                background-color: #3989F5;
            }

            QPushButton#Primary:pressed {
                background-color: #1D5FB9;
            }

            QPushButton#ProjectButton {
                background-color: #202938;
                color: #DCE7F7;
                border: 1px solid #303D50;
                border-radius: 8px;
                text-align: left;
                padding: 12px 14px;
                font-size: 12px;
            }

            QPushButton#ProjectButton:hover {
                background-color: #29394F;
                border-color: #3989F5;
            }

            QScrollBar:vertical {
                background: #10141D;
                width: 8px;
                margin: 2px;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #35445B;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #52749D;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        # Main layout
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 18, 18, 18)
        root.setSpacing(0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        content = QWidget()
        content.setObjectName("DashboardContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 10, 16)
        layout.setSpacing(20)

        # --------------------------------------------------
        # PAGE HEADER
        # --------------------------------------------------

        header = QVBoxLayout()
        header.setSpacing(5)

        heading = QLabel("Dashboard")
        heading.setObjectName("PageTitle")

        subtitle = QLabel(
            "Your workspace at a glance. Keep learning, "
            "building, and making progress."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)

        header.addWidget(heading)
        header.addWidget(subtitle)

        layout.addLayout(header)

        # --------------------------------------------------
        # WELCOME HERO
        # --------------------------------------------------

        hero = QFrame()
        hero.setObjectName("Hero")

        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(25, 23, 25, 23)
        hero_layout.setSpacing(12)

        eyebrow = QLabel("YOUR PROGRAMMING WORKSPACE")
        eyebrow.setObjectName("HeroEyebrow")

        welcome = QLabel("Welcome to LogicFlow.")
        welcome.setObjectName("HeroTitle")
        welcome.setWordWrap(True)

        description = QLabel(
            "Turn your ideas into working programs. "
            "Learn programming visually, build flowcharts, "
            "understand logic, and generate Python code."
        )
        description.setObjectName("HeroDescription")
        description.setWordWrap(True)

        hero_buttons = QHBoxLayout()
        hero_buttons.setSpacing(10)

        self.continue_button = QPushButton(
            "Continue Working  →"
        )
        self.continue_button.setObjectName("Primary")
        self.continue_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.new_button = QPushButton("+  New Flowchart")
        self.new_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        hero_buttons.addWidget(self.continue_button)
        hero_buttons.addWidget(self.new_button)
        hero_buttons.addStretch()

        hero_layout.addWidget(eyebrow)
        hero_layout.addWidget(welcome)
        hero_layout.addWidget(description)
        hero_layout.addSpacing(4)
        hero_layout.addLayout(hero_buttons)

        layout.addWidget(hero)

        # --------------------------------------------------
        # PROGRESS STATISTICS
        # --------------------------------------------------

        section_header = QVBoxLayout()
        section_header.setSpacing(4)

        progress_title = QLabel("Your Progress")
        progress_title.setObjectName("SectionTitle")

        progress_subtitle = QLabel(
            "A snapshot of your learning journey."
        )
        progress_subtitle.setObjectName("SectionSubtitle")

        section_header.addWidget(progress_title)
        section_header.addWidget(progress_subtitle)

        layout.addLayout(section_header)

        stats = QGridLayout()
        stats.setSpacing(12)

        self.lesson_value = self.add_stat(
            stats,
            0,
            0,
            "0 / 4",
            "LESSONS COMPLETED",
            "Keep learning"
        )

        self.challenge_value = self.add_stat(
            stats,
            0,
            1,
            "0 / 5",
            "CHALLENGES COMPLETED",
            "Put your skills to work"
        )

        self.project_value = self.add_stat(
            stats,
            0,
            2,
            "0",
            "RECENT PROJECTS",
            "Your saved workspace"
        )

        layout.addLayout(stats)

        # --------------------------------------------------
        # QUICK ACCESS
        # --------------------------------------------------

        quick_header = QVBoxLayout()
        quick_header.setSpacing(4)

        quick_title = QLabel("Quick Access")
        quick_title.setObjectName("SectionTitle")

        quick_subtitle = QLabel(
            "Jump straight into what you want to do."
        )
        quick_subtitle.setObjectName("SectionSubtitle")

        quick_header.addWidget(quick_title)
        quick_header.addWidget(quick_subtitle)

        layout.addLayout(quick_header)

        actions = QGridLayout()
        actions.setSpacing(12)

        self.learn_button = self.add_action(
            actions,
            0,
            0,
            "Learn Programming",
            "Explore variables, conditions, algorithms, "
            "and flowcharts.",
            "01"
        )

        self.challenge_button = self.add_action(
            actions,
            0,
            1,
            "Programming Challenges",
            "Test your understanding with practical "
            "programming problems.",
            "02"
        )

        self.projects_button = self.add_action(
            actions,
            1,
            0,
            "My Projects",
            "Find and continue working on your saved "
            "LogicFlow projects.",
            "03"
        )

        self.editor_button = self.add_action(
            actions,
            1,
            1,
            "Logic Editor",
            "Design flowcharts using visual programming "
            "nodes and connections.",
            "04"
        )

        layout.addLayout(actions)

        # --------------------------------------------------
        # RECENT PROJECTS
        # --------------------------------------------------

        recent_header = QVBoxLayout()
        recent_header.setSpacing(4)

        recent_title = QLabel("Recent Projects")
        recent_title.setObjectName("SectionTitle")

        recent_subtitle = QLabel(
            "Pick up where you left off."
        )
        recent_subtitle.setObjectName("SectionSubtitle")

        recent_header.addWidget(recent_title)
        recent_header.addWidget(recent_subtitle)

        layout.addLayout(recent_header)

        recent_card = QFrame()
        recent_card.setObjectName("RecentCard")

        recent_card_layout = QVBoxLayout(recent_card)
        recent_card_layout.setContentsMargins(
            14, 14, 14, 14
        )
        recent_card_layout.setSpacing(8)

        self.recent_container = QWidget()

        self.recent_layout = QVBoxLayout(
            self.recent_container
        )
        self.recent_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_layout.setSpacing(8)

        recent_card_layout.addWidget(self.recent_container)

        layout.addWidget(recent_card)

        layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

        # --------------------------------------------------
        # SIGNAL CONNECTIONS
        # --------------------------------------------------

        self.continue_button.clicked.connect(
            self.continue_requested.emit
        )

        self.editor_button.clicked.connect(
            self.continue_requested.emit
        )

        self.new_button.clicked.connect(
            self.new_project_requested.emit
        )

        self.learn_button.clicked.connect(
            self.learn_requested.emit
        )

        self.challenge_button.clicked.connect(
            self.challenges_requested.emit
        )

        self.projects_button.clicked.connect(
            self.projects_requested.emit
        )

    # ======================================================
    # STAT CARD
    # ======================================================

    def add_stat(
        self,
        grid,
        row,
        column,
        value,
        label,
        footer
    ):

        card = QFrame()
        card.setObjectName("StatCard")
        card.setMinimumHeight(118)

        box = QVBoxLayout(card)
        box.setContentsMargins(17, 15, 17, 14)
        box.setSpacing(7)

        label_widget = QLabel(label)
        label_widget.setObjectName("StatLabel")
        label_widget.setWordWrap(True)

        value_label = QLabel(value)
        value_label.setObjectName("StatValue")

        footer_label = QLabel(footer)
        footer_label.setObjectName("StatAccent")

        box.addWidget(label_widget)
        box.addWidget(value_label)
        box.addWidget(footer_label)
        box.addStretch()

        grid.addWidget(card, row, column)

        return value_label

    # ======================================================
    # QUICK ACCESS CARD
    # ======================================================

    def add_action(
        self,
        grid,
        row,
        column,
        title,
        description,
        number
    ):

        card = QFrame()
        card.setObjectName("ActionCard")
        card.setMinimumHeight(145)

        box = QVBoxLayout(card)
        box.setContentsMargins(17, 15, 17, 15)
        box.setSpacing(9)

        number_label = QLabel(f"WORKSPACE / {number}")
        number_label.setStyleSheet("""
            color: #529BEF;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        """)

        title_label = QLabel(title)
        title_label.setObjectName("ActionTitle")
        title_label.setWordWrap(True)

        description_label = QLabel(description)
        description_label.setObjectName("ActionDescription")
        description_label.setWordWrap(True)

        button = QPushButton("Open  →")
        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        box.addWidget(number_label)
        box.addWidget(title_label)
        box.addWidget(description_label)
        box.addStretch()
        box.addWidget(button)

        grid.addWidget(card, row, column)

        return button

    # ======================================================
    # REFRESH DASHBOARD DATA
    # ======================================================

    def refresh_data(
        self,
        completed_lessons=0,
        total_lessons=4,
        completed_challenges=0,
        total_challenges=5,
        recent_projects=None
    ):

        recent_projects = recent_projects or []

        # Update statistics
        self.lesson_value.setText(
            f"{completed_lessons} / {total_lessons}"
        )

        self.challenge_value.setText(
            f"{completed_challenges} / {total_challenges}"
        )

        self.project_value.setText(
            str(len(recent_projects))
        )

        # Clear old recent project entries
        while self.recent_layout.count():

            item = self.recent_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        # Empty state
        if not recent_projects:

            empty_label = QLabel(
                "No saved projects yet.\n"
                "Create a flowchart and save it to see "
                "your recent work here."
            )

            empty_label.setObjectName("Muted")
            empty_label.setWordWrap(True)

            empty_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty_label.setMinimumHeight(65)

            self.recent_layout.addWidget(empty_label)

            return

        # Recent project buttons
        for project in recent_projects[:5]:

            project = Path(project)

            button = QPushButton(
                f"  ◈    {project.stem}    →"
            )

            button.setObjectName("ProjectButton")
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )
            button.setToolTip(str(project))

            button.clicked.connect(
                lambda checked=False, path=str(project):
                self.open_project_requested.emit(path)
            )

            self.recent_layout.addWidget(button)
