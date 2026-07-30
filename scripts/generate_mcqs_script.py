import json
import os

mcqs = []

# A answers (1-10)
mcqs.extend([
  {
    "question": "A 45-year-old man presents with severe epigastric pain, weight loss, and generalized edema. Endoscopy shows massively enlarged gastric rugae in the body and fundus, sparing the antrum. A biopsy reveals marked foveolar hyperplasia with cystic dilatation. Which of the following molecular abnormalities is most directly responsible for the pathogenesis of this patient's condition?",
    "option_a": "Overexpression of transforming growth factor-alpha (TGF-alpha)",
    "option_b": "Inactivating mutation of the CDH1 (E-cadherin) gene",
    "option_c": "Activating mutation in the KIT receptor tyrosine kinase",
    "option_d": "Hypersecretion of gastrin from a pancreatic neuroendocrine tumor",
    "option_e": "Autoimmune destruction of H+/K+ ATPase",
    "correct_answer": "A",
    "explanation": "Menetrier disease is characterized by massive foveolar hyperplasia and protein-losing enteropathy. Pathogenesis is linked to TGF-alpha overexpression binding to EGFR.",
    "source_context": "GI Pathology - Menetrier Disease"
  },
  {
    "question": "A 32-year-old woman with a history of recurrent pruritus and fatigue is found to have elevated transaminases. Serologic testing is negative for viral hepatitis. However, testing for specific autoantibodies reveals high titers of anti-soluble liver antigen (anti-SLA). A liver biopsy demonstrates prominent plasma cell infiltrates in the portal tracts extending into the lobules. Which of the following is the most accurate classification and feature of her disease?",
    "option_a": "Type 1 Autoimmune Hepatitis; often associated with anti-smooth muscle antibodies (ASMA)",
    "option_b": "Type 2 Autoimmune Hepatitis; characterized by anti-LKM-1 antibodies",
    "option_c": "Primary Biliary Cholangitis; characterized by destruction of small intrahepatic bile ducts",
    "option_d": "Primary Sclerosing Cholangitis; associated with p-ANCA and inflammatory bowel disease",
    "option_e": "IgG4-related sclerosing cholangitis; responsive to systemic corticosteroids",
    "correct_answer": "A",
    "explanation": "Anti-SLA is highly specific for autoimmune hepatitis (AIH). AIH type 1 is classically associated with ANA and ASMA.",
    "source_context": "Liver Pathology - Autoimmune Hepatitis"
  },
  {
    "question": "A 40-year-old Caucasian male with chronic diarrhea and weight loss is found to have a vesicular rash on his extensor surfaces. Duodenal biopsy reveals intraepithelial lymphocytosis, crypt hyperplasia, and villous blunting. Despite a strict dietary change, he develops abdominal pain and jejunal perforation months later. What is the most likely neoplastic complication this patient has developed?",
    "option_a": "Enteropathy-associated T-cell lymphoma (EATL)",
    "option_b": "Gastrointestinal stromal tumor (GIST)",
    "option_c": "Diffuse large B-cell lymphoma (DLBCL)",
    "option_d": "Adenocarcinoma of the distal ileum",
    "option_e": "Carcinoid tumor of the appendix",
    "correct_answer": "A",
    "explanation": "Celiac disease (associated with dermatitis herpetiformis) has a known complication of enteropathy-associated T-cell lymphoma (EATL).",
    "source_context": "GI Pathology - Celiac Disease"
  },
  {
    "question": "A 55-year-old male farmer presents with chronic diarrhea, polyarthralgia, and cognitive decline. Biopsy of the duodenum reveals numerous macrophages in the lamina propria that are PAS-positive and diastase-resistant. Which of the following is the most appropriate pathophysiologic description of this patient's condition?",
    "option_a": "Intracellular proliferation of a gram-positive actinomycete within lysosomes of macrophages",
    "option_b": "Invasion of the intestinal mucosa by trophozoites leading to flask-shaped ulcers",
    "option_c": "Impaired formation of apolipoprotein B-48 leading to lipid accumulation in enterocytes",
    "option_d": "Excessive proliferation of blind-loop bacteria causing bile salt deconjugation",
    "option_e": "Loss of myenteric plexus ganglionic cells due to Trypanosoma cruzi infection",
    "correct_answer": "A",
    "explanation": "Whipple disease is caused by Tropheryma whipplei, a gram-positive actinomycete. It proliferates within the lysosomes of macrophages.",
    "source_context": "GI Pathology - Whipple Disease"
  },
  {
    "question": "A 60-year-old woman presents with episodic flushing, watery diarrhea, and right-sided heart failure. She recently underwent appendectomy where a 2.5 cm yellow, firm tumor was found at the tip. A pellagra-like rash is noted on her hands. The depletion of which of the following essential amino acids is most likely responsible for her dermatologic findings?",
    "option_a": "Tryptophan",
    "option_b": "Tyrosine",
    "option_c": "Phenylalanine",
    "option_d": "Histidine",
    "option_e": "Methionine",
    "correct_answer": "A",
    "explanation": "Carcinoid syndrome is caused by excess serotonin production from a neuroendocrine tumor. Massive serotonin production depletes tryptophan, leading to niacin (Vitamin B3) deficiency.",
    "source_context": "GI Pathology - Carcinoid Syndrome"
  },
  {
    "question": "A 48-year-old woman presents with severe generalized pruritus and fatigue. Lab results show markedly elevated alkaline phosphatase and IgM levels. Liver biopsy shows a dense portal inflammatory infiltrate composed of lymphocytes, plasma cells, and eosinophils, surrounding a destroyed interlobular bile duct with a noncaseating granuloma. Which autoantibody is most characteristic of this disease?",
    "option_a": "Anti-mitochondrial antibody (AMA)",
    "option_b": "Anti-nuclear antibody (ANA)",
    "option_c": "Anti-smooth muscle antibody (ASMA)",
    "option_d": "Anti-neutrophil cytoplasmic antibody (p-ANCA)",
    "option_e": "Anti-liver kidney microsomal type 1 antibody (Anti-LKM-1)",
    "correct_answer": "A",
    "explanation": "Primary biliary cholangitis (PBC) typically presents with a florid duct lesion with granulomatous destruction, and >90% have anti-mitochondrial antibodies (AMA).",
    "source_context": "Liver Pathology - PBC"
  },
  {
    "question": "A 35-year-old man with a history of ulcerative colitis presents with progressive jaundice and right upper quadrant pain. MRCP demonstrates alternating strictures and dilations of the intrahepatic and extrahepatic bile ducts. A liver biopsy reveals periductal onion-skin fibrosis. This patient is at significantly increased risk of developing which of the following malignancies?",
    "option_a": "Cholangiocarcinoma",
    "option_b": "Hepatocellular carcinoma",
    "option_c": "Pancreatic adenocarcinoma",
    "option_d": "Hepatic angiosarcoma",
    "option_e": "Gallbladder adenocarcinoma",
    "correct_answer": "A",
    "explanation": "Primary sclerosing cholangitis (PSC) carries a high risk for the development of cholangiocarcinoma.",
    "source_context": "Liver Pathology - PSC"
  },
  {
    "question": "A 28-year-old woman taking oral contraceptives presents with sudden onset of severe right upper quadrant pain. CT scan shows a large subcapsular hepatic mass with active intraperitoneal hemorrhage. Resection of the mass reveals well-differentiated hepatocytes in cords without portal tracts. Mutations in which of the following genes are most strongly associated with the highest risk of malignant transformation of this lesion?",
    "option_a": "Beta-catenin (CTNNB1)",
    "option_b": "Hepatocyte nuclear factor 1 alpha (HNF1A)",
    "option_c": "Fibroblast growth factor receptor 2 (FGFR2)",
    "option_d": "KRAS",
    "option_e": "SMAD4",
    "correct_answer": "A",
    "explanation": "Hepatic adenomas with beta-catenin (CTNNB1) mutations have a significantly increased risk of malignant transformation into hepatocellular carcinoma.",
    "source_context": "Liver Pathology - Hepatic Adenoma"
  },
  {
    "question": "A 22-year-old man undergoes colonoscopy revealing over 1000 adenomatous polyps throughout the colon. Genetic testing confirms a germline mutation in the APC gene. If this patient also develops multiple osteomas, epidermal cysts, and locally aggressive but non-metastasizing fibromatoses, what is the specific eponymous syndrome?",
    "option_a": "Gardner syndrome",
    "option_b": "Turcot syndrome",
    "option_c": "Peutz-Jeghers syndrome",
    "option_d": "Cowden syndrome",
    "option_e": "Lynch syndrome",
    "correct_answer": "A",
    "explanation": "Gardner syndrome is a variant of FAP (APC mutation) characterized by colonic polyposis plus osteomas, epidermal cysts, and desmoid tumors.",
    "source_context": "GI Pathology - Polyposis Syndromes"
  },
  {
    "question": "A 40-year-old woman develops ascending colon cancer. Tumor tissue immunohistochemistry shows loss of staining for MLH1 and PMS2 proteins. Which of the following mechanisms is fundamentally responsible for the pathogenesis of her colon cancer?",
    "option_a": "Defective DNA mismatch repair leading to microsatellite instability",
    "option_b": "Chromosomal instability due to an inherited APC gene mutation",
    "option_c": "Hypermethylation of the promoter region of the CDH1 gene",
    "option_d": "Constitutive activation of the Wnt signaling pathway",
    "option_e": "Gain-of-function mutation in the RET proto-oncogene",
    "correct_answer": "A",
    "explanation": "Lynch syndrome (HNPCC) is caused by germline mutations in mismatch repair genes, leading to microsatellite instability (MSI).",
    "source_context": "GI Pathology - Lynch Syndrome"
  }
])

# B answers (11-20)
mcqs.extend([
  {
    "question": "A 65-year-old man from sub-Saharan Africa presents with weight loss, right upper quadrant pain, and an enlarging liver mass. He has a history of chronic hepatitis B infection. A biopsy of the mass demonstrates pleomorphic cells arranged in thick trabeculae, producing bile. Exposure to a toxin produced by Aspergillus species is also suspected. This specific toxin induces a characteristic mutation in which of the following gene loci?",
    "option_a": "Codon 12 of the KRAS oncogene",
    "option_b": "Codon 249 of the TP53 tumor suppressor gene",
    "option_c": "Codon 61 of the HRAS oncogene",
    "option_d": "Codon 130 of the IDH1 gene",
    "option_e": "Promoter region of the TERT gene",
    "correct_answer": "B",
    "explanation": "Aflatoxin B1, produced by Aspergillus, is a potent hepatocarcinogen that causes a characteristic G:C to T:A transversion at codon 249 of the TP53 tumor suppressor gene, heavily contributing to HCC.",
    "source_context": "Liver Pathology - HCC"
  },
  {
    "question": "A 72-year-old woman presents with painless jaundice, dark urine, and pale stools. She reports an unintentional weight loss of 10 kg over the past 3 months. Physical examination reveals a palpable, non-tender gallbladder. She also notes recent migratory thrombophlebitis. An inactivating mutation in which of the following genes, which normally mediates TGF-beta signaling, is frequently implicated in the pathogenesis of her likely underlying malignancy?",
    "option_a": "CDKN2A (p16)",
    "option_b": "SMAD4 (DPC4)",
    "option_c": "BRCA2",
    "option_d": "APC",
    "option_e": "STK11",
    "correct_answer": "B",
    "explanation": "The patient has pancreatic ductal adenocarcinoma presenting with Courvoisier sign and Trousseau syndrome. SMAD4 (DPC4) is inactivated in roughly 55% of pancreatic cancers.",
    "source_context": "Pancreatic Pathology - Adenocarcinoma"
  },
  {
    "question": "A 58-year-old man presents with chronic gastrointestinal bleeding and anemia. Endoscopy reveals a 4 cm submucosal mass in the gastric fundus with a central ulceration. Biopsy shows spindle cells. Immunohistochemistry is strongly positive for CD117 (c-KIT) and DOG1. Which of the following cells is considered the cell of origin for this specific tumor?",
    "option_a": "Smooth muscle cells of the muscularis propria",
    "option_b": "Interstitial cells of Cajal",
    "option_c": "Submucosal neuroendocrine cells",
    "option_d": "Schwann cells of the enteric nervous system",
    "option_e": "Fibroblasts of the lamina propria",
    "correct_answer": "B",
    "explanation": "Gastrointestinal stromal tumors (GISTs) arise from the interstitial cells of Cajal, the pacemaker cells for gut peristalsis, and typically express CD117 (c-KIT) and DOG1.",
    "source_context": "GI Pathology - GIST"
  },
  {
    "question": "A 45-year-old man with a history of chronic gastritis presents with worsening dyspepsia. Endoscopy reveals thickened gastric folds and erythema. Biopsy demonstrates a dense lymphoid infiltrate in the lamina propria forming lymphoepithelial lesions. Genetic analysis of the tissue reveals a t(11;18)(q21;q21) translocation. Which of the following fusion products is characteristic of this lesion?",
    "option_a": "IGH-BCL2",
    "option_b": "API2-MALT1",
    "option_c": "MYC-IGH",
    "option_d": "CCND1-IGH",
    "option_e": "NPM-ALK",
    "correct_answer": "B",
    "explanation": "Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue (MALT lymphoma) is often driven by the t(11;18) translocation creating the API2-MALT1 fusion protein, rendering the tumor resistant to H. pylori eradication.",
    "source_context": "GI Pathology - MALT Lymphoma"
  },
  {
    "question": "A 30-year-old asymptomatic woman undergoes a routine abdominal ultrasound which reveals a well-demarcated 3 cm solid mass in the right lobe of the liver. An MRI demonstrates an isointense mass with a hyperintense central stellate scar. A biopsy is performed, showing nodular architecture with a localized map-like pattern of glutamine synthetase staining. What is the most likely diagnosis?",
    "option_a": "Hepatic adenoma",
    "option_b": "Focal nodular hyperplasia",
    "option_c": "Hepatocellular carcinoma",
    "option_d": "Hepatoblastoma",
    "option_e": "Hepatic hemangioma",
    "correct_answer": "B",
    "explanation": "Focal nodular hyperplasia (FNH) is characterized by a central stellate scar and a map-like pattern of glutamine synthetase staining. It is thought to be a hyperplastic response to an anomalous artery.",
    "source_context": "Liver Pathology - Focal Nodular Hyperplasia"
  },
  {
    "question": "A 50-year-old immigrant from Southeast Asia presents with recurrent cholangitis and jaundice. He reports consuming raw freshwater fish in the past. Imaging reveals dilatation of the intrahepatic biliary tree and a stricture in the common bile duct. Biopsy of the biliary stricture reveals malignant glandular structures with prominent mucin production and abundant desmoplastic stroma. Which of the following infectious agents is most likely responsible for his increased risk?",
    "option_a": "Schistosoma japonicum",
    "option_b": "Clonorchis sinensis",
    "option_c": "Echinococcus granulosus",
    "option_d": "Entamoeba histolytica",
    "option_e": "Ascaris lumbricoides",
    "correct_answer": "B",
    "explanation": "Clonorchis sinensis (the Chinese liver fluke) is acquired by eating raw freshwater fish and resides in the biliary tract. Chronic infection is a major risk factor for cholangiocarcinoma.",
    "source_context": "Liver Pathology - Cholangiocarcinoma"
  },
  {
    "question": "A 75-year-old man with severe atherosclerosis presents with acute onset of crampy left lower quadrant pain and bloody diarrhea. Colonoscopy demonstrates edematous, friable mucosa with cyanosis and superficial ulceration localized to the splenic flexure. The remainder of the colon is normal. This highly specific location of injury is best explained by which of the following anatomic principles?",
    "option_a": "It represents an area of naturally decreased intramural capillary density",
    "option_b": "It is a watershed area between the distribution of the superior and inferior mesenteric arteries",
    "option_c": "It is supplied exclusively by the inferior mesenteric artery, which lacks collateral circulation",
    "option_d": "It has an inherently thinner muscularis mucosae making it susceptible to mucosal infarction",
    "option_e": "It represents a watershed area between the inferior mesenteric artery and internal iliac artery",
    "correct_answer": "B",
    "explanation": "The splenic flexure (Griffith point) is a watershed area at the junction of the territories supplied by the superior mesenteric artery and the inferior mesenteric artery, making it highly susceptible to ischemic colitis.",
    "source_context": "GI Pathology - Ischemic Colitis"
  },
  {
    "question": "A 60-year-old woman develops voluminous, watery diarrhea accompanied by lower abdominal cramps and fever one week after starting clindamycin for a skin infection. Sigmoidoscopy reveals elevated, yellowish-white plaques overlying an erythematous mucosa. Histopathologically, these plaques resemble erupting volcanoes of neutrophils, mucin, and necrotic cellular debris. The primary virulence factor responsible for disrupting the enterocyte cytoskeleton in this condition is:",
    "option_a": "An enterotoxin that ribosylates Gs alpha, increasing cAMP",
    "option_b": "An exotoxin that glucosylates Rho family GTPases",
    "option_c": "A shiga-like toxin that cleaves the 28S rRNA of the 60S ribosomal subunit",
    "option_d": "A superantigen that cross-links MHC II and T-cell receptors",
    "option_e": "A cytolysin that forms pores in the enterocyte membrane",
    "correct_answer": "B",
    "explanation": "Pseudomembranous colitis is caused by Clostridioides difficile. Toxin B (and Toxin A) glucosylates Rho GTPases, causing actin depolymerization, disruption of the enterocyte cytoskeleton, and cell death.",
    "source_context": "GI Pathology - Pseudomembranous Colitis"
  },
  {
    "question": "A 22-year-old male presents with worsening tremor, dysarthria, and drooling. Slit-lamp examination reveals a golden-brown ring at the periphery of the cornea. Laboratory tests indicate mild transaminitis and a decreased serum ceruloplasmin. A liver biopsy shows steatosis, ballooning degeneration, and glycogenated nuclei. A defect in a gene located on which of the following chromosomes is responsible for this disease?",
    "option_a": "Chromosome 6",
    "option_b": "Chromosome 13",
    "option_c": "Chromosome 14",
    "option_d": "Chromosome 7",
    "option_e": "Chromosome 11",
    "correct_answer": "B",
    "explanation": "Wilson disease is an autosomal recessive disorder caused by a mutation in the ATP7B gene, located on chromosome 13. It leads to impaired copper excretion into bile and failure to incorporate copper into ceruloplasmin.",
    "source_context": "Liver Pathology - Wilson Disease"
  },
  {
    "question": "A 52-year-old man presents with generalized weakness, joint pain, and darkening of his skin despite no significant sun exposure. Fasting blood glucose is 210 mg/dL. He also has hepatomegaly. Genetic testing confirms a homozygous C282Y mutation. Which of the following is the primary mechanism leading to iron overload in this patient?",
    "option_a": "Increased binding of transferrin to its receptor on hepatocytes",
    "option_b": "Decreased production of hepcidin leading to uninhibited ferroportin activity",
    "option_c": "Excessive breakdown of erythrocytes in the reticuloendothelial system",
    "option_d": "Upregulation of divalent metal transporter 1 (DMT1) by mutant HFE protein",
    "option_e": "Inability to excrete iron through biliary secretion",
    "correct_answer": "B",
    "explanation": "Hereditary hemochromatosis (HFE gene mutation, C282Y) causes decreased synthesis of hepcidin by the liver. Low hepcidin leads to uninhibited ferroportin activity on enterocytes, resulting in excessive dietary iron absorption.",
    "source_context": "Liver Pathology - Hemochromatosis"
  }
])

# C answers (21-30)
mcqs.extend([
  {
    "question": "A 35-year-old non-smoker presents with progressive dyspnea. Pulmonary function tests show an obstructive pattern. Liver biopsy reveals spherical, PAS-positive, diastase-resistant inclusions in periportal hepatocytes. The patient is found to be homozygous for the Z allele. The accumulation of the abnormal protein in the endoplasmic reticulum of hepatocytes is primarily due to a defect in:",
    "option_a": "Glycosylation in the Golgi apparatus",
    "option_b": "Signal peptide cleavage",
    "option_c": "Protein folding and secretion",
    "option_d": "Ubiquitination and proteasomal degradation",
    "option_e": "Lysosomal targeting via mannose-6-phosphate",
    "correct_answer": "C",
    "explanation": "Alpha-1 antitrypsin deficiency (PiZZ phenotype) is caused by a single amino acid substitution (glutamate to lysine) that results in misfolding of the protein. The misfolded protein aggregates and is trapped in the rough endoplasmic reticulum of hepatocytes.",
    "source_context": "Liver Pathology - Alpha-1 Antitrypsin Deficiency"
  },
  {
    "question": "A 4-day-old neonate develops rapidly worsening jaundice, hypotonia, and seizures. Laboratory tests show a total bilirubin of 28 mg/dL, almost entirely unconjugated. Despite intensive phototherapy, the bilirubin levels remain dangerously high. Genetic analysis reveals a complete absence of uridine diphosphate-glucuronosyltransferase (UGT1A1) activity. Without liver transplantation, what is the most likely pathological finding in the brain of this infant?",
    "option_a": "Cystic encephalomalacia of the cerebral cortex",
    "option_b": "Demyelination of the pontine tracts",
    "option_c": "Yellow discoloration of the basal ganglia and brainstem nuclei",
    "option_d": "Spongiform degeneration of the gray matter",
    "option_e": "Hemorrhagic necrosis of the mammillary bodies",
    "correct_answer": "C",
    "explanation": "The infant has Crigler-Najjar syndrome Type I. The massive unconjugated hyperbilirubinemia leads to kernicterus, which pathologically manifests as yellow discoloration and neuronal death in the basal ganglia, hippocampus, and brainstem nuclei.",
    "source_context": "Liver Pathology - Crigler-Najjar Syndrome"
  },
  {
    "question": "A 25-year-old medical student is noted to be mildly jaundiced after recovering from a viral respiratory infection. Laboratory studies show a total bilirubin of 3.5 mg/dL, predominantly conjugated (direct). Liver enzymes are normal. A biopsy is obtained which shows an intensely pigmented, gross black appearance of the liver, due to dark granular pigment in the lysosomes of hepatocytes. Which of the following transporters is mutated in this condition?",
    "option_a": "OATP1B1",
    "option_b": "BSEP (Bile salt export pump)",
    "option_c": "MRP2 (Multidrug resistance-associated protein 2)",
    "option_d": "MDR3 (Multidrug resistance protein 3)",
    "option_e": "NTCP (Na+/taurocholate cotransporting polypeptide)",
    "correct_answer": "C",
    "explanation": "Dubin-Johnson syndrome is an autosomal recessive disorder caused by mutations in the ABCC2 gene, which encodes the canalicular multidrug resistance-associated protein 2 (MRP2), leading to defective excretion of conjugated bilirubin and epinephrine metabolites (which polymerize to form the black pigment).",
    "source_context": "Liver Pathology - Dubin-Johnson Syndrome"
  },
  {
    "question": "A 28-year-old male presents with intermittent, mild jaundice since childhood. Labs show an elevated conjugated bilirubin level, but normal AST, ALT, and alkaline phosphatase. Unlike Dubin-Johnson syndrome, his liver is not grossly black. Urinary coproporphyrin excretion is elevated, with a striking increase in coproporphyrin I relative to coproporphyrin III. This condition is caused by defective expression of which of the following?",
    "option_a": "Glucuronosyltransferase",
    "option_b": "Canalicular organic anion transporter",
    "option_c": "Sinusoidal organic anion transporting polypeptides (OATP1B1 and OATP1B3)",
    "option_d": "Bile acid receptor FXR",
    "option_e": "Heme oxygenase",
    "correct_answer": "C",
    "explanation": "Rotor syndrome presents similarly to Dubin-Johnson syndrome (conjugated hyperbilirubinemia without significant transaminitis) but lacks the black liver pigment. It is caused by mutations in the SLCO1B1 and SLCO1B3 genes, resulting in simultaneous deficiency of sinusoidal transporters OATP1B1 and OATP1B3.",
    "source_context": "Liver Pathology - Rotor Syndrome"
  },
  {
    "question": "A 62-year-old man with a 20-year history of severe gastroesophageal reflux disease presents with progressive dysphagia to solid foods and a 15-pound weight loss. Endoscopy reveals a stricture and an irregular mass in the distal esophagus. Biopsy of the mass reveals malignant glands invading the submucosa. Which of the following precursor lesions is most strongly associated with this type of malignancy?",
    "option_a": "Squamous dysplasia",
    "option_b": "Esophageal webs",
    "option_c": "Intestinal metaplasia of the distal esophagus",
    "option_d": "Hyperplasia of the basal zone of the squamous epithelium",
    "option_e": "Tylosis",
    "correct_answer": "C",
    "explanation": "The patient has esophageal adenocarcinoma, which almost exclusively arises from Barrett esophagus, defined as intestinal metaplasia (presence of goblet cells) of the distal esophageal squamous mucosa due to chronic GERD.",
    "source_context": "GI Pathology - Esophageal Adenocarcinoma"
  },
  {
    "question": "A 58-year-old man from Iran presents with severe dysphagia, hoarseness, and significant weight loss. He has a 40-pack-year smoking history and consumes alcohol heavily. Endoscopy shows an ulcerating lesion in the middle third of the esophagus. Biopsy shows invasive pleomorphic cells with keratin pearls and intercellular bridges. Which of the following is a classic risk factor for this specific histologic type of esophageal cancer, outside of smoking and alcohol?",
    "option_a": "Chronic gastroesophageal reflux",
    "option_b": "Obesity",
    "option_c": "Plummer-Vinson syndrome",
    "option_d": "Helicobacter pylori infection",
    "option_e": "Celiac sprue",
    "correct_answer": "C",
    "explanation": "Esophageal squamous cell carcinoma usually occurs in the upper or middle third of the esophagus. Risk factors include smoking, alcohol, hot beverages, achalasia, and Plummer-Vinson syndrome (severe iron deficiency anemia, esophageal webs, glossitis).",
    "source_context": "GI Pathology - Squamous Cell Carcinoma of Esophagus"
  },
  {
    "question": "A 45-year-old immigrant from Brazil presents with dysphagia to both solids and liquids, regurgitation of undigested food, and halitosis. Barium swallow shows a dilated esophagus tapering to a 'bird-beak' deformity at the lower esophageal sphincter. Histologic examination of the affected esophagus would most likely reveal:",
    "option_a": "Hypertrophy of the inner circular muscle layer",
    "option_b": "Dense eosinophilic infiltration of the mucosa",
    "option_c": "Loss of ganglion cells in the myenteric (Auerbach) plexus",
    "option_d": "Replacement of skeletal muscle by smooth muscle",
    "option_e": "Mucosal outpouching above the upper esophageal sphincter",
    "correct_answer": "C",
    "explanation": "The patient has secondary achalasia due to Chagas disease (Trypanosoma cruzi infection). Achalasia is characterized by failure of the lower esophageal sphincter to relax and absent peristalsis, caused by loss of inhibitory ganglion cells in the myenteric (Auerbach) plexus.",
    "source_context": "GI Pathology - Achalasia"
  },
  {
    "question": "A 2-day-old male newborn with Down syndrome has failed to pass meconium. Abdominal x-ray shows massively distended loops of bowel. Barium enema reveals a narrow segment in the rectum with a dilated sigmoid colon above it. Rectal biopsy shows a complete lack of ganglion cells in both the submucosal and myenteric plexuses. Mutations in which of the following genes are most commonly implicated in the pathogenesis of this disease?",
    "option_a": "APC",
    "option_b": "CFTR",
    "option_c": "RET",
    "option_d": "CDH1",
    "option_e": "SMAD4",
    "correct_answer": "C",
    "explanation": "Hirschsprung disease is caused by failure of neural crest cell migration, resulting in an aganglionic segment of the colon. Loss-of-function mutations in the RET proto-oncogene are present in a significant majority of familial and sporadic cases.",
    "source_context": "GI Pathology - Hirschsprung Disease"
  },
  {
    "question": "A 10-month-old infant is brought to the emergency department for sudden onset of severe, colicky abdominal pain and vomiting. The parents report the infant has been passing stools mixed with blood and mucus, resembling 'currant jelly.' Ultrasound shows a 'target sign' in the right lower quadrant. Which of the following is the most common anatomical lead point for this condition in children of this age?",
    "option_a": "Colonic adenocarcinoma",
    "option_b": "Lipoma",
    "option_c": "Hypertrophied Peyer patches",
    "option_d": "Meckel diverticulum",
    "option_e": "Appendiceal carcinoid",
    "correct_answer": "C",
    "explanation": "Intussusception in infants is classically associated with hypertrophied Peyer patches (often following a recent viral illness like rotavirus/adenovirus) serving as the lead point. In adults, it is usually a tumor.",
    "source_context": "GI Pathology - Intussusception"
  },
  {
    "question": "A 78-year-old nursing home resident with a history of chronic constipation presents with massive abdominal distension and obstipation. Abdominal radiograph demonstrates a grossly dilated loop of large bowel forming a 'coffee bean' sign, projecting from the pelvis to the right upper quadrant. Which of the following segments of the gastrointestinal tract is most commonly affected by this specific condition in the elderly?",
    "option_a": "Cecum",
    "option_b": "Transverse colon",
    "option_c": "Sigmoid colon",
    "option_d": "Terminal ileum",
    "option_e": "Descending colon",
    "correct_answer": "C",
    "explanation": "Volvulus is a twisting of the bowel along its mesenteric axis. In the elderly, it most commonly involves the sigmoid colon, creating a classic 'coffee bean' sign on plain films. Cecal volvulus is more common in young adults.",
    "source_context": "GI Pathology - Volvulus"
  }
])

# D answers (31-40)
mcqs.extend([
  {
    "question": "A 15-year-old boy presents with periumbilical pain that has migrated to the right lower quadrant over the past 12 hours. He has anorexia, nausea, and a mild fever. Physical examination reveals exquisite tenderness at McBurney's point. A laparotomy is performed, and the resected specimen reveals a transmural neutrophilic infiltrate. What is the most common initiating event in the pathogenesis of this patient's acute condition?",
    "option_a": "Bacterial invasion by Yersinia enterocolitica",
    "option_b": "Viral-induced lymphoid hyperplasia",
    "option_c": "Parasitic infection by Enterobius vermicularis",
    "option_d": "Obstruction of the lumen by a fecalith",
    "option_e": "Ischemic necrosis due to appendiceal artery thrombosis",
    "correct_answer": "D",
    "explanation": "Acute appendicitis in adults and older children is most commonly initiated by obstruction of the appendiceal lumen by a fecalith (stone made of feces), leading to increased intraluminal pressure, ischemia, and subsequent bacterial invasion.",
    "source_context": "GI Pathology - Acute Appendicitis"
  },
  {
    "question": "A 25-year-old woman presents with a history of chronic abdominal pain, diarrhea, and a recent perianal fistula. Colonoscopy reveals discontinuous areas of mucosal erythema, aphthous ulcers, and a cobblestone appearance. Biopsy of the terminal ileum demonstrates transmural inflammation and noncaseating granulomas. Which of the following serological markers is most likely to be positive in this patient?",
    "option_a": "Anti-mitochondrial antibodies (AMA)",
    "option_b": "Anti-neutrophil cytoplasmic antibodies with a perinuclear staining pattern (p-ANCA)",
    "option_c": "Anti-tissue transglutaminase IgA (tTG-IgA)",
    "option_d": "Anti-Saccharomyces cerevisiae antibodies (ASCA)",
    "option_e": "Anti-soluble liver antigen (anti-SLA)",
    "correct_answer": "D",
    "explanation": "Crohn disease is characterized by transmural inflammation, skip lesions, cobblestoning, and granulomas. It is strongly associated with Anti-Saccharomyces cerevisiae antibodies (ASCA), whereas Ulcerative Colitis is associated with p-ANCA.",
    "source_context": "GI Pathology - Crohn Disease"
  },
  {
    "question": "A 30-year-old man complains of bloody diarrhea and crampy lower abdominal pain for the past 6 months. Colonoscopy demonstrates continuous mucosal inflammation starting from the rectum and extending to the splenic flexure, with loss of vascular pattern and numerous inflammatory pseudopolyps. Biopsies reveal crypt abscesses but no granulomas. This patient is at significantly increased risk of developing which of the following hepatobiliary complications?",
    "option_a": "Hepatic adenoma",
    "option_b": "Focal nodular hyperplasia",
    "option_c": "Primary biliary cholangitis",
    "option_d": "Primary sclerosing cholangitis",
    "option_e": "Cholesterol gallstones",
    "correct_answer": "D",
    "explanation": "The patient has ulcerative colitis (continuous mucosal inflammation, crypt abscesses, starting from rectum). UC is strongly associated with primary sclerosing cholangitis (PSC).",
    "source_context": "GI Pathology - Ulcerative Colitis"
  },
  {
    "question": "A 65-year-old man presents with weight loss, early satiety, and epigastric pain. Endoscopy reveals a large, ulcerated mass with heaped-up margins on the lesser curvature of the stomach. Biopsy demonstrates malignant glandular structures infiltrating the gastric wall. A strong epidemiological association exists between this specific type of gastric cancer and which of the following?",
    "option_a": "CDH1 germline mutations",
    "option_b": "Blood type O",
    "option_c": "Hypergastrinemia from a pancreatic tumor",
    "option_d": "Chronic Helicobacter pylori infection",
    "option_e": "Autoimmune gastritis",
    "correct_answer": "D",
    "explanation": "Intestinal-type gastric adenocarcinoma classically forms a mass or ulcer with heaped-up margins on the lesser curvature. It is strongly associated with chronic H. pylori infection, dietary nitrosamines, and blood type A.",
    "source_context": "GI Pathology - Gastric Adenocarcinoma"
  },
  {
    "question": "A 48-year-old woman presents with bilateral adnexal masses and significant weight loss. She recently noted severe early satiety and abdominal fullness. Upper endoscopy reveals a thick, rigid gastric wall (linitis plastica) with no distinct mass. Biopsies show single infiltrating tumor cells with large cytoplasmic mucin vacuoles pushing the nucleus to the periphery. The underlying molecular defect most commonly responsible for this phenotype is:",
    "option_a": "Amplification of the HER2/neu oncogene",
    "option_b": "Microsatellite instability",
    "option_c": "Overexpression of TGF-alpha",
    "option_d": "Loss of function of E-cadherin",
    "option_e": "Activating mutation of beta-catenin",
    "correct_answer": "D",
    "explanation": "Diffuse-type gastric adenocarcinoma is characterized by signet ring cells and a desmoplastic stroma (linitis plastica). It is frequently caused by loss-of-function mutations in the CDH1 gene, which encodes E-cadherin, a cell adhesion molecule.",
    "source_context": "GI Pathology - Diffuse Gastric Cancer"
  },
  {
    "question": "A 50-year-old man complains of burning epigastric pain that usually wakes him up at night and is consistently relieved by eating a meal. Urea breath test is positive. Endoscopy shows a solitary 1 cm ulcer in the proximal duodenum. Which of the following pathophysiological mechanisms is most likely driving this specific patient's ulcer formation?",
    "option_a": "Decreased mucosal prostaglandin synthesis",
    "option_b": "Bile reflux into the stomach",
    "option_c": "Ischemia of the gastric mucosa",
    "option_d": "Increased basal and stimulated gastric acid secretion",
    "option_e": "Autoimmune destruction of parietal cells",
    "correct_answer": "D",
    "explanation": "Duodenal ulcers are almost universally associated with H. pylori and are characterized by increased gastric acid secretion (often due to loss of somatostatin inhibition). The pain classically improves with meals.",
    "source_context": "GI Pathology - Peptic Ulcer Disease"
  },
  {
    "question": "A 42-year-old man presents with severe, recurrent peptic ulcers located in the stomach, duodenum, and even the jejunum. The ulcers are refractory to proton pump inhibitor therapy. He also reports chronic watery diarrhea. Fasting serum gastrin levels are massively elevated. An intravenous secretin test is performed, which results in a paradoxical significant increase in serum gastrin. This patient's condition is frequently associated with mutations in a gene located on which chromosome?",
    "option_a": "Chromosome 3",
    "option_b": "Chromosome 5",
    "option_c": "Chromosome 10",
    "option_d": "Chromosome 11",
    "option_e": "Chromosome 17",
    "correct_answer": "D",
    "explanation": "Zollinger-Ellison syndrome (gastrinoma) is diagnosed with a paradoxical rise in gastrin following secretin administration. It is a common component of MEN 1 syndrome, caused by mutations in the MEN1 gene on chromosome 11.",
    "source_context": "GI Pathology - Zollinger-Ellison Syndrome"
  },
  {
    "question": "A 2-year-old boy is brought to the pediatrician for painless lower gastrointestinal bleeding. His hemoglobin is 8 g/dL. A technetium-99m pertechnetate scan shows intense focal uptake in the right lower quadrant, separate from the stomach. The embryonic structure that failed to completely obliterate in this patient normally connects the fetal midgut to which of the following?",
    "option_a": "Allantois",
    "option_b": "Cloaca",
    "option_c": "Amniotic cavity",
    "option_d": "Yolk sac",
    "option_e": "Urachus",
    "correct_answer": "D",
    "explanation": "Meckel diverticulum results from the failure of the vitelline (omphalomesenteric) duct to obliterate. It normally connects the midgut to the yolk sac. It often contains ectopic gastric mucosa, which is detected by a Tc-99m scan.",
    "source_context": "GI Pathology - Meckel Diverticulum"
  },
  {
    "question": "A 4-week-old firstborn male infant presents with non-bilious, projectile vomiting immediately after feeding. He is always hungry and eager to feed again. Physical examination reveals a small, firm, olive-like mass in the right upper quadrant of the abdomen. Laboratory tests on the infant's serum would most likely show which of the following metabolic disturbances?",
    "option_a": "Hyperchloremic metabolic acidosis",
    "option_b": "Hyponatremic hyperkalemic acidosis",
    "option_c": "Hyperkalemic metabolic alkalosis",
    "option_d": "Hypokalemic hypochloremic metabolic alkalosis",
    "option_e": "Hypocalcemic respiratory alkalosis",
    "correct_answer": "D",
    "explanation": "Hypertrophic pyloric stenosis classically presents with nonbilious projectile vomiting in a 2-6 week old infant. Vomiting of gastric acid leads to a hypokalemic, hypochloremic metabolic alkalosis.",
    "source_context": "GI Pathology - Pyloric Stenosis"
  },
  {
    "question": "A 6-week-old infant who appeared normal at birth has developed progressive jaundice, dark urine, and pale, acholic stools over the past few weeks. Laboratory evaluation demonstrates marked conjugated hyperbilirubinemia. Ultrasound shows an absent or 'ghost' gallbladder and no intrahepatic biliary dilation. Liver biopsy shows marked bile ductular proliferation, portal tract edema, and fibrosis. What is the most definitive surgical intervention to prevent progression to cirrhosis in the short term?",
    "option_a": "Cholecystectomy",
    "option_b": "Endoscopic retrograde cholangiopancreatography (ERCP)",
    "option_c": "Sphincterotomy",
    "option_d": "Kasai portoenterostomy",
    "option_e": "Phototherapy",
    "correct_answer": "D",
    "explanation": "Biliary atresia presents with conjugated jaundice in a newborn due to fibro-obliterative destruction of the extrahepatic biliary tree. The Kasai procedure (hepatoportoenterostomy) establishes a path for bile flow and is a crucial temporizing measure before a liver transplant.",
    "source_context": "Liver Pathology - Biliary Atresia"
  }
])

# E answers (41-50)
mcqs.extend([
  {
    "question": "A 45-year-old man presents with severe, unrelenting epigastric pain radiating to his back, accompanied by nausea and vomiting. Physical examination reveals periumbilical ecchymosis (Cullen sign). Lab tests show markedly elevated serum lipase. He denies any alcohol use and an ultrasound of his gallbladder is completely normal. Genetic testing reveals a gain-of-function mutation in the PRSS1 gene. This mutation directly promotes the premature intracellular activation of which of the following enzymes?",
    "option_a": "Phospholipase A2",
    "option_b": "Elastase",
    "option_c": "Amylase",
    "option_d": "Chymotrypsinogen",
    "option_e": "Trypsinogen",
    "correct_answer": "E",
    "explanation": "Hereditary pancreatitis is often caused by mutations in the PRSS1 gene, which encodes cationic trypsinogen. Gain-of-function mutations prevent the normal autodegradation of prematurely activated trypsin, leading to autodigestion of the pancreas.",
    "source_context": "Pancreatic Pathology - Acute Pancreatitis"
  },
  {
    "question": "A 50-year-old man with a long history of chronic alcoholism presents with persistent abdominal pain, weight loss, and bulky, foul-smelling stools. A plain abdominal radiograph demonstrates diffuse calcifications throughout the mid-abdomen. He was recently diagnosed with diabetes mellitus. Which of the following complications is most specifically associated with this long-standing condition, due to local inflammatory extension?",
    "option_a": "Portal vein thrombosis",
    "option_b": "Superior mesenteric artery aneurysm",
    "option_c": "Gastric varices due to left gastric vein occlusion",
    "option_d": "Cholangiocarcinoma",
    "option_e": "Splenic vein thrombosis",
    "correct_answer": "E",
    "explanation": "Chronic pancreatitis is characterized by pancreatic parenchymal destruction, fibrosis, and calcification. Inflammation often extends posteriorly, causing splenic vein thrombosis, which leads to isolated gastric varices.",
    "source_context": "Pancreatic Pathology - Chronic Pancreatitis"
  },
  {
    "question": "A newborn with Down syndrome presents with feeding intolerance and bilious vomiting shortly after birth. Abdominal X-ray shows a 'double bubble' sign. During surgery, a ring of normal-appearing glandular tissue is seen completely encircling the second part of the duodenum. This anomaly results from the abnormal migration of which of the following embryological structures?",
    "option_a": "Dorsal pancreatic bud",
    "option_b": "Hepatic diverticulum",
    "option_c": "Vitelline duct",
    "option_d": "Septum transversum",
    "option_e": "Ventral pancreatic bud",
    "correct_answer": "E",
    "explanation": "Annular pancreas is caused by the failure of the bilobed ventral pancreatic bud to migrate correctly (or abnormal splitting), resulting in a ring of pancreatic tissue that surrounds and constricts the duodenum.",
    "source_context": "Embryology/Pancreas - Annular Pancreas"
  },
  {
    "question": "A 35-year-old woman is evaluated for recurrent episodes of mild acute pancreatitis. Gallstones and alcohol use are definitively ruled out. Magnetic resonance cholangiopancreatography (MRCP) reveals that the majority of the pancreas drains through the minor duodenal papilla via the duct of Santorini. What is the embryological basis for this anatomical variant?",
    "option_a": "Failure of the ventral bud to migrate dorsally",
    "option_b": "Premature obliteration of the main pancreatic duct",
    "option_c": "Duplication of the dorsal pancreatic bud",
    "option_d": "Incomplete canalization of the ampulla of Vater",
    "option_e": "Failure of the dorsal and ventral pancreatic buds to fuse",
    "correct_answer": "E",
    "explanation": "Pancreas divisum occurs when the dorsal and ventral pancreatic buds fail to fuse. As a result, the bulk of the pancreas (derived from the dorsal bud) drains exclusively through the minor papilla via the accessory duct of Santorini, predisposing to recurrent pancreatitis.",
    "source_context": "Embryology/Pancreas - Pancreas Divisum"
  },
  {
    "question": "A 45-year-old woman with a history of recurrent deep vein thromboses presents with massive ascites, hepatomegaly, and right upper quadrant abdominal pain. Laboratory studies show a high hematocrit and a JAK2 V617F mutation. Liver biopsy reveals severe centrilobular congestion and necrosis, but no fibrosis. Doppler ultrasound shows absent flow in the hepatic veins. What is the most likely diagnosis?",
    "option_a": "Right-sided heart failure (Cor Pulmonale)",
    "option_b": "Sinusoidal obstruction syndrome (Veno-occlusive disease)",
    "option_c": "Cirrhosis",
    "option_d": "Portal vein thrombosis",
    "option_e": "Budd-Chiari syndrome",
    "correct_answer": "E",
    "explanation": "Budd-Chiari syndrome is thrombosis of the hepatic veins, presenting with hepatomegaly, ascites, and abdominal pain. It is strongly associated with hypercoagulable states, notably polycythemia vera (JAK2 mutation).",
    "source_context": "Liver Pathology - Budd-Chiari Syndrome"
  },
  {
    "question": "A 7-year-old boy recovering from chickenpox develops a sudden onset of intractable vomiting and lethargy, which rapidly progresses to a coma. The parents report giving him an over-the-counter medication for fever a few days ago. Laboratory studies show elevated ammonia, AST, ALT, and prolonged prothrombin time, but normal bilirubin. A liver biopsy is performed. What is the classic histopathologic finding in the liver of this patient?",
    "option_a": "Macrovesicular steatosis with Mallory-Denk bodies",
    "option_b": "Massive hepatic necrosis with collapse of the reticulin framework",
    "option_c": "Intracytoplasmic eosinophilic inclusions (Councilman bodies)",
    "option_d": "Perivenular fibrosis and pericellular chicken-wire fibrosis",
    "option_e": "Microvesicular steatosis without inflammation",
    "correct_answer": "E",
    "explanation": "Reye syndrome occurs in children given aspirin during a viral illness. It causes mitochondrial dysfunction leading to hepatic failure and encephalopathy. The classic pathologic finding is panlobular microvesicular steatosis without significant inflammation.",
    "source_context": "Liver Pathology - Reye Syndrome"
  },
  {
    "question": "A 60-year-old man with known alcoholic cirrhosis is brought to the ER with altered mental status, daytime sleepiness, and a flapping tremor of his hands when his wrists are extended. His blood ammonia levels are markedly elevated. He is treated with a non-absorbable disaccharide. The neurologic dysfunction in this patient is primarily mediated by the morphological alteration of which of the following central nervous system cells?",
    "option_a": "Oligodendrocytes",
    "option_b": "Microglia",
    "option_c": "Purkinje cells",
    "option_d": "Ependymal cells",
    "option_e": "Astrocytes",
    "correct_answer": "E",
    "explanation": "In hepatic encephalopathy, excess ammonia crosses the blood-brain barrier and is converted to glutamine by astrocytes. This causes severe osmotic swelling of the astrocytes (Alzheimer type II astrocytes), leading to brain edema and neuronal dysfunction.",
    "source_context": "Liver Pathology - Hepatic Encephalopathy"
  },
  {
    "question": "A 55-year-old man with severe cirrhosis presents with massive hematemesis. Upper endoscopy reveals actively bleeding dilated submucosal vessels in the lower third of the esophagus. The engorgement of these specific vessels is a direct consequence of portosystemic shunting between the portal circulation and which of the following systemic veins?",
    "option_a": "Superior vena cava",
    "option_b": "Inferior vena cava",
    "option_c": "Inferior mesenteric vein",
    "option_d": "Internal iliac vein",
    "option_e": "Azygos vein",
    "correct_answer": "E",
    "explanation": "Esophageal varices occur when portal hypertension forces blood through portosystemic anastomoses. The left gastric vein (portal) shunts blood to the esophageal veins, which drain into the azygos vein (systemic).",
    "source_context": "GI Pathology - Portal Hypertension"
  },
  {
    "question": "A 25-year-old man with a history of asthma and allergic rhinitis presents with solid food dysphagia and recurrent food impaction. Endoscopy reveals multiple mucosal rings (trachealization) and linear furrows in the esophagus. A biopsy of the esophageal mucosa shows >15 of a specific inflammatory cell type per high-power field. This condition is primarily mediated by which of the following immune responses?",
    "option_a": "Th1-mediated delayed hypersensitivity",
    "option_b": "IgA-mediated epithelial destruction",
    "option_c": "CD8+ T-cell cytotoxicity",
    "option_d": "Macrophage-induced granulomatous inflammation",
    "option_e": "Th2-mediated allergic response",
    "correct_answer": "E",
    "explanation": "Eosinophilic esophagitis is a chronic, immune-mediated disorder characterized by eosinophilic infiltration (>15/hpf). It is a Th2-mediated allergic response often triggered by food allergens, presenting with dysphagia and rings/furrows.",
    "source_context": "GI Pathology - Eosinophilic Esophagitis"
  },
  {
    "question": "A 35-year-old woman returns from a year-long mission trip to the Caribbean. She reports chronic diarrhea, significant weight loss, fatigue, and a sore tongue. Laboratory tests reveal a macrocytic anemia. Intestinal biopsy shows villous blunting and intraepithelial lymphocytes, affecting the jejunum and ileum more severely than the duodenum. Her symptoms completely resolve after a prolonged course of tetracycline and folic acid. What is the most likely diagnosis?",
    "option_a": "Celiac disease",
    "option_b": "Crohn disease",
    "option_c": "Abetalipoproteinemia",
    "option_d": "Whipple disease",
    "option_e": "Tropical sprue",
    "correct_answer": "E",
    "explanation": "Tropical sprue presents with malabsorption (often B12 and folate, causing megaloblastic anemia) following residence in the tropics. It involves the entire small bowel (unlike Celiac, which favors the duodenum) and responds to broad-spectrum antibiotics.",
    "source_context": "GI Pathology - Tropical Sprue"
  }
])

output_dir = r'E:\USAMA\MBBS Books\MCQ_Generator\batches'
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, 'bank_batch_gipath.json'), 'w') as f:
    json.dump(mcqs, f, indent=4)
print('Generated successfully!')
