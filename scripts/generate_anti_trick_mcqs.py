import os
import sys
import json
import re
import random
import time
from datetime import datetime

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Banned meta-tricks in option choices
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

def extract_text_from_pdf(pdf_path, start_page=1, end_page=None, max_chars=15000):
    """Extracts text from a given PDF path between specified pages."""
    if not pypdf:
        print("Error: 'pypdf' is not installed.")
        return ""
        
    try:
        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        end_page = end_page or total_pages
        start_page = max(1, start_page)
        end_page = min(total_pages, end_page)
        
        extracted_text = ""
        for page_num in range(start_page - 1, end_page):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                extracted_text += f"\n--- Page {page_num + 1} ---\n" + text
                if len(extracted_text) >= max_chars:
                    break
        return extracted_text
    except Exception as e:
        print(f"PDF extraction error for {pdf_path}: {e}")
        return ""

def sanitize_mcq(raw_mcq):
    """
    Cleans, shuffles, balances distractor lengths, and validates an MCQ object.
    Returns (cleaned_mcq, is_valid, reason)
    """
    required_keys = ["question", "option_a", "option_b", "option_c", "option_d", "option_e", "correct_answer", "explanation"]
    for key in required_keys:
        if key not in raw_mcq or not str(raw_mcq[key]).strip():
            return None, False, f"Missing or empty field: {key}"
            
    # Normalize correct_answer key ('A', 'B', 'C', 'D', 'E')
    correct_key = str(raw_mcq["correct_answer"]).strip().upper()
    if correct_key.startswith("OPTION_"):
        correct_key = correct_key.replace("OPTION_", "")
    if correct_key.startswith("OPTION "):
        correct_key = correct_key.replace("OPTION ", "")
    if correct_key not in ["A", "B", "C", "D", "E"]:
        return None, False, f"Invalid correct_answer key: {raw_mcq.get('correct_answer')}"

    options_map = {
        "A": str(raw_mcq["option_a"]).strip(),
        "B": str(raw_mcq["option_b"]).strip(),
        "C": str(raw_mcq["option_c"]).strip(),
        "D": str(raw_mcq["option_d"]).strip(),
        "E": str(raw_mcq["option_e"]).strip()
    }
    
    correct_option_text = options_map[correct_key]
    
    # 1. Anti-Meta Check
    for opt_key, opt_text in options_map.items():
        for pat in BANNED_PATTERNS:
            if re.search(pat, opt_text, re.IGNORECASE):
                return None, False, f"Option {opt_key} contains banned meta-choice pattern: '{pat}'"
                
    # 2. Hard Vignette Length Check (>100 chars required for high-yield scenario)
    if len(str(raw_mcq["question"]).strip()) < 100:
        return None, False, "Question vignette too short for high-difficulty clinical scenario."

    # 3. Distractor Length Uniformity Check
    lens = [len(txt) for txt in options_map.values()]
    avg_len = sum(lens) / 5.0
    max_dev = max(abs(l - avg_len) for l in lens)
    # If maximum deviation is > 65% of average length, options are unbalanced in length
    if avg_len > 20 and (max_dev / avg_len) > 0.65:
        # Check if the correct answer is the longest option (longest option bias!)
        longest_len = max(lens)
        if len(correct_option_text) == longest_len:
            return None, False, "Correct answer rejected due to Longest Option Bias."

    # 4. Shuffle Options & Reassign Answer Key for Strict ~20% Equal Distribution
    option_pairs = list(options_map.values())
    random.shuffle(option_pairs)
    
    new_keys = ["A", "B", "C", "D", "E"]
    new_options = {}
    new_correct_key = None
    
    for idx, text in enumerate(option_pairs):
        k = new_keys[idx]
        new_options[f"option_{k.lower()}"] = text
        if text == correct_option_text:
            new_correct_key = k
            
    cleaned_mcq = {
        "category": str(raw_mcq.get("category", "General Medicine")).strip(),
        "question": str(raw_mcq["question"]).strip(),
        "option_a": new_options["option_a"],
        "option_b": new_options["option_b"],
        "option_c": new_options["option_c"],
        "option_d": new_options["option_d"],
        "option_e": new_options["option_e"],
        "correct_answer": new_correct_key,
        "explanation": str(raw_mcq["explanation"]).strip(),
        "difficulty": str(raw_mcq.get("difficulty", "Hard")).strip(),
        "book_source": str(raw_mcq.get("book_source", "Medical Textbook")).strip()
    }
    
    return cleaned_mcq, True, "OK"

def generate_anti_trick_mcqs(text, api_key, exam_name, num_mcqs=5, book_name="Medical Textbook"):
    """Queries Gemini API with anti-trick guidelines and parses response."""
    if not genai:
        print("Error: google-generativeai module not found.")
        return []

    genai.configure(api_key=api_key)
    
    prompt = f"""
You are an elite medical board exam author creating top-tier, hard clinical vignette MCQs for {exam_name}.
Use the provided textbook source text to generate {num_mcqs} UNIQUE, HIGH-DIFFICULTY multiple choice questions.

STRICT WRITING & ANTI-TRICK RULES:
1. VIGNETTE: Write multi-step clinical vignettes (Patient age/gender $\\rightarrow$ history $\\rightarrow$ labs/vitals $\\rightarrow$ ask for underlying molecular mechanism, next best diagnostic step, or second-line management).
2. NO TRICKS / NO META-OPTIONS:
   - DO NOT include "All of the above", "None of the above", "Both A and C", or similar choices under any circumstances.
   - All 5 choices (A, B, C, D, E) MUST be plausible, real clinical entities (drugs, enzymes, diagnoses, or procedures).
3. LENGTH BALANCING:
   - Make all 5 options of NEAR-EQUAL CHARACTER LENGTH and grammatical structure. Do NOT make the correct answer significantly longer or more detailed than distractors.
4. ANSWER DISTRIBUTION:
   - Distribute correct answers across A, B, C, D, and E equally.
5. EXPLANATION:
   - Provide a comprehensive, high-yield explanation detailing why the correct option is right and why each of the 4 distractors is wrong.

RETURN FORMAT:
Return strictly a raw JSON array of objects. Do not surround with markdown code blocks (no ```json).

JSON Structure:
[
  {{
    "category": "Subject - System, Topic",
    "question": "A 45-year-old male presents with... What is the most likely underlying mechanism?",
    "option_a": "Symmetrical Distractor A",
    "option_b": "Symmetrical Distractor B",
    "option_c": "Symmetrical Distractor C",
    "option_d": "Symmetrical Distractor D",
    "option_e": "Symmetrical Distractor E",
    "correct_answer": "C",
    "explanation": "Detailed mechanism explanation...",
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
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\n", "", raw_text)
            raw_text = re.sub(r"\n```$", "", raw_text)
            
        raw_mcqs = json.loads(raw_text)
        
        valid_mcqs = []
        for raw in raw_mcqs:
            cleaned, is_valid, reason = sanitize_mcq(raw)
            if is_valid:
                valid_mcqs.append(cleaned)
            else:
                print(f"Skipped question due to anti-trick filter: {reason}")
                
        return valid_mcqs
    except Exception as e:
        print(f"Gemini API error or JSON parse failure: {e}")
        return []

def main():
    print("==========================================================")
    print("     MedPrep Pro Anti-Trick High-Difficulty MCQ Generator ")
    print("==========================================================")
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    books_dir = os.path.join(workspace_root, "books")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    os.makedirs(qbank_dir, exist_ok=True)
    
    if not os.path.exists(books_dir):
        print(f"Books directory not found: {books_dir}")
        return
        
    books = [f for f in os.listdir(books_dir) if f.lower().endswith(".pdf")]
    print(f"Found {len(books)} books in {books_dir}:")
    for i, b in enumerate(books):
        print(f" [{i+1}] {b}")
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = input("\nEnter your Gemini API Key (or set GEMINI_API_KEY env): ").strip()
        
    if not api_key:
        print("API Key required. Exiting.")
        return
        
    print("\nStarting generation test batch...")
    # Select first book for demonstration run
    selected_book = books[0]
    book_path = os.path.join(books_dir, selected_book)
    
    print(f"\nProcessing book: {selected_book}")
    extracted = extract_text_from_pdf(book_path, start_page=15, end_page=25, max_chars=8000)
    if not extracted:
        print("Could not extract text.")
        return
        
    print(f"Extracted {len(extracted)} characters. Requesting anti-trick MCQs...")
    mcqs = generate_anti_trick_mcqs(extracted, api_key, "USMLE Step 1 / FCPS Part 1", num_mcqs=5, book_name=selected_book)
    
    print(f"\nGenerated {len(mcqs)} anti-trick MCQs successfully.")
    for idx, q in enumerate(mcqs):
        print(f"\n--- Question {idx+1} [Answer: {q['correct_answer']}] ---")
        print(f"Stem: {q['question'][:120]}...")
        print(f"A: {q['option_a']}")
        print(f"B: {q['option_b']}")
        print(f"C: {q['option_c']}")
        print(f"D: {q['option_d']}")
        print(f"E: {q['option_e']}")

if __name__ == "__main__":
    main()
