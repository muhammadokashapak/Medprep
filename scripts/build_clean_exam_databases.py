import os
import sqlite3
import json
import re

EXAM_DATABASES_CONFIG = {
    "USMLE_Step_1_QBank.db": {
        "title": "USMLE Step 1 QBank",
        "description": "High-Yield Basic Medical Sciences for USMLE Step 1",
        "json_file": "USMLE_Step_1_QBank.json",
        "book_matches": ["First Aid Step 1 2023", "First Aid Q&A Step 1", "Pathoma Fundamentals of Pathology"]
    },
    "USMLE_Step_2_CK_QBank.db": {
        "title": "USMLE Step 2 CK QBank",
        "description": "Clinical Knowledge, Internal Medicine, Pediatrics & Surgery for USMLE Step 2 CK",
        "json_file": "USMLE_Step_2_CK_QBank.json",
        "book_matches": ["First Aid Step 2 CK 10th Ed"]
    },
    "FCPS_Part_1_and_NLE_QBank.db": {
        "title": "FCPS Part 1 & NLE Medical QBank",
        "description": "High-Yield Review for FCPS Part 1, NLE, NEB, and CPSP Residency",
        "json_file": "FCPS_Part_1_and_NLE_QBank.json",
        "book_matches": ["ROAMS Medical Review", "Pathoma 2021 Edition"]
    },
    "PLAB_1_and_UKMLA_QBank.db": {
        "title": "PLAB 1 / UKMLA QBank",
        "description": "High-Yield Clinical Vignettes for GMC PLAB 1 & UKMLA Exams",
        "json_file": "PLAB_1_and_UKMLA_QBank.json",
        "book_matches": ["First Aid Step 2 CK 10th Ed", "ROAMS Medical Review"]
    },
    "NEET_PG_and_FMGE_QBank.db": {
        "title": "NEET PG / INI-CET & FMGE QBank",
        "description": "Comprehensive PG Medical Entrance QBank for NEET PG, FMGE & INI-CET",
        "json_file": "NEET_PG_and_FMGE_QBank.json",
        "book_matches": ["Review of Pharmacology 9th Ed (Garg & Gupta)", "ROAMS Medical Review", "Self-Assessment Pharmacology 4th Ed"]
    },
    "MRCS_Surgery_QBank.db": {
        "title": "Surgery & MRCS QBank",
        "description": "General Surgery, Trauma & Surgical Specialties for MRCS Part A & MS Surgery",
        "json_file": "MRCS_Surgery_QBank.json",
        "book_matches": ["Bailey & Love Surgery 26th Ed"]
    },
    "Pharmacology_Therapeutics_QBank.db": {
        "title": "Pharmacology & Therapeutics QBank",
        "description": "Master QBank for Pharmacology, MOA, Adverse Effects & Drug Interactions",
        "json_file": "Pharmacology_Therapeutics_QBank.json",
        "book_matches": ["Self-Assessment Pharmacology 4th Ed", "Pharmacology An Illustrated Review", "Review of Pharmacology 9th Ed (Garg & Gupta)"]
    },
    "Anatomy_and_Physiology_QBank.db": {
        "title": "Anatomy & Physiology QBank",
        "description": "Core Basic Sciences (Guyton Physiology & Snell Anatomy) for MBBS 1st/2nd Proff, AMC & MCCQE",
        "json_file": "Anatomy_and_Physiology_QBank.json",
        "book_matches": ["Guyton and Hall Physiology 14th Ed", "Snell's Clinical Anatomy 8th Ed"]
    }
}

def build_named_exam_databases():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(qbank_dir, exist_ok=True)

    if not os.path.exists(questions_file):
        print("questions.json file not found!")
        return

    with open(questions_file, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    print("=================================================================")
    print("  CREATING NAMED TEST DATABASES IN DATABASE/ FOLDER (.DB)        ")
    print("=================================================================")

    catalog = []

    for db_filename, config in EXAM_DATABASES_CONFIG.items():
        matched_mcqs = [
            q for q in all_questions
            if any(b_name.lower() in q.get("book_source", "").lower() for b_name in config["book_matches"])
        ]

        db_path = os.path.join(db_dir, db_filename)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS mcqs;")
        cursor.execute('''
            CREATE TABLE mcqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL UNIQUE,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                option_e TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT NOT NULL,
                difficulty TEXT DEFAULT 'Hard',
                book_source TEXT NOT NULL
            );
        ''')

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mcqs_category ON mcqs(category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mcqs_book ON mcqs(book_source);")

        for q in matched_mcqs:
            try:
                cursor.execute('''
                    INSERT INTO mcqs (category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
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
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        db_count = cursor.execute("SELECT COUNT(*) FROM mcqs;").fetchone()[0]
        conn.close()

        # Save dedicated JSON file in qbank/
        json_path = os.path.join(qbank_dir, config["json_file"])
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(matched_mcqs, f, indent=2, ensure_ascii=False)

        catalog.append({
            "database_file": db_filename,
            "title": config["title"],
            "description": config["description"],
            "mcq_count": db_count,
            "json_file": f"qbank/{config['json_file']}",
            "books_included": config["book_matches"]
        })

        print(f"[OK] Database File Created: {db_filename}")
        print(f"     Exam Title: {config['title']}")
        print(f"     MCQs Count: {db_count:,}\n")

    catalog_path = os.path.join(workspace_root, "src", "data", "exam_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("=================================================================")
    print(" SUCCESS! All Database files are named directly after the tests.")
    print("=================================================================")

if __name__ == "__main__":
    build_named_exam_databases()
