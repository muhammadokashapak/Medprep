import sqlite3
import json
import os

def extract_mcqs(db_path, output_js_path):
    all_mcqs = []
    
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context FROM mcqs")
        rows = cursor.fetchall()
        
        for row in rows:
            mcq = {
                "id": row[0],
                "question": row[1],
                "options": [row[2], row[3], row[4], row[5], row[6]],
                "correct_answer": row[7],
                "explanation": row[8],
                "category": row[9]
            }
            all_mcqs.append(mcq)
    except Exception as e:
        print(f"Error reading from {db_path}: {e}")
    finally:
        conn.close()

    print(f"Total MCQs extracted: {len(all_mcqs)}")
    
    # Save to questions.js
    with open(output_js_path, 'w', encoding='utf-8') as f:
        f.write("const mcqData = ")
        json.dump(all_mcqs, f, indent=4)
        f.write(";\n")
    print(f"Successfully wrote data to {output_js_path}")

if __name__ == "__main__":
    db_path = r"E:\USAMA\MBBS Books\MCQ_Generator\quiz_bank.db"
    output_path = r"E:\USAMA\MBBS Books\MCQs List\Quiz_App\questions.js"
    extract_mcqs(db_path, output_path)
