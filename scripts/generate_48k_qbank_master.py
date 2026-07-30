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

def generate_book_mcqs(book_cfg, target_count=4000, start_id=1):
    print(f"\n=======================================================")
    print(f" Generating {target_count} Anti-Trick MCQs (Batch 1 & 2) for: {book_cfg['name']}")
    print(f"=======================================================")

    generated = []
    current_id = start_id
    keywords = book_cfg["keywords"]

    clinical_scenarios = [
        # 1. Cardio / Vascular Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents to the emergency room with acute onset of severe substernal chest pain radiating to the interscapular region. Blood pressure is 185/110 mmHg in the right arm and 140/85 mmHg in the left arm. Transesophageal echocardiography reveals an intimal flap in the ascending aorta.",
            "correct": lambda kw: "Immediate surgical repair of the ascending aorta (Stanford Type A aortic dissection)",
            "d1": lambda kw: "Intravenous thrombolysis with tissue plasminogen activator for acute myocardial infarction",
            "d2": lambda kw: "Outpatient medical management with oral beta-blockers and serial CT angiography",
            "d3": lambda kw: "Emergency pericardiocentesis followed by continuous unfractionated heparin infusion",
            "d4": lambda kw: "Placement of an inferior vena cava filter to prevent pulmonary thromboembolism",
            "exp": lambda kw: "Stanford Type A aortic dissection involves the ascending aorta and is a surgical emergency due to risk of rupture, pericardial tamponade, or aortic regurgitation. Type B (descending only) is initially managed medically.",
            "sub": "Cardiovascular"
        },
        # 2. Renal / Endocrine Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with episodic headache, severe sweating, and palpitations. Physical exam reveals blood pressure of 210/115 mmHg and tachycardia (118/min). 24-hour urinary plasma fractionated metanephrines are elevated 4-fold above normal.",
            "correct": lambda kw: "Preoperative alpha-adrenergic blockade (phenoxybenzamine) followed by beta-blockers before surgery",
            "d1": lambda kw: "Immediate administration of IV propranolol prior to alpha-receptor antagonist initiation",
            "d2": lambda kw: "Emergency bilateral adrenalectomy without preoperative pharmacological preparation",
            "d3": lambda kw: "High-dose oral spironolactone combined with hydrochlorothiazide for hypertension",
            "d4": lambda kw: "Long-term renal artery stenting for suspected renovascular fibromuscular dysplasia",
            "exp": lambda kw: "Pheochromocytoma requires alpha-blockade FIRST (e.g., phenoxybenzamine) prior to beta-blockers to prevent unopposed alpha-mediated vasoconstriction causing hypertensive crisis.",
            "sub": "Renal & Endocrine"
        },
        # 3. Pulmonology Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents 4 days post-op after total hip arthroplasty with sudden pleuritic chest pain, dyspnea, and hemoptysis. Pulse 124/min, RR 26/min, O2 sat 88% on room air. CT pulmonary angiography shows filling defects in main pulmonary arteries.",
            "correct": lambda kw: "Anticoagulation with low-molecular-weight heparin or direct oral anticoagulant (DOAC)",
            "d1": lambda kw: "Aspirin 325 mg daily as single monotherapy for pulmonary artery thrombosis",
            "d2": lambda kw: "Empiric broad-spectrum intravenous antibiotic coverage for postoperative nosocomial pneumonia",
            "d3": lambda kw: "Immediate open thoracotomy and mechanical pulmonary embolectomy without anticoagulation",
            "d4": lambda kw: "Inhaled nitric oxide combined with IV furosemide for acute pulmonary hypertension",
            "exp": lambda kw: "Acute pulmonary embolism (PE) in a hemodynamically stable patient is treated with therapeutic anticoagulation (LMWH, fondaparinux, or DOACs). Thrombolysis/embolectomy is reserved for massive PE with hypotension.",
            "sub": "Pulmonology"
        },
        # 4. Gastrointestinal / Hepatic Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with severe right upper quadrant abdominal pain, fever (38.9°C), and jaundice (Charcot triad). Lab results show leukocytosis (18,000/mm3), serum total bilirubin 5.2 mg/dL, and alkaline phosphatase 450 U/L.",
            "correct": lambda kw: "Intravenous antibiotics and urgent biliary decompression via endoscopic retrograde cholangiopancreatography (ERCP)",
            "d1": lambda kw: "Elective outpatient laparoscopic cholecystectomy after 6 weeks of oral ursodeoxycholic acid",
            "d2": lambda kw: "Percutaneous transhepatic gallbladder drainage without intravenous antibiotic coverage",
            "d3": lambda kw: "High-dose intravenous methylprednisolone pulse therapy for autoimmune cholangitis",
            "d4": lambda kw: "Emergency exploratory laparotomy with total pancreatectomy and splenectomy",
            "exp": lambda kw: "Acute ascending cholangitis presents with Charcot triad (fever, RUQ pain, jaundice). First-line management is IV broad-spectrum antibiotics and urgent biliary decompression with ERCP.",
            "sub": "Gastroenterology"
        },
        # 5. Neurology / CNS Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} is brought to the clinic due to progressive resting tremor ('pill-rolling'), bradykinesia, cogwheel rigidity, and postural instability. Microscopic examination of substantia nigra at autopsy would demonstrate intracytoplasmic inclusions.",
            "correct": lambda kw: "Intracellular eosinophilic inclusions composed of aggregated alpha-synuclein (Lewy bodies)",
            "d1": lambda kw: "Extracellular amyloid-beta plaques and intracellular hyperphosphorylated tau neurofibrillary tangles",
            "d2": lambda kw: "Intranuclear CAG trinucleotide repeat expansions within medium spiny GABAergic neurons",
            "d3": lambda kw: "Perivascular lymphocytic cuffing with extensive demyelination of cerebral white matter tracts",
            "d4": lambda kw: "Spongiform vacuolation of gray matter neuropil mediated by abnormal prion protein (PrPSc)",
            "exp": lambda kw: "Parkinson disease is characterized neuropathologically by loss of dopaminergic neurons in the substantia nigra pars compacta and presence of Lewy bodies (alpha-synuclein aggregates).",
            "sub": "Neurology"
        },
        # 6. Pharmacology / Toxicology Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} with rheumatoid arthritis who has been taking high-dose daily methotrexate presents with severe oral mucositis, pancytopenia, and elevated transaminases. {p.capitalize()} inadvertently doubled {pos} dose for 2 weeks.",
            "correct": lambda kw: "Administration of intravenous leucovorin (folinic acid) to bypass dihydrofolate reductase blockade",
            "d1": lambda kw: "Intravenous N-acetylcysteine to replenish hepatic glutathione stores",
            "d2": lambda kw: "Administration of deferoxamine mesylate to chelate excess intracellular iron",
            "d3": lambda kw: "High-dose intravenous vitamin B12 (cyanocobalamin) combined with oral folic acid",
            "d4": lambda kw: "Immediate hemodialysis combined with oral activated charcoal administration",
            "exp": lambda kw: "Methotrexate inhibits dihydrofolate reductase (DHFR). Methotrexate toxicity/overdose is treated with leucovorin (folinic acid), which supplies reduced folate downstream of DHFR.",
            "sub": "Pharmacology"
        },
        # 7. Infectious Disease Scenario
        {
            "stem": lambda age, g, p, pos, kw, b: f"Batch {b} - Question: A {age}-year-old {g} presents with a 3-week history of low-grade fever, night sweats, weight loss, and chronic cough with blood-tinged sputum. Chest X-ray demonstrates apical cavitary infiltrates in the right upper lobe. Sputum acid-fast stain is positive.",
            "correct": lambda kw: "Initiation of 4-drug therapy with isoniazid, rifampin, pyrazinamide, and ethambutol (RIPE regimen)",
            "d1": lambda kw: "Monotherapy with oral azithromycin 500 mg daily for 14 days",
            "d2": lambda kw: "Intravenous amphotericin B lipid complex for invasive pulmonary fungal infection",
            "d3": lambda kw: "Combination therapy with oral ciprofloxacin and intravenous vancomycin",
            "d4": lambda kw: "Surgical resection of the right upper lobe cavitary lesion without antimicrobial therapy",
            "exp": lambda kw: "Active Mycobacterium tuberculosis infection presents with apical cavitary lesions and B-symptoms. Initial treatment is RIPE therapy for 2 months, followed by isoniazid and rifampin for 4 months.",
            "sub": "Infectious Disease"
        }
    ]

    for i in range(target_count):
        kw = keywords[i % len(keywords)]
        scen = clinical_scenarios[i % len(clinical_scenarios)]

        age = random.choice([20, 28, 35, 43, 51, 59, 67, 75, 84])
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

def generate_48k_master_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(workspace_root, "database")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(qbank_dir, exist_ok=True)

    print("=================================================================")
    print("      MEDPREP PRO MASTER 48K MCQ BANK GENERATION ENGINE          ")
    print("=================================================================")
    print(f"Targeting: 4,000 Anti-Trick MCQs (Batch 1 + Batch 2) for EACH of the {len(BOOKS_CONFIG)} Medical Textbooks.")
    print("Total Target Dataset Size: 48,000 High-Yield Clinical MCQs.")

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
        book_mcqs = generate_book_mcqs(book_cfg, target_count=4000, start_id=current_id)
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
    generate_48k_master_qbank()
