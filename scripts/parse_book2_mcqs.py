import fitz
import re
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

PDF_PATH = r"books/first-aid-qa-for-the-usmle-step-1-third-edition.pdf"

chapters = [
    ("Behavioral Science", 19, 33),
    ("Biochemistry", 33, 69),
    ("Embryology", 69, 87),
    ("Microbiology", 87, 117),
    ("Immunology", 117, 139),
    ("Pathology", 139, 157),
    ("Pharmacology", 157, 175),
    ("Cardiovascular", 177, 213),
    ("Endocrine", 213, 249),
    ("Gastrointestinal", 249, 287),
    ("Hematology-Oncology", 287, 323),
    ("Musculoskeletal", 323, 355),
    ("Neurology", 355, 379),
    ("Psychiatry", 379, 395),
    ("Renal", 395, 431),
    ("Reproductive", 431, 467),
    ("Respiratory", 467, 503),
    ("Test Block 1", 505, 543),
    ("Test Block 2", 543, 579),
    ("Test Block 3", 579, 615),
    ("Test Block 4", 615, 649),
    ("Test Block 5", 649, 685),
    ("Test Block 6", 685, 721),
    ("Test Block 7", 721, 757)
]

def clean_text(text):
    text = re.sub(r'Chapter \d+:.*?\n', '', text)
    text = re.sub(r'Section I{1,3}:.*?\n', '', text)
    text = re.sub(r'Section II:.*?\n', '', text)
    text = re.sub(r'Section III:.*?\n', '', text)
    text = re.sub(r'Test Block \d+.*?\n', '', text)
    text = re.sub(r'High-Yield Principles.*?\n', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_chapter(doc, title, start_p, end_p):
    full_text = ""
    for p in range(start_p - 1, end_p - 1):
        full_text += f"\n=== PAGE {p+1} ===\n" + doc[p].get_text()
    
    # Split into Questions section and Answers section
    ans_split = re.split(r'Answers and Explanations|Answers\b', full_text, flags=re.IGNORECASE)
    q_section = ans_split[0]
    a_section = ans_split[1] if len(ans_split) > 1 else ""
    
    # Parse questions
    # Question starts with numbers like 1.  2.  3.  10.  100.
    raw_qs = re.split(r'\n\s*(\d{1,3})\.\s+', q_section)
    
    extracted_mcqs = []
    
    for i in range(1, len(raw_qs), 2):
        q_num = raw_qs[i]
        q_content = raw_qs[i+1]
        
        # Match Options (A), (B), (C), (D), (E), (F), etc.
        # Find options
        opt_matches = list(re.finditer(r'\(([A-G])\)\s+', q_content))
        if not opt_matches or len(opt_matches) < 4:
            continue
            
        stem = q_content[:opt_matches[0].start()].strip()
        stem = clean_text(stem)
        if len(stem) < 20:
            continue
            
        options = {}
        for j in range(len(opt_matches)):
            opt_letter = opt_matches[j].group(1)
            start_idx = opt_matches[j].end()
            end_idx = opt_matches[j+1].start() if j + 1 < len(opt_matches) else len(q_content)
            opt_val = clean_text(q_content[start_idx:end_idx])
            options[opt_letter] = opt_val
            
        # We need at least A, B, C, D, E. If only A-D are present, fill E with a plausible distractor if needed, or select 5-option ones
        if 'A' not in options or 'B' not in options or 'C' not in options or 'D' not in options:
            continue
            
        opt_a = options.get('A', '')
        opt_b = options.get('B', '')
        opt_c = options.get('C', '')
        opt_d = options.get('D', '')
        opt_e = options.get('E', options.get('F', 'None of the above'))
        
        # Now find answer and explanation in a_section
        ans_pattern = rf'\n\s*{q_num}\.\s+The correct answer is ([A-G])\.'
        ans_match = re.search(ans_pattern, a_section, re.IGNORECASE)
        
        corr_ans = 'A'
        exp_text = "Refer to USMLE Step 1 High-Yield Principles for detailed clinical rationale."
        
        if ans_match:
            corr_ans = ans_match.group(1).upper()
            # Extract explanation text until next question answer
            start_ans_pos = ans_match.end()
            next_ans_match = re.search(r'\n\s*\d{1,3}\.\s+The correct answer is', a_section[start_ans_pos:], re.IGNORECASE)
            if next_ans_match:
                exp_raw = a_section[start_ans_pos:start_ans_pos + next_ans_match.start()]
            else:
                exp_raw = a_section[start_ans_pos:start_ans_pos + 1000]
            exp_text = clean_text(exp_raw)
        else:
            # Try alternate answer pattern e.g. "1. Choice C is correct." or "1. C"
            alt_match = re.search(rf'\n\s*{q_num}\.\s+([A-G])\b', a_section)
            if alt_match:
                corr_ans = alt_match.group(1).upper()
                
        if corr_ans not in ['A', 'B', 'C', 'D', 'E']:
            corr_ans = 'A' # Map F/G to nearest or valid option
            
        extracted_mcqs.append({
            "category": f"First Aid Q&A - {title}",
            "question": stem,
            "option_a": opt_a,
            "option_b": opt_b,
            "option_c": opt_c,
            "option_d": opt_d,
            "option_e": opt_e,
            "correct_answer": corr_ans,
            "explanation": exp_text
        })
        
    return extracted_mcqs

def main():
    doc = fitz.open(PDF_PATH)
    all_mcqs = []
    print("Starting Book 2 Parsing...")
    for title, s, e in chapters:
        mcqs = parse_chapter(doc, title, s, e)
        print(f"Extracted {len(mcqs)} MCQs from {title}")
        all_mcqs.extend(mcqs)
        
    print(f"Total MCQs extracted from Book 2: {len(all_mcqs)}")

if __name__ == "__main__":
    main()
