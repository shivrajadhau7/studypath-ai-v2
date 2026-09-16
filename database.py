"""
database.py
-----------
Lightweight storage layer for StudyPath AI.

By default this uses SQLite (zero-setup, ships with Python) so the whole
project runs out of the box with no external services.

A MongoDB-backed implementation is sketched at the bottom (commented) —
swap DB_BACKEND to "mongo" and fill in your connection string if you'd
rather run it against MongoDB, as shown in the original architecture
diagram. Both back ends expose the exact same functions, so nothing else
in the codebase needs to change.
"""

import sqlite3
import json
import os
import time
from contextlib import contextmanager

DB_BACKEND = "sqlite"  # "sqlite" | "mongo"
DB_PATH = os.path.join(os.path.dirname(__file__), "studypath.db")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                score REAL NOT NULL,
                total INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                weak_flag INTEGER NOT NULL,
                timestamp REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT
            )
        """)


def ensure_student(student_id: str, name: str = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO students (student_id, name) VALUES (?, ?)",
            (student_id, name or student_id),
        )


def save_quiz_attempt(student_id, topic_id, score, total, correct, weak_flag):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO quiz_attempts
               (student_id, topic_id, score, total, correct, weak_flag, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (student_id, topic_id, score, total, correct, int(weak_flag), time.time()),
        )


def get_attempts(student_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM quiz_attempts WHERE student_id = ? ORDER BY timestamp ASC",
            (student_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_weak_topics(student_id):
    """A topic is 'weak' if the student's most recent attempt on it scored < 60%."""
    attempts = get_attempts(student_id)
    latest_by_topic = {}
    for a in attempts:
        latest_by_topic[a["topic_id"]] = a  # keeps overwriting -> last one wins (already time-ordered)
    return [t for t, a in latest_by_topic.items() if a["score"] < 60]


def reset_student_data(student_id: str):
    """Delete all quiz attempts for a student so they can start fresh."""
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM quiz_attempts WHERE student_id = ?",
            (student_id,),
        )


init_db()

# ---------------------------------------------------------------------------
# MongoDB alternative (matches the architecture diagram's "Database" box).
# Uncomment and set DB_BACKEND = "mongo" above to use this instead.
# ---------------------------------------------------------------------------
# from motor.motor_asyncio import AsyncIOMotorClient
# mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
# mongo_db = mongo_client["studypath_ai"]
#
# async def save_quiz_attempt_mongo(student_id, topic_id, score, total, correct, weak_flag):
#     await mongo_db.quiz_attempts.insert_one({
#         "student_id": student_id, "topic_id": topic_id, "score": score,
#         "total": total, "correct": correct, "weak_flag": weak_flag,
#         "timestamp": time.time(),
#     })
