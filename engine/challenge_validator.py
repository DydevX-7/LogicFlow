
from dataclasses import dataclass
import math
import re

from engine.execution_engine import ExecutionEngine


@dataclass
class ChallengeResult:
    passed: bool
    message: str
    tests_passed: int = 0
    total_tests: int = 0
    xp: int = 0


class ChallengeValidator:
    """
    Tests LogicFlow challenge solutions by executing the student's
    flowchart against several predefined test cases.
    """

    CHALLENGES = {
        0: {
            "name": "Build a Simple Calculator",
            "xp": 20,
            "minimum": {
                "START": 1,
                "INPUT": 2,
                "OPERATION": 4,
                "OUTPUT": 4,
                "END": 1,
            },
            "tests": [
                {
                    "inputs": ["10", "5"],
                    "expected": [15, 5, 50, 2],
                },
                {
                    "inputs": ["20", "4"],
                    "expected": [24, 16, 80, 5],
                },
                {
                    "inputs": ["9", "3"],
                    "expected": [12, 6, 27, 3],
                },
            ],
        },

        1: {
            "name": "Voting Eligibility Checker",
            "xp": 25,
            "minimum": {
                "START": 1,
                "INPUT": 1,
                "CONDITION": 1,
                "OUTPUT": 2,
                "END": 1,
            },
            "tests": [
                {
                    "inputs": ["20"],
                    "expected_text": ["eligible to vote"],
                },
                {
                    "inputs": ["18"],
                    "expected_text": ["eligible to vote"],
                },
                {
                    "inputs": ["15"],
                    "expected_text": ["not eligible to vote"],
                },
            ],
        },

        2: {
            "name": "Find the Largest of Three Numbers",
            "xp": 30,
            "minimum": {
                "START": 1,
                "INPUT": 3,
                "CONDITION": 2,
                "OUTPUT": 1,
                "END": 1,
            },
            "tests": [
                {
                    "inputs": ["10", "20", "30"],
                    "expected": [30],
                },
                {
                    "inputs": ["50", "20", "10"],
                    "expected": [50],
                },
                {
                    "inputs": ["15", "40", "25"],
                    "expected": [40],
                },
            ],
        },

        3: {
            "name": "Student Average & Grade Calculator",
            "xp": 35,
            "minimum": {
                "START": 1,
                "INPUT": 3,
                "OPERATION": 4,
                "CONDITION": 3,
                "OUTPUT": 4,
                "END": 1,
            },
            "tests": [
                {
                    "inputs": ["90", "95", "85"],
                    "expected": [90],
                    "expected_text": ["grade a"],
                },
                {
                    "inputs": ["75", "80", "70"],
                    "expected": [75],
                    "expected_text": ["grade b"],
                },
                {
                    "inputs": ["60", "65", "55"],
                    "expected": [60],
                    "expected_text": ["grade c"],
                },
                {
                    "inputs": ["40", "45", "50"],
                    "expected": [45],
                    "expected_text": ["grade d"],
                },
            ],
        },

        4: {
            "name": "Rectangle Calculator",
            "xp": 20,
            "minimum": {
                "START": 1,
                "INPUT": 2,
                "OPERATION": 4,
                "OUTPUT": 2,
                "END": 1,
            },
            "tests": [
                {
                    "inputs": ["10", "5"],
                    "expected": [50, 30],
                },
                {
                    "inputs": ["8", "4"],
                    "expected": [32, 24],
                },
                {
                    "inputs": ["6", "3"],
                    "expected": [18, 18],
                },
            ],
        },
    }

    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections

    # ==================================
    # MAIN VALIDATION
    # ==================================

    def validate(self, challenge_index: int) -> ChallengeResult:

        challenge = self.CHALLENGES.get(challenge_index)

        if challenge is None:
            return ChallengeResult(
                False,
                "Challenge not found."
            )

        if not self.nodes:
            return ChallengeResult(
                False,
                "Your flowchart is empty. Build your solution first."
            )

        structural_error = self.check_structure(
            challenge["minimum"]
        )

        if structural_error:
            return ChallengeResult(
                False,
                structural_error
            )

        passed = 0
        total = len(challenge["tests"])

        for test_number, test in enumerate(
            challenge["tests"],
            start=1
        ):

            result = self.run_test(test["inputs"])

            if not result["success"]:
                return ChallengeResult(
                    False,
                    (
                        f"Test {test_number} failed.\n"
                        f"{result['message']}"
                    ),
                    passed,
                    total
                )

            outputs = result["outputs"]

            numbers_match = self.check_expected_numbers(
                outputs,
                test.get("expected", [])
            )

            text_matches = self.check_expected_text(
                outputs,
                test.get("expected_text", [])
            )

            if numbers_match and text_matches:
                passed += 1

        if passed == total:
            return ChallengeResult(
                True,
                (
                    f"Excellent! You completed "
                    f"{challenge['name']}.\n"
                    f"All {total} test cases passed!"
                ),
                passed,
                total,
                challenge["xp"]
            )

        return ChallengeResult(
            False,
            (
                f"You passed {passed} out of {total} tests.\n"
                "Your flowchart still needs some improvements."
            ),
            passed,
            total
        )

    # ==================================
    # STRUCTURE VALIDATION
    # ==================================

    def check_structure(self, minimum):

        counts = {}

        for node in self.nodes:
            node_type = getattr(node, "node_type", None)
            counts[node_type] = counts.get(node_type, 0) + 1

        for node_type, required_count in minimum.items():

            actual_count = counts.get(node_type, 0)

            if actual_count < required_count:
                return (
                    f"Your flowchart needs at least "
                    f"{required_count} {node_type} node(s). "
                    f"You currently have {actual_count}."
                )

        if counts.get("START", 0) != 1:
            return (
                "Your flowchart must contain exactly one START node."
            )

        if counts.get("END", 0) != 1:
            return (
                "Your flowchart must contain exactly one END node."
            )

        return None

    # ==================================
    # RUN ONE TEST CASE
    # ==================================

    def run_test(self, test_inputs):

        engine = ExecutionEngine(
            self.nodes,
            self.connections
        )

        input_index = 0
        outputs = []

        def test_input_provider(question):

            nonlocal input_index

            if input_index >= len(test_inputs):
                raise ValueError(
                    "Your flowchart requested more inputs "
                    "than this challenge provides."
                )

            value = test_inputs[input_index]
            input_index += 1

            return value

        try:

            start_result = engine.start()

            if not start_result.success:
                return {
                    "success": False,
                    "message": start_result.message,
                    "outputs": [],
                }

            while not engine.finished:

                result = engine.step(
                    input_provider=test_input_provider
                )

                executed_node = result.current_node

                if (
                    executed_node is not None
                    and getattr(executed_node, "node_type", None) == "OUTPUT"
                    and not result.error
                ):
                    outputs.append(
                        str(engine.last_output)
                    )

                if result.error or not result.success:
                    return {
                        "success": False,
                        "message": result.message,
                        "outputs": outputs,
                    }

            if input_index != len(test_inputs):
                return {
                    "success": False,
                    "message": (
                        "Your flowchart did not use "
                        "all the required inputs."
                    ),
                    "outputs": outputs,
                }

            return {
                "success": True,
                "message": "Execution completed.",
                "outputs": outputs,
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error),
                "outputs": outputs,
            }

    # ==================================
    # NUMBER EXTRACTION
    # ==================================

    @staticmethod
    def extract_numbers(outputs):

        numbers = []

        number_pattern = re.compile(
            r"(?<![A-Za-z_])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?![A-Za-z_])"
        )

        for output in outputs:

            matches = number_pattern.findall(str(output))

            for match in matches:
                try:
                    number = float(match)

                    if math.isfinite(number):
                        numbers.append(number)

                except (ValueError, OverflowError):
                    pass

        return numbers

    # ==================================
    # CHECK EXPECTED NUMBERS
    # ==================================

    def check_expected_numbers(self, outputs, expected):

        if not expected:
            return True

        actual = self.extract_numbers(outputs)

        # Each expected number must have its own matching occurrence.
        # One occurrence cannot satisfy multiple expected values.
        remaining_numbers = actual.copy()

        for expected_value in expected:

            found_index = None

            for index, actual_value in enumerate(remaining_numbers):

                if math.isclose(
                    actual_value,
                    float(expected_value),
                    rel_tol=1e-5,
                    abs_tol=1e-5
                ):
                    found_index = index
                    break

            if found_index is None:
                return False

            remaining_numbers.pop(found_index)

        return True

    # ==================================
    # CHECK EXPECTED TEXT
    # ==================================

    @staticmethod
    def check_expected_text(outputs, expected):

        if not expected:
            return True

        combined = " ".join(
            str(output) for output in outputs
        ).lower()

        combined = re.sub(
            r"\s+",
            " ",
            combined
        ).strip()

        for phrase in expected:

            phrase = re.sub(
                r"\s+",
                " ",
                phrase.lower()
            ).strip()

            if not phrase:
                return False

            # A positive voting result must not match
            # the negative voting result.
            if phrase == "eligible to vote":
                if re.search(
                    r"(?<![a-z])not\s+eligible\s+to\s+vote(?![a-z])",
                    combined
                ):
                    return False

            pattern = (
                r"(?<![a-z])"
                + re.escape(phrase)
                + r"(?![a-z])"
            )

            if not re.search(pattern, combined):
                return False

        return True
