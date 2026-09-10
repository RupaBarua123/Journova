import sqlite3

connection = sqlite3.connect("database/journova.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM journal_entries")
entries = cursor.fetchall()

for entry in entries:
    print(entry)

connection.close()