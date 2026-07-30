import os
import sqlite3
import json

def sync_questions_to_sqlite():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace_root, "src", "data", "questions.json")
    db_path = os.path.join(workspace_root, "database", "fcps_qbank.db")
    
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        mcqs = json.load(f)

    print(f"Loaded {len(mcqs)} MCQs from questions.json.")
    print(f"Connecting to SQLite database: {db_path}...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY,
            category TEXT,
            question TEXT UNIQUE,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            option_e TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            difficulty TEXT,
            book_source TEXT
        )
    ''')

    # Clear old table and insert updated 18,000 anti-trick dataset
    cursor.execute("DELETE FROM mcqs;")

    inserted = 0
    for q in mcqs:
        try:
            cursor.execute('''
                INSERT INTO mcqs (id, category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                q.get("id"),
                q.get("category", "General"),
                q.get("question"),
                q.get("option_a"),
                q.get("option_b"),
                q.get("option_c"),
                q.get("option_d"),
                q.get("option_e"),
                q.get("correct_answer"),
                q.get("explanation"),
                q.get("difficulty", "Hard"),
                q.get("book_source", "Medical Textbook")
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            pass # Skip duplicate questions if any

    conn.commit()

    # Get total count
    count = cursor.execute("SELECT COUNT(*) FROM mcqs;").fetchone()[0]
    conn.close()

    print(f"Successfully synced {inserted} MCQs to SQLite database ({db_path}).")
    print(f"Total rows in SQLite database: {count}")

if __name__ == "__main__":
    sync_questions_to_sqlite()
