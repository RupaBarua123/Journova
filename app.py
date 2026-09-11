from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "journova-development-key"


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


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id, email, password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["email"] = user[1]
            return redirect(url_for("dashboard"))
        else:
            message = "Email or password is incorrect."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", email=session["email"])


@app.route("/journal", methods=["GET", "POST"])
def journal():
    if "user_id" not in session:
        return redirect(url_for("login"))

    message = ""

    if request.method == "POST":
        entry_text = request.form["entry_text"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO journal_entries (user_id, entry_text) VALUES (?, ?)",
            (session["user_id"], entry_text)
        )

        connection.commit()
        connection.close()

        message = "Journal entry saved."

    return render_template("journal.html", message=message)


@app.route("/mood", methods=["GET", "POST"])
def mood():
    if "user_id" not in session:
        return redirect(url_for("login"))

    message = ""

    if request.method == "POST":
        selected_mood = request.form["mood"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO mood_entries (user_id, mood) VALUES (?, ?)",
            (session["user_id"], selected_mood)
        )

        connection.commit()
        connection.close()

        message = "Mood saved."

    return render_template("mood.html", message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)