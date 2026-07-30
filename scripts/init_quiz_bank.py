import sqlite3
import os

def create_unified_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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
    conn.commit()
    return conn, cursor

def migrate_data(source_db, dest_cursor):
    if not os.path.exists(source_db):
        return 0
    
    conn = sqlite3.connect(source_db)
    cursor = conn.cursor()
    cursor.execute("SELECT question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context FROM mcqs")
    rows = cursor.fetchall()
    
    inserted = 0
    for row in rows:
        try:
            dest_cursor.execute('''
                INSERT INTO mcqs (question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)
            inserted += 1
        except sqlite3.IntegrityError:
            pass # duplicate
    
    conn.close()
    return inserted

if __name__ == "__main__":
    db_path = r"E:\USAMA\MBBS Books\MCQ_Generator\quiz_bank.db"
    dest_conn, dest_cursor = create_unified_db(db_path)
    
    source1 = r"E:\USAMA\MBBS Books\MCQ_Generator\fcps_mcqs.db"
    source2 = r"E:\USAMA\MBBS Books\MCQ_Generator\part2mcqs.db"
    
    c1 = migrate_data(source1, dest_cursor)
    c2 = migrate_data(source2, dest_cursor)
    
    dest_conn.commit()
    dest_conn.close()
    
    print(f"Migrated {c1} from source 1 and {c2} from source 2 into quiz_bank.db. Total: {c1+c2}")
