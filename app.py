
from flask import Flask, render_template, request, redirect, session
import sqlite3

from registration import registration_bp
from login import login_bp
from management import management_bp

app = Flask(__name__)
app.secret_key = "student-management-secret-key"

# Register feature blueprints
app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(management_bp)


def connect_db():
    return sqlite3.connect("students.db")


# Create the table if it does not exist
with connect_db() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT,
            password TEXT
        )
    """)


# Week 7: Display all students
@app.route("/")
def home():
    with connect_db() as con:
        students = con.execute(
            "SELECT * FROM students"
        ).fetchall()

    return render_template("index.html", students=students)


# Week 7: Add student
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        with connect_db() as con:
            con.execute(
                "INSERT INTO students (name, department) VALUES (?, ?)",
                (name, department)
            )

    return redirect("/")


# Week 7: Update student
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        with connect_db() as con:
            con.execute(
                "UPDATE students SET name=?, department=? WHERE id=?",
                (name, department, id)
            )

    return redirect("/")


# Week 7: Delete student
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
