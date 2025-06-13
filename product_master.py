from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog, QComboBox
from database import get_db_connection
import os

class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master Form")
        layout = QFormLayout()

        self.barcode = QLineEdit()
        self.sku = QLineEdit()
        self.category = QLineEdit()
        self.subcategory = QLineEdit()
        self.image_path = QLineEdit()
        self.name = QLineEdit()
        self.description = QLineEdit()
        self.tax = QLineEdit()
        self.price = QLineEdit()
        self.unit = QComboBox()
        self.unit.addItems(["kg", "pcs", "liters"])

        img_btn = QPushButton("Browse Image")
        img_btn.clicked.connect(self.browse_image)

        submit = QPushButton("Add Product")
        submit.clicked.connect(self.submit_form)

        layout.addRow("Barcode", self.barcode)
        layout.addRow("SKU", self.sku)
        layout.addRow("Category", self.category)
        layout.addRow("Subcategory", self.subcategory)
        layout.addRow("Image Path", self.image_path)
        layout.addRow(img_btn)
        layout.addRow("Name", self.name)
        layout.addRow("Description", self.description)
        layout.addRow("Tax", self.tax)
        layout.addRow("Price", self.price)
        layout.addRow("Unit", self.unit)
        layout.addRow(submit)
        self.setLayout(layout)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image")
        if file_path:
            self.image_path.setText(file_path)

    def submit_form(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO product_master
                     (barcode, sku, category, subcategory, image_path, name, description, tax, price, unit)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (self.barcode.text(), self.sku.text(), self.category.text(), self.subcategory.text(),
                   self.image_path.text(), self.name.text(), self.description.text(),
                   self.tax.text(), self.price.text(), self.unit.currentText()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Product Added")
