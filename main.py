from PySide6.QtWidgets import QApplication
from login import LoginWindow
import sys

app = QApplication(sys.argv)
login = LoginWindow()
login.show()
sys.exit(app.exec())
