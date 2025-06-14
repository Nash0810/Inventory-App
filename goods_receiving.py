from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QDoubleSpinBox, QDateEdit, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate
from database import get_db_connection

class GoodsReceivingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving Form")
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()

        # Product ID
        self.product_id = QLineEdit()
        layout.addWidget(QLabel("Product ID"))
        layout.addWidget(self.product_id)

        # Supplier Name
        self.supplier = QLineEdit()
        layout.addWidget(QLabel("Supplier Name"))
        layout.addWidget(self.supplier)

        # Quantity
        self.quantity = QDoubleSpinBox()
        self.quantity.setMaximum(999999)
        layout.addWidget(QLabel("Quantity"))
        layout.addWidget(self.quantity)

        # Unit
        self.unit = QComboBox()
        self.unit.addItems(["kg", "litre", "pcs", "box"])
        layout.addWidget(QLabel("Unit of Measurement"))
        layout.addWidget(self.unit)

        # Rate
        self.rate = QDoubleSpinBox()
        self.rate.setMaximum(999999)
        layout.addWidget(QLabel("Rate per Unit"))
        layout.addWidget(self.rate)

        # Total (read-only)
        self.total = QLineEdit()
        self.total.setReadOnly(True)
        layout.addWidget(QLabel("Total Rate"))
        layout.addWidget(self.total)

        # Tax
        self.tax = QDoubleSpinBox()
        self.tax.setMaximum(100)
        layout.addWidget(QLabel("Tax %"))
        layout.addWidget(self.tax)

        # Date
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Date"))
        layout.addWidget(self.date)

        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_entry)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # Update total when qty or rate changes
        self.quantity.valueChanged.connect(self.update_total)
        self.rate.valueChanged.connect(self.update_total)

    def update_total(self):
        qty = self.quantity.value()
        rate = self.rate.value()
        total = qty * rate
        self.total.setText(f"{total:.2f}")

    def save_entry(self):
        try:
            pid = self.product_id.text().strip()
            supplier = self.supplier.text().strip()
            unit = self.unit.currentText()
            qty = self.quantity.value()
            rate = self.rate.value()
            total = float(self.total.text()) if self.total.text() else 0
            tax = self.tax.value()
            date_str = self.date.date().toString("yyyy-MM-dd")

            if not pid or not supplier:
                QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
                return

            conn = get_db_connection()
            c = conn.cursor()
            c.execute("""
                INSERT INTO goods_receiving
                (product_id, supplier, quantity, unit, rate, total, tax, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (pid, supplier, qty, unit, rate, total, tax, date_str))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Entry saved successfully.")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong: {e}")

    def clear_form(self):
        self.product_id.clear()
        self.supplier.clear()
        self.quantity.setValue(0)
        self.rate.setValue(0)
        self.total.clear()
        self.tax.setValue(0)
        self.date.setDate(QDate.currentDate())
