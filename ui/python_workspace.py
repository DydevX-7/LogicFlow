
import sys

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QFrame,
    QLabel,
    QPushButton,
    QGraphicsView,
    QPlainTextEdit,
    QLineEdit,
    QFileDialog,
    QApplication,
)
from PySide6.QtCore import QProcess

from engine.code_generator import CodeGenerator


class PythonWorkspace(QWidget):

    back_requested = Signal()

    def __init__(self, canvas, parent=None):
        super().__init__(parent)

        self.canvas = canvas
        self.scene = canvas.scene

        self.program = None
        self.sections = []
        self.syncing = False

        self.zoom_factor = 1.15

        # Python execution process
        self.process = QProcess(self)

        self.process.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels
        )

        self.process.readyReadStandardOutput.connect(
            self.read_output
        )

        self.process.finished.connect(
            self.process_finished
        )

        # Delayed code refresh
        self.refresh_timer = QTimer(self)

        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.setInterval(250)

        self.refresh_timer.timeout.connect(
            self.refresh_code
        )

        self.build_ui()

        self.scene.changed.connect(
            self.schedule_refresh
        )

        self.scene.selectionChanged.connect(
            self.on_selection_changed
        )

        self.refresh_code()

    # ==================================
    # BUILD USER INTERFACE
    # ==================================

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)

        # ==================================
        # TOP BAR
        # ==================================

        top_bar = QFrame()

        top_layout = QHBoxLayout(top_bar)

        top_layout.setContentsMargins(5, 3, 5, 3)

        back_button = QPushButton(
            "← Flowchart Editor"
        )

        back_button.clicked.connect(
            self.back_requested.emit
        )

        title = QLabel(
            "Python Code Generator"
        )

        title.setStyleSheet("""
            font-size: 19px;
            font-weight: bold;
            color: #F3F4F6;
        """)

        subtitle = QLabel(
            "Visual logic → Python"
        )

        subtitle.setStyleSheet(
            "color: #9CA3AF;"
        )

        top_layout.addWidget(back_button)
        top_layout.addSpacing(12)
        top_layout.addWidget(title)
        top_layout.addWidget(subtitle)
        top_layout.addStretch()

        main_layout.addWidget(top_bar)

        # ==================================
        # MAIN WORKSPACE SPLITTER
        # ==================================

        self.splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(6)

        # ==================================
        # LEFT PANEL: FLOWCHART
        # ==================================

        graph_panel = QFrame()

        graph_panel.setMinimumWidth(170)

        graph_layout = QVBoxLayout(graph_panel)

        graph_layout.setContentsMargins(8, 8, 8, 8)
        graph_layout.setSpacing(7)

        graph_title = QLabel(
            "YOUR FLOWCHART"
        )

        graph_title.setStyleSheet("""
            font-weight: bold;
            color: #D1D5DB;
        """)

        # ZOOM CONTROLS

        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(4)

        self.zoom_out_button = QPushButton("−")
        self.zoom_out_button.setToolTip("Zoom out")

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.setToolTip("Zoom in")

        self.fit_button = QPushButton("Fit")
        self.fit_button.setToolTip(
            "Fit the entire flowchart into view"
        )

        self.zoom_out_button.setFixedWidth(38)
        self.zoom_in_button.setFixedWidth(38)

        self.zoom_out_button.clicked.connect(
            self.zoom_out
        )

        self.zoom_in_button.clicked.connect(
            self.zoom_in
        )

        self.fit_button.clicked.connect(
            self.fit_graph
        )

        zoom_layout.addWidget(self.zoom_out_button)
        zoom_layout.addWidget(self.zoom_in_button)
        zoom_layout.addWidget(self.fit_button)
        zoom_layout.addStretch()

        # SECOND VIEW OF THE EXISTING SCENE

        self.graph_view = QGraphicsView(
            self.scene
        )

        self.graph_view.setRenderHints(
            self.canvas.view.renderHints()
        )

        self.graph_view.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )

        self.graph_view.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.graph_view.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        self.graph_view.setMinimumWidth(150)

        self.graph_view.setStyleSheet("""
            QGraphicsView {
                background-color: #111318;
                border: 1px solid #292D36;
                border-radius: 6px;
            }
        """)

        graph_layout.addWidget(graph_title)
        graph_layout.addLayout(zoom_layout)
        graph_layout.addWidget(
            self.graph_view,
            1
        )

        # ==================================
        # MIDDLE PANEL: PYTHON CODE
        # ==================================

        code_panel = QFrame()

        code_panel.setMinimumWidth(300)

        code_layout = QVBoxLayout(code_panel)

        code_layout.setContentsMargins(10, 8, 10, 8)
        code_layout.setSpacing(6)

        # CODE HEADER

        code_header = QHBoxLayout()

        code_title = QLabel(
            "GENERATED PYTHON"
        )

        code_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #60A5FA;
        """)

        self.code_status = QLabel(
            "Live generation enabled"
        )

        self.code_status.setStyleSheet(
            "color: #9CA3AF; font-size: 11px;"
        )

        code_header.addWidget(code_title)
        code_header.addStretch()
        code_header.addWidget(self.code_status)

        # CODE EDITOR

        self.code_editor = QPlainTextEdit()

        self.code_editor.setReadOnly(True)

        self.code_editor.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )

        self.code_editor.setFont(
            QFont("Consolas", 12)
        )

        self.code_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #111827;
                color: #E5E7EB;
                border: 1px solid #292D36;
                border-radius: 7px;
                padding: 12px;
                selection-background-color: #2563EB;
            }
        """)

        self.code_editor.cursorPositionChanged.connect(
            self.on_code_cursor_changed
        )

        # ACTION BUTTONS

        buttons = QHBoxLayout()

        self.copy_button = QPushButton(
            "Copy Code"
        )

        self.export_button = QPushButton(
            "Export .py"
        )

        self.run_button = QPushButton(
            "▶ Run Python"
        )

        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3B82F6;
            }
        """)

        self.copy_button.clicked.connect(
            self.copy_code
        )

        self.export_button.clicked.connect(
            self.export_code
        )

        self.run_button.clicked.connect(
            self.run_code
        )

        buttons.addWidget(self.copy_button)
        buttons.addWidget(self.export_button)
        buttons.addStretch()
        buttons.addWidget(self.run_button)

        # ==================================
        # COMPACT OUTPUT TERMINAL
        # ==================================

        output_header = QHBoxLayout()

        output_title = QLabel(
            "PROGRAM OUTPUT"
        )

        output_title.setStyleSheet("""
            font-weight: bold;
            color: #D1D5DB;
            font-size: 11px;
        """)

        self.clear_output_button = QPushButton(
            "Clear"
        )

        self.clear_output_button.setFixedHeight(26)

        self.clear_output_button.clicked.connect(
            self.clear_console
        )

        output_header.addWidget(output_title)
        output_header.addStretch()
        output_header.addWidget(
            self.clear_output_button
        )

        self.console = QPlainTextEdit()

        self.console.setReadOnly(True)

        self.console.setMaximumHeight(85)
        self.console.setMinimumHeight(55)

        self.console.setFont(
            QFont("Consolas", 9)
        )

        self.console.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth
        )

        self.console.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0D1117;
                color: #A7F3D0;
                border: 1px solid #292D36;
                border-radius: 6px;
                padding: 5px;
            }
        """)

        self.console.setPlaceholderText(
            "Program output will appear here, one line at a time."
        )

        # INPUT FIELD

        self.input_field = QLineEdit()

        self.input_field.setMinimumHeight(34)

        self.input_field.setPlaceholderText(
            "Enter program input and press Enter..."
        )

        self.input_field.returnPressed.connect(
            self.send_input
        )

        # ADD CODE PANEL WIDGETS

        code_layout.addLayout(code_header)

        code_layout.addWidget(
            self.code_editor,
            1
        )

        code_layout.addLayout(buttons)

        code_layout.addLayout(output_header)

        code_layout.addWidget(
            self.console
        )

        code_layout.addWidget(
            self.input_field
        )

        # ==================================
        # RIGHT PANEL: EXPLANATION
        # ==================================

        learning_panel = QFrame()

        learning_panel.setMinimumWidth(150)

        learning_layout = QVBoxLayout(
            learning_panel
        )

        learning_layout.setContentsMargins(
            9, 8, 9, 8
        )

        learning_layout.setSpacing(8)

        learning_title = QLabel(
            "UNDERSTAND THE CODE"
        )

        learning_title.setStyleSheet("""
            font-weight: bold;
            color: #D1D5DB;
        """)

        self.node_title = QLabel(
            "Select a flowchart node"
        )

        self.node_title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #60A5FA;
        """)

        self.node_title.setWordWrap(True)

        self.explanation = QPlainTextEdit()

        self.explanation.setReadOnly(True)

        self.explanation.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth
        )

        self.explanation.setFont(
            QFont("Segoe UI", 10)
        )

        self.explanation.setStyleSheet("""
            QPlainTextEdit {
                background-color: #111827;
                border: 1px solid #292D36;
                border-radius: 6px;
                padding: 7px;
                color: #D1D5DB;
            }
        """)

        self.explanation.setPlaceholderText(
            "Select a node to understand its Python code."
        )

        learning_layout.addWidget(
            learning_title
        )

        learning_layout.addWidget(
            self.node_title
        )

        learning_layout.addWidget(
            self.explanation,
            1
        )

        # ==================================
        # ADD PANELS TO SPLITTER
        # ==================================

        self.splitter.addWidget(
            graph_panel
        )

        self.splitter.addWidget(
            code_panel
        )

        self.splitter.addWidget(
            learning_panel
        )

        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 6)
        self.splitter.setStretchFactor(2, 2)

        self.splitter.setSizes([
            240,
            700,
            240
        ])

        main_layout.addWidget(
            self.splitter,
            1
        )

        # Fit the graph after the widget has been displayed.
        QTimer.singleShot(
            300,
            self.fit_graph
        )

    # ==================================
    # GRAPH ZOOM CONTROLS
    # ==================================

    def zoom_in(self):

        self.graph_view.scale(
            self.zoom_factor,
            self.zoom_factor
        )

    def zoom_out(self):

        self.graph_view.scale(
            1 / self.zoom_factor,
            1 / self.zoom_factor
        )

    def fit_graph(self):

        bounds = self.scene.itemsBoundingRect()

        if bounds.isNull() or not bounds.isValid():
            return

        bounds = bounds.adjusted(
            -70,
            -70,
            70,
            70
        )

        self.graph_view.resetTransform()

        self.graph_view.fitInView(
            bounds,
            Qt.AspectRatioMode.KeepAspectRatio
        )

    # ==================================
    # GRAPH AND CODE GENERATION
    # ==================================

    def get_nodes(self):

        return [
            item
            for item in self.scene.items()
            if hasattr(item, "node_type")
            and hasattr(item, "node_id")
        ]

    def schedule_refresh(self, *args):

        self.refresh_timer.start()

    def refresh_code(self):

        try:

            nodes = self.get_nodes()
            connections = self.scene.connections

            generator = CodeGenerator(
                nodes,
                connections
            )

            self.program = generator.generate()

            self.sections = self.program.sections

            self.code_editor.setPlainText(
                self.program.code
            )

            self.code_status.setText(
                "Code generated successfully"
            )

            self.set_buttons_enabled(True)

            selected = [
                item
                for item in self.scene.selectedItems()
                if hasattr(item, "node_type")
                and hasattr(item, "node_id")
            ]

            if selected:

                self.select_node(
                    selected[0]
                )

            else:

                self.node_title.setText(
                    "Select a flowchart node"
                )

                self.explanation.clear()

        except Exception as error:

            self.program = None
            self.sections = []

            self.code_editor.setPlainText(
                "# Python code cannot be generated yet.\n"
                "# Check your flowchart connections.\n\n"
                f"# {error}"
            )

            self.code_status.setText(
                "Generation needs attention"
            )

            self.node_title.setText(
                "Flowchart needs attention"
            )

            self.explanation.setPlainText(
                str(error)
            )

            self.set_buttons_enabled(False)

    def set_buttons_enabled(self, enabled):

        self.copy_button.setEnabled(enabled)
        self.export_button.setEnabled(enabled)
        self.run_button.setEnabled(enabled)

    # ==================================
    # NODE SELECTION
    # ==================================

    def get_section(self, node):

        if self.program is None:
            return None

        return self.program.get_section_for_node(
            node
        )

    def on_selection_changed(self):

        if self.syncing:
            return

        selected = [
            item
            for item in self.scene.selectedItems()
            if hasattr(item, "node_type")
            and hasattr(item, "node_id")
        ]

        if selected:

            self.select_node(
                selected[0]
            )

    def select_node(self, node):

        if self.syncing:
            return

        section = self.get_section(node)

        if section is None:
            return

        self.syncing = True

        try:

            self.node_title.setText(
                f"{section.node_type}: {section.node_name}"
            )

            explanation = getattr(
                section,
                "explanation",
                ""
            )

            concepts = getattr(
                section,
                "concepts",
                []
            )

            if concepts:

                explanation += (
                    "\n\nPython concepts:\n"
                )

                explanation += "\n".join(
                    f"• {concept}"
                    for concept in concepts
                )

            self.explanation.setPlainText(
                explanation or "No explanation available."
            )

            self.highlight_section(
                section
            )

        finally:

            self.syncing = False

    # ==================================
    # HIGHLIGHT GENERATED CODE
    # ==================================

    def highlight_section(self, section):

        start = max(
            0,
            getattr(section, "start_line", 1) - 1
        )

        end = max(
            start,
            getattr(section, "end_line", start + 1) - 1
        )

        document = self.code_editor.document()

        first = document.findBlockByNumber(
            start
        )

        last = document.findBlockByNumber(
            end
        )

        if not first.isValid():
            return

        cursor = QTextCursor(document)

        cursor.setPosition(
            first.position()
        )

        if last.isValid():

            cursor.setPosition(
                last.position() + len(last.text()),
                QTextCursor.MoveMode.KeepAnchor
            )

        self.code_editor.setTextCursor(
            cursor
        )

        self.code_editor.centerCursor()

    # ==================================
    # CODE TO NODE NAVIGATION
    # ==================================

    def on_code_cursor_changed(self):

        if self.syncing or self.program is None:
            return

        line = (
            self.code_editor.textCursor().blockNumber() + 1
        )

        for section in self.sections:

            start = getattr(
                section,
                "start_line",
                1
            )

            end = getattr(
                section,
                "end_line",
                start
            )

            if start <= line <= end:

                node = getattr(
                    section,
                    "node_ref",
                    None
                )

                if node is None:
                    return

                self.syncing = True

                try:

                    self.scene.clearSelection()

                    node.setSelected(True)

                    self.graph_view.centerOn(
                        node
                    )

                    self.node_title.setText(
                        f"{section.node_type}: {section.node_name}"
                    )

                    explanation = getattr(
                        section,
                        "explanation",
                        ""
                    )

                    concepts = getattr(
                        section,
                        "concepts",
                        []
                    )

                    if concepts:

                        explanation += (
                            "\n\nPython concepts:\n"
                            + "\n".join(
                                f"• {concept}"
                                for concept in concepts
                            )
                        )

                    self.explanation.setPlainText(
                        explanation
                    )

                finally:

                    self.syncing = False

                return

    # ==================================
    # CONSOLE HELPERS
    # ==================================

    def clear_console(self):

        self.console.clear()

    def append_console_message(self, message):

        self.console.appendPlainText(
            str(message)
        )

        self.console.ensureCursorVisible()

    # ==================================
    # COPY CODE
    # ==================================

    def copy_code(self):

        if self.program is None:
            return

        QApplication.clipboard().setText(
            self.program.code
        )

        self.append_console_message(
            "Code copied to clipboard."
        )

    # ==================================
    # EXPORT PYTHON FILE
    # ==================================

    def export_code(self):

        if self.program is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Python Program",
            "logicflow_program.py",
            "Python Files (*.py)"
        )

        if not path:
            return

        if not path.lower().endswith(".py"):
            path += ".py"

        try:

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.program.code
                )

            self.append_console_message(
                f"Exported successfully: {path}"
            )

        except OSError as error:

            self.append_console_message(
                f"Export failed: {error}"
            )

    # ==================================
    # RUN GENERATED PYTHON
    # ==================================

    def run_code(self):

        if self.program is None:
            return

        if (
            self.process.state()
            != QProcess.ProcessState.NotRunning
        ):

            self.append_console_message(
                "A program is already running."
            )

            return

        self.console.clear()

        self.append_console_message(
            "Running generated Python program..."
        )

        self.process.start(
            sys.executable,
            [
                "-u",
                "-c",
                self.program.code
            ]
        )

    # ==================================
    # READ PROGRAM OUTPUT
    # ==================================

    def read_output(self):

        output = bytes(
            self.process.readAllStandardOutput()
        ).decode(
            "utf-8",
            errors="replace"
        )

        if not output:
            return

        # Normalize Windows line endings while preserving
        # every newline produced by Python print().

        output = output.replace(
            "\r\n",
            "\n"
        )

        self.console.moveCursor(
            QTextCursor.MoveOperation.End
        )

        self.console.insertPlainText(
            output
        )

        self.console.ensureCursorVisible()

    # ==================================
    # SEND INPUT TO RUNNING PROGRAM
    # ==================================

    def send_input(self):

        if (
            self.process.state()
            != QProcess.ProcessState.Running
        ):
            return

        value = self.input_field.text()

        self.input_field.clear()

        self.append_console_message(
            value
        )

        self.process.write(
            (value + "\n").encode("utf-8")
        )

    # ==================================
    # PROGRAM FINISHED
    # ==================================

    def process_finished(
        self,
        exit_code,
        exit_status
    ):

        self.read_output()

        if exit_code == 0:

            self.append_console_message(
                "Program finished successfully."
            )

        else:

            self.append_console_message(
                f"Program exited with code {exit_code}."
            )
