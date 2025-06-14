from PySide6.QtWidgets import QApplication
from login import LoginWindow
import sys
from database import init_db

init_db()
app = QApplication(sys.argv)
login = LoginWindow()
login.show()
sys.exit(app.exec())
