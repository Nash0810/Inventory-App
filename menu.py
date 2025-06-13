from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from product_master import ProductMasterForm
from goods_receiving import GoodsReceivingForm
from sales_form import SalesForm

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setFixedSize(250, 200)

        layout = QVBoxLayout()

        btn_product_master = QPushButton("Product Master")
        btn_goods_receiving = QPushButton("Goods Receiving")
        btn_sales_form = QPushButton("Sales Form")

        btn_product_master.clicked.connect(self.open_product_master)
        btn_goods_receiving.clicked.connect(self.open_goods_receiving)
        btn_sales_form.clicked.connect(self.open_sales_form)

        layout.addWidget(btn_product_master)
        layout.addWidget(btn_goods_receiving)
        layout.addWidget(btn_sales_form)
        self.setLayout(layout)

    def open_product_master(self):
        self.product_form = ProductMasterForm()
        self.product_form.show()

    def open_goods_receiving(self):
        self.goods_form = GoodsReceivingForm()
        self.goods_form.show()

    def open_sales_form(self):
        self.sales_form = SalesForm()
        self.sales_form.show()
