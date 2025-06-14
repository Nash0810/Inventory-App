from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from goods_receiving import GoodsReceivingForm
from sales_form import SalesForm
from product_master import ProductMasterForm

class MenuWindow(QWidget):
    def __init__(self, role="operator"):
        super().__init__()
        self.setWindowTitle("Inventory App Menu")
        self.setFixedSize(300, 300)
        layout = QVBoxLayout()

        title = QLabel("Inventory Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        if role in ["admin", "operator"]:
            self.goods_btn = QPushButton("Goods Receiving")
            self.goods_btn.clicked.connect(self.open_goods_form)
            layout.addWidget(self.goods_btn)

            self.sales_btn = QPushButton("Sales Form")
            self.sales_btn.clicked.connect(self.open_sales_form)
            layout.addWidget(self.sales_btn)

        if role == "admin":
            self.master_btn = QPushButton("Product Master")
            self.master_btn.clicked.connect(self.open_master_form)
            layout.addWidget(self.master_btn)

        self.setLayout(layout)

    def open_goods_form(self):
        self.goods_form = GoodsReceivingForm()
        self.goods_form.show()

    def open_sales_form(self):
        self.sales_form = SalesForm()
        self.sales_form.show()

    def open_master_form(self):
        self.master_form = ProductMasterForm()
        self.master_form.show()
