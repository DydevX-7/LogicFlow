
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    QVariantAnimation,
    QEasingCurve,
)
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QColor,
    QPen,
    QBrush,
    QLinearGradient,
    QFont,
    QPainterPath,
    QIcon,
)
from PySide6.QtWidgets import QSplashScreen


# ==========================================
# LOGICFLOW LOGO
# ==========================================

def create_logo_pixmap(size=256):
    """Create the LogicFlow application logo."""

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    margin = size * 0.06

    rect = QRectF(
        margin,
        margin,
        size - margin * 2,
        size - margin * 2
    )

    gradient = QLinearGradient(
        rect.topLeft(),
        rect.bottomRight()
    )

    gradient.setColorAt(0, QColor("#2563EB"))
    gradient.setColorAt(1, QColor("#06B6D4"))

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(gradient))

    painter.drawRoundedRect(
        rect,
        size * 0.20,
        size * 0.20
    )

    # Flowchart connections
    pen = QPen(
        QColor("#FFFFFF"),
        size * 0.035
    )

    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    path = QPainterPath()

    path.moveTo(size * 0.36, size * 0.31)
    path.lineTo(size * 0.36, size * 0.48)
    path.lineTo(size * 0.64, size * 0.48)
    path.lineTo(size * 0.64, size * 0.66)

    painter.drawPath(path)

    # Branch connection
    branch = QPainterPath()

    branch.moveTo(size * 0.36, size * 0.48)
    branch.lineTo(size * 0.36, size * 0.68)

    painter.drawPath(branch)

    # Flowchart nodes
    node_positions = [
        (0.36, 0.29),
        (0.36, 0.48),
        (0.64, 0.48),
        (0.64, 0.68),
        (0.36, 0.68),
    ]

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#FFFFFF"))

    node_size = size * 0.105

    for x, y in node_positions:
        painter.drawEllipse(
            QPointF(size * x, size * y),
            node_size / 2,
            node_size / 2
        )

    painter.end()

    return pixmap


# ==========================================
# APPLICATION ICON
# ==========================================

def create_app_icon():
    """Return the LogicFlow application icon."""

    return QIcon(create_logo_pixmap(256))


# ==========================================
# SPLASH SCREEN DESIGN
# ==========================================

def create_splash_pixmap(
    width=680,
    height=380,
    progress=0,
    message="Initializing LogicFlow..."
):
    """Create the LogicFlow startup screen."""

    progress = max(0, min(100, int(progress)))

    pixmap = QPixmap(width, height)
    pixmap.fill(QColor("#0B1120"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Background gradient
    gradient = QLinearGradient(
        0,
        0,
        width,
        height
    )

    gradient.setColorAt(0, QColor("#0B1120"))
    gradient.setColorAt(1, QColor("#172554"))

    painter.fillRect(
        0,
        0,
        width,
        height,
        QBrush(gradient)
    )

    # Background grid
    grid_pen = QPen(
        QColor(255, 255, 255, 12),
        1
    )

    painter.setPen(grid_pen)

    for x in range(0, width, 40):
        painter.drawLine(x, 0, x, height)

    for y in range(0, height, 40):
        painter.drawLine(0, y, width, y)

    # Logo
    logo = create_logo_pixmap(112)

    painter.drawPixmap(
        (width - 112) // 2,
        48,
        logo
    )

    # Application name
    painter.setPen(QColor("#FFFFFF"))

    painter.setFont(
        QFont(
            "Segoe UI",
            32,
            QFont.Weight.Bold
        )
    )

    painter.drawText(
        QRectF(0, 170, width, 55),
        Qt.AlignmentFlag.AlignCenter,
        "LogicFlow"
    )

    # Tagline
    painter.setPen(QColor("#94A3B8"))
    painter.setFont(QFont("Segoe UI", 11))

    painter.drawText(
        QRectF(0, 225, width, 30),
        Qt.AlignmentFlag.AlignCenter,
        "Think visually. Learn logically. Build confidently."
    )

    # Startup message
    painter.setPen(QColor("#CBD5E1"))
    painter.setFont(QFont("Segoe UI", 10))

    painter.drawText(
        QRectF(150, 275, 380, 22),
        Qt.AlignmentFlag.AlignLeft,
        message
    )

    # Percentage
    painter.setPen(QColor("#38BDF8"))

    painter.setFont(
        QFont(
            "Segoe UI",
            10,
            QFont.Weight.Bold
        )
    )

    painter.drawText(
        QRectF(150, 275, 380, 22),
        Qt.AlignmentFlag.AlignRight,
        f"{progress}%"
    )

    # Progress bar background
    bar_rect = QRectF(
        150,
        305,
        380,
        7
    )

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#334155"))

    painter.drawRoundedRect(
        bar_rect,
        4,
        4
    )

    # Progress bar fill
    fill_width = bar_rect.width() * progress / 100

    if fill_width > 0:
        fill_rect = QRectF(
            bar_rect.x(),
            bar_rect.y(),
            fill_width,
            bar_rect.height()
        )

        bar_gradient = QLinearGradient(
            fill_rect.topLeft(),
            fill_rect.topRight()
        )

        bar_gradient.setColorAt(0, QColor("#2563EB"))
        bar_gradient.setColorAt(1, QColor("#06B6D4"))

        painter.setBrush(QBrush(bar_gradient))

        painter.drawRoundedRect(
            fill_rect,
            4,
            4
        )

    # Footer
    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Segoe UI", 9))

    painter.drawText(
        QRectF(0, 340, width, 20),
        Qt.AlignmentFlag.AlignCenter,
        "LOGICFLOW DESKTOP  •  VERSION 1.0"
    )

    painter.end()

    return pixmap


# ==========================================
# ANIMATED SPLASH SCREEN
# ==========================================

class LogicFlowSplash(QSplashScreen):
    """Splash screen with smooth animated progress."""

    def __init__(self):
        super().__init__(
            create_splash_pixmap(),
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint,
            True
        )

        self.progress = 0
        self.message = "Initializing LogicFlow..."

        # Progress animation
        self.animation = QVariantAnimation(self)

        self.animation.setDuration(4000)

        self.animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        self.animation.valueChanged.connect(
            self._update_animation
        )

    def _update_animation(self, value):
        """Update progress during animation."""

        self.set_progress(value)

    def set_progress(self, value, message=None):
        """Update splash screen progress and message."""

        self.progress = max(
            0,
            min(100, int(value))
        )

        if message is not None:
            self.message = message

        updated_pixmap = create_splash_pixmap(
            progress=self.progress,
            message=self.message
        )

        self.setPixmap(updated_pixmap)
        self.repaint()

    def animate_to_completion(self):
        """Animate smoothly from the current progress to 100%."""

        self.animation.stop()

        self.animation.setStartValue(self.progress)
        self.animation.setEndValue(100)

        self.message = "Preparing your workspace..."

        self.animation.start()


# ==========================================
# SPLASH SCREEN CREATOR
# ==========================================

def create_splash_screen():
    """Create and display the LogicFlow splash screen."""

    splash = LogicFlowSplash()
    splash.show()

    return splash
