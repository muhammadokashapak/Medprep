import json
import os
import re

chunks_dir = r"E:\USAMA\MBBS Books\MCQ_Generator\chunks"
questions_js_path = r"E:\USAMA\MBBS Books\MCQs List\Quiz_App\questions.js"

# 1. Read existing questions from questions.js
with open(questions_js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract the JSON array from the JS file
match = re.search(r"window\.bankData\s*=\s*(\[.*\]);", js_content, re.DOTALL)
if match:
    existing_mcqs = json.loads(match.group(1))
else:
    print("Error: Could not parse questions.js")
    exit(1)

initial_count = len(existing_mcqs)

# 2. Read new MCQs from JSON files
new_mcqs = []
for i in range(1, 9):
    file_path = os.path.join(chunks_dir, f"mcqs_{i}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                batch = json.load(f)
                new_mcqs.extend(batch)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    else:
        print(f"File not found: {file_path}")

print(f"Loaded {len(new_mcqs)} new MCQs.")

# Format them to match existing schema
max_id = max([q.get('id', 0) for q in existing_mcqs]) if existing_mcqs else 0

for i, q in enumerate(new_mcqs):
    max_id += 1
    formatted_q = {
        "id": max_id,
        "category": "FCPS Topic (Extreme)",
        "question": q.get("question", ""),
        "options": q.get("options", []),
        "correct_answer": q.get("correct_answer", ""),
        "explanation": q.get("explanation", "")
    }
    existing_mcqs.append(formatted_q)

# 3. Save back to questions.js
final_js = f"window.bankData = {json.dumps(existing_mcqs, indent=2)};"

with open(questions_js_path, "w", encoding="utf-8") as f:
    f.write(final_js)

print(f"Successfully added {len(new_mcqs)} MCQs. New total: {len(existing_mcqs)}")
