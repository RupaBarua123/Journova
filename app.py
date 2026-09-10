from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("database/journova.db")
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)