from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox,
                                 QPushButton, QComboBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt
from database import get_db_connection
from reportlab.pdfgen import canvas
import os
import datetime

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        self.product_dropdown = QComboBox()
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, name FROM product_master")
        self.products = c.fetchall()
        conn.close()

        for pid, name in self.products:
            self.product_dropdown.addItem(name, pid)

        self.customer = QLineEdit()
        layout.addWidget(QLabel("Customer Details"))
        layout.addWidget(self.customer)

        self.qty = QDoubleSpinBox()
        self.qty.setMaximum(99999)
        layout.addWidget(QLabel("Quantity"))
        layout.addWidget(self.qty)

        self.unit = QComboBox()
        self.unit.addItems(["kg", "litre", "pcs", "box"])
        layout.addWidget(QLabel("Unit of Measurement"))
        layout.addWidget(self.unit)

        self.rate = QDoubleSpinBox()
        self.rate.setMaximum(999999)
        layout.addWidget(QLabel("Rate per Unit"))
        layout.addWidget(self.rate)

        self.tax = QDoubleSpinBox()
        self.tax.setMaximum(100)
        layout.addWidget(QLabel("Tax %"))
        layout.addWidget(self.tax)

        self.total = QLabel("Total: ₹0.00")
        layout.addWidget(self.total)

        self.calculate_btn = QPushButton("Calculate Total")
        self.calculate_btn.clicked.connect(self.calculate_total)
        layout.addWidget(self.calculate_btn)

        self.save_btn = QPushButton("Save & Generate Invoice")
        self.save_btn.clicked.connect(self.save_and_generate_invoice)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def calculate_total(self):
        subtotal = self.qty.value() * self.rate.value()
        tax_amount = subtotal * self.tax.value() / 100
        total_amount = subtotal + tax_amount
        self.total.setText(f"Total: ₹{total_amount:.2f}")

    def save_and_generate_invoice(self):
        try:
            product = self.product_dropdown.currentData()
            customer = self.customer.text().strip()
            qty = self.qty.value()
            unit = self.unit.currentText()
            rate = self.rate.value()
            tax = self.tax.value()
            subtotal = qty * rate
            tax_amount = subtotal * tax / 100
            total = subtotal + tax_amount

            if not product or not customer:
                QMessageBox.warning(self, "Validation", "Customer and Product details are required.")
                return

            # Save to DB (optional)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("""
                INSERT INTO sales (product_id, customer, quantity, unit, rate, tax, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (product, customer, qty, unit, rate, tax, total))
            conn.commit()
            conn.close()

            # Ask location to save
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Invoice", f"Invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", "PDF Files (*.pdf)")
            if save_path:
                self.generate_pdf(save_path, product, customer, qty, unit, rate, tax, total)
                QMessageBox.information(self, "Invoice Saved", "PDF invoice created successfully.")
                self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save or export: {e}")

    def generate_pdf(self, filepath, product, customer, qty, unit, rate, tax, total):
        c = canvas.Canvas(filepath)
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, f"INVOICE")
        c.drawString(50, 780, f"Customer: {customer}")
        c.drawString(50, 760, f"Product: {product}")
        c.drawString(50, 740, f"Quantity: {qty} {unit}")
        c.drawString(50, 720, f"Rate: ₹{rate:.2f}")
        c.drawString(50, 700, f"Tax: {tax:.2f}%")
        c.drawString(50, 680, f"Total: ₹{total:.2f}")
        c.drawString(50, 660, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.save()

    def clear_form(self):
        self.product.clear()
        self.customer.clear()
        self.qty.setValue(0)
        self.rate.setValue(0)
        self.tax.setValue(0)
        self.total.setText("Total: ₹0.00")
