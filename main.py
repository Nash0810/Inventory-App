import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from database import init_db
from login import LoginWindow


def main():
    # Initialize database
    init_db()

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Inventory Management System")
    app.setApplicationVersion("1.0")

    # Create and show login window
    login_window = LoginWindow()
    login_window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()