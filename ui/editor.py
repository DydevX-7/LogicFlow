
import copy
import time

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QInputDialog,
    QMenu,
    QLabel,
)
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen,
    QFont,
    QPainter,
    QPainterPath,
    QUndoStack,
    QUndoCommand,
)


# ==================================
# UNDO / REDO COMMAND
# ==================================

class GraphSnapshotCommand(QUndoCommand):

    COMMAND_ID = 1

    def __init__(
        self,
        editor,
        before,
        after,
        description="Edit graph",
        merge_key=None
    ):
        super().__init__(description)

        self.editor = editor
        self.before = copy.deepcopy(before)
        self.after = copy.deepcopy(after)
        self.merge_key = merge_key
        self.timestamp = time.monotonic()
        self.skip_first_redo = True

    def id(self):
        return self.COMMAND_ID

    def mergeWith(self, other):
        if not isinstance(other, GraphSnapshotCommand):
            return False

        if self.merge_key is None:
            return False

        if self.merge_key != other.merge_key:
            return False

        if other.timestamp - self.timestamp > 1.0:
            return False

        self.after = copy.deepcopy(other.after)
        self.timestamp = other.timestamp
        self.setText(other.text())

        return True

    def undo(self):
        self.editor.restore_snapshot(self.before)

    def redo(self):
        if self.skip_first_redo:
            self.skip_first_redo = False
            return

        self.editor.restore_snapshot(self.after)


# ==================================
# CONNECTION POINT
# ==================================

class PortItem(QGraphicsEllipseItem):

    def __init__(self, node, port_type):
        super().__init__(-7, -7, 14, 14, node)

        self.node = node
        self.port_type = port_type

        self.normal_color = QColor("#60A5FA")

        if port_type == "true":
            self.normal_color = QColor("#34D399")

        elif port_type == "false":
            self.normal_color = QColor("#F87171")

        self.setBrush(QBrush(self.normal_color))
        self.setPen(QPen(QColor("#FFFFFF"), 1.5))
        self.setZValue(5)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)

        self.setToolTip(f"Drag from {port_type.upper()} port")

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor("#FBBF24")))
        self.setRect(-9, -9, 18, 18)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(self.normal_color))
        self.setRect(-7, -7, 14, 14)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.port_type != "input":
                self.scene().start_connection(self)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.port_type != "input":
            self.scene().update_connection(event.scenePos())

        event.accept()

    def mouseReleaseEvent(self, event):
        if self.port_type != "input":
            self.scene().finish_connection(event.scenePos())

        event.accept()


# ==================================
# CONNECTION LINE
# ==================================

class ConnectionItem(QGraphicsPathItem):

    def __init__(
        self,
        source_node,
        target_node,
        source_port_type="output"
    ):
        super().__init__()

        self.source_node = source_node
        self.target_node = target_node
        self.source_port_type = source_port_type
        self.branch = source_port_type

        self.source_port = source_node.get_output_port(
            source_port_type
        )

        self.normal_pen = QPen(QColor("#60A5FA"), 2.8)
        self.normal_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.setPen(self.normal_pen)
        self.setBrush(Qt.BrushStyle.NoBrush)

        self.setFlag(
            QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        self.setZValue(0)

        self.label = None

        if source_port_type in ("true", "false"):
            self.label = QGraphicsTextItem(source_port_type.upper(), self)

            color = (
                QColor("#34D399")
                if source_port_type == "true"
                else QColor("#F87171")
            )

            self.label.setDefaultTextColor(color)
            self.label.setFont(
                QFont("Segoe UI", 8, QFont.Weight.Bold)
            )
            self.label.setZValue(2)

        self.update_position()

    def update_position(self):
        start = self.source_port.mapToScene(QPointF(0, 0))
        end = self.target_node.input_port.mapToScene(QPointF(0, 0))

        path = QPainterPath(start)

        distance = max(60, abs(end.x() - start.x()) * 0.5)

        path.cubicTo(
            QPointF(start.x() + distance, start.y()),
            QPointF(end.x() - distance, end.y()),
            end
        )

        self.setPath(path)

        if self.label:
            midpoint = path.pointAtPercent(0.5)
            self.label.setPos(
                midpoint.x(),
                midpoint.y() - 18
            )

    def itemChange(self, change, value):
        if (
            change
            == QGraphicsPathItem.GraphicsItemChange.ItemSelectedHasChanged
        ):
            pen = QPen(
                QColor("#FBBF24") if value else QColor("#60A5FA"),
                3.5 if value else 2.8
            )

            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            self.setPen(pen)

        return super().itemChange(change, value)


# ==================================
# NODE COMPONENT
# ==================================

class NodeItem(QGraphicsRectItem):

    WIDTH = 200
    HEIGHT = 95

    NORMAL_Z_VALUE = 1
    ACTIVE_Z_VALUE = 1000

    COLORS = {
        "START": "#244B72",
        "INPUT": "#28543E",
        "OPERATION": "#59482C",
        "CONDITION": "#59482C",
        "OUTPUT": "#28543E",
        "END": "#244B72",
    }

    def __init__(self, node_type, node_id, name=None):
        super().__init__(0, 0, self.WIDTH, self.HEIGHT)

        self.node_type = node_type
        self.node_id = node_id
        self.node_name = name or f"{node_type.title()} {node_id}"

        self.settings = {
            "INPUT": {
                "question": "What is your name?",
                "variable": "name",
            },
            "OPERATION": {
                "action": "Set a value",
                "variable": "score",
                "value": "0",
                "amount": "1",
            },
            "CONDITION": {
                "variable": "score",
                "comparison": "Greater than",
                "compare_value": "10",
            },
            "OUTPUT": {
                "message": "Hello!",
            },
        }.get(node_type, {})

        self.connections = []
        self._history_start_pos = None

        self.setBrush(QBrush(QColor(self.COLORS[node_type])))
        self.setPen(QPen(QColor("#64748B"), 1.5))

        self.setFlags(
            QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        self.setZValue(self.NORMAL_Z_VALUE)

        self.title = QGraphicsTextItem(self.node_name, self)
        self.title.setDefaultTextColor(QColor("#FFFFFF"))

        font = QFont("Segoe UI", 12)
        font.setBold(True)

        self.title.setFont(font)
        self.title.setTextWidth(172)
        self.title.setPos(14, 12)

        self.subtitle = QGraphicsTextItem(
            f"{node_type} | ID: {node_id}", self
        )

        self.subtitle.setDefaultTextColor(QColor("#D1D5DB"))
        self.subtitle.setFont(QFont("Segoe UI", 9))
        self.subtitle.setPos(14, 58)

        # EXECUTION EXPLANATION CARD

        self.explanation_card = QGraphicsRectItem(self)
        self.explanation_card.setRect(0, 0, 280, 60)
        self.explanation_card.setBrush(QBrush(QColor("#202B3A")))
        self.explanation_card.setPen(QPen(QColor("#60A5FA"), 1.5))
        self.explanation_card.setPos(0, self.HEIGHT + 12)
        self.explanation_card.setZValue(10)

        self.explanation_text = QGraphicsTextItem(
            self.explanation_card
        )

        self.explanation_text.setDefaultTextColor(
            QColor("#E5E7EB")
        )

        self.explanation_text.setFont(QFont("Segoe UI", 9))
        self.explanation_text.setTextWidth(256)
        self.explanation_text.setPos(12, 9)

        self.explanation_card.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self.explanation_card.setFlag(
            QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable,
            False
        )

        self.explanation_text.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self.explanation_card.setVisible(False)

        self.input_port = None
        self.output_port = None
        self.true_port = None
        self.false_port = None

        if node_type != "START":
            self.input_port = PortItem(self, "input")
            self.input_port.setPos(0, self.HEIGHT / 2)

        if node_type == "CONDITION":
            self.true_port = PortItem(self, "true")
            self.false_port = PortItem(self, "false")

            self.true_port.setPos(self.WIDTH, 29)
            self.false_port.setPos(self.WIDTH, 69)

            self.output_port = self.true_port

            true_label = QGraphicsTextItem("TRUE", self)
            true_label.setDefaultTextColor(QColor("#34D399"))
            true_label.setFont(
                QFont("Segoe UI", 8, QFont.Weight.Bold)
            )
            true_label.setPos(140, 15)

            false_label = QGraphicsTextItem("FALSE", self)
            false_label.setDefaultTextColor(QColor("#F87171"))
            false_label.setFont(
                QFont("Segoe UI", 8, QFont.Weight.Bold)
            )
            false_label.setPos(140, 55)

        elif node_type != "END":
            self.output_port = PortItem(self, "output")
            self.output_port.setPos(self.WIDTH, self.HEIGHT / 2)

    # ----------------------------------
    # EXECUTION EXPLANATION
    # ----------------------------------

    def set_execution_explanation(self, message, kind="info"):

        colors = {
            "info": ("#202B3A", "#60A5FA"),
            "success": ("#1D352B", "#34D399"),
            "warning": ("#3A3020", "#FBBF24"),
            "error": ("#3A2225", "#F87171"),
        }

        background, border = colors.get(kind, colors["info"])

        self.explanation_text.setPlainText(str(message))

        text_height = self.explanation_text.boundingRect().height()
        card_height = max(48, text_height + 18)

        self.explanation_card.setRect(
            0, 0, 280, card_height
        )

        self.explanation_card.setBrush(
            QBrush(QColor(background))
        )

        self.explanation_card.setPen(
            QPen(QColor(border), 1.5)
        )

        # Bring the complete node and its explanation above
        # neighbouring nodes while debugging.
        self.setZValue(self.ACTIVE_Z_VALUE)

        self.explanation_card.setVisible(True)

    def clear_execution_explanation(self):

        self.explanation_card.setVisible(False)
        self.explanation_text.setPlainText("")

        # Restore the normal drawing order.
        self.setZValue(self.NORMAL_Z_VALUE)

    def get_output_port(self, port_type="output"):

        if self.node_type == "CONDITION":

            if port_type == "true":
                return self.true_port

            if port_type == "false":
                return self.false_port

            raise ValueError(
                "CONDITION nodes require a TRUE or FALSE output."
            )

        return self.output_port

    # ----------------------------------
    # MOVE HISTORY
    # ----------------------------------

    def mousePressEvent(self, event):
        self._history_start_pos = QPointF(self.pos())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self._history_start_pos is not None:
            moved = self.pos() != self._history_start_pos

            if moved and self.scene():
                editor = self.scene().editor

                if editor:
                    editor.record_history("Move node")

        self._history_start_pos = None

    def itemChange(self, change, value):

        if (
            change
            == QGraphicsRectItem.GraphicsItemChange.ItemPositionHasChanged
        ):
            for connection in self.connections:
                connection.update_position()

        return super().itemChange(change, value)

    # ----------------------------------
    # CONTEXT MENU
    # ----------------------------------

    def contextMenuEvent(self, event):

        menu = QMenu()

        rename_action = menu.addAction("Rename")
        duplicate_action = menu.addAction("Duplicate")

        menu.addSeparator()

        delete_action = menu.addAction("Delete")

        action = menu.exec(event.screenPos())
        scene = self.scene()

        if scene is None:
            return

        if action == rename_action:
            scene.rename_node(self)

        elif action == duplicate_action:
            scene.duplicate_node(self)

        elif action == delete_action:
            scene.delete_node(self)

        event.accept()


# ==================================
# GRAPH SCENE
# ==================================

class GraphScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.connections = []
        self.pending_source = None
        self.preview_connection = None
        self.editor = None

    def start_connection(self, port):

        if port.port_type == "input":
            return

        self.cancel_connection()

        self.pending_source = port
        self.preview_connection = QGraphicsPathItem()

        pen = QPen(QColor("#FBBF24"), 2.5)
        pen.setStyle(Qt.PenStyle.DashLine)

        self.preview_connection.setPen(pen)
        self.preview_connection.setZValue(2)

        self.addItem(self.preview_connection)

        self.update_connection(
            port.mapToScene(QPointF(0, 0))
        )

    def update_connection(self, end):

        if self.pending_source is None:
            return

        start = self.pending_source.mapToScene(QPointF(0, 0))
        path = QPainterPath(start)

        distance = max(60, abs(end.x() - start.x()) * 0.5)

        path.cubicTo(
            QPointF(start.x() + distance, start.y()),
            QPointF(end.x() - distance, end.y()),
            end
        )

        if self.preview_connection:
            self.preview_connection.setPath(path)

    def finish_connection(self, scene_pos):

        if self.pending_source is None:
            return

        source_port = self.pending_source
        source = source_port.node
        source_type = source_port.port_type

        target_port = None

        for item in self.items(scene_pos):

            if (
                isinstance(item, PortItem)
                and item.port_type == "input"
            ):
                target_port = item
                break

        self.cancel_connection()

        if target_port is None:
            return

        target = target_port.node

        if source == target:
            return

        if source.node_type not in ("CONDITION", "INPUT"):

            if any(
                c.source_node == source
                for c in self.connections
            ):
                return

        elif source.node_type == "CONDITION":

            if any(
                c.source_node == source
                and c.source_port_type == source_type
                for c in self.connections
            ):
                return

        if any(
            c.source_node == source
            and c.target_node == target
            and c.source_port_type == source_type
            for c in self.connections
        ):
            return

        connection = ConnectionItem(source, target, source_type)

        self.addItem(connection)
        self.connections.append(connection)

        source.connections.append(connection)
        target.connections.append(connection)

        if self.editor:
            self.editor.record_history("Create connection")

    def cancel_connection(self):

        self.pending_source = None

        if self.preview_connection is not None:
            self.removeItem(self.preview_connection)
            self.preview_connection = None

    # ----------------------------------
    # RENAME
    # ----------------------------------

    def rename_node(self, node):

        name, accepted = QInputDialog.getText(
            self.editor,
            "Rename Node",
            "Enter node name:",
            text=node.node_name
        )

        if accepted and name.strip():

            new_name = name.strip()

            if new_name == node.node_name:
                return

            node.node_name = new_name
            node.title.setPlainText(node.node_name)

            if self.editor:
                self.editor.record_history(
                    "Rename node",
                    merge_key=None
                )
                self.editor.node_selected.emit(node)

    # ----------------------------------
    # DUPLICATE
    # ----------------------------------

    def duplicate_node(self, node):

        self.editor.add_node(
            node.node_type,
            position=node.pos() + QPointF(35, 35),
            name=f"{node.node_name} Copy"
        )

    # ----------------------------------
    # DELETE HELPERS
    # ----------------------------------

    def _delete_connection(self, connection):

        if connection not in self.connections:
            return

        self.connections.remove(connection)

        if connection in connection.source_node.connections:
            connection.source_node.connections.remove(connection)

        if connection in connection.target_node.connections:
            connection.target_node.connections.remove(connection)

        self.removeItem(connection)

    def delete_connection(self, connection):

        if connection not in self.connections:
            return

        self._delete_connection(connection)

        if self.editor:
            self.editor.record_history("Delete connection")

    def _delete_node(self, node):

        if node.scene() != self:
            return

        for connection in list(node.connections):
            self._delete_connection(connection)

        self.removeItem(node)

    def delete_node(self, node):

        if node.scene() != self:
            return

        self._delete_node(node)

        if self.editor:
            self.editor.record_history("Delete node")
            self.editor.emit_selected_node()

    def delete_selected(self):

        selected = list(self.selectedItems())

        nodes = [
            item for item in selected
            if isinstance(item, NodeItem)
        ]

        connections = [
            item for item in selected
            if isinstance(item, ConnectionItem)
        ]

        if not nodes and not connections:
            return

        for node in nodes:
            self._delete_node(node)

        for connection in connections:
            self._delete_connection(connection)

        if self.editor:
            self.editor.record_history("Delete selected")
            self.editor.emit_selected_node()

    def keyPressEvent(self, event):

        if event.key() in (
            Qt.Key.Key_Delete,
            Qt.Key.Key_Backspace
        ):
            self.delete_selected()
            event.accept()
            return

        super().keyPressEvent(event)


# ==================================
# CANVAS VIEW WITH ZOOM
# ==================================

class CanvasView(QGraphicsView):

    zoom_changed = Signal(float)

    MIN_ZOOM = 0.35
    MAX_ZOOM = 2.5
    ZOOM_STEP = 1.15

    def __init__(self, scene):
        super().__init__(scene)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QColor("#111318"))

        self.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )

        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setMinimumWidth(400)

    def zoom_by(self, factor):

        current_zoom = self.transform().m11()
        new_zoom = current_zoom * factor

        new_zoom = max(
            self.MIN_ZOOM,
            min(self.MAX_ZOOM, new_zoom)
        )

        actual_factor = new_zoom / current_zoom

        self.scale(actual_factor, actual_factor)
        self.zoom_changed.emit(new_zoom)

    def reset_zoom(self):

        self.resetTransform()
        self.zoom_changed.emit(1.0)

    def wheelEvent(self, event):

        if (
            event.modifiers()
            & Qt.KeyboardModifier.ControlModifier
        ):
            delta = event.angleDelta().y()

            if delta > 0:
                self.zoom_by(self.ZOOM_STEP)

            elif delta < 0:
                self.zoom_by(1 / self.ZOOM_STEP)

            event.accept()
            return

        super().wheelEvent(event)

    def drawBackground(self, painter, rect):

        super().drawBackground(painter, rect)

        grid_size = 25

        left = (
            int(rect.left())
            - int(rect.left()) % grid_size
        )

        top = (
            int(rect.top())
            - int(rect.top()) % grid_size
        )

        painter.setPen(QPen(QColor("#252A34"), 1))

        x = left

        while x < rect.right():

            painter.drawLine(
                x,
                int(rect.top()),
                x,
                int(rect.bottom())
            )

            x += grid_size

        y = top

        while y < rect.bottom():

            painter.drawLine(
                int(rect.left()),
                y,
                int(rect.right()),
                y
            )

            y += grid_size


# ==================================
# NODE EDITOR
# ==================================

class NodeEditor(QWidget):

    node_selected = Signal(object)

    def __init__(self):
        super().__init__()

        self.node_counter = 0
        self._restoring_history = False

        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(100)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(5)

        for node_type in [
            "START",
            "INPUT",
            "OPERATION",
            "CONDITION",
            "OUTPUT",
            "END"
        ]:

            button = QPushButton(f"+ {node_type.title()}")

            button.clicked.connect(
                lambda checked=False, t=node_type:
                self.add_node(t)
            )

            toolbar.addWidget(button)

        self.layout.addLayout(toolbar)

        self.scene = GraphScene(self)
        self.scene.editor = self

        self.scene.setSceneRect(
            -1000, -1000, 3000, 3000
        )

        self.scene.selectionChanged.connect(
            self.emit_selected_node
        )

        self.view = CanvasView(self.scene)

        self.view.setStyleSheet("""
            QGraphicsView {
                border: 1px solid #292D36;
                border-radius: 8px;
            }
        """)

        self.view.zoom_changed.connect(
            self.update_zoom_label
        )

        self.layout.addWidget(self.view, 1)

        zoom_toolbar = QHBoxLayout()
        zoom_toolbar.setSpacing(6)
        zoom_toolbar.addStretch()

        zoom_out_button = QPushButton("−")
        zoom_out_button.setToolTip("Zoom out")
        zoom_out_button.setFixedSize(38, 34)

        zoom_in_button = QPushButton("+")
        zoom_in_button.setToolTip("Zoom in")
        zoom_in_button.setFixedSize(38, 34)

        reset_button = QPushButton("100%")
        reset_button.setToolTip("Reset zoom")
        reset_button.setFixedHeight(34)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet(
            "color: #9CA3AF; padding: 5px;"
        )

        zoom_out_button.clicked.connect(
            lambda: self.view.zoom_by(
                1 / self.view.ZOOM_STEP
            )
        )

        zoom_in_button.clicked.connect(
            lambda: self.view.zoom_by(
                self.view.ZOOM_STEP
            )
        )

        reset_button.clicked.connect(self.view.reset_zoom)

        zoom_toolbar.addWidget(zoom_out_button)
        zoom_toolbar.addWidget(self.zoom_label)
        zoom_toolbar.addWidget(zoom_in_button)
        zoom_toolbar.addWidget(reset_button)

        self.layout.addLayout(zoom_toolbar)

        self._last_snapshot = self.capture_snapshot()

    # ----------------------------------
    # SNAPSHOT SYSTEM
    # ----------------------------------

    def capture_snapshot(self):

        nodes = []

        for item in self.scene.items():

            if not isinstance(item, NodeItem):
                continue

            nodes.append({
                "node_id": item.node_id,
                "node_type": item.node_type,
                "node_name": item.node_name,
                "settings": copy.deepcopy(item.settings),
                "x": item.pos().x(),
                "y": item.pos().y(),
            })

        connections = []

        for connection in self.scene.connections:

            connections.append({
                "source_id": connection.source_node.node_id,
                "target_id": connection.target_node.node_id,
                "source_port": connection.source_port_type,
            })

        nodes.sort(key=lambda n: str(n["node_id"]))

        connections.sort(
            key=lambda c: (
                str(c["source_id"]),
                str(c["target_id"]),
                c["source_port"]
            )
        )

        return {
            "node_counter": self.node_counter,
            "nodes": nodes,
            "connections": connections,
        }

    def record_history(self, description="Edit graph", merge_key=None):

        if self._restoring_history:
            return

        new_snapshot = self.capture_snapshot()

        if new_snapshot == self._last_snapshot:
            return

        command = GraphSnapshotCommand(
            self,
            self._last_snapshot,
            new_snapshot,
            description,
            merge_key
        )

        self._last_snapshot = copy.deepcopy(new_snapshot)

        self.undo_stack.push(command)

    def restore_snapshot(self, snapshot):

        self._restoring_history = True

        try:

            self.scene.cancel_connection()
            self.scene.clear()
            self.scene.connections.clear()

            node_map = {}

            for data in snapshot["nodes"]:

                node = NodeItem(
                    data["node_type"],
                    data["node_id"],
                    data["node_name"]
                )

                node.settings = copy.deepcopy(data["settings"])

                self.scene.addItem(node)

                node.setPos(
                    QPointF(data["x"], data["y"])
                )

                node_map[node.node_id] = node

            for data in snapshot["connections"]:

                source = node_map.get(data["source_id"])
                target = node_map.get(data["target_id"])

                if source is None or target is None:
                    continue

                connection = ConnectionItem(
                    source,
                    target,
                    data["source_port"]
                )

                self.scene.addItem(connection)
                self.scene.connections.append(connection)

                source.connections.append(connection)
                target.connections.append(connection)

            self.node_counter = snapshot["node_counter"]

            self.scene.clearSelection()

            self._last_snapshot = copy.deepcopy(snapshot)

        finally:
            self._restoring_history = False

        self.emit_selected_node()

    def reset_history(self):

        self.undo_stack.clear()
        self._last_snapshot = self.capture_snapshot()

    # ----------------------------------
    # ZOOM
    # ----------------------------------

    def update_zoom_label(self, zoom):

        self.zoom_label.setText(
            f"{round(zoom * 100)}%"
        )

    # ----------------------------------
    # SELECTION
    # ----------------------------------

    def emit_selected_node(self):

        selected_nodes = [
            item for item in self.scene.selectedItems()
            if isinstance(item, NodeItem)
        ]

        self.node_selected.emit(
            selected_nodes[0] if selected_nodes else None
        )

    # ----------------------------------
    # ADD NODE
    # ----------------------------------

    def add_node(self, node_type, position=None, name=None):

        self.node_counter += 1

        node = NodeItem(
            node_type,
            self.node_counter,
            name
        )

        self.scene.addItem(node)

        if position is None:

            x = (
                100
                + ((self.node_counter - 1) % 3) * 240
            )

            y = (
                100
                + ((self.node_counter - 1) // 3) * 150
            )

            position = QPointF(x, y)

        node.setPos(position)

        self.scene.clearSelection()
        node.setSelected(True)

        self.node_selected.emit(node)

        self.record_history("Add node")

        return node
