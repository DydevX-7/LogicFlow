
from contextlib import redirect_stdout
from io import StringIO

from engine.code_generator import CodeGenerator


# --------------------------------------------------
# FAKE NODES
# --------------------------------------------------

class FakeNode:

    def __init__(self, node_id, node_type, node_name, settings=None):
        self.node_id = node_id
        self.node_type = node_type
        self.node_name = node_name
        self.settings = settings or {}


class FakeConnection:

    def __init__(self, source_node, target_node, branch="output"):
        self.source_node = source_node
        self.target_node = target_node
        self.source_port_type = branch


# --------------------------------------------------
# CREATE FLOWCHART
# --------------------------------------------------

start = FakeNode(1, "START", "Start")

operation = FakeNode(
    2,
    "OPERATION",
    "Set Score",
    {
        "action": "Set a value",
        "variable": "score",
        "value": "15"
    }
)

condition = FakeNode(
    3,
    "CONDITION",
    "Check Score",
    {
        "variable": "score",
        "comparison": "Greater than",
        "compare_value": "10"
    }
)

true_output = FakeNode(
    4,
    "OUTPUT",
    "Passed",
    {
        "message": "Passed!"
    }
)

false_output = FakeNode(
    5,
    "OUTPUT",
    "Not Passed",
    {
        "message": "Not passed!"
    }
)

end = FakeNode(6, "END", "End")


nodes = [
    start,
    operation,
    condition,
    true_output,
    false_output,
    end
]


connections = [
    FakeConnection(start, operation),
    FakeConnection(operation, condition),

    FakeConnection(condition, true_output, "true"),
    FakeConnection(condition, false_output, "false"),

    FakeConnection(true_output, end),
    FakeConnection(false_output, end)
]


# --------------------------------------------------
# GENERATE PYTHON
# --------------------------------------------------

print("\n1. Generating conditional Python code...")

generator = CodeGenerator(nodes, connections)

program = generator.generate()

print("SUCCESS: Code generated!")


# --------------------------------------------------
# DISPLAY CODE
# --------------------------------------------------

print("\n2. Generated Python:")
print("-" * 40)
print(program.code)
print("-" * 40)


# --------------------------------------------------
# CHECK SYNTAX
# --------------------------------------------------

print("\n3. Checking Python syntax...")

compiled_code = compile(
    program.code,
    "<LogicFlow Conditional Test>",
    "exec"
)

print("SUCCESS: Syntax is valid!")


# --------------------------------------------------
# TEST TRUE BRANCH
# --------------------------------------------------

print("\n4. Testing TRUE branch...")

true_output_capture = StringIO()

with redirect_stdout(true_output_capture):
    exec(compiled_code, {})

actual_true = true_output_capture.getvalue().strip()

assert actual_true == "Passed!", (
    f"Expected 'Passed!', received '{actual_true}'"
)

print("SUCCESS: TRUE branch executed correctly!")


# --------------------------------------------------
# TEST FALSE BRANCH
# --------------------------------------------------

print("\n5. Testing FALSE branch...")

# Change the score to 5 in the generated code.
false_code = program.code.replace(
    "score = 15",
    "score = 5"
)

compiled_false_code = compile(
    false_code,
    "<LogicFlow False Branch Test>",
    "exec"
)

false_output_capture = StringIO()

with redirect_stdout(false_output_capture):
    exec(compiled_false_code, {})

actual_false = false_output_capture.getvalue().strip()

assert actual_false == "Not passed!", (
    f"Expected 'Not passed!', received '{actual_false}'"
)

print("SUCCESS: FALSE branch executed correctly!")


# --------------------------------------------------
# TEST NODE MAPPING
# --------------------------------------------------

print("\n6. Testing node mapping...")

condition_section = program.get_section_for_node(condition)

assert condition_section is not None

print("SUCCESS: Condition node is mapped to generated code!")


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n" + "=" * 45)
print("ALL CONDITIONAL TESTS PASSED!")
print("IF-ELSE generation is working correctly.")
print("=" * 45)
