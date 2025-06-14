from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, role="operator", username=""):
        super().__init__()
        self.role = role
        self.username = username
        self.setWindowTitle(f"Inventory Management - {role.title()}")
        self.setFixedSize(400, 350)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Inventory Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        user_info = QLabel(f"Welcome, {self.username} ({self.role})")
        user_info.setStyleSheet("font-size: 12px; color: blue;")
        user_info.setAlignment(Qt.AlignRight)

        layout.addWidget(title)
        layout.addWidget(user_info)

        # Menu buttons
        if self.role in ["admin", "operator"]:
            self.goods_btn = QPushButton("📦 Goods Receiving")
            self.goods_btn.clicked.connect(self.open_goods_form)
            self.goods_btn.setStyleSheet("QPushButton { padding: 12px; font-size: 14px; }")
            layout.addWidget(self.goods_btn)

            self.sales_btn = QPushButton("💰 Sales Form")
            self.sales_btn.clicked.connect(self.open_sales_form)
            self.sales_btn.setStyleSheet("QPushButton { padding: 12px; font-size: 14px; }")
            layout.addWidget(self.sales_btn)

        if self.role == "admin":
            self.master_btn = QPushButton("📋 Product Master")
            self.master_btn.clicked.connect(self.open_master_form)
            self.master_btn.setStyleSheet("QPushButton { padding: 12px; font-size: 14px; }")
            layout.addWidget(self.master_btn)

            self.add_product_btn = QPushButton("➕ Add New Product")
            self.add_product_btn.clicked.connect(self.open_add_product_form)
            self.add_product_btn.setStyleSheet("QPushButton { padding: 12px; font-size: 14px; }")
            layout.addWidget(self.add_product_btn)

        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet(
            "QPushButton { padding: 8px; font-size: 12px; background-color: #ff6b6b; color: white; }")
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def open_goods_form(self):
        from goods_receiving import GoodsReceivingForm
        self.goods_form = GoodsReceivingForm()
        self.goods_form.show()

    def open_sales_form(self):
        from sales_form import SalesForm
        self.sales_form = SalesForm()
        self.sales_form.show()

    def open_master_form(self):
        from product_master import ProductMasterForm
        self.master_form = ProductMasterForm()
        self.master_form.show()

    def open_add_product_form(self):
        from product_add import AddProductForm
        self.add_form = AddProductForm()
        self.add_form.show()

    def logout(self):
        self.close()
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()