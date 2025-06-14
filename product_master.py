# product_master.py (with filterable product table)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView)
from PySide6.QtCore import Qt
from database import get_db_connection

class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master List")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search product name or SKU")
        self.search_box.textChanged.connect(self.load_data)
        filter_layout.addWidget(QLabel("Search: "))
        filter_layout.addWidget(self.search_box)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["SKU", "Product Name", "Category", "Price", "Unit", "Tax %"])
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        keyword = self.search_box.text().lower()
        conn = get_db_connection()
        c = conn.cursor()
        if keyword:
            c.execute("""
                SELECT sku, name, category, price, unit, tax FROM product_master
                WHERE LOWER(name) LIKE ? OR LOWER(sku) LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
        else:
            c.execute("SELECT sku, name, category, price, unit, tax FROM product_master")
        results = c.fetchall()
        conn.close()

        self.table.setRowCount(len(results))
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, data in enumerate(results):
            for col, item in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))
