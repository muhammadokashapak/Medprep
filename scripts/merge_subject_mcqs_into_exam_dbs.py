import os
import sqlite3
import json
import re

# Precise Mapping of Medical Textbooks/Subjects into Target Licensing Exam Databases
EXAM_DISTRIBUTION = {
    "USMLE_Step_1_QBank.db": {
        "title": "USMLE Step 1 QBank",
        "description": "Comprehensive Basic Medical Sciences (First Aid Step 1, Pathoma, Pharmacology, Physiology, Anatomy)",
        "json_file": "USMLE_Step_1_QBank.json",
        "book_sources": [
            "First Aid Step 1 2023",
            "First Aid Q&A Step 1",
            "Pathoma Fundamentals of Pathology",
            "Guyton and Hall Physiology 14th Ed",
            "Snell's Clinical Anatomy 8th Ed",
            "Pharmacology An Illustrated Review",
            "Review of Pharmacology 9th Ed (Garg & Gupta)",
            "Self-Assessment Pharmacology 4th Ed"
        ]
    },
    "USMLE_Step_2_CK_QBank.db": {
        "title": "USMLE Step 2 CK QBank",
        "description": "Clinical Knowledge Board Exam QBank (Internal Medicine, Surgery, Pediatrics, ObGyn, Psych)",
        "json_file": "USMLE_Step_2_CK_QBank.json",
        "book_sources": [
            "First Aid Step 2 CK 10th Ed"
        ]
    },
    "FCPS_Part_1_and_NLE_QBank.db": {
        "title": "FCPS Part 1 & NLE Medical QBank",
        "description": "High-Yield Pakistani Licensing & Residency Exam (ROAMS, Pathoma, Physiology, Anatomy, Pharmacology)",
        "json_file": "FCPS_Part_1_and_NLE_QBank.json",
        "book_sources": [
            "ROAMS Medical Review",
            "Pathoma 2021 Edition",
            "Pathoma Fundamentals of Pathology",
            "Guyton and Hall Physiology 14th Ed",
            "Snell's Clinical Anatomy 8th Ed",
            "Review of Pharmacology 9th Ed (Garg & Gupta)",
            "Self-Assessment Pharmacology 4th Ed"
        ]
    },
    "PLAB_1_and_UKMLA_QBank.db": {
        "title": "PLAB 1 / UKMLA QBank",
        "description": "UK General Medical Council Licensing Exam (Clinical Vignettes, Applied Pharmacology & Guidelines)",
        "json_file": "PLAB_1_and_UKMLA_QBank.json",
        "book_sources": [
            "First Aid Step 2 CK 10th Ed",
            "ROAMS Medical Review",
            "Pharmacology An Illustrated Review"
        ]
    },
    "NEET_PG_and_FMGE_QBank.db": {
        "title": "NEET PG / INI-CET & FMGE QBank",
        "description": "Indian PG Entrance QBank (ROAMS, Pharmacology, Physiology, Anatomy, Pathology)",
        "json_file": "NEET_PG_and_FMGE_QBank.json",
        "book_sources": [
            "Review of Pharmacology 9th Ed (Garg & Gupta)",
            "Self-Assessment Pharmacology 4th Ed",
            "ROAMS Medical Review",
            "Guyton and Hall Physiology 14th Ed",
            "Snell's Clinical Anatomy 8th Ed",
            "Pathoma 2021 Edition"
        ]
    },
    "MRCS_Surgery_QBank.db": {
        "title": "Surgery & MRCS QBank",
        "description": "Royal College of Surgeons MRCS Part A & MS Surgery (Bailey & Love Surgery + Surgical Anatomy)",
        "json_file": "MRCS_Surgery_QBank.json",
        "book_sources": [
            "Bailey & Love Surgery 26th Ed",
            "Snell's Clinical Anatomy 8th Ed"
        ]
    }
}

def merge_and_build_exam_databases():
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
    print("  MERGING SUBJECT MCQS (PHARM/ANATOMY/PHYSIO) INTO EXAM DBS    ")
    print("=================================================================")

    # First clean out old standalone subject DB files
    standalone_subject_files = [
        "Pharmacology_Therapeutics_QBank.db",
        "Anatomy_and_Physiology_QBank.db",
        "pharmacology_pg.db",
        "basic_sciences_anatomy_physio.db"
    ]
    for s_file in standalone_subject_files:
        p = os.path.join(db_dir, s_file)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"Removed standalone subject DB file: {s_file}")
            except Exception as e:
                print(f"Could not remove {s_file}: {e}")

    catalog = []

    for db_filename, config in EXAM_DISTRIBUTION.items():
        # Match MCQs whose book_source matches any of the exam's book_sources
        matched_mcqs = [
            q for q in all_questions
            if any(b_name.lower() in q.get("book_source", "").lower() for b_name in config["book_sources"])
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

        # Save dedicated JSON file
        json_path = os.path.join(qbank_dir, config["json_file"])
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(matched_mcqs, f, indent=2, ensure_ascii=False)

        catalog.append({
            "database_file": db_filename,
            "title": config["title"],
            "description": config["description"],
            "mcq_count": db_count,
            "json_file": f"qbank/{config['json_file']}",
            "books_included": config["book_sources"]
        })

        print(f"[OK] Exam Database Built: {db_filename}")
        print(f"     Title: {config['title']}")
        print(f"     Merged MCQs Count: {db_count:,}")
        print(f"     Books Included: {len(config['book_sources'])} books\n")

    # Update Catalog JSON
    catalog_path = os.path.join(workspace_root, "src", "data", "exam_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("=================================================================")
    print(f" SUCCESS! All {len(catalog)} Databases are Strictly Exam Named.")
    print("=================================================================")

if __name__ == "__main__":
    merge_and_build_exam_databases()
