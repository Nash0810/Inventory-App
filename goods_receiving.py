from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox
from database import get_db_connection

class GoodsReceivingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving Form")
        layout = QFormLayout()

        self.product_id = QLineEdit()
        self.supplier = QLineEdit()
        self.quantity = QLineEdit()
        self.unit = QComboBox()
        self.unit.addItems(["kg", "pcs", "liters"])
        self.rate = QLineEdit()
        self.total = QLineEdit()
        self.tax = QLineEdit()

        submit = QPushButton("Submit")
        submit.clicked.connect(self.submit_form)

        layout.addRow("Product ID", self.product_id)
        layout.addRow("Supplier", self.supplier)
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
        c.execute('''INSERT INTO goods_receiving (product_id, supplier, quantity, unit, rate, total, tax)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (self.product_id.text(), self.supplier.text(), self.quantity.text(),
                   self.unit.currentText(), self.rate.text(), self.total.text(), self.tax.text()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Goods Receiving Entry Saved")