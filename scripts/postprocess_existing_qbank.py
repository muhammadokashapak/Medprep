import os
import json
import re
import random

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

def postprocess_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    
    if not os.path.exists(questions_file):
        print(f"File not found: {questions_file}")
        return

    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Loaded {len(questions)} existing questions.")
    
    sanitized_count = 0
    rejected_meta_count = 0
    answer_dist_before = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    answer_dist_after = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    
    processed_questions = []

    for q in questions:
        ans = str(q.get("correct_answer", "")).strip().upper()
        if ans.startswith("OPTION_"): ans = ans.replace("OPTION_", "")
        if ans.startswith("OPTION "): ans = ans.replace("OPTION ", "")
        if ans in answer_dist_before:
            answer_dist_before[ans] += 1

        # Check for 5 options
        opt_a = str(q.get("option_a", "")).strip()
        opt_b = str(q.get("option_b", "")).strip()
        opt_c = str(q.get("option_c", "")).strip()
        opt_d = str(q.get("option_d", "")).strip()
        opt_e = str(q.get("option_e", "")).strip()

        if not (opt_a and opt_b and opt_c and opt_d and opt_e and ans in ["A", "B", "C", "D", "E"]):
            continue

        opts_dict = {"A": opt_a, "B": opt_b, "C": opt_c, "D": opt_d, "E": opt_e}
        correct_text = opts_dict[ans]

        # Banned meta check
        has_meta = False
        for text in opts_dict.values():
            for pat in BANNED_PATTERNS:
                if re.search(pat, text, re.IGNORECASE):
                    has_meta = True
                    break
            if has_meta:
                break
                
        if has_meta:
            rejected_meta_count += 1
            continue

        # Shuffle options to balance correct answer distribution
        all_options = [opt_a, opt_b, opt_c, opt_d, opt_e]
        random.shuffle(all_options)

        keys = ["A", "B", "C", "D", "E"]
        new_opts = {}
        new_ans = None
        for idx, text in enumerate(all_options):
            k = keys[idx]
            new_opts[f"option_{k.lower()}"] = text
            if text == correct_text:
                new_ans = k

        q["option_a"] = new_opts["option_a"]
        q["option_b"] = new_opts["option_b"]
        q["option_c"] = new_opts["option_c"]
        q["option_d"] = new_opts["option_d"]
        q["option_e"] = new_opts["option_e"]
        q["correct_answer"] = new_ans
        
        answer_dist_after[new_ans] += 1
        processed_questions.append(q)
        sanitized_count += 1

    print("\n--- Post-Processing Results ---")
    print(f"Original total questions: {len(questions)}")
    print(f"Rejected due to meta-options ('All/None of the above'): {rejected_meta_count}")
    print(f"Sanitized & anti-trick balanced questions: {len(processed_questions)}")
    print(f"\nAnswer Distribution BEFORE Shuffling: {answer_dist_before}")
    print(f"Answer Distribution AFTER Shuffling:  {answer_dist_after}")

    # Write back sanitized questions
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(processed_questions, f, indent=2, ensure_ascii=False)
        
    print(f"\nUpdated {questions_file} with anti-trick balanced dataset.")

if __name__ == "__main__":
    postprocess_qbank()
