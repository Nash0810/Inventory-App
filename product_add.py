from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTextEdit, QDoubleSpinBox, QComboBox,
                               QFileDialog, QMessageBox, QFormLayout)
from PySide6.QtCore import Qt
from database import get_db_connection


class AddProductForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Product")
        self.setFixedSize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Barcode
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText("Scan or enter barcode")
        form_layout.addRow("Barcode:", self.barcode)

        # SKU
        self.sku = QLineEdit()
        self.sku.setPlaceholderText("Enter unique SKU")
        form_layout.addRow("SKU:", self.sku)

        # Product Name
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter product name")
        form_layout.addRow("Product Name:", self.name)

        # Category
        self.category = QComboBox()
        self.category.setEditable(True)
        self.category.addItems(["Electronics", "Food", "Clothing", "Books", "Other"])
        form_layout.addRow("Category:", self.category)

        # Subcategory
        self.subcategory = QLineEdit()
        self.subcategory.setPlaceholderText("Enter subcategory")
        form_layout.addRow("Subcategory:", self.subcategory)

        # Description
        self.description = QTextEdit()
        self.description.setMaximumHeight(80)
        self.description.setPlaceholderText("Enter product description")
        form_layout.addRow("Description:", self.description)

        # Price
        self.price = QDoubleSpinBox()
        self.price.setMaximum(999999.99)
        self.price.setDecimals(2)
        form_layout.addRow("Price (₹):", self.price)

        # Tax
        self.tax = QDoubleSpinBox()
        self.tax.setMaximum(100)
        self.tax.setDecimals(2)
        self.tax.setSuffix("%")
        form_layout.addRow("Tax Rate:", self.tax)

        # Unit
        self.unit = QComboBox()
        self.unit.addItems(["pcs", "kg", "litre", "box", "meter", "dozen"])
        form_layout.addRow("Default Unit:", self.unit)

        # Image
        image_layout = QHBoxLayout()
        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("No image selected")
        self.image_path.setReadOnly(True)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_image)
        image_layout.addWidget(self.image_path)
        image_layout.addWidget(browse_btn)
        form_layout.addRow("Product Image:", image_layout)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Product")
        save_btn.clicked.connect(self.save_product)
        save_btn.setStyleSheet("QPushButton { padding: 10px; background-color: #4CAF50; color: white; }")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("QPushButton { padding: 10px; background-color: #f44336; color: white; }")

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Product Image", "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.image_path.setText(file_path)

    def save_product(self):
        # Validation
        if not all([self.sku.text().strip(), self.name.text().strip()]):
            QMessageBox.warning(self, "Validation Error", "SKU and Product Name are required!")
            return

        try:
            conn = get_db_connection()
            c = conn.cursor()

            # Check if SKU already exists
            c.execute("SELECT id FROM product_master WHERE sku = ?", (self.sku.text().strip(),))
            if c.fetchone():
                QMessageBox.warning(self, "Duplicate SKU", "A product with this SKU already exists!")
                conn.close()
                return

            # Insert new product
            c.execute("""
                INSERT INTO product_master 
                (barcode, sku, category, subcategory, image_path, name, description, tax, price, unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.barcode.text().strip(),
                self.sku.text().strip(),
                self.category.currentText(),
                self.subcategory.text().strip(),
                self.image_path.text(),
                self.name.text().strip(),
                self.description.toPlainText().strip(),
                self.tax.value(),
                self.price.value(),
                self.unit.currentText()
            ))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Product added successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save product: {str(e)}")

    def clear_form(self):
        self.barcode.clear()
        self.sku.clear()
        self.name.clear()
        self.subcategory.clear()
        self.description.clear()
        self.price.setValue(0)
        self.tax.setValue(0)
        self.image_path.clear()
        self.category.setCurrentIndex(0)
        self.unit.setCurrentIndex(0)