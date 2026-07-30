import os
import json
import random

def generate_mcqs():
    questions_data = [
        {
            "q": "A 14-month-old child presents with coarse facial features, clouded corneas, restricted joint mobility, and hepatosplenomegaly. Fibroblast cultures demonstrate a marked deficiency of multiple lysosomal hydrolases. The serum, however, contains highly elevated levels of these same enzymes. A defect in which of the following processes is the most likely underlying mechanism for this disorder?",
            "options": ["Phosphorylation of mannose residues", "Addition of mannose-6-phosphate receptors in the trans-Golgi", "Cleavage of the signal sequence by signal peptidase", "Ubiquitination of misfolded proteins in the endoplasmic reticulum", "Attachment of N-acetylglucosamine to an asparagine residue"],
            "exp": "This patient has I-cell disease (mucolipidosis type II), caused by a deficiency of N-acetylglucosamine-1-phosphotransferase. This enzyme is responsible for the phosphorylation of mannose residues on lysosomal enzymes in the Golgi apparatus. Without this mannose-6-phosphate tag, the enzymes are not targeted to lysosomes and are instead secreted into the extracellular space.",
            "ctx": "Molecular Biology - Protein Trafficking"
        },
        {
            "q": "A male infant born at 38 weeks' gestation presents with hypotonia, poor feeding, and a large anterior fontanelle. Over the next few weeks, he develops seizures, hepatomegaly, and jaundice. Very long-chain fatty acids (VLCFAs), phytanic acid, and pipecolic acid are markedly elevated in his plasma. A mutation in a gene coding for a biogenesis factor (PEX) is suspected. Which of the following cellular processes is most likely directly impaired?",
            "options": ["Alpha-oxidation of branched-chain fatty acids", "Beta-oxidation of medium-chain fatty acids", "Synthesis of cardiolipin", "Elongation of fatty acids", "Degradation of unfolded proteins"],
            "exp": "The clinical picture is Zellweger syndrome (cerebrohepatorenal syndrome), a peroxisomal biogenesis disorder. Peroxisomes are responsible for the beta-oxidation of very long-chain fatty acids (VLCFAs) and the alpha-oxidation of branched-chain fatty acids (like phytanic acid).",
            "ctx": "Cellular Biology - Organelles"
        },
        {
            "q": "A 22-year-old man presents with subacute, painless, bilateral vision loss over the past 3 weeks. Examination reveals hyperemia of the optic discs and telangiectatic peripapillary vessels. Pedigree analysis shows that his maternal uncle and older brother have similar visual deficits, but his father and paternal uncle are unaffected. The primary defect in this patient’s condition most likely resides in which of the following components?",
            "options": ["NADH dehydrogenase", "Cytochrome c oxidase", "ATP synthase", "Succinate dehydrogenase", "Coenzyme Q reductase"],
            "exp": "The patient has Leber hereditary optic neuropathy (LHON), which exhibits mitochondrial inheritance (maternal transmission). It is most commonly caused by mutations in mitochondrial DNA that encode subunits of Complex I (NADH dehydrogenase) of the electron transport chain.",
            "ctx": "Genetics - Mitochondrial Inheritance"
        },
        {
            "q": "A 3-year-old girl is brought to the clinic for delayed speech and frequent inappropriate bouts of laughter. She has microcephaly, a wide-based uncoordinated gait, and recurrent seizures. Genetic analysis reveals a deletion on chromosome 15q11-q13. The defective gene in this patient normally undergoes which of the following modifications in the non-deleted allele inherited from the father?",
            "options": ["DNA methylation", "Histone acetylation", "Somatic hypermutation", "Alternative splicing", "Polyadenylation"],
            "exp": "The patient has Angelman syndrome, caused by loss of the maternal allele of UBE3A (located at 15q11-q13). Since she has a deletion on the maternal chromosome, she is relying on the paternal chromosome. However, the paternal UBE3A allele is normally silenced by epigenetic DNA methylation (imprinting). Thus, she has no functional UBE3A.",
            "ctx": "Genetics - Imprinting"
        },
        {
            "q": "A 7-year-old boy presents with declining school performance and behavioral changes. Over the next year, he develops progressive visual loss, spasticity, and adrenal insufficiency. Accumulation of very long-chain fatty acids (VLCFAs) is found in his plasma and fibroblasts. The defective protein in this condition is normally involved in which of the following functions?",
            "options": ["Transport of VLCFAs across the peroxisomal membrane", "Transport of long-chain fatty acids into mitochondria", "Elongation of VLCFAs in the endoplasmic reticulum", "Beta-oxidation of VLCFAs within the peroxisome matrix", "Synthesis of plasmalogens for myelin sheath formation"],
            "exp": "The patient has X-linked adrenoleukodystrophy (X-ALD), caused by mutations in the ABCD1 gene. This gene encodes the adrenoleukodystrophy protein (ALDP), an ATP-binding cassette (ABC) transporter located in the peroxisomal membrane, which is responsible for transporting VLCFAs into the peroxisome for degradation.",
            "ctx": "Cell Biology - Peroxisomal Function"
        },
        {
            "q": "A 9-year-old boy presents with numerous freckle-like hyperpigmented macules on sun-exposed areas and several cutaneous squamous cell carcinomas. Cultured skin fibroblasts are exposed to ultraviolet irradiation, and a defect in thymine dimer repair is identified. The primary defective enzyme in this patient’s condition relies on which of the following activities?",
            "options": ["Endonuclease", "Glycosylase", "DNA ligase", "Topoisomerase", "Helicase"],
            "exp": "The patient has xeroderma pigmentosum, an autosomal recessive condition characterized by a defect in nucleotide excision repair (NER), preventing the repair of pyrimidine dimers. NER typically begins with an endonuclease complex (uvrABC exinuclease in prokaryotes, specific endonucleases in eukaryotes) that cleaves the damaged DNA strand on both sides of the lesion.",
            "ctx": "Molecular Biology - DNA Repair"
        },
        {
            "q": "A 45-year-old man undergoes colonoscopy, which reveals an adenocarcinoma of the proximal colon. Family history includes a sister with endometrial cancer and a father with colon cancer at age 50. Genetic testing reveals a germline mutation that results in microsatellite instability. The wild-type version of the mutated gene normally functions by recognizing which of the following?",
            "options": ["Newly synthesized, unmethylated DNA strands", "Single-strand DNA breaks", "Double-strand DNA breaks", "Deaminated cytosine residues", "Bulky DNA adducts"],
            "exp": "The patient has Lynch syndrome (HNPCC), primarily caused by defects in mismatch repair (MMR) genes (e.g., MSH2, MLH1). In prokaryotes, MMR recognizes the newly synthesized strand because it is not yet methylated. In eukaryotes, it recognizes the new strand via nicks (from Okazaki fragments) or interactions with the replication machinery.",
            "ctx": "Genetics - Oncogenesis"
        },
        {
            "q": "A 10-year-old boy presents with progressive cerebellar ataxia, choreoathetosis, and recurrent sinopulmonary infections. Physical examination reveals telangiectasias on the conjunctivae. Laboratory testing shows elevated alpha-fetoprotein and a profound IgA deficiency. His cells demonstrate increased sensitivity to ionizing radiation. The mutated gene product in this condition is a kinase that normally signals the presence of which of the following?",
            "options": ["Double-strand DNA breaks", "Single-strand DNA breaks", "Pyrimidine dimers", "Mismatched base pairs", "Deaminated bases"],
            "exp": "The patient has ataxia-telangiectasia, caused by a mutation in the ATM (Ataxia Telangiectasia Mutated) gene. The ATM protein is a serine/threonine kinase that detects double-strand DNA breaks (caused by ionizing radiation) and activates checkpoints (via p53) and DNA repair mechanisms.",
            "ctx": "Molecular Biology - DNA Repair"
        },
        {
            "q": "A 5-year-old boy has a short stature, a sun-sensitive erythematous facial rash in a butterfly distribution, and a high-pitched voice. Cytogenetic analysis of his lymphocytes shows a markedly elevated rate of sister chromatid exchanges. The defective enzyme in this disorder typically unwinds which of the following structures during DNA replication and repair?",
            "options": ["G-quadruplexes and homologous recombination intermediates", "Nucleosomes containing histone H2A.Z", "Supercoiled DNA ahead of the replication fork", "Okazaki fragments on the lagging strand", "T-loops at the ends of linear chromosomes"],
            "exp": "The patient has Bloom syndrome, caused by mutations in the BLM gene encoding a RecQ helicase. This helicase is essential for maintaining genome stability by unwinding aberrant DNA structures such as G-quadruplexes and Holliday junctions during homologous recombination, preventing excessive sister chromatid exchanges.",
            "ctx": "Genetics - Cytogenetics"
        },
        {
            "q": "A 7-year-old girl is found to have aplastic anemia, short stature, absent radii, and hyperpigmented patches on her skin. Chromosomal breakage analysis using diepoxybutane shows increased radial chromosomes and breaks. The protein complex defective in this disorder normally acts to repair which of the following types of DNA damage?",
            "options": ["Interstrand crosslinks", "Double-strand breaks", "Bulky adducts", "Thymine dimers", "Apurinic sites"],
            "exp": "The patient has Fanconi anemia, an autosomal recessive condition characterized by bone marrow failure and physical anomalies. The Fanconi anemia pathway is specifically required for the repair of DNA interstrand crosslinks (ICLs) via a complex interplay of nucleases, translesion polymerases, and homologous recombination.",
            "ctx": "Molecular Biology - DNA Repair"
        },
        {
            "q": "A 1-year-old child presents with failure to thrive, microcephaly, deep-set eyes, and severe photosensitivity without an increased risk for skin cancer. Skin biopsy fibroblasts show a defect in the resumption of RNA synthesis following UV irradiation. The affected pathway in this disease typically recruits repair machinery to which of the following?",
            "options": ["Actively transcribed DNA strands", "Silent heterochromatin", "The newly synthesized DNA strand", "Replication fork origins", "Centromeric satellite DNA"],
            "exp": "The patient has Cockayne syndrome, characterized by a defect in transcription-coupled repair (TCR), a sub-pathway of nucleotide excision repair (NER). ERCC6 (CSB) and ERCC8 (CSA) mutations prevent the repair machinery from removing lesions that stall RNA polymerase II on actively transcribed DNA strands.",
            "ctx": "Molecular Biology - Transcription"
        },
        {
            "q": "A 40-year-old woman is diagnosed with triple-negative breast cancer. Her mother had ovarian cancer at age 45. Genetic testing confirms a BRCA1 mutation. The BRCA1 protein functions in complex with BRCA2 and RAD51 to maintain genomic stability through which of the following mechanisms?",
            "options": ["Homologous recombination", "Non-homologous end joining", "Nucleotide excision repair", "Base excision repair", "Mismatch repair"],
            "exp": "BRCA1 and BRCA2 are essential for homologous recombination (HR), an error-free mechanism for repairing double-strand DNA breaks that relies on using an undamaged sister chromatid as a template.",
            "ctx": "Molecular Biology - DNA Repair"
        },
        {
            "q": "A 28-year-old man inadvertently consumed Amanita phalloides mushrooms while foraging. He developed severe abdominal pain and diarrhea, progressing to acute liver failure over 3 days. The toxin responsible for this condition exerts its effect by binding directly to an enzyme and halting the synthesis of which of the following?",
            "options": ["Messenger RNA (mRNA)", "Ribosomal RNA (rRNA)", "Transfer RNA (tRNA)", "Small nuclear RNA (snRNA)", "Micro RNA (miRNA)"],
            "exp": "Alpha-amanitin, the toxin in Amanita phalloides (death cap mushrooms), tightly binds and inhibits RNA polymerase II. RNA polymerase II is responsible for synthesizing mRNA. Inhibition of mRNA synthesis halts protein production, leading to cell death, particularly in hepatocytes and renal cells.",
            "ctx": "Molecular Biology - Transcription"
        },
        {
            "q": "A 34-year-old woman presents with joint pain, a malar rash, and proteinuria. Serologic testing reveals high titers of anti-Smith (anti-Sm) antibodies. The targets of these autoantibodies are ribonucleoproteins normally found in the nucleus. What is the primary function of the molecular complex targeted by these antibodies?",
            "options": ["Removal of introns from primary transcripts", "Addition of the 5' cap to mRNA", "Polyadenylation of the 3' end of mRNA", "Transport of mRNA out of the nucleus", "Initiation of translation on the ribosome"],
            "exp": "Anti-Smith antibodies are highly specific for Systemic Lupus Erythematosus (SLE). They target snRNPs (small nuclear ribonucleoproteins), which are the essential components of the spliceosome. The spliceosome is responsible for removing introns from pre-mRNA (primary transcripts).",
            "ctx": "Molecular Biology - RNA Processing"
        },
        {
            "q": "A 6-month-old infant presents with severe hypotonia, absent deep tendon reflexes, and fasciculations of the tongue. The parents note a progressive decline in motor milestones. Genetic analysis confirms a homozygous deletion in the SMN1 gene. The product of this gene normally functions in the assembly of a complex essential for which of the following processes?",
            "options": ["Pre-mRNA splicing", "rRNA transcription", "tRNA charging", "Protein folding", "Vesicle fusion"],
            "exp": "The patient has Spinal Muscular Atrophy (SMA), caused by mutations in the SMN1 (survival motor neuron) gene. The SMN protein plays a critical role in the biogenesis and assembly of small nuclear ribonucleoproteins (snRNPs). Defective snRNP assembly impairs pre-mRNA splicing, which particularly affects lower motor neurons.",
            "ctx": "Molecular Biology - RNA Processing"
        },
        {
            "q": "A 24-year-old male presents with recurrent sinusitis, chronic cough with purulent sputum, and infertility. Chest radiograph shows dextrocardia. A biopsy of respiratory mucosa is analyzed by electron microscopy. A defect in which of the following structural components is most likely present?",
            "options": ["Dynein arms", "Nexin links", "Radial spokes", "Basal bodies", "Kinesin motors"],
            "exp": "The patient has Kartagener syndrome (primary ciliary dyskinesia with situs inversus). The condition is most commonly caused by mutations affecting the dynein arms of cilia and flagella, leading to immotile cilia, which explains the respiratory infections (poor mucociliary clearance), infertility (immotile sperm), and dextrocardia (defective ciliary currents during embryogenesis).",
            "ctx": "Cellular Biology - Cytoskeleton"
        },
        {
            "q": "A 3-year-old girl with partial albinism presents with a severe staphylococcal skin infection. Peripheral blood smear shows giant granules in neutrophils and eosinophils. The patient is subsequently found to have a mutation in the LYST gene. The pathogenesis of this disorder involves impaired function of which of the following cellular components?",
            "options": ["Microtubules", "Microfilaments", "Intermediate filaments", "Centrosomes", "Myosin"],
            "exp": "The patient has Chediak-Higashi syndrome, caused by a mutation in the LYST (lysosomal trafficking regulator) gene. This defect results in microtubule dysfunction, leading to failure of phagosome-lysosome fusion, which causes the giant granules in leukocytes and immunodeficiency.",
            "ctx": "Cellular Biology - Vesicular Transport"
        },
        {
            "q": "A newborn presents with extensive blistering of the skin on the hands and feet after mild friction from handling. A skin biopsy reveals cleavage within the basal layer of the epidermis, above the basement membrane. Genetic testing reveals a mutation in keratin 5. The mutated protein normally assembles into which of the following cytoskeletal elements?",
            "options": ["Intermediate filaments", "Actin microfilaments", "Microtubules", "Thick filaments", "Septins"],
            "exp": "The patient has Epidermolysis bullosa simplex, caused by mutations in keratin 5 or keratin 14. Keratins form intermediate filaments, which provide structural integrity to epithelial cells. Mutations lead to blistering within the basal layer of the epidermis upon mechanical stress.",
            "ctx": "Cellular Biology - Cytoskeleton"
        },
        {
            "q": "A 6-year-old boy is evaluated for delayed speech, macrocephaly, and long facies with prominent ears. Further evaluation later in life reveals macroorchidism. Molecular analysis of the FMR1 gene reveals >200 CGG repeats. The abnormal repeat expansion in this gene leads to silencing of transcription through which of the following primary mechanisms?",
            "options": ["DNA methylation of the promoter region", "Nonsense-mediated mRNA decay", "Impaired binding of the ribosome", "Premature termination of transcription", "Blockade of nuclear export of the mRNA"],
            "exp": "The patient has Fragile X syndrome. The expansion of the CGG trinucleotide repeat in the 5' untranslated region of the FMR1 gene to >200 copies (full mutation) leads to hypermethylation of the promoter and the repeat region. This epigenetic modification condenses the chromatin, silencing FMR1 transcription.",
            "ctx": "Genetics - Epigenetics"
        },
        {
            "q": "A 40-year-old man presents with progressive choreiform movements, depression, and cognitive decline. Genetic testing reveals a CAG repeat expansion in the HTT gene. The resulting mutant huntingtin protein binds tightly to CBP (CREB-binding protein), disrupting its normal function. What is the physiological role of CBP that is lost in this disease model?",
            "options": ["Histone acetylation", "DNA methylation", "Histone deacetylation", "RNA polymerase processivity", "Spliceosome assembly"],
            "exp": "In Huntington's disease, the mutant huntingtin protein contains an expanded polyglutamine tract that binds and sequesters CREB-binding protein (CBP). CBP normally has histone acetyltransferase (HAT) activity. Loss of CBP function leads to decreased histone acetylation, increased chromatin condensation, and transcriptional silencing of neurotrophic factors like BDNF.",
            "ctx": "Molecular Biology - Transcription"
        },
        {
            "q": "A 12-year-old boy presents with progressive gait ataxia, frequent falls, and high plantar arches. Echocardiography reveals hypertrophic cardiomyopathy. Genetic analysis shows a GAA trinucleotide repeat expansion in the FXN gene. The protein encoded by this gene is normally involved in the regulation of which of the following intracellular processes?",
            "options": ["Iron-sulfur cluster biosynthesis", "Calcium sequestration in the sarcoplasmic reticulum", "Nuclear export of pre-mRNA", "Peroxisomal very long-chain fatty acid oxidation", "Lysosomal degradation of glycosaminoglycans"],
            "exp": "The patient has Friedreich ataxia, caused by a GAA expansion in the FXN gene. Frataxin is a mitochondrial protein essential for iron-sulfur cluster biosynthesis. Deficiency leads to mitochondrial iron accumulation, oxidative stress, and impaired ATP production.",
            "ctx": "Cellular Biology - Mitochondria"
        },
        {
            "q": "A 35-year-old man presents with progressive muscle weakness and difficulty releasing his grip after shaking hands. Physical examination reveals frontal balding, temporal muscle wasting, and cataracts. Molecular analysis reveals a CTG trinucleotide repeat expansion. The pathogenesis of this disorder involves the mutant transcript sequestering muscleblind-like proteins, leading to widespread abnormalities in which of the following?",
            "options": ["Alternative splicing of pre-mRNAs", "Polyadenylation of pre-mRNAs", "5' capping of primary transcripts", "MicroRNA-mediated translational repression", "Ribosomal frameshifting during translation"],
            "exp": "Myotonic dystrophy type 1 (Steinert disease) is caused by a CTG repeat expansion in the DMPK gene. The expanded CUG repeats in the transcribed mRNA form hairpins that sequester RNA-binding proteins like muscleblind-like 1 (MBNL1), leading to widespread misregulation of alternative splicing (e.g., in the chloride channel CLCN1, causing myotonia).",
            "ctx": "Molecular Biology - RNA Processing"
        },
        {
            "q": "A 16-year-old girl presents with short stature, generalized tonic-clonic seizures, and stroke-like episodes. A muscle biopsy shows ragged red fibers with the modified Gomori trichrome stain. The specific mutation in this syndrome most frequently occurs in the mitochondrial gene encoding which of the following?",
            "options": ["tRNA-Leucine", "Cytochrome b", "ATP synthase subunit 6", "tRNA-Lysine", "NADH dehydrogenase subunit 1"],
            "exp": "The patient has MELAS (Mitochondrial Encephalomyopathy, Lactic Acidosis, and Stroke-like episodes). Approximately 80% of MELAS cases are caused by an A3243G point mutation in the mitochondrial MT-TL1 gene, which encodes the mitochondrial tRNA for Leucine (tRNA-Leu).",
            "ctx": "Genetics - Mitochondrial Inheritance"
        },
        {
            "q": "A 9-month-old infant is evaluated for failure to thrive and severe megaloblastic anemia that does not respond to vitamin B12 or folate. Urinalysis shows a striking accumulation of orotic acid. Blood ammonia levels are strictly normal. This patient's condition is due to a defect in an enzyme complex that ultimately produces which of the following nucleotides?",
            "options": ["Uridine monophosphate (UMP)", "Adenosine monophosphate (AMP)", "Inosine monophosphate (IMP)", "Guanosine monophosphate (GMP)", "Thymidine monophosphate (TMP)"],
            "exp": "The patient has Orotic aciduria, an autosomal recessive disorder of de novo pyrimidine synthesis caused by a defect in UMP synthase. UMP synthase normally converts orotic acid into UMP. The lack of pyrimidines causes megaloblastic anemia.",
            "ctx": "Biochemistry - Nucleotide Metabolism"
        },
        {
            "q": "A 25-year-old woman is diagnosed with an invasive ductal carcinoma of the breast. She previously had an osteosarcoma at age 15, and her father died of a glioblastoma at age 35. Genetic testing reveals a mutation in a tumor suppressor gene. The wild-type product of this gene typically arrests the cell cycle at the G1/S checkpoint by inducing the transcription of which of the following?",
            "options": ["p21", "Retinoblastoma protein (Rb)", "Cyclin E", "E2F transcription factor", "Bcl-2"],
            "exp": "The patient has Li-Fraumeni syndrome, resulting from an inherited mutation in TP53. The wild-type p53 protein acts as a transcription factor in response to DNA damage, upregulating the cyclin-dependent kinase inhibitor p21. p21 inhibits CDK/cyclin complexes, preventing the phosphorylation of Rb and arresting the cell cycle at G1/S.",
            "ctx": "Cellular Biology - Cell Cycle"
        },
        {
            "q": "An 18-month-old boy is diagnosed with bilateral retinoblastoma. Genetic analysis confirms an inherited germline mutation in the RB1 gene. The wild-type Retinoblastoma (Rb) protein normally acts to inhibit progression from the G1 to the S phase of the cell cycle by physically binding to and sequestering which of the following?",
            "options": ["E2F transcription factor", "Cyclin D", "CDK4", "p53", "c-Myc"],
            "exp": "The Rb protein is a critical tumor suppressor that regulates the G1/S checkpoint. In its hypophosphorylated (active) state, Rb binds to and sequesters the E2F transcription factor, preventing E2F from transcribing genes required for DNA synthesis (S phase). When hyperphosphorylated by CDK4/Cyclin D, Rb releases E2F.",
            "ctx": "Cellular Biology - Cell Cycle"
        },
        {
            "q": "A 9-month-old infant of Ashkenazi Jewish descent presents with developmental regression, exaggerated startle response to loud noises, and a 'cherry-red' spot on the macula. Hepatomegaly is absent. A defect in the alpha subunit of hexosaminidase A is confirmed. What specific substrate accumulates in the neuronal lysosomes of this patient?",
            "options": ["GM2 ganglioside", "Sphingomyelin", "Glucocerebroside", "Galactocerebroside", "Ceramide trihexoside"],
            "exp": "The patient has Tay-Sachs disease, caused by a deficiency in Hexosaminidase A. This enzyme is responsible for cleaving the terminal N-acetylgalactosamine from GM2 ganglioside. The accumulation of GM2 ganglioside in neurons leads to progressive neurodegeneration.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 1-year-old boy presents with failure to thrive, progressive hepatosplenomegaly, and loss of motor skills. Fundoscopy reveals a bilateral 'cherry-red' macula. Bone marrow aspirate shows numerous lipid-laden macrophages with a 'foamy' appearance. The enzyme deficient in this patient is normally responsible for cleaving a structural lipid to yield which of the following products?",
            "options": ["Ceramide and phosphorylcholine", "Sphingosine and galactose", "Ceramide and glucose", "Sphingosine and a fatty acid", "Ceramide and galactose"],
            "exp": "The patient has Niemann-Pick disease (Type A), caused by a deficiency in sphingomyelinase. Sphingomyelinase normally hydrolyzes sphingomyelin to yield ceramide and phosphorylcholine. The accumulation of sphingomyelin causes the foamy macrophages and organomegaly.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 30-year-old man presents with bone pain, easy bruising, and marked hepatosplenomegaly. Radiography reveals an 'Erlenmeyer flask' deformity of the distal femurs. A bone marrow biopsy shows macrophages with a fibrillary, 'crumpled tissue paper' appearance. What is the normal physiological function of the enzyme deficient in this patient?",
            "options": ["Hydrolysis of glucocerebroside to ceramide and glucose", "Hydrolysis of galactocerebroside to ceramide and galactose", "Cleavage of sulfate from cerebroside sulfate", "Cleavage of alpha-galactosidic linkages in globotriaosylceramide", "Transfer of a carbohydrate residue to ceramide"],
            "exp": "The patient has Gaucher disease, the most common lysosomal storage disorder, caused by a deficiency of glucocerebrosidase (beta-glucosidase). This enzyme hydrolyzes glucocerebroside into ceramide and glucose.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 6-month-old infant presents with irritability, extreme hypertonia, and an unexplained fever. Over the next few weeks, the infant develops optic atrophy, profound developmental regression, and feeding difficulties. An MRI shows diffuse demyelination. The deficient enzyme in this leukodystrophy normally degrades a lipid prominent in myelin. Which lipid accumulates?",
            "options": ["Galactocerebroside", "Glucocerebroside", "Cerebroside sulfate", "Sphingomyelin", "GM1 ganglioside"],
            "exp": "The infant has Krabbe disease (globoid cell leukodystrophy), an autosomal recessive disorder caused by a deficiency of galactocerebrosidase. This leads to the accumulation of galactocerebroside and its toxic derivative, psychosine, which destroys oligodendrocytes and causes severe demyelination.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 2-year-old boy previously walking independently presents with frequent falls, spasticity, and peripheral neuropathy. Metachromatic granules are found in Schwann cells on nerve biopsy. The pathogenesis of this disorder involves a failure to remove a functional group from a membrane sphingolipid. The deficient enzyme is:",
            "options": ["Arylsulfatase A", "Alpha-galactosidase A", "Beta-galactosidase", "Iduronate sulfatase", "Heparan N-sulfatase"],
            "exp": "The patient has Metachromatic leukodystrophy, caused by a deficiency of Arylsulfatase A. This enzyme normally removes the sulfate group from cerebroside sulfate (sulfatide). Accumulation of sulfatides causes central and peripheral demyelination, and the sulfatides form metachromatic granules.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 16-year-old boy presents with episodic burning pain in his hands and feet, decreased sweating, and small dark red macules on his umbilicus and thighs. Urinalysis reveals proteinuria. The defective enzyme in this X-linked recessive disorder normally cleaves the terminal galactose from which of the following?",
            "options": ["Ceramide trihexoside (Globotriaosylceramide)", "GM1 ganglioside", "Galactosylceramide", "Lactosylceramide", "Chondroitin sulfate"],
            "exp": "The patient has Fabry disease, an X-linked recessive deficiency of alpha-galactosidase A. This enzyme normally hydrolyzes ceramide trihexoside (globotriaosylceramide, Gb3), which progressively accumulates in the endothelial cells of the kidneys, heart, and skin.",
            "ctx": "Biochemistry - Lysosomal Storage"
        },
        {
            "q": "A 55-year-old woman presents with flaccid, easily ruptured blisters in her oral mucosa and on her chest. Gentle rubbing of unaffected skin causes blister formation (positive Nikolsky sign). Immunofluorescence shows a net-like pattern of IgG deposition between epidermal cells. The autoantibodies in this condition target proteins that normally connect to which cytoskeletal filaments?",
            "options": ["Intermediate filaments", "Actin microfilaments", "Microtubules", "Thick filaments", "Septins"],
            "exp": "The patient has Pemphigus vulgaris, caused by IgG autoantibodies against desmoglein 1 and 3, which are cadherins found in desmosomes. Desmosomes normally anchor cells to one another by connecting to the intermediate filaments (keratin) within the cytoplasm.",
            "ctx": "Cellular Biology - Cell Junctions"
        },
        {
            "q": "A 70-year-old man presents with tense blisters on his abdomen and inner thighs. The blisters do not easily rupture (negative Nikolsky sign). Direct immunofluorescence reveals linear IgG deposition along the epidermal basement membrane. The targeted structures in this condition normally mediate cellular adhesion to which extracellular matrix component?",
            "options": ["Laminin", "Hyaluronic acid", "Elastin", "Fibrillin", "Chondroitin sulfate"],
            "exp": "The patient has Bullous pemphigoid, caused by autoantibodies against hemidesmosomal proteins (BP180 and BP230). Hemidesmosomes attach the basal keratinocytes to the underlying basement membrane by binding to laminin-5 and collagen type IV.",
            "ctx": "Cellular Biology - Cell Junctions"
        },
        {
            "q": "A newborn is found to have multiple long bone fractures and a blue hue to the sclerae. The genetic defect responsible for this condition usually involves a mutation in COL1A1 or COL1A2. The mutation most commonly involves the substitution of a bulky amino acid for which of the following residues, disrupting the triple helix?",
            "options": ["Glycine", "Proline", "Lysine", "Hydroxyproline", "Alanine"],
            "exp": "The patient has Osteogenesis Imperfecta (Type I collagen defect). The collagen triple helix consists of a repeating (Gly-X-Y) pattern. Glycine, the smallest amino acid, is positioned in the tightly packed center of the triple helix. A missense mutation substituting a bulkier amino acid for glycine prevents normal helical assembly.",
            "ctx": "Biochemistry - Extracellular Matrix"
        },
        {
            "q": "A 25-year-old man is brought to the emergency department after a sudden onset of severe abdominal pain. CT imaging reveals a ruptured berry aneurysm. His skin is translucent, and he has a history of easy bruising but normal joint mobility. A defect in the synthesis of which type of collagen is most likely responsible?",
            "options": ["Type III", "Type I", "Type II", "Type IV", "Type V"],
            "exp": "The patient has the vascular type of Ehlers-Danlos syndrome (Type IV EDS), which is caused by a defect in Type III collagen. Type III collagen is a crucial structural component of blood vessels, hollow organs (uterus, intestines), and granulation tissue. Mutations lead to spontaneous arterial and bowel ruptures.",
            "ctx": "Biochemistry - Extracellular Matrix"
        },
        {
            "q": "A 20-year-old contortionist presents with multiple joint dislocations. His skin is hyperextensible and feels exceptionally soft and doughy. He is diagnosed with the classical type of Ehlers-Danlos syndrome. This phenotype is most often caused by a mutation affecting which of the following?",
            "options": ["Type V collagen", "Elastin", "Fibrillin-1", "Lysyl oxidase", "Procollagen peptidase"],
            "exp": "Classical Ehlers-Danlos syndrome is most commonly caused by mutations in COL5A1 or COL5A2, which encode Type V collagen. Type V collagen plays a critical role in regulating the assembly and diameter of Type I collagen fibrils in the skin and tendons.",
            "ctx": "Biochemistry - Extracellular Matrix"
        },
        {
            "q": "A 9-month-old infant presents with developmental delay, hypotonia, and sparse, brittle, 'kinky' hair. Serum copper and ceruloplasmin levels are markedly low. The defective protein in this condition is an ATP-dependent transporter. The structural symptoms are primarily due to the inactivity of which of the following copper-dependent enzymes?",
            "options": ["Lysyl oxidase", "Cytochrome c oxidase", "Tyrosinase", "Dopamine beta-hydroxylase", "Superoxide dismutase"],
            "exp": "The patient has Menkes disease, an X-linked recessive disorder caused by a mutation in ATP7A, leading to defective intestinal copper absorption. The deficiency of copper impairs several enzymes. The brittle hair and connective tissue defects are caused by decreased activity of lysyl oxidase, which requires copper to cross-link collagen and elastin.",
            "ctx": "Biochemistry - Trace Elements"
        },
        {
            "q": "A 22-year-old basketball player is evaluated for sudden-onset chest pain. He is exceptionally tall with long limbs, arachnodactyly, and a highly arched palate. Echocardiography shows aortic root dilatation. The primary molecular defect in this syndrome involves a glycoprotein that normally provides a scaffold for which of the following molecules?",
            "options": ["Tropoelastin", "Procollagen", "Fibronectin", "Laminin", "Hyaluronic acid"],
            "exp": "The patient has Marfan syndrome, caused by mutations in the FBN1 gene encoding fibrillin-1. Fibrillin-1 is a widespread extracellular matrix glycoprotein that forms microfibrils. These microfibrils act as a structural scaffold onto which tropoelastin is deposited to form mature elastic fibers.",
            "ctx": "Biochemistry - Extracellular Matrix"
        },
        {
            "q": "A 5-year-old girl is evaluated for developmental delay, hypercalcemia, and a heart murmur. She is extremely friendly and talkative with strangers. Echocardiography demonstrates supravalvular aortic stenosis. The pathogenesis of this condition involves a chromosomal microdeletion that includes the gene for which of the following proteins?",
            "options": ["Elastin", "Fibrillin-1", "Type I collagen", "Dystrophin", "Neurofibromin"],
            "exp": "The patient has Williams syndrome, caused by a microdeletion on chromosome 7q11.23. This region includes the elastin (ELN) gene. Loss of elastin haplosufficiency is directly responsible for the vascular abnormalities, particularly supravalvular aortic stenosis.",
            "ctx": "Genetics - Microdeletions"
        },
        {
            "q": "Human stem cells have the ability to continuously divide without undergoing senescence. This immortal replication is dependent on the activity of a specific ribonucleoprotein complex. The catalytic subunit of this enzyme complex is best classified as which of the following?",
            "options": ["Reverse transcriptase", "DNA-dependent RNA polymerase", "RNA-dependent RNA polymerase", "Endonuclease", "Exonuclease"],
            "exp": "The enzyme is telomerase (TERT - Telomerase Reverse Transcriptase), which maintains telomere length in stem cells, germ cells, and cancer cells. It uses a built-in RNA template (TERC) to synthesize telomeric DNA repeats (TTAGGG) onto the 3' ends of linear chromosomes, acting as an RNA-dependent DNA polymerase (a reverse transcriptase).",
            "ctx": "Molecular Biology - DNA Replication"
        },
        {
            "q": "A 7-year-old unvaccinated boy develops a grey pseudomembrane over his tonsils and posterior pharynx, accompanied by a 'bull-neck' appearance due to lymphadenopathy. The exotoxin produced by the causative organism inhibits protein synthesis in host cells by catalyzing the transfer of an ADP-ribose group to which of the following targets?",
            "options": ["Elongation factor 2 (eEF-2)", "The 60S ribosomal subunit", "The 40S ribosomal subunit", "Initiation factor 2 (eIF-2)", "RNA polymerase II"],
            "exp": "Corynebacterium diphtheriae produces diphtheria toxin, an A-B exotoxin. The A subunit catalyzes the ADP-ribosylation of eukaryotic elongation factor 2 (eEF-2). This inactivates eEF-2, preventing the translocation step of translation, halting protein synthesis and causing cell death. Pseudomonas Exotoxin A has the same mechanism.",
            "ctx": "Molecular Biology - Translation"
        },
        {
            "q": "A 6-year-old girl presents with bloody diarrhea followed by oliguria and pallor. Laboratory results show hemolytic anemia, thrombocytopenia, and elevated creatinine. A stool culture grows Escherichia coli O157:H7. The toxin responsible for her renal failure halts protein synthesis by which of the following mechanisms?",
            "options": ["Cleaving a specific adenine base from the 28S rRNA", "ADP-ribosylating the Gs alpha subunit", "Inhibiting the peptidyl transferase activity of the 50S subunit", "Preventing the binding of aminoacyl-tRNA to the A site", "Phosphorylating initiation factor eIF-2"],
            "exp": "The patient has Hemolytic Uremic Syndrome (HUS) caused by Shiga-like toxin (Verotoxin) produced by EHEC. Shiga toxin and Shiga-like toxin are N-glycosidases that cleave a specific adenine nucleobase from the 28S rRNA of the eukaryotic 60S ribosomal subunit. This depurination prevents the binding of elongation factors, halting translation.",
            "ctx": "Molecular Biology - Translation"
        },
        {
            "q": "In a molecular biology laboratory, researchers are studying the translation of an integral membrane protein. They observe that as the nascent polypeptide emerges from the ribosome, translation pauses temporarily. Which of the following molecules is responsible for binding the signal sequence and arresting translation until the ribosome docks at the endoplasmic reticulum?",
            "options": ["Signal recognition particle (SRP)", "Chaperonin (Hsp60)", "Coatomer protein II (COPII)", "Clathrin", "BiP (Binding immunoglobulin protein)"],
            "exp": "The signal recognition particle (SRP) is a ribonucleoprotein that recognizes and binds to the hydrophobic N-terminal signal sequence of nascent secretory and membrane proteins as they emerge from the ribosome. SRP binding pauses translation until the SRP-ribosome complex docks with the SRP receptor on the rough endoplasmic reticulum (RER).",
            "ctx": "Molecular Biology - Protein Trafficking"
        },
        {
            "q": "A familial hypercholesterolemia phenotype can result from mutations in the LDL receptor. Normally, when LDL binds to its receptor on the cell surface, the receptor-ligand complex internalizes via coated pits. Which of the following coat proteins specifically mediates this endocytic pathway from the plasma membrane?",
            "options": ["Clathrin", "COPII", "COPI", "Caveolin", "Dynamin"],
            "exp": "Receptor-mediated endocytosis of molecules like LDL and transferrin occurs via clathrin-coated pits. Clathrin assembles on the cytoplasmic face of the plasma membrane, invaginating it to form a vesicle. COPI and COPII mediate vesicular transport between the Golgi and the ER.",
            "ctx": "Cellular Biology - Vesicular Transport"
        },
        {
            "q": "Tetanus toxin causes spastic paralysis by preventing the release of inhibitory neurotransmitters (GABA and glycine) from Renshaw cells in the spinal cord. The toxin acts as a zinc endopeptidase. What is the specific target of its proteolytic activity?",
            "options": ["SNARE proteins (e.g., synaptobrevin)", "Voltage-gated calcium channels", "Nicotinic acetylcholine receptors", "Acetylcholinesterase", "GABA receptors"],
            "exp": "Tetanus toxin (and botulinum toxin) cleaves SNARE proteins (specifically synaptobrevin, a v-SNARE). SNARE proteins are essential for the fusion of neurotransmitter-containing synaptic vesicles with the presynaptic membrane. By destroying SNAREs, tetanus toxin blocks the exocytosis of inhibitory neurotransmitters.",
            "ctx": "Cellular Biology - Vesicular Transport"
        },
        {
            "q": "A cell biological study is conducted on the sorting of acid hydrolases to lysosomes. A specific tag is required for these enzymes to be recognized by receptors in the trans-Golgi network. The addition of this tag occurs in the cis-Golgi. Which of the following sugar derivatives constitutes this critical sorting signal?",
            "options": ["Mannose-6-phosphate", "Glucose-1-phosphate", "N-acetylneuraminic acid", "Fructose-6-phosphate", "Galactose-1-phosphate"],
            "exp": "Lysosomal hydrolases are tagged with a mannose-6-phosphate (M6P) residue in the cis-Golgi. This tag allows them to bind M6P receptors in the trans-Golgi network, which then package them into clathrin-coated vesicles destined for the endosomes and ultimately the lysosomes. A defect here causes I-cell disease.",
            "ctx": "Molecular Biology - Protein Trafficking"
        },
        {
            "q": "Proteins that function in the endoplasmic reticulum (ER), such as protein disulfide isomerase, occasionally escape into the Golgi apparatus and must be retrieved. This retrograde transport is mediated by vesicles that recognize a specific C-terminal signal sequence (KDEL) on the escaped proteins. Which of the following coat proteins directs this retrograde trafficking?",
            "options": ["COPI", "COPII", "Clathrin", "Adaptin", "Caveolin"],
            "exp": "COPI (Coatomer protein I) mediates retrograde vesicular transport from the Golgi back to the ER (e.g., for retrieving KDEL-tagged ER resident proteins) and between Golgi cisternae. COPII mediates anterograde transport from the ER to the Golgi.",
            "ctx": "Cellular Biology - Vesicular Transport"
        },
        {
            "q": "Apoptosis can be initiated by either intrinsic or extrinsic pathways. The intrinsic pathway is highly dependent on mitochondrial integrity. Which of the following molecules is released from the mitochondrial intermembrane space into the cytosol to trigger the assembly of the apoptosome?",
            "options": ["Cytochrome c", "Bcl-2", "Bax", "Caspase-8", "Fas ligand"],
            "exp": "During the intrinsic pathway of apoptosis, mitochondrial permeability transition pore opens. This allows cytochrome c to escape from the inner mitochondrial space into the cytosol. Cytochrome c binds to APAF-1, forming the apoptosome, which activates caspase-9.",
            "ctx": "Cellular Biology - Apoptosis"
        },
        {
            "q": "A 50-year-old woman with a history of melanoma is treated with a specific inhibitor of the BRAF V600E mutation (Vemurafenib). BRAF is a serine/threonine kinase that forms part of a major signal transduction pathway regulating cell growth. Which of the following is the direct upstream activator of BRAF in this pathway?",
            "options": ["Ras", "Receptor tyrosine kinase (RTK)", "MEK", "ERK", "Phosphoinositide 3-kinase (PI3K)"],
            "exp": "BRAF is a kinase in the MAPK/ERK signaling pathway. When a growth factor binds a receptor tyrosine kinase (RTK), the RTK activates Ras (a small G-protein). Active GTP-bound Ras directly recruits and activates RAF (e.g., BRAF). RAF then phosphorylates MEK, which phosphorylates ERK. Thus, Ras is the direct upstream activator of BRAF.",
            "ctx": "Cellular Biology - Signal Transduction"
        }
    ]

    target_counts = {'A': 10, 'B': 10, 'C': 10, 'D': 10, 'E': 10}
    letters = ['A', 'B', 'C', 'D', 'E']
    assignments = []
    for l in letters:
        assignments.extend([l]*10)
    
    random.seed(42)
    random.shuffle(assignments)

    mcqs = []
    for i, data in enumerate(questions_data):
        correct_letter = assignments[i]
        correct_idx = letters.index(correct_letter)
        
        options = data['options']
        correct_opt = options[0]
        wrong_opts = options[1:]
        random.shuffle(wrong_opts)
        
        final_options = []
        for j in range(5):
            if j == correct_idx:
                final_options.append(correct_opt)
            else:
                final_options.append(wrong_opts.pop())
                
        mcqs.append({
            "question": data['q'],
            "option_a": final_options[0],
            "option_b": final_options[1],
            "option_c": final_options[2],
            "option_d": final_options[3],
            "option_e": final_options[4],
            "correct_answer": correct_letter,
            "explanation": data['exp'],
            "source_context": data['ctx']
        })

    output_path = r"E:\USAMA\MBBS Books\MCQ_Generator\batches\bank_batch_molbio.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(mcqs, f, indent=2)

    print(f"Created JSON file with {len(mcqs)} MCQs.")

if __name__ == '__main__':
    generate_mcqs()
