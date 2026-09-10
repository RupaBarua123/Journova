import sqlite3

connection = sqlite3.connect("database/journova.db")
cursor = connection.cursor()

tables = ["users", "journal_entries", "mood_entries", "sentiment_results"]

for table in tables:
    print("\n" + table)

    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()

    for column in columns:
        print(column[1])

connection.close()