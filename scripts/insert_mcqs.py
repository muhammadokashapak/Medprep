import sqlite3
import json
import sys
import os

DB_PATH = r"E:\USAMA\MBBS Books\MCQ_Generator\fcps_mcqs.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
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
    conn.commit()
    return conn

def insert_mcqs_from_json(json_file_path):
    conn = setup_database()
    cursor = conn.cursor()
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        mcqs = json.load(f)
    
    count = 0
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
                mcq.get('source_context', 'First Aid USMLE Step 1')
            ))
            count += 1
        except Exception as e:
            print(f"Error inserting MCQ: {e}")
    
    conn.commit()
    
    # Print total count
    cursor.execute('SELECT COUNT(*) FROM mcqs')
    total = cursor.fetchone()[0]
    print(f"Inserted {count} MCQs. Total in database: {total}")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python insert_mcqs.py <json_file_path>")
        sys.exit(1)
    insert_mcqs_from_json(sys.argv[1])
