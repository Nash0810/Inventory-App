import sqlite3

def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Operators
    c.execute('''
        CREATE TABLE IF NOT EXISTS operators (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Product Master
    c.execute('''
        CREATE TABLE IF NOT EXISTS product_master (
            id INTEGER PRIMARY KEY,
            barcode TEXT,
            sku TEXT,
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
            FOREIGN KEY (product_id) REFERENCES product_master(id)
        )
    ''')

    # Insert sample operators
    c.execute("INSERT OR IGNORE INTO operators (username, password) VALUES ('operator1', 'pass123')")
    c.execute("INSERT OR IGNORE INTO operators (username, password) VALUES ('operator2', 'pass123')")

    conn.commit()
    conn.close()
