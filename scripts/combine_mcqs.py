import json
import random
import sys
import os

# Ensure the paths are in sys.path if needed, but we can just import directly since they are in the same dir
sys.path.append(r"E:\USAMA\MBBS Books\MCQ_Generator")

from gen_part1 import q_list_1
from gen_part2 import q_list_2

all_qs = q_list_1 + q_list_2

if len(all_qs) != 50:
    print(f"Error: Expected 50 questions, got {len(all_qs)}")
    sys.exit(1)

# We want exactly 10 of each correct answer
targets = ['A']*10 + ['B']*10 + ['C']*10 + ['D']*10 + ['E']*10
random.seed(42) # Optional: reproducible shuffling of targets, but let's just use random
random.shuffle(targets)

final_json = []

for i, q in enumerate(all_qs):
    target_letter = targets[i]
    target_idx = ord(target_letter) - ord('A')
    
    # We have 4 distractors.
    distractors = q['d'].copy()
    random.shuffle(distractors)
    
    # Insert the correct answer at the target index
    options = distractors.copy()
    options.insert(target_idx, q['c'])
    
    final_json.append({
        "question": q['q'],
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "option_e": options[4],
        "correct_answer": target_letter,
        "explanation": q['e'],
        "source_context": q['s']
    })

# Shuffle the final array so the test itself doesn't have a predictable pattern
# (Wait, if I shuffle the final_json, the answer distribution remains exactly 10 of each!)
random.shuffle(final_json)

out_dir = r"E:\USAMA\MBBS Books\MCQ_Generator\batches"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "bank_batch_genpath2.json")

with open(out_file, "w", encoding="utf-8") as f:
    json.dump(final_json, f, indent=2)

print(f"Successfully wrote 50 MCQs to {out_file}")
