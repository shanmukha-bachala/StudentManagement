
from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
import sqlite3
from database import get_db

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        with get_db() as con:
            student = con.execute(
                "SELECT * FROM students WHERE email = ?",
                (email,)
            ).fetchone()

        if student and check_password_hash(student["password"], password):
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect("/")

        return "Invalid email or password", 401

    return render_template("login.html")
