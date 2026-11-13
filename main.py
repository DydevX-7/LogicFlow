
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from ui.branding import (
    create_app_icon,
    create_splash_screen,
)

from ui.auth_screen import AuthScreen
from auth.auth_manager import AuthManager


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("LogicFlow")
    app.setApplicationDisplayName("LogicFlow")
    app.setOrganizationName("LogicFlow")

    app_icon = create_app_icon()
    app.setWindowIcon(app_icon)

    splash = create_splash_screen()

    splash.set_progress(
        0,
        "Starting LogicFlow..."
    )

    app.processEvents()

    try:

        auth_manager = AuthManager()

        auth_screen = AuthScreen(auth_manager)
        auth_screen.setWindowIcon(app_icon)

    except Exception as error:

        splash.close()

        QMessageBox.critical(
            None,
            "LogicFlow Startup Error",
            f"Could not initialize LogicFlow:\n\n{error}"
        )

        return 1

    splash.set_progress(
        10,
        "Loading local accounts..."
    )

    app.processEvents()

    main_window = None

    def return_to_login():

        nonlocal main_window

        auth_screen.show_login_page()

        auth_screen.show()
        auth_screen.raise_()
        auth_screen.activateWindow()

        if main_window is not None:
            main_window.deleteLater()
            main_window = None

    def open_main_window(username):

        nonlocal main_window

        try:

            from ui.main_window import MainWindow

            main_window = MainWindow(
                username=username
            )

            main_window.setWindowIcon(app_icon)

            main_window.logout_requested.connect(
                return_to_login
            )

            main_window.show()

            auth_screen.hide()

        except Exception as error:

            main_window = None

            auth_screen.show()

            QMessageBox.critical(
                auth_screen,
                "Application Error",
                f"Could not open LogicFlow:\n\n{error}"
            )

    auth_screen.authenticated.connect(
        open_main_window
    )

    def finish_startup():

        auth_screen.show()
        splash.finish(auth_screen)

    splash.animation.finished.connect(
        finish_startup
    )

    splash.animate_to_completion()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
