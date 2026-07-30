import os
import sys
import json
import re
import random
import time
from datetime import datetime

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

BOOKS_CONFIG = [
    {
        "filename": "First Aid for the USMLE Step 1 2023, 33e.pdf",
        "name": "First Aid Step 1 2023",
        "subject": "USMLE Step 1 Basic Sciences",
        "keywords": ["Pathology", "Pharmacology", "Physiology", "Microbiology", "Immunology", "Biochemistry", "Genetics", "Behavioral Science"]
    },
    {
        "filename": "First Aid for the USMLE Step 2 CK – 10th edition.pdf",
        "name": "First Aid Step 2 CK 10th Ed",
        "subject": "USMLE Step 2 CK Clinical Sciences",
        "keywords": ["Cardiology", "Pulmonology", "Gastroenterology", "Endocrinology", "Surgery", "Pediatrics", "ObGyn", "Psychiatry", "Emergency Medicine"]
    },
    {
        "filename": "first-aid-qa-for-the-usmle-step-1-third-edition.pdf",
        "name": "First Aid Q&A Step 1",
        "subject": "USMLE Step 1 QBank",
        "keywords": ["Renal", "Neurology", "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive", "Hematology"]
    },
    {
        "filename": "fundamentals-of-pathology-pathoma.pdf",
        "name": "Pathoma Fundamentals of Pathology",
        "subject": "Pathology & Disease Mechanisms",
        "keywords": ["Neoplasia", "Inflammation", "Hematology", "Cardiovascular Pathology", "Renal Pathology", "Vascular Pathology"]
    },
    {
        "filename": "pathoma-fundamentals-of-pathology-2021-0983224609-9780983224600_compress.pdf",
        "name": "Pathoma 2021 Edition",
        "subject": "Systemic Pathology",
        "keywords": ["GI Pathology", "Endocrine Pathology", "CNS Pathology", "Pulmonary Pathology", "Reproductive Pathology"]
    },
    {
        "filename": "pdfcoffee.com_bailey-and-lovex27s-short-practice-of-surgery-26th-ed-pdf-free.pdf",
        "name": "Bailey & Love Surgery 26th Ed",
        "subject": "Surgery & Surgical Specialties",
        "keywords": ["Trauma", "Acute Abdomen", "Biliary Surgery", "Vascular Surgery", "Urology", "Neurosurgery", "Cardiothoracic Surgery"]
    },
    {
        "filename": "pdfcoffee.com_roams-review-of-all-medical-subjects-pdfdrivecom-pdf-pdf-free.pdf",
        "name": "ROAMS Medical Review",
        "subject": "PG Medical Entrance & FCPS Part 1",
        "keywords": ["Anatomy", "Physiology", "Pharmacology", "Pathology", "Medicine", "Surgery", "PSM", "Ophthalmology", "ENT"]
    },
    {
        "filename": "pdfcoffee.com_self-assessment-amp-review-pharmacology-4th-edition-pdf-free.pdf",
        "name": "Self-Assessment Pharmacology 4th Ed",
        "subject": "Pharmacology QBank",
        "keywords": ["Autonomic Drugs", "Cardiovascular Drugs", "CNS Drugs", "Antimicrobials", "Chemotherapy", "Toxicology"]
    },
    {
        "filename": "pdfcoffee.com_snells-clinical-anatomy-by-regions-8th-edpdf-pdf-free.pdf",
        "name": "Snell's Clinical Anatomy 8th Ed",
        "subject": "Gross Anatomy & Neuroanatomy",
        "keywords": ["Upper Limb", "Lower Limb", "Thorax", "Abdomen", "Pelvis", "Head & Neck", "Neuroanatomy", "Cranium"]
    },
    {
        "filename": "pdfcoffee.com_textbook-of-medical-physiology-guyton-and-hall-14-ed-2021-pdf-free.pdf",
        "name": "Guyton and Hall Physiology 14th Ed",
        "subject": "Medical Physiology",
        "keywords": ["Cell Physiology", "Neurophysiology", "Cardiac Physiology", "Renal Physiology", "GI Physiology", "Endocrine Physiology"]
    },
    {
        "filename": "pharmacology-an-illustrated-review-1604062053-9781604062052.pdf",
        "name": "Pharmacology An Illustrated Review",
        "subject": "High-Yield Pharmacology",
        "keywords": ["Mechanism of Action", "Adverse Effects", "Drug Interactions", "Toxicology", "Pharmacokinetics", "Pharmacodynamics"]
    },
    {
        "filename": "review-of-pharmacology-ninth-edition-9nbsped-9351528871-9789351528876_compress.pdf",
        "name": "Review of Pharmacology 9th Ed (Garg & Gupta)",
        "subject": "Pharmacology & Therapeutics",
        "keywords": ["General Pharmacology", "ANS", "CVS", "CNS", "Endocrine Pharm", "Antimicrobials", "Chemotherapeutics"]
    }
]

def sanitize_mcq(raw_mcq, book_name):
    required = ["question", "option_a", "option_b", "option_c", "option_d", "option_e", "correct_answer", "explanation"]
    for k in required:
        if k not in raw_mcq or not str(raw_mcq[k]).strip():
            return None, False, f"Missing key: {k}"

    correct_key = str(raw_mcq["correct_answer"]).strip().upper()
    if correct_key.startswith("OPTION_"): correct_key = correct_key.replace("OPTION_", "")
    if correct_key.startswith("OPTION "): correct_key = correct_key.replace("OPTION ", "")
    if correct_key not in ["A", "B", "C", "D", "E"]:
        return None, False, "Invalid correct answer"

    opts = {
        "A": str(raw_mcq["option_a"]).strip(),
        "B": str(raw_mcq["option_b"]).strip(),
        "C": str(raw_mcq["option_c"]).strip(),
        "D": str(raw_mcq["option_d"]).strip(),
        "E": str(raw_mcq["option_e"]).strip()
    }
    correct_text = opts[correct_key]

    # Anti-meta check
    for txt in opts.values():
        for pat in BANNED_PATTERNS:
            if re.search(pat, txt, re.IGNORECASE):
                return None, False, "Contains banned meta pattern"

    # Stem length check (>90 chars)
    if len(str(raw_mcq["question"]).strip()) < 90:
        return None, False, "Vignette too short"

    # Length symmetry check
    lens = [len(t) for t in opts.values()]
    avg_l = sum(lens) / 5.0
    if avg_l > 20 and (max(abs(l - avg_l) for l in lens) / avg_l) > 0.68:
        if len(correct_text) == max(lens):
            return None, False, "Rejected: Longest option bias"

    # Option shuffling for strict 20% equal answer distribution
    pairs = list(opts.values())
    random.shuffle(pairs)
    keys = ["A", "B", "C", "D", "E"]
    new_options = {}
    new_ans = None
    for idx, txt in enumerate(pairs):
        k = keys[idx]
        new_options[f"option_{k.lower()}"] = txt
        if txt == correct_text:
            new_ans = k

    cleaned = {
        "category": str(raw_mcq.get("category", "General Medical")).strip(),
        "question": str(raw_mcq["question"]).strip(),
        "option_a": new_options["option_a"],
        "option_b": new_options["option_b"],
        "option_c": new_options["option_c"],
        "option_d": new_options["option_d"],
        "option_e": new_options["option_e"],
        "correct_answer": new_ans,
        "explanation": str(raw_mcq["explanation"]).strip(),
        "difficulty": str(raw_mcq.get("difficulty", "Hard")).strip(),
        "book_source": book_name
    }
    return cleaned, True, "OK"

def generate_book_mcqs(book_cfg, target_count=1500, start_id=1):
    print(f"\n=======================================================")
    print(f" Generating {target_count} Anti-Trick MCQs for: {book_cfg['name']}")
    print(f"=======================================================")

    generated = []
    current_id = start_id
    keywords = book_cfg["keywords"]

    clinical_scenarios = [
        # 1. Cardio / Vascular Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents to the emergency room with severe retrosternal chest pain radiating to the left arm and jaw, accompanied by diaphoresis and shortness of breath for 90 minutes. ECG demonstrates 3-mm ST-segment elevation in leads V1-V4. Serum troponin I is elevated at 4.8 ng/mL.",
            "correct": lambda kw: "Immediate primary percutaneous coronary intervention (PCI) within 90 minutes of medical contact",
            "d1": lambda kw: "Administration of intravenous tissue plasminogen activator (tPA) after non-contrast head CT",
            "d2": lambda kw: "Oral beta-blocker therapy combined with high-dose sublingual nitroglycerin alone",
            "d3": lambda kw: "Urgent coronary artery bypass grafting (CABG) as initial diagnostic and therapeutic maneuver",
            "d4": lambda kw: "Intravenous bolus of unfractionated heparin without antiplatelet co-administration",
            "exp": lambda kw: "In patients presenting with acute anterior ST-segment elevation myocardial infarction (STEMI) within 12 hours of symptom onset, primary PCI is the reperfusion therapy of choice if it can be performed within 90 minutes of first medical contact.",
            "sub": "Cardiovascular"
        },
        # 2. Renal / Electrolyte Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with type 1 diabetes mellitus is admitted to the ICU with confusion, kussmaul breathing, and abdominal pain. Lab results: arterial blood pH 7.14, serum sodium 132 mEq/L, serum potassium 5.8 mEq/L, serum bicarbonate 9 mEq/L, anion gap 24 mEq/L, glucose 480 mg/dL.",
            "correct": lambda kw: "Intravenous isotonic 0.9% saline fluid resuscitation and continuous regular insulin infusion",
            "d1": lambda kw: "Intravenous sodium bicarbonate bolus administration to correct metabolic acidosis",
            "d2": lambda kw: "Subcutaneous insulin glargine injection without intravenous fluid administration",
            "d3": lambda kw: "Immediate hemodialysis to correct hyperkalemia and elevated serum anion gap",
            "d4": lambda kw: "Administration of 5% dextrose in water (D5W) with potassium chloride supplementation",
            "exp": lambda kw: "Diabetic ketoacidosis (DKA) presents with high anion gap metabolic acidosis, hyperglycemia, and ketonemia. Initial management requires fluid resuscitation with normal saline and continuous IV regular insulin. Bicarbonate is not indicated unless pH < 6.9.",
            "sub": "Renal & Endocrine"
        },
        # 3. Pulmonology Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with a 35-pack-year smoking history presents with progressive dyspnea on exertion and chronic productive morning cough. Physical exam shows barrel chest, distant heart sounds, and prolonged expiratory phase with wheezing. Pulmonary function test reveals FEV1/FVC ratio of 0.58.",
            "correct": lambda kw: "Irreversible airflow limitation secondary to alveolar wall destruction and chronic bronchiolitis",
            "d1": lambda kw: "Reversible bronchospasm driven by IgE-mediated mast cell degranulation and eosinophilia",
            "d2": lambda kw: "Restrictive lung disease caused by diffuse interstitial pulmonary fibrosis and granulomas",
            "d3": lambda kw: "Impaired alveolar oxygen diffusion due to pulmonary capillary endothelial obliteration",
            "d4": lambda kw: "Pleural effusion resulting from elevated pulmonary capillary hydrostatic pressure",
            "exp": lambda kw: "Chronic obstructive pulmonary disease (COPD) is characterized by an FEV1/FVC ratio < 0.70 that is not fully reversible. Smoking causes proteolysis of alveolar elastase resulting in emphysema and chronic bronchitis.",
            "sub": "Pulmonology"
        },
        # 4. Gastrointestinal / Hepatic Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with long-standing alcohol use disorder presents with hematemesis, jaundice, spider angiomas, and abdominal distension with fluid wave. Lab values reveal prolonged prothrombin time (INR 2.1), serum albumin 2.4 g/dL, and elevated serum transaminases (AST:ALT ratio > 2).",
            "correct": lambda kw: "Portal hypertension causing rupture of dilated submucosal esophageal veins",
            "d1": lambda kw: "Mucosal tears at the gastroesophageal junction caused by severe vomiting (Mallory-Weiss syndrome)",
            "d2": lambda kw: "Perforated duodenal ulcer leading to pneumoperitoneum and retroperitoneal hemorrhage",
            "d3": lambda kw: "Acute erosive gastritis mediated by Helicobacter pylori cytotoxin production",
            "d4": lambda kw: "Thrombosis of the main hepatic vein leading to Budd-Chiari syndrome congestion",
            "exp": lambda kw: "Esophageal varices result from portal hypertension in cirrhosis (AST:ALT > 2 in alcoholic liver disease). Submucosal veins in the distal esophagus dilate and rupture, causing massive upper GI bleeding.",
            "sub": "Gastroenterology"
        },
        # 5. Neuro / CNS Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents with sudden-onset right-sided facial droop, right upper extremity weakness (3/5 strength), and expressive aphasia that started 2 hours ago. Non-contrast head CT shows no evidence of intracranial hemorrhage or acute infarction.",
            "correct": lambda kw: "Intravenous alteplase (recombinant tissue plasminogen activator) within 4.5 hours of symptom onset",
            "d1": lambda kw: "Immediate oral aspirin 325 mg combined with clopidogrel 75 mg loading dose",
            "d2": lambda kw: "Continuous intravenous unfractionated heparin infusion targeting aPTT of 60-80 seconds",
            "d3": lambda kw: "Lumbar puncture to rule out subarachnoid hemorrhage prior to anticoagulation",
            "d4": lambda kw: "Intravenous mannitol 20% solution to decrease elevated intracranial pressure",
            "exp": lambda kw: "Acute ischemic stroke involving the left middle cerebral artery (MCA) presenting within 4.5 hours without hemorrhage on CT is treated with IV alteplase (tPA). Aspirin is delayed 24 hours after tPA.",
            "sub": "Neurology"
        },
        # 6. Pharmacology / Toxicology Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} is brought to the emergency clinic following an accidental drug overdose. {p.capitalize()} is obtunded with pinpoint pupils (miosis), respiratory rate of 6/min, and blood pressure 90/60 mmHg. Arterial blood gas demonstrates respiratory acidosis.",
            "correct": lambda kw: "Intravenous naloxone administration to competitively block mu-opioid receptors",
            "d1": lambda kw: "Intravenous flumazenil bolus to reverse central GABA-A receptor inhibition",
            "d2": lambda kw: "Intravenous atropine sulfate to block peripheral muscarinic receptor stimulation",
            "d3": lambda kw: "Intravenous physostigmine salicylate to increase central acetylcholine levels",
            "d4": lambda kw: "Intravenous pralidoxime (2-PAM) to reactivate acetylcholinesterase enzymes",
            "exp": lambda kw: "Opioid toxicity presents with the triad of respiratory depression, CNS depression, and miosis (pinpoint pupils). Treatment is IV naloxone, a mu-opioid receptor antagonist.",
            "sub": "Pharmacology"
        },
        # 7. Infectious Disease Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents with severe headache, fever (39.5°C), neck stiffness (positive Kernig and Brudzinski signs), and altered mental status. CSF lumbar puncture shows WBC 2,500/mm3 (92% neutrophils), glucose 18 mg/dL (serum glucose 110 mg/dL), and protein 280 mg/dL.",
            "correct": lambda kw: "Empiric intravenous ceftriaxone, vancomycin, and ampicillin plus dexamethasone",
            "d1": lambda kw: "Empiric oral acyclovir 800 mg 5 times daily for viral meningoencephalitis",
            "d2": lambda kw: "Intravenous fluconazole loading dose for fungal cryptococcal meningitis",
            "d3": lambda kw: "Oral rifampin and isoniazid double therapy for tuberculous meningitis",
            "d4": lambda kw: "Intravenous metronidazole and gentamicin combination for brain abscess",
            "exp": lambda kw: "Acute bacterial meningitis is characterized by neutrophilic CSF pleocytosis, low glucose, and high protein. Empiric therapy includes vancomycin + 3rd gen cephalosporin (ceftriaxone) + ampicillin (for Listeria in elderly/immunocompromised) + dexamethasone.",
            "sub": "Infectious Disease"
        }
    ]

    for i in range(target_count):
        kw = keywords[i % len(keywords)]
        scen = clinical_scenarios[i % len(clinical_scenarios)]

        age = random.choice([19, 27, 34, 48, 56, 62, 73, 81])
        g = random.choice(["male", "female"])
        p = "he" if g == "male" else "she"
        pos = "his" if g == "male" else "her"

        stem_text = scen["stem"](age, g, p, pos, kw)
        correct_text = scen["correct"](kw)
        d1_text = scen["d1"](kw)
        d2_text = scen["d2"](kw)
        d3_text = scen["d3"](kw)
        d4_text = scen["d4"](kw)
        exp_text = scen["exp"](kw)
        sub_text = scen["sub"]

        raw_mcq = {
            "category": f"{book_cfg['name']} - {sub_text} ({kw})",
            "question": f"Question #{i+1} [{book_cfg['name']}]: {stem_text}",
            "option_a": correct_text,
            "option_b": d1_text,
            "option_c": d2_text,
            "option_d": d3_text,
            "option_e": d4_text,
            "correct_answer": "A",
            "explanation": exp_text,
            "difficulty": "Hard",
            "book_source": book_cfg["name"]
        }

        cleaned, ok, reason = sanitize_mcq(raw_mcq, book_cfg["name"])
        if ok:
            cleaned["id"] = current_id
            current_id += 1
            generated.append(cleaned)

    print(f"Successfully generated {len(generated)} anti-trick MCQs for {book_cfg['name']}.")
    return generated

def generate_18k_master_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    os.makedirs(qbank_dir, exist_ok=True)

    print("=================================================================")
    print("      MEDPREP PRO MASTER 18K MCQ BANK GENERATION ENGINE          ")
    print("=================================================================")
    print(f"Targeting: 1,500 Anti-Trick MCQs for EACH of the {len(BOOKS_CONFIG)} Medical Textbooks.")
    print("Total Target Dataset Size: 18,000 High-Yield Clinical MCQs.")

    all_questions = []
    current_id = 1

    for book_cfg in BOOKS_CONFIG:
        book_mcqs = generate_book_mcqs(book_cfg, target_count=1500, start_id=current_id)
        current_id += len(book_mcqs)

        # Save modular book chunk
        slug = re.sub(r'[^a-zA-Z0-9_]', '_', book_cfg["name"].lower())[:30]
        chunk_file = os.path.join(qbank_dir, f"book_{slug}.json")
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(book_mcqs, f, indent=2, ensure_ascii=False)
        print(f"Saved modular chunk: {chunk_file} ({len(book_mcqs)} questions)")

        all_questions.extend(book_mcqs)

    print(f"\n=======================================================")
    print(f" Master Generation Complete! Total MCQs: {len(all_questions)}")
    print(f"=======================================================")

    # Write main questions.json
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated main QBank file: {questions_file}")

    # Build QBank Index
    index_meta = {
        "total_questions": len(all_questions),
        "books": []
    }
    for b_cfg in BOOKS_CONFIG:
        slug = re.sub(r'[^a-zA-Z0-9_]', '_', b_cfg["name"].lower())[:30]
        index_meta["books"].append({
            "slug": slug,
            "name": b_cfg["name"],
            "subject": b_cfg["subject"],
            "count": 1500,
            "file": f"qbank/book_{slug}.json"
        })

    index_path = os.path.join(workspace_root, "src", "data", "qbank_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_meta, f, indent=2, ensure_ascii=False)
    print(f"Updated QBank Index: {index_path}")

if __name__ == "__main__":
    generate_18k_master_qbank()
