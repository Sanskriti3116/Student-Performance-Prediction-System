import sqlite3

DB_NAME = "database/database.db"

def register_student(name, email, password, department, semester):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, email, password, department, semester)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email, password, department, semester))

    conn.commit()
    conn.close()

def login_student(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user