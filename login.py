from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from database import get_db_connection, init_db
from menu import MenuWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operator Login")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        self.setLayout(layout)



    def login(self):
        user = self.username.text()
        pwd = self.password.text()
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM operators WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.hide()
            self.menu = MenuWindow(role=role)
            self.menu.show()

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")