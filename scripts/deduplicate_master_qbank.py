import os
import sqlite3
import json
import re

def normalize_stem(stem):
    """Strips variable question number prefixes and normalizes text for deduplication."""
    # Strip prefixes like "Question #123 [Book Name]: " or "Batch 1 - Question: "
    cleaned = re.sub(r'^Question\s+#\d+\s+\[[^\]]+\]:\s*', '', stem, flags=re.IGNORECASE)
    cleaned = re.sub(r'^Batch\s+\d+\s+-\s+Question:\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return cleaned

def deduplicate_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")

    if not os.path.exists(questions_file):
        print("questions.json file not found!")
        return

    with open(questions_file, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    print("=================================================================")
    print("        MEDPREP PRO MASTER QBANK DEDUPLICATION ENGINE            ")
    print("=================================================================")
    print(f"Total Raw MCQs in Master Pool: {len(all_questions):,}")

    seen_stems = set()
    unique_questions = []
    duplicate_count = 0

    for q in all_questions:
        stem = q.get("question", "")
        norm = normalize_stem(stem)
        
        # Also check option_a text to differentiate identical clinical vignettes
        opt_a = str(q.get("option_a", "")).strip().lower()
        unique_key = f"{norm} ||| {opt_a}"

        if unique_key in seen_stems:
            duplicate_count += 1
        else:
            seen_stems.add(unique_key)
            unique_questions.append(q)

    print(f"\n--- Master Deduplication Analysis ---")
    print(f"Total Input MCQs: {len(all_questions):,}")
    print(f"Duplicates Removed: {duplicate_count:,}")
    print(f"100% Unique MCQs Retained: {len(unique_questions):,}")

    # Re-assign clean IDs
    for idx, q in enumerate(unique_questions):
        q["id"] = idx + 1

    # Overwrite main questions.json
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(unique_questions, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Saved 100% unique dataset to: {questions_file}")

    # Deduplicate each specific SQLite Database File
    db_files = [f for f in os.listdir(db_dir) if f.endswith(".db")]
    print(f"\nDeduplicating and Syncing {len(db_files)} SQLite Database files in database/...")

    for db_name in db_files:
        db_path = os.path.join(db_dir, db_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all rows
        rows = cursor.execute("SELECT id, category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source FROM mcqs;").fetchall()
        
        db_seen = set()
        unique_db_rows = []
        db_dupes = 0

        for r in rows:
            q_id, cat, q_text, opt_a, opt_b, opt_c, opt_d, opt_e, corr, exp, diff, b_source = r
            norm = normalize_stem(q_text)
            key = f"{norm} ||| {opt_a.strip().lower()}"

            if key in db_seen:
                db_dupes += 1
            else:
                db_seen.add(key)
                unique_db_rows.append(r)

        # Clear and re-insert unique rows
        cursor.execute("DELETE FROM mcqs;")
        inserted_db = 0
        for r in unique_db_rows:
            q_id, cat, q_text, opt_a, opt_b, opt_c, opt_d, opt_e, corr, exp, diff, b_source = r
            try:
                cursor.execute('''
                    INSERT INTO mcqs (category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (cat, q_text, opt_a, opt_b, opt_c, opt_d, opt_e, corr, exp, diff, b_source))
                inserted_db += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        final_count = cursor.execute("SELECT COUNT(*) FROM mcqs;").fetchone()[0]
        conn.close()

        print(f"[OK] Database '{db_name}': {db_dupes:,} duplicates removed. {final_count:,} 100% Unique MCQs retained.")

    print("\n=================================================================")
    print(" SUCCESS! All Database files are 100% Deduplicated and Unique.")
    print("=================================================================")

if __name__ == "__main__":
    deduplicate_qbank()
