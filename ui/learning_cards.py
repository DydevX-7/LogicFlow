
from PySide6.QtWidgets import QFrame


def polish_learning_card(card: QFrame):
    """Apply LogicFlow's polished interactive card styling."""

    card.setObjectName("LearningCard")
    card.setFrameShape(QFrame.Shape.NoFrame)

    card.setStyleSheet("""
        QFrame#LearningCard {
            background-color: #191F2B;
            border: 1px solid #303B4D;
            border-radius: 13px;
        }

        QFrame#LearningCard:hover {
            background-color: #202B3B;
            border: 1px solid #4B83C5;
        }
    """)
