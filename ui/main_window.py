from PySide6.QtGui import QKeySequence, QShortcut
from ui.dashboard import DashboardPage
from ui.sidebar import Sidebar

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QComboBox,
    QScrollArea, QSplitter, QFileDialog, QSizePolicy, QInputDialog,
    QTextEdit, QListWidget, QListWidgetItem, QStackedWidget,
    QMessageBox,
)
from storage.project_manager import ProjectManager
from storage.learning_progress import LearningProgressManager
from PySide6.QtCore import Qt, QEvent, QPoint, Signal
from PySide6.QtGui import QColor, QPen

from ui.editor import NodeItem
from ui.debugger import DebuggerPanel
from ui.learning import LearningPage, LESSONS
from ui.python_workspace import PythonWorkspace
from engine.challenge_validator import ChallengeValidator


class MainWindow(QMainWindow):

    logout_requested = Signal()

    def __init__(self,username=None):
        super().__init__()
        self.username= username

        self.setWindowTitle("LogicFlow")
        self.resize(1450, 900)
        self.setMinimumSize(1100, 700)

        self.current_node = None
        self.property_fields = {}

        self.execution_engine = None
        self.execution_outputs = []
        self.execution_success = False

        self.highlighted_node = None
        self.original_node_pens = {}

        self.active_variable_field = None
        self.autocomplete_fields = set()
        self.variable_popup = None
        self.updating_popup = False

        self.username = username

        self.completed_challenges = set()
        self.challenge_xp = 0

        self.project_manager = ProjectManager(username=username)

        self.learning_progress_manager = LearningProgressManager(
            username=username
        )

        self.current_project_path = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #111318;
            }

            QWidget {
                color: #E5E7EB;
                font-family: Segoe UI;
                font-size: 13px;
            }

            QFrame#Sidebar {
                background-color: #181B22;
                border-right: 1px solid #292D36;
            }

            QFrame#Toolbar {
                background-color: #181B22;
                border: 1px solid #292D36;
                border-radius: 8px;
            }

            QLabel#Brand {
                color: #60A5FA;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#Muted {
                color: #9CA3AF;
            }

            QLabel#SectionTitle {
                font-size: 15px;
                font-weight: bold;
                color: #F3F4F6;
            }

            QLabel#FieldLabel {
                color: #D1D5DB;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton {
                background-color: #252A34;
                border: 1px solid #353B48;
                border-radius: 6px;
                padding: 9px 12px;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #343B49;
            }

            QPushButton:disabled {
                color: #64748B;
                background-color: #1C2029;
            }

            QPushButton#RunButton {
                background-color: #2563EB;
                border: none;
                font-weight: bold;
            }

            QPushButton#RunButton:hover {
                background-color: #3B82F6;
            }

            QPushButton#PythonButton {
                background-color: #174B3A;
                border: 1px solid #237653;
                font-weight: bold;
            }

            QPushButton#PythonButton:hover {
                background-color: #20664E;
            }

            QFrame#Panel {
                background-color: #181B22;
                border: 1px solid #292D36;
                border-radius: 8px;
            }

            QLineEdit, QComboBox, QTextEdit {
                background-color: #252A34;
                border: 1px solid #353B48;
                border-radius: 6px;
                padding: 8px;
                color: #E5E7EB;
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #60A5FA;
            }

            QComboBox QAbstractItemView {
                background-color: #252A34;
                selection-background-color: #2563EB;
                padding: 5px;
            }

            QListWidget#VariablePopup {
                background-color: #202631;
                border: 1px solid #60A5FA;
                border-radius: 6px;
                color: #E5E7EB;
                padding: 4px;
                outline: none;
            }

            QListWidget#VariablePopup::item {
                padding: 8px;
                border-radius: 4px;
            }

            QListWidget#VariablePopup::item:selected {
                background-color: #2563EB;
                color: white;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #181B22;
                width: 9px;
                margin: 2px;
            }

            QScrollBar::handle:vertical {
                background: #454D5C;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #64748B;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QSplitter::handle {
                background-color: #343B49;
                width: 5px;
                height: 5px;
            }

            QSplitter::handle:hover {
                background-color: #60A5FA;
            }
        """)

        self.build_interface()
        self.create_variable_popup()

    # ==================================
    # MAIN INTERFACE
    # ==================================

    
    def build_interface(self):

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==================================
        # SIDEBAR
        # ==================================

        self.sidebar = Sidebar()
        self.sidebar.logout_requested.connect(
            self.request_logout
        )

        sidebar = self.sidebar
        self.nav_buttons = self.sidebar.nav_buttons

        # ==================================
        # MAIN CONTENT
        # ==================================

        content = QWidget()

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(10)

        # ==================================
        # TOOLBAR
        # ==================================

        toolbar = QFrame()
        toolbar.setObjectName("Toolbar")
        toolbar.setMaximumHeight(75)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 12, 16, 12)

        heading = QLabel("Logic Editor")
        heading.setStyleSheet(
            "font-size: 19px; font-weight: bold;"
        )

        self.python_code_button = QPushButton("Python Code")
        self.python_code_button.setObjectName("PythonButton")
        self.python_code_button.setToolTip(
            "Convert your visual flowchart into readable Python code"
        )

        self.debugger_button = QPushButton("🐛 Debugger")
        self.debugger_button.setToolTip(
            "Show or hide the debugging controls"
        )

        self.run_button = QPushButton("▶ Run Program")
        self.run_button.setObjectName("RunButton")

        self.save_button = QPushButton("💾 Save")
        self.save_button.setToolTip(
            "Save your current flowchart"
        )

        self.load_button = QPushButton("📂 Load")
        self.load_button.setToolTip(
            "Open a saved LogicFlow project"
        )

        self.undo_button = QPushButton("↶ Undo")
        self.undo_button.setToolTip("Undo last change (Ctrl+Z)")
        self.undo_button.setEnabled(False)

        self.redo_button = QPushButton("↷ Redo")
        self.redo_button.setToolTip("Redo last undone change (Ctrl+Y)")
        self.redo_button.setEnabled(False)

        toolbar_layout.addWidget(heading)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.undo_button)
        toolbar_layout.addWidget(self.redo_button)
        toolbar_layout.addWidget(self.save_button)
        toolbar_layout.addWidget(self.load_button)
        toolbar_layout.addWidget(self.python_code_button)
        toolbar_layout.addWidget(self.debugger_button)
        toolbar_layout.addWidget(self.run_button)

        # ==================================
        # DEBUGGER
        # ==================================

        self.debugger_panel = DebuggerPanel()
        self.debugger_panel.setVisible(False)

        # ==================================
        # EDITOR WORKSPACE
        # ==================================

        self.workspace_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.workspace_splitter.setChildrenCollapsible(False)
        self.workspace_splitter.setHandleWidth(5)
        self.workspace_splitter.setMinimumHeight(350)

        self.canvas = self.create_node_editor()
        self.canvas.setMinimumWidth(300)
        self.canvas.setMinimumHeight(350)

        # Undo / Redo

        self.undo_button.clicked.connect(
            self.canvas.undo_stack.undo
        )

        self.redo_button.clicked.connect(
            self.canvas.undo_stack.redo
        )

        self.canvas.undo_stack.canUndoChanged.connect(
            self.undo_button.setEnabled
        )

        self.canvas.undo_stack.canRedoChanged.connect(
            self.redo_button.setEnabled
        )

        self.undo_shortcut = QShortcut(
            QKeySequence("Ctrl+Z"),
            self.canvas.view
        )

        self.undo_shortcut.setContext(
            Qt.ShortcutContext.WidgetWithChildrenShortcut
        )

        self.undo_shortcut.activated.connect(
            self.canvas.undo_stack.undo
        )

        self.redo_shortcut = QShortcut(
            QKeySequence("Ctrl+Y"),
            self.canvas.view
        )

        self.redo_shortcut.setContext(
            Qt.ShortcutContext.WidgetWithChildrenShortcut
        )

        self.redo_shortcut.activated.connect(
            self.canvas.undo_stack.redo
        )

        # Inspector

        self.inspector = self.create_inspector()
        self.inspector.setMinimumWidth(220)
        self.inspector.setMaximumWidth(500)

        self.workspace_splitter.addWidget(self.canvas)
        self.workspace_splitter.addWidget(self.inspector)

        self.workspace_splitter.setStretchFactor(0, 1)
        self.workspace_splitter.setStretchFactor(1, 0)
        self.workspace_splitter.setSizes([900, 360])

        # Python workspace

        self.python_workspace = PythonWorkspace(self.canvas)

        self.editor_mode_stack = QStackedWidget()

        self.editor_mode_stack.addWidget(
            self.workspace_splitter
        )

        self.editor_mode_stack.addWidget(
            self.python_workspace
        )

        self.editor_mode_stack.setCurrentWidget(
            self.workspace_splitter
        )

        
        # ==================================
        # OUTPUT CONSOLE
        # ==================================

        console = QFrame()
        console.setObjectName("Panel")
        console.setMinimumHeight(190)
        console.setMaximumHeight(260)

        console_layout = QVBoxLayout(console)
        console_layout.setContentsMargins(18, 14, 18, 14)
        console_layout.setSpacing(9)

        console_title = QLabel("OUTPUT CONSOLE")
        console_title.setObjectName("SectionTitle")
        console_title.setStyleSheet("""
            QLabel {
                color: #60A5FA;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.console_message = QLabel(
            "Welcome to LogicFlow. Select a node to configure it."
        )
        self.console_message.setObjectName("Muted")
        self.console_message.setWordWrap(True)
        self.console_message.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.console_message.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 13px;
                padding: 5px 2px;
            }
        """)

        self.explanation_message = QLabel(
            "Execution explanations will appear beneath active nodes."
        )
        self.explanation_message.setObjectName("Muted")
        self.explanation_message.setWordWrap(True)
        self.explanation_message.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.memory_message = QLabel(
            "Variables: No information stored yet."
        )
        self.memory_message.setObjectName("Muted")
        self.memory_message.setWordWrap(True)
        self.memory_message.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        console_layout.addWidget(console_title)
        console_layout.addWidget(self.console_message, 2)
        console_layout.addWidget(self.explanation_message)
        console_layout.addWidget(self.memory_message)

        content_layout.addWidget(toolbar)
        content_layout.addWidget(self.debugger_panel)
        content_layout.addWidget(self.editor_mode_stack, 1)
        content_layout.addWidget(console, 0)


        # ==================================
        # EDITOR AND LEARNING PAGES
        # ==================================

        self.editor_page = content
        self.learning_page = LearningPage()

        # Restore previously saved learning progress.
        saved_progress = self.learning_progress_manager.load_progress(
            lesson_count=len(LESSONS),
            challenge_count=5
        )

        self.learning_page.completed_lessons = set(
            saved_progress["completed_lessons"]
        )

        self.completed_challenges = set(
            saved_progress["completed_challenges"]
        )

        self.challenge_xp = saved_progress["challenge_xp"]

        self.learning_page.refresh_roadmap()

        self.lesson_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.lesson_splitter.setChildrenCollapsible(False)
        self.lesson_splitter.setHandleWidth(5)

        self.lesson_splitter.addWidget(
            self.learning_page.lesson_panel
        )

        self.lesson_splitter.addWidget(
            self.editor_page
        )

        self.lesson_splitter.setStretchFactor(0, 1)
        self.lesson_splitter.setStretchFactor(1, 1)
        self.lesson_splitter.setSizes([600, 600])

        self.lesson_workspace_page = QWidget()

        lesson_workspace_layout = QVBoxLayout(
            self.lesson_workspace_page
        )

        lesson_workspace_layout.setContentsMargins(8, 8, 8, 8)
        lesson_workspace_layout.setSpacing(0)

        lesson_workspace_layout.addWidget(
            self.lesson_splitter
        )

        # ==================================
        # PAGE STACK
        # ==================================

        self.page_stack = QStackedWidget()

        # Create Dashboard only after page stack exists.
        self.dashboard_page = DashboardPage()

        self.page_stack.addWidget(self.dashboard_page)
        self.page_stack.addWidget(self.editor_page)
        self.page_stack.addWidget(self.learning_page)
        self.page_stack.addWidget(self.lesson_workspace_page)

        self.page_stack.addWidget(
            self.learning_page.challenge_page
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.page_stack, 1)

        # ==================================
        # DASHBOARD SIGNALS
        # ==================================

        self.dashboard_page.continue_requested.connect(
            self.show_editor_page
        )

        self.dashboard_page.new_project_requested.connect(
            self.new_project
        )

        self.dashboard_page.learn_requested.connect(
            self.show_learning_page
        )

        self.dashboard_page.challenges_requested.connect(
            self.show_challenges_page
        )

        self.dashboard_page.projects_requested.connect(
            self.load_project
        )

        self.dashboard_page.open_project_requested.connect(
            self.open_project_file
        )

        # ==================================
        # EDITOR SIGNALS
        # ==================================

        self.canvas.node_selected.connect(
            self.show_node_properties
        )

        self.run_button.clicked.connect(
            self.run_program
        )

        self.save_button.clicked.connect(
            self.save_project
        )

        self.load_button.clicked.connect(
            self.load_project
        )

        # ==================================
        # SIDEBAR NAVIGATION
        # ==================================

        self.nav_buttons["Dashboard"].setEnabled(True)
        self.nav_buttons["Dashboard"].setToolTip(
            "Open your LogicFlow dashboard"
        )
        self.nav_buttons["Dashboard"].clicked.connect(
            self.show_dashboard_page
        )

        self.nav_buttons["My Projects"].setEnabled(True)
        self.nav_buttons["My Projects"].setToolTip(
            "Open a saved LogicFlow project"
        )

        self.nav_buttons["My Projects"].clicked.connect(
            self.load_project
        )

        self.nav_buttons["Learn"].clicked.connect(
            self.show_learning_page
        )

        self.nav_buttons["Logic Editor"].clicked.connect(
            self.show_editor_page
        )

        self.nav_buttons["Challenges"].clicked.connect(
            self.show_challenges_page
        )

        # ==================================
        # TOOLBAR SIGNALS
        # ==================================

        self.debugger_button.clicked.connect(
            self.toggle_debugger
        )

        self.python_code_button.clicked.connect(
            self.show_python_workspace
        )

        self.python_workspace.back_requested.connect(
            self.show_flowchart_workspace
        )

        # ==================================
        # DEBUGGER SIGNALS
        # ==================================

        self.debugger_panel.start_requested.connect(
            self.start_execution
        )

        self.debugger_panel.step_requested.connect(
            self.execute_next_step
        )

        self.debugger_panel.stop_requested.connect(
            self.stop_execution
        )

        self.debugger_panel.reset_requested.connect(
            self.reset_execution
        )

        # ==================================
        # LEARNING SIGNALS
        # ==================================

        self.learning_page.lesson_selected.connect(
            self.open_lesson_workspace
        )

        self.learning_page.lesson_completed.connect(
            self.on_lesson_completed
        )

        self.learning_page.open_editor.connect(
            self.return_to_learning_roadmap
        )

        self.learning_page.challenge_editor_requested.connect(
            self.show_editor_page
        )

        # ==================================
        # INITIAL DASHBOARD
        # ==================================

        self.refresh_dashboard()

        self.page_stack.setCurrentWidget(
            self.dashboard_page
        )

    # ==================================
# PYTHON WORKSPACE NAVIGATION
# ==================================

    def show_python_workspace(self):

        self.editor_mode_stack.setCurrentWidget(
            self.python_workspace
        )

        self.python_workspace.refresh_code()


    def show_flowchart_workspace(self):

        self.editor_mode_stack.setCurrentWidget(
            self.workspace_splitter
        )
    

    # ==================================
    # PAGE NAVIGATION
    # ==================================

    def show_editor_page(self):

        self.sidebar.set_active("Logic Editor")

        if self.page_stack.indexOf(self.editor_page) == -1:
            self.page_stack.addWidget(self.editor_page)

        self.page_stack.setCurrentWidget(self.editor_page)

    def show_learning_page(self):

        self.sidebar.set_active("Learn")    
        self.page_stack.setCurrentWidget(
            self.learning_page
        )

        self.learning_page.refresh_roadmap()

    def show_challenges_page(self):

        self.sidebar.set_active("Challenges")
        self.page_stack.setCurrentWidget(
            self.learning_page.challenge_page
        )

        if self.learning_page.active_challenge is not None:
            self.learning_page.challenge_page.setCurrentIndex(1)

    def open_lesson_workspace(self, lesson_index):

        self.sidebar.set_active("Learn")
        self.learning_page.start_lesson(lesson_index)

        self.lesson_splitter.addWidget(
            self.editor_page
        )

        self.lesson_splitter.setSizes([600, 600])

        self.page_stack.setCurrentWidget(
            self.lesson_workspace_page
        )

    def save_learning_progress(self):

        try:
            self.learning_progress_manager.save_progress(
                completed_lessons=self.learning_page.completed_lessons,
                completed_challenges=self.completed_challenges,
                challenge_xp=self.challenge_xp
            )

            return True

        except Exception as error:
            self.console_message.setText(
                f"Could not save learning progress: {error}"
            )

            return False

    def request_logout(self):

        answer = QMessageBox.question(
            self,
            "Log Out",
            (
                f"Log out of {self.username}?\n\n"
                "Your learning progress will be saved. "
                "Make sure your current flowchart is saved "
                "before continuing."
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        if not self.save_learning_progress():

            QMessageBox.warning(
                self,
                "Could Not Log Out",
                (
                    "Your learning progress could not be saved.\n\n"
                    "Please resolve the problem before logging out."
                )
            )

            return

        self.reset_execution()
        self.hide()

        self.logout_requested.emit()


    def on_lesson_completed(self, lesson_index):

        self.save_learning_progress()
        self.refresh_dashboard()
        self.return_to_learning_roadmap()

    def return_to_learning_roadmap(self):

        self.sidebar.set_active("Learn")
        if self.editor_page.parentWidget() is not self.page_stack:
            self.page_stack.addWidget(self.editor_page)

        self.learning_page.refresh_roadmap()

        self.page_stack.setCurrentWidget(
            self.learning_page
        )

        # ==================================
    # DASHBOARD
    # ==================================

    def show_dashboard_page(self):
        self.sidebar.set_active("Dashboard")
        self.refresh_dashboard()

        self.page_stack.setCurrentWidget(
            self.dashboard_page
        )

    def refresh_dashboard(self):

        from pathlib import Path

        projects_directory = Path(
            self.project_manager.projects_directory
        )

        projects_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        recent_projects = sorted(
            projects_directory.glob("*.logicflow"),
            key=lambda path: path.stat().st_mtime,
            reverse=True
        )

        completed_lessons = len(
            self.learning_page.completed_lessons
        )

        total_lessons = len(
            self.learning_page.lessons
        ) if hasattr(self.learning_page, "lessons") else 4

        self.dashboard_page.refresh_data(
            completed_lessons=completed_lessons,
            total_lessons=total_lessons,
            completed_challenges=len(
                self.completed_challenges
            ),
            total_challenges=5,
            recent_projects=recent_projects
        )

    # ==================================
    # NEW PROJECT
    # ==================================

    def new_project(self):

        answer = QMessageBox.question(
            self,
            "New Flowchart",
            (
                "Create a new flowchart?\n\n"
                "Unsaved changes in your current project "
                "will be lost."
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.reset_execution()

        self.canvas.scene.clear()
        self.canvas.scene.connections.clear()

        self.canvas.node_counter = 0
        self.canvas.reset_history()

        self.current_project_path = None

        self.setWindowTitle("LogicFlow - New Project")

        self.show_node_properties(None)

        self.console_message.setText(
            "New flowchart created. Start building your program!"
        )

        self.explanation_message.setText(
            "Add a Start node to begin."
        )

        self.show_editor_page()

    # ==================================
    # OPEN RECENT PROJECT
    # ==================================

    def open_project_file(self, file_path):

        from pathlib import Path

        file_path = Path(file_path)

        if not file_path.exists():
            QMessageBox.warning(
                self,
                "Project Not Found",
                "This project could not be found."
            )
            self.refresh_dashboard()
            return

        try:

            self.reset_execution()

            self.project_manager.load_project(
                str(file_path),
                self.canvas.scene,
                self.canvas
            )

            self.canvas.reset_history()

            self.current_project_path = str(file_path)

            self.setWindowTitle(
                f"LogicFlow - {file_path.stem}"
            )

            self.show_node_properties(None)

            self.console_message.setText(
                f"Project loaded successfully: {file_path.name}"
            )

            self.explanation_message.setText(
                "Project loaded. Your flowchart is ready."
            )

            self.show_editor_page()

            self.refresh_dashboard()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Load Failed",
                f"Could not load the project:\n{error}"
            )
    # ==================================
    # DEBUGGER VISIBILITY
    # ==================================

    def toggle_debugger(self):

        visible = not self.debugger_panel.isVisible()

        self.debugger_panel.setVisible(visible)

        self.debugger_button.setText(
            "🐛 Hide Debugger" if visible else "🐛 Debugger"
        )

    # ==================================
    # CREATE NODE EDITOR
    # ==================================

    def create_node_editor(self):

        from ui.editor import NodeEditor
        return NodeEditor()

    # ==================================
    # CREATE NODE INSPECTOR
    # ==================================

    def create_inspector(self):

        panel = QFrame()
        panel.setObjectName("Panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 17, 16, 12)
        panel_layout.setSpacing(12)

        title = QLabel("Node Inspector")
        title.setObjectName("SectionTitle")

        self.node_description = QLabel(
            "Select a node to configure what it does."
        )

        self.node_description.setObjectName("Muted")
        self.node_description.setWordWrap(True)
        self.node_description.setMinimumHeight(45)
        self.node_description.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.inspector_scroll = QScrollArea()
        self.inspector_scroll.setWidgetResizable(True)

        self.inspector_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.inspector_content = QWidget()
        self.inspector_content.setMinimumWidth(0)

        self.inspector_content.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.inspector_fields_layout = QVBoxLayout(
            self.inspector_content
        )

        self.inspector_fields_layout.setContentsMargins(
            2, 8, 8, 12
        )

        self.inspector_fields_layout.setSpacing(18)
        self.inspector_fields_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.inspector_scroll.setWidget(
            self.inspector_content
        )

        panel_layout.addWidget(title)
        panel_layout.addWidget(self.node_description)
        panel_layout.addWidget(self.inspector_scroll, 1)

        return panel

    # ==================================
    # VARIABLE POPUP
    # ==================================

    def create_variable_popup(self):

        popup = QListWidget(self)
        popup.setObjectName("VariablePopup")

        popup.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
        )

        popup.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        popup.setMouseTracking(True)
        popup.setMinimumWidth(190)
        popup.setMaximumHeight(180)

        self.variable_popup = popup

        popup.itemClicked.connect(
            self.select_variable_suggestion
        )

    def hide_variable_popup(self):

        if self.variable_popup is not None:
            self.variable_popup.hide()

    # ==================================
    # CLEAR NODE PROPERTIES
    # ==================================

    def clear_properties(self):

        self.hide_variable_popup()

        for field in list(self.autocomplete_fields):
            field.removeEventFilter(self)

        self.autocomplete_fields.clear()
        self.active_variable_field = None

        while self.inspector_fields_layout.count():

            item = self.inspector_fields_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.property_fields.clear()

    # ==================================
    # ADD FIELD
    # ==================================

    def add_field(
        self,
        key,
        label,
        value,
        hint=None,
        autocomplete=False
    ):

        container = QWidget()
        container.setMinimumWidth(0)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        field_label = QLabel(label)
        field_label.setObjectName("FieldLabel")
        field_label.setWordWrap(True)

        layout.addWidget(field_label)

        field = QLineEdit(str(value))
        field.setMinimumHeight(43)

        field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        field.textChanged.connect(
            lambda text, k=key: self.save_property(k, text)
        )

        field.editingFinished.connect(
            lambda k=key, f=field: self.save_text_property(k, f)
        )

        if autocomplete:
            self.enable_variable_autocomplete(field)

        layout.addWidget(field)

        if hint:
            hint_label = QLabel(hint)
            hint_label.setObjectName("Muted")
            hint_label.setWordWrap(True)
            layout.addWidget(hint_label)

        self.inspector_fields_layout.addWidget(container)
        self.property_fields[key] = field

        return field

    # ==================================
    # ADD DROPDOWN
    # ==================================

    def add_dropdown(
        self,
        key,
        label,
        options,
        value,
        hint=None
    ):

        container = QWidget()
        container.setMinimumWidth(0)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        field_label = QLabel(label)
        field_label.setObjectName("FieldLabel")
        field_label.setWordWrap(True)

        layout.addWidget(field_label)

        field = QComboBox()
        field.setMinimumHeight(43)
        field.addItems(options)
        field.setCurrentText(value)

        field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        field.currentTextChanged.connect(
            lambda new_value, k=key:
            self.save_property(k, new_value)
        )

        layout.addWidget(field)

        if hint:
            hint_label = QLabel(hint)
            hint_label.setObjectName("Muted")
            hint_label.setWordWrap(True)
            layout.addWidget(hint_label)

        self.inspector_fields_layout.addWidget(container)
        self.property_fields[key] = field

        return field

    # ==================================
    # SAVE SETTINGS
    # ==================================

    def save_text_property(self, key, field):

        if self.current_node is None:
            return

        self.save_property(key, field.text())

    def save_property(self, key, value):

        if self.current_node is None:
            return

        node = self.current_node

        if key == "node_name":

            new_name = str(value).strip()

            if not new_name:
                return

            if new_name == node.node_name:
                return

            node.node_name = new_name
            node.title.setPlainText(new_name)

            self.canvas.record_history(
                "Rename node",
                merge_key=f"rename:{node.node_id}"
            )

            return

        if node.settings.get(key) == value:
            return

        node.settings[key] = value

        self.canvas.record_history(
            f"Change {key.replace('_', ' ')}",
            merge_key=f"setting:{node.node_id}:{key}"
        )

        if key in (
            "operation",
            "first_variable",
            "second_variable",
            "result_variable"
        ):
            self.update_operation_preview()

    # ==================================
    # AVAILABLE VARIABLES
    # ==================================

    def get_available_variables(self):

        variables = []
        seen = set()

        for item in self.canvas.scene.items():

            if not isinstance(item, NodeItem):
                continue

            settings = item.settings

            if item.node_type == "INPUT":

                variable = str(
                    settings.get("variable", "")
                ).strip()

                if (
                    variable.startswith("{")
                    and variable.endswith("}")
                ):
                    variable = variable[1:-1].strip()

                if variable and variable not in seen:
                    variables.append(variable)
                    seen.add(variable)

            elif item.node_type == "OPERATION":

                variable = str(
                    settings.get("result_variable", "")
                ).strip()

                if variable and variable not in seen:
                    variables.append(variable)
                    seen.add(variable)

                legacy_variable = str(
                    settings.get("variable", "")
                ).strip()

                if (
                    legacy_variable
                    and legacy_variable not in seen
                    and not variable
                ):
                    variables.append(legacy_variable)
                    seen.add(legacy_variable)

        return variables

    # ==================================
    # AUTOCOMPLETE
    # ==================================

    def enable_variable_autocomplete(self, field):

        self.autocomplete_fields.add(field)
        field.installEventFilter(self)

        if isinstance(field, QLineEdit):

            field.textChanged.connect(
                self.update_variable_suggestions
            )

            field.cursorPositionChanged.connect(
                self.update_variable_suggestions
            )

        elif isinstance(field, QTextEdit):

            field.textChanged.connect(
                self.update_variable_suggestions
            )

            field.cursorPositionChanged.connect(
                self.update_variable_suggestions
            )

    def get_active_field_text(self):

        field = self.active_variable_field

        if isinstance(field, QLineEdit):
            return field.text()

        if isinstance(field, QTextEdit):
            return field.toPlainText()

        return ""

    def get_active_cursor_position(self):

        field = self.active_variable_field

        if isinstance(field, QLineEdit):
            return field.cursorPosition()

        if isinstance(field, QTextEdit):
            return field.textCursor().position()

        return 0

    def get_variable_context(self):

        field = self.active_variable_field

        if field is None:
            return None

        text = self.get_active_field_text()
        cursor_position = self.get_active_cursor_position()

        opening = text.rfind("{", 0, cursor_position)

        if opening == -1:
            return None

        closing = text.find("}", opening + 1)
        has_closing = closing != -1

        if not has_closing:
            closing = len(text)

        if not (opening < cursor_position <= closing):
            return None

        prefix = text[opening + 1:cursor_position]

        if "{" in prefix or "}" in prefix:
            return None

        return {
            "opening": opening,
            "closing": closing,
            "cursor": cursor_position,
            "prefix": prefix,
            "has_closing": has_closing,
        }

    def update_variable_suggestions(self, *_):

        if self.updating_popup:
            return

        field = self.active_variable_field

        if field is None:
            self.hide_variable_popup()
            return

        context = self.get_variable_context()

        if context is None:
            self.hide_variable_popup()
            return

        prefix = context["prefix"].strip().lower()
        variables = self.get_available_variables()

        matches = [
            variable
            for variable in variables
            if variable.lower().startswith(prefix)
        ]

        if not matches:
            self.hide_variable_popup()
            return

        popup = self.variable_popup
        popup.clear()

        for variable in matches:
            popup.addItem(QListWidgetItem(variable))

        popup.setCurrentRow(0)

        if isinstance(field, QLineEdit):
            cursor_rectangle = field.cursorRect()

        elif isinstance(field, QTextEdit):
            cursor_rectangle = field.cursorRect()

        else:
            return

        global_position = field.mapToGlobal(
            QPoint(
                cursor_rectangle.left(),
                cursor_rectangle.bottom() + 4
            )
        )

        popup_height = min(
            180,
            max(45, len(matches) * 34 + 8)
        )

        popup.resize(210, popup_height)
        popup.move(global_position)
        popup.show()

    def select_variable_suggestion(self, item=None):

        field = self.active_variable_field

        if field is None:
            return

        if item is None:
            item = self.variable_popup.currentItem()

        if item is None:
            return

        variable = item.text()
        context = self.get_variable_context()

        if context is None:
            self.hide_variable_popup()
            return

        opening = context["opening"]
        closing = context["closing"]

        replace_end = (
            closing + 1
            if context["has_closing"]
            else closing
        )

        reference = "{" + variable + "}"

        self.updating_popup = True

        try:

            if isinstance(field, QLineEdit):

                text = field.text()

                new_text = (
                    text[:opening]
                    + reference
                    + text[replace_end:]
                )

                field.setText(new_text)
                field.setCursorPosition(
                    opening + len(reference)
                )

            elif isinstance(field, QTextEdit):

                text = field.toPlainText()

                new_text = (
                    text[:opening]
                    + reference
                    + text[replace_end:]
                )

                field.setPlainText(new_text)

                cursor = field.textCursor()
                cursor.setPosition(
                    opening + len(reference)
                )

                field.setTextCursor(cursor)

        finally:
            self.updating_popup = False

        self.hide_variable_popup()
        field.setFocus()

    # ==================================
    # KEYBOARD EVENT FILTER
    # ==================================

    def eventFilter(self, watched, event):

        if watched in self.autocomplete_fields:

            if event.type() == QEvent.Type.FocusIn:

                self.active_variable_field = watched
                self.hide_variable_popup()
                return False

            if event.type() == QEvent.Type.FocusOut:

                self.hide_variable_popup()
                return False

            if event.type() == QEvent.Type.KeyPress:

                key = event.key()
                popup = self.variable_popup

                popup_visible = (
                    popup is not None
                    and popup.isVisible()
                    and popup.count() > 0
                )

                if popup_visible and key in (
                    Qt.Key.Key_Up,
                    Qt.Key.Key_Down
                ):

                    current_row = popup.currentRow()

                    if key == Qt.Key.Key_Down:
                        current_row = min(
                            current_row + 1,
                            popup.count() - 1
                        )
                    else:
                        current_row = max(
                            current_row - 1,
                            0
                        )

                    popup.setCurrentRow(current_row)
                    return True

                if popup_visible and key in (
                    Qt.Key.Key_Return,
                    Qt.Key.Key_Enter,
                    Qt.Key.Key_Tab
                ):

                    self.select_variable_suggestion()
                    return True

                if (
                    key == Qt.Key.Key_Escape
                    and popup_visible
                ):

                    self.hide_variable_popup()
                    return True

                if key in (
                    Qt.Key.Key_Left,
                    Qt.Key.Key_Right,
                    Qt.Key.Key_Home,
                    Qt.Key.Key_End,
                    Qt.Key.Key_PageUp,
                    Qt.Key.Key_PageDown
                ):

                    self.hide_variable_popup()

        return super().eventFilter(watched, event)

    # ==================================
    # OUTPUT EDITOR
    # ==================================

    def create_message_editor(self, node):

        settings = node.settings

        if "message_parts" in settings:

            parts = settings.get("message_parts", [])
            converted_message = ""

            for part in parts:

                if not isinstance(part, dict):
                    continue

                if part.get("type") == "text":

                    converted_message += str(
                        part.get("value", "")
                    )

                elif part.get("type") == "variable":

                    variable = str(
                        part.get("variable", "")
                    ).strip()

                    if variable:
                        converted_message += "{" + variable + "}"

            settings["message"] = converted_message
            settings.pop("message_parts", None)

        container = QWidget()
        container.setMinimumWidth(0)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        heading = QLabel("Output message")
        heading.setObjectName("FieldLabel")
        layout.addWidget(heading)

        explanation = QLabel(
            "Use {variable_name} to insert stored information. "
            "Type { to see available variable suggestions."
        )

        explanation.setObjectName("Muted")
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        field = QTextEdit()
        field.setAcceptRichText(False)
        field.setMinimumHeight(180)
        field.setMaximumHeight(300)

        field.setPlaceholderText(
            "Example:\nHello {name}!\nWelcome to LogicFlow."
        )

        field.setPlainText(
            str(settings.get("message", "Hello!"))
        )

        field.setTabChangesFocus(False)
        layout.addWidget(field)

        field.textChanged.connect(
            lambda: self.save_message_text(node, field)
        )

        self.enable_variable_autocomplete(field)

        refresh_button = QPushButton(
            "↻ Refresh available variables"
        )

        refresh_button.clicked.connect(
            self.refresh_variable_suggestions
        )

        layout.addWidget(refresh_button)

        hint = QLabel(
            "Type { to view variables. Use Up/Down to navigate "
            "and Enter or Tab to insert a suggestion."
        )

        hint.setObjectName("Muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self.inspector_fields_layout.addWidget(container)

    def save_message_text(self, node, field):

        new_message = field.toPlainText()

        if node.settings.get("message", "") == new_message:
            return

        node.settings["message"] = new_message

        self.canvas.record_history(
            "Edit output message",
            merge_key=f"message:{node.node_id}"
        )

    def refresh_variable_suggestions(self):

        variables = self.get_available_variables()

        if variables:

            self.console_message.setText(
                "Available variables: " + ", ".join(variables)
            )

        else:

            self.console_message.setText(
                "No variables found. Add an INPUT or OPERATION node "
                "and give it a variable name."
            )

        self.update_variable_suggestions()

    # ==================================
    # SHOW SELECTED NODE
    # ==================================

    def show_node_properties(self, node):

        self.current_node = node
        self.clear_properties()

        if node is None:
            self.node_description.setText(
                "Select a node to configure what it does."
            )
            return

        descriptions = {
            "START": "This is where your program begins.",
            "INPUT": "Ask the user to enter information.",
            "OPERATION": "Perform a mathematical calculation using two operands.",
            "CONDITION": "Make a decision by comparing values.",
            "OUTPUT": "Display a message or result.",
            "END": "This marks the end of your program."
        }

        self.node_description.setText(
            descriptions.get(node.node_type, "Configure this node.")
        )

        self.add_field(
            "node_name",
            "Node name",
            node.node_name
        )

        self.property_fields["node_name"].editingFinished.connect(
            self.update_node_name
        )

        settings = node.settings

        if node.node_type == "INPUT":

            self.add_field(
                "question",
                "Question to ask",
                settings.get("question", ""),
                "What should the program ask the user?"
            )

            self.add_field(
                "variable",
                "Save answer as",
                settings.get("variable", "answer"),
                "Example: age, name, score"
            )

        elif node.node_type == "OPERATION":

            self.show_mathematical_operation_fields(node)

        elif node.node_type == "CONDITION":

            self.add_field(
                "variable",
                "Variable to check",
                settings.get("variable", "score"),
                "Type { to select an existing variable.",
                autocomplete=True
            )

            self.add_dropdown(
                "comparison",
                "Compare using",
                [
                    "Equal to",
                    "Not equal to",
                    "Greater than",
                    "Less than",
                    "Greater than or equal to",
                    "Less than or equal to"
                ],
                settings.get("comparison", "Greater than")
            )

            self.add_field(
                "compare_value",
                "Compare against",
                settings.get("compare_value", "10"),
                "Enter a number or use {variable_name}.",
                autocomplete=True
            )

        elif node.node_type == "OUTPUT":

            self.create_message_editor(node)

        elif node.node_type in ("START", "END"):

            information = QLabel(
                "Your program begins here."
                if node.node_type == "START"
                else "Your program finishes here."
            )

            information.setWordWrap(True)
            information.setObjectName("Muted")

            self.inspector_fields_layout.addWidget(information)

    # ==================================
    # MATHEMATICAL OPERATION INSPECTOR
    # ==================================

    def show_mathematical_operation_fields(self, node):

        settings = node.settings

        if "operation" not in settings:

            old_action = settings.get(
                "action",
                "Set a value"
            )

            old_operation_map = {
                "Increase a value": "Add",
                "Decrease a value": "Subtract",
                "Multiply a value": "Multiply",
                "Divide a value": "Divide",
            }

            settings["operation"] = old_operation_map.get(
                old_action,
                "Add"
            )

            settings.setdefault(
                "first_variable",
                settings.get("variable", "num1")
            )

            settings.setdefault(
                "second_variable",
                "num2"
            )

            settings.setdefault(
                "result_variable",
                settings.get("variable", "result")
            )

        settings.setdefault("first_variable", "num1")
        settings.setdefault("second_variable", "num2")
        settings.setdefault("result_variable", "result")

        self.add_dropdown(
            "operation",
            "Mathematical operation",
            [
                "Add",
                "Subtract",
                "Multiply",
                "Divide",
            ],
            settings.get("operation", "Add")
        )

        # Both operand fields accept:
        # 1. A variable reference, e.g. {num1}
        # 2. A direct number, e.g. 10
        #
        # Autocomplete activates when the user types "{".

        self.add_field(
            "first_variable",
            "First operand",
            settings.get("first_variable", "num1"),
            "Enter a number (10) or type { to select a variable.",
            autocomplete=True
        )

        self.add_field(
            "second_variable",
            "Second operand",
            settings.get("second_variable", "num2"),
            "Enter a number (5) or type { to select a variable.",
            autocomplete=True
        )

        self.add_field(
            "result_variable",
            "Store answer in",
            settings.get("result_variable", "result"),
            "Enter the name of the variable that will store the answer."
        )

        preview_container = QWidget()

        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 4, 0, 0)
        preview_layout.setSpacing(7)

        preview_heading = QLabel("Expression preview")
        preview_heading.setObjectName("FieldLabel")

        self.operation_preview = QLabel()
        self.operation_preview.setWordWrap(True)
        self.operation_preview.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.operation_preview.setStyleSheet("""
            QLabel {
                background-color: #202631;
                border: 1px solid #353B48;
                border-radius: 6px;
                padding: 12px;
                color: #93C5FD;
                font-size: 15px;
                font-weight: bold;
            }
        """)

        preview_layout.addWidget(preview_heading)
        preview_layout.addWidget(self.operation_preview)

        self.inspector_fields_layout.addWidget(
            preview_container
        )

        for key in (
            "first_variable",
            "second_variable",
            "result_variable"
        ):

            field = self.property_fields.get(key)

            if field is not None:
                field.textChanged.connect(
                    self.update_operation_preview
                )

        operation_field = self.property_fields.get("operation")

        if operation_field is not None:
            operation_field.currentTextChanged.connect(
                self.update_operation_preview
            )

        self.update_operation_preview()

        self.node_description.setText(
            "Choose an operation and enter two operands. "
            "Each operand can be a number or an existing variable "
            "written inside curly brackets, such as {num1}. "
            "Store the answer in a result variable."
        )

    def update_operation_preview(self, *_):

        if not hasattr(self, "operation_preview"):
            return

        operation_field = self.property_fields.get("operation")
        first_field = self.property_fields.get("first_variable")
        second_field = self.property_fields.get("second_variable")
        result_field = self.property_fields.get("result_variable")

        if not all((
            operation_field,
            first_field,
            second_field,
            result_field
        )):
            return

        operation = operation_field.currentText()

        first = first_field.text().strip() or "?"
        second = second_field.text().strip() or "?"
        result = result_field.text().strip() or "?"

        symbols = {
            "Add": "+",
            "Subtract": "-",
            "Multiply": "×",
            "Divide": "÷",
        }

        symbol = symbols.get(operation, "?")

        self.operation_preview.setText(
            f"{result} = {first} {symbol} {second}"
        )

    # ==================================
    # RENAME NODE
    # ==================================

    def update_node_name(self):

        if self.current_node is None:
            return

        field = self.property_fields.get("node_name")

        if field is None:
            return

        new_name = field.text().strip()

        if not new_name:
            field.setText(self.current_node.node_name)
            return

        self.save_property("node_name", new_name)

    # ==================================
    # REQUEST USER INPUT
    # ==================================

    def request_input(self, question):

        answer, accepted = QInputDialog.getText(
            self,
            "LogicFlow - Input",
            question
        )

        if not accepted:
            return None

        return answer

    # ==================================
    # EXECUTION VISUALS
    # ==================================

    def clear_execution_visuals(self):

        for item in self.canvas.scene.items():

            if isinstance(item, NodeItem):
                item.clear_execution_explanation()

        if self.highlighted_node is not None:

            original_pen = self.original_node_pens.get(
                self.highlighted_node
            )

            if original_pen is not None:
                self.highlighted_node.setPen(original_pen)

        self.highlighted_node = None

    def highlight_node(
        self,
        node,
        message=None,
        kind="info"
    ):

        if self.highlighted_node is not None:

            original_pen = self.original_node_pens.get(
                self.highlighted_node
            )

            if original_pen is not None:
                self.highlighted_node.setPen(original_pen)

            self.highlighted_node.clear_execution_explanation()

        self.highlighted_node = node

        if node is None:
            return

        if node not in self.original_node_pens:
            self.original_node_pens[node] = node.pen()

        node.setPen(
            QPen(QColor("#FBBF24"), 3)
        )

        if message:
            node.set_execution_explanation(
                message,
                kind
            )

        self.canvas.view.ensureVisible(
            node,
            80,
            80
        )

    # ==================================
    # START DEBUG EXECUTION
    # ==================================

    def start_execution(self):

        from engine.execution_engine import ExecutionEngine

        self.reset_execution()

        nodes = [
            item
            for item in self.canvas.scene.items()
            if isinstance(item, NodeItem)
        ]

        connections = self.canvas.scene.connections

        if not nodes:

            self.console_message.setText(
                "Your workspace is empty. Add some nodes first."
            )

            return

        self.execution_engine = ExecutionEngine(
            nodes,
            connections
        )

        result = self.execution_engine.start()

        if not result.success:

            self.console_message.setText(
                "ERROR: " + result.message
            )

            self.debugger_panel.set_state(
                "error",
                result.message
            )

            self.execution_engine = None
            return

        self.console_message.setText(
            "Execution is ready. Press Next Step to begin."
        )

        self.explanation_message.setText(
            "The Start node is ready to execute."
        )

        self.debugger_panel.clear_history()

        self.debugger_panel.set_state(
            "ready",
            "Program ready. Press Next Step to execute."
        )

        self.update_variable_memory()

        self.highlight_node(
            result.current_node,
            "Program execution starts here. Press Next Step to execute this node.",
            "info"
        )

    # ==================================
    # EXECUTE NEXT NODE
    # ==================================

    def execute_next_step(self):

        if self.execution_engine is None:
            return

        engine = self.execution_engine

        result = engine.step(
            input_provider=self.request_input
        )

        executed_node = result.current_node

        if executed_node is not None:

            if result.error:
                explanation_kind = "error"

            elif executed_node.node_type == "CONDITION":
                explanation_kind = "warning"

            elif executed_node.node_type == "OUTPUT":
                explanation_kind = "success"

            else:
                explanation_kind = "info"

            self.highlight_node(
                executed_node,
                result.message,
                explanation_kind
            )

            self.debugger_panel.add_history_entry(
                engine.step_count,
                executed_node.node_name,
                executed_node.node_type,
                result.message,
                result.error
            )

        self.explanation_message.setText(result.message)

        if (
            executed_node is not None
            and executed_node.node_type == "OUTPUT"
            and not result.error
        ):

            self.execution_outputs.append(
                engine.last_output
            )

        if self.execution_outputs:

            self.console_message.setText(
                "PROGRAM OUTPUT:\n"
                + "\n".join(self.execution_outputs)
            )

        self.update_variable_memory()

        if result.error or not result.success:

            self.console_message.setText(
                "EXECUTION ERROR:\n" + result.message
            )

            self.debugger_panel.set_state(
                "error",
                result.message
            )

            return

        if result.finished:

            self.console_message.setText(
                "PROGRAM OUTPUT:\n"
                + (
                    "\n".join(self.execution_outputs)
                    if self.execution_outputs
                    else "No output was produced."
                )
                + "\n\nProgram completed successfully!"
            )

            self.debugger_panel.set_state(
                "completed",
                "Program execution completed successfully."
            )

        else:

            self.debugger_panel.set_state(
                "ready",
                f"Executed {executed_node.node_name}. "
                "Press Next Step to continue."
            )

    # ==================================
    # STOP EXECUTION
    # ==================================

    def stop_execution(self):

        if self.execution_engine is None:
            return

        result = self.execution_engine.stop()

        self.clear_execution_visuals()

        self.debugger_panel.set_state(
            "stopped",
            result.message
        )

        self.explanation_message.setText(
            result.message
        )

    # ==================================
    # VARIABLE MEMORY
    # ==================================

    def update_variable_memory(self):

        if self.execution_engine is None:

            self.memory_message.setText(
                "Variables: No information stored yet."
            )

            return

        variables = self.execution_engine.variables

        if not variables:

            self.memory_message.setText(
                "Variables: No information stored yet."
            )

            return

        memory_text = "Variables: " + " | ".join(
            f"{name} = {value}"
            for name, value in variables.items()
        )

        self.memory_message.setText(memory_text)

    # ==================================
    # RESET EXECUTION
    # ==================================

    def reset_execution(self):

        self.clear_execution_visuals()

        self.execution_engine = None
        self.execution_outputs.clear()
        self.execution_success = False

        self.console_message.setText(
            "Execution has been reset."
        )

        self.explanation_message.setText(
            "Press Start to begin again."
        )

        self.memory_message.setText(
            "Variables: No information stored yet."
        )

        self.debugger_panel.clear_history()

        self.debugger_panel.set_state(
            "idle",
            "Execution reset. Ready to start again."
        )

    # ==================================
    # CHALLENGE VALIDATION
    # ==================================

    def validate_active_challenge(self):

        challenge_index = getattr(
            self.learning_page,
            "active_challenge",
            None
        )

        if challenge_index is None:
            return

        nodes = [
            item
            for item in self.canvas.scene.items()
            if isinstance(item, NodeItem)
        ]

        connections = self.canvas.scene.connections

        validator = ChallengeValidator(
            nodes,
            connections
        )

        result = validator.validate(challenge_index)

        if result.passed:

            already_completed = (
                challenge_index in self.completed_challenges
            )

            if not already_completed:

                self.completed_challenges.add(
                    challenge_index
                )

                self.challenge_xp += result.xp
                self.save_learning_progress()
                self.refresh_dashboard()

                self.console_message.setText(
                    self.console_message.text()
                    + "\n\nCHALLENGE COMPLETED!"
                    + f"\nXP earned: {result.xp}"
                    + f"\nTotal challenge XP: {self.challenge_xp}"
                )

                QMessageBox.information(
                    self,
                    "Challenge Completed!",
                    (
                        result.message
                        + f"\n\nYou earned {result.xp} XP!"
                        + f"\nTotal XP: {self.challenge_xp}"
                    )
                )

            else:

                self.console_message.setText(
                    self.console_message.text()
                    + "\n\nChallenge already completed. "
                    "You have already received its XP."
                )

        else:

            self.console_message.setText(
                self.console_message.text()
                + "\n\nCHALLENGE NOT COMPLETED"
                + "\n"
                + result.message
            )

            QMessageBox.information(
                self,
                "Keep Working!",
                (
                    result.message
                    + f"\n\nTests passed: "
                    f"{result.tests_passed}/{result.total_tests}"
                )
            )

    # ==================================
    # RUN ENTIRE PROGRAM
    # ==================================

    def run_program(self):

        from engine.execution_engine import ExecutionEngine

        self.reset_execution()

        self.execution_outputs = []
        self.execution_success = False

        nodes = [
            item
            for item in self.canvas.scene.items()
            if isinstance(item, NodeItem)
        ]

        connections = self.canvas.scene.connections

        if not nodes:

            self.console_message.setText(
                "Your workspace is empty. Add some nodes first."
            )

            return

        self.console_message.setText(
            "Preparing your program..."
        )

        self.run_button.setEnabled(False)

        outputs = []

        try:

            engine = ExecutionEngine(
                nodes,
                connections
            )

            self.execution_engine = engine

            start_result = engine.start()

            if not start_result.success:

                self.console_message.setText(
                    start_result.message
                )

                self.debugger_panel.set_state(
                    "error",
                    start_result.message
                )

                return

            while not engine.finished:

                result = engine.step(
                    input_provider=self.request_input
                )

                executed_node = result.current_node

                if executed_node is not None:

                    self.debugger_panel.add_history_entry(
                        engine.step_count,
                        executed_node.node_name,
                        executed_node.node_type,
                        result.message,
                        result.error
                    )

                if (
                    executed_node is not None
                    and executed_node.node_type == "OUTPUT"
                    and not result.error
                ):

                    outputs.append(engine.last_output)
                    self.execution_outputs = outputs.copy()

                if result.error or not result.success:

                    error_message = result.message
                    self.execution_success = False

                    self.console_message.setText(
                        (
                            "PROGRAM OUTPUT:\n"
                            + "\n".join(outputs)
                            + "\n\nERROR:\n"
                            + error_message
                        )
                        if outputs
                        else "ERROR: " + error_message
                    )

                    self.debugger_panel.set_state(
                        "error",
                        error_message
                    )

                    return

            self.execution_engine = engine
            self.execution_outputs = outputs.copy()
            self.execution_success = True

            self.update_variable_memory()

            if outputs:

                self.console_message.setText(
                    "PROGRAM OUTPUT:\n"
                    + "\n".join(outputs)
                    + "\n\nProgram completed successfully!"
                )

            else:

                self.console_message.setText(
                    "Program completed successfully, "
                    "but no OUTPUT node produced a message."
                )

            self.debugger_panel.set_state(
                "completed",
                "Program executed successfully."
            )

            self.validate_active_challenge()

        except Exception as error:

            self.execution_success = False

            self.console_message.setText(
                f"An unexpected error occurred: {error}"
            )

            self.debugger_panel.set_state(
                "error",
                str(error)
            )

        finally:

            self.run_button.setEnabled(True)

            # ==================================
    # SAVE PROJECT
    # ==================================

    def save_project(self):

        if self.current_project_path is None:

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save LogicFlow Project",
                str(
                    self.project_manager.projects_directory
                    / "My Project.logicflow"
                ),
                "LogicFlow Projects (*.logicflow)"
            )

            if not file_path:
                return

        else:
            file_path = str(self.current_project_path)

        try:

            saved_path = self.project_manager.save_project(
                file_path,
                self.canvas.scene,
                self.canvas.node_counter
            )

            self.current_project_path = saved_path

            self.setWindowTitle(
                f"LogicFlow - {saved_path.stem}"
            )

            self.console_message.setText(
                f"Project saved successfully: {saved_path.name}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Failed",
                f"Could not save the project:\n{error}"
            )

    # ==================================
    # LOAD PROJECT
    # ==================================

    def load_project(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open LogicFlow Project",
            str(self.project_manager.projects_directory),
            "LogicFlow Projects (*.logicflow)"
        )

        if not file_path:
            return

        try:

            # Clear temporary execution state before replacing
            # the current graph.
            self.reset_execution()

            self.project_manager.load_project(
                file_path,
                self.canvas.scene,
                self.canvas
            )
            self.canvas.reset_history()

            self.current_project_path = file_path

            from pathlib import Path

            project_name = Path(file_path).stem

            self.setWindowTitle(
                f"LogicFlow - {project_name}"
            )

            self.show_node_properties(None)

            self.console_message.setText(
                f"Project loaded successfully: {Path(file_path).name}"
            )

            self.explanation_message.setText(
                "Project loaded. Your flowchart is ready."
            )

            self.refresh_dashboard()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Load Failed",
                f"Could not load the project:\n{error}"
            )