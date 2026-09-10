import sqlite3

connection = sqlite3.connect("database/journova.db")
cursor = connection.cursor()

cursor.execute(
    "INSERT INTO journal_entries (entry_text, mood) VALUES (?, ?)",
    ("Today I am feeling calm and positive.", "Calm")
)

connection.commit()
print("Test journal entry saved successfully.")

connection.close()