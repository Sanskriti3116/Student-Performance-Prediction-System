import sqlite3

DB_NAME = "database/database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_students_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        department TEXT,
        semester TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_daily_updates_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        study_hours REAL,
        attendance TEXT,
        sleep_hours REAL,
        assignments_completed INTEGER,
        participation INTEGER,
        mood TEXT,
        quiz_score REAL,
        internal_marks REAL,
        subject TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()


def add_daily_update(
    student_id,
    date,
    study_hours,
    attendance,
    sleep_hours,
    assignments_completed,
    participation,
    mood,
    quiz_score,
    internal_marks,
    subject
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO daily_updates (
        student_id,
        date,
        study_hours,
        attendance,
        sleep_hours,
        assignments_completed,
        participation,
        mood,
        quiz_score,
        internal_marks,
        subject
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        date,
        study_hours,
        attendance,
        sleep_hours,
        assignments_completed,
        participation,
        mood,
        quiz_score,
        internal_marks,
        subject
    ))

    conn.commit()
    conn.close()


def daily_update_exists(student_id, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM daily_updates
    WHERE student_id = ? AND date = ?
    """, (student_id, date))

    result = cursor.fetchone()

    conn.close()

    return result is not None


def get_daily_updates(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        date,
        study_hours,
        attendance,
        sleep_hours,
        mood
    FROM daily_updates
    WHERE student_id = ?
    ORDER BY id DESC
    """, (student_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_dashboard_data(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            study_hours,
            attendance,
            sleep_hours,
            mood
        FROM daily_updates
        WHERE student_id = ?
        ORDER BY id ASC
    """, (student_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_analytics_data(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            study_hours,
            attendance,
            sleep_hours,
            mood
        FROM daily_updates
        WHERE student_id = ?
        ORDER BY id ASC
    """, (student_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_student(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student