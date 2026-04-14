"""
SQLite database for tracking quiz attempt history.
"""
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "quiz_history.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            section TEXT NOT NULL,
            mode TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            attempted INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            wrong INTEGER NOT NULL,
            skipped INTEGER NOT NULL,
            earned_marks INTEGER NOT NULL,
            total_marks INTEGER NOT NULL,
            percentage REAL NOT NULL,
            time_seconds INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempt_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER,
            question_text TEXT NOT NULL,
            section TEXT,
            marks INTEGER NOT NULL,
            user_answer TEXT,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            FOREIGN KEY (attempt_id) REFERENCES attempts(id)
        )
    """)
    conn.commit()
    conn.close()


def save_attempt(section, mode, questions, answers, time_seconds):
    """Save a completed quiz attempt and return the attempt_id."""
    total_questions = len(questions)
    attempted = len(answers)
    correct = 0
    wrong = 0
    earned_marks = 0
    total_marks = 0

    details = []
    for i, q in enumerate(questions):
        q_marks = q.get('marks', 1)
        total_marks += q_marks
        user_answer = answers.get(i)
        correct_answer = q['answer']
        is_correct = user_answer == correct_answer

        if user_answer is None:
            pass  # skipped
        elif is_correct:
            correct += 1
            earned_marks += q_marks
        else:
            wrong += 1

        details.append({
            'question_id': q.get('id'),
            'question_text': q['question'],
            'section': q.get('section', 'EVS'),
            'marks': q_marks,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': 1 if is_correct else 0,
        })

    skipped = total_questions - attempted
    percentage = (earned_marks / total_marks * 100) if total_marks > 0 else 0

    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO attempts (timestamp, section, mode, total_questions, attempted,
                              correct, wrong, skipped, earned_marks, total_marks,
                              percentage, time_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        section,
        mode,
        total_questions,
        attempted,
        correct,
        wrong,
        skipped,
        earned_marks,
        total_marks,
        round(percentage, 1),
        time_seconds,
    ))
    attempt_id = cursor.lastrowid

    for d in details:
        conn.execute("""
            INSERT INTO attempt_details (attempt_id, question_id, question_text,
                                         section, marks, user_answer,
                                         correct_answer, is_correct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt_id,
            d['question_id'],
            d['question_text'],
            d['section'],
            d['marks'],
            d['user_answer'],
            d['correct_answer'],
            d['is_correct'],
        ))

    conn.commit()
    conn.close()
    return attempt_id


def get_all_attempts():
    """Return all attempts as a list of dicts."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM attempts ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_attempt_details(attempt_id):
    """Return details for a specific attempt."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM attempt_details WHERE attempt_id = ? ORDER BY id",
        (attempt_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_stats():
    """Return aggregate stats for the dashboard."""
    conn = get_connection()

    total_attempts = conn.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]

    if total_attempts == 0:
        conn.close()
        return {
            'total_attempts': 0,
            'total_questions_answered': 0,
            'overall_correct': 0,
            'overall_wrong': 0,
            'overall_skipped': 0,
            'avg_percentage': 0,
            'best_percentage': 0,
            'total_time_minutes': 0,
            'avg_time_seconds': 0,
            'recent_attempts': [],
            'section_stats': [],
            'score_trend': [],
        }

    agg = conn.execute("""
        SELECT
            SUM(attempted) as total_answered,
            SUM(correct) as total_correct,
            SUM(wrong) as total_wrong,
            SUM(skipped) as total_skipped,
            AVG(percentage) as avg_pct,
            MAX(percentage) as best_pct,
            SUM(time_seconds) as total_time,
            AVG(time_seconds) as avg_time
        FROM attempts
    """).fetchone()

    recent = conn.execute(
        "SELECT * FROM attempts ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()

    section_stats = conn.execute("""
        SELECT section,
               COUNT(*) as count,
               AVG(percentage) as avg_pct,
               MAX(percentage) as best_pct
        FROM attempts
        GROUP BY section
    """).fetchall()

    score_trend = conn.execute("""
        SELECT id, timestamp, percentage, section, mode
        FROM attempts ORDER BY timestamp ASC
    """).fetchall()

    conn.close()

    return {
        'total_attempts': total_attempts,
        'total_questions_answered': agg['total_answered'] or 0,
        'overall_correct': agg['total_correct'] or 0,
        'overall_wrong': agg['total_wrong'] or 0,
        'overall_skipped': agg['total_skipped'] or 0,
        'avg_percentage': round(agg['avg_pct'] or 0, 1),
        'best_percentage': round(agg['best_pct'] or 0, 1),
        'total_time_minutes': round((agg['total_time'] or 0) / 60, 1),
        'avg_time_seconds': int(agg['avg_time'] or 0),
        'recent_attempts': [dict(r) for r in recent],
        'section_stats': [dict(r) for r in section_stats],
        'score_trend': [dict(r) for r in score_trend],
    }
