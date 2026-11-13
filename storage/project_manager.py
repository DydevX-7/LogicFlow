
import json
from pathlib import Path

from PySide6.QtCore import QPointF

from ui.editor import NodeItem, ConnectionItem
from storage.account_storage import get_account_storage_directory


class ProjectManager:

    FORMAT_VERSION = 1

    VALID_NODE_TYPES = {
        "START",
        "INPUT",
        "OPERATION",
        "CONDITION",
        "OUTPUT",
        "END",
    }

    def __init__(self, username=None):

        if username:
            account_directory = get_account_storage_directory(username)
            self.projects_directory = account_directory / "projects"
        else:
            self.projects_directory = (
                Path(__file__).resolve().parent / "projects"
            )

        self.projects_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================
    # SERIALIZE PROJECT
    # ==================================

    def serialize_project(self, scene, node_counter):

        nodes = []
        connections = []

        node_items = [
            item
            for item in scene.items()
            if isinstance(item, NodeItem)
        ]

        node_ids = set()

        for node in node_items:

            if node.node_id in node_ids:
                raise ValueError(
                    f"Duplicate node ID: {node.node_id}"
                )

            node_ids.add(node.node_id)

            position = node.pos()

            nodes.append({
                "id": node.node_id,
                "type": node.node_type,
                "name": node.node_name,
                "x": position.x(),
                "y": position.y(),
                "settings": node.settings,
            })

        for connection in scene.connections:

            connections.append({
                "source": connection.source_node.node_id,
                "target": connection.target_node.node_id,
                "source_port": connection.source_port_type,
            })

        return {
            "format_version": self.FORMAT_VERSION,
            "application": "LogicFlow",
            "node_counter": node_counter,
            "nodes": nodes,
            "connections": connections,
        }

    # ==================================
    # VALIDATE PROJECT DATA
    # ==================================

    def validate_project_data(self, data):

        if not isinstance(data, dict):
            raise ValueError("Invalid project format.")

        if data.get("application") != "LogicFlow":
            raise ValueError("This is not a LogicFlow project.")

        if data.get("format_version") != self.FORMAT_VERSION:
            raise ValueError(
                "Unsupported project file version."
            )

        nodes = data.get("nodes")
        connections = data.get("connections")

        if not isinstance(nodes, list):
            raise ValueError("Invalid nodes data.")

        if not isinstance(connections, list):
            raise ValueError("Invalid connections data.")

        node_map = {}

        for node_data in nodes:

            if not isinstance(node_data, dict):
                raise ValueError("Invalid node data.")

            node_id = node_data.get("id")
            node_type = node_data.get("type")

            if (
                not isinstance(node_id, int)
                or isinstance(node_id, bool)
                or node_id < 1
            ):
                raise ValueError("Invalid node ID.")

            if node_id in node_map:
                raise ValueError("Duplicate node ID found.")

            if node_type not in self.VALID_NODE_TYPES:
                raise ValueError("Unknown node type.")

            if not isinstance(node_data.get("name"), str):
                raise ValueError("Invalid node name.")

            if not isinstance(node_data.get("settings"), dict):
                raise ValueError("Invalid node settings.")

            for coordinate in ("x", "y"):

                value = node_data.get(coordinate)

                if (
                    not isinstance(value, (int, float))
                    or isinstance(value, bool)
                ):
                    raise ValueError("Invalid node position.")

            node_map[node_id] = node_data

        outgoing = set()
        existing_connections = set()

        for connection_data in connections:

            if not isinstance(connection_data, dict):
                raise ValueError("Invalid connection data.")

            source_id = connection_data.get("source")
            target_id = connection_data.get("target")
            source_port = connection_data.get("source_port")

            if (
                source_id not in node_map
                or target_id not in node_map
            ):
                raise ValueError(
                    "A connection refers to a missing node."
                )

            source_type = node_map[source_id]["type"]
            target_type = node_map[target_id]["type"]

            if source_id == target_id:
                raise ValueError(
                    "Connections cannot connect a node to itself."
                )

            if source_type == "END":
                raise ValueError(
                    "END nodes cannot have outgoing connections."
                )

            if target_type == "START":
                raise ValueError(
                    "START nodes cannot have incoming connections."
                )

            if source_type == "CONDITION":

                if source_port not in ("true", "false"):
                    raise ValueError(
                        "Invalid CONDITION output port."
                    )

            elif source_port != "output":
                raise ValueError(
                    "Invalid output port."
                )

            connection_key = (
                source_id,
                target_id,
                source_port
            )

            if connection_key in existing_connections:
                raise ValueError(
                    "Duplicate connection found."
                )

            existing_connections.add(connection_key)

            outgoing_key = (source_id, source_port)

            if outgoing_key in outgoing:
                raise ValueError(
                    "Multiple connections use the same output port."
                )

            outgoing.add(outgoing_key)

        return node_map

    # ==================================
    # SAVE PROJECT
    # ==================================

    def save_project(self, file_path, scene, node_counter):

        file_path = Path(file_path)

        if file_path.suffix.lower() != ".logicflow":
            file_path = file_path.with_suffix(".logicflow")

        project_data = self.serialize_project(
            scene,
            node_counter
        )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        temporary_path = file_path.with_name(
            file_path.name + ".tmp"
        )

        try:

            with temporary_path.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    project_data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                    allow_nan=False
                )

            temporary_path.replace(file_path)

        except Exception:

            if temporary_path.exists():
                temporary_path.unlink()

            raise

        return file_path

    # ==================================
    # LOAD PROJECT
    # ==================================

    def load_project(self, file_path, scene, editor):

        file_path = Path(file_path)

        with file_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        node_map = self.validate_project_data(data)

        new_nodes = {}
        new_connections = []

        for node_data in data["nodes"]:

            node = NodeItem(
                node_data["type"],
                node_data["id"],
                node_data["name"]
            )

            node.settings = node_data["settings"].copy()

            node.setPos(
                QPointF(
                    node_data["x"],
                    node_data["y"]
                )
            )

            new_nodes[node.node_id] = node

        for connection_data in data["connections"]:

            source = new_nodes[
                connection_data["source"]
            ]

            target = new_nodes[
                connection_data["target"]
            ]

            connection = ConnectionItem(
                source,
                target,
                connection_data["source_port"]
            )

            new_connections.append(connection)

        # Replace the previous graph only after reconstruction succeeds.
        scene.cancel_connection()

        scene.clear()
        scene.connections.clear()

        for node in new_nodes.values():
            scene.addItem(node)

        for connection in new_connections:

            scene.addItem(connection)
            scene.connections.append(connection)

            connection.source_node.connections.append(
                connection
            )

            connection.target_node.connections.append(
                connection
            )

        scene.clearSelection()

        max_id = max(new_nodes.keys(), default=0)

        saved_counter = data.get("node_counter", 0)

        if (
            not isinstance(saved_counter, int)
            or isinstance(saved_counter, bool)
            or saved_counter < 0
        ):
            saved_counter = 0

        editor.node_counter = max(
            max_id,
            saved_counter
        )

        if hasattr(editor, "emit_selected_node"):
            editor.emit_selected_node()

        return editor.node_counter
