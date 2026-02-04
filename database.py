import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_new_product(db_path, product_url):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM products WHERE url = ?", (product_url,))
    exists = cur.fetchone()

    if exists:
        conn.close()
        return False

    cur.execute("INSERT INTO products (url) VALUES (?)", (product_url,))
    conn.commit()
    conn.close()
    return True
