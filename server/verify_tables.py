# server/verify_tables.py
import sqlite3

conn = sqlite3.connect('app/dividends.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("Tables in the database:")
    for table in tables:
        print(table[0])
else:
    print("No tables found.")

conn.close()
