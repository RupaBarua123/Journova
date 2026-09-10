from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("database/journova.db")
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password_hash)
            )
            connection.commit()
            message = "Account created successfully."

        except sqlite3.IntegrityError:
            message = "An account with this email already exists."

        connection.close()

    return render_template("register.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)