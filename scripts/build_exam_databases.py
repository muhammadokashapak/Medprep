import os
import sqlite3
import json
import re

# Mapping of book names to target exam databases
EXAM_CATEGORIES = {
    "usmle_step1": {
        "title": "USMLE Step 1 QBank",
        "description": "High-yield Basic Medical Sciences for USMLE Step 1",
        "db_file": "usmle_step1.db",
        "json_file": "usmle_step1.json",
        "books": ["First Aid Step 1 2023", "First Aid Q&A Step 1", "Pathoma Fundamentals of Pathology"]
    },
    "usmle_step2_ck": {
        "title": "USMLE Step 2 CK QBank",
        "description": "Clinical Knowledge & Internal Medicine for USMLE Step 2 CK",
        "db_file": "usmle_step2_ck.db",
        "json_file": "usmle_step2_ck.json",
        "books": ["First Aid Step 2 CK 10th Ed"]
    },
    "fcps_nle_medical": {
        "title": "FCPS Part 1 & NLE Medical QBank",
        "description": "Comprehensive Review for FCPS Part 1, NLE, NEB, and PG Entrance",
        "db_file": "fcps_nle_medical.db",
        "json_file": "fcps_nle_medical.json",
        "books": ["ROAMS Medical Review", "Pathoma 2021 Edition"]
    },
    "surgery_mrcs": {
        "title": "Surgery & MRCS QBank",
        "description": "General Surgery & Surgical Specialties for MRCS and Final Proff",
        "db_file": "surgery_mrcs.db",
        "json_file": "surgery_mrcs.json",
        "books": ["Bailey & Love Surgery 26th Ed"]
    },
    "pharmacology_pg": {
        "title": "Pharmacology & Therapeutics QBank",
        "description": "High-Yield Pharmacology for NEET PG, FMGE, PLAB, and USMLE",
        "db_file": "pharmacology_pg.db",
        "json_file": "pharmacology_pg.json",
        "books": ["Self-Assessment Pharmacology 4th Ed", "Pharmacology An Illustrated Review", "Review of Pharmacology 9th Ed (Garg & Gupta)"]
    },
    "basic_sciences_anatomy_physio": {
        "title": "Anatomy & Physiology QBank",
        "description": "Core Basic Sciences (Guyton Physiology & Snell Anatomy) for MBBS 1st/2nd Proff",
        "db_file": "basic_sciences_anatomy_physio.db",
        "json_file": "basic_sciences_anatomy_physio.json",
        "books": ["Guyton and Hall Physiology 14th Ed", "Snell's Clinical Anatomy 8th Ed"]
    }
}

def build_exam_databases():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(qbank_dir, exist_ok=True)

    if not os.path.exists(questions_file):
        print("questions.json not found!")
        return

    with open(questions_file, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    print(f"Loaded {len(all_questions)} total MCQs. Partitioning into exam-specific databases...\n")

    summary_results = []

    for cat_id, meta in EXAM_CATEGORIES.items():
        matched_questions = [
            q for q in all_questions 
            if any(b.lower() in q.get("book_source", "").lower() for b in meta["books"])
        ]

        # SQLite DB Path
        db_path = os.path.join(db_dir, meta["db_file"])
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create Table
        cursor.execute("DROP TABLE IF EXISTS mcqs;")
        cursor.execute('''
            CREATE TABLE mcqs (
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

        inserted = 0
        for q in matched_questions:
            try:
                cursor.execute('''
                    INSERT INTO mcqs (id, category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    q.get("id"),
                    q.get("category"),
                    q.get("question"),
                    q.get("option_a"),
                    q.get("option_b"),
                    q.get("option_c"),
                    q.get("option_d"),
                    q.get("option_e"),
                    q.get("correct_answer"),
                    q.get("explanation"),
                    q.get("difficulty", "Hard"),
                    q.get("book_source")
                ))
                inserted += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        conn.close()

        # Save JSON File in qbank/
        json_path = os.path.join(qbank_dir, meta["json_file"])
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(matched_questions, f, indent=2, ensure_ascii=False)

        summary_results.append({
            "category_id": cat_id,
            "title": meta["title"],
            "db_file": meta["db_file"],
            "json_file": meta["json_file"],
            "count": len(matched_questions),
            "books": meta["books"]
        })

        print(f"[OK] Created Exam Database: {meta['db_file']}")
        print(f"   Title: {meta['title']}")
        print(f"   MCQs Count: {len(matched_questions)}")
        print(f"   Books Included: {', '.join(meta['books'])}\n")

    # Update Index File
    exam_index_path = os.path.join(workspace_root, "src", "data", "exam_index.json")
    with open(exam_index_path, "w", encoding="utf-8") as f:
        json.dump(summary_results, f, indent=2, ensure_ascii=False)

    print(f"Created Exam Index: {exam_index_path}")

if __name__ == "__main__":
    build_exam_databases()
