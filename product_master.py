from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QMessageBox, QHeaderView,
                               QDialog, QFormLayout, QLineEdit, QDoubleSpinBox,
                               QComboBox, QTextEdit, QDialogButtonBox, QLabel)
from database import get_db_connection


class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master List")
        self.setFixedSize(900, 600)
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Product Master List")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Barcode", "SKU", "Name", "Category", "Subcategory",
            "Description", "Price (₹)", "Tax (%)", "Unit", "Image"
        ])

        # Make table columns fit content
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Name column
        header.setSectionResizeMode(6, QHeaderView.Stretch)  # Description column

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_products)
        self.refresh_btn.setStyleSheet("QPushButton { padding: 8px; }")

        self.edit_btn = QPushButton("✏️ Edit Selected")
        self.edit_btn.clicked.connect(self.edit_product)
        self.edit_btn.setStyleSheet("QPushButton { padding: 8px; background-color: #2196F3; color: white; }")

        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.clicked.connect(self.delete_product)
        self.delete_btn.setStyleSheet("QPushButton { padding: 8px; background-color: #f44336; color: white; }")

        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_products(self):
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("""SELECT id, barcode, sku, name, category, subcategory, 
                         description, price, tax, unit, image_path FROM product_master ORDER BY name""")
            products = c.fetchall()
            conn.close()

            self.table.setRowCount(len(products))
            for row, product in enumerate(products):
                for col, value in enumerate(product):
                    if col == 10:  # Image path column
                        display_value = "Yes" if value and value.strip() else "No"
                    else:
                        display_value = str(value) if value is not None else ""

                    item = QTableWidgetItem(display_value)
                    self.table.setItem(row, col, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")

    def edit_product(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a product to edit.")
            return

        product_id = int(self.table.item(current_row, 0).text())

        # Get current product data
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM product_master WHERE id = ?", (product_id,))
        product = c.fetchone()
        conn.close()

        if product:
            dialog = EditProductDialog(product, self)
            if dialog.exec() == QDialog.Accepted:
                self.load_products()  # Refresh table

    def delete_product(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a product to delete.")
            return

        product_id = int(self.table.item(current_row, 0).text())
        product_name = self.table.item(current_row, 3).text()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("DELETE FROM product_master WHERE id = ?", (product_id,))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Success", "Product deleted successfully!")
                self.load_products()  # Refresh table

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete product: {e}")


class EditProductDialog(QDialog):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setWindowTitle("Edit Product")
        self.setFixedSize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Extract current values
        (self.product_id, barcode, sku, category, subcategory, image_path,
         name, description, tax, price, unit) = self.product_data

        # Barcode
        self.barcode = QLineEdit(barcode or "")
        form_layout.addRow("Barcode:", self.barcode)

        # SKU (read-only for editing)
        self.sku = QLineEdit(sku or "")
        self.sku.setReadOnly(True)
        form_layout.addRow("SKU:", self.sku)

        # Product Name
        self.name = QLineEdit(name or "")
        form_layout.addRow("Product Name:", self.name)

        # Category
        self.category = QComboBox()
        self.category.setEditable(True)
        self.category.addItems(["Electronics", "Food", "Clothing", "Books", "Other"])
        if category:
            self.category.setCurrentText(category)
        form_layout.addRow("Category:", self.category)

        # Subcategory
        self.subcategory = QLineEdit(subcategory or "")
        form_layout.addRow("Subcategory:", self.subcategory)

        # Description
        self.description = QTextEdit()
        self.description.setMaximumHeight(80)
        self.description.setPlainText(description or "")
        form_layout.addRow("Description:", self.description)

        # Price
        self.price = QDoubleSpinBox()
        self.price.setMaximum(999999.99)
        self.price.setDecimals(2)
        self.price.setValue(price or 0)
        form_layout.addRow("Price (₹):", self.price)

        # Tax
        self.tax = QDoubleSpinBox()
        self.tax.setMaximum(100)
        self.tax.setDecimals(2)
        self.tax.setSuffix("%")
        self.tax.setValue(tax or 0)
        form_layout.addRow("Tax Rate:", self.tax)

        # Unit
        self.unit = QComboBox()
        self.unit.addItems(["pcs", "kg", "litre", "box", "meter", "dozen"])
        if unit:
            unit_index = self.unit.findText(unit)
            if unit_index >= 0:
                self.unit.setCurrentIndex(unit_index)
        form_layout.addRow("Default Unit:", self.unit)

        layout.addLayout(form_layout)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_changes)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def save_changes(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Product name is required!")
            return

        try:
            conn = get_db_connection()
            c = conn.cursor()

            c.execute("""
                UPDATE product_master 
                SET barcode=?, category=?, subcategory=?, name=?, description=?, 
                    tax=?, price=?, unit=?
                WHERE id=?
            """, (
                self.barcode.text().strip(),
                self.category.currentText(),
                self.subcategory.text().strip(),
                self.name.text().strip(),
                self.description.toPlainText().strip(),
                self.tax.value(),
                self.price.value(),
                self.unit.currentText(),
                self.product_id
            ))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Product updated successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update product: {str(e)}")
