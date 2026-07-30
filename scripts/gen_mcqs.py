import json
import os

qA = [
    {
        "question": "A 45-year-old female with Graves' disease is started on propylthiouracil. Six weeks later, she presents with a sore throat, fever, and a macular rash. Laboratory evaluation reveals a leukocyte count of 800/mm3. Which of the following best describes the molecular mechanism responsible for the primary therapeutic effect of the drug prior to this adverse event?",
        "option_a": "Inhibition of thyroid peroxidase-catalyzed iodination and coupling, plus peripheral inhibition of 5'-deiodinase",
        "option_b": "Direct inhibition of the sodium-iodide symporter on the basolateral membrane of thyroid follicular cells",
        "option_c": "Proteolytic cleavage of thyroglobulin and inhibition of hormone release via lysosomal pathways",
        "option_d": "Irreversible destruction of thyroid follicular cells via beta-particle emission causing local tissue necrosis",
        "option_e": "Competitive antagonism of TSH at its Gs-protein coupled receptor on thyroid follicular cells",
        "correct_answer": "A",
        "explanation": "Propylthiouracil (PTU) acts primarily by inhibiting thyroid peroxidase (TPO). It also blocks peripheral conversion of T4 to T3 by inhibiting 5'-deiodinase. The patient presents with agranulocytosis, a severe adverse effect.",
        "source_context": "Endocrine Pharmacology - Thyroid"
    },
    {
        "question": "A 62-year-old man with a 10-year history of type 2 diabetes mellitus is prescribed glipizide. After taking the medication, he experiences a severe episode of hypoglycemia. The medication primarily exerted its effect by binding to a specific receptor on the pancreatic beta cell. Binding to this receptor directly causes which of the following intracellular events?",
        "option_a": "Closure of ATP-sensitive potassium channels by binding SUR1, leading to membrane depolarization",
        "option_b": "Activation of adenylyl cyclase via Gs-coupled receptor, directly phosphorylating calcium channels",
        "option_c": "Inhibition of dipeptidyl peptidase-4, prolonging the half-life of endogenous GLP-1",
        "option_d": "Direct allosteric activation of peroxisome proliferator-activated receptor-gamma (PPAR-gamma)",
        "option_e": "Opening of ATP-sensitive potassium channels causing hyperpolarization and reduced insulin secretion",
        "correct_answer": "A",
        "explanation": "Sulfonylureas like glipizide bind to the SUR1 subunit of the ATP-sensitive potassium channel (K-ATP channel) on the pancreatic beta cell membrane. This binding closes the channel, preventing potassium efflux, which depolarizes the cell membrane and opens voltage-gated calcium channels.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 23-year-old woman with a history of recurrent epistaxis and heavy menstrual bleeding is diagnosed with von Willebrand disease type 1. She is scheduled for a minor dental extraction. Which of the following pharmacologic agents, when administered preoperatively, will most effectively increase her circulating levels of von Willebrand factor?",
        "option_a": "Desmopressin (dDAVP)",
        "option_b": "Aminocaproic acid",
        "option_c": "Tranexamic acid",
        "option_d": "Recombinant factor VIII",
        "option_e": "Fresh frozen plasma",
        "correct_answer": "A",
        "explanation": "Desmopressin (dDAVP) is a synthetic analog of vasopressin that stimulates the release of von Willebrand factor (vWF) and Factor VIII from endothelial cells (Weibel-Palade bodies).",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 55-year-old man with New York Heart Association class III heart failure is started on a medication that has been shown to reduce mortality. Six months later, he presents complaining of painful breast enlargement and decreased libido. The medication responsible for these side effects most likely acts at which of the following nephron segments?",
        "option_a": "Late distal tubule and cortical collecting duct",
        "option_b": "Thick ascending limb of the loop of Henle",
        "option_c": "Proximal convoluted tubule",
        "option_d": "Early distal convoluted tubule",
        "option_e": "Medullary collecting duct",
        "correct_answer": "A",
        "explanation": "Spironolactone is an aldosterone antagonist that acts on the late distal tubule and cortical collecting duct by competitively inhibiting the mineralocorticoid receptor. Its antiandrogenic effects can cause gynecomastia.",
        "source_context": "Endocrine Pharmacology - Adrenal/Renal"
    },
    {
        "question": "A 28-year-old woman with polycystic ovary syndrome (PCOS) is seeking treatment for infertility. She is prescribed a medication that acts as a selective estrogen receptor modulator (SERM). By which of the following mechanisms does this medication primarily induce ovulation?",
        "option_a": "Antagonism of estrogen receptors in the hypothalamus, blocking negative feedback and increasing GnRH pulse frequency",
        "option_b": "Direct stimulation of follicle-stimulating hormone (FSH) receptors on ovarian granulosa cells",
        "option_c": "Inhibition of aromatase in the ovaries, leading to a decrease in the conversion of androgens to estrogens",
        "option_d": "Agonism of progesterone receptors in the endometrium, promoting a secretory phase conducive to implantation",
        "option_e": "Stimulation of luteinizing hormone (LH) surge via direct action on the anterior pituitary gonadotrophs",
        "correct_answer": "A",
        "explanation": "Clomiphene citrate is a SERM that acts primarily as an estrogen receptor antagonist in the hypothalamus. By blocking the negative feedback of endogenous estrogens, it increases the pulsatile release of GnRH.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 72-year-old woman with severe osteoporosis is prescribed a subcutaneous monoclonal antibody. The drug prevents the differentiation and activation of a specific bone cell type. Which of the following is the specific molecular target of this medication?",
        "option_a": "Receptor activator of nuclear factor kappa-B ligand (RANKL)",
        "option_b": "Sclerostin (SOST) glycoprotein secreted by osteocytes",
        "option_c": "Macrophage colony-stimulating factor (M-CSF) receptor",
        "option_d": "Parathyroid hormone 1 receptor (PTH1R) on osteoblasts",
        "option_e": "Farnesyl pyrophosphate synthase in the mevalonate pathway",
        "correct_answer": "A",
        "explanation": "Denosumab is a monoclonal antibody that binds to and neutralizes RANKL, preventing it from binding to RANK on osteoclast precursors, thereby profoundly inhibiting bone resorption.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 68-year-old man with type 2 diabetes and chronic kidney disease (eGFR 25 mL/min) presents with deep, rapid breathing and an elevated anion gap metabolic acidosis. He was recently started on a first-line antidiabetic medication. Which of the following mechanisms best explains the primary intended pharmacological effect of the offending agent?",
        "option_a": "Inhibition of hepatic gluconeogenesis via activation of AMP-activated protein kinase (AMPK) and inhibition of mitochondrial complex I",
        "option_b": "Activation of peroxisome proliferator-activated receptor-gamma (PPAR-gamma) in adipose tissue",
        "option_c": "Inhibition of sodium-glucose cotransporter-2 (SGLT2) in the proximal renal tubule",
        "option_d": "Stimulation of insulin release from pancreatic beta cells by closing ATP-sensitive potassium channels",
        "option_e": "Competitive inhibition of alpha-glucosidase enzymes in the intestinal brush border",
        "correct_answer": "A",
        "explanation": "Metformin's primary mechanism is the inhibition of hepatic gluconeogenesis via AMPK activation and mitochondrial complex I inhibition. It can cause lactic acidosis, especially in severe renal impairment.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 34-year-old woman presents with galactorrhea, amenorrhea, and bitemporal hemianopsia. MRI reveals a pituitary macroadenoma. She is started on an ergot derivative with high affinity for D2 receptors. Which of the following describes the most likely downstream intracellular effect in the tumor cells following administration of this drug?",
        "option_a": "Decreased adenylyl cyclase activity and reduced cyclic AMP (cAMP) production",
        "option_b": "Increased phospholipase C activity and elevated inositol triphosphate (IP3)",
        "option_c": "Opening of voltage-gated calcium channels causing rapid calcium influx",
        "option_d": "Inhibition of tyrosine kinase auto-phosphorylation and decreased MAP kinase activity",
        "option_e": "Activation of guanylyl cyclase and increased cyclic GMP (cGMP) production",
        "correct_answer": "A",
        "explanation": "Dopamine D2 receptors are Gi-protein coupled. Activation of Gi by agonists like cabergoline leads to the inhibition of adenylyl cyclase, decreasing cAMP production, suppressing prolactin synthesis.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 40-year-old man with primary adrenal insufficiency (Addison's disease) is stabilized on hydrocortisone but continues to experience orthostatic hypotension and hyperkalemia. An additional medication is added. Which of the following distinct properties makes the added drug highly efficacious for treating this patient's remaining symptoms?",
        "option_a": "High mineralocorticoid potency relative to its glucocorticoid activity",
        "option_b": "Selective competitive antagonism of the angiotensin II type 1 (AT1) receptor",
        "option_c": "Irreversible inhibition of 11-beta-hydroxylase in the adrenal cortex",
        "option_d": "Potent stimulation of antidiuretic hormone (ADH) release from the posterior pituitary",
        "option_e": "Direct activation of epithelial sodium channels (ENaC) independent of receptor binding",
        "correct_answer": "A",
        "explanation": "Fludrocortisone is a synthetic corticosteroid with very high mineralocorticoid potency, used specifically for its potent sodium-retaining effects in primary adrenal insufficiency.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 60-year-old postmenopausal woman with a history of deep vein thrombosis is seeking medication for severe osteoporosis. A drug is considered that acts as an agonist at estrogen receptors in bone but as an antagonist in breast tissue. Which of the following agents fits this specific mechanistic profile?",
        "option_a": "Raloxifene",
        "option_b": "Tamoxifen",
        "option_c": "Alendronate",
        "option_d": "Anastrozole",
        "option_e": "Fulvestrant",
        "correct_answer": "A",
        "explanation": "Raloxifene is a SERM that acts as an agonist in bone and an antagonist in breast and endometrial tissue. It carries a boxed warning for increased risk of venous thromboembolism.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    }
]

qB = [
    {
        "question": "A 28-year-old pregnant woman in her first trimester is diagnosed with severe hyperthyroidism due to Graves' disease. Which of the following treatments is strictly contraindicated due to the risk of irreversible fetal destruction of a developing endocrine gland?",
        "option_a": "Propylthiouracil",
        "option_b": "Radioactive iodine (131-I)",
        "option_c": "Propranolol",
        "option_d": "Potassium iodide (Lugol's solution)",
        "option_e": "Methimazole",
        "correct_answer": "B",
        "explanation": "Radioactive iodine (131-I) is absolutely contraindicated during pregnancy because it readily crosses the placenta and will concentrate in the fetal thyroid gland, causing irreversible destruction and lifelong cretinism.",
        "source_context": "Endocrine Pharmacology - Thyroid"
    },
    {
        "question": "A 55-year-old man with type 2 diabetes is prescribed a medication that competitively inhibits intestinal brush border enzymes. Two weeks later, he complains of severe flatulence. Which of the following is the most appropriate advice regarding the management of potential hypoglycemia in this patient while on this specific drug?",
        "option_a": "Administer oral sucrose immediately at the onset of hypoglycemic symptoms",
        "option_b": "Administer oral glucose or dextrose, as complex carbohydrates will not be effectively absorbed",
        "option_c": "Inject intramuscular glucagon, as all oral sugars will be malabsorbed",
        "option_d": "Stop the medication immediately and administer intravenous 50% dextrose",
        "option_e": "Administer oral fructose, as it bypasses the inhibited enzymatic pathways",
        "correct_answer": "B",
        "explanation": "Acarbose and miglitol are alpha-glucosidase inhibitors. If a patient experiences hypoglycemia, they must be treated with oral glucose (dextrose) because the breakdown of complex sugars (like sucrose) is inhibited by the drug.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 42-year-old man with acromegaly fails to respond to somatostatin analog therapy. He is started on a medication that is a genetically engineered analog of growth hormone. By which of the following mechanisms does this medication exert its therapeutic effect?",
        "option_a": "Activation of dopamine D2 receptors on somatotrophs, decreasing GH release",
        "option_b": "Competitive antagonism of growth hormone at its peripheral cell surface receptors",
        "option_c": "Irreversible binding to the growth hormone-releasing hormone (GHRH) receptor on the anterior pituitary",
        "option_d": "Inhibition of hepatic insulin-like growth factor 1 (IGF-1) synthesis via a direct toxic effect on hepatocytes",
        "option_e": "Allosteric modulation of the somatostatin receptor subtype 5 (SSTR5)",
        "correct_answer": "B",
        "explanation": "Pegvisomant is a growth hormone receptor antagonist used in the treatment of acromegaly. It competitively blocks the peripheral action of endogenous GH, lowering IGF-1 levels.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 38-year-old woman is diagnosed with Cushing's disease. To manage her severe hypercortisolism preoperatively, she is prescribed an antifungal medication known to inhibit multiple cytochrome P450 enzymes. Which of the following enzymes is the primary target of this medication at high doses in the adrenal cortex?",
        "option_a": "3-beta-hydroxysteroid dehydrogenase",
        "option_b": "Cholesterol desmolase (CYP11A1) and 11-beta-hydroxylase (CYP11B1)",
        "option_c": "17-alpha-hydroxylase (CYP17A1) only",
        "option_d": "21-hydroxylase (CYP21A2) only",
        "option_e": "Aldosterone synthase (CYP11B2)",
        "correct_answer": "B",
        "explanation": "Ketoconazole at high doses broadly inhibits gonadal and adrenal steroidogenesis. It primarily blocks cholesterol desmolase and 11-beta-hydroxylase, effectively lowering cortisol levels.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 65-year-old man with benign prostatic hyperplasia and male pattern baldness is prescribed a medication that improves his urinary symptoms but causes decreased libido. The medication prescribed primarily works by inhibiting which of the following processes?",
        "option_a": "Conversion of testosterone to estradiol by aromatase",
        "option_b": "Conversion of testosterone to dihydrotestosterone (DHT) by 5-alpha-reductase",
        "option_c": "Binding of dihydrotestosterone to the androgen receptor",
        "option_d": "Pulsatile release of gonadotropin-releasing hormone (GnRH) from the hypothalamus",
        "option_e": "Synthesis of androgens in the Leydig cells by inhibiting 17,20-lyase",
        "correct_answer": "B",
        "explanation": "Finasteride is a competitive inhibitor of type II 5-alpha-reductase, preventing the peripheral conversion of testosterone to the more potent androgen dihydrotestosterone (DHT).",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 68-year-old woman with severe osteoporosis is initiated on a daily subcutaneous injection of a recombinant peptide. When administered in this pulsatile manner, the medication stimulates bone formation. Continuous administration of the same endogenous hormone would result in which of the following physiological effects?",
        "option_a": "Stimulation of osteoblast differentiation and increased bone mass",
        "option_b": "Increased osteoclast activity and net bone resorption via RANKL upregulation",
        "option_c": "Decreased renal reabsorption of calcium in the distal tubule",
        "option_d": "Inhibition of 1-alpha-hydroxylase activity in the proximal tubule",
        "option_e": "Increased synthesis of osteoprotegerin (OPG) by osteoblasts",
        "correct_answer": "B",
        "explanation": "Teriparatide is a recombinant portion of human parathyroid hormone. Intermittent exposure stimulates bone formation, whereas continuous exposure (like in hyperparathyroidism) promotes net bone resorption.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 45-year-old obese man with type 2 diabetes mellitus is started on an injectable incretin mimetic to improve glycemic control and promote weight loss. The medication resists degradation by DPP-4. Which of the following best describes the physiological classification of this drug?",
        "option_a": "Dipeptidyl peptidase-4 (DPP-4) inhibitor",
        "option_b": "Glucagon-like peptide-1 (GLP-1) receptor agonist",
        "option_c": "Amylin analog",
        "option_d": "Gastric inhibitory polypeptide (GIP) analog",
        "option_e": "Melanocortin 4 receptor (MC4R) agonist",
        "correct_answer": "B",
        "explanation": "Liraglutide and exenatide are GLP-1 receptor agonists. They resist degradation by DPP-4 and act on GLP-1 receptors to potentiate glucose-dependent insulin secretion and delay gastric emptying.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 50-year-old man with cirrhosis presents with massive hematemesis due to ruptured esophageal varices. An intravenous infusion of a synthetic octapeptide is initiated to control bleeding by inducing splanchnic vasoconstriction. The endogenous hormone this drug mimics is normally secreted by which of the following cell types?",
        "option_a": "Alpha cells of the pancreatic islets",
        "option_b": "Delta cells of the pancreatic islets and hypothalamus",
        "option_c": "G cells of the gastric antrum",
        "option_d": "Parafollicular C cells of the thyroid gland",
        "option_e": "Chromaffin cells of the adrenal medulla",
        "correct_answer": "B",
        "explanation": "Octreotide is a synthetic analog of somatostatin. Somatostatin is naturally secreted by the delta (D) cells of the pancreatic islets, the hypothalamus, and the GI tract.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 32-year-old woman requests medical termination of a 6-week intrauterine pregnancy. She is administered a drug that acts as a competitive receptor antagonist. Which of the following side effects is most uniquely associated with high doses of this specific medication due to its secondary pharmacological target?",
        "option_a": "Severe hepatotoxicity and fulminant liver failure",
        "option_b": "Glucocorticoid receptor antagonism leading to symptoms of transient adrenal insufficiency",
        "option_c": "Irreversible bone marrow suppression and aplastic anemia",
        "option_d": "Thromboembolic events due to potent estrogenic activity",
        "option_e": "Prolonged QT interval and torsades de pointes",
        "correct_answer": "B",
        "explanation": "Mifepristone (RU-486) is a competitive antagonist at both progesterone and glucocorticoid receptors. Because of its potent anti-glucocorticoid effects at high doses, it can cause symptoms of adrenal insufficiency.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 58-year-old postmenopausal woman with estrogen receptor-positive breast cancer is treated with an oral nonsteroidal drug that significantly lowers her circulating estrogen levels. She subsequently develops severe joint pains. The enzyme inhibited by this drug normally catalyzes the conversion of:",
        "option_a": "Cholesterol to pregnenolone",
        "option_b": "Testosterone to estradiol and androstenedione to estrone",
        "option_c": "Progesterone to 17-hydroxyprogesterone",
        "option_d": "Estrone to estradiol",
        "option_e": "Dehydroepiandrosterone (DHEA) to androstenedione",
        "correct_answer": "B",
        "explanation": "Anastrozole and letrozole are nonsteroidal aromatase inhibitors. Aromatase (CYP19A1) catalyzes the aromatization of androgens into estrogens, specifically converting testosterone to estradiol and androstenedione to estrone.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    }
]

qC = [
    {
        "question": "A 60-year-old man with chronic kidney disease on hemodialysis presents with severe secondary hyperparathyroidism. He is prescribed a medication that allosterically increases the sensitivity of the calcium-sensing receptor on the parathyroid gland. What is the most expected change in his serum laboratory values after starting this medication?",
        "option_a": "Increased serum calcium, increased serum PTH",
        "option_b": "Increased serum calcium, decreased serum PTH",
        "option_c": "Decreased serum calcium, decreased serum PTH",
        "option_d": "Decreased serum calcium, increased serum PTH",
        "option_e": "No change in serum calcium, decreased serum PTH",
        "correct_answer": "C",
        "explanation": "Cinacalcet is a calcimimetic agent that binds to the calcium-sensing receptor (CaSR) on the parathyroid gland, increasing its sensitivity to extracellular calcium. This suppresses PTH secretion, which subsequently lowers serum calcium.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 55-year-old man with type 2 diabetes presents to the ER with nausea, vomiting, and abdominal pain. Blood tests reveal a pH of 7.25, bicarbonate of 14 mEq/L, and elevated serum ketones, but a surprisingly normal blood glucose level of 145 mg/dL. He recently started a new oral hypoglycemic agent. This adverse event is strongly associated with which of the following drug classes?",
        "option_a": "Sulfonylureas",
        "option_b": "Thiazolidinediones",
        "option_c": "Sodium-glucose cotransporter-2 (SGLT2) inhibitors",
        "option_d": "Glucagon-like peptide-1 (GLP-1) receptor agonists",
        "option_e": "Biguanides",
        "correct_answer": "C",
        "explanation": "The patient has euglycemic diabetic ketoacidosis (DKA), a known complication of SGLT2 inhibitors (like canagliflozin). By causing massive glycosuria, they lower blood glucose, which decreases insulin secretion and increases glucagon, promoting ketogenesis.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 65-year-old man with heart failure and severe euvolemic hyponatremia is administered an intravenous drug that acts as a dual antagonist of both V1a and V2 vasopressin receptors. Which of the following correctly describes the expected physiological outcome in the renal collecting duct?",
        "option_a": "Increased insertion of aquaporin-2 channels into the apical membrane",
        "option_b": "Increased synthesis of cyclic GMP (cGMP) and natriuretic peptide release",
        "option_c": "Decreased synthesis of cyclic AMP (cAMP) and reduced aquaporin-2 expression on the apical membrane",
        "option_d": "Activation of the V2 receptor linked to a Gq protein cascade",
        "option_e": "Opening of sodium-potassium-2chloride (NKCC2) cotransporters in the macula densa",
        "correct_answer": "C",
        "explanation": "Conivaptan is a dual V1a and V2 receptor antagonist. In the collecting duct, vasopressin V2 receptors normally increase cAMP, leading to the insertion of aquaporin-2. Antagonism of V2 decreases cAMP, reducing aquaporin-2 insertion and promoting aquaresis.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 40-year-old woman is being evaluated for suspected secondary adrenal insufficiency. The physician administers a drug that blocks the final step of cortisol synthesis. In a patient with a completely intact HPA axis, administration of this drug should cause a significant compensatory increase in which of the following urinary metabolites?",
        "option_a": "Vanillylmandelic acid (VMA)",
        "option_b": "Aldosterone glucuronide",
        "option_c": "17-hydroxycorticosteroids (17-OHCS), specifically 11-deoxycortisol",
        "option_d": "Homovanillic acid (HVA)",
        "option_e": "Pregnanetriol",
        "correct_answer": "C",
        "explanation": "Metyrapone inhibits 11-beta-hydroxylase, blocking the conversion of 11-deoxycortisol to cortisol. This removes cortisol's negative feedback, leading to increased ACTH and accumulation of 11-deoxycortisol, excreted as 17-OHCS.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 70-year-old man with metastatic prostate cancer is treated with a combination of a continuous long-acting GnRH agonist and a nonsteroidal oral medication to prevent the initial 'flare' of tumor growth. The oral medication exerts its effect via which of the following mechanisms?",
        "option_a": "Irreversible inhibition of 5-alpha-reductase type 2",
        "option_b": "Direct inhibition of 17-alpha-hydroxylase in the testes",
        "option_c": "Competitive antagonism at the androgen receptor",
        "option_d": "Stimulation of sex hormone-binding globulin (SHBG) production",
        "option_e": "Inhibition of aromatase in peripheral adipose tissue",
        "correct_answer": "C",
        "explanation": "Flutamide and bicalutamide are nonsteroidal competitive antagonists at the androgen receptor. When a continuous GnRH agonist is initiated, it causes a transient surge in testosterone (the 'flare'). An AR antagonist blocks this effect.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 65-year-old woman has been taking oral alendronate for 7 years for osteoporosis. She presents with deep thigh pain and radiographs reveal a transverse fracture of the subtrochanteric femur with cortical thickening. The pathogenesis of this specific complication is most directly related to the drug's profound suppression of which of the following processes?",
        "option_a": "Intestinal calcium absorption via vitamin D resistance",
        "option_b": "Osteoblast differentiation and survival in the cortical shaft",
        "option_c": "Targeted bone remodeling and microdamage repair by osteoclasts",
        "option_d": "Renal synthesis of 1,25-dihydroxycholecalciferol",
        "option_e": "Collagen cross-linking in the extracellular matrix by lysyl oxidase",
        "correct_answer": "C",
        "explanation": "Atypical femoral fractures are a rare complication of long-term bisphosphonate therapy. By profoundly suppressing osteoclast-mediated bone resorption, bisphosphonates impair normal targeted bone remodeling, leading to microdamage accumulation.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 52-year-old man with type 2 diabetes and a history of congestive heart failure is started on pioglitazone. Three months later, he presents with significant peripheral edema and weight gain, exacerbating his heart failure. This adverse effect is mediated by the activation of PPAR-gamma receptors leading to altered gene transcription in which of the following locations?",
        "option_a": "Hepatocytes, increasing glycogenolysis",
        "option_b": "Proximal convoluted tubule, increasing glucose reabsorption",
        "option_c": "Renal collecting ducts, increasing sodium reabsorption via ENaC",
        "option_d": "Pancreatic beta cells, causing cellular hypertrophy",
        "option_e": "Skeletal muscle, decreasing insulin sensitivity",
        "correct_answer": "C",
        "explanation": "Thiazolidinediones activate PPAR-gamma. In the renal collecting ducts, this upregulates the expression of the epithelial sodium channel (ENaC), leading to sodium and fluid retention, exacerbating heart failure.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 40-year-old woman with hyperprolactinemia due to a microprolactinoma is treated with an ergot derivative. Interestingly, the same medication class, typically at higher doses, is used to manage motor fluctuations in Parkinson's disease. The therapeutic efficacy of this drug in both conditions relies on its agonism at which of the following receptors?",
        "option_a": "Serotonin 5-HT2B receptors",
        "option_b": "Alpha-1 adrenergic receptors",
        "option_c": "Dopamine D2 receptors",
        "option_d": "Histamine H1 receptors",
        "option_e": "Muscarinic M3 receptors",
        "correct_answer": "C",
        "explanation": "Bromocriptine and cabergoline are dopamine D2 receptor agonists. In the anterior pituitary, D2 agonism inhibits prolactin secretion. In the striatum, D2 agonism mimics dopamine to treat Parkinson's.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 60-year-old man with heart failure and a recent myocardial infarction is prescribed a potassium-sparing diuretic. The physician selects a drug that avoids the painful gynecomastia the patient experienced on a previous medication of the same class. The chosen drug achieves this improved side-effect profile due to which of the following properties?",
        "option_a": "It is a non-competitive, irreversible antagonist of aldosterone",
        "option_b": "It directly blocks the epithelial sodium channel (ENaC) without interacting with steroid receptors",
        "option_c": "It is highly selective for the mineralocorticoid receptor with negligible affinity for androgen receptors",
        "option_d": "It is metabolized rapidly by plasma esterases, avoiding tissue accumulation in the breast",
        "option_e": "It acts centrally to decrease sympathetic outflow to the heart",
        "correct_answer": "C",
        "explanation": "Eplerenone is a selective mineralocorticoid receptor antagonist. Unlike spironolactone, which has significant affinity for androgen and progesterone receptors (causing gynecomastia), eplerenone is highly selective.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 22-year-old woman presents to the clinic requesting emergency contraception 48 hours after unprotected intercourse. She is prescribed a single oral dose of a progestin-only medication (1.5 mg). The primary mechanism by which this medication prevents pregnancy when taken at this specific time is by:",
        "option_a": "Causing immediate sloughing of the endometrial lining",
        "option_b": "Being directly toxic to the fertilized zygote before implantation",
        "option_c": "Delaying or inhibiting the mid-cycle luteinizing hormone (LH) surge and subsequent ovulation",
        "option_d": "Competitively blocking progesterone receptors in the uterus",
        "option_e": "Increasing the permeability of the zona pellucida to prevent sperm entry",
        "correct_answer": "C",
        "explanation": "Levonorgestrel (Plan B) is a progestin-only emergency contraceptive. Its primary mechanism of action, when taken before ovulation, is to delay or inhibit the LH surge, thereby preventing ovulation.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    }
]

qD = [
    {
        "question": "A 35-year-old woman with hypothyroidism has been euthyroid on a stable dose of levothyroxine for 2 years. She recently began taking over-the-counter calcium carbonate and ferrous sulfate supplements for general wellness. Six weeks later, she complains of fatigue and cold intolerance. Her TSH is significantly elevated. What is the most likely pharmacokinetic explanation?",
        "option_a": "Increased hepatic metabolism of levothyroxine via CYP450 induction",
        "option_b": "Displacement of levothyroxine from thyroxine-binding globulin (TBG)",
        "option_c": "Increased renal excretion of free T4 via organic anion transporters",
        "option_d": "Decreased gastrointestinal absorption of levothyroxine due to luminal chelation",
        "option_e": "Decreased conversion of T4 to T3 in peripheral tissues by deiodinases",
        "correct_answer": "D",
        "explanation": "Levothyroxine absorption in the gastrointestinal tract is significantly impaired by divalent and trivalent cations, such as calcium and iron, which chelate the drug in the gut lumen. They should be separated by at least 4 hours.",
        "source_context": "Endocrine Pharmacology - Thyroid"
    },
    {
        "question": "A 54-year-old man with type 2 diabetes mellitus is started on sitagliptin. This drug improves his postprandial glucose levels by modulating an endogenous neuroendocrine pathway. Which of the following is the most accurate description of its direct molecular mechanism?",
        "option_a": "Direct agonism at the GLP-1 receptor on pancreatic beta cells",
        "option_b": "Inhibition of sodium-glucose cotransporter-2 (SGLT2) in the kidney",
        "option_c": "Activation of AMP-activated protein kinase (AMPK) in the liver",
        "option_d": "Competitive inhibition of the enzyme dipeptidyl peptidase-4 (DPP-4)",
        "option_e": "Inhibition of alpha-glucosidase in the intestinal brush border",
        "correct_answer": "D",
        "explanation": "Sitagliptin is a DPP-4 inhibitor. DPP-4 rapidly degrades endogenous incretin hormones (GLP-1 and GIP). By inhibiting DPP-4, sitagliptin prolongs their half-life, enhancing glucose-dependent insulin secretion.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 28-year-old woman experiences severe postpartum hemorrhage immediately following a vaginal delivery. The obstetrician administers a continuous intravenous infusion of a nonapeptide hormone that strongly contracts the uterine myometrium. The intracellular signaling cascade initiated by this hormone involves activation of:",
        "option_a": "Adenylyl cyclase and an increase in intracellular cAMP",
        "option_b": "Guanylyl cyclase and an increase in intracellular cGMP",
        "option_c": "Tyrosine kinase and autophosphorylation of receptor dimers",
        "option_d": "Phospholipase C and an increase in IP3 and DAG",
        "option_e": "JAK-STAT pathway and altered specific gene transcription",
        "correct_answer": "D",
        "explanation": "Oxytocin is a posterior pituitary hormone used to control postpartum hemorrhage. It binds to Gq-protein coupled receptors on the myometrium, stimulating phospholipase C, leading to the generation of IP3 and DAG, increasing calcium and causing contraction.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 45-year-old woman presents with central obesity, moon facies, and purple striae. A low-dose dexamethasone suppression test is performed, and her morning serum cortisol remains elevated. A high-dose dexamethasone suppression test is then performed, and her cortisol levels are completely suppressed by >50%. The diagnostic utility of dexamethasone in this scenario relies on its ability to:",
        "option_a": "Stimulate ectopic CRH production from occult tumor cells",
        "option_b": "Block the peripheral conversion of cortisone to active cortisol",
        "option_c": "Directly inhibit adrenal cortex steroidogenesis enzymes downstream of cholesterol",
        "option_d": "Provide potent negative feedback on the anterior pituitary corticotrophs",
        "option_e": "Compete with cortisol at the glucocorticoid receptor in peripheral tissues",
        "correct_answer": "D",
        "explanation": "Dexamethasone is a potent synthetic glucocorticoid that exerts negative feedback on the anterior pituitary. In Cushing's disease (pituitary adenoma), the adenoma is resistant to low-dose feedback but will suppress ACTH in response to high-dose dexamethasone.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 14-year-old boy is diagnosed with central precocious puberty. He is initiated on a synthetic peptide analog of gonadotropin-releasing hormone (GnRH). After a few weeks of treatment, his gonadotropin levels are markedly reduced. The sustained therapeutic effect of this medication relies upon which of the following pharmacokinetic properties?",
        "option_a": "Rapid pulsatile release identical to endogenous GnRH",
        "option_b": "Irreversible covalent binding to the GnRH receptor complex",
        "option_c": "Rapid degradation by plasma proteases preventing receptor recycling",
        "option_d": "Continuous non-pulsatile stimulation leading to GnRH receptor downregulation",
        "option_e": "Competitive antagonism directly blocking endogenous GnRH binding",
        "correct_answer": "D",
        "explanation": "Leuprolide and other GnRH agonists, when administered continuously, initially stimulate the pituitary but rapidly cause downregulation and desensitization of GnRH receptors, resulting in profound suppression of FSH and LH.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 60-year-old man with end-stage renal disease is noted to have severe hyperphosphatemia despite strict dietary restrictions. He is prescribed a non-absorbable synthetic polymer to take with meals. The drug binds dietary phosphate in the gut, exchanging it for chloride or carbonate. Which of the following drugs fits this description?",
        "option_a": "Calcium carbonate",
        "option_b": "Ergocalciferol",
        "option_c": "Cinacalcet",
        "option_d": "Sevelamer",
        "option_e": "Calcitriol",
        "correct_answer": "D",
        "explanation": "Sevelamer is a non-absorbable phosphate-binding polymer used in patients with CKD. It lacks calcium or aluminum, reducing the risk of hypercalcemia or aluminum toxicity while effectively binding dietary phosphate.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 28-year-old woman with type 1 diabetes mellitus struggles with severe postprandial hyperglycemic spikes despite optimal insulin titration. Her endocrinologist adds a synthetic analog of a beta-cell hormone given via subcutaneous injection before meals. This added medication acts to lower postprandial glucose primarily by:",
        "option_a": "Increasing skeletal muscle glucose uptake independent of insulin action",
        "option_b": "Stimulating further insulin release from the remaining functioning beta cells",
        "option_c": "Inhibiting sodium-glucose cotransporter-2 (SGLT2) in the proximal tubule",
        "option_d": "Slowing gastric emptying and suppressing glucagon secretion",
        "option_e": "Decreasing hepatic insulin clearance to prolong exogenous insulin half-life",
        "correct_answer": "D",
        "explanation": "Pramlintide is a synthetic analog of amylin, co-secreted with insulin by beta cells. It acts centrally to delay gastric emptying, suppress postprandial glucagon secretion, and promote satiety.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 6-year-old girl with a 45,X karyotype (Turner syndrome) is noted to have severe short stature. She is initiated on a daily subcutaneous injection of a recombinant hormone. The primary mediator of this hormone's linear growth-promoting effect on the epiphyseal plates is synthesized mainly in the:",
        "option_a": "Anterior pituitary gland",
        "option_b": "Thyroid gland",
        "option_c": "Adrenal cortex",
        "option_d": "Liver",
        "option_e": "Kidneys",
        "correct_answer": "D",
        "explanation": "Somatropin (recombinant human growth hormone) primarily stimulates linear growth by inducing the synthesis and release of Insulin-like Growth Factor 1 (IGF-1), which is predominantly produced in the liver.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 50-year-old woman with hormone receptor-positive metastatic breast cancer is treated with an agent that blocks the conversion of cholesterol to pregnenolone. Because this drug profoundly suppresses the synthesis of all adrenal steroids, she must be supplemented with hydrocortisone. The drug described is:",
        "option_a": "Ketoconazole",
        "option_b": "Metyrapone",
        "option_c": "Mitotane",
        "option_d": "Aminoglutethimide",
        "option_e": "Fludrocortisone",
        "correct_answer": "D",
        "explanation": "Aminoglutethimide inhibits cholesterol desmolase (CYP11A1), the enzyme that catalyzes the first and rate-limiting step in all steroid hormone synthesis (conversion of cholesterol to pregnenolone).",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 65-year-old man presents to the emergency department with severe, crushing chest pain. He is diagnosed with an acute myocardial infarction and administered sublingual nitroglycerin. However, the patient quickly develops profound and refractory hypotension. Upon further questioning, the patient admits to taking a medication for erectile dysfunction 12 hours ago. The severe drug interaction observed is a result of synergistic accumulation of which intracellular messenger?",
        "option_a": "cAMP",
        "option_b": "Intracellular Calcium",
        "option_c": "Inositol triphosphate (IP3)",
        "option_d": "cGMP",
        "option_e": "Diacylglycerol (DAG)",
        "correct_answer": "D",
        "explanation": "PDE5 inhibitors (like sildenafil) prevent the degradation of cGMP. Nitroglycerin stimulates guanylyl cyclase to produce massive amounts of cGMP. Co-administration leads to a synergistic, potentially fatal accumulation of cGMP, causing massive vasodilation.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    }
]

qE = [
    {
        "question": "A 32-year-old pregnant woman presents in her first trimester with severe palpitations, heat intolerance, and weight loss. She is diagnosed with Graves' disease. The physician selects propylthiouracil (PTU) over methimazole. The preference for PTU during this specific period of pregnancy is primarily due to methimazole's association with which of the following teratogenic effects?",
        "option_a": "Ebstein's anomaly of the tricuspid valve",
        "option_b": "Neural tube defects such as spina bifida",
        "option_c": "Phocomelia and limb hypoplasia",
        "option_d": "Renal agenesis leading to Potter sequence",
        "option_e": "Aplasia cutis congenita on the fetal scalp",
        "correct_answer": "E",
        "explanation": "Methimazole is generally preferred over PTU due to a lower risk of hepatotoxicity, EXCEPT in the first trimester. Methimazole is a teratogen associated with aplasia cutis congenita (congenital focal absence of skin) and choanal atresia.",
        "source_context": "Endocrine Pharmacology - Thyroid"
    },
    {
        "question": "A 48-year-old man with type 2 diabetes and a highly irregular eating schedule experiences frequent hypoglycemic episodes on a sulfonylurea. He is switched to an oral insulin secretagogue with a very rapid onset and short duration of action, allowing him to take it strictly with meals and skip it if a meal is missed. The new medication belongs to which of the following drug classes?",
        "option_a": "Biguanides",
        "option_b": "Thiazolidinediones",
        "option_c": "Alpha-glucosidase inhibitors",
        "option_d": "Dipeptidyl peptidase-4 (DPP-4) inhibitors",
        "option_e": "Meglitinides",
        "correct_answer": "E",
        "explanation": "Repaglinide and nateglinide are meglitinides. They bind to the same K-ATP channel as sulfonylureas but have a very rapid onset and short half-life, making them ideal for targeting postprandial glucose spikes in patients with irregular eating.",
        "source_context": "Endocrine Pharmacology - Antidiabetics"
    },
    {
        "question": "A 55-year-old man with small cell lung cancer develops confusion and lethargy. Laboratory evaluation reveals a serum sodium of 115 mEq/L and high urine osmolality, consistent with the Syndrome of Inappropriate Antidiuretic Hormone (SIADH). Fluid restriction is ineffective, and he is started on an oral tetracycline derivative that induces nephrogenic diabetes insipidus as its primary therapeutic mechanism. Which of the following is the prescribed drug?",
        "option_a": "Doxycycline",
        "option_b": "Minocycline",
        "option_c": "Tigecycline",
        "option_d": "Tetracycline",
        "option_e": "Demeclocycline",
        "correct_answer": "E",
        "explanation": "Demeclocycline is a tetracycline antibiotic utilized off-label for the treatment of SIADH. It interferes with the intracellular cascade downstream of the vasopressin V2 receptor in the collecting duct, inducing nephrogenic diabetes insipidus.",
        "source_context": "Endocrine Pharmacology - Pituitary"
    },
    {
        "question": "A 45-year-old man with inoperable adrenocortical carcinoma is treated with an oral chemotherapeutic agent structurally related to the insecticide DDT. The drug causes selective destruction of the zona fasciculata and zona reticularis of the adrenal cortex, sparing the zona glomerulosa. The patient often requires glucocorticoid replacement. The medication is most likely:",
        "option_a": "Ketoconazole",
        "option_b": "Metyrapone",
        "option_c": "Aminoglutethimide",
        "option_d": "Etomidate",
        "option_e": "Mitotane",
        "correct_answer": "E",
        "explanation": "Mitotane is an adrenolytic agent related to DDT. It causes selective necrosis of the adrenal cortex, severely impairing cortisol and androgen production, used as medical treatment for adrenocortical carcinoma.",
        "source_context": "Endocrine Pharmacology - Adrenal"
    },
    {
        "question": "A 30-year-old woman with severe endometriosis is treated with a synthetic androgenic steroid that has weak progestational and glucocorticoid activity. The drug effectively suppresses the pituitary-ovarian axis and directly inhibits endometrial tissue growth. A major limiting factor in its use is the development of hirsutism, acne, and deepening of the voice. Which of the following is the prescribed drug?",
        "option_a": "Desogestrel",
        "option_b": "Spironolactone",
        "option_c": "Flutamide",
        "option_d": "Finasteride",
        "option_e": "Danazol",
        "correct_answer": "E",
        "explanation": "Danazol is a synthetic androgen with weak progestational and glucocorticoid activity. It inhibits the mid-cycle LH/FSH surges. It is used in endometriosis but limited by significant androgenic side effects.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 70-year-old man with multiple myeloma presents to the emergency department with altered mental status and polyuria. His corrected serum calcium is profoundly elevated at 14.5 mg/dL. In addition to vigorous intravenous hydration, a hormone secreted by the parafollicular cells of the thyroid is administered for its rapid calcium-lowering effect. This hormone lowers serum calcium primarily by:",
        "option_a": "Increasing intestinal calcium absorption via enterocyte transcellular transport",
        "option_b": "Decreasing renal calcium excretion in the distal convoluted tubule",
        "option_c": "Stimulating 1-alpha-hydroxylase activity in the proximal convoluted tubule",
        "option_d": "Activating osteoclasts via RANKL-RANK interaction",
        "option_e": "Directly inhibiting osteoclastic bone resorption",
        "correct_answer": "E",
        "explanation": "Calcitonin is secreted by parafollicular C cells. In severe hypercalcemia, it is administered because it acts rapidly to lower serum calcium by directly binding to receptors on osteoclasts, profoundly inhibiting bone resorption.",
        "source_context": "Endocrine Pharmacology - Bone"
    },
    {
        "question": "A 3-year-old boy is brought to the ER after accidentally ingesting a handful of his grandfather's propranolol pills. He is profoundly bradycardic and hypotensive. Intravenous fluids and atropine are administered with no improvement. The physician orders a specific antidote that is a peptide hormone normally secreted by the alpha cells of the pancreas. This hormone overcomes the beta-blockade by:",
        "option_a": "Directly activating beta-1 adrenergic receptors independent of the blockade",
        "option_b": "Inhibiting phosphodiesterase, reducing cAMP breakdown in the myocardium",
        "option_c": "Activating the parasympathetic nervous system via vagal stimulation",
        "option_d": "Opening fast sodium channels on myocardial cell membranes",
        "option_e": "Activating adenylyl cyclase via a distinct Gs-coupled receptor",
        "correct_answer": "E",
        "explanation": "Glucagon is the antidote for profound beta-blocker overdose. It binds to its own specific Gs-coupled receptor on the myocardium, bypassing the blocked beta receptors, directly stimulating adenylyl cyclase, and increasing cAMP.",
        "source_context": "Endocrine Pharmacology - Antidiabetics/Toxicology"
    },
    {
        "question": "A 32-year-old woman is undergoing controlled ovarian hyperstimulation for in vitro fertilization (IVF). To prevent a premature LH surge that would cause early ovulation and ruin the cycle, she is administered a daily injection of a drug that acts as a competitive antagonist at GnRH receptors in the anterior pituitary. Which of the following drugs fits this description?",
        "option_a": "Leuprolide",
        "option_b": "Clomiphene",
        "option_c": "Letrozole",
        "option_d": "Goserelin",
        "option_e": "Ganirelix",
        "correct_answer": "E",
        "explanation": "Ganirelix and cetrorelix are GnRH receptor antagonists. They cause immediate competitive blockade of GnRH receptors without the initial flare seen with GnRH agonists, effectively preventing premature LH surges during IVF.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    },
    {
        "question": "A 68-year-old man with metastatic castration-resistant prostate cancer is treated with an oral medication that permanently blocks a key enzyme required for androgen synthesis in the testes, adrenal glands, and the tumor itself. Because it blocks 17-alpha-hydroxylase and C17,20-lyase, it shunts steroidogenesis towards mineralocorticoids, causing hypertension and hypokalemia. The drug described is:",
        "option_a": "Enzalutamide",
        "option_b": "Bicalutamide",
        "option_c": "Degarelix",
        "option_d": "Finasteride",
        "option_e": "Abiraterone",
        "correct_answer": "E",
        "explanation": "Abiraterone acetate is an irreversible inhibitor of CYP17A1 (17-alpha-hydroxylase/C17,20-lyase). It completely blocks androgen synthesis from all sources, shunting precursors to mineralocorticoids.",
        "source_context": "Endocrine Pharmacology - Adrenal/Reproductive"
    },
    {
        "question": "A 55-year-old man is seeking treatment for erectile dysfunction. He prefers a medication that allows for spontaneous sexual activity over the weekend without needing to time the pill strictly before intercourse. He is prescribed a PDE5 inhibitor known for its exceptionally long half-life (up to 36 hours). Which of the following is the prescribed medication?",
        "option_a": "Sildenafil",
        "option_b": "Vardenafil",
        "option_c": "Avanafil",
        "option_d": "Alprostadil",
        "option_e": "Tadalafil",
        "correct_answer": "E",
        "explanation": "Tadalafil is a PDE5 inhibitor known as the 'weekend pill' due to its long half-life of 17.5 hours, allowing for a duration of action up to 36 hours, unlike sildenafil or vardenafil which last ~4 hours.",
        "source_context": "Endocrine Pharmacology - Reproductive"
    }
]

all_mcqs = qA + qB + qC + qD + qE

output_path = r"E:\USAMA\MBBS Books\MCQ_Generator\batches\bank_batch_endo_pharm.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_mcqs, f, indent=2)

print(f"Successfully generated {len(all_mcqs)} MCQs and saved to {output_path}")
