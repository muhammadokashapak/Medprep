import os
import sys
import json
import re
import random
import time
import argparse
from datetime import datetime

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

BANNED_PATTERNS = [
    r"\ball of the above\b",
    r"\bnone of the above\b",
    r"\bboth [a-e] and [a-e]\b",
    r"\bneither [a-e] nor [a-e]\b",
    r"\ball of these\b",
    r"\bnone of these\b",
    r"\bchoices [a-e] and [a-e]\b",
    r"\boptions? [a-e] and [a-e]\b"
]

def get_pdf_page_count(pdf_path):
    if not pypdf:
        return 0
    try:
        reader = pypdf.PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        print(f"Error counting pages in {pdf_path}: {e}")
        return 0

def extract_pdf_chunk(pdf_path, start_page, end_page, max_chars=12000):
    if not pypdf:
        return ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        total = len(reader.pages)
        start_page = max(1, start_page)
        end_page = min(total, end_page)
        
        text = ""
        for page_num in range(start_page - 1, end_page):
            t = reader.pages[page_num].extract_text()
            if t:
                text += f"\n--- Page {page_num + 1} ---\n" + t
                if len(text) >= max_chars:
                    break
        return text
    except Exception as e:
        print(f"Extraction error: {e}")
        return ""

def sanitize_mcq(raw_mcq, book_name):
    required_keys = ["question", "option_a", "option_b", "option_c", "option_d", "option_e", "correct_answer", "explanation"]
    for key in required_keys:
        if key not in raw_mcq or not str(raw_mcq[key]).strip():
            return None, False, f"Missing key: {key}"

    correct_key = str(raw_mcq["correct_answer"]).strip().upper()
    if correct_key.startswith("OPTION_"): correct_key = correct_key.replace("OPTION_", "")
    if correct_key.startswith("OPTION "): correct_key = correct_key.replace("OPTION ", "")
    if correct_key not in ["A", "B", "C", "D", "E"]:
        return None, False, f"Invalid correct_answer: {correct_key}"

    options_map = {
        "A": str(raw_mcq["option_a"]).strip(),
        "B": str(raw_mcq["option_b"]).strip(),
        "C": str(raw_mcq["option_c"]).strip(),
        "D": str(raw_mcq["option_d"]).strip(),
        "E": str(raw_mcq["option_e"]).strip()
    }
    
    correct_option_text = options_map[correct_key]

    # Anti-meta check
    for opt_key, opt_text in options_map.items():
        for pat in BANNED_PATTERNS:
            if re.search(pat, opt_text, re.IGNORECASE):
                return None, False, f"Option {opt_key} contains banned meta pattern: '{pat}'"

    # Stem length check
    if len(str(raw_mcq["question"]).strip()) < 90:
        return None, False, "Vignette stem too short"

    # Distractor length check
    lens = [len(txt) for txt in options_map.values()]
    avg_len = sum(lens) / 5.0
    max_dev = max(abs(l - avg_len) for l in lens)
    if avg_len > 20 and (max_dev / avg_len) > 0.70:
        if len(correct_option_text) == max(lens):
            return None, False, "Rejected: Longest option bias"

    # Shuffle choices to guarantee equal distribution across A-E
    pairs = list(options_map.values())
    random.shuffle(pairs)
    
    keys = ["A", "B", "C", "D", "E"]
    new_options = {}
    new_correct = None
    for idx, txt in enumerate(pairs):
        k = keys[idx]
        new_options[f"option_{k.lower()}"] = txt
        if txt == correct_option_text:
            new_correct = k

    cleaned = {
        "category": str(raw_mcq.get("category", "General Medicine")).strip(),
        "question": str(raw_mcq["question"]).strip(),
        "option_a": new_options["option_a"],
        "option_b": new_options["option_b"],
        "option_c": new_options["option_c"],
        "option_d": new_options["option_d"],
        "option_e": new_options["option_e"],
        "correct_answer": new_correct,
        "explanation": str(raw_mcq["explanation"]).strip(),
        "difficulty": str(raw_mcq.get("difficulty", "Hard")).strip(),
        "book_source": book_name
    }
    return cleaned, True, "OK"

def generate_mcqs_from_text(text, api_key, book_name, num_mcqs=5):
    if not genai:
        return []
    genai.configure(api_key=api_key)

    prompt = f"""
You are an expert medical board exam author creating hard, high-yield clinical MCQs.
Extract concepts from the source text and write {num_mcqs} UNIQUE, HIGH-DIFFICULTY multiple choice questions.

ANTI-TRICK RULES:
1. Write multi-step clinical vignettes (Patient scenario $\\rightarrow$ ask for underlying mechanism, lab finding, or second-line management).
2. NEVER use "All of the above", "None of the above", or "Both A and B". All choices must be realistic medical choices.
3. Make options A-E equal in length and complexity. Do not make the correct choice longer.
4. Distribute correct answers across A, B, C, D, E.
5. Provide detailed explanation for why the correct option is right and distractors are wrong.

Return ONLY raw JSON list of objects:
[
  {{
    "category": "Subject - Topic",
    "question": "Clinical scenario...",
    "option_a": "Choice A",
    "option_b": "Choice B",
    "option_c": "Choice C",
    "option_d": "Choice D",
    "option_e": "Choice E",
    "correct_answer": "D",
    "explanation": "High yield explanation...",
    "difficulty": "Hard",
    "book_source": "{book_name}"
  }}
]

SOURCE TEXT:
\"\"\"
{text}
\"\"\"
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content(prompt)
        raw_text = resp.text.strip()
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\n", "", raw_text)
            raw_text = re.sub(r"\n```$", "", raw_text)
        items = json.loads(raw_text)
        
        valid = []
        for raw in items:
            cleaned, ok, reason = sanitize_mcq(raw, book_name)
            if ok:
                valid.append(cleaned)
            else:
                print(f"Filtered out question: {reason}")
        return valid
    except Exception as e:
        print(f"API generation error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Batch MCQ Generator for MedPrep Pro App")
    parser.add_argument("--book_idx", type=int, default=None, help="Index of book to generate from (1-12)")
    parser.add_argument("--mcqs_target", type=int, default=100, help="Target number of MCQs to generate per run")
    parser.add_argument("--batch_size", type=int, default=5, help="MCQs per API request")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY environment variable.")
        return

    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    books_dir = os.path.join(workspace_root, "books")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")

    pdf_files = [f for f in os.listdir(books_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDF files in books directory.")
        return

    print("==================================================")
    print("      MedPrep Pro Batch MCQ Generator             ")
    print("==================================================")

    if args.book_idx is not None and 1 <= args.book_idx <= len(pdf_files):
        selected_books = [pdf_files[args.book_idx - 1]]
    else:
        selected_books = pdf_files

    # Load existing questions to maintain IDs
    existing = []
    if os.path.exists(questions_file):
        with open(questions_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

    next_id = max([q.get("id", 0) for q in existing] + [0]) + 1

    for b_idx, book_filename in enumerate(selected_books):
        book_path = os.path.join(books_dir, book_filename)
        total_pages = get_pdf_page_count(book_path)
        print(f"\n[{b_idx+1}/{len(selected_books)}] Processing: {book_filename} ({total_pages} pages)")

        generated_for_book = 0
        current_page = 1

        while generated_for_book < args.mcqs_target and current_page < total_pages:
            end_p = min(current_page + 6, total_pages)
            print(f"Reading pages {current_page} to {end_p}...")
            text_chunk = extract_pdf_chunk(book_path, current_page, end_p)
            current_page = end_p + 1

            if not text_chunk.strip():
                continue

            num_to_req = min(args.batch_size, args.mcqs_target - generated_for_book)
            print(f"Requesting {num_to_req} anti-trick MCQs...")
            mcqs = generate_mcqs_from_text(text_chunk, api_key, book_filename, num_to_req)

            if mcqs:
                for q in mcqs:
                    q["id"] = next_id
                    next_id += 1
                    existing.append(q)
                    generated_for_book += 1

                # Save progress incrementally
                with open(questions_file, "w", encoding="utf-8") as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)

                print(f"Progress: {generated_for_book}/{args.mcqs_target} generated for this book. Total QBank size: {len(existing)}")
            
            time.sleep(1) # Prevent API rate limits

    print(f"\nDone! QBank now contains {len(existing)} total questions.")

if __name__ == "__main__":
    main()
