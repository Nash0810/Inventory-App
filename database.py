import sqlite3
import os


def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Always refers to Inventory_App/
    db_path = os.path.join(base_dir, "inventory.db")
    conn = sqlite3.connect(db_path)
    return conn


def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Operators table
    c.execute('''
        CREATE TABLE IF NOT EXISTS operators (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'operator'
        )
    ''')

    # Product Master
    c.execute('''
        CREATE TABLE IF NOT EXISTS product_master (
            id INTEGER PRIMARY KEY,
            barcode TEXT,
            sku TEXT UNIQUE,
            category TEXT,
            subcategory TEXT,
            image_path TEXT,
            name TEXT,
            description TEXT,
            tax REAL,
            price REAL,
            unit TEXT
        )
    ''')

    # Goods Receiving
    c.execute('''
        CREATE TABLE IF NOT EXISTS goods_receiving (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            supplier TEXT,
            quantity REAL,
            unit TEXT,
            rate REAL,
            total REAL,
            tax REAL,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES product_master(id)
        )
    ''')

    # Sales
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer TEXT,
            quantity REAL,
            unit TEXT,
            rate REAL,
            total REAL,
            tax REAL,
            sale_date TEXT,
            FOREIGN KEY (product_id) REFERENCES product_master(id)
        )
    ''')

    # Insert default admin and operators
    c.execute("INSERT OR IGNORE INTO operators (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    c.execute("INSERT OR IGNORE INTO operators (username, password, role) VALUES ('operator1', 'pass123', 'operator')")
    c.execute("INSERT OR IGNORE INTO operators (username, password, role) VALUES ('operator2', 'pass456', 'operator')")

    # Insert sample products
    c.execute("""INSERT OR IGNORE INTO product_master 
                (barcode, sku, category, subcategory, name, description, tax, price, unit) 
                VALUES ('1234567890', 'SKU001', 'Electronics', 'Mobile', 'Sample Phone', 'Basic smartphone', 18.0, 15000.0, 'pcs')""")
    c.execute("""INSERT OR IGNORE INTO product_master 
                (barcode, sku, category, subcategory, name, description, tax, price, unit) 
                VALUES ('0987654321', 'SKU002', 'Food', 'Beverages', 'Sample Juice', 'Orange juice 1L', 5.0, 120.0, 'litre')""")

    conn.commit()
    conn.close()
