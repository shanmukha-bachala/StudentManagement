
from flask import Blueprint, render_template, request, redirect
from database import get_db

management_bp = Blueprint("management", __name__)


@management_bp.route("/students")
def view_students():
    with get_db() as con:
        students = con.execute(
            "SELECT id, name, email, department FROM students"
        ).fetchall()

    return render_template("students.html", students=students)


@management_bp.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    with get_db() as con:
        student = con.execute(
            "SELECT id, name, email, department FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        if not student:
            return "Student not found", 404

        if request.method == "POST":
            name = request.form["name"].strip()
            email = request.form["email"].strip()
            department = request.form["department"].strip()

            con.execute(
                """UPDATE students
                   SET name = ?, email = ?, department = ?
                   WHERE id = ?""",
                (name, email, department, student_id)
            )
            return redirect("/students")

    return render_template("update.html", student=student)


@management_bp.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as con:
        con.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    return redirect("/students")
