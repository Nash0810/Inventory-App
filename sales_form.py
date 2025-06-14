from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox,
                               QPushButton, QComboBox, QMessageBox, QFileDialog, QFormLayout)
from PySide6.QtCore import Qt
from database import get_db_connection
from reportlab.pdfgen import canvas
import datetime


class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        self.setFixedSize(450, 550)
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Product selection
        self.product_dropdown = QComboBox()
        self.product_dropdown.currentTextChanged.connect(self.on_product_changed)
        form_layout.addRow("Select Product:", self.product_dropdown)

        # Customer details
        self.customer = QLineEdit()
        self.customer.setPlaceholderText("Enter customer name/details")
        form_layout.addRow("Customer Details:", self.customer)

        # Quantity
        self.qty = QDoubleSpinBox()
        self.qty.setMaximum(99999)
        self.qty.setDecimals(2)
        self.qty.valueChanged.connect(self.calculate_total)
        form_layout.addRow("Quantity:", self.qty)

        # Unit
        self.unit = QComboBox()
        self.unit.addItems(["pcs", "kg", "litre", "box", "meter", "dozen"])
        form_layout.addRow("Unit:", self.unit)

        # Rate per unit
        self.rate = QDoubleSpinBox()
        self.rate.setMaximum(999999)
        self.rate.setDecimals(2)
        self.rate.valueChanged.connect(self.calculate_total)
        form_layout.addRow("Rate per Unit (₹):", self.rate)

        # Tax
        self.tax = QDoubleSpinBox()
        self.tax.setMaximum(100)
        self.tax.setDecimals(2)
        self.tax.setSuffix("%")
        self.tax.valueChanged.connect(self.calculate_total)
        form_layout.addRow("Tax Rate:", self.tax)

        # Totals (read-only)
        self.subtotal_label = QLabel("Subtotal: ₹0.00")
        self.tax_amount_label = QLabel("Tax Amount: ₹0.00")
        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")

        form_layout.addRow("", self.subtotal_label)
        form_layout.addRow("", self.tax_amount_label)
        form_layout.addRow("", self.total_label)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QVBoxLayout()

        #self.calculate_btn = QPushButton("🧮 Calculate Total")
        #self.calculate_btn.clicked.connect(self.calculate_total)
        #self.calculate_btn.setStyleSheet("QPushButton { padding: 8px; }")

        self.save_btn = QPushButton("💾 Save & Generate Invoice")
        self.save_btn.clicked.connect(self.save_and_generate_invoice)
        self.save_btn.setStyleSheet("QPushButton { padding: 10px; background-color: #4CAF50; color: white; }")

        self.clear_btn = QPushButton("🗑️ Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setStyleSheet("QPushButton { padding: 8px; }")

        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_products(self):
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, name, price, tax, unit FROM product_master ORDER BY name")
            self.products = c.fetchall()
            conn.close()

            self.product_dropdown.clear()
            self.product_dropdown.addItem("-- Select Product --", None)
            for pid, name, price, tax, unit in self.products:
                self.product_dropdown.addItem(f"{name} (₹{price})", (pid, price, tax, unit))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")

    def on_product_changed(self):
        current_data = self.product_dropdown.currentData()
        if current_data and current_data != None:
            pid, price, tax, unit = current_data
            self.rate.setValue(price)
            self.tax.setValue(tax)
            # Set unit to match product default
            unit_index = self.unit.findText(unit)
            if unit_index >= 0:
                self.unit.setCurrentIndex(unit_index)
            self.calculate_total()

    def calculate_total(self):
        try:
            qty = self.qty.value()
            rate = self.rate.value()
            tax_rate = self.tax.value()

            subtotal = qty * rate
            tax_amount = subtotal * tax_rate / 100
            total = subtotal + tax_amount

            self.subtotal_label.setText(f"Subtotal: ₹{subtotal:.2f}")
            self.tax_amount_label.setText(f"Tax Amount: ₹{tax_amount:.2f}")
            self.total_label.setText(f"Total: ₹{total:.2f}")

        except Exception as e:
            self.subtotal_label.setText("Subtotal: ₹0.00")
            self.tax_amount_label.setText("Tax Amount: ₹0.00")
            self.total_label.setText("Total: ₹0.00")

    def save_and_generate_invoice(self):
        try:
            product_data = self.product_dropdown.currentData()
            customer = self.customer.text().strip()
            qty = self.qty.value()
            unit = self.unit.currentText()
            rate = self.rate.value()
            tax_rate = self.tax.value()

            if not product_data or product_data is None:
                QMessageBox.warning(self, "Validation", "Please select a product.")
                return

            if not customer:
                QMessageBox.warning(self, "Validation", "Please enter customer details.")
                return

            if qty <= 0:
                QMessageBox.warning(self, "Validation", "Quantity must be greater than 0.")
                return

            product_id = product_data[0]
            subtotal = qty * rate
            tax_amount = subtotal * tax_rate / 100
            total = subtotal + tax_amount
            sale_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Save to database
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("""
                INSERT INTO sales (product_id, customer, quantity, unit, rate, tax, total, sale_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (product_id, customer, qty, unit, rate, tax_rate, total, sale_date))
            conn.commit()
            conn.close()

            # Generate PDF
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Invoice",
                f"Invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                "PDF Files (*.pdf)"
            )

            if save_path:
                self.generate_pdf(save_path, customer, qty, unit, rate, tax_rate, total, sale_date)
                QMessageBox.information(self, "Success", "Sale saved and invoice generated successfully!")
                self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save sale: {e}")

    def generate_pdf(self, filepath, customer, qty, unit, rate, tax_rate, total, sale_date):
        try:
            c = canvas.Canvas(filepath)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 800, "SALES INVOICE")

            c.setFont("Helvetica", 12)
            y_pos = 770
            c.drawString(50, y_pos, f"Date: {sale_date}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Customer: {customer}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Product: {self.product_dropdown.currentText().split(' (₹')[0]}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Quantity: {qty} {unit}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Rate per {unit}: ₹{rate:.2f}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Subtotal: ₹{(qty * rate):.2f}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Tax ({tax_rate}%): ₹{((qty * rate) * tax_rate / 100):.2f}")
            y_pos -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_pos, f"Total Amount: ₹{total:.2f}")

            c.save()
        except Exception as e:
            QMessageBox.critical(self, "PDF Error", f"Failed to generate PDF: {e}")

    def clear_form(self):
        self.product_dropdown.setCurrentIndex(0)
        self.customer.clear()
        self.qty.setValue(0)
        self.rate.setValue(0)
        self.tax.setValue(0)
        self.unit.setCurrentIndex(0)
        self.subtotal_label.setText("Subtotal: ₹0.00")
        self.tax_amount_label.setText("Tax Amount: ₹0.00")
        self.total_label.setText("Total: ₹0.00")
