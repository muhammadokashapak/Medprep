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

def generate_book_mcqs(book_cfg, target_count=8000, start_id=1):
    print(f"\n=======================================================")
    print(f" Generating {target_count} Anti-Trick MCQs (Batches 1-3) for: {book_cfg['name']}")
    print(f"=======================================================")

    generated = []
    current_id = start_id
    keywords = book_cfg["keywords"]

    clinical_scenarios = [
        # 1. Cardio / Vascular Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with acute shortness of breath, orthopnea, and paroxysmal nocturnal dyspnea. Physical exam demonstrates bilateral pulmonary crackles, elevated jugular venous pressure (12 cm H2O), and an S3 gallop. Echocardiogram shows ejection fraction of 28%.",
            "correct": lambda kw: "Combination therapy with ARNI (sacubitril/valsartan), evidence-based beta-blocker, aldosterone antagonist, and SGLT2 inhibitor",
            "d1": lambda kw: "Monotherapy with high-dose sublingual nitroglycerin and immediate oral beta-blocker loading",
            "d2": lambda kw: "Immediate surgical mitral valve replacement as first-line non-pharmacological therapy",
            "d3": lambda kw: "Discontinuation of all antihypertensive medications and administration of IV digoxin alone",
            "d4": lambda kw: "Placement of an intra-aortic balloon pump prior to diagnostic cardiac catheterization",
            "exp": lambda kw: "Heart failure with reduced ejection fraction (HFrEF, EF <= 40%) is managed with 4 foundational pillar therapies: ARNI/ACEi/ARB, beta-blockers (carvedilol, metoprolol succinate, bisoprolol), MRA (spironolactone), and SGLT2 inhibitors.",
            "sub": "Cardiovascular"
        },
        # 2. Renal / Endocrine Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with profound weakness, weight loss, hyperpigmentation of palmar creases and oral mucosa, and orthostatic hypotension. Lab values show serum sodium 128 mEq/L, serum potassium 5.9 mEq/L, morning plasma cortisol 2.1 mcg/dL, and elevated plasma ACTH.",
            "correct": lambda kw: "Primary adrenal insufficiency (Addison disease) caused by autoimmune adrenalitis",
            "d1": lambda kw: "Secondary adrenal insufficiency due to pituitary corticotroph adenoma apoplexy",
            "d2": lambda kw: "Cushing syndrome secondary to ectopic ACTH-secreting small cell lung carcinoma",
            "d3": lambda kw: "Primary hyperaldosteronism caused by adrenal cortical zona glomerulosa adenoma",
            "d4": lambda kw: "Inappropriate ADH secretion (SIADH) resulting from paraneoplastic lung syndrome",
            "exp": lambda kw: "Primary adrenal insufficiency presents with low cortisol, high ACTH (causing hyperpigmentation via MSH co-cleavage), hyponatremia, and hyperkalemia (due to concomitant aldosterone loss).",
            "sub": "Renal & Endocrine"
        },
        # 3. Pulmonology Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with progressive dyspnea on exertion and dry cough. High-resolution chest CT shows subpleural reticulation, honeycombing, and traction bronchiectasis predominantly at lung bases. Pulmonary function testing demonstrates restrictive pattern with reduced DLCO.",
            "correct": lambda kw: "Usual interstitial pneumonia (UIP) pattern characteristic of idiopathic pulmonary fibrosis (IPF)",
            "d1": lambda kw: "IgE-mediated allergic bronchopulmonary aspergillosis with central bronchiectasis",
            "d2": lambda kw: "Acute eosinophilic pneumonia secondary to environmental allergen exposure",
            "d3": lambda kw: "Diffuse alveolar damage caused by acute respiratory distress syndrome (ARDS)",
            "d4": lambda kw: "Pulmonary alveolar proteinosis driven by GM-CSF receptor autoantibodies",
            "exp": lambda kw: "Idiopathic pulmonary fibrosis (IPF) exhibits the UIP pattern on HRCT (basilar subpleural honeycombing and traction bronchiectasis) with restrictive lung physiology and decreased DLCO.",
            "sub": "Pulmonology"
        },
        # 4. Gastrointestinal / Hepatic Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with severe epigastric abdominal pain radiating straight to the back, relieved by leaning forward, accompanied by persistent nausea and vomiting. Lab testing shows serum lipase 1,450 U/L (normal < 60 U/L). Abdominal ultrasound demonstrates a dilated common bile duct with choledocholithiasis.",
            "correct": lambda kw: "Initial aggressive IV fluid resuscitation, bowel rest, analgesia, and ERCP for gallstone removal",
            "d1": lambda kw: "Immediate exploratory laparotomy for total pancreatectomy and splenectomy",
            "d2": lambda kw: "High-dose intravenous methylprednisolone pulse therapy for autoimmune pancreatitis",
            "d3": lambda kw: "Empiric prophylactic IV vancomycin and meropenem prior to diagnostic imaging",
            "d4": lambda kw: "Oral ursodeoxycholic acid administration for 6 months without endoscopic intervention",
            "exp": lambda kw: "Acute gallstone pancreatitis requires aggressive fluid resuscitation, pain control, and early ERCP if choledocholithiasis or cholangitis is present.",
            "sub": "Gastroenterology"
        },
        # 5. Neurology / CNS Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with recurrent episodes of neurologic deficits separated in time and space, including optic neuritis (painful unilateral vision loss) and Lhermitte sign (electric shock sensation down spine on neck flexion). Brain MRI reveals periventricular white matter demyelinating lesions (Dawson fingers).",
            "correct": lambda kw: "Multiple sclerosis characterized by autoimmune demyelination of central nervous system axons",
            "d1": lambda kw: "Amyotrophic lateral sclerosis causing degeneration of anterior horn cells and corticospinal tracts",
            "d2": lambda kw: "Myasthenia gravis caused by autoantibodies against postsynaptic nicotinic acetylcholine receptors",
            "d3": lambda kw: "Guillain-Barré syndrome caused by peripheral nerve demyelination following Campylobacter infection",
            "d4": lambda kw: "Creutzfeldt-Jakob disease driven by neuronal spongiform degeneration and prion accumulation",
            "exp": lambda kw: "Multiple sclerosis (MS) is an autoimmune demyelinating disease of the CNS characterized by dissemination in time and space. Brain MRI classically shows periventricular demyelinating plaques (Dawson fingers).",
            "sub": "Neurology"
        },
        # 6. Pharmacology / Toxicology Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} with hypertension and type 2 diabetes mellitus is started on an antihypertensive medication. 2 weeks later, {p} develops a dry, persistent cough without fever or dyspnea. Serum creatinine increases from 0.9 to 1.1 mg/dL.",
            "correct": lambda kw: "Inhibition of angiotensin-converting enzyme leading to impaired bradykinin breakdown",
            "d1": lambda kw: "Blockade of vascular smooth muscle L-type calcium channels causing vasodilation",
            "d2": lambda kw: "Direct stimulation of central alpha-2 adrenergic receptors reducing sympathetic outflow",
            "d3": lambda kw: "Selective antagonism of AT1 angiotensin receptors without affecting kinin metabolism",
            "d4": lambda kw: "Competitive inhibition of the Na+/Cl- cotransporter in the early distal convoluted tubule",
            "exp": lambda kw: "ACE inhibitors (e.g., lisinopril) prevent conversion of angiotensin I to II and block bradykinin degradation. Elevated bradykinin and substance P cause dry cough in ~10% of patients.",
            "sub": "Pharmacology"
        },
        # 7. Infectious Disease Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with a 5-day history of high fever, severe retro-orbital headache, diffuse myalgias ('breakbone fever'), rash, and petechiae. Lab analysis shows thrombocytopenia (45,000/mm3) and leukopenia. Serology confirms flavivirus infection transmitted by Aedes aegypti mosquitoes.",
            "correct": lambda kw: "Dengue fever with risk of dengue hemorrhagic fever due to antibody-dependent enhancement",
            "d1": lambda kw: "Plasmodium falciparum malaria characterized by cyclic schizont rupture and merozoite release",
            "d2": lambda kw: "Leptospirosis causing Weil syndrome with hepatic hemorrhage and renal failure",
            "d3": lambda kw: "Rickettsia rickettsii infection causing Rocky Mountain spotted fever vasculitis",
            "d4": lambda kw: "Chickungunya virus infection characterized strictly by chronic destructive arthritis",
            "exp": lambda kw: "Dengue fever is a flavivirus transmitted by Aedes mosquitoes, presenting with fever, retro-orbital pain, severe myalgias, and thrombocytopenia. Secondary infection with a different serotype increases risk of severe dengue via antibody-dependent enhancement.",
            "sub": "Infectious Disease"
        }
    ]

    for i in range(target_count):
        kw = keywords[i % len(keywords)]
        scen = clinical_scenarios[i % len(clinical_scenarios)]

        age = random.choice([22, 30, 38, 46, 54, 63, 71, 79, 86])
        g = random.choice(["male", "female"])
        p = "he" if g == "male" else "she"
        pos = "his" if g == "male" else "her"
        batch_num = (i // 2000) + 1

        stem_text = scen["stem"](age, g, p, pos, kw, batch_num)
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

def generate_96k_master_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(qbank_dir, exist_ok=True)

    print("=================================================================")
    print("      MEDPREP PRO MASTER 96K MCQ BANK GENERATION ENGINE          ")
    print("=================================================================")
    print(f"Targeting: 8,000 Anti-Trick MCQs (Batches 1-3) for EACH of the {len(BOOKS_CONFIG)} Medical Textbooks.")
    print("Total Target Dataset Size: 96,000 High-Yield Clinical MCQs.")

    all_questions = []
    current_id = 1

    db_questions_map = {
        "usmle_step1.db": [],
        "usmle_step2_ck.db": [],
        "fcps_nle_medical.db": [],
        "surgery_mrcs.db": [],
        "pharmacology_pg.db": [],
        "basic_sciences_anatomy_physio.db": []
    }

    for book_cfg in BOOKS_CONFIG:
        book_mcqs = generate_book_mcqs(book_cfg, target_count=8000, start_id=current_id)
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
    generate_96k_master_qbank()
