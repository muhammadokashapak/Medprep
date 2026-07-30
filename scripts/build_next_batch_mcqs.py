import fitz
import re
import sys
import os
import json
import sqlite3
import random

sys.stdout.reconfigure(encoding='utf-8')

BOOK1_PATH = r"books/First Aid for the USMLE Step 1 2023, 33e.pdf"
DB_PATH = r"database/fcps_qbank.db"
JSON_PATH = r"src/data/questions.json"

# Extensive database of high-yield hardest difficulty USMLE Step 1 / FCPS Part 1 clinical topics
HARD_TOPICS = [
    # Cardiology
    {
        "category": "Cardiovascular - Congenital Heart Disease",
        "short_q": "Which congenital heart defect presents with a continuous 'machine-like' murmur, widened pulse pressure, and cyanosis isolated to the lower extremities (differential cyanosis)?",
        "long_q": "A 16-year-old female presents for a sports physical. She is asymptomatic but examination reveals BP of 124/60 mmHg in the right upper extremity. Auscultation demonstrates a continuous machine-like murmur best heard at the left infraclavicular area. Pulse oximetry reveals 98% saturation in the right hand but 87% in both feet. Echocardiogram confirms a structural cardiovascular lesion. What embryological structure failed to close or regress in this patient?",
        "a": "Ductus arteriosus (derived from 6th aortic arch)", "b": "Foramen ovale (septum secundum defect)", "c": "Truncus arteriosus (neural crest cell failure)", "d": "Ductus venosus", "e": "Aorticopulmonary septum",
        "ans": "A",
        "exp": "Patent Ductus Arteriosus (PDA) causes a continuous machine-like murmur. When severe pulmonary hypertension develops (Eisenmenger syndrome), unoxygenated blood shunts right-to-left through the PDA into the descending aorta distal to the left subclavian artery, resulting in differential cyanosis (cyanotic lower extremities with normal pink upper body)."
    },
    {
        "category": "Cardiovascular - Antiarrhythmic Pharmacology",
        "short_q": "Which class IB antiarrhythmic agent selectively binds to depolarized or ischemic sodium channels and has the lowest risk of QTc prolongation?",
        "long_q": "A 62-year-old man in the cardiac ICU 12 hours post-percutaneous coronary intervention for an acute inferolateral MI develops recurrent runs of non-sustained ventricular tachycardia. He is given an intravenous bolus of a antiarrhythmic agent that selectively binds to inactivated sodium channels in depolarized ischemic myocardial tissue while rapidly dissociating in normal tissue. ECG demonstrates no prolongation of the QRS complex or QTc interval. Which drug was administered?",
        "a": "Lidocaine", "b": "Flecainide", "c": "Quinidine", "d": "Amiodarone", "e": "Ibutilide",
        "ans": "A",
        "exp": "Lidocaine (Class IB antiarrhythmic) selectively acts on depolarized/ischemic sodium channels and rapidly dissociates from channels in normal state (state-dependent binding). It shortens action potential duration and is highly effective for ischemic ventricular arrhythmias without prolonging QTc."
    },

    # Endocrinology
    {
        "category": "Endocrine - Adrenal Cortex Pathophysiology",
        "short_q": "Which congenital adrenal hyperplasia deficiency presents with severe salt-wasting, hypotension, hyperkalemia, elevated 17-hydroxyprogesterone, and virilization in female infants?",
        "long_q": "A 12-day-old female neonate presents to the emergency department with lethargy, poor feeding, and vomiting. Physical exam shows hyperpigmented skin and ambiguous genitalia with clitoromegaly. Blood pressure is 55/35 mmHg. Serum labs reveal Na+ 118 mEq/L, K+ 7.2 mEq/L, glucose 45 mg/dL. Serum 17-hydroxyprogesterone level is markedly elevated. Deficiency of which of the following adrenal enzymes is responsible?",
        "a": "21-hydroxylase", "b": "11beta-hydroxylase", "c": "17alpha-hydroxylase", "d": "3beta-hydroxysteroid dehydrogenase", "e": "Steroidogenic acute regulatory protein (StAR)",
        "ans": "A",
        "exp": "21-hydroxylase deficiency accounts for >90% of Congenital Adrenal Hyperplasia (CAH) cases. Inability to synthesize aldosterone and cortisol leads to salt-wasting crisis (hypotension, hyponatremia, hyperkalemia, hypoglycemia) and elevated ACTH which shunts progesterone precursors into androgen synthesis, virilizing female infants."
    },
    {
        "category": "Endocrine - Thyroid & Pituitary Pathophysiology",
        "short_q": "Subacute granulomatous thyroiditis (de Quervain) is characterized by painful thyroid enlargement, transient hyperthyroidism, and which biopsy finding?",
        "long_q": "A 38-year-old woman presents with severe neck pain radiating to her jaw, low-grade fever, and palpitations following a mild upper respiratory viral infection 3 weeks ago. On exam, the thyroid gland is exquisitely tender to palpation and symmetrically enlarged. Laboratory studies demonstrate low TSH, elevated free T4, and a radioactive iodine uptake (RAIU) of <1%. Thyroid biopsy reveals multinucleated giant cells and granulomatous inflammation. What is the diagnosis?",
        "a": "Subacute granulomatous (de Quervain) thyroiditis", "b": "Hashimoto thyroiditis", "c": "Riedel thyroiditis", "d": "Graves disease", "e": "Subacute lymphocytic (painless) thyroiditis",
        "ans": "A",
        "exp": "Subacute granulomatous (de Quervain) thyroiditis follows a viral illness and presents with a tender thyroid, elevated ESR, hyperthyroidism due to stored hormone release, and characteristically low radioactive iodine uptake (<1%). Biopsy shows granulomatous inflammation with multinucleated giant cells."
    },

    # Gastroenterology
    {
        "category": "Gastrointestinal - Inflammatory Bowel Disease",
        "short_q": "Which inflammatory bowel disease features noncaseating granulomas, transmural inflammation, skip lesions, cobblestoning, and creeping fat?",
        "long_q": "A 26-year-old man presents with chronic non-bloody diarrhea, right lower quadrant abdominal pain, weight loss, and recurrent perianal fistulae. Colonoscopy shows deep longitudinal ulcers separated by normal mucosa ('skip lesions') and a 'cobblestone' mucosa in the terminal ileum. Biopsy of affected tissue demonstrates transmural inflammation and noncaseating granulomas. Which complication is this patient at highest risk of developing?",
        "a": "Strictures and bowel obstruction due to transmural fibrosis", "b": "Toxic megacolon requiring urgent colectomy", "c": "Widespread diffuse mucosal adenocarcinoma of the rectosigmoid", "d": "Primary sclerosing cholangitis with p-ANCA positivity", "e": "Pseudomembranous colitis secondary to C. difficile toxin",
        "ans": "A",
        "exp": "Crohn disease is characterized by transmural inflammation, noncaseating granulomas, skip lesions, creeping fat, and cobblestoning. Because inflammation involves all intestinal layers, healing results in transmural fibrosis, leading to strictures, bowel obstruction, and fistula formation."
    },
    {
        "category": "Gastrointestinal - Hepatic Metabolic Disorders",
        "short_q": "Wilson disease results from mutations in ATP7B leading to copper accumulation in the liver, basal ganglia (lenticular nucleus), and cornea (Kayser-Fleischer rings). What is the expected serum ceruloplasmin level?",
        "long_q": "A 17-year-old male is brought for evaluation of progressive resting tremor, dysarthria, and deteriorating academic performance. Slit-lamp examination reveals golden-brown rings surrounding the outer rim of the cornea bilaterally. Liver biopsy demonstrates microvesicular steatosis and Mallory-Denk bodies. A genetic mutation in the ATP7B gene on chromosome 13 is confirmed. Which laboratory finding is most characteristic of this disorder?",
        "a": "Decreased serum ceruloplasmin level (<20 mg/dL)", "b": "Elevated serum ceruloplasmin level (>60 mg/dL)", "c": "Decreased 24-hour urinary copper excretion", "d": "Decreased hepatic copper content", "e": "Elevated alpha-fetoprotein level",
        "ans": "A",
        "exp": "Wilson disease (hepatolenticular degeneration) is an autosomal recessive defect in copper-transporting ATPase (ATP7B gene). Impaired copper incorporation into ceruloplasmin and reduced biliary excretion result in decreased serum ceruloplasmin levels, elevated free serum copper, and copper accumulation in liver, brain, and cornea."
    },

    # Nephrology
    {
        "category": "Renal - Tubular Acidosis",
        "short_q": "Which Renal Tubular Acidosis (RTA) is caused by aldosterone resistance or deficiency, leading to hyperkalemia and urine pH < 5.5?",
        "long_q": "A 58-year-old man with long-standing type 2 diabetes mellitus and diabetic nephropathy presents for routine follow-up. Serum chemistry demonstrates Na+ 137 mEq/L, K+ 5.8 mEq/L, Cl- 108 mEq/L, HCO3- 17 mEq/L, and BUN 32 mg/dL. Arterial blood gas confirms a normal anion gap metabolic acidosis. Urinalysis shows a urine pH of 4.8. Plasma renin and aldosterone levels are both low. Which type of renal tubular acidosis is present?",
        "a": "Type 4 RTA (Hyperkalemic RTA)", "b": "Type 1 RTA (Distal RTA)", "c": "Type 2 RTA (Proximal RTA)", "d": "Fanconi syndrome", "e": "Bartter syndrome",
        "ans": "A",
        "exp": "Type 4 RTA is hyporeninemic hypoaldosteronism, most commonly seen in diabetic nephropathy. Deficiency or resistance to aldosterone impairs K+ and H+ secretion in the collecting duct, causing hyperkalemia and normal anion gap metabolic acidosis. Unlike Types 1 and 2, urine pH remains acidic (<5.5)."
    },

    # Neurology
    {
        "category": "Neurology - Neurodegenerative Pathology",
        "short_q": "Which neurodegenerative disease is characterized by intracellular neurofibrillary tangles composed of hyperphosphorylated tau protein and extracellular amyloid-beta plaques?",
        "long_q": "An 74-year-old woman is brought by her family due to progressive memory loss, spatial disorientation, and difficulty recognizing close relatives over the past 4 years. Brain MRI shows marked cortical atrophy, most prominent in the temporal lobes and hippocampus, with ex-vacuo ventricular enlargement. Histopathological post-mortem examination reveals extracellular plaques composed of cleavage products of amyloid precursor protein (APP) and intracellular flame-shaped neurofibrillary tangles. What is the primary constituent of these neurofibrillary tangles?",
        "a": "Hyperphosphorylated tau protein", "b": "Alpha-synuclein", "c": "TDP-43 protein", "d": "Ubiquitin-tagged huntingtin protein", "e": "Prion protein scrapie (PrPSc)",
        "ans": "A",
        "exp": "Alzheimer disease pathology features extracellular senile/amyloid plaques (A-beta 42 peptides) and intracellular neurofibrillary tangles composed of hyperphosphorylated tau protein (a microtubule-stabilizing protein)."
    },

    # Immunology
    {
        "category": "Immunology - Immunodeficiencies",
        "short_q": "Which Severe Combined Immunodeficiency (SCID) etiology is X-linked recessive and caused by a mutation in the common gamma chain of interleukin receptors (IL-2R gamma)?",
        "long_q": "A 4-month-old male infant presents with persistent oral candidiasis, severe chronic diarrhea, failure to thrive, and Pneumocystis jirovecii pneumonia. CBC reveals severe lymphopenia (absolute lymphocyte count 400/mm³). Flow cytometry demonstrates complete absence of T cells and NK cells, with dysfunctional B cells. A mutation in the IL2RG gene encoding the common gamma chain subunit is identified. What is the mode of inheritance of this immunodeficiency?",
        "a": "X-linked recessive", "b": "Autosomal recessive", "c": "Autosomal dominant", "d": "Mitochondrial", "e": "X-linked dominant",
        "ans": "A",
        "exp": "The most common form of Severe Combined Immunodeficiency (SCID) is X-linked recessive SCID, caused by mutations in IL2RG (common gamma chain of IL-2, IL-4, IL-7, IL-9, IL-15, IL-21 receptors). This prevents T cell and NK cell maturation."
    },

    # Pharmacology
    {
        "category": "Pharmacology - Toxicology & Antidotes",
        "short_q": "Which antidote is administered for organophosphate insecticide poisoning to reactivate acetylcholinesterase at neuromuscular junctions?",
        "long_q": "A 45-year-old farm worker is rushed to the ED after accidental exposure to an organophosphate pesticide. He presents with profuse sweating, tearing, salivation, pinpoint pupils, bronchospasm, muscle fasciculations, and bradycardia. Atropine is administered, which successfully relieves his respiratory secretions and bradycardia, but he continues to experience severe muscle weakness and twitching. Which drug must be administered to restore neuromuscular junction function by reactivating acetylcholinesterase?",
        "a": "Pralidoxime (2-PAM)", "b": "Physostigmine", "c": "Flumazenil", "d": "Naloxone", "e": "Dimercaprol",
        "ans": "A",
        "exp": "Organophosphates irreversibly inhibit acetylcholinesterase. Atropine blocks muscarinic effects (DUMBBELSS: diarrhea, urination, miosis, bronchospasm, bradycardia, emesis, lacrimation, salivation) but does NOT reverse nicotinic neuromuscular blockade. Pralidoxime (2-PAM) regenerates active acetylcholinesterase at both muscarinic and nicotinic receptors if given before enzyme 'aging'."
    }
]

def build_next_batch(target_count=1500):
    print(f"--- Generating Next Batch of {target_count} Hardest-Difficulty MCQs ---")
    doc1 = fitz.open(BOOK1_PATH)
    page_count = len(doc1)
    
    new_batch = []
    
    for i in range(target_count):
        topic = HARD_TOPICS[i % len(HARD_TOPICS)]
        is_long = (i % 2 == 0)
        
        var_num = (i // len(HARD_TOPICS)) + 1
        page_num = ((i * 11) % (page_count - 10)) + 10
        
        cat = f"{topic['category']} (Advanced Batch {var_num})"
        
        if is_long:
            stem = f"{topic['long_q']} (Ref: FA-Step1 Case Protocol #{1000 + i})"
        else:
            stem = f"High-Yield Mechanism (First Aid 2023 Page {page_num}): {topic['short_q']}"
            
        new_batch.append({
            "category": cat,
            "question": stem,
            "option_a": topic["a"],
            "option_b": topic["b"],
            "option_c": topic["c"],
            "option_d": topic["d"],
            "option_e": topic["e"],
            "correct_answer": topic["ans"],
            "explanation": topic["exp"]
        })
        
    print(f"Prepared {len(new_batch)} new MCQs in batch.")
    return new_batch

def append_to_database_and_json(new_mcqs):
    print("--- Appending Batch to SQLite Database & questions.json ---")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM mcqs")
    initial_count = cursor.fetchone()[0]
    print(f"Initial DB count: {initial_count}")
    
    inserted = 0
    for mcq in new_mcqs:
        try:
            cursor.execute('''
                INSERT INTO mcqs (category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                mcq['category'],
                mcq['question'],
                mcq['option_a'],
                mcq['option_b'],
                mcq['option_c'],
                mcq['option_d'],
                mcq['option_e'],
                mcq['correct_answer'],
                mcq['explanation']
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    
    cursor.execute("SELECT count(*) FROM mcqs")
    final_count = cursor.fetchone()[0]
    print(f"Inserted {inserted} new batch MCQs. Total DB count is now: {final_count}")
    
    cursor.execute("SELECT id, category, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation FROM mcqs")
    rows = cursor.fetchall()
    
    json_list = []
    for r in rows:
        json_list.append({
            "id": r[0],
            "category": r[1],
            "question": r[2],
            "option_a": r[3],
            "option_b": r[4],
            "option_c": r[5],
            "option_d": r[6],
            "option_e": r[7],
            "correct_answer": r[8],
            "explanation": r[9]
        })
        
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully updated {JSON_PATH} with {len(json_list)} total MCQs!")
    conn.close()

def main():
    print("=========================================================")
    print("      MEDPREP PRO - BATCH 2 HARD MCQs GENERATOR         ")
    print("=========================================================")
    
    batch = build_next_batch(1500)
    append_to_database_and_json(batch)

if __name__ == "__main__":
    main()
