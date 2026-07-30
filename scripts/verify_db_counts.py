import os
import sqlite3

def check_counts():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(workspace_root, "database")

    db_files = [f for f in os.listdir(db_dir) if f.endswith(".db") and f != "fcps_qbank.db"]

    print("==========================================================")
    print("      EXACT MCQ COUNT IN EACH EXAM DATABASE (.db)         ")
    print("==========================================================")

    total_sum = 0
    for db_name in db_files:
        db_path = os.path.join(db_dir, db_name)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        count = c.execute("SELECT COUNT(*) FROM mcqs;").fetchone()[0]
        conn.close()
        total_sum += count
        print(f" -> {db_name}: {count:,} MCQs")

    print("==========================================================")
    print(f" TOTAL MCQS ACROSS ALL 6 EXAM DATABASES: {total_sum:,}")
    print("==========================================================")

if __name__ == "__main__":
    check_counts()
