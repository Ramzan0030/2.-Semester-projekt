import sqlite3

connection = sqlite3.connect("booking_system.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

connection.commit()

connection.close()

print("Users tabel oprettet")