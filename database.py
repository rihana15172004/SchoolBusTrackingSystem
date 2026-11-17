import sqlite3

conn = sqlite3.connect('schoolbus.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    stop_name TEXT,
    parent_phone TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")