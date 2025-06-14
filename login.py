from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database import get_db_connection


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management - Login")
        self.setFixedSize(350, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Inventory Management System")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        layout.addWidget(self.username)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Enter password")
        layout.addWidget(self.password)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet("QPushButton { padding: 8px; font-size: 12px; }")
        layout.addWidget(login_btn)

        # Sample credentials info
        info_label = QLabel("Sample Logins:\nAdmin: admin/admin123\nOperator: operator1/pass123")
        info_label.setStyleSheet("font-size: 10px; color: gray; margin-top: 10px;")
        layout.addWidget(info_label)

        self.setLayout(layout)

        # Allow Enter key to login
        self.password.returnPressed.connect(self.login)

    def login(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()

        if not user or not pwd:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM operators WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            user_id, username, password, role = result
            self.hide()
            from menu import MenuWindow
            self.menu = MenuWindow(role=role, username=username)
            self.menu.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            self.password.clear()