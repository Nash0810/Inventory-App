# 📋 Inventory Management System

A desktop-based inventory management application built with **Python** and **PySide6 (Qt for Python)**. It provides features like operator/admin login, goods receiving, sales processing, and a searchable product master list. The application also supports PDF invoice generation.

---

## ✨ Features

* **Login System**

  * Secure login with roles: `admin` and `operator`
* **Product Master**

  * Admin-only access
  * Searchable product list by SKU or name
* **Goods Receiving**

  * Capture supplier, quantity, rate, tax, and date
* **Sales Form**

  * Customer entry
  * Real-time total + tax calculation
  * PDF invoice generation
* **PDF Invoice**

  * Timestamped and saved with customer/product info
* **Database**

  * Local SQLite (`inventory.db`)
  * Auto-initialized on first run

---

## ⚙ Requirements

```bash
pip install PySide6 reportlab
```

* Python 3.7+

---

## 📂 File Structure

```
inventory_app/
│
├── main.py                # Application entry point
├── images/                # Contain the image of product
├── database.py            # DB setup & connection
├── login.py               # Login UI
├── menu.py                # Role-based navigation menu
├── product_master.py      # Product search/view table
├── goods_receiving.py     # Goods receiving form
├── sales_form.py          # Sales form + PDF invoice
└── inventory.db           # Auto-generated SQLite DB
```

---

## 🚀 Getting Started

Run the application with:

```bash
python main.py
```

The app will auto-create the database and sample user accounts.

### 📆 Default Credentials

| Username  | Password  | Role     |
| --------- | --------- | -------- |
| adminuser | adminpass | admin    |
| operator1 | pass123   | operator |
| operator2 | pass123   | operator |

---

## 🗃 Notes

* `Product ID` must exist for goods receiving and sales.
* Only `admin` can access the **Product Master** form.
* Invoices are saved as PDFs via `reportlab`.
* GUI uses standard PySide6 widgets with `QVBoxLayout` and `QTableWidget` for tables.

---

## 🌟 Optional Enhancements

* Password hashing (e.g. bcrypt)
* Stock tracking (inventory balance)
* Edit/delete options for existing records
* Report exports (CSV/PDF)
* Better invoice design

---

## 📄 License

This project is for educational and internal-use purposes. You may modify and use it freely.

---
