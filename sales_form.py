from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox
from database import get_db_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        layout = QFormLayout()

        self.product_id = QLineEdit()
        self.customer = QLineEdit()
        self.quantity = QLineEdit()
        self.unit = QComboBox()
        self.unit.addItems(["kg", "pcs", "liters"])
        self.rate = QLineEdit()
        self.total = QLineEdit()
        self.tax = QLineEdit()

        submit = QPushButton("Submit")
        submit.clicked.connect(self.submit_form)

        layout.addRow("Product ID", self.product_id)
        layout.addRow("Customer", self.customer)
        layout.addRow("Quantity", self.quantity)
        layout.addRow("Unit", self.unit)
        layout.addRow("Rate", self.rate)
        layout.addRow("Total", self.total)
        layout.addRow("Tax", self.tax)
        layout.addRow(submit)
        self.setLayout(layout)

    def submit_form(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO sales (product_id, customer, quantity, unit, rate, total, tax)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (self.product_id.text(), self.customer.text(), self.quantity.text(),
                   self.unit.currentText(), self.rate.text(), self.total.text(), self.tax.text()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Sales Entry Saved")
