from ui.learning_cards import polish_learning_card
from ui.learning_theme import apply_learning_theme
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QStackedWidget, QProgressBar,
    QRadioButton, QButtonGroup
)


LESSONS = [
    {
        "title": "Algorithms & Flowcharts",
        "subtitle": "Understand how to plan a program.",
        "intro": "Before building anything, you need a plan. "
                 "Programs work the same way. Let's learn how to plan "
                 "a solution before turning it into a flowchart.",

        "theory": [
            {
                "title": "01  What is an algorithm?",
                "analogy_title": "Think of it like following a recipe",
                "analogy": "Imagine making a cup of tea. You boil water, "
                           "add tea leaves, add milk, and serve it. "
                           "You follow a sequence of instructions to get "
                           "the result you want.",
                "definition": "An algorithm is a finite, ordered sequence "
                              "of clear instructions designed to solve a "
                              "problem or complete a task.",
                "example_title": "A simple everyday algorithm",
                "example": [
                    "1. Take a glass.",
                    "2. Fill it with water.",
                    "3. Drink the water."
                ],
                "takeaway": "An algorithm is the plan behind a solution."
            },
            {
                "title": "02  What is a flowchart?",
                "analogy_title": "Think of it like a map",
                "analogy": "A map shows you where to go and which direction "
                           "to take. A flowchart does something similar: "
                           "it shows the steps of a program and how they "
                           "are connected.",
                "definition": "A flowchart is a graphical representation "
                              "of an algorithm using standard symbols and "
                              "arrows to show the sequence of operations.",
                "example_title": "A simple program flow",
                "example": [
                    "START",
                    "   ↓",
                    "DISPLAY A MESSAGE",
                    "   ↓",
                    "END"
                ],
                "takeaway": "A flowchart turns a written plan into a visual plan."
            },
            {
                "title": "03  Understanding program flow",
                "analogy_title": "Think of it like a journey",
                "analogy": "When travelling, you follow a route from your "
                           "starting point to your destination. A program "
                           "also follows a route through connected nodes.",
                "definition": "Program flow is the order in which the "
                              "instructions of a program are executed.",
                "example_title": "The basic execution sequence",
                "example": [
                    "START",
                    "   ↓",
                    "PROCESS",
                    "   ↓",
                    "OUTPUT",
                    "   ↓",
                    "END"
                ],
                "takeaway": "Connections determine which instruction runs next."
            }
        ],

        "task": "Create a flowchart that displays a welcome message.",
        "steps": [
            "Add a START node.",
            "Add an OUTPUT node and set its message to: Welcome to LogicFlow!",
            "Add an END node.",
            "Connect START → OUTPUT → END.",
            "Run the program and check the output."
        ],

        "questions": [
            {
                "q": "What is an algorithm?",
                "options": [
                    "A sequence of steps to solve a problem",
                    "A programming language",
                    "A computer component",
                    "A type of variable"
                ],
                "answer": 0,
                "explanation": "An algorithm is a sequence of instructions for solving a problem."
            },
            {
                "q": "What does a flowchart represent?",
                "options": [
                    "Computer hardware",
                    "A visual representation of a process",
                    "Only mathematical equations",
                    "A storage device"
                ],
                "answer": 1,
                "explanation": "A flowchart represents the steps and decisions in a process visually."
            },
            {
                "q": "Which node marks the beginning of a program?",
                "options": ["OUTPUT", "END", "START", "CONDITION"],
                "answer": 2,
                "explanation": "The START node identifies where program execution begins."
            }
        ]
    },

    {
        "title": "Variables & Data",
        "subtitle": "Learn how programs store information.",
        "intro": "Programs need information to work. They must be able "
                 "to remember names, numbers, scores, and other values. "
                 "That's where variables come in.",

        "theory": [
            {
                "title": "01  What is a variable?",
                "analogy_title": "Imagine a labelled storage box",
                "analogy": "Imagine you have a box labelled SCORE. "
                           "You put the number 100 inside it. Whenever "
                           "you need the score, you look inside that box.",
                "definition": "A variable is a named storage location "
                              "used by a program to hold a value that "
                              "can be accessed and, when permitted, changed.",
                "example_title": "A variable in action",
                "example": [
                    "Variable name: score",
                    "Stored value: 100",
                    "Later value: 150"
                ],
                "takeaway": "A variable has a name and stores a value."
            },
            {
                "title": "02  Choosing variable names",
                "analogy_title": "Think of labels on your school notebooks",
                "analogy": "You label your notebooks Maths, Physics, and "
                           "Chemistry so you can identify them easily. "
                           "Variable names work in the same way.",
                "definition": "A variable name is an identifier used to "
                              "refer to a stored value in a program.",
                "example_title": "Good and poor variable names",
                "example": [
                    "student_name  →  Clear and meaningful",
                    "total_marks   →  Clear and meaningful",
                    "x1            →  Less descriptive",
                    "123           →  Invalid as a variable name"
                ],
                "takeaway": "Choose names that explain what the data represents."
            },
            {
                "title": "03  Using stored information",
                "analogy_title": "Think of retrieving a saved contact",
                "analogy": "You don't need to remember someone's entire "
                           "phone number. You search for their saved name "
                           "and retrieve the number when you need it.",
                "definition": "A program accesses a variable by referring "
                              "to its identifier wherever the stored value "
                              "is required.",
                "example_title": "Using a variable in LogicFlow",
                "example": [
                    "Variable: name",
                    "Stored value: Alex",
                    "Output message: Hello {name}!",
                    "Result: Hello Alex!"
                ],
                "takeaway": "Stored values can be reused throughout a program."
            }
        ],

        "task": "Create a flowchart that stores a name and displays a greeting.",
        "steps": [
            "Add a START node.",
            "Add an INPUT node asking: What is your name?",
            "Set its variable name to: name.",
            "Add an OUTPUT node with the message: Hello {name}!",
            "Add an END node.",
            "Connect the nodes in order and run the program."
        ],

        "questions": [
            {
                "q": "What is the purpose of a variable?",
                "options": [
                    "To connect nodes",
                    "To store information",
                    "To stop a program",
                    "To display the editor"
                ],
                "answer": 1,
                "explanation": "Variables store information that a program can use later."
            },
            {
                "q": "Which is a meaningful variable name?",
                "options": ["x1", "123", "student_name", " "],
                "answer": 2,
                "explanation": "student_name clearly communicates what the variable represents."
            },
            {
                "q": "How do you insert a stored variable into an OUTPUT message?",
                "options": ["(name)", "[name]", "{name}", "<name>"],
                "answer": 2,
                "explanation": "LogicFlow uses curly braces, like {name}, to insert a variable."
            }
        ]
    },

    {
        "title": "Input, Operations & Output",
        "subtitle": "Make your flowcharts interact with information.",
        "intro": "A useful program doesn't just follow instructions. "
                 "It receives information, works with it, and gives "
                 "something meaningful back.",

        "theory": [
            {
                "title": "01  Input",
                "analogy_title": "Think of ordering food",
                "analogy": "When you order food, the restaurant needs "
                           "to know what you want. You provide information "
                           "before anything can be prepared.",
                "definition": "Input is the process through which a "
                              "program receives data from an external "
                              "source, such as its user.",
                "example_title": "An example",
                "example": [
                    "Question: What is your name?",
                    "User enters: Alex",
                    "Variable receives: name = Alex"
                ],
                "takeaway": "Input allows a program to receive information."
            },
            {
                "title": "02  Operations",
                "analogy_title": "Think of a bank account",
                "analogy": "Imagine your account has ₹500. You deposit "
                           "₹200, and your balance becomes ₹700. "
                           "The stored amount has been changed.",
                "definition": "An operation is an instruction that "
                              "performs an action on data, such as "
                              "assigning or modifying a value.",
                "example_title": "Operations available in LogicFlow",
                "example": [
                    "Set a value      →  score = 10",
                    "Increase a value →  score increases",
                    "Decrease a value →  score decreases"
                ],
                "takeaway": "Operations assign or modify stored values."
            },
            {
                "title": "03  Output",
                "analogy_title": "Think of a result displayed on a screen",
                "analogy": "After calculating your exam result, the "
                           "school displays your marks. The result is "
                           "communicated to you.",
                "definition": "Output is the information produced by a "
                              "program and presented to a user or another "
                              "system.",
                "example_title": "An example",
                "example": [
                    "Stored variable: name = Alex",
                    "Output message: Hello {name}!",
                    "Displayed result: Hello Alex!"
                ],
                "takeaway": "Output communicates the result of a program."
            }
        ],

        "task": "Build a simple flowchart that receives a number and displays it.",
        "steps": [
            "Add START.",
            "Add an INPUT node asking for a number. Store it as number.",
            "Add an OUTPUT node displaying: You entered {number}.",
            "Add END.",
            "Connect the nodes and run your flowchart."
        ],

        "questions": [
            {
                "q": "Which node receives information from the user?",
                "options": ["OUTPUT", "INPUT", "END", "START"],
                "answer": 1,
                "explanation": "The INPUT node asks the user for information."
            },
            {
                "q": "Which operation increases a stored numeric value?",
                "options": [
                    "Set a value",
                    "Decrease a value",
                    "Increase a value",
                    "End program"
                ],
                "answer": 2,
                "explanation": "Increase a value adds an amount to an existing variable."
            },
            {
                "q": "Which node displays information?",
                "options": ["INPUT", "CONDITION", "OUTPUT", "START"],
                "answer": 2,
                "explanation": "The OUTPUT node displays messages and stored values."
            }
        ]
    },

    {
        "title": "Conditions & Branching",
        "subtitle": "Teach your program to make decisions.",
        "intro": "Imagine a program that needs to decide whether "
                 "someone has passed an exam. It needs to check the "
                 "marks before choosing what to display.",

        "theory": [
            {
                "title": "01  What is a condition?",
                "analogy_title": "Think of an eligibility check",
                "analogy": "Imagine a school rule: students who score "
                           "at least 40 marks pass. The school checks "
                           "the marks before deciding the result.",
                "definition": "A condition is an expression that is "
                              "evaluated as either True or False.",
                "example_title": "A simple comparison",
                "example": [
                    "marks = 75",
                    "Check: marks >= 40",
                    "Result: TRUE"
                ],
                "takeaway": "A condition evaluates whether something is true or false."
            },
            {
                "title": "02  True and False paths",
                "analogy_title": "Think of a road with two directions",
                "analogy": "At a junction, you may choose one road or "
                           "another depending on your destination. "
                           "A condition creates two possible paths.",
                "definition": "Branching is a programming structure "
                              "that selects one execution path based "
                              "on the result of a condition.",
                "example_title": "Two possible outcomes",
                "example": [
                    "             CONDITION",
                    "                  ↓",
                    "          ┌───────┴───────┐",
                    "          ↓               ↓",
                    "        TRUE            FALSE",
                    "          ↓               ↓",
                    "       PASSED          FAILED"
                ],
                "takeaway": "TRUE and FALSE paths let programs choose what happens next."
            },
            {
                "title": "03  Why branching matters",
                "analogy_title": "Think of a traffic signal",
                "analogy": "A traffic signal changes what drivers should "
                           "do depending on its current state. Programs "
                           "also change their behaviour depending on "
                           "the information they receive.",
                "definition": "Conditional execution allows a program "
                              "to perform different instructions depending "
                              "on whether specified conditions are met.",
                "example_title": "Where branching is used",
                "example": [
                    "Exam result: Pass or fail",
                    "Login system: Accepted or rejected",
                    "Age check: Eligible or not eligible"
                ],
                "takeaway": "Branching makes programs respond intelligently to different situations."
            }
        ],

        "task": "Build a program that checks whether a student has passed.",
        "steps": [
            "Add START.",
            "Add an INPUT node asking for the student's marks. Store the answer as marks.",
            "Add a CONDITION node checking whether marks are greater than or equal to 40.",
            "Connect the TRUE path to an OUTPUT node displaying: You passed!",
            "Connect the FALSE path to another OUTPUT node displaying: You did not pass.",
            "Connect both OUTPUT nodes to END.",
            "Run the program with different marks to test both paths."
        ],

        "questions": [
            {
                "q": "What does a CONDITION node do?",
                "options": [
                    "Stores a message",
                    "Checks whether a comparison is true or false",
                    "Always ends the program",
                    "Receives user input"
                ],
                "answer": 1,
                "explanation": "A condition evaluates a comparison and selects a path."
            },
            {
                "q": "When does a program follow the TRUE path?",
                "options": [
                    "When the condition is satisfied",
                    "When the program starts",
                    "When the user closes the editor",
                    "Whenever an OUTPUT node runs"
                ],
                "answer": 0,
                "explanation": "The TRUE path is followed when the condition evaluates to true."
            },
            {
                "q": "Which node is suitable for checking whether marks are at least 40?",
                "options": ["INPUT", "OUTPUT", "CONDITION", "END"],
                "answer": 2,
                "explanation": "A CONDITION node can compare marks with 40 using greater than or equal to."
            }
        ]
    }
]


class LearningPage(QWidget):
    lesson_selected = Signal(int)
    lesson_completed = Signal(int)
    open_editor = Signal()
    challenge_editor_requested = Signal()

    def __init__(self):
        super().__init__()
        apply_learning_theme(self)

        self.completed_lessons = set()
        self.current_lesson = 0
        self.question_index = 0
        self.question_answered = False

        self.build_roadmap()
        self.build_lesson_panel()
        self.refresh_roadmap()
        self.build_challenges_page()

    # ---------------------------------------------------------
    # ROADMAP - KEPT AS THE ORIGINAL DESIGN
    # ---------------------------------------------------------

    def build_roadmap(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(16)

        heading = QLabel("Learning Roadmap")
        heading.setStyleSheet("font-size: 25px; font-weight: bold;")
        root.addWidget(heading)

        description = QLabel(
            "Follow the lessons in order. Complete each practical task "
            "and answer its questions to unlock your progress."
        )
        description.setObjectName("Muted")
        description.setWordWrap(True)
        root.addWidget(description)

        progress_header = QHBoxLayout()

        progress_title = QLabel("YOUR PROGRESS")
        progress_title.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #9CA3AF;"
        )

        self.progress_text = QLabel("0 of 4 lessons completed")
        self.progress_text.setObjectName("Muted")

        progress_header.addWidget(progress_title)
        progress_header.addStretch()
        progress_header.addWidget(self.progress_text)
        root.addLayout(progress_header)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(LESSONS))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #252A34;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: #3B82F6;
                border-radius: 4px;
            }
        """)
        root.addWidget(self.progress_bar)

        root.addSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.roadmap_layout = QVBoxLayout(content)
        self.roadmap_layout.setContentsMargins(4, 4, 12, 12)
        self.roadmap_layout.setSpacing(12)

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def refresh_roadmap(self):
        while self.roadmap_layout.count():
            item = self.roadmap_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        total = len(LESSONS)
        done = len(self.completed_lessons)

        self.progress_bar.setValue(done)
        self.progress_text.setText(
            f"{done} of {total} lessons completed"
        )

        for index, lesson in enumerate(LESSONS):
            completed = index in self.completed_lessons

            card = QFrame()
            polish_learning_card(card)

            layout = QHBoxLayout(card)
            layout.setContentsMargins(16, 14, 16, 14)
            layout.setSpacing(14)

            number = QLabel("✓" if completed else str(index + 1))
            number.setAlignment(Qt.AlignmentFlag.AlignCenter)
            number.setFixedSize(38, 38)

            number.setStyleSheet(
                "background: #173D30; color: #6EE7B7; "
                "border-radius: 19px; font-weight: bold;"
                if completed else
                "background: #252A34; color: #60A5FA; "
                "border-radius: 19px; font-weight: bold;"
            )

            text_layout = QVBoxLayout()

            title = QLabel(lesson["title"])
            title.setStyleSheet("font-size: 15px; font-weight: bold;")

            subtitle = QLabel(lesson["subtitle"])
            subtitle.setObjectName("Muted")
            subtitle.setWordWrap(True)

            text_layout.addWidget(title)
            text_layout.addWidget(subtitle)

            button = QPushButton(
                "Review lesson" if completed else "Start lesson"
            )
            button.setFixedWidth(130)
            button.clicked.connect(
                lambda checked=False, i=index: self.open_lesson(i)
            )

            layout.addWidget(number)
            layout.addLayout(text_layout, 1)
            layout.addWidget(button)

            self.roadmap_layout.addWidget(card)

        self.roadmap_layout.addStretch()

    # ---------------------------------------------------------
    # LESSON PANEL
    # ---------------------------------------------------------

    def build_lesson_panel(self):
        self.lesson_panel = QWidget()
        root = QVBoxLayout(self.lesson_panel)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(12)

        header = QHBoxLayout()

        self.back_button = QPushButton("← Roadmap")
        self.back_button.clicked.connect(self.return_to_roadmap)

        self.lesson_heading = QLabel("Lesson")
        self.lesson_heading.setStyleSheet(
            "font-size: 19px; font-weight: bold;"
        )

        header.addWidget(self.back_button)
        header.addWidget(self.lesson_heading, 1)
        root.addLayout(header)

        self.stage_stack = QStackedWidget()
        root.addWidget(self.stage_stack, 1)

        self.theory_page = self.create_theory_page()
        self.practice_page = self.create_practice_page()
        self.quiz_page = self.create_quiz_page()
        self.finished_page = self.create_finished_page()

        self.stage_stack.addWidget(self.theory_page)
        self.stage_stack.addWidget(self.practice_page)
        self.stage_stack.addWidget(self.quiz_page)
        self.stage_stack.addWidget(self.finished_page)

    # ---------------------------------------------------------
    # REUSABLE LESSON DESIGN COMPONENTS
    # ---------------------------------------------------------

    def create_card(self, title, body, accent="#60A5FA"):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #181B22;
                border: 1px solid #292D36;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(17, 15, 17, 15)
        layout.setSpacing(9)

        heading = QLabel(title)
        heading.setStyleSheet(
            f"font-size: 15px; font-weight: bold; color: {accent}; "
            "border: none; background: transparent;"
        )

        text = QLabel(body)
        text.setWordWrap(True)
        text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        text.setStyleSheet(
            "font-size: 13px; color: #D1D5DB; "
            "line-height: 1.5; border: none; background: transparent;"
        )

        layout.addWidget(heading)
        layout.addWidget(text)

        return card

    def create_example_card(self, title, lines):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #141820;
                border: 1px solid #303846;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(17, 14, 17, 14)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #93C5FD;"
            "border: none; background: transparent;"
        )
        layout.addWidget(heading)

        for line in lines:
            row = QLabel(line)
            row.setWordWrap(True)
            row.setStyleSheet(
                "font-family: Consolas; font-size: 12px; "
                "color: #E5E7EB; border: none; background: transparent;"
            )
            layout.addWidget(row)

        return card

    def create_theory_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.theory_layout = QVBoxLayout(content)
        self.theory_layout.setContentsMargins(4, 4, 12, 12)
        self.theory_layout.setSpacing(14)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        self.theory_continue = QPushButton(
            "Continue to practical task  →"
        )
        self.theory_continue.setObjectName("RunButton")
        self.theory_continue.clicked.connect(
            lambda: self.stage_stack.setCurrentWidget(self.practice_page)
        )
        layout.addWidget(self.theory_continue)

        return page

    def populate_theory(self, lesson):
        while self.theory_layout.count():
            item = self.theory_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Lesson introduction
        intro = QLabel(lesson["intro"])
        intro.setWordWrap(True)
        intro.setStyleSheet("""
            font-size: 14px;
            color: #D1D5DB;
            padding: 8px 4px 12px 4px;
        """)
        self.theory_layout.addWidget(intro)

        for section in lesson["theory"]:
            # Main section heading
            heading = QLabel(section["title"])
            heading.setWordWrap(True)
            heading.setStyleSheet("""
                font-size: 19px;
                font-weight: bold;
                color: #E5E7EB;
                padding: 8px 2px;
            """)
            self.theory_layout.addWidget(heading)

            # Analogy
            self.theory_layout.addWidget(
                self.create_card(
                    section["analogy_title"],
                    section["analogy"],
                    "#FBBF24"
                )
            )

            # Technical definition
            self.theory_layout.addWidget(
                self.create_card(
                    "THE ACTUAL DEFINITION",
                    section["definition"],
                    "#60A5FA"
                )
            )

            # Example
            self.theory_layout.addWidget(
                self.create_example_card(
                    section["example_title"],
                    section["example"]
                )
            )

            # Key takeaway
            self.theory_layout.addWidget(
                self.create_card(
                    "REMEMBER THIS",
                    section["takeaway"],
                    "#6EE7B7"
                )
            )

            self.theory_layout.addSpacing(8)

        self.theory_layout.addStretch(1)

    # ---------------------------------------------------------
    # PRACTICAL TASK
    # ---------------------------------------------------------

    
    def create_practice_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.practice_layout = QVBoxLayout(content)
        self.practice_layout.setContentsMargins(4, 4, 12, 12)
        self.practice_layout.setSpacing(14)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        self.practice_continue = QPushButton(
            "I've completed the challenge — Start questions  →"
        )
        self.practice_continue.setObjectName("RunButton")
        self.practice_continue.clicked.connect(self.start_quiz)
        layout.addWidget(self.practice_continue)

        return page

    
    def populate_practice_page(self, lesson, index):
        while self.practice_layout.count():
            item = self.practice_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        challenges = [
            {
                "number": "CHALLENGE 01",
                "title": "Your First Flowchart",
                "scenario": (
                    "Imagine you're building the welcome screen for an "
                    "application. Whenever someone opens it, the program "
                    "should display a welcome message."
                ),
                "mission": (
                    "Create a flowchart that displays exactly:\n\n"
                    "Welcome to LogicFlow!"
                ),
                "instructions": [
                    "Open the LogicFlow editor.",
                    "Add a START node.",
                    "Add an OUTPUT node.",
                    "Set its message to: Welcome to LogicFlow!",
                    "Add an END node.",
                    "Connect START → OUTPUT → END.",
                    "Run the flowchart."
                ],
                "nodes": [
                    "START — Begins program execution.",
                    "OUTPUT — Displays the welcome message.",
                    "END — Finishes the program."
                ],
                "tests": [
                    "The program starts successfully.",
                    "The output says: Welcome to LogicFlow!",
                    "The program reaches END."
                ],
                "hint": (
                    "You only need three nodes. The OUTPUT node should "
                    "be placed between START and END. Check the spelling "
                    "and punctuation of your message."
                )
            },
            {
                "number": "CHALLENGE 02",
                "title": "Build a Greeting Program",
                "scenario": (
                    "You're creating a simple greeting feature. Instead "
                    "of displaying the same message to everyone, the "
                    "program should ask for the user's name and greet "
                    "them personally."
                ),
                "mission": (
                    "Ask the user for their name and display a greeting "
                    "using the name they entered."
                ),
                "instructions": [
                    "Add a START node.",
                    "Add an INPUT node.",
                    "Set its question to: What is your name?",
                    "Set its variable name to: name.",
                    "Add an OUTPUT node.",
                    "Set its message to: Hello {name}!",
                    "Add an END node.",
                    "Connect START → INPUT → OUTPUT → END.",
                    "Run the program and enter a name."
                ],
                "nodes": [
                    "START — Begins execution.",
                    "INPUT — Receives the user's name.",
                    "OUTPUT — Displays the greeting.",
                    "END — Finishes execution."
                ],
                "tests": [
                    "Enter Alex → Hello Alex!",
                    "Enter Sam → Hello Sam!",
                    "Enter another name → The program should use that name."
                ],
                "hint": (
                    "The INPUT node stores the answer in a variable. "
                    "The variable name must match the name inside the "
                    "curly braces in your OUTPUT message."
                )
            },
            {
                "number": "CHALLENGE 03",
                "title": "Create an Input Display Program",
                "scenario": (
                    "You're building a small utility that receives a "
                    "number from the user and displays the number back. "
                    "This is a simple example of how programs receive "
                    "and communicate information."
                ),
                "mission": (
                    "Ask the user to enter a number and display the "
                    "number they entered."
                ),
                "instructions": [
                    "Add a START node.",
                    "Add an INPUT node.",
                    "Set its question to: Enter a number.",
                    "Set its variable name to: number.",
                    "Add an OUTPUT node.",
                    "Set its message to: You entered {number}.",
                    "Add an END node.",
                    "Connect START → INPUT → OUTPUT → END.",
                    "Run the program and test different numbers."
                ],
                "nodes": [
                    "START — Begins execution.",
                    "INPUT — Receives the number.",
                    "OUTPUT — Displays the stored number.",
                    "END — Finishes execution."
                ],
                "tests": [
                    "Enter 10 → You entered 10.",
                    "Enter 25 → You entered 25.",
                    "Enter 100 → You entered 100."
                ],
                "hint": (
                    "Use number as the INPUT variable name. Then write "
                    "{number} inside the OUTPUT message. The braces tell "
                    "LogicFlow to insert the stored value."
                )
            },
            {
                "number": "CHALLENGE 04",
                "title": "Build a Pass or Fail Checker",
                "scenario": (
                    "A school wants a simple program to check whether "
                    "a student has passed an examination. A student "
                    "needs at least 40 marks to pass."
                ),
                "mission": (
                    "Create a program that asks for marks, checks whether "
                    "the marks are at least 40, and displays the correct "
                    "result."
                ),
                "instructions": [
                    "Add a START node.",
                    "Add an INPUT node asking for the student's marks.",
                    "Set its variable name to: marks.",
                    "Add a CONDITION node.",
                    "Set its variable to: marks.",
                    "Set comparison to: Greater than or equal to.",
                    "Set compare value to: 40.",
                    "Connect the TRUE output to an OUTPUT node displaying: You passed!",
                    "Connect the FALSE output to another OUTPUT node displaying: You did not pass.",
                    "Connect both OUTPUT nodes to END.",
                    "Run the program with different marks."
                ],
                "nodes": [
                    "START — Begins execution.",
                    "INPUT — Receives the student's marks.",
                    "CONDITION — Checks whether marks >= 40.",
                    "TRUE OUTPUT — Displays You passed!",
                    "FALSE OUTPUT — Displays You did not pass.",
                    "END — Finishes either path."
                ],
                "tests": [
                    "Enter 75 → You passed!",
                    "Enter 40 → You passed!",
                    "Enter 25 → You did not pass."
                ],
                "hint": (
                    "Remember that greater than or equal to includes 40. "
                    "The TRUE connection should lead to the passing "
                    "message. The FALSE connection should lead to the "
                    "failing message. Both paths should eventually reach END."
                )
            }
        ]

        challenge = challenges[index]

        # Challenge heading
        number = QLabel(challenge["number"])
        number.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #60A5FA;"
        )
        self.practice_layout.addWidget(number)

        title = QLabel(challenge["title"])
        title.setWordWrap(True)
        title.setStyleSheet(
            "font-size: 23px; font-weight: bold; color: #E5E7EB;"
        )
        self.practice_layout.addWidget(title)

        subtitle = QLabel(
            "PRACTICAL ASSIGNMENT  •  LESSON " + str(index + 1)
        )
        subtitle.setStyleSheet(
            "font-size: 10px; color: #9CA3AF; font-weight: bold;"
        )
        self.practice_layout.addWidget(subtitle)

        self.practice_layout.addSpacing(6)

        # Real-world scenario
        self.practice_layout.addWidget(
            self.create_card(
                "THE SCENARIO",
                challenge["scenario"],
                "#FBBF24"
            )
        )

        # Mission
        self.practice_layout.addWidget(
            self.create_card(
                "YOUR MISSION",
                challenge["mission"],
                "#60A5FA"
            )
        )

        # Instructions
        instruction_lines = [
            f"{i + 1}. {step}"
            for i, step in enumerate(challenge["instructions"])
        ]

        self.practice_layout.addWidget(
            self.create_example_card(
                "BUILD INSTRUCTIONS",
                instruction_lines
            )
        )

        # Node guide
        self.practice_layout.addWidget(
            self.create_example_card(
                "NODE REFERENCE",
                challenge["nodes"]
            )
        )

        # Test cases
        self.practice_layout.addWidget(
            self.create_example_card(
                "TEST YOUR PROGRAM",
                challenge["tests"]
            )
        )

        # Revealable hint
        hint_frame = QFrame()
        hint_frame.setStyleSheet("""
            QFrame {
                background: #181B22;
                border: 1px solid #383B45;
                border-radius: 10px;
            }
        """)

        hint_layout = QVBoxLayout(hint_frame)
        hint_layout.setContentsMargins(15, 13, 15, 13)
        hint_layout.setSpacing(10)

        hint_button = QPushButton("Show hint  ↓")
        hint_button.setStyleSheet("""
            QPushButton {
                color: #FBBF24;
                background: transparent;
                border: none;
                text-align: left;
                font-weight: bold;
                padding: 4px;
            }
            QPushButton:hover {
                color: #FDE68A;
            }
        """)

        hint_text = QLabel(challenge["hint"])
        hint_text.setWordWrap(True)
        hint_text.setVisible(False)
        hint_text.setStyleSheet(
            "color: #D1D5DB; font-size: 13px; "
            "background: transparent; border: none;"
        )

        def toggle_hint():
            visible = not hint_text.isVisible()
            hint_text.setVisible(visible)
            hint_button.setText(
                "Hide hint  ↑" if visible else "Show hint  ↓"
            )

        hint_button.clicked.connect(toggle_hint)

        hint_layout.addWidget(hint_button)
        hint_layout.addWidget(hint_text)

        self.practice_layout.addWidget(hint_frame)

        # Completion note
        self.practice_layout.addWidget(
            self.create_card(
                "READY TO CONTINUE?",
                "Build and run your flowchart in the editor. Check the "
                "test cases before continuing to the quiz.",
                "#6EE7B7"
            )
        )

        self.practice_layout.addStretch(1)



    # ---------------------------------------------------------
    # QUIZ
    # ---------------------------------------------------------

    def create_quiz_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(14)

        self.question_progress = QLabel()
        self.question_progress.setObjectName("Muted")
        layout.addWidget(self.question_progress)

        self.question_title = QLabel()
        self.question_title.setWordWrap(True)
        self.question_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 10px 0;"
        )
        layout.addWidget(self.question_title)

        self.answer_group = QButtonGroup(self)
        self.answer_group.setExclusive(True)
        self.answer_buttons = []

        for index in range(4):
            button = QRadioButton()
            button.setMinimumHeight(52)
            button.setStyleSheet("""
                QRadioButton {
                    background: #181B22;
                    border: 1px solid #292D36;
                    border-radius: 8px;
                    padding: 13px;
                    spacing: 10px;
                }
                QRadioButton:checked {
                    border: 1px solid #60A5FA;
                    background: #202B3D;
                }
            """)
            self.answer_group.addButton(button, index)
            self.answer_buttons.append(button)
            layout.addWidget(button)

        self.answer_feedback = QLabel()
        self.answer_feedback.setWordWrap(True)
        self.answer_feedback.setStyleSheet("padding: 8px;")
        layout.addWidget(self.answer_feedback)

        layout.addStretch(1)

        self.check_button = QPushButton("Check answer")
        self.check_button.setObjectName("RunButton")
        self.check_button.clicked.connect(self.check_answer)
        layout.addWidget(self.check_button)

        return page

    def show_question(self):
        questions = LESSONS[self.current_lesson]["questions"]
        question = questions[self.question_index]

        self.question_progress.setText(
            f"QUESTION {self.question_index + 1} OF {len(questions)}"
        )
        self.question_title.setText(question["q"])

        self.answer_group.setExclusive(False)

        for index, button in enumerate(self.answer_buttons):
            button.setText(question["options"][index])
            button.setChecked(False)
            button.setEnabled(True)

        self.answer_group.setExclusive(True)

        self.answer_feedback.clear()
        self.question_answered = False
        self.check_button.setText("Check answer")

    def start_quiz(self):
        self.question_index = 0
        self.show_question()
        self.stage_stack.setCurrentWidget(self.quiz_page)

    def check_answer(self):
        if self.question_answered:
            self.question_index += 1

            if self.question_index >= len(
                LESSONS[self.current_lesson]["questions"]
            ):
                self.stage_stack.setCurrentWidget(self.finished_page)
            else:
                self.show_question()

            return

        selected = self.answer_group.checkedId()

        if selected < 0:
            self.answer_feedback.setStyleSheet("color: #FBBF24;")
            self.answer_feedback.setText("Choose an answer first.")
            return

        question = LESSONS[self.current_lesson]["questions"][
            self.question_index
        ]

        if selected == question["answer"]:
            self.answer_feedback.setStyleSheet("color: #6EE7B7;")
            self.answer_feedback.setText(
                "Correct! " + question["explanation"]
            )
            self.question_answered = True

            if self.question_index < len(
                LESSONS[self.current_lesson]["questions"]
            ) - 1:
                self.check_button.setText("Next question  →")
            else:
                self.check_button.setText("Finish questions  →")
        else:
            self.answer_feedback.setStyleSheet("color: #FCA5A5;")
            self.answer_feedback.setText(
                "Not quite. Try again. " + question["explanation"]
            )

    # ---------------------------------------------------------
    # FINISHED
    # ---------------------------------------------------------

    def create_finished_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        title = QLabel("Lesson completed!")
        title.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #6EE7B7;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        description = QLabel(
            "You've completed the practical assignment and answered "
            "all three questions correctly."
            )

        description.setObjectName("Muted")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Continue your lessons  →")
        button.setObjectName("RunButton")
        button.clicked.connect(self.finish_lesson)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(button)

        return page

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def open_lesson(self, index):
        if not 0 <= index < len(LESSONS):
            return

        self.start_lesson(index)
        self.lesson_selected.emit(index)

    
    def start_lesson(self, index):
        if not 0 <= index < len(LESSONS):
            return

        self.current_lesson = index
        self.question_index = 0
        self.question_answered = False

        lesson = LESSONS[index]

        self.lesson_heading.setText(
            f"{index + 1:02d}  {lesson['title']}"
        )

        self.populate_theory(lesson)
        self.populate_practice_page(lesson, index)

        self.stage_stack.setCurrentWidget(self.theory_page)


    def finish_lesson(self):
        self.completed_lessons.add(self.current_lesson)
        self.refresh_roadmap()
        self.lesson_completed.emit(self.current_lesson)
        self.return_to_roadmap()

    def return_to_roadmap(self):
        self.refresh_roadmap()
        self.open_editor.emit()
    # ---------------------------------------------------------
    # CHALLENGES SYSTEM
    # ---------------------------------------------------------

    def build_challenges_page(self):
        self.active_challenge = None

        self.challenges = [
            {
                "emoji": "🧮",
                "title": "Build a Simple Calculator",
                "xp": 20,
                "difficulty": "EASY",
                "description": (
                    "Create a calculator that receives two numbers "
                    "and performs basic arithmetic operations."
                ),
                "intro": (
                    "Imagine you're developing a calculator application. "
                    "Your task is to build its basic calculation system "
                    "using LogicFlow."
                ),
                "mission": (
                    "Ask the user for two numbers, calculate their sum, "
                    "difference, product and quotient, and display "
                    "the results."
                ),
                "tasks": [
                    "Create a START node.",
                    "Ask the user to enter the first number. Store it as num1.",
                    "Ask the user to enter the second number. Store it as num2.",
                    "Create operations to calculate addition, subtraction, multiplication and division.",
                    "Store the results in separate variables.",
                    "Display all four results using OUTPUT nodes.",
                    "Connect the nodes and run your program."
                ],
                "concepts": [
                    "Variables",
                    "User input",
                    "Arithmetic operations",
                    "Output"
                ],
                "tests": [
                    "Enter 10 and 5. Addition should give 15.",
                    "Subtraction should give 5.",
                    "Multiplication should give 50.",
                    "Division should give 2."
                ]
            },
            {
                "emoji": "🗳️",
                "title": "Voting Eligibility Checker",
                "xp": 25,
                "difficulty": "EASY",
                "description": (
                    "Build a program that determines whether "
                    "a person is eligible to vote."
                ),
                "intro": (
                    "A voting registration system needs to check "
                    "a person's age before determining their eligibility. "
                    "You are going to build a simplified version."
                ),
                "mission": (
                    "Ask the user for their age. If their age is "
                    "18 or above, display that they are eligible "
                    "to vote. Otherwise, display that they are not."
                ),
                "tasks": [
                    "Create a START node.",
                    "Add an INPUT node asking for the person's age.",
                    "Store the answer in a variable named age.",
                    "Add a CONDITION node.",
                    "Set the condition to age Greater than or equal to 18.",
                    "Connect TRUE to an OUTPUT displaying: You are eligible to vote!",
                    "Connect FALSE to an OUTPUT displaying: You are not eligible to vote.",
                    "Connect both paths to END.",
                    "Run the program with different ages."
                ],
                "concepts": [
                    "Variables",
                    "Input",
                    "Conditions",
                    "Branching",
                    "Output"
                ],
                "tests": [
                    "Age 20 → Eligible to vote.",
                    "Age 18 → Eligible to vote.",
                    "Age 15 → Not eligible to vote."
                ]
            },
            {
                "emoji": "🔢",
                "title": "Find the Largest of Three Numbers",
                "xp": 30,
                "difficulty": "MEDIUM",
                "description": (
                    "Compare three numbers and identify "
                    "the largest one."
                ),
                "intro": (
                    "Imagine you're building a system that compares "
                    "three values. It needs to determine which value "
                    "is the greatest, regardless of the order in "
                    "which the numbers are entered."
                ),
                "mission": (
                    "Receive three numbers from the user and display "
                    "the largest number using conditional branching."
                ),
                "tasks": [
                    "Create a START node.",
                    "Ask for three numbers and store them as a, b and c.",
                    "Add a CONDITION checking whether a is greater than or equal to b.",
                    "On the TRUE path, add another CONDITION checking whether a is greater than or equal to c.",
                    "If both conditions are TRUE, display a.",
                    "If the second condition is FALSE, display c.",
                    "On the first condition's FALSE path, check whether b is greater than or equal to c.",
                    "Display b if TRUE, otherwise display c.",
                    "Connect the result paths to END.",
                    "Test the program using different combinations."
                ],
                "concepts": [
                    "Variables",
                    "Input",
                    "Comparison operators",
                    "Nested conditions",
                    "Branching"
                ],
                "tests": [
                    "10, 20, 30 → Largest is 30.",
                    "50, 20, 10 → Largest is 50.",
                    "15, 40, 25 → Largest is 40."
                ]
            },
            {
                "emoji": "🎓",
                "title": "Student Average & Grade Calculator",
                "xp": 35,
                "difficulty": "MEDIUM",
                "description": (
                    "Calculate a student's average marks "
                    "and determine their grade."
                ),
                "intro": (
                    "A school wants a simple result calculator. "
                    "It should calculate the average marks of a student "
                    "and assign a grade based on the result."
                ),
                "mission": (
                    "Receive marks in three subjects, calculate "
                    "the average, and display the corresponding grade."
                ),
                "tasks": [
                    "Create a START node.",
                    "Ask for marks in three subjects and store them as mark1, mark2 and mark3.",
                    "Calculate the total marks.",
                    "Calculate the average by dividing the total by 3.",
                    "Display the average.",
                    "Check whether the average is greater than or equal to 90. If TRUE, display Grade A.",
                    "Otherwise, check whether the average is greater than or equal to 75. If TRUE, display Grade B.",
                    "Otherwise, check whether the average is greater than or equal to 60. If TRUE, display Grade C.",
                    "Otherwise, display Grade D.",
                    "Connect all paths to END."
                ],
                "concepts": [
                    "Variables",
                    "Arithmetic operations",
                    "Conditions",
                    "Nested branching",
                    "Output"
                ],
                "tests": [
                    "90, 95, 85 → Average 90, Grade A.",
                    "75, 80, 70 → Average 75, Grade B.",
                    "60, 65, 55 → Average 60, Grade C.",
                    "40, 45, 50 → Average 45, Grade D."
                ]
            },
            {
                "emoji": "📐",
                "title": "Rectangle Calculator",
                "xp": 20,
                "difficulty": "EASY",
                "description": (
                    "Calculate the area and perimeter of a rectangle."
                ),
                "intro": (
                    "You're developing a small geometry utility. "
                    "The user enters the length and width of a rectangle, "
                    "and the program calculates its measurements."
                ),
                "mission": (
                    "Receive the rectangle's length and width, "
                    "calculate its area and perimeter, and display "
                    "both results."
                ),
                "tasks": [
                    "Create a START node.",
                    "Ask the user for the rectangle's length. Store it as length.",
                    "Ask for the width. Store it as width.",
                    "Calculate area = length × width.",
                    "Calculate perimeter = 2 × (length + width).",
                    "Store both results in separate variables.",
                    "Display the area and perimeter.",
                    "Connect all nodes and run the program."
                ],
                "concepts": [
                    "Variables",
                    "Input",
                    "Arithmetic operations",
                    "Output"
                ],
                "tests": [
                    "Length 10, width 5 → Area 50, perimeter 30.",
                    "Length 8, width 4 → Area 32, perimeter 24.",
                    "Length 6, width 3 → Area 18, perimeter 18."
                ]
            }
        ]

        self.challenge_page = QStackedWidget()

        # OVERVIEW PAGE
        overview = QWidget()
        root = QVBoxLayout(overview)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(14)

        heading = QLabel("Programming Challenges")
        heading.setStyleSheet(
            "font-size: 25px; font-weight: bold;"
        )
        root.addWidget(heading)

        description = QLabel(
            "Put your programming knowledge into practice. "
            "Complete these five challenges using LogicFlow."
        )
        description.setObjectName("Muted")
        description.setWordWrap(True)
        root.addWidget(description)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.challenge_list_layout = QVBoxLayout(content)
        self.challenge_list_layout.setContentsMargins(4, 4, 12, 12)
        self.challenge_list_layout.setSpacing(12)

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

        for index, challenge in enumerate(self.challenges):
            card = QFrame()
            polish_learning_card(card)

            layout = QHBoxLayout(card)
            layout.setContentsMargins(16, 15, 16, 15)
            layout.setSpacing(14)

            emoji = QLabel(challenge["emoji"])
            emoji.setFixedWidth(42)
            emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
            emoji.setStyleSheet("font-size: 27px;")

            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)

            title = QLabel(
                f"{index + 1:02d}  {challenge['title']}"
            )
            title.setWordWrap(True)
            title.setStyleSheet(
                "font-size: 15px; font-weight: bold;"
            )

            description = QLabel(challenge["description"])
            description.setWordWrap(True)
            description.setObjectName("Muted")

            metadata = QLabel(
                f"{challenge['xp']} XP     •     "
                f"{challenge['difficulty']}"
            )
            metadata.setStyleSheet(
                "font-size: 11px; font-weight: bold; color: #60A5FA;"
            )

            text_layout.addWidget(title)
            text_layout.addWidget(description)
            text_layout.addWidget(metadata)

            button = QPushButton("Start Challenge  →")
            button.setFixedWidth(145)
            button.clicked.connect(
                lambda checked=False, i=index:
                self.open_challenge_details(i)
            )

            layout.addWidget(emoji)
            layout.addLayout(text_layout, 1)
            layout.addWidget(button)

            self.challenge_list_layout.addWidget(card)

        self.challenge_list_layout.addStretch(1)

        self.challenge_page.addWidget(overview)

        # DETAILS PAGE
        self.challenge_details_page = QWidget()
        details_root = QVBoxLayout(self.challenge_details_page)
        details_root.setContentsMargins(18, 16, 18, 16)
        details_root.setSpacing(12)

        header = QHBoxLayout()

        back_button = QPushButton("← Challenges")
        back_button.clicked.connect(self.show_challenges)

        self.challenge_detail_heading = QLabel("Challenge")
        self.challenge_detail_heading.setStyleSheet(
            "font-size: 19px; font-weight: bold;"
        )

        header.addWidget(back_button)
        header.addWidget(self.challenge_detail_heading, 1)

        details_root.addLayout(header)

        self.challenge_details_scroll = QScrollArea()
        self.challenge_details_scroll.setWidgetResizable(True)
        self.challenge_details_scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.challenge_details_content = QWidget()
        self.challenge_details_layout = QVBoxLayout(
            self.challenge_details_content
        )
        self.challenge_details_layout.setContentsMargins(
            4, 4, 12, 12
        )
        self.challenge_details_layout.setSpacing(14)

        self.challenge_details_scroll.setWidget(
            self.challenge_details_content
        )

        details_root.addWidget(
            self.challenge_details_scroll, 1
        )

        footer = QHBoxLayout()

        self.challenge_back_button = QPushButton(
            "← Back to Challenges"
        )
        self.challenge_back_button.clicked.connect(
            self.show_challenges
        )

        self.challenge_editor_button = QPushButton(
            "Open Logic Editor  →"
        )
        self.challenge_editor_button.setObjectName("RunButton")
        self.challenge_editor_button.clicked.connect(
    lambda: self.challenge_editor_requested.emit()
)

        footer.addWidget(self.challenge_back_button)
        footer.addStretch()
        footer.addWidget(self.challenge_editor_button)

        details_root.addLayout(footer)

        self.challenge_page.addWidget(
            self.challenge_details_page
        )

    def open_challenge_details(self, index):
        if not 0 <= index < len(self.challenges):
            return

        self.active_challenge = index
        challenge = self.challenges[index]

        self.challenge_detail_heading.setText(
            f"{index + 1:02d}  {challenge['title']}"
        )

        while self.challenge_details_layout.count():
            item = self.challenge_details_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        title = QLabel(
            f"{challenge['emoji']}  {challenge['title']}"
        )
        title.setWordWrap(True)
        title.setStyleSheet(
            "font-size: 25px; font-weight: bold; color: #E5E7EB;"
        )

        metadata = QLabel(
            f"{challenge['xp']} XP REWARD     •     "
            f"{challenge['difficulty']} DIFFICULTY"
        )
        metadata.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #60A5FA;"
        )

        self.challenge_details_layout.addWidget(title)
        self.challenge_details_layout.addWidget(metadata)

        self.challenge_details_layout.addWidget(
            self.create_card(
                "THE SCENARIO",
                challenge["intro"],
                "#FBBF24"
            )
        )

        self.challenge_details_layout.addWidget(
            self.create_card(
                "YOUR MISSION",
                challenge["mission"],
                "#60A5FA"
            )
        )

        instructions = [
            f"{i + 1}. {task}"
            for i, task in enumerate(challenge["tasks"])
        ]

        self.challenge_details_layout.addWidget(
            self.create_example_card(
                "BUILD INSTRUCTIONS",
                instructions
            )
        )

        self.challenge_details_layout.addWidget(
            self.create_example_card(
                "CONCEPTS YOU WILL USE",
                [
                    f"• {concept}"
                    for concept in challenge["concepts"]
                ]
            )
        )

        self.challenge_details_layout.addWidget(
            self.create_example_card(
                "TEST YOUR PROGRAM",
                [
                    f"• {test}"
                    for test in challenge["tests"]
                ]
            )
        )

        self.challenge_details_layout.addWidget(
            self.create_card(
                "READY TO BUILD?",
                "When you're ready, open the Logic Editor and "
                "construct your solution. Test it using the cases "
                "provided above.",
                "#6EE7B7"
            )
        )

        self.challenge_details_layout.addStretch(1)

        self.challenge_details_scroll.verticalScrollBar().setValue(0)

        self.challenge_page.setCurrentWidget(
            self.challenge_details_page
        )

    def show_challenges(self):
        self.challenge_page.setCurrentIndex(0)
        return self.challenge_page