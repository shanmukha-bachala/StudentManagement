
import sqlite3

con = sqlite3.connect("students.db")

try:
    columns = [
        row[1] for row in con.execute(
            "PRAGMA table_info(students)"
        ).fetchall()
    ]

    if "email" not in columns:
        con.execute("ALTER TABLE students ADD COLUMN email TEXT")

    if "password" not in columns:
        con.execute("ALTER TABLE students ADD COLUMN password TEXT")

    con.commit()
    print("Database updated successfully!")
    print("Current columns:",
          [row[1] for row in con.execute(
              "PRAGMA table_info(students)"
          ).fetchall()])

finally:
    con.close()
