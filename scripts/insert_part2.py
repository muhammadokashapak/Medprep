import sqlite3
import sys
import json

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            option_e TEXT,
            correct_answer TEXT,
            explanation TEXT,
            source_context TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_mcqs(db_path, json_file):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    count = 0
    for item in data:
        try:
            c.execute('''
                INSERT INTO mcqs (question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('question', ''),
                item.get('option_a', ''),
                item.get('option_b', ''),
                item.get('option_c', ''),
                item.get('option_d', ''),
                item.get('option_e', ''),
                item.get('correct_answer', ''),
                item.get('explanation', ''),
                item.get('source_context', '')
            ))
            count += 1
        except sqlite3.IntegrityError:
            pass # Skip duplicates
            
    conn.commit()
    
    c.execute("SELECT COUNT(*) FROM mcqs")
    total = c.fetchone()[0]
    conn.close()
    
    print(f"Inserted {count} MCQs. Total in database {db_path}: {total}")

if __name__ == '__main__':
    db_file = r"E:\USAMA\MBBS Books\MCQ_Generator\part2mcqs.db"
    init_db(db_file)
    if len(sys.argv) > 1:
        insert_mcqs(db_file, sys.argv[1])
