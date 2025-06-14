
---


# Inventory Management System

A comprehensive desktop application for managing inventory, sales, and product data built with Python and PySide6 (Qt for Python).

## Features

### 🔐 User Authentication
- Role-based access control (Admin / Operator)
- Secure login system
- Pre-configured sample accounts

### 📦 Product Management
- **Product Master**: Complete product catalog management
- **Add New Products**: Easy product registration with barcode support
- **Edit/Delete Products**: Full CRUD operations
- **Image Support**: Upload, display, and store product images
- **Categories & Subcategories**: Organized classification

### 📥 Goods Receiving
- Record incoming inventory
- Supplier tracking
- Automatic total & tax calculation
- Date logging

### 💰 Sales Management
- Point-of-sale interface
- Real-time subtotal, tax, and total computation
- Product image display
- PDF invoice generation with product and tax details

### 📊 Data Management
- SQLite backend with foreign key relationships
- Data validation and error handling
- Clean schema design

---

## System Requirements

- Python 3.7 or higher
- Works on Windows, macOS, or Linux

## Dependencies

```bash
pip install PySide6 reportlab
````

---

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd inventory-management-system
```

2. **Install dependencies**

```bash
pip install PySide6 reportlab
```

3. **Run the application**

```bash
python main.py
```

---

## Project Structure

```
inventory-management-system/
├── main.py              # Entry point, initializes DB and login
├── database.py          # SQLite DB setup and connection
├── login.py             # Login interface
├── menu.py              # Role-based menu interface
├── product_master.py    # Product catalog management
├── product_add.py       # Product registration form
├── goods_receiving.py   # Goods receiving entry
├── sales_form.py        # Sales and invoice module
├── main.spec            # PyInstaller configuration
└── inventory.db         # SQLite database (auto-created)
```

---

## Usage

### 🧪 First Launch

1. Run `python main.py`
2. The database is auto-initialized with sample users and products

### 🔑 Login Credentials

**Admin Account:**

* Username: `admin`
* Password: `admin123`

**Operator Account:**

* Username: `operator1`
* Password: `pass123`

> Admins can access all modules. Operators can only access Sales and Goods Receiving.

---

## Database Schema

### Tables

#### `operators`

* `id` (Primary Key)
* `username` (Unique)
* `password`
* `role` (admin/operator)

#### `product_master`

* `id` (Primary Key)
* `barcode`
* `sku` (Unique)
* `category`
* `subcategory`
* `image_path`
* `name`
* `description`
* `tax`
* `price`
* `unit`

#### `goods_receiving`

* `id` (Primary Key)
* `product_id` (Foreign Key)
* `supplier`
* `quantity`
* `unit`
* `rate`
* `total`
* `tax`
* `date`

#### `sales`

* `id` (Primary Key)
* `product_id` (Foreign Key)
* `customer`
* `quantity`
* `unit`
* `rate`
* `total`
* `tax`
* `sale_date`

---

## Building Executable (Windows)

Includes a `main.spec` file for PyInstaller.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build Command

```bash
pyinstaller main.spec
```

### Executable Output

* Single `.exe` file
* Embedded database
* Custom icon support
* No console window
* UPX compression enabled

---

## Configuration

### Database Location

The `inventory.db` file is created in the same directory as `main.py`. Make sure your app always runs from that location.

### Image Storage

Product images are stored as local file paths in the database. Ensure image files remain accessible for display.

### Default Data

* Admin and Operator user accounts
* Two sample products across categories (e.g., Electronics, Food)

---

## User Interface Design

* Minimal, intuitive layout
* Role-based menus
* Reusable PySide6 forms
* Error and input validation
* Consistent visual style

---

## Error Handling

Handled exceptions for:

* Database connectivity
* Invalid user input
* File operations (image, PDF)
* PDF generation errors

---

## Security Features

* Password-based login
* Role-based UI control
* Parameterized SQL queries (prevents injection)
* Input validation and sanitization

---

## Future Enhancements

* Reporting and analytics dashboards
* Database backup/restore
* Multi-location inventory tracking
* Barcode scanner integration
* Cloud sync or LAN networking
* CSV/Excel export
* Smart filtering and search

---

## Support

If you encounter issues:

1. Check in-app error dialogs
2. Verify dependencies are installed
3. Make sure `inventory.db` is writable
4. Use console output for detailed traceback

---


