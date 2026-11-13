
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class VariableInspector(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("VariableInspector")

        self.previous_variables = {}

        self.setStyleSheet("""
            QFrame#VariableInspector {
                background-color: #181B22;
                border: 1px solid #292D36;
                border-radius: 8px;
            }

            QLabel#InspectorTitle {
                color: #F3F4F6;
                font-size: 15px;
                font-weight: bold;
            }

            QLabel#InspectorMessage {
                color: #9CA3AF;
            }

            QTableWidget {
                background-color: #111318;
                border: 1px solid #292D36;
                border-radius: 6px;
                gridline-color: #292D36;
                selection-background-color: #252A34;
                outline: none;
            }

            QHeaderView::section {
                background-color: #252A34;
                color: #D1D5DB;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #353B48;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 7px;
            }
        """)

        self.build_interface()

    # ----------------------------------
    # BUILD INTERFACE
    # ----------------------------------

    def build_interface(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        title = QLabel("Variable Inspector")
        title.setObjectName("InspectorTitle")

        layout.addWidget(title)

        self.message_label = QLabel(
            "Variables will appear here during execution."
        )
        self.message_label.setObjectName("InspectorMessage")
        self.message_label.setWordWrap(True)

        layout.addWidget(self.message_label)

        self.variable_table = QTableWidget()

        self.variable_table.setColumnCount(2)
        self.variable_table.setHorizontalHeaderLabels(
            ["Variable", "Current Value"]
        )

        self.variable_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.variable_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.variable_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.variable_table.verticalHeader().setVisible(False)

        header = self.variable_table.horizontalHeader()

        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

        self.variable_table.setMinimumHeight(150)

        layout.addWidget(self.variable_table)

    # ----------------------------------
    # UPDATE VARIABLES
    # ----------------------------------

    def update_variables(self, variables):

        if not variables:

            self.variable_table.setRowCount(0)

            self.message_label.setText(
                "No variables have been created yet."
            )

            self.previous_variables = {}
            return

        self.variable_table.setRowCount(len(variables))

        for row, (name, value) in enumerate(
            variables.items()
        ):

            name = str(name)
            display_value = str(value)

            previous_value = self.previous_variables.get(
                name,
                object()
            )

            changed = (
                previous_value != value
            )

            name_item = QTableWidgetItem(name)
            value_item = QTableWidgetItem(display_value)

            name_item.setFlags(
                name_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            value_item.setFlags(
                value_item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

            if changed:

                highlight = QColor("#263B32")

                name_item.setBackground(highlight)
                value_item.setBackground(highlight)

                value_item.setForeground(
                    QColor("#86EFAC")
                )

            self.variable_table.setItem(
                row, 0, name_item
            )

            self.variable_table.setItem(
                row, 1, value_item
            )

        self.message_label.setText(
            f"{len(variables)} variable(s) currently stored."
        )

        self.previous_variables = dict(variables)

    # ----------------------------------
    # CLEAR VARIABLES
    # ----------------------------------

    def clear_variables(self):

        self.variable_table.setRowCount(0)

        self.previous_variables.clear()

        self.message_label.setText(
            "No variables have been created yet."
        )

    # ----------------------------------
    # GET CURRENT VARIABLES
    # ----------------------------------

    def get_displayed_variables(self):

        return dict(self.previous_variables)
