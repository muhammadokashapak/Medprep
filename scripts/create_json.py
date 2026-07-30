import json
import os
import subprocess

mcqs = []
def add_q(q, a, b, c, d, e, ans, exp, topic="Metabolic Disorders"):
    mcqs.append({
        "question": q, "option_a": a, "option_b": b, "option_c": c, "option_d": d, "option_e": e,
        "correct_answer": ans, "explanation": exp, "source_context": topic
    })

# --- A (1-10) ---
add_q(
    "A 3-week-old neonate presents with refractory seizures unresponsive to phenobarbital. CSF analysis reveals elevated alpha-aminoadipic semialdehyde (alpha-AASA). Intravenous pyridoxine administration ceases seizures within minutes. Which of the following is the primary pathophysiological mechanism responsible for this infant's condition?",
    "Accumulation of piperideine-6-carboxylate inactivating pyridoxal 5'-phosphate",
    "Defective transport of basic amino acids across the intestinal epithelium",
    "Impaired oxidative decarboxylation of branched-chain amino acids",
    "Deficiency of gamma-aminobutyric acid transaminase",
    "Impaired dopamine beta-hydroxylase activity",
    "A",
    "Pyridoxine-dependent epilepsy is caused by ALDH7A1 mutation (antiquitin deficiency). Antiquitin metabolizes alpha-AASA. Its absence accumulates piperideine-6-carboxylate (P6C), which condenses with and inactivates pyridoxal 5'-phosphate (PLP), impairing PLP-dependent GABA synthesis.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 10-month-old infant presents with failure to thrive, jaundice, and a cabbage-like odor. Labs show severe hypoglycemia and coagulopathy. Urinalysis is positive for reducing substances but negative for glucose. GC-MS of urine reveals a highly specific abnormal metabolite. Inhibition of which of the following enzymes by this specific metabolite explains the patient's acute neuropathic crises?",
    "Porphobilinogen synthase",
    "Uroporphyrinogen III cosynthase",
    "Hydroxymethylbilane synthase",
    "Protoporphyrinogen oxidase",
    "Ferrochelatase",
    "A",
    "Tyrosinemia type I is caused by fumarylacetoacetate hydrolase deficiency, leading to accumulation of succinylacetone. Succinylacetone structurally resembles delta-aminolevulinic acid (ALA) and strongly inhibits porphobilinogen synthase (ALA dehydratase), leading to porphyria-like neuropathic attacks.",
    "Metabolic Disorders"
)
add_q(
    "A 6-month-old boy presents with failure to thrive, hypotonia, and sparse, brittle, kinky hair. Serum ceruloplasmin and copper levels are low. A genetic defect is identified in a copper-transporting ATPase. Decreased activity of which of the following enzymes best explains this patient's hair findings and tortuous blood vessels?",
    "Lysyl oxidase",
    "Tyrosinase",
    "Dopamine beta-hydroxylase",
    "Cytochrome c oxidase",
    "Superoxide dismutase",
    "A",
    "Menkes disease is an X-linked recessive disorder caused by a mutation in the ATP7A gene, leading to defective intestinal copper absorption. Decreased copper availability impairs the activity of multiple copper-dependent enzymes, most notably lysyl oxidase, which requires copper to cross-link collagen and elastin, causing kinky hair and fragile, tortuous blood vessels.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 5-year-old child presents with progressive ataxia, night blindness, and foul-smelling stools. Peripheral blood smear reveals acanthocytes. Endoscopy shows lipid-laden enterocytes. A mutation in the MTTP gene is confirmed. Which of the following is the primary pathophysiological consequence of this defect?",
    "Impaired assembly and secretion of apolipoprotein B-containing lipoproteins",
    "Defective synthesis of apolipoprotein E in the liver",
    "Inability to clear chylomicron remnants due to apolipoprotein C-II deficiency",
    "Defective transport of cholesterol from peripheral tissues to the liver",
    "Overproduction of very low-density lipoproteins by hepatocytes",
    "A",
    "Abetalipoproteinemia is caused by a mutation in the microsomal triglyceride transfer protein (MTP), which is required for the proper assembly and secretion of chylomicrons and VLDL, both of which contain ApoB (ApoB-48 and ApoB-100, respectively). This leads to severe fat malabsorption and secondary deficiencies in fat-soluble vitamins, notably vitamin E.",
    "Metabolic Disorders"
)
add_q(
    "A 4-month-old infant presents with hypotonia, generalized seizures, alopecia, and a widespread erythematous rash. Arterial blood gas reveals severe lactic acidosis. Urine organic acid analysis shows elevated levels of 3-hydroxyisovaleric acid and beta-methylcrotonylglycine. Administration of which of the following is most likely to reverse these clinical findings?",
    "Biotin",
    "Thiamine",
    "Riboflavin",
    "Niacin",
    "Pyridoxine",
    "A",
    "This patient has biotinidase deficiency, a defect in the recycling of biotin. Biotin is a crucial cofactor for multiple carboxylases (pyruvate carboxylase, acetyl-CoA carboxylase, propionyl-CoA carboxylase, and beta-methylcrotonyl-CoA carboxylase). Deficiency causes impaired gluconeogenesis (lactic acidosis) and impaired branched-chain amino acid catabolism. Treatment is free biotin supplementation.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A newborn develops lethargy, poor feeding, and vomiting 48 hours after birth. Laboratory studies show severe metabolic acidosis, ketonuria, and a plasma ammonia level of 800 umol/L. Serum analysis demonstrates extremely high levels of propionic acid. Which of the following is the primary mechanism of hyperammonemia in this patient?",
    "Inhibition of N-acetylglutamate synthase by accumulated organic acid derivatives",
    "Deficiency of carbamoyl phosphate synthetase I due to a direct gene mutation",
    "Impaired transport of ornithine across the inner mitochondrial membrane",
    "Defective conversion of citrulline to argininosuccinate in the cytosol",
    "Increased shunting of glutamine to ammonia in the renal proximal tubules",
    "A",
    "Propionic acidemia (propionyl-CoA carboxylase deficiency) leads to the accumulation of propionyl-CoA and its derivatives. These toxic organic acids inhibit N-acetylglutamate (NAG) synthase. NAG is an essential allosteric activator of carbamoyl phosphate synthetase I (CPSI), the rate-limiting enzyme of the urea cycle. Thus, inhibition leads to severe secondary hyperammonemia.",
    "Metabolic Disorders"
)
add_q(
    "A 2-year-old child presents with coarse facial features, hepatosplenomegaly, and limited joint mobility. Ophthalmic examination reveals bilateral corneal clouding. Urinalysis demonstrates elevated levels of dermatan sulfate and heparan sulfate. Which of the following specific enzyme deficiencies is responsible for this patient's condition?",
    "Alpha-L-iduronidase",
    "Iduronate-2-sulfatase",
    "Heparan N-sulfatase",
    "Beta-glucuronidase",
    "Galactose-6-sulfatase",
    "A",
    "Hurler syndrome (Mucopolysaccharidosis Type I) is caused by a deficiency of alpha-L-iduronidase, leading to the lysosomal accumulation of dermatan sulfate and heparan sulfate. It is characterized by severe skeletal and neurological manifestations, along with corneal clouding (which distinguishes it from Hunter syndrome, caused by iduronate-2-sulfatase deficiency, an X-linked recessive disorder with no corneal clouding).",
    "Metabolic Disorders"
)
add_q(
    "A 6-year-old boy presents with progressive clumsiness, frequent falls, and a decline in school performance. On examination, he exhibits a vertical supranuclear gaze palsy and massive splenomegaly. Bone marrow biopsy reveals the presence of large, foamy macrophages. A filipin staining test of cultured fibroblasts is markedly positive. Which of the following best describes the underlying pathophysiology?",
    "Defective intracellular trafficking of unesterified cholesterol",
    "Deficiency of sphingomyelinase leading to sphingomyelin accumulation",
    "Deficiency of beta-glucocerebrosidase causing glucosylceramide accumulation",
    "Defective breakdown of ganglioside GM2 in the lysosome",
    "Impaired addition of mannose-6-phosphate to lysosomal hydrolases",
    "A",
    "Niemann-Pick Type C (NPC) is a lysosomal lipid storage disease characterized by defective intracellular transport of unesterified cholesterol, primarily due to mutations in NPC1 or NPC2 genes. This leads to massive cholesterol accumulation in lysosomes (positive filipin stain) and resultant neurodegeneration, classic vertical supranuclear gaze palsy, and hepatosplenomegaly.",
    "Metabolic Disorders"
)
add_q(
    "A 7-month-old infant who was recently weaned from breast milk to cow's milk formula develops severe diarrhea, alopecia, and an erythematous, vesiculobullous rash around the mouth and perineal area. Which of the following is the most likely underlying genetic defect in this patient?",
    "Mutation in the SLC39A4 gene encoding an intestinal trace element transporter",
    "Mutation in the SLC11A2 gene encoding the divalent metal transporter 1 (DMT1)",
    "Mutation in the ATP7A gene encoding a copper-transporting ATPase",
    "Mutation in the HFE gene disrupting intestinal iron sensing",
    "Mutation in the CFTR gene leading to generalized malabsorption",
    "A",
    "Acrodermatitis enteropathica is an autosomal recessive disorder caused by a mutation in the SLC39A4 gene, which encodes the ZIP4 intestinal zinc transporter. Symptoms typically manifest upon weaning from breast milk (which contains bioavailable zinc-binding ligands) to formula. It presents with a classic triad: periorificial and acral dermatitis, alopecia, and diarrhea.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 1-year-old boy presents with sudden onset of hypotonia and loss of motor skills following a mild upper respiratory tract infection. Physical examination reveals macrocephaly. Brain MRI shows profound bilateral striatal necrosis and widely open sylvian fissures. Urine organic acid profile demonstrates massively elevated levels of glutaric acid and 3-hydroxyglutaric acid. Deficiency of which of the following enzymes is responsible?",
    "Glutaryl-CoA dehydrogenase",
    "Isovaleryl-CoA dehydrogenase",
    "Methylmalonyl-CoA mutase",
    "Propionyl-CoA carboxylase",
    "Branched-chain alpha-keto acid dehydrogenase",
    "A",
    "Glutaric acidemia type I is an autosomal recessive disorder caused by a deficiency of glutaryl-CoA dehydrogenase, an enzyme involved in the catabolism of lysine, hydroxylysine, and tryptophan. This causes an accumulation of glutaric acid and 3-hydroxyglutaric acid, which are highly toxic to the basal ganglia, particularly the striatum, leading to acute neurodegenerative crises often triggered by intercurrent illness.",
    "Metabolic Disorders"
)

# --- B (11-20) ---
add_q(
    "A 55-year-old strict vegan presents with symmetric paresthesias in the lower extremities, broad-based gait ataxia, and memory loss. Laboratory evaluation reveals macrocytic anemia. Both serum homocysteine and methylmalonic acid (MMA) levels are significantly elevated. Which of the following biochemical conversions is directly impaired, leading to the accumulation of MMA?",
    "Conversion of homocysteine to methionine",
    "Conversion of methylmalonyl-CoA to succinyl-CoA",
    "Conversion of propionyl-CoA to D-methylmalonyl-CoA",
    "Conversion of N5,N10-methylenetetrahydrofolate to N5-methyltetrahydrofolate",
    "Conversion of deoxyuridine monophosphate to thymidine monophosphate",
    "B",
    "Vitamin B12 (cobalamin) is a crucial cofactor for two distinct enzymes: methionine synthase (converting homocysteine to methionine) and methylmalonyl-CoA mutase (converting L-methylmalonyl-CoA to succinyl-CoA). A deficiency in B12 leads to impaired function of methylmalonyl-CoA mutase, causing the accumulation of methylmalonic acid, which is believed to contribute to defective myelin synthesis and subsequent subacute combined degeneration of the spinal cord.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 4-month-old boy presents with severe, progressive muscle weakness, poor feeding, and failure to thrive. Echocardiogram reveals massive biventricular hypertrophic cardiomyopathy. Skeletal muscle biopsy demonstrates large vacuoles filled with a PAS-positive substance that is sensitive to diastase. Which of the following enzymes is most likely deficient in this patient?",
    "Muscle glycogen phosphorylase",
    "Alpha-1,4-glucosidase",
    "Glucose-6-phosphatase",
    "Glycogen debranching enzyme",
    "Glycogen branching enzyme",
    "B",
    "Pompe disease (Glycogen Storage Disease Type II) is a lysosomal storage disease caused by a deficiency of lysosomal acid alpha-1,4-glucosidase (acid maltase). This leads to massive accumulation of glycogen within lysosomes, severely affecting cardiac and skeletal muscle. It typically presents in early infancy with profound cardiomegaly, severe hypotonia, and early death if untreated.",
    "Metabolic Disorders"
)
add_q(
    "A 6-month-old infant presents with extreme irritability, hypertonia, and an exaggerated startle response. The child has lost previously acquired motor milestones. Optic atrophy is noted on fundoscopy. A peripheral nerve biopsy shows profound demyelination, and brain histology reveals large multinucleated macrophages containing crystalline, periodic acid-Schiff-positive inclusions. Which of the following substrates is accumulating in this patient?",
    "Cerebroside sulfate",
    "Psychosine",
    "Sphingomyelin",
    "Glucosylceramide",
    "GM2 ganglioside",
    "B",
    "Krabbe disease is an autosomal recessive leukodystrophy caused by a deficiency of galactocerebrosidase. This leads to the accumulation of galactocerebroside and, more toxically, psychosine (galactosylsphingosine) in oligodendrocytes and Schwann cells. Psychosine is highly cytotoxic, leading to widespread demyelination. The multinucleated macrophages seen on histology are the classic 'globoid cells'.",
    "Metabolic Disorders"
)
add_q(
    "A 3-year-old boy presents with delayed motor development, choreoathetoid movements, and striking self-injurious behavior, repeatedly biting his lips and fingers. Laboratory studies show severe hyperuricemia. Which of the following enzymes exhibits markedly increased activity due to loss of feedback inhibition in this patient?",
    "Hypoxanthine-guanine phosphoribosyltransferase",
    "Phosphoribosyl pyrophosphate (PRPP) amidotransferase",
    "Xanthine oxidase",
    "Adenosine deaminase",
    "Urate oxidase",
    "B",
    "Lesch-Nyhan syndrome is an X-linked recessive disorder caused by a complete deficiency of hypoxanthine-guanine phosphoribosyltransferase (HGPRT), disrupting the purine salvage pathway. The inability to salvage purines leads to a compensatory massive increase in de novo purine synthesis. This is driven by the markedly increased activity of PRPP amidotransferase, due to both excess substrate (PRPP) and absent feedback inhibition from salvage-derived purine nucleotides.",
    "Metabolic Disorders"
)
add_q(
    "A 32-year-old malnourished man presents with a sore throat, profound angular cheilitis, glossitis, and an intensely pruritic, scaly rash on his scrotum. A slit-lamp examination reveals corneal vascularization. An enzymatic assay using patient erythrocytes is performed to confirm the suspected vitamin deficiency. Decreased activity of which of the following enzymes is diagnostic?",
    "Transketolase",
    "Glutathione reductase",
    "Pyruvate dehydrogenase",
    "Succinate dehydrogenase",
    "Alpha-ketoglutarate dehydrogenase",
    "B",
    "Riboflavin (Vitamin B2) deficiency manifests with cheilosis, stomatitis, glossitis, corneal vascularization, and a highly characteristic seborrheic dermatitis-like rash that often affects the scrotum or vulva. Riboflavin is a precursor for FAD and FMN. The standard diagnostic test is the measurement of erythrocyte glutathione reductase activity, an FAD-dependent enzyme, which will be decreased and will markedly increase upon in vitro addition of FAD.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 45-year-old man presents with chronic blistering skin lesions on the dorsum of his hands and forearms. He reports these lesions worsen significantly with sun exposure. His urine frequently turns a dark tea-color upon standing. Laboratory tests reveal elevated serum transaminases, a high serum ferritin level, and positive hepatitis C serology. Which of the following enzymes is most likely inhibited in this patient?",
    "Porphobilinogen deaminase",
    "Uroporphyrinogen decarboxylase",
    "Coproporphyrinogen oxidase",
    "Protoporphyrinogen oxidase",
    "Delta-aminolevulinic acid synthase",
    "B",
    "Porphyria cutanea tarda (PCT) is the most common porphyria, caused by a deficiency or acquired inhibition of uroporphyrinogen decarboxylase (UROD). The inhibition is highly exacerbated by iron overload, alcohol use, and hepatitis C infection. Accumulation of uroporphyrinogen in the skin leads to severe photosensitivity and blistering, while its excretion darkens the urine.",
    "Metabolic Disorders"
)
add_q(
    "A completely asymptomatic 8-year-old child undergoes routine urinalysis, which yields a positive result for reducing substances but is negative on a glucose-specific dipstick test. The child’s diet includes normal amounts of fruit, table sugar, and dairy. A deficiency in which of the following enzymes is most likely responsible for this finding?",
    "Galactose-1-phosphate uridyltransferase",
    "Fructokinase",
    "Aldolase B",
    "Galactokinase",
    "Lactase",
    "B",
    "Essential fructosuria is a benign, asymptomatic condition caused by a deficiency of fructokinase. Fructose is not phosphorylated and trapped inside cells; instead, it freely circulates and is excreted in the urine. It appears as a reducing sugar on standard copper-reduction tests (like Benedict's test) but is negative on glucose oxidase dipsticks.",
    "Metabolic Disorders"
)
add_q(
    "A 2-year-old girl is brought to the emergency department unconscious after a prolonged gastrointestinal illness where she was unable to eat for 24 hours. Laboratory results show profound hypoglycemia but notably absent serum ketones. Urine analysis reveals an elevated concentration of dicarboxylic acids. Which of the following metabolic processes is fundamentally impaired?",
    "Hepatic glycogenolysis",
    "Mitochondrial beta-oxidation of medium-chain fatty acids",
    "Hepatic gluconeogenesis from amino acid precursors",
    "Conversion of acetyl-CoA to ketone bodies",
    "Peroxisomal alpha-oxidation of branched-chain fatty acids",
    "B",
    "Medium-chain acyl-CoA dehydrogenase (MCAD) deficiency is the most common fatty acid oxidation defect. During prolonged fasting, the inability to oxidize medium-chain fatty acids leads to an energy crisis (no ATP to run gluconeogenesis) and an inability to produce acetyl-CoA (the substrate for ketone bodies). This classic presentation is severe non-ketotic (or hypoketotic) hypoglycemia with dicarboxylic aciduria (due to compensatory omega-oxidation).",
    "Metabolic Disorders"
)
add_q(
    "A 50-year-old man with a long history of severe alcohol use disorder presents with confusion, bilateral horizontal nystagmus, and a wide-based, unsteady gait. If untreated, he may develop irreversible memory loss and confabulation. The defective function of which of the following enzymes, functioning in the non-oxidative phase of the pentose phosphate pathway, is directly linked to his pathogenesis?",
    "Glucose-6-phosphate dehydrogenase",
    "Transketolase",
    "Transaldolase",
    "6-phosphogluconate dehydrogenase",
    "Ribulose-5-phosphate isomerase",
    "B",
    "Wernicke-Korsakoff syndrome is caused by severe thiamine (Vitamin B1) deficiency, common in chronic alcoholics. Thiamine pyrophosphate is a crucial cofactor for Transketolase (in the HMP shunt/pentose phosphate pathway), Pyruvate dehydrogenase, Alpha-ketoglutarate dehydrogenase, and Branched-chain ketoacid dehydrogenase. Decreased transketolase activity in RBCs is diagnostic of thiamine deficiency.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A neonate presents within hours of birth with intractable seizures, profound hypotonia, and dysmorphic features including a small head and deep-set eyes. Ophthalmologic exam reveals dislocated lenses. Laboratory investigations show severe hypouricemia and drastically reduced urinary excretion of sulfate, with elevated urinary sulfite. Which of the following best explains this clinical picture?",
    "Isolated deficiency of sulfite oxidase",
    "Combined deficiency of enzymes requiring a molybdenum cofactor",
    "Deficiency of cystathionine beta-synthase",
    "Deficiency of xanthine oxidase",
    "Defective transport of copper across cellular membranes",
    "B",
    "Molybdenum cofactor deficiency is a rare, devastating autosomal recessive disorder. The molybdenum cofactor is essential for three human enzymes: sulfite oxidase, xanthine oxidase (dehydrogenase), and aldehyde oxidase. Loss of sulfite oxidase causes severe brain damage and lens dislocation (resembling isolated sulfite oxidase deficiency), while loss of xanthine oxidase causes severe hypouricemia. The combination is virtually pathognomonic.",
    "Metabolic Disorders"
)

# --- C (21-30) ---
add_q(
    "A 12-year-old girl from a remote region of China, where the soil is notoriously poor in trace minerals, presents with progressive dyspnea on exertion, peripheral edema, and a markedly enlarged cardiac silhouette on chest X-ray. Echocardiography confirms a severe dilated cardiomyopathy. She is diagnosed with Keshan disease. A deficiency in which of the following enzyme functions is most directly responsible for her condition?",
    "Lysyl oxidase",
    "Cytochrome c oxidase",
    "Glutathione peroxidase",
    "Superoxide dismutase",
    "Xanthine oxidase",
    "C",
    "Keshan disease is an endemic dilated cardiomyopathy caused by a severe deficiency of the trace element selenium. Selenium is a required cofactor for glutathione peroxidase, an antioxidant enzyme that converts toxic hydrogen peroxide to water. In its absence, severe oxidative stress damages the myocardium.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 6-year-old boy presents with a severely pruritic, erythematous, scaly rash in sun-exposed areas. His mother notes he has been increasingly unsteady on his feet and has exhibited erratic, aggressive behavior over the past month. Urinalysis reveals massive generalized neutral aminoaciduria, but basic and acidic amino acid excretion is normal. The underlying pathophysiology directly impairs the endogenous synthesis of which of the following?",
    "Serotonin",
    "Melatonin",
    "Niacin",
    "Dopamine",
    "Histamine",
    "C",
    "Hartnup disease is an autosomal recessive disorder caused by a mutation in the SLC6A19 gene, leading to defective transport of neutral amino acids (especially tryptophan) in the proximal renal tubules and intestinal mucosa. Tryptophan is an essential precursor for the endogenous synthesis of niacin (Vitamin B3). The lack of tryptophan leads to a severe niacin deficiency, presenting clinically as pellagra (diarrhea, dementia, dermatitis).",
    "Metabolic Disorders"
)
add_q(
    "A 24-year-old man of Ashkenazi Jewish descent presents with chronic fatigue, easy bruising, and diffuse bone pain. Examination reveals massive splenomegaly but no hepatomegaly. CBC shows pancytopenia. A bone marrow biopsy demonstrates large, lipid-laden macrophages with a striated, 'crumpled tissue paper' appearance in the cytoplasm. Which of the following enzymes is deficient?",
    "Sphingomyelinase",
    "Hexosaminidase A",
    "Beta-glucocerebrosidase",
    "Alpha-galactosidase A",
    "Arylsulfatase A",
    "C",
    "Gaucher disease, the most common lysosomal storage disease, is caused by a deficiency of beta-glucocerebrosidase, resulting in the accumulation of glucocerebroside in macrophages. These engorged macrophages (Gaucher cells) infiltrate the bone marrow, spleen, and liver, causing pancytopenia, massive splenomegaly, and severe skeletal manifestations like bone crises and avascular necrosis.",
    "Metabolic Disorders"
)
add_q(
    "A 2-year-old child who previously met all developmental milestones begins to exhibit progressive ataxia, hypotonia, and eventual loss of speech. Reflexes are initially brisk but become absent as the disease progresses. MRI reveals diffuse, symmetric demyelination of the central nervous system. A deficiency of arylsulfatase A is confirmed. Which of the following substances is accumulating?",
    "Globotriaosylceramide",
    "Ceramide trihexoside",
    "Cerebroside sulfate",
    "Galactocerebroside",
    "GM1 ganglioside",
    "C",
    "Metachromatic leukodystrophy is an autosomal recessive lysosomal storage disease caused by a deficiency of arylsulfatase A. This results in the accumulation of sulfatides (cerebroside sulfate), which are highly toxic to both central and peripheral myelin, leading to progressive demyelination. The disease is named for the metachromatic granules formed by the accumulating sulfatides when stained with cresyl violet.",
    "Metabolic Disorders"
)
add_q(
    "A 40-year-old man presents with severe, debilitating back pain and stiffness. Radiographs show extensive calcification of the intervertebral discs. On physical examination, there is striking dark blue-black pigmentation of the sclerae and the cartilage of his ears. The patient mentions his urine often turns black if left sitting in the toilet bowl. A defect in which of the following metabolic pathways is responsible?",
    "Tryptophan degradation",
    "Branched-chain amino acid degradation",
    "Tyrosine degradation",
    "Methionine degradation",
    "Histidine degradation",
    "C",
    "Alkaptonuria is an autosomal recessive disorder caused by a deficiency of homogentisate oxidase in the tyrosine degradation pathway. This leads to massive accumulation of homogentisic acid. Homogentisic acid is excreted in urine (turning black upon oxidation) and polymerizes into a dark pigment that deposits in connective tissue and cartilage (ochronosis), causing severe, early-onset degenerative arthropathy.",
    "Metabolic Disorders"
)
add_q(
    "A 28-year-old woman who has been aggressively treating her severe acne with high doses of various dietary supplements presents to the ER with a severe headache, blurry vision, and nausea. Examination reveals papilledema. She has dry, pruritic skin and diffuse alopecia. Laboratory tests show elevated serum aminotransferases. Which of the following supplements is most likely responsible for her symptoms?",
    "Vitamin E",
    "Vitamin C",
    "Vitamin A",
    "Vitamin D",
    "Vitamin B6",
    "C",
    "Hypervitaminosis A (Vitamin A toxicity) is characterized by increased intracranial pressure (pseudotumor cerebri) causing headaches and papilledema, hepatotoxicity (elevated LFTs, possible cirrhosis), dry and pruritic skin, alopecia, and bone pain. It typically occurs from massive megadose supplementation or, classically, from consuming polar bear liver.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 3-month-old infant presents with severe hypotonia, lethargy, and failure to thrive. Blood tests reveal profound, persistent lactic acidosis. A fibroblast assay confirms a severe defect in the pyruvate dehydrogenase complex. The physician prescribes a highly specific, strictly controlled diet. To provide energy while minimizing further lactate production, the diet should be exclusively enriched with which of the following amino acids?",
    "Alanine and glutamine",
    "Phenylalanine and tyrosine",
    "Leucine and lysine",
    "Methionine and valine",
    "Aspartate and glutamate",
    "C",
    "In Pyruvate Dehydrogenase (PDH) complex deficiency, pyruvate cannot be converted to acetyl-CoA and is instead massively shunted to lactate, causing severe lactic acidosis. Treatment relies on a strictly ketogenic diet to bypass the PDH step and provide acetyl-CoA directly to the TCA cycle. The only two exclusively ketogenic amino acids are leucine and lysine.",
    "Metabolic Disorders"
)
add_q(
    "A 3-day-old neonate born at home to a mother who received no prenatal care presents to the emergency department with uncontrollable bleeding from the umbilical stump and diffuse petechiae. Coagulation studies reveal a markedly prolonged PT and a prolonged PTT. A deficiency in which of the following biochemical processes is the direct cause of this bleeding diathesis?",
    "Hydroxylation of proline residues",
    "Methylation of homocysteine",
    "Gamma-carboxylation of glutamic acid residues",
    "Oxidative deamination of biogenic amines",
    "Polyglutamation of dietary folates",
    "C",
    "Vitamin K deficiency presents as hemorrhagic disease of the newborn, especially in neonates who do not receive prophylactic intramuscular Vitamin K at birth (common in home births). Vitamin K is an essential cofactor for gamma-glutamyl carboxylase, which catalyzes the gamma-carboxylation of glutamic acid residues on coagulation factors II, VII, IX, and X, as well as proteins C and S, rendering them capable of binding calcium.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 19-year-old military recruit collapses during an intense, prolonged training run. In the emergency department, he complains of severe muscle cramps and his urine is noted to be dark red. Laboratory testing reveals markedly elevated serum creatine kinase and myoglobinuria. A defect in which of the following processes is the most likely underlying cause?",
    "Glycogen phosphorylase activity in skeletal muscle",
    "Oxidative phosphorylation complex IV activity",
    "Transport of long-chain fatty acids into the mitochondrial matrix",
    "Synthesis of carnitine in the liver",
    "Mitochondrial beta-oxidation of short-chain fatty acids",
    "C",
    "Carnitine palmitoyltransferase II (CPT II) deficiency is a classic cause of recurrent exercise-induced myalgia, muscle stiffness, and myoglobinuria (rhabdomyolysis). Unlike McArdle disease, which is triggered by brief, intense anaerobic exercise, CPT II deficiency is typically triggered by prolonged endurance exercise or fasting, states that heavily rely on long-chain fatty acid oxidation, which is impaired due to inability to transport acyl-carnitines into the mitochondria.",
    "Metabolic Disorders"
)
add_q(
    "A 6-month-old infant presents with painful, progressive swelling of the interphalangeal joints, a characteristic weak and hoarse cry, and the development of multiple subcutaneous periarticular nodules. The patient rapidly develops severe progressive neurologic deterioration. A biopsy of a subcutaneous nodule reveals granulomas containing lipid-laden macrophages. Deficiency of which of the following lysosomal enzymes is responsible?",
    "Alpha-galactosidase A",
    "Beta-galactosidase",
    "Acid ceramidase",
    "Galactocerebrosidase",
    "Sphingomyelinase",
    "C",
    "Farber disease (Farber lipogranulomatosis) is a rare autosomal recessive lysosomal storage disease caused by a deficiency of acid ceramidase. This leads to the massive accumulation of ceramide in macrophages and various tissues. The classic clinical triad consists of a hoarse cry (due to vocal cord granulomas), painful swollen joints, and subcutaneous nodules (lipogranulomas).",
    "Metabolic Disorders"
)

# --- D (31-40) ---
add_q(
    "A 15-year-old boy presents with sudden severe chest pain and shortness of breath. He is extremely tall with long, thin limbs, arachnodactyly, and a highly arched palate. Ophthalmoscopy reveals bilateral downward subluxation of the lenses. A CT pulmonary angiogram confirms a massive pulmonary embolism. Which of the following enzymes is most likely deficient in this patient?",
    "Fibrillin-1",
    "Lysyl oxidase",
    "Alpha-1 antitrypsin",
    "Cystathionine beta-synthase",
    "Methionine synthase",
    "D",
    "Homocystinuria caused by cystathionine beta-synthase deficiency presents with a Marfanoid habitus (tall, long limbs, arachnodactyly). However, unlike Marfan syndrome (which features upward lens subluxation and aortic root dilation), homocystinuria classically presents with downward/inward lens subluxation, intellectual disability, and a severe predisposition to arterial and venous thromboembolism (the cause of the PE here).",
    "Metabolic Disorders"
)
add_q(
    "A 9-month-old infant of Eastern European Jewish descent is brought to the clinic for progressive weakness and loss of motor skills. The parents report the child exhibits an exaggerated startle response to loud noises. Fundoscopic examination reveals a bright 'cherry-red spot' at the macula. Abdominal examination is unremarkable, with no hepatosplenomegaly. Which of the following substrates is accumulating in this patient's lysosomes?",
    "Sphingomyelin",
    "Glucocerebroside",
    "Cerebroside sulfate",
    "GM2 ganglioside",
    "Heparan sulfate",
    "D",
    "Tay-Sachs disease is an autosomal recessive disorder caused by a deficiency of hexosaminidase A, leading to the toxic accumulation of GM2 ganglioside primarily in the central nervous system. It presents with neurodegeneration, hyperreflexia, a hyperacusis-induced startle response, and a cherry-red macula. The absence of hepatosplenomegaly crucially distinguishes it from Niemann-Pick disease (sphingomyelinase deficiency).",
    "Metabolic Disorders"
)
add_q(
    "A 5-day-old neonate develops poor feeding, vomiting, profound jaundice, and hepatomegaly shortly after the introduction of breast milk. The infant rapidly deteriorates and blood cultures grow Escherichia coli. Urinalysis reveals the presence of reducing substances. A deficiency of which of the following enzymes is the primary cause of this presentation?",
    "Galactokinase",
    "Fructokinase",
    "Aldolase B",
    "Galactose-1-phosphate uridyltransferase",
    "Lactase",
    "D",
    "Classic galactosemia is caused by a severe deficiency of galactose-1-phosphate uridyltransferase (GALT). Ingestion of lactose (glucose + galactose) in breast milk leads to a massive toxic accumulation of galactose-1-phosphate and galactitol. This causes severe hepatotoxicity (jaundice, hepatomegaly), cataracts, and a highly specific, severe predisposition to E. coli neonatal sepsis.",
    "Metabolic Disorders"
)
add_q(
    "A 2-year-old child presents with bowed legs, a waddling gait, and total body alopecia. Laboratory tests reveal severe hypocalcemia, hypophosphatemia, and markedly elevated parathyroid hormone levels. Surprisingly, serum 1,25-dihydroxycholecalciferol levels are found to be massively elevated. Which of the following is the most likely underlying mechanism?",
    "Deficiency of renal 1-alpha-hydroxylase",
    "Deficiency of hepatic 25-hydroxylase",
    "Inactivating mutation of the calcium-sensing receptor",
    "End-organ resistance due to a mutated vitamin D receptor",
    "Malabsorption of fat-soluble vitamins in the terminal ileum",
    "D",
    "Vitamin D Dependent Rickets Type II (VDDR II) is caused by an inactivating mutation in the intracellular Vitamin D Receptor (VDR), leading to total end-organ resistance to active vitamin D. The lack of negative feedback causes a massive compensatory increase in 1,25-dihydroxycholecalciferol levels. The classic unique feature distinguishing it from Type I (1-alpha-hydroxylase deficiency) is the presence of total body alopecia.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 55-year-old woman presents with severe watery diarrhea, a hyperpigmented scaly rash on her face and neck, and periods of confusion and disorientation. She also reports frequent episodes of intense facial flushing and wheezing. An echocardiogram reveals right-sided valvular lesions. The deficiency responsible for her rash and dementia is caused by the depletion of which of the following precursors?",
    "Tyrosine",
    "Histidine",
    "Phenylalanine",
    "Tryptophan",
    "Arginine",
    "D",
    "This patient has carcinoid syndrome (flushing, wheezing, right-sided heart lesions, diarrhea) resulting from a neuroendocrine tumor secreting massive amounts of serotonin. Serotonin is synthesized from the amino acid tryptophan. Because up to 50% of the body's tryptophan is diverted to make serotonin in this condition, there is a severe lack of tryptophan available for endogenous Niacin (Vitamin B3) synthesis, leading to Pellagra (diarrhea, dementia, dermatitis).",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 22-year-old man presents with a resting tremor, slurred speech, and an unsteady gait. His family reports he has become increasingly irritable and paranoid over the last year. Slit-lamp examination reveals a golden-brown ring at the limbus of the cornea. Laboratory tests show elevated serum transaminases and extremely low serum ceruloplasmin. The primary defect in this condition leads to an inability to perform which of the following cellular functions?",
    "Absorption of copper across the apical membrane of the enterocyte",
    "Synthesis of the apoceruloplasmin protein backbone",
    "Incorporation of iron into protoporphyrin IX",
    "Hepatic excretion of copper into the biliary canaliculi",
    "Transport of copper from the bloodstream across the blood-brain barrier",
    "D",
    "Wilson disease is caused by an autosomal recessive mutation in the ATP7B gene, which encodes a hepatic copper-transporting ATPase. This ATPase is essential for two primary functions: loading copper onto apoceruloplasmin to form functional ceruloplasmin, and actively excreting excess copper into the bile. Defective ATP7B leads to copper accumulation in the liver, brain (basal ganglia), and corneas (Kayser-Fleischer rings).",
    "Metabolic Disorders"
)
add_q(
    "A newborn presents with profound hypotonia, severe craniofacial dysmorphism (including a high forehead, large anterior fontanelle, and flattened midface), and hepatomegaly. The infant experiences multiple seizures and dies within the first week of life. Biochemical analysis reveals massively elevated levels of very long-chain fatty acids (VLCFAs) in the plasma. A defect in the biogenesis of which of the following organelles is responsible?",
    "Mitochondrion",
    "Lysosome",
    "Rough endoplasmic reticulum",
    "Peroxisome",
    "Golgi apparatus",
    "D",
    "Zellweger syndrome is a severe peroxisomal biogenesis disorder. Mutations in PEX genes prevent the assembly of functional peroxisomes. Because peroxisomes are exclusively responsible for the initial steps of beta-oxidation of very long-chain fatty acids (VLCFAs) and branched-chain fatty acids (like phytanic acid), these lipids accumulate to massive, highly toxic levels, causing severe neurologic and hepatic dysfunction.",
    "Metabolic Disorders"
)
add_q(
    "A 40-year-old pregnant woman presents with fatigue and pallor. CBC reveals a macrocytic anemia with hypersegmented neutrophils on the peripheral smear. Serum methylmalonic acid levels are normal, but homocysteine levels are elevated. A deficiency of which of the following is most likely responsible, and what critical synthesis pathway is directly impaired?",
    "Vitamin B12; Impaired synthesis of methionine",
    "Vitamin B6; Impaired synthesis of heme",
    "Iron; Impaired synthesis of hemoglobin",
    "Folic Acid; Impaired synthesis of thymidylate",
    "Vitamin C; Impaired absorption of iron",
    "D",
    "This patient has folic acid (Vitamin B9) deficiency, characterized by megaloblastic macrocytic anemia (hypersegmented neutrophils) with elevated homocysteine but NORMAL methylmalonic acid (distinguishing it from B12 deficiency). Folate is essential for the transfer of 1-carbon units. Its deficiency directly impairs thymidylate synthase (conversion of dUMP to dTMP), halting DNA synthesis and causing megaloblastic changes.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 10-month-old infant with a known diagnosis of phenylketonuria (PKU) has been strictly maintained on a phenylalanine-restricted diet since birth, and serum phenylalanine levels have remained within normal limits. Despite this, the child presents with severe developmental delay, progressive hypotonia, and frequent seizures. Prolactin levels are found to be highly elevated. A deficiency of which of the following is most likely responsible for this clinical deterioration?",
    "Phenylalanine hydroxylase",
    "Tyrosine hydroxylase",
    "Dopa decarboxylase",
    "Tetrahydrobiopterin (BH4)",
    "Dopamine beta-hydroxylase",
    "D",
    "Malignant PKU (atypical PKU) occurs when the defect is not in the enzyme Phenylalanine Hydroxylase itself, but rather a deficiency of its required cofactor, Tetrahydrobiopterin (BH4) (most commonly due to dihydropteridine reductase deficiency). BH4 is also absolutely required for Tyrosine Hydroxylase (dopamine synthesis) and Tryptophan Hydroxylase (serotonin synthesis). Thus, despite dietary phenylalanine restriction, the patient suffers severe catecholamine and serotonin depletion. Low dopamine leads to uninhibited prolactin secretion.",
    "Metabolic Disorders"
)
add_q(
    "A 60-year-old man who lives alone and consumes a diet consisting exclusively of canned soup and crackers presents with generalized fatigue, severe joint pain, and bleeding gums. Physical examination reveals numerous perifollicular petechiae and coiled, 'corkscrew' hairs on his lower extremities. The underlying pathophysiology involves a defect in which of the following subcellular locations?",
    "Mitochondrial matrix",
    "Cytosol",
    "Golgi apparatus",
    "Rough endoplasmic reticulum",
    "Nucleus",
    "D",
    "Scurvy is caused by a severe deficiency of Vitamin C (ascorbic acid). Vitamin C is an essential reducing agent for prolyl hydroxylase and lysyl hydroxylase, enzymes that function entirely within the rough endoplasmic reticulum. These enzymes hydroxylate proline and lysine residues on procollagen alpha chains, a step absolutely necessary for the subsequent formation of the stable collagen triple helix. Failure leads to fragile blood vessels and poor wound healing.",
    "Vitamins/Nutritional Deficiencies"
)

# --- E (41-50) ---
add_q(
    "A 5-day-old infant presents with poor feeding, vomiting, and lethargy. The infant exhibits alternating episodes of severe hypertonia and flaccidity. The diaper emits a distinct, sweet, burnt-sugar odor. Laboratory analysis reveals elevated levels of leucine, isoleucine, and valine. The deficient enzyme complex in this disorder requires which of the following as a crucial cofactor?",
    "Pyridoxal phosphate",
    "Biotin",
    "Cobalamin",
    "Tetrahydrofolate",
    "Thiamine pyrophosphate",
    "E",
    "Maple Syrup Urine Disease (MSUD) is caused by a deficiency of the branched-chain alpha-keto acid dehydrogenase (BCKDH) complex. This enzyme is responsible for the oxidative decarboxylation of leucine, isoleucine, and valine. Like Pyruvate Dehydrogenase and Alpha-Ketoglutarate Dehydrogenase, BCKDH requires five specific cofactors: Thiamine pyrophosphate (B1), Lipoic acid, CoA (B5), FAD (B2), and NAD+ (B3).",
    "Metabolic Disorders"
)
add_q(
    "A 6-month-old infant who was recently transitioned from breast milk to a diet including pureed fruits and fruit juices presents with recurrent episodes of diaphoresis, tachycardia, vomiting, and profound lethargy shortly after feeding. Laboratory studies show severe hypoglycemia, hypophosphatemia, and elevated serum transaminases. The primary pathophysiologic mechanism of the hypoglycemia is:",
    "Inability to transport glucose out of the hepatocyte",
    "Inability to convert galactose-1-phosphate to UDP-galactose",
    "Defective function of the debranching enzyme in glycogenolysis",
    "Impaired insulin secretion from pancreatic beta cells",
    "Depletion of intracellular inorganic phosphate inhibiting glycogenolysis",
    "E",
    "Hereditary Fructose Intolerance is caused by a deficiency of Aldolase B. Upon ingestion of fructose, it is rapidly phosphorylated by fructokinase to fructose-1-phosphate, which then accumulates massively because Aldolase B cannot cleave it. This essentially traps and profoundly depletes the cell's pool of inorganic phosphate (Pi). The lack of Pi directly halts glycogen phosphorylase, fatally impairing glycogenolysis and leading to severe, rapid-onset fasting hypoglycemia.",
    "Metabolic Disorders"
)
add_q(
    "A 20-year-old man presents with progressive night blindness, loss of peripheral vision, and a loss of the sense of smell. Physical examination reveals an unsteady gait, absent deep tendon reflexes, and bilaterally short fourth toes. Fundoscopy demonstrates retinitis pigmentosa. Laboratory analysis reveals massively elevated levels of phytanic acid. This condition is caused by a primary defect in which of the following cellular processes?",
    "Lysosomal degradation of glycosaminoglycans",
    "Mitochondrial beta-oxidation of long-chain fatty acids",
    "Peroxisomal beta-oxidation of very long-chain fatty acids",
    "Cytosolic synthesis of fatty acids",
    "Peroxisomal alpha-oxidation of branched-chain fatty acids",
    "E",
    "Refsum disease is an autosomal recessive disorder caused by a deficiency of phytanoyl-CoA hydroxylase, an essential enzyme for the peroxisomal alpha-oxidation of branched-chain fatty acids (phytanic acid, found in dairy and ruminant fat). Massive accumulation of phytanic acid is highly toxic, causing retinitis pigmentosa, severe peripheral neuropathy, cerebellar ataxia, anosmia, and characteristic skeletal anomalies (short fourth toe).",
    "Metabolic Disorders"
)
add_q(
    "A 16-year-old high school athlete complains of severe muscle cramping and extreme fatigue occurring within minutes of initiating a sprint. He notes that if he pushes through the pain, he sometimes experiences dark red urine. An ischemic forearm exercise test is performed, which shows a flat venous lactate curve despite adequate exertion. Deficiency of which of the following enzymes is responsible?",
    "Phosphofructokinase-1",
    "Carnitine palmitoyltransferase II",
    "Alpha-1,4-glucosidase",
    "Lactate dehydrogenase",
    "Muscle glycogen phosphorylase",
    "E",
    "McArdle disease (Glycogen Storage Disease Type V) is caused by a deficiency of muscle glycogen phosphorylase (myophosphorylase). Skeletal muscle cannot break down glycogen into glucose-1-phosphate during the initial highly anaerobic phase of intense exercise, leading to rapid energy depletion, severe cramps, and rhabdomyolysis. Because glycogenolysis is halted, the muscle cannot produce pyruvate to reduce to lactate, resulting in a classic 'flat' lactate curve on the ischemic forearm test.",
    "Metabolic Disorders"
)
add_q(
    "A 30-year-old woman presents to the emergency department with severe, unremitting abdominal pain, nausea, and vomiting. She also reports tingling in her arms and profound anxiety. An exploratory laparotomy shows no anatomical abnormalities. A urine sample left by the window turns a deep port-wine color after several hours. The patient is found to be deficient in an enzyme in the heme synthesis pathway. What is the deficient enzyme?",
    "Uroporphyrinogen decarboxylase",
    "Ferrochelatase",
    "Coproporphyrinogen oxidase",
    "Delta-aminolevulinic acid dehydratase",
    "Porphobilinogen deaminase",
    "E",
    "Acute Intermittent Porphyria (AIP) is an autosomal dominant disorder caused by a deficiency of porphobilinogen (PBG) deaminase (also known as hydroxymethylbilane synthase). It is characterized by acute, severe attacks of abdominal pain, psychiatric symptoms, and peripheral neuropathy, often triggered by drugs (CYP inducers), fasting, or stress. The classic finding is urine that turns dark/port-wine colored upon standing in light, due to the oxidation of the massively accumulating PBG and ALA.",
    "Metabolic Disorders"
)
add_q(
    "A 7-year-old child from a developing nation is brought to a medical mission clinic. The mother states the child cannot see in dim light. Examination of the eyes reveals thick, dry, silver-grey foamy plaques on the bulbar conjunctiva, and the cornea appears dangerously soft and ulcerated. The primary pathophysiological mechanism of the conjunctival lesions is:",
    "Deposition of oxidized lipofuscin within the retinal pigmented epithelium",
    "Infiltration of the subconjunctival space by lipid-laden macrophages",
    "Precipitation of calcium-phosphate complexes due to altered pH",
    "Accumulation of amyloid fibrils in the substantia propria",
    "Squamous metaplasia of the specialized columnar epithelium",
    "E",
    "Severe Vitamin A deficiency is a leading cause of preventable blindness worldwide. Vitamin A is essential not only for the formation of rhodopsin (preventing night blindness) but also for the maintenance of specialized epithelia. A severe deficiency leads to the squamous metaplasia of normal columnar/transitional epithelia to a keratinizing squamous epithelium. In the eye, this causes Bitot spots (foamy keratin plaques) and keratomalacia (corneal softening/ulceration).",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 3-year-old boy presents with delayed motor milestones and progressive stiffness in his lower extremities. Examination reveals severe spastic diplegia and choreoathetoid movements. Serum ammonia levels are found to be strictly within normal limits, while plasma amino acid profiling reveals massively elevated levels of arginine. Which of the following enzymes of the urea cycle is deficient?",
    "Ornithine transcarbamylase",
    "Carbamoyl phosphate synthetase I",
    "Argininosuccinate synthetase",
    "Argininosuccinate lyase",
    "Arginase",
    "E",
    "Arginase deficiency is the unique urea cycle defect that rarely presents with severe hyperammonemia. Arginase catalyzes the final step of the urea cycle: the cleavage of arginine to urea and ornithine. Its deficiency leads to massive arginine accumulation, causing a specific, progressive neurologic phenotype characterized by severe spastic diplegia (resembling cerebral palsy), growth delay, and choreoathetosis, but without the acute hyperammonemic crises typical of other urea cycle defects.",
    "Metabolic Disorders"
)
add_q(
    "An experimental human dietary restriction study inadvertently completely eliminates a specific water-soluble vitamin from the diet of a healthy volunteer. Over several weeks, the volunteer develops severe dermatitis, enteritis, alopecia, and progressive adrenal insufficiency. Biochemical analysis reveals a profound inability to synthesize Coenzyme A. Which of the following vitamins was eliminated?",
    "Thiamine (Vitamin B1)",
    "Riboflavin (Vitamin B2)",
    "Niacin (Vitamin B3)",
    "Pyridoxine (Vitamin B6)",
    "Pantothenic acid (Vitamin B5)",
    "E",
    "Pantothenic acid (Vitamin B5) is an essential structural component of Coenzyme A (CoA) and fatty acid synthase. CoA is absolutely required for a vast array of metabolic reactions, including the TCA cycle (acetyl-CoA, succinyl-CoA), fatty acid synthesis and oxidation, and cholesterol synthesis. Deficiency is exceptionally rare but presents with 'burning feet syndrome', dermatitis, alopecia, and, due to impaired cholesterol synthesis, adrenal insufficiency.",
    "Vitamins/Nutritional Deficiencies"
)
add_q(
    "A 4-month-old infant is evaluated for recurrent seizures occurring exclusively in the early morning. Physical exam shows a prominent 'doll-like' face, thin extremities, and massive hepatomegaly extending to the pelvis. Laboratory studies reveal profound severe fasting hypoglycemia, lactic acidosis, hyperuricemia, and hyperlipidemia. A defect in which of the following enzymes is responsible?",
    "Hepatic glycogen phosphorylase",
    "Debranching enzyme",
    "Lysosomal alpha-1,4-glucosidase",
    "Fructose-1,6-bisphosphatase",
    "Glucose-6-phosphatase",
    "E",
    "Von Gierke disease (Glycogen Storage Disease Type I) is caused by a deficiency of glucose-6-phosphatase. This enzyme catalyzes the final, crucial step shared by BOTH glycogenolysis and gluconeogenesis: the dephosphorylation of glucose-6-phosphate to free glucose in the liver and kidneys. Its complete absence leads to extremely severe fasting hypoglycemia. The trapped G6P is shunted into glycolysis (lactic acidosis), lipogenesis (hyperlipidemia), and the HMP shunt (hyperuricemia).",
    "Metabolic Disorders"
)
add_q(
    "A 14-year-old boy presents with severe chest pain radiating to his left arm. ECG confirms an acute anterolateral myocardial infarction. Physical examination reveals firm, nodular masses on his Achilles tendons and bilateral arcus corneae. Family history is significant for a father who died of a massive heart attack at age 28. The primary pathophysiological mechanism underlying his condition is a defect in:",
    "Hepatic synthesis of apolipoprotein B-100",
    "Lipoprotein lipase activity on the vascular endothelium",
    "Clearance of chylomicron remnants by apolipoprotein E receptors",
    "Activity of lecithin-cholesterol acyltransferase",
    "Receptor-mediated endocytosis of low-density lipoproteins",
    "E",
    "Familial Hypercholesterolemia (Type IIa familial dyslipidemia) is most commonly an autosomal dominant disorder caused by a mutation in the LDL receptor gene. This leads to defective receptor-mediated endocytosis of LDL by the liver, resulting in astronomically high serum LDL levels from birth. This causes accelerated atherosclerosis (early, severe myocardial infarctions), tendon xanthomas (especially Achilles), and premature corneal arcus.",
    "Metabolic Disorders"
)

out_path = r"E:\USAMA\MBBS Books\MCQ_Generator\batches\bank_batch_metabolic.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(mcqs, f, indent=2)

print(f"Generated {len(mcqs)} MCQs.")

insert_script = r"E:\USAMA\MBBS Books\MCQ_Generator\insert_to_bank.py"
if os.path.exists(insert_script):
    print("Running insert script...")
    subprocess.run(["python", insert_script, out_path], check=True)
else:
    print(f"Insert script not found at {insert_script}. Please check path.")
