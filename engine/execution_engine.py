
from dataclasses import dataclass
from typing import Any
import re


@dataclass
class ExecutionResult:
    success: bool
    message: str
    current_node: Any = None
    finished: bool = False
    error: bool = False


class ExecutionEngine:

    VARIABLE_PATTERN = re.compile(r"\{([^{}]+)\}")

    def __init__(self, nodes, connections, max_steps=1000):
        self.nodes = nodes
        self.connections = connections
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        self.variables = {}
        self.current_node = None
        self.finished = False
        self.stopped = False
        self.failed = False
        self.last_output = ""
        self.step_count = 0
        self._next_branch = None

    def _get_node_type(self, node):
        return getattr(node, "node_type", None)

    def _get_setting(self, node, key, default=None):
        settings = getattr(node, "settings", {}) or {}
        return settings.get(key, default)

    def _get_start_nodes(self):
        return [
            node for node in self.nodes
            if self._get_node_type(node) == "START"
        ]

    def _fail(self, message):
        self.failed = True
        self.finished = True

        return ExecutionResult(
            False,
            message,
            self.current_node,
            True,
            True
        )

    def get_variable_name(self, reference):
        name = str(reference).strip()

        if name.startswith("{") and name.endswith("}"):
            name = name[1:-1].strip()

        if not name:
            raise ValueError("Variable name cannot be empty.")

        if "{" in name or "}" in name:
            raise ValueError("Invalid variable reference.")

        return name

    def _validate_declaration_name(self, name, setting_name):
        name = str(name).strip()

        if not name:
            raise ValueError(
                f"{setting_name} cannot be empty."
            )

        if "{" in name or "}" in name:
            raise ValueError(
                f"{setting_name} must be a plain variable name."
            )

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(
                f"'{name}' is not a valid variable name. "
                "Use letters, numbers and underscores, "
                "and do not start with a number."
            )

        return name

    def resolve_value(self, value):
        if not isinstance(value, str):
            return value

        stripped = value.strip()

        exact_match = re.fullmatch(r"\{([^{}]+)\}", stripped)

        if exact_match:
            name = exact_match.group(1).strip()

            if not name:
                raise ValueError("Variable reference cannot be empty.")

            if name not in self.variables:
                raise ValueError(
                    f"Variable '{name}' has not been defined."
                )

            return self.variables[name]

        def replace(match):
            name = match.group(1).strip()

            if not name:
                raise ValueError("Empty variable reference found.")

            if name not in self.variables:
                raise ValueError(
                    f"Variable '{name}' has not been defined."
                )

            return str(self.variables[name])

        result = self.VARIABLE_PATTERN.sub(replace, value)

        if "{" in result or "}" in result:
            raise ValueError(
                "Invalid variable brackets. Use {variable_name}."
            )

        return result

    def build_output_message(self, message):
        if not isinstance(message, str):
            raise ValueError("Output message must be text.")

        return str(self.resolve_value(message))

    def _get_connection_branch(self, connection):
        branch = getattr(
            connection,
            "source_port_type",
            getattr(connection, "branch", "output")
        )

        return str(branch).strip().lower()

    def get_next_node(self, current_node, branch=None):
        outgoing = [
            connection for connection in self.connections
            if getattr(connection, "source_node", None) == current_node
        ]

        if self._get_node_type(current_node) == "CONDITION":

            if branch not in ("true", "false"):
                raise ValueError(
                    "A CONDITION node requires a TRUE or FALSE result."
                )

            matching = [
                connection for connection in outgoing
                if self._get_connection_branch(connection) == branch
            ]

            if len(matching) != 1:
                raise ValueError(
                    f"CONDITION node must have exactly one "
                    f"{branch.upper()} connection."
                )

            return matching[0].target_node

        if len(outgoing) == 0:
            raise ValueError(
                f"No outgoing connection from "
                f"{self._get_node_type(current_node)} node."
            )

        if len(outgoing) > 1:
            raise ValueError(
                f"{self._get_node_type(current_node)} node "
                "has multiple outgoing connections."
            )

        return outgoing[0].target_node

    @staticmethod
    def get_number(value):
        try:
            number = float(value)

            if number != number or number in (
                float("inf"),
                float("-inf")
            ):
                raise ValueError

            return number

        except (ValueError, TypeError, OverflowError):
            raise ValueError(f"'{value}' is not a valid number.")

    @staticmethod
    def format_number(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)

    def resolve_numeric_operand(self, expression):
        """
        Resolves either:
        - A variable reference such as {num1}
        - A numeric literal such as 10 or 5.5

        Numeric input values are converted only when used
        in mathematical operations.
        """

        if expression is None:
            raise ValueError("An operand cannot be empty.")

        expression = str(expression).strip()

        if not expression:
            raise ValueError("An operand cannot be empty.")

        exact_match = re.fullmatch(
            r"\{([^{}]+)\}",
            expression
        )

        if exact_match:
            variable_name = exact_match.group(1).strip()

            if not variable_name:
                raise ValueError("Variable reference cannot be empty.")

            if variable_name not in self.variables:
                raise ValueError(
                    f"Variable '{variable_name}' has not been defined."
                )

            value = self.variables[variable_name]
            return self.get_number(value)

        if "{" in expression or "}" in expression:
            raise ValueError(
                f"Invalid operand '{expression}'. "
                "Use a number or a variable reference like {num1}."
            )

        return self.get_number(expression)

    def start(self):
        self.reset()

        start_nodes = self._get_start_nodes()

        if len(start_nodes) == 0:
            return self._fail("No START node found.")

        if len(start_nodes) > 1:
            return self._fail(
                "Multiple START nodes found. "
                "A program must have exactly one START node."
            )

        self.current_node = start_nodes[0]

        return ExecutionResult(
            True,
            "Program execution started.",
            self.current_node
        )

    def execute_input(self, node, input_provider):
        question = self._get_setting(
            node,
            "question",
            "Enter a value:"
        )

        variable = self._validate_declaration_name(
            self._get_setting(node, "variable", ""),
            "INPUT variable"
        )

        if input_provider is None:
            raise ValueError("No input provider was supplied.")

        question = self.resolve_value(str(question))
        value = input_provider(str(question))

        if value is None:
            raise ValueError("Input was cancelled.")

        self.variables[variable] = value

        return f"Stored input in variable '{variable}'."

    def execute_mathematical_operation(self, node):
        operation = str(
            self._get_setting(node, "operation", "Add")
        ).strip()

        first_expression = self._get_setting(
            node,
            "first_variable",
            ""
        )

        second_expression = self._get_setting(
            node,
            "second_variable",
            ""
        )

        result_variable = self._validate_declaration_name(
            self._get_setting(node, "result_variable", ""),
            "Result variable"
        )

        first_value = self.resolve_numeric_operand(
            first_expression
        )

        second_value = self.resolve_numeric_operand(
            second_expression
        )

        if operation == "Add":
            result = first_value + second_value
            symbol = "+"

        elif operation == "Subtract":
            result = first_value - second_value
            symbol = "-"

        elif operation == "Multiply":
            result = first_value * second_value
            symbol = "*"

        elif operation == "Divide":
            if second_value == 0:
                raise ValueError(
                    "Cannot divide by zero. "
                    "Please use a non-zero divisor."
                )

            result = first_value / second_value
            symbol = "/"

        else:
            raise ValueError(
                f"Unknown mathematical operation: '{operation}'."
            )

        self.variables[result_variable] = result

        return (
            f"{result_variable} = "
            f"{self.format_number(first_value)} "
            f"{symbol} "
            f"{self.format_number(second_value)} "
            f"= {self.format_number(result)}"
        )

    def execute_operation(self, node):

        # NEW MATHEMATICAL OPERATION FORMAT
        settings = getattr(node, "settings", {}) or {}

        if "operation" in settings:
            return self.execute_mathematical_operation(node)

        # LEGACY OPERATION FORMAT
        action = self._get_setting(
            node,
            "action",
            "Set a value"
        )

        variable = self._validate_declaration_name(
            self._get_setting(node, "variable", ""),
            "Operation variable"
        )

        value = self._get_setting(node, "value", "0")
        amount = self._get_setting(node, "amount", "1")

        if action == "Set a value":

            resolved_value = self.resolve_value(value)

            try:
                resolved_value = self.get_number(resolved_value)
            except ValueError:
                pass

            self.variables[variable] = resolved_value

            return (
                f"Set {variable} = "
                f"{self.format_number(resolved_value)}"
            )

        arithmetic_actions = (
            "Increase a value",
            "Decrease a value",
            "Multiply a value",
            "Divide a value",
        )

        if action in arithmetic_actions:

            if variable not in self.variables:
                raise ValueError(
                    f"Variable '{variable}' has not been defined."
                )

            current = self.get_number(
                self.variables[variable]
            )

            resolved_amount = self.resolve_value(amount)
            change = self.get_number(resolved_amount)

            if action == "Increase a value":
                result = current + change
                action_message = "Increased"

            elif action == "Decrease a value":
                result = current - change
                action_message = "Decreased"

            elif action == "Multiply a value":
                result = current * change
                action_message = "Multiplied"

            else:
                if change == 0:
                    raise ValueError(
                        "Cannot divide by zero. "
                        "Please use a non-zero divisor."
                    )

                result = current / change
                action_message = "Divided"

            self.variables[variable] = result

            return (
                f"{action_message} {variable} "
                f"to {self.format_number(result)}."
            )

        raise ValueError(f"Unknown operation: '{action}'.")

    def execute_condition(self, node):
        variable = self.get_variable_name(
            self._get_setting(node, "variable", "")
        )

        comparison = str(
            self._get_setting(node, "comparison", "Equal to")
        ).strip().lower()

        compare_value = self._get_setting(
            node,
            "compare_value",
            ""
        )

        if variable not in self.variables:
            raise ValueError(
                f"Variable '{variable}' has not been defined."
            )

        actual_value = self.variables[variable]
        compare_value = self.resolve_value(compare_value)

        aliases = {
            "equal to": "==",
            "equals": "==",
            "equal": "==",
            "==": "==",
            "not equal to": "!=",
            "not equal": "!=",
            "!=": "!=",
            "greater than": ">",
            ">": ">",
            "less than": "<",
            "<": "<",
            "greater than or equal to": ">=",
            "greater than or equal": ">=",
            ">=": ">=",
            "less than or equal to": "<=",
            "less than or equal": "<=",
            "<=": "<=",
        }

        operator = aliases.get(comparison)

        if operator is None:
            raise ValueError(
                f"Unsupported comparison operator: '{comparison}'."
            )

        try:
            left = self.get_number(actual_value)
            right = self.get_number(compare_value)

        except ValueError:
            if operator not in ("==", "!="):
                raise ValueError(
                    f"Comparison '{operator}' requires numeric values."
                )

            left = str(actual_value).strip()
            right = str(compare_value).strip()

        if operator == "==":
            result = left == right

        elif operator == "!=":
            result = left != right

        elif operator == ">":
            result = left > right

        elif operator == "<":
            result = left < right

        elif operator == ">=":
            result = left >= right

        else:
            result = left <= right

        self._next_branch = (
            "true" if result else "false"
        )

        return result

    def step(self, input_provider=None):

        if self.failed:
            return ExecutionResult(
                False,
                "Execution has failed.",
                self.current_node,
                True,
                True
            )

        if self.stopped:
            return ExecutionResult(
                False,
                "Execution was stopped.",
                self.current_node,
                True
            )

        if self.finished:
            return ExecutionResult(
                True,
                "Program has already finished.",
                self.current_node,
                True
            )

        if self.current_node is None:
            return self._fail(
                "Execution has not been started. Call start() first."
            )

        if self.step_count >= self.max_steps:
            return self._fail(
                f"Maximum execution limit of {self.max_steps} "
                "steps reached. Check for an infinite loop."
            )

        node = self.current_node
        node_type = self._get_node_type(node)

        self.step_count += 1
        self._next_branch = None

        try:

            if node_type == "START":
                message = "Starting program execution."

            elif node_type == "INPUT":
                message = self.execute_input(
                    node,
                    input_provider
                )

            elif node_type == "OPERATION":
                message = self.execute_operation(node)

            elif node_type == "OUTPUT":
                output_text = self._get_setting(
                    node,
                    "message",
                    ""
                )

                message = self.build_output_message(
                    output_text
                )

                self.last_output = message

            elif node_type == "CONDITION":
                result = self.execute_condition(node)
                branch = self._next_branch

                message = (
                    f"Condition evaluated to {result}. "
                    f"Following the {branch.upper()} branch."
                )

            elif node_type == "END":
                self.finished = True

                return ExecutionResult(
                    True,
                    "Program execution completed.",
                    node,
                    True
                )

            else:
                raise ValueError(
                    f"Unknown node type: '{node_type}'."
                )

            if node_type == "CONDITION":
                self.current_node = self.get_next_node(
                    node,
                    self._next_branch
                )

            else:
                self.current_node = self.get_next_node(node)

            return ExecutionResult(
                True,
                message,
                node,
                False
            )

        except Exception as error:
            return self._fail(str(error))

    def stop(self):
        self.stopped = True

        return ExecutionResult(
            False,
            "Program execution stopped.",
            self.current_node,
            True
        )
