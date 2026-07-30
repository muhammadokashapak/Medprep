import sqlite3
import json
import sys
import os

def insert_mcqs(json_file_path):
    db_path = r"E:\USAMA\MBBS Books\MCQ_Generator\quiz_bank.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL UNIQUE,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            option_e TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            source_context TEXT
        )
    ''')
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        mcqs = json.load(f)

    inserted_count = 0
    for mcq in mcqs:
        try:
            cursor.execute('''
                INSERT INTO mcqs (question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                mcq['question'],
                mcq['option_a'],
                mcq['option_b'],
                mcq['option_c'],
                mcq['option_d'],
                mcq['option_e'],
                mcq['correct_answer'],
                mcq['explanation'],
                mcq.get('source_context', 'General')
            ))
            inserted_count += 1
        except sqlite3.IntegrityError:
            pass # Skip duplicates

    conn.commit()
    conn.close()
    print(f"Inserted {inserted_count} MCQs into {db_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python insert_to_bank.py <path_to_json_file>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    insert_mcqs(json_path)
