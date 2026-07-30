import json
import random
import os

raw_mcqs = [
    {
        "q": "A 54-year-old woman presents with nephrotic-range proteinuria and hematuria. Renal biopsy reveals expanded mesangium with randomly oriented fibrils measuring 20 nm in diameter on electron microscopy. These deposits are Congo red negative. Which of the following immunohistochemical markers is most specific for this condition?",
        "c": "DNAJB9",
        "w": ["Phospholipase A2 receptor", "Thrombospondin type-1 domain-containing 7A", "C3 nephritic factor", "Factor H"],
        "exp": "Fibrillary glomerulonephritis is characterized by randomly arranged non-amyloid fibrils (10-30 nm) that are Congo red negative. DNAJB9 is a highly sensitive and specific immunohistochemical marker for this disease."
    },
    {
        "q": "A 22-year-old man with no prior history of liver disease is found to have a large hepatic mass. Biopsy shows large polygonal cells with deeply eosinophilic cytoplasm separated by dense collagen bands. What is the characteristic genetic alteration associated with this neoplasm?",
        "c": "DNAJB1-PRKACA fusion",
        "w": ["CTNNB1 (beta-catenin) mutation", "HNF1A biallelic inactivation", "TERT promoter mutation", "IDH1/2 mutation"],
        "exp": "Fibrolamellar hepatocellular carcinoma typically affects young patients without underlying cirrhosis. The characteristic genetic signature is an in-frame fusion of DNAJB1 and PRKACA."
    },
    {
        "q": "A 14-year-old girl is found to have a well-circumscribed tail mass in her pancreas. Histology shows solid and pseudopapillary architectural patterns with uniform cells and cholesterol clefts. Which of the following mutations is predominantly driving this neoplasm?",
        "c": "CTNNB1",
        "w": ["KRAS", "SMAD4", "CDKN2A", "VHL"],
        "exp": "Solid pseudopapillary neoplasms of the pancreas characteristically harbor somatic mutations in CTNNB1 (beta-catenin), leading to aberrant nuclear localization of beta-catenin. They rarely have the KRAS or SMAD4 mutations seen in ductal adenocarcinoma."
    },
    {
        "q": "A 28-year-old woman presents with painless gross hematuria. A nephrectomy is performed for a polar mass. The tumor shows papillary architecture with clear cells. Immunohistochemistry demonstrates strong nuclear expression of TFE3. This tumor is characterized by a translocation involving which chromosome?",
        "c": "Chromosome Xp11.2",
        "w": ["Chromosome 3p25", "Chromosome 7q31", "Chromosome 11p13", "Chromosome 17p13"],
        "exp": "Xp11 translocation renal cell carcinomas involve the TFE3 gene on chromosome Xp11.2. They predominantly affect young adults and children, often presenting with papillary architecture and clear to eosinophilic cells."
    },
    {
        "q": "A 65-year-old man presents with a slow-growing testicular mass. Orchiectomy reveals a tumor composed of three cell types: small lymphocyte-like cells, intermediate cells, and giant multinucleated cells. There is no evidence of germ cell neoplasia in situ (GCNIS) in the adjacent parenchyma. Which genetic abnormality is often implicated?",
        "c": "FGFR3 amplification",
        "w": ["Isochromosome 12p", "KIT mutation", "OCT3/4 amplification", "PLAP overexpression"],
        "exp": "Spermatocytic tumors affect older men, consist of a triad of cell sizes, and lack association with GCNIS. They do not have i(12p), but often harbor activating mutations or amplification of FGFR3."
    },
    {
        "q": "A 42-year-old woman undergoes resection of a 10 cm unilateral ovarian mass. Microscopic examination reveals small, uniform cells with grooved nuclei arranged in microfollicular patterns around eosinophilic fluid spaces. Which of the following molecular findings is virtually pathognomonic for this adult-type tumor?",
        "c": "FOXL2 c.402C>G (p.C134W) mutation",
        "w": ["DICER1 mutation", "STK11 mutation", "BRCA1 mutation", "SMARCA4 loss"],
        "exp": "Adult granulosa cell tumors show Call-Exner bodies and grooved nuclei. More than 95% of adult cases harbor a somatic missense mutation in the FOXL2 gene (C134W)."
    },
    {
        "q": "A 35-year-old man develops a deep-seated mass in the thigh. Histopathology shows a biphasic tumor with both epithelial-like glands and spindle cells. Immunohistochemistry is positive for TLE1. Which chromosomal translocation is diagnostic?",
        "c": "t(X;18)(p11;q11)",
        "w": ["t(11;22)(q24;q12)", "t(12;16)(q13;p11)", "t(2;13)(q35;q14)", "t(17;22)(q22;q13)"],
        "exp": "Synovial sarcoma is characterized by the t(X;18)(p11;q11) translocation, resulting in the SYT-SSX fusion gene. TLE1 is a useful immunohistochemical marker."
    },
    {
        "q": "A 12-year-old boy presents with a slow-growing, painless mass in the parotid gland. Histology shows a lobulated tumor with microcystic and solid patterns containing eosinophilic secretory material positive for S100 and mammaglobin. What genetic translocation is associated with this tumor?",
        "c": "ETV6-NTRK3",
        "w": ["MYB-NFIB", "CRTC1-MAML2", "PLAG1 rearrangement", "HMGA2 rearrangement"],
        "exp": "Mammary analogue secretory carcinoma (MASC) of the salivary gland shares morphological and genetic features with secretory carcinoma of the breast, characteristically harboring the ETV6-NTRK3 fusion."
    },
    {
        "q": "A 45-year-old woman is incidentally found to have multiple small, firm hepatic nodules. Biopsy reveals chords of epithelioid cells in a myxohyaline stroma. The cells express CD31 and CD34. Which genetic fusion is most characteristic of this vascular neoplasm?",
        "c": "WWTR1-CAMTA1",
        "w": ["YAP1-TFE3", "COL1A1-PDGFB", "EWSR1-FLI1", "ASPSCR1-TFE3"],
        "exp": "Epithelioid hemangioendothelioma is an intermediate-grade vascular tumor that characteristically features the WWTR1-CAMTA1 fusion."
    },
    {
        "q": "A 38-year-old man presents with a protuberant, nodular skin mass on his trunk. It has been slowly enlarging over years. Histology demonstrates a highly cellular spindle cell tumor in a storiform pattern, infiltrating the subcutaneous fat in a honeycomb pattern. It is CD34 positive. Which chromosomal alteration is typical?",
        "c": "t(17;22)",
        "w": ["t(11;22)", "t(12;16)", "t(9;22)", "t(2;13)"],
        "exp": "Dermatofibrosarcoma protuberans (DFSP) is driven by t(17;22), fusing COL1A1 to PDGFB, leading to autocrine activation of the PDGF receptor."
    },
    {
        "q": "A 29-year-old woman notices a rapidly growing, tender mass on her forearm over the last three weeks. Biopsy reveals a tissue culture-like proliferation of plump spindle cells with extravasated red blood cells and frequent, but typical, mitoses. What genetic rearrangement is defining for this self-limiting lesion?",
        "c": "MYH9-USP6",
        "w": ["EWSR1-NR4A3", "PAX3-FOXO1", "FUS-DDIT3", "SS18-SSX1"],
        "exp": "Nodular fasciitis is a benign, self-limiting clonal myofibroblastic proliferation typically harboring a MYH9-USP6 gene fusion, proving it is a transient neoplasm rather than purely reactive."
    },
    {
        "q": "A 7-year-old child presents with cranial nerve palsies and ataxia. MRI reveals an infiltrative tumor centered in the pons. Biopsy shows a diffuse astrocytic proliferation. Which specific mutation characterizes this highly aggressive midline glioma?",
        "c": "H3 K27M",
        "w": ["IDH1 R132H", "BRAF V600E", "EGFRvIII", "TERT promoter"],
        "exp": "Diffuse midline gliomas (such as Diffuse Intrinsic Pontine Glioma) often harbor the H3 K27M mutation, which leads to global reduction in H3K27 trimethylation and a dismal prognosis."
    },
    {
        "q": "A 62-year-old man with a primary gastric stromal tumor undergoes genotyping of the tumor before starting targeted therapy. The tumor is found to harbor a PDGFRA D842V mutation. Which of the following describes the likely clinical implication?",
        "c": "Primary resistance to imatinib therapy",
        "w": ["Exceptional sensitivity to imatinib", "High likelihood of malignant transformation", "Association with Carney triad", "Lack of expression of DOG1"],
        "exp": "GISTs with PDGFRA D842V mutations are notoriously resistant to standard tyrosine kinase inhibitors like imatinib, often requiring alternate therapies like avapritinib."
    },
    {
        "q": "A 72-year-old man presents with a rapidly growing erythematous nodule on his sun-exposed scalp. Biopsy shows sheets of small round blue cells in the dermis. Immunohistochemistry demonstrates perinuclear dot-like positivity for Cytokeratin 20 (CK20). What infectious agent is implicated in the pathogenesis?",
        "c": "Merkel cell polyomavirus",
        "w": ["Human papillomavirus 16", "Epstein-Barr virus", "Human herpesvirus 8", "Cytomegalovirus"],
        "exp": "Merkel cell carcinoma is an aggressive neuroendocrine carcinoma of the skin. The majority of cases are driven by Merkel cell polyomavirus (MCPyV). Characteristic IHC includes dot-like CK20 positivity."
    },
    {
        "q": "A 50-year-old woman undergoes core needle biopsy for a breast mass. The pathology report describes an infiltrative proliferation of small, round glands with open lumina containing eosinophilic secretions, entirely lacking a myoepithelial cell layer. The cells are triple-negative (ER/PR/HER2 negative) but strongly express S100. What is the diagnosis?",
        "c": "Microglandular adenosis",
        "w": ["Tubular carcinoma", "Adenoid cystic carcinoma", "Sclerosing adenosis", "Secretory carcinoma"],
        "exp": "Microglandular adenosis is a rare, benign breast lesion that uniquely lacks a myoepithelial layer, mimicking carcinoma. It is typically triple-negative and S-100 positive, differentiating it from tubular carcinoma."
    },
    {
        "q": "A 16-year-old boy presents with knee pain. X-ray shows an eccentric, lytic lesion in the epiphysis of the distal femur. Biopsy reveals mononuclear cells with longitudinal nuclear grooves and scattered osteoclast-like giant cells. A characteristic chicken-wire calcification pattern is seen. Which mutation is most likely present?",
        "c": "H3F3A K36M",
        "w": ["H3F3A G34W", "GNAS1", "EXT1/EXT2", "RUNX2"],
        "exp": "Chondroblastoma is a benign cartilaginous tumor typically arising in the epiphysis. It is defined by mutations in histone H3.3 (H3F3A or H3F3B), specifically the K36M mutation."
    },
    {
        "q": "A 32-year-old woman presents with pain and swelling around her knee. Imaging shows an expansile, purely lytic lesion in the epiphysis and metaphysis of the proximal tibia. Histology shows numerous uniformly distributed osteoclast-like giant cells in a background of mononuclear cells. Which mutation drives the neoplastic mononuclear cells?",
        "c": "H3F3A G34W",
        "w": ["H3F3A K36M", "MDM2 amplification", "CTNNB1", "USP6 rearrangement"],
        "exp": "Giant cell tumors of bone typically occur in adults (closed epiphyses) and are driven by H3F3A G34W mutations in the mononuclear stromal cell component."
    },
    {
        "q": "A 60-year-old woman undergoes hysterectomy for abnormal uterine bleeding. The tumor consists of tubular and glandular structures with dense eosinophilic secretions in the lumina, mimicking cervical mesonephric rests. It occurs in the uterine corpus. Which molecular alterations are characteristic?",
        "c": "KRAS mutation and GATA3 expression",
        "w": ["PTEN mutation and PAX2 loss", "TP53 mutation and p16 block positivity", "POLE mutation and MMR deficiency", "CTNNB1 mutation and LEF1 expression"],
        "exp": "Mesonephric-like adenocarcinoma of the endometrium is a distinct entity showing mesonephric morphology, KRAS mutations, and positivity for GATA3 and TTF1, differentiating it from usual endometrioid carcinomas."
    },
    {
        "q": "A 58-year-old woman has a 2 cm solid mass in her breast. Biopsy reveals follicles lined by columnar cells with abundant eosinophilic cytoplasm and nuclei located at the apical pole (reversed polarity). What specific mutation characterizes this rare breast tumor type?",
        "c": "IDH2 mutation",
        "w": ["PIK3CA mutation", "BRCA1 mutation", "GATA3 mutation", "E-cadherin loss"],
        "exp": "Tall cell carcinoma with reversed polarity (formerly solid papillary carcinoma with reversed polarity) is a rare breast tumor characterized by IDH2 hot spot mutations."
    },
    {
        "q": "A 40-year-old man undergoes thyroidectomy for a 3 cm encapsulated follicular-patterned nodule. The cells exhibit nuclear clearing, grooves, and pseudoinclusions. The tumor is completely surrounded by a capsule with no capsular or vascular invasion. Which genetic alteration is most closely associated with this entity?",
        "c": "RAS mutation",
        "w": ["BRAF V600E mutation", "RET/PTC rearrangement", "PAX8-PPARg rearrangement", "TERT promoter mutation"],
        "exp": "Non-invasive follicular thyroid neoplasm with papillary-like nuclear features (NIFTP) typically harbors RAS mutations, unlike conventional papillary thyroid carcinoma which predominantly has BRAF V600E mutations."
    },
    {
        "q": "A 68-year-old Hispanic man presents with progressive chronic kidney disease. A renal biopsy shows prominent mesangial amorphous deposits that are Congo red positive with apple-green birefringence. Immunohistochemistry for immunoglobulins, kappa, lambda, and serum amyloid A are negative. Mass spectrometry is most likely to identify which protein?",
        "c": "Leukocyte cell-derived chemotaxin-2 (ALECT2)",
        "w": ["Beta-2 microglobulin", "Transthyretin", "Apolipoprotein A-I", "Fibrinogen A alpha chain"],
        "exp": "ALECT2 amyloidosis is an increasingly recognized form of renal amyloidosis, particularly common in individuals of Hispanic/Latino descent. It frequently presents with CKD and prominent cortical interstitial and mesangial deposits."
    },
    {
        "q": "A 28-year-old man presents with progressive lower back pain and saddle anesthesia. MRI reveals an enhancing intradural, extramedullary mass at the filum terminale. Microscopic examination demonstrates cuboidal cells arranged radially around vascular cores in a myxoid background. Which immunohistochemical marker is characteristically positive?",
        "c": "GFAP",
        "w": ["Cytokeratin 20", "CD45", "Synaptophysin", "EMA (dot-like)"],
        "exp": "Myxopapillary ependymomas characteristically occur in the conus medullaris/filum terminale region. Unlike some other tumors in this location, they strongly express GFAP (Glial Fibrillary Acidic Protein) due to their ependymal origin."
    },
    {
        "q": "A 72-year-old man presents with widespread purplish skin nodules and pancytopenia. Skin biopsy shows a diffuse, non-epidermotropic infiltrate of medium-sized mononuclear cells. The cells are positive for CD4, CD56, CD123, and TCL1, but negative for CD3 and CD20. What is the diagnosis?",
        "c": "Blastic plasmacytoid dendritic cell neoplasm",
        "w": ["Extranodal NK/T-cell lymphoma", "Mycosis fungoides", "Acute myeloid leukemia (myelomonocytic)", "Primary cutaneous follicle center lymphoma"],
        "exp": "BPDCN is an aggressive hematologic malignancy originating from precursors of plasmacytoid dendritic cells. The classical immunophenotype is CD4+, CD56+, and CD123+, with frequent skin involvement."
    },
    {
        "q": "A 25-year-old Asian woman presents with fever and cervical lymphadenopathy. Lymph node biopsy shows patchy areas of necrosis with abundant karyorrhectic debris and a proliferation of plasmacytoid dendritic cells and histiocytes. Neutrophils are notably absent. Which of the following characterizes this disease?",
        "c": "Kikuchi-Fujimoto disease",
        "w": ["Rosai-Dorfman disease", "Kimura disease", "Castleman disease", "Systemic lupus erythematosus"],
        "exp": "Kikuchi-Fujimoto disease (histiocytic necrotizing lymphadenitis) typically affects young Asian women. Histology shows karyorrhectic debris and plasmacytoid dendritic cells (CD123+) without neutrophils."
    },
    {
        "q": "A 50-year-old man undergoes splenectomy for massive splenomegaly and hypersplenism. Gross examination reveals a spongy spleen with numerous blood-filled cystic spaces. The lining cells are positive for CD31 and CD68 but negative for CD8. What is the diagnosis?",
        "c": "Littoral cell angioma",
        "w": ["Peliosis of the spleen", "Splenic hemangioma", "Splenic hamartoma", "Angiosarcoma"],
        "exp": "Littoral cell angioma is a primary vascular tumor of the spleen. The lining cells exhibit a hybrid endothelial/histiocytic phenotype (CD31+, CD68+) but lack the normal sinusoidal CD8 positivity."
    },
    {
        "q": "A 45-year-old woman with myasthenia gravis is found to have an anterior mediastinal mass. Biopsy shows a lobulated architecture with a predominant population of polygonal epithelial cells exhibiting mild atypia, admixed with a minor population of small lymphocytes. The lymphocytes are TdT positive. Which WHO classification type does this represent?",
        "c": "Type B3 thymoma",
        "w": ["Type A thymoma", "Type AB thymoma", "Type B1 thymoma", "Thymic carcinoma"],
        "exp": "Type B3 thymoma (atypical thymoma) is predominantly composed of neoplastic epithelial cells with mild atypia, and only a scarce number of immature T cells (thymocytes, TdT+)."
    },
    {
        "q": "A 38-year-old man with advanced HIV infection presents with heart failure. Echocardiography shows a massive, infiltrating mass in the right atrium. Biopsy reveals sheets of large lymphoid cells with prominent nucleoli. The cells are CD20+ and EBV-encoded RNA (EBER) positive. What is the diagnosis?",
        "c": "Primary cardiac diffuse large B-cell lymphoma",
        "w": ["Cardiac myxoma", "Cardiac rhabdomyoma", "Kaposi sarcoma", "Angiosarcoma"],
        "exp": "Primary cardiac lymphomas are extremely rare, predominantly occurring in immunocompromised patients (e.g., HIV). They are almost exclusively diffuse large B-cell lymphomas (DLBCL) driven by EBV."
    },
    {
        "q": "A 2-year-old boy presents with severe, intractable diarrhea and failure to thrive. Endoscopic biopsy of the small intestine shows villous atrophy and a massive infiltrate of lymphocytes, but an absence of goblet cells and Paneth cells. Genetic testing reveals a mutation in the FOXP3 gene. Which associated finding is most likely?",
        "c": "Anti-enterocyte antibodies",
        "w": ["Anti-tissue transglutaminase antibodies", "Anti-Saccharomyces cerevisiae antibodies (ASCA)", "Defective oxidative burst", "Absent germinal centers"],
        "exp": "FOXP3 mutations cause IPEX syndrome. The enteropathy is an autoimmune enteropathy characterized by anti-enterocyte antibodies and loss of goblet/Paneth cells."
    },
    {
        "q": "A 65-year-old woman presents with chronic watery, non-bloody diarrhea. Colonoscopy is visually unremarkable. However, biopsies from the right colon show a normal crypt architecture but an irregular, thickened eosinophilic band just below the surface epithelium measuring 20 micrometers, accompanied by increased intraepithelial lymphocytes. What is the diagnosis?",
        "c": "Collagenous colitis",
        "w": ["Lymphocytic colitis", "Crohn's disease", "Ulcerative colitis", "Ischemic colitis"],
        "exp": "Microscopic colitis has two main subtypes: lymphocytic and collagenous. Collagenous colitis is defined by a thickened subepithelial collagen band (>10 um) under normal-appearing mucosa, often presenting in older women with watery diarrhea."
    },
    {
        "q": "A 20-year-old man is found to have spotty skin pigmentation, a left atrial myxoma, and primary pigmented nodular adrenocortical disease causing Cushing syndrome. This familial syndrome is most commonly caused by an inactivating mutation in which of the following genes?",
        "c": "PRKAR1A",
        "w": ["MEN1", "RET", "VHL", "PTEN"],
        "exp": "Carney complex is an autosomal dominant multiple neoplasia syndrome characterized by skin lentigines, cardiac myxomas, and endocrine overactivity. It is caused by mutations in PRKAR1A (protein kinase A regulatory subunit 1 alpha)."
    },
    {
        "q": "A 22-year-old woman presents with a slow-growing mass in her right thigh. Biopsy shows large, polygonal cells with abundant eosinophilic, granular cytoplasm, arranged in nests separated by delicate vascular channels. PAS staining highlights intracytoplasmic crystalline inclusions. Which gene fusion is present?",
        "c": "ASPSCR1-TFE3",
        "w": ["SS18-SSX1", "EWSR1-ATF1", "PAX3-FOXO1", "MYH9-USP6"],
        "exp": "Alveolar soft part sarcoma typically affects young adults, showing large cells in an alveolar pattern with PAS+ crystals. It is defined by the ASPSCR1-TFE3 fusion."
    },
    {
        "q": "A 30-year-old man presents with a nodule deep in the aponeurosis of his foot. Histology reveals nests of uniform spindled-to-epithelioid cells separated by fibrous septa. The cells are positive for S100 and HMB-45, but there is no epidermal involvement. What genetic alteration is diagnostic?",
        "c": "EWSR1-ATF1",
        "w": ["BRAF V600E", "NRAS Q61R", "t(X;18)", "COL1A1-PDGFB"],
        "exp": "Clear cell sarcoma of soft parts (melanoma of soft parts) presents in deep tissues, expresses melanocytic markers, but lacks epidermal involvement and BRAF mutations. It is driven by the EWSR1-ATF1 fusion t(12;22)."
    },
    {
        "q": "A 25-year-old man presents with a hard, painless nodule on the volar aspect of his finger, initially misdiagnosed as a benign fibroma. It soon ulcerates. Histology shows a nodular proliferation of plump epithelioid cells with central necrosis, mimicking a granuloma. The cells co-express cytokeratin and CD34. Which molecular finding is characteristic?",
        "c": "Loss of INI1 (SMARCB1) expression",
        "w": ["CD117 (c-KIT) mutation", "t(X;18) translocation", "MYC amplification", "MDM2 amplification"],
        "exp": "Epithelioid sarcoma is a rare soft tissue sarcoma occurring in the distal extremities of young adults. It characteristically shows loss of nuclear INI1 (SMARCB1) expression and co-expresses keratins and vimentin."
    },
    {
        "q": "A 45-year-old woman undergoes resection of a submandibular gland tumor. Histology shows basaloid cells forming cribriform, tubular, and solid structures. Perineural invasion is prominent. This tumor is associated with a translocation involving which genes?",
        "c": "MYB-NFIB",
        "w": ["CRTC1-MAML2", "ETV6-NTRK3", "PLAG1", "HMGA2"],
        "exp": "Adenoid cystic carcinoma (ACC) of the salivary glands often harbors the t(6;9) translocation resulting in the MYB-NFIB fusion, which drives tumor progression."
    },
    {
        "q": "A 19-year-old man presents with a rapidly growing mass in the mediastinum. Biopsy shows an undifferentiated carcinoma with focal abrupt squamous differentiation. The tumor is extraordinarily aggressive and fatal within months. Immunohistochemistry shows diffuse nuclear positivity for NUT. Which gene is most commonly fused with NUTM1 in this entity?",
        "c": "BRD4",
        "w": ["EWSR1", "ETV6", "MYC", "ALK"],
        "exp": "NUT carcinoma (formerly NUT midline carcinoma) is an aggressive cancer defined by rearrangement of the NUTM1 gene, most commonly fusing with BRD4 (t(15;19))."
    },
    {
        "q": "A 55-year-old woman with a BRCA1 mutation undergoes a prophylactic salpingo-oophorectomy. Detailed examination of the fallopian tube fimbriae reveals a microscopic focus of atypical epithelial cells with loss of polarity and prominent nucleoli. There is no stromal invasion. Immunohistochemistry for which protein is most likely to show a diffuse, strong block staining pattern?",
        "c": "p53",
        "w": ["p16", "WT1", "ER", "HER2"],
        "exp": "Serous tubal intraepithelial carcinoma (STIC) is the precursor lesion for most high-grade serous ovarian carcinomas. STIC lesions universally harbor TP53 mutations, reflected as either diffuse strong positivity (missense) or complete absence (nonsense) on IHC."
    },
    {
        "q": "A 40-year-old man presents with severe hypertension, palpitations, and diaphoresis. Imaging reveals a 6 cm extra-adrenal retroperitoneal mass. Biopsy confirms a paraganglioma. Genetic testing is pursued due to a family history of similar tumors. Mutation in which of the following succinate dehydrogenase (SDH) subunits confers the highest risk for malignant transformation and metastasis?",
        "c": "SDHB",
        "w": ["SDHA", "SDHC", "SDHD", "SDHAF2"],
        "exp": "While mutations in any SDH complex gene can cause hereditary paraganglioma-pheochromocytoma syndromes, SDHB mutations are strongly associated with a high risk of malignancy and extra-adrenal location (B for Bad)."
    },
    {
        "q": "A 30-year-old male athlete suddenly collapses and dies during a marathon. Autopsy reveals extensive fibrofatty replacement of the right ventricular myocardium. Genetic analysis would most likely reveal a mutation in a gene encoding which of the following proteins?",
        "c": "Plakoglobin",
        "w": ["Beta-myosin heavy chain", "Cardiac troponin T", "Dystrophin", "Titin"],
        "exp": "Arrhythmogenic right ventricular cardiomyopathy (ARVC) is caused by mutations in desmosomal proteins, such as plakoglobin (Naxos disease), desmoplakin, or plakophilin-2, leading to fibrofatty replacement of the RV."
    },
    {
        "q": "A 4-month-old infant presents with a rapidly enlarging, purplish plaque on the thigh, accompanied by profound thrombocytopenia and a severe consumptive coagulopathy. Biopsy shows an infiltrative vascular proliferation of spindled endothelial cells forming slit-like vessels. What is the diagnosis?",
        "c": "Kaposiform hemangioendothelioma",
        "w": ["Infantile hemangioma", "Pyogenic granuloma", "Tufted angioma", "Angiosarcoma"],
        "exp": "Kaposiform hemangioendothelioma (and tufted angioma) are closely associated with Kasabach-Merritt phenomenon, a life-threatening consumptive coagulopathy and thrombocytopenia secondary to platelet trapping within the tumor."
    },
    {
        "q": "A 45-year-old woman is incidentally found to have a multilocular cystic mass in the tail of the pancreas. Resection reveals cysts lined by columnar mucin-producing cells. Immediately beneath the epithelium is a densely cellular spindle cell stroma. Which immunohistochemical markers would best confirm the nature of this characteristic stroma?",
        "c": "Estrogen and progesterone receptors",
        "w": ["CD34 and STAT6", "S100 and SOX10", "Chromogranin and Synaptophysin", "CK7 and CK20"],
        "exp": "Mucinous cystic neoplasms of the pancreas exclusively occur in women (mostly in the tail) and are defined by the presence of an ovarian-type subepithelial stroma, which expresses ER, PR, and inhibin."
    },
    {
        "q": "A 55-year-old man presents with progressive abdominal distension. Laparotomy reveals massive amounts of gelatinous ascites (jelly belly). Histological examination of the mucin reveals scanty, low-grade mucinous epithelial cells. Which of the following is the most likely primary source of this condition?",
        "c": "Appendix",
        "w": ["Pancreas", "Colon", "Stomach", "Gallbladder"],
        "exp": "Pseudomyxoma peritonei in both men and women is almost always derived from a mucinous neoplasm of the appendix (often low-grade appendiceal mucinous neoplasm, LAMN)."
    },
    {
        "q": "A 40-year-old woman presents with bloody nipple discharge. A subareolar mass is excised, revealing a complex arborizing papillary proliferation within a dilated duct. To definitively distinguish an intraductal papilloma from an encapsulated papillary carcinoma, immunohistochemistry should be directed against which cell type?",
        "c": "Myoepithelial cells",
        "w": ["Luminal epithelial cells", "Endothelial cells", "Fibroblasts", "Macrophages"],
        "exp": "The key histological feature distinguishing benign intraductal papilloma from papillary carcinoma is the presence of an intact myoepithelial cell layer within the papillary fibrovascular cores, highlighted by markers like p63, calponin, or smooth muscle myosin heavy chain."
    },
    {
        "q": "A 60-year-old man undergoes nephrectomy for a multifocal, bilateral renal tumor. Histology shows papillae lined by cells with scant cytoplasm and low-grade nuclei, accompanied by foamy macrophages in the fibrovascular cores. Genetic analysis reveals a germline mutation. Which gene is most likely implicated?",
        "c": "MET",
        "w": ["VHL", "FLCN", "FH", "BAP1"],
        "exp": "Hereditary papillary renal cell carcinoma (Type 1) is an autosomal dominant syndrome caused by activating mutations in the MET proto-oncogene on chromosome 7q."
    },
    {
        "q": "A 55-year-old woman undergoes resection of a well-circumscribed, mahogany-brown renal mass with a central stellate scar. The tumor cells are large with prominent cell membranes, pale eosinophilic cytoplasm, and perinuclear halos. Hale colloidal iron stain shows diffuse, strong cytoplasmic positivity. What cytogenetic abnormality is characteristic?",
        "c": "Multiple chromosome losses (hypodiploidy)",
        "w": ["Deletion of chromosome 3p", "Trisomy 7 and 17", "Translocation t(X;1)(p11.2;q21)", "Amplification of 1q"],
        "exp": "Chromophobe renal cell carcinoma is characterized by multiple whole-chromosome losses (hypodiploidy, involving 1, 2, 6, 10, 13, 17, 21). They are Hale colloidal iron positive, distinguishing them from oncocytomas."
    },
    {
        "q": "A 28-year-old man presents with gynecomastia and a palpable testicular mass. Orchiectomy reveals a well-circumscribed, solid, golden-brown tumor. Microscopic examination shows uniform polygonal cells with abundant eosinophilic cytoplasm. Scattered rod-shaped crystalloids are seen in the cytoplasm. What is the diagnosis?",
        "c": "Leydig cell tumor",
        "w": ["Sertoli cell tumor", "Seminoma", "Yolk sac tumor", "Choriocarcinoma"],
        "exp": "Leydig cell tumors produce androgens and/or estrogens (causing gynecomastia). The pathognomonic histological feature, present in about 25-30% of cases, is the presence of Reinke crystals (rod-shaped intracytoplasmic inclusions)."
    },
    {
        "q": "A 3-year-old boy presents with an enlarged testicle. Serum alpha-fetoprotein (AFP) is significantly elevated. Orchiectomy reveals a tumor with a reticular, microcystic pattern and occasional glomeruloid structures with a central blood vessel. Which immunohistochemical marker, aside from AFP, is highly sensitive and specific for this neoplasm?",
        "c": "Glypican-3",
        "w": ["PLAP", "OCT3/4", "CD30", "hCG"],
        "exp": "Yolk sac tumor (endodermal sinus tumor) features Schiller-Duval bodies. It is characteristically positive for AFP and Glypican-3."
    },
    {
        "q": "A 35-year-old woman undergoes cystectomy for an ovarian mass. Pathology demonstrates hierarchical branching papillae with stratified serous epithelium, mild nuclear atypia, and no destructive stromal invasion. Which genetic mutations are most frequently implicated in the pathogenesis of this specific tumor?",
        "c": "KRAS and BRAF",
        "w": ["TP53 and BRCA1", "PTEN and ARID1A", "FOXL2 and DICER1", "CTNNB1 and MMR genes"],
        "exp": "Serous borderline tumors (and low-grade serous carcinomas) arise via the low-grade pathway and frequently harbor mutations in KRAS, BRAF, or ERBB2, in contrast to high-grade serous carcinomas which universally have TP53 mutations."
    },
    {
        "q": "A 45-year-old woman with a history of endometriosis presents with a cystic ovarian mass. Histology shows tubules and cysts lined by cells with abundant clear cytoplasm and hobnail nuclei protruding into the lumina. Which gene mutation is highly characteristic of this malignancy?",
        "c": "ARID1A",
        "w": ["BRCA2", "WT1", "STK11", "SMARCA4"],
        "exp": "Clear cell carcinoma of the ovary is strongly associated with endometriosis. It frequently harbors somatic mutations in ARID1A (a SWI/SNF chromatin remodeling gene) and PIK3CA."
    },
    {
        "q": "A 35-year-old man is diagnosed with a thyroid nodule. Fine needle aspiration shows loosely cohesive plasmacytoid cells with eccentric nuclei and salt-and-pepper chromatin. A Congo red stain on the cell block shows apple-green birefringence. Prophylactic thyroidectomy of his children may be indicated if a mutation is found in which gene?",
        "c": "RET",
        "w": ["BRAF", "RAS", "APC", "PTEN"],
        "exp": "The presentation is classic for medullary thyroid carcinoma (calcitonin-producing C cells, amyloid stroma). Germline RET mutations cause MEN2 syndromes, often prompting prophylactic thyroidectomy in relatives."
    },
    {
        "q": "A 78-year-old woman with a long-standing history of a multinodular goiter presents with a rapidly enlarging neck mass, hoarseness, and dysphagia. Biopsy shows highly pleomorphic giant cells, spindle cells, and extensive necrosis. Which genetic alteration, in addition to BRAF or RAS, is typically required for this transformation?",
        "c": "TP53",
        "w": ["RET/PTC", "PAX8/PPARg", "MEN1", "TSHR"],
        "exp": "Anaplastic thyroid carcinoma is a highly aggressive malignancy that often arises from dedifferentiation of a pre-existing well-differentiated thyroid carcinoma. This dedifferentiation is typically driven by late mutations in TP53 and/or the TERT promoter."
    }
]

# Ensure EXACTLY 50 MCQs.
# We will use exactly 50 and distribute correct answers precisely 10 times for each of A, B, C, D, E
assert len(raw_mcqs) == 50, "Must be exactly 50 MCQs."

random.seed(1337)
correct_positions = ['A']*10 + ['B']*10 + ['C']*10 + ['D']*10 + ['E']*10
random.shuffle(correct_positions)
random.shuffle(raw_mcqs)

output_mcqs = []
for i, mcq in enumerate(raw_mcqs):
    correct_letter = correct_positions[i]
    c_text = mcq['c']
    w_texts = mcq['w']
    random.shuffle(w_texts)
    
    options = [""] * 5
    correct_idx = ord(correct_letter) - ord('A')
    options[correct_idx] = c_text
    
    w_idx = 0
    for j in range(5):
        if j != correct_idx:
            options[j] = w_texts[w_idx]
            w_idx += 1
            
    output_mcqs.append({
        "question": mcq['q'],
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "option_e": options[4],
        "correct_answer": correct_letter,
        "explanation": mcq['exp'],
        "source_context": "Systemic Pathology - Advanced Molecular/Genetics"
    })

out_dir = r"E:\USAMA\MBBS Books\MCQ_Generator\batches"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "bank_batch_syspath.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output_mcqs, f, indent=2)

print(f"Successfully wrote {len(output_mcqs)} MCQs to {out_path}")
