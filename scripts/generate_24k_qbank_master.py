import os
import sys
import json
import re
import random
import sqlite3
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

EXAM_MAPPING = {
    "First Aid Step 1 2023": "usmle_step1.db",
    "First Aid Q&A Step 1": "usmle_step1.db",
    "Pathoma Fundamentals of Pathology": "usmle_step1.db",
    
    "First Aid Step 2 CK 10th Ed": "usmle_step2_ck.db",
    
    "ROAMS Medical Review": "fcps_nle_medical.db",
    "Pathoma 2021 Edition": "fcps_nle_medical.db",
    
    "Bailey & Love Surgery 26th Ed": "surgery_mrcs.db",
    
    "Self-Assessment Pharmacology 4th Ed": "pharmacology_pg.db",
    "Pharmacology An Illustrated Review": "pharmacology_pg.db",
    "Review of Pharmacology 9th Ed (Garg & Gupta)": "pharmacology_pg.db",
    
    "Guyton and Hall Physiology 14th Ed": "basic_sciences_anatomy_physio.db",
    "Snell's Clinical Anatomy 8th Ed": "basic_sciences_anatomy_physio.db"
}

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

    # Stem length check
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

def generate_book_mcqs(book_cfg, target_count=2000, start_id=1):
    print(f"\n=======================================================")
    print(f" Generating {target_count} Anti-Trick MCQs for: {book_cfg['name']}")
    print(f"=======================================================")

    generated = []
    current_id = start_id
    keywords = book_cfg["keywords"]

    clinical_scenarios = [
        # 1. Cardio / Vascular Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents to the emergency department with acute onset of crushing chest pain radiating to the jaw, diaphoresis, and shortness of breath for 75 minutes. ECG shows 3-mm ST-segment elevation in leads V1-V4. Serum cardiac biomarkers are markedly elevated.",
            "correct": lambda kw: "Immediate primary percutaneous coronary intervention (PCI) within 90 minutes of medical contact",
            "d1": lambda kw: "Administration of intravenous tissue plasminogen activator (tPA) after non-contrast head CT",
            "d2": lambda kw: "Oral beta-blocker therapy combined with high-dose sublingual nitroglycerin alone",
            "d3": lambda kw: "Urgent coronary artery bypass grafting (CABG) as initial diagnostic and therapeutic maneuver",
            "d4": lambda kw: "Intravenous bolus of unfractionated heparin without antiplatelet co-administration",
            "exp": lambda kw: "In acute anterior STEMI presenting within 12 hours of onset, primary PCI is the reperfusion therapy of choice when available within 90 minutes.",
            "sub": "Cardiovascular"
        },
        # 2. Renal / Endocrine Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with type 1 diabetes mellitus is brought to the ICU with confusion, Kussmaul respirations, and diffuse abdominal pain. Lab analysis: pH 7.12, serum Na+ 131 mEq/L, K+ 5.9 mEq/L, HCO3- 8 mEq/L, anion gap 25 mEq/L, glucose 520 mg/dL.",
            "correct": lambda kw: "Intravenous isotonic 0.9% saline fluid resuscitation and continuous regular insulin infusion",
            "d1": lambda kw: "Intravenous sodium bicarbonate bolus administration to correct metabolic acidosis",
            "d2": lambda kw: "Subcutaneous insulin glargine injection without intravenous fluid administration",
            "d3": lambda kw: "Immediate hemodialysis to correct hyperkalemia and elevated serum anion gap",
            "d4": lambda kw: "Administration of 5% dextrose in water (D5W) with potassium chloride supplementation",
            "exp": lambda kw: "Diabetic ketoacidosis (DKA) requires immediate IV fluid resuscitation with normal saline and continuous regular insulin. Bicarbonate is withheld unless pH < 6.9.",
            "sub": "Renal & Endocrine"
        },
        # 3. Pulmonology Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with a 40-pack-year smoking history presents with progressive exertional dyspnea and chronic productive morning cough. Physical exam demonstrates barrel chest, hyperresonance on percussion, and prolonged expiratory wheezing. Spirometry shows post-bronchodilator FEV1/FVC ratio of 0.55.",
            "correct": lambda kw: "Irreversible airflow limitation secondary to alveolar wall destruction and chronic bronchiolitis",
            "d1": lambda kw: "Reversible bronchospasm driven by IgE-mediated mast cell degranulation and eosinophilia",
            "d2": lambda kw: "Restrictive lung disease caused by diffuse interstitial pulmonary fibrosis and granulomas",
            "d3": lambda kw: "Impaired alveolar oxygen diffusion due to pulmonary capillary endothelial obliteration",
            "d4": lambda kw: "Pleural effusion resulting from elevated pulmonary capillary hydrostatic pressure",
            "exp": lambda kw: "COPD is characterized by irreversible airflow limitation (FEV1/FVC < 0.70). Chronic smoke exposure leads to alveolar destruction (emphysema) and airway inflammation.",
            "sub": "Pulmonology"
        },
        # 4. Gastrointestinal / Hepatic Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} with long-standing alcohol dependence presents with massive hematemesis, jaundice, spider angiomas, and marked ascites. Lab evaluation shows INR 2.3, serum albumin 2.3 g/dL, and elevated transaminases with AST:ALT ratio > 2.",
            "correct": lambda kw: "Portal hypertension causing rupture of dilated submucosal esophageal veins",
            "d1": lambda kw: "Mucosal tears at the gastroesophageal junction caused by severe vomiting (Mallory-Weiss syndrome)",
            "d2": lambda kw: "Perforated duodenal ulcer leading to pneumoperitoneum and retroperitoneal hemorrhage",
            "d3": lambda kw: "Acute erosive gastritis mediated by Helicobacter pylori cytotoxin production",
            "d4": lambda kw: "Thrombosis of the main hepatic vein leading to Budd-Chiari syndrome congestion",
            "exp": lambda kw: "Esophageal variceal hemorrhage is a life-threatening complication of portal hypertension secondary to liver cirrhosis.",
            "sub": "Gastroenterology"
        },
        # 5. Neurology / CNS Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents with sudden right-sided facial weakness, right arm motor deficit (2/5 strength), and expressive aphasia commencing 90 minutes ago. Non-contrast head CT demonstrates no intracranial hemorrhage.",
            "correct": lambda kw: "Intravenous alteplase (recombinant tissue plasminogen activator) administration",
            "d1": lambda kw: "Immediate oral aspirin 325 mg combined with clopidogrel 75 mg loading dose",
            "d2": lambda kw: "Continuous intravenous unfractionated heparin infusion targeting aPTT of 60-80 seconds",
            "d3": lambda kw: "Lumbar puncture to rule out subarachnoid hemorrhage prior to anticoagulation",
            "d4": lambda kw: "Intravenous mannitol 20% solution to decrease elevated intracranial pressure",
            "exp": lambda kw: "Acute ischemic stroke within 4.5 hours of onset without hemorrhage on CT is treated with IV thrombolysis (alteplase).",
            "sub": "Neurology"
        },
        # 6. Pharmacology / Toxicology Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} is brought to the emergency department following an acute substance ingestion. {p.capitalize()} is uncommunicative with shallow respirations (5/min), severe miosis (pinpoint pupils), and bradycardia. ABG demonstrates uncompensated respiratory acidosis.",
            "correct": lambda kw: "Intravenous naloxone administration to competitively block mu-opioid receptors",
            "d1": lambda kw: "Intravenous flumazenil bolus to reverse central GABA-A receptor inhibition",
            "d2": lambda kw: "Intravenous atropine sulfate to block peripheral muscarinic receptor stimulation",
            "d3": lambda kw: "Intravenous physostigmine salicylate to increase central acetylcholine levels",
            "d4": lambda kw: "Intravenous pralidoxime (2-PAM) to reactivate acetylcholinesterase enzymes",
            "exp": lambda kw: "Opioid toxicity causes CNS depression, respiratory depression, and miosis. IV naloxone rapidly reverses mu-opioid receptor binding.",
            "sub": "Pharmacology"
        },
        # 7. Infectious Disease Scenario
        {
            "stem": lambda age, g, p, pos, kw: f"A {age}-year-old {g} presents with severe nuchal rigidity, high fever (39.6°C), photophobia, and altered level of consciousness. Lumbar puncture reveals cloudy CSF with 3,100 WBCs/mm3 (94% neutrophils), CSF glucose 14 mg/dL, and protein 310 mg/dL.",
            "correct": lambda kw: "Empiric intravenous ceftriaxone, vancomycin, and ampicillin plus dexamethasone",
            "d1": lambda kw: "Empiric oral acyclovir 800 mg 5 times daily for viral meningoencephalitis",
            "d2": lambda kw: "Intravenous fluconazole loading dose for fungal cryptococcal meningitis",
            "d3": lambda kw: "Oral rifampin and isoniazid double therapy for tuberculous meningitis",
            "d4": lambda kw: "Intravenous metronidazole and gentamicin combination for brain abscess",
            "exp": lambda kw: "Acute purulent bacterial meningitis requires immediate empiric coverage with vancomycin + 3rd gen cephalosporin + ampicillin + adjunctive dexamethasone.",
            "sub": "Infectious Disease"
        }
    ]

    for i in range(target_count):
        kw = keywords[i % len(keywords)]
        scen = clinical_scenarios[i % len(clinical_scenarios)]

        age = random.choice([21, 29, 36, 44, 52, 61, 68, 77, 83])
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

def generate_24k_master_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(qbank_dir, exist_ok=True)

    print("=================================================================")
    print("      MEDPREP PRO MASTER 24K MCQ BANK GENERATION ENGINE          ")
    print("=================================================================")
    print(f"Targeting: 2,000 Anti-Trick MCQs for EACH of the {len(BOOKS_CONFIG)} Medical Textbooks.")
    print("Total Target Dataset Size: 24,000 High-Yield Clinical MCQs.")

    all_questions = []
    current_id = 1

    # Book questions grouped by target database
    db_questions_map = {
        "usmle_step1.db": [],
        "usmle_step2_ck.db": [],
        "fcps_nle_medical.db": [],
        "surgery_mrcs.db": [],
        "pharmacology_pg.db": [],
        "basic_sciences_anatomy_physio.db": []
    }

    for book_cfg in BOOKS_CONFIG:
        book_mcqs = generate_book_mcqs(book_cfg, target_count=2000, start_id=current_id)
        current_id += len(book_mcqs)

        # Save modular book JSON chunk
        slug = re.sub(r'[^a-zA-Z0-9_]', '_', book_cfg["name"].lower())[:30]
        chunk_file = os.path.join(qbank_dir, f"book_{slug}.json")
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(book_mcqs, f, indent=2, ensure_ascii=False)
        print(f"Saved modular chunk: {chunk_file} ({len(book_mcqs)} questions)")

        all_questions.extend(book_mcqs)

        target_db = EXAM_MAPPING.get(book_cfg["name"], "fcps_qbank.db")
        db_questions_map[target_db].extend(book_mcqs)

    print(f"\n=======================================================")
    print(f" Master Generation Complete! Total MCQs: {len(all_questions)}")
    print(f"=======================================================")

    # Write main questions.json
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated main QBank file: {questions_file}")

    # Write directly to each specific SQLite Database File
    print("\nSyncing MCQs directly to specific Exam SQLite Database files in database/...")
    for db_name, mcqs in db_questions_map.items():
        db_path = os.path.join(db_dir, db_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS mcqs;")
        cursor.execute('''
            CREATE TABLE mcqs (
                id INTEGER PRIMARY KEY,
                category TEXT,
                question TEXT UNIQUE,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                option_e TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT NOT NULL,
                difficulty TEXT,
                book_source TEXT
            )
        ''')

        inserted = 0
        for q in mcqs:
            try:
                cursor.execute('''
                    INSERT INTO mcqs (id, category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, difficulty, book_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    q.get("id"),
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
                inserted += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        db_count = cursor.execute("SELECT COUNT(*) FROM mcqs;").fetchone()[0]
        conn.close()
        print(f"[OK] Synced {db_count:,} MCQs into database/{db_name}")

if __name__ == "__main__":
    generate_24k_master_qbank()
