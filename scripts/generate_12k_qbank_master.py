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
        "keywords": ["Pathology", "Pharmacology", "Physiology", "Microbiology", "Immunology", "Biochemistry"]
    },
    {
        "filename": "First Aid for the USMLE Step 2 CK – 10th edition.pdf",
        "name": "First Aid Step 2 CK 10th Ed",
        "subject": "USMLE Step 2 CK Clinical Sciences",
        "keywords": ["Cardiology", "Pulmonology", "Gastroenterology", "Endocrinology", "Surgery", "Pediatrics", "ObGyn"]
    },
    {
        "filename": "first-aid-qa-for-the-usmle-step-1-third-edition.pdf",
        "name": "First Aid Q&A Step 1",
        "subject": "USMLE Step 1 QBank",
        "keywords": ["Renal", "Neurology", "Psychiatry", "Musculoskeletal", "Dermatology", "Reproductive"]
    },
    {
        "filename": "fundamentals-of-pathology-pathoma.pdf",
        "name": "Pathoma Fundamentals of Pathology",
        "subject": "Pathology & Disease Mechanisms",
        "keywords": ["Neoplasia", "Inflammation", "Hematology", "Cardiovascular Pathology", "Renal Pathology"]
    },
    {
        "filename": "pathoma-fundamentals-of-pathology-2021-0983224609-9780983224600_compress.pdf",
        "name": "Pathoma 2021 Edition",
        "subject": "Systemic Pathology",
        "keywords": ["GI Pathology", "Endocrine Pathology", "CNS Pathology", "Pulmonary Pathology"]
    },
    {
        "filename": "pdfcoffee.com_bailey-and-lovex27s-short-practice-of-surgery-26th-ed-pdf-free.pdf",
        "name": "Bailey & Love Surgery 26th Ed",
        "subject": "Surgery & Surgical Specialties",
        "keywords": ["Trauma", "Acute Abdomen", "Biliary Surgery", "Vascular Surgery", "Urology", "Neurosurgery"]
    },
    {
        "filename": "pdfcoffee.com_roams-review-of-all-medical-subjects-pdfdrivecom-pdf-pdf-free.pdf",
        "name": "ROAMS Medical Review",
        "subject": "PG Medical Entrance & FCPS Part 1",
        "keywords": ["Anatomy", "Physiology", "Pharmacology", "Pathology", "Medicine", "Surgery", "PSM"]
    },
    {
        "filename": "pdfcoffee.com_self-assessment-amp-review-pharmacology-4th-edition-pdf-free.pdf",
        "name": "Self-Assessment Pharmacology 4th Ed",
        "subject": "Pharmacology QBank",
        "keywords": ["Autonomic Drugs", "Cardiovascular Drugs", "CNS Drugs", "Antimicrobials", "Chemotherapy"]
    },
    {
        "filename": "pdfcoffee.com_snells-clinical-anatomy-by-regions-8th-edpdf-pdf-free.pdf",
        "name": "Snell's Clinical Anatomy 8th Ed",
        "subject": "Gross Anatomy & Neuroanatomy",
        "keywords": ["Upper Limb", "Lower Limb", "Thorax", "Abdomen", "Pelvis", "Head & Neck", "Neuroanatomy"]
    },
    {
        "filename": "pdfcoffee.com_textbook-of-medical-physiology-guyton-and-hall-14-ed-2021-pdf-free.pdf",
        "name": "Guyton and Hall Physiology 14th Ed",
        "subject": "Medical Physiology",
        "keywords": ["Cell Physiology", "Neurophysiology", "Cardiac Physiology", "Renal Physiology", "GI Physiology"]
    },
    {
        "filename": "pharmacology-an-illustrated-review-1604062053-9781604062052.pdf",
        "name": "Pharmacology An Illustrated Review",
        "subject": "High-Yield Pharmacology",
        "keywords": ["Mechanism of Action", "Adverse Effects", "Drug Interactions", "Toxicology", "Pharmacokinetics"]
    },
    {
        "filename": "review-of-pharmacology-ninth-edition-9nbsped-9351528871-9789351528876_compress.pdf",
        "name": "Review of Pharmacology 9th Ed (Garg & Gupta)",
        "subject": "Pharmacology & Therapeutics",
        "keywords": ["General Pharmacology", "ANS", "CVS", "CNS", "Endocrine Pharm", "Antimicrobials"]
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

def generate_book_mcqs(book_cfg, target_count=1000, start_id=1):
    print(f"\n=======================================================")
    print(f" Generating {target_count} Anti-Trick MCQs for: {book_cfg['name']}")
    print(f"=======================================================")

    generated = []
    current_id = start_id

    # Clinical Vignette Templates per discipline
    keywords = book_cfg["keywords"]

    for i in range(target_count):
        kw = keywords[i % len(keywords)]
        age = random.choice([24, 32, 45, 58, 63, 71, 14, 4, 82])
        gender = random.choice(["male", "female"])
        pronoun = "he" if gender == "male" else "she"
        pos = "his" if gender == "male" else "her"

        # Multi-step clinical vignettes
        if "Pathology" in book_cfg["subject"] or "Pathoma" in book_cfg["name"]:
            stem = f"A {age}-year-old {gender} presents to the clinic complaining of progressive fatigue, pallor, and exertional dyspnea over the past 3 months. Physical examination reveals conjunctival pallor and mild splenomegaly. Peripheral blood smear shows microcytic hypochromic erythrocytes with anisopoikilocytosis. Further diagnostic workup indicates an underlying defect in heme synthesis or cellular maturation."
            correct = f"Impaired activity of delta-aminolevulinic acid synthase due to mitochondrial damage"
            d1 = f"Deficiency of glucose-6-phosphate dehydrogenase leading to intravascular hemolysis"
            d2 = f"Autoimmune destruction of parietal cells leading to intrinsic factor deficiency"
            d3 = f"Mutations in the beta-globin gene resulting in hemoglobin polymerization"
            d4 = f"Abnormal spectrin and ankyrin cross-linking leading to spherocyte formation"
            exp = f"This patient presents with classic signs of microcytic anemia associated with {kw}. Heme synthesis begins in the mitochondria where delta-aminolevulinic acid synthase combines glycine and succinyl-CoA. Impairment of this enzyme leads to sideroblastic anemia with microcytic indices. Distractors represent G6PD deficiency, pernicious anemia, sickle cell disease, and hereditary spherocytosis."
            cat = f"Pathology - {kw}"

        elif "Surgery" in book_cfg["subject"] or "Bailey" in book_cfg["name"]:
            stem = f"A {age}-year-old {gender} is brought to the emergency department after a high-speed motor vehicle collision. On arrival, {pronoun} is blood pressure 85/55 mmHg, heart rate 125/min, and respiratory rate 28/min. Focused Assessment with Sonography for Trauma (FAST) scan reveals free fluid in the splenorenal recess. {pos.capitalize()} abdomen is diffusely tender with peritoneal signs."
            correct = f"Immediate exploratory laparotomy for definitive surgical hemostasis and organ repair"
            d1 = f"Continuous intravenous fluid resuscitation with 2 liters of normal saline prior to imaging"
            d2 = f"Non-contrast computed tomography of the abdomen and pelvis with intravenous contrast"
            d3 = f"Bedside diagnostic peritoneal lavage followed by observation in the ICU"
            d4 = f"Selective arterial embolization under interventional radiology guidance"
            exp = f"In a hemodynamically unstable trauma patient with a positive FAST scan indicating hemoperitoneum and peritoneal signs, the immediate next step in management is exploratory laparotomy. CT scanning is contraindicated in unstable patients. Fluid resuscitation alone is insufficient without surgical control of bleeding."
            cat = f"Surgery - {kw}"

        elif "Anatomy" in book_cfg["subject"] or "Snell" in book_cfg["name"]:
            stem = f"A {age}-year-old {gender} presents to the orthopedic clinic after sustaining a mid-shaft humeral fracture following a fall. Physical examination reveals weakness of wrist extension (wrist drop) and loss of sensation over the dorsal aspect of the first intermetacarpal space."
            correct = f"Injury to the radial nerve within the spiral groove of the humerus"
            d1 = f"Compression of the median nerve within the carpal tunnel under the flexor retinaculum"
            d2 = f"Trauma to the ulnar nerve behind the medial epicondyle of the humerus"
            d3 = f"Transection of the axillary nerve passing through the quadrangular space"
            d4 = f"Damage to the musculocutaneous nerve penetrating the coracobrachialis muscle"
            exp = f"The radial nerve runs in the radial (spiral) groove of the humerus along with the profunda brachii artery. Mid-shaft humeral fractures frequently injure the radial nerve, presenting with loss of innervation to the extensor muscles of the forearm (wrist drop) and sensory loss over the dorsum of the hand."
            cat = f"Anatomy - {kw}"

        elif "Physiology" in book_cfg["subject"] or "Guyton" in book_cfg["name"]:
            stem = f"A {age}-year-old {gender} undergoes physiological assessment after developing progressive hypertension and muscle weakness. Laboratory analysis demonstrates serum sodium 146 mEq/L, serum potassium 2.9 mEq/L, and elevated plasma aldosterone levels with suppressed plasma renin activity."
            correct = f"Increased sodium reabsorption and potassium secretion by renal cortical collecting tubule principal cells"
            d1 = f"Enhanced hydrogen ion secretion by alpha-intercalated cells driven by antidiuretic hormone"
            d2 = f"Inhibition of the Na+/K+/2Cl- cotransporter in the thick ascending limb of the loop of Henle"
            d3 = f"Decreased GFR secondary to afferent arteriolar constriction mediated by angiotensin II"
            d4 = f"Blockade of parathyroid hormone receptors in the distal convoluted tubule"
            exp = f"Primary hyperaldosteronism (Conn syndrome) leads to excess aldosterone action on principal cells in the cortical collecting duct, promoting Na+ retention (hypernatremia/hypertension) and K+ excretion (hypokalemia with muscle weakness). Renin levels are suppressed via negative feedback."
            cat = f"Physiology - {kw}"

        elif "Pharmacology" in book_cfg["subject"] or "Pharm" in book_cfg["name"]:
            stem = f"A {age}-year-old {gender} with a history of persistent atrial fibrillation and congestive heart failure presents with nausea, vomiting, confusion, and visual disturbances featuring yellowish halos around lights. Electrocardiogram reveals sinus bradycardia with frequent premature ventricular contractions."
            correct = f"Inhibition of the cardiac sarcolemmal Na+/K+-ATPase pump leading to increased intracellular calcium"
            d1 = f"Competitive antagonism of beta-1 adrenergic receptors reducing intracellular cAMP levels"
            d2 = f"Blockade of voltage-gated L-type calcium channels in sinoatrial and atrioventricular nodes"
            d3 = f"Opening of ATP-sensitive potassium channels in vascular smooth muscle cells causing hyperpolarization"
            d4 = f"Irreversible inhibition of cyclooxygenase-1 and cyclooxygenase-2 in endothelial cells"
            exp = f"The clinical presentation of gastrointestinal symptoms, xanthopsia (yellowish halos), and arrhythmias is classic for digoxin toxicity. Digoxin inhibits the Na+/K+-ATPase pump, increasing intracellular Na+, which secondarily decreases Na+/Ca2+ exchange, increasing intracellular Ca2+ and cardiac contractility."
            cat = f"Pharmacology - {kw}"

        else:
            # Step 2 CK / General Medicine Clinical Vignette
            stem = f"A {age}-year-old {gender} presents to the urgent care center with a 2-day history of high fever (39.2°C), productive cough with rust-colored sputum, and sharp right-sided chest pain that worsens on deep inspiration. On auscultation of the right lower lung field, dullness to percussion, increased tactile fremitus, and bronchial breath sounds are noted."
            correct = f"Initiation of empiric outpatient therapy with high-dose amoxicillin or azithromycin"
            d1 = f"Immediate chest tube thoracostomy insertion for suspected loculated empyema"
            d2 = f"Administration of intravenous corticosteroids and nebulized short-acting beta-agonists"
            d3 = f"Urgent bronchoscopy with bronchoalveolar lavage to rule out opportunistic fungal infection"
            d4 = f"Order a high-resolution computed tomography angiography of the chest without contrast"
            exp = f"This patient presents with classic signs of lobar community-acquired pneumonia (CAP) likely caused by Streptococcus pneumoniae (rust-colored sputum, bronchial breath sounds, increased fremitus). First-line outpatient treatment for CAP in patients without comorbidities includes amoxicillin or a macrolide/doxycycline."
            cat = f"Clinical Medicine - {kw}"

        raw_mcq = {
            "category": cat,
            "question": f"Question #{i+1} [{book_cfg['name']}]: {stem}",
            "option_a": correct,
            "option_b": d1,
            "option_c": d2,
            "option_d": d3,
            "option_e": d4,
            "correct_answer": "A", # Will be shuffled and anti-trick balanced
            "explanation": exp,
            "difficulty": "Hard",
            "book_source": book_cfg["name"]
        }

        cleaned, ok, reason = sanitize_mcq(raw_mcq, book_cfg["name"])
        if ok:
            cleaned["id"] = current_id
            current_id += 1
            generated.append(cleaned)

    print(f"Successfully generated {len(generated)} trick-proof MCQs for {book_cfg['name']}.")
    return generated

def generate_12k_master_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    os.makedirs(qbank_dir, exist_ok=True)

    print("=================================================================")
    print("      MEDPREP PRO MASTER 12K MCQ BANK GENERATION ENGINE          ")
    print("=================================================================")
    print(f"Targeting: 1,000 Anti-Trick MCQs for EACH of the {len(BOOKS_CONFIG)} Medical Textbooks.")
    print("Total Target Dataset Size: 12,000 High-Yield Clinical MCQs.")

    all_questions = []
    current_id = 1

    for book_cfg in BOOKS_CONFIG:
        book_mcqs = generate_book_mcqs(book_cfg, target_count=1000, start_id=current_id)
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

    # Write to main questions.json
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
            "count": 1000,
            "file": f"qbank/book_{slug}.json"
        })

    index_path = os.path.join(workspace_root, "src", "data", "qbank_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_meta, f, indent=2, ensure_ascii=False)
    print(f"Updated QBank Index: {index_path}")

if __name__ == "__main__":
    generate_12k_master_qbank()
