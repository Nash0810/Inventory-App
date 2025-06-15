from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QDoubleSpinBox, QDateEdit, QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PySide6.QtCore import QDate
from database import get_db_connection


class GoodsReceivingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving Form")
        self.setFixedSize(450, 500)
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Product Selection (FIXED: Dropdown instead of manual ID entry)
        self.product_dropdown = QComboBox()
        self.product_dropdown.currentIndexChanged.connect(self.on_product_changed)
        form_layout.addRow("Select Product:", self.product_dropdown)

        # Display selected product info
        self.product_info = QLabel("No product selected")
        self.product_info.setStyleSheet("color: #666; font-style: italic;")
        form_layout.addRow("Product Info:", self.product_info)

        # Supplier Name
        self.supplier = QLineEdit()
        self.supplier.setPlaceholderText("Enter supplier name")
        form_layout.addRow("Supplier Name:", self.supplier)

        # Quantity
        self.quantity = QDoubleSpinBox()
        self.quantity.setMaximum(999999)
        self.quantity.setDecimals(2)
        self.quantity.valueChanged.connect(self.update_total)
        form_layout.addRow("Quantity:", self.quantity)

        # Unit (auto-filled from product, but editable)
        self.unit = QComboBox()
        self.unit.setEditable(True)
        self.unit.addItems(["kg", "litre", "pcs", "box", "meter", "dozen"])
        form_layout.addRow("Unit of Measurement:", self.unit)

        # Rate per unit
        self.rate = QDoubleSpinBox()
        self.rate.setMaximum(999999)
        self.rate.setDecimals(2)
        self.rate.valueChanged.connect(self.update_total)
        form_layout.addRow("Rate per Unit (₹):", self.rate)

        # Tax percentage
        self.tax_rate = QDoubleSpinBox()
        self.tax_rate.setMaximum(100)
        self.tax_rate.setDecimals(2)
        self.tax_rate.setSuffix("%")
        self.tax_rate.valueChanged.connect(self.update_total)
        form_layout.addRow("Tax Rate:", self.tax_rate)

        # Calculated fields (read-only)
        self.subtotal = QLineEdit()
        self.subtotal.setReadOnly(True)
        self.subtotal.setStyleSheet("background-color: #f0f0f0;")
        form_layout.addRow("Subtotal (₹):", self.subtotal)

        self.tax_amount = QLineEdit()
        self.tax_amount.setReadOnly(True)
        self.tax_amount.setStyleSheet("background-color: #f0f0f0;")
        form_layout.addRow("Tax Amount (₹):", self.tax_amount)

        self.total = QLineEdit()
        self.total.setReadOnly(True)
        self.total.setStyleSheet("background-color: #f0f0f0; font-weight: bold;")
        form_layout.addRow("Total Amount (₹):", self.total)

        # Date
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        form_layout.addRow("Receiving Date:", self.date)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QVBoxLayout()

        self.save_btn = QPushButton("💾 Save Goods Receiving")
        self.save_btn.clicked.connect(self.save_entry)
        self.save_btn.setStyleSheet("QPushButton { padding: 10px; background-color: #4CAF50; color: white; }")

        self.clear_btn = QPushButton("🗑️ Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setStyleSheet("QPushButton { padding: 8px; }")

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_products(self):
        """Load products from database into dropdown"""
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, name, sku, price, tax, unit FROM product_master ORDER BY name")
            self.products = c.fetchall()
            conn.close()

            self.product_dropdown.clear()
            self.product_dropdown.addItem("-- Select Product --", None)

            for product_id, name, sku, price, tax, unit in self.products:
                display_text = f"{name} (SKU: {sku})"
                self.product_dropdown.addItem(display_text, {
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'price': price,
                    'tax': tax,
                    'unit': unit
                })

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")

    def on_product_changed(self):
        """Handle product selection change"""
        current_data = self.product_dropdown.currentData()
        if current_data:
            # Auto-fill product information
            self.product_info.setText(f"SKU: {current_data['sku']} | Suggested Price: ₹{current_data['price']}")

            # Set default values from product master
            self.rate.setValue(current_data['price'])
            self.tax_rate.setValue(current_data['tax'])

            # Set unit
            unit_index = self.unit.findText(current_data['unit'])
            if unit_index >= 0:
                self.unit.setCurrentIndex(unit_index)

            self.update_total()
        else:
            self.product_info.setText("No product selected")
            self.clear_calculations()

    def update_total(self):
        """Calculate and display totals"""
        try:
            qty = self.quantity.value()
            rate = self.rate.value()
            tax_rate = self.tax_rate.value()

            subtotal_amount = qty * rate
            tax_amount_value = subtotal_amount * tax_rate / 100
            total_amount = subtotal_amount + tax_amount_value

            self.subtotal.setText(f"{subtotal_amount:.2f}")
            self.tax_amount.setText(f"{tax_amount_value:.2f}")
            self.total.setText(f"{total_amount:.2f}")

        except Exception:
            self.clear_calculations()

    def clear_calculations(self):
        """Clear all calculated fields"""
        self.subtotal.clear()
        self.tax_amount.clear()
        self.total.clear()

    def save_entry(self):
        """Save goods receiving entry to database"""
        try:
            # Validation
            product_data = self.product_dropdown.currentData()
            supplier = self.supplier.text().strip()
            qty = self.quantity.value()
            rate = self.rate.value()

            if not product_data:
                QMessageBox.warning(self, "Validation Error", "Please select a product.")
                return
            if not supplier:
                QMessageBox.warning(self, "Validation Error", "Please enter supplier name.")
                return
            if qty <= 0:
                QMessageBox.warning(self, "Validation Error", "Quantity must be greater than 0.")
                return
            if rate <= 0:
                QMessageBox.warning(self, "Validation Error", "Rate must be greater than 0.")
                return

            # Calculate final values
            subtotal_amount = qty * rate
            tax_rate = self.tax_rate.value()
            tax_amount_value = subtotal_amount * tax_rate / 100
            total_amount = subtotal_amount + tax_amount_value

            # Get other values
            product_id = product_data['id']
            unit = self.unit.currentText()
            date_str = self.date.date().toString("yyyy-MM-dd")

            # Save to database
            conn = get_db_connection()
            c = conn.cursor()

            c.execute("""
                INSERT INTO goods_receiving 
                (product_id, supplier, quantity, unit, rate, total, tax, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (product_id, supplier, qty, unit, rate, total_amount, tax_rate, date_str))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Goods receiving entry saved successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry: {e}")

    def clear_form(self):
        """Clear all form fields"""
        self.product_dropdown.setCurrentIndex(0)
        self.supplier.clear()
        self.quantity.setValue(0)
        self.rate.setValue(0)
        self.tax_rate.setValue(0)
        self.unit.setCurrentIndex(0)
        self.date.setDate(QDate.currentDate())
        self.product_info.setText("No product selected")
        self.clear_calculations()