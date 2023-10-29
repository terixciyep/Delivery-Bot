import sqlite3 as sq

with sq.connect("db/waves.db") as sq_con:
    cur = sq_con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS wave (
        date DATE,
        start_wave INTEGER,
        end_wave INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store VARCHAR(50)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS delivery_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        delivery_type TEXT
    )""")
    cur.execute('''CREATE TABLE IF NOT EXISTS community (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS condition_delivery_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        delivery_type INTEGER,
        condition_name VARCHAR(50),
        delivery_condition TEXT,
        FOREIGN KEY (delivery_type) REFERENCES delivery_type(id)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS store_with_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        delivery_type INTEGER,
        FOREIGN KEY (delivery_type) REFERENCES delivery_type(id)
        FOREIGN KEY (store_id) REFERENCES store(id)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        name VARCHAR(100),
        phone_number TEXT,
        telegram_link_on_user TEXT,
        community_id INTEGER,
        block VARCHAR(100),
        type_of_delivery INTEGER,
        store_id INTEGER,
        time DATETIME,
        block TEXT,
        FOREIGN KEY (store_id) REFERENCES store(id),
        FOREIGN KEY (community_id) REFERENCES community(id),
        FOREIGN KEY (type_of_delivery) REFERENCES delivery_type(id)
    )''')
    cur.execute("""CREATE TABLE IF NOT EXISTS users_condition_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        condition_id INTEGER,
        answer TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (condition_id) REFERENCES condition_delivery_type(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS community_place (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        community_id INTEGER,
        name TEXT,
        FOREIGN KEY (community_id) REFERENCES community(id)
    )""")