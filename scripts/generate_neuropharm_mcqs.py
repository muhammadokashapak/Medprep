import json

raw_data = [
    # A (1-10)
    {
        "q": "A 34-year-old woman with a history of refractory complex partial seizures is started on a novel antiepileptic drug that acts primarily as a selective, non-competitive antagonist at AMPA receptors. Six months later, she presents to the emergency department with profound aggressive behavior, homicidal ideation, and severe mood changes. Which of the following drugs is most likely responsible, and what is its specific molecular target?",
        "correct": "Perampanel; postsynaptic AMPA glutamate receptors",
        "distractors": [
            "Brivaracetam; synaptic vesicle protein 2A (SV2A)",
            "Felbamate; NMDA glutamate receptors",
            "Rufinamide; voltage-gated sodium channels",
            "Tiagabine; GAT-1 GABA transporter"
        ],
        "ans": "A",
        "exp": "Perampanel is a highly selective, non-competitive AMPA receptor antagonist used for focal-onset seizures. It carries a black-box warning for serious psychiatric and behavioral reactions, including aggression, hostility, irritability, anger, and homicidal ideation. None of the other agents act primarily at AMPA receptors.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 28-year-old man with bipolar I disorder is stabilized on a mood stabilizer. He later presents with polyuria, polydipsia, and a serum sodium of 148 mEq/L. Urine osmolality is low and does not respond to exogenous desmopressin. At a cellular level, the offending drug induces this condition by interfering with which of the following signaling pathways in the renal collecting duct?",
        "correct": "Inhibition of glycogen synthase kinase 3-beta (GSK3β) and adenylyl cyclase, downregulating aquaporin-2",
        "distractors": [
            "Agonism of the vasopressin V2 receptor, leading to receptor downregulation",
            "Blockade of the V1a receptor, shifting vasopressin to V1b pathways",
            "Upregulation of prostaglandin E2 synthesis, enhancing urinary concentrating ability",
            "Direct inhibition of the Na-K-2Cl symporter in the thick ascending limb"
        ],
        "ans": "A",
        "exp": "The patient has lithium-induced nephrogenic diabetes insipidus. Lithium enters the principal cells of the collecting duct via ENaC channels and inhibits GSK3β and adenylyl cyclase, impairing cAMP generation. This results in decreased transcription and apical membrane insertion of aquaporin-2 (AQP2) water channels.",
        "ctx": "Psychopharmacology - Mood Stabilizers"
    },
    {
        "q": "A 45-year-old man on a psychiatric medication consumes a large plate of aged cheeses and cured meats. Hours later, he presents with a throbbing headache, diaphoresis, and a blood pressure of 210/115 mmHg. The exact mechanism by which the ingested dietary compound precipitates this crisis involves which of the following?",
        "correct": "Reversal of the norepinephrine transporter (NET) and displacement of vesicular norepinephrine",
        "distractors": [
            "Direct agonism of postsynaptic alpha-1 and beta-1 adrenergic receptors",
            "Inhibition of catechol-O-methyltransferase (COMT) in the synaptic cleft",
            "Irreversible inhibition of monoamine oxidase type B in peripheral neurons",
            "Blockade of vesicular monoamine transporter 2 (VMAT2), preventing dopamine release"
        ],
        "ans": "A",
        "exp": "The patient is taking a non-selective MAOI and consumed tyramine-rich foods. Tyramine escapes hepatic first-pass metabolism (due to MAO inhibition), enters systemic circulation, and is taken up by sympathetic nerve terminals via NET. Inside the terminal, it acts as an indirect sympathomimetic by displacing norepinephrine from synaptic vesicles, which then exits via reverse transport through NET, causing a hypertensive crisis.",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 25-year-old man with treatment-resistant schizophrenia is started on a medication that significantly improves his positive and negative symptoms but causes marked sialorrhea, particularly at night. The paradoxical hypersalivation caused by this atypical antipsychotic is most likely mediated by which of the following mechanisms?",
        "correct": "Agonism at muscarinic M4 receptors and blockade of alpha-2 adrenergic receptors",
        "distractors": [
            "Direct agonism of muscarinic M1 and M3 receptors in the salivary glands",
            "Inhibition of acetylcholinesterase in the peripheral nervous system",
            "Blockade of dopamine D2 receptors in the area postrema",
            "Histamine H1 receptor agonism combined with alpha-1 blockade"
        ],
        "ans": "A",
        "exp": "Clozapine frequently causes paradoxical sialorrhea. Although it is generally strongly anticholinergic (M1, M2, M3, M5 antagonist), it acts as a partial agonist at the M4 receptor, which is thought to stimulate salivation. Additionally, alpha-2 adrenergic blockade impairs swallowing reflexes, exacerbating drooling.",
        "ctx": "Psychopharmacology - Antipsychotics"
    },
    {
        "q": "A 55-year-old woman with chronic insomnia characterized by sleep maintenance difficulty is prescribed a medication that targets neuropeptide signaling originating in the lateral hypothalamus. This drug promotes sleep without significant next-day respiratory depression. What is the precise mechanism of action of this drug?",
        "correct": "Dual antagonism of OX1R and OX2R orexin receptors",
        "distractors": [
            "Positive allosteric modulation of the GABAA receptor complex",
            "Agonism at melatonin MT1 and MT2 receptors in the suprachiasmatic nucleus",
            "Inverse agonism at the histamine H1 receptor",
            "Selective antagonism of the serotonin 5-HT2A receptor"
        ],
        "ans": "A",
        "exp": "Suvorexant is a dual orexin receptor antagonist (DORA). It blocks the binding of wake-promoting neuropeptides orexin A and orexin B to receptors OX1R and OX2R. These neuropeptides are produced by neurons in the lateral hypothalamus.",
        "ctx": "Neuropharmacology - Sedative-Hypnotics"
    },
    {
        "q": "A 60-year-old man with a long history of haloperidol use develops severe, involuntary, repetitive movements of his mouth and tongue. He is prescribed valbenazine to manage these symptoms. Which of the following accurately describes the molecular action of this new therapy?",
        "correct": "Reversible inhibition of the vesicular monoamine transporter 2 (VMAT2)",
        "distractors": [
            "Irreversible inhibition of the vesicular monoamine transporter 1 (VMAT1)",
            "Direct antagonism of postsynaptic dopamine D2 receptors in the striatum",
            "Positive allosteric modulation of GABAA receptors in the globus pallidus",
            "Selective inhibition of the norepinephrine transporter (NET)"
        ],
        "ans": "A",
        "exp": "Valbenazine is a highly selective, reversible inhibitor of VMAT2. By inhibiting VMAT2, it prevents the packaging of dopamine into presynaptic vesicles, depleting dopamine release into the synaptic cleft and thereby reducing the hypersensitive dopaminergic signaling characteristic of tardive dyskinesia.",
        "ctx": "Psychopharmacology - Movement Disorders"
    },
    {
        "q": "A 30-year-old woman presents with severe, life-threatening postpartum depression two weeks after delivering her first child. She receives a continuous intravenous infusion of brexanolone over 60 hours. What is the specific neurochemical identity and receptor target of this drug?",
        "correct": "A synthetic analog of allopregnanolone acting as a positive allosteric modulator of synaptic and extrasynaptic GABAA receptors",
        "distractors": [
            "A selective serotonin reuptake inhibitor that rapidly downregulates 5-HT1A autoreceptors",
            "A ketamine enantiomer acting as a non-competitive antagonist at the NMDA receptor",
            "A synthetic oxytocin analog acting at peripheral and central oxytocin receptors",
            "A dual orexin receptor antagonist blocking OX1R and OX2R in the hypothalamus"
        ],
        "ans": "A",
        "exp": "Brexanolone is an exogenous formulation of allopregnanolone, a naturally occurring neuroactive steroid metabolite of progesterone. It acts as a positive allosteric modulator of GABAA receptors, specifically acting at both synaptic and extrasynaptic sites to rapidly restore GABAergic tone and improve postpartum depression.",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 40-year-old man seeking treatment for opioid use disorder is prescribed a sublingual film medication that contains both a mu-opioid receptor ligand and an antagonist. The active therapeutic ligand in this formulation has which of the following specific intrinsic receptor profiles?",
        "correct": "Partial agonism at the mu-opioid receptor and antagonism at the kappa-opioid receptor",
        "distractors": [
            "Full agonism at the mu-opioid receptor and antagonism at the delta-opioid receptor",
            "Partial agonism at both mu and kappa opioid receptors",
            "Antagonism at the mu-opioid receptor and full agonism at the kappa-opioid receptor",
            "Full agonism at the mu-opioid receptor and partial agonism at the nociceptin receptor"
        ],
        "ans": "A",
        "exp": "Buprenorphine is a unique opioid that acts as a partial agonist at the mu-opioid receptor (MOR) and an antagonist at the kappa-opioid receptor (KOR). Its high affinity for MOR displaces full agonists (like heroin) but its partial agonism provides a ceiling effect on respiratory depression. The antagonist in the film is naloxone, which is inactive sublingually.",
        "ctx": "Neuropharmacology - Opioids"
    },
    {
        "q": "A 22-year-old woman is prescribed a medication for migraine prophylaxis that is also used as a broad-spectrum antiepileptic. Six months later, routine labs reveal a non-anion gap metabolic acidosis. This adverse effect is mediated by the drug's inhibitory action on which of the following enzymes?",
        "correct": "Carbonic anhydrase in the proximal renal tubule",
        "distractors": [
            "Sodium-potassium ATPase in the distal convoluted tubule",
            "Gamma-glutamyl transferase in the hepatic biliary canaliculi",
            "Cytochrome P450 3A4 in the intestinal mucosa",
            "Monoamine oxidase type A in the peripheral nervous system"
        ],
        "ans": "A",
        "exp": "Topiramate is known to cause a non-anion gap hyperchloremic metabolic acidosis. This is due to its weak inhibitory effect on carbonic anhydrase (types II and IV) in the renal proximal tubule, leading to decreased bicarbonate reabsorption (type 2 renal tubular acidosis).",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 35-year-old woman with a history of recurrent episodic chest pain at rest, occasionally occurring early in the morning, presents to the clinic for management of severe migraines. Which of the following drug mechanisms is strictly contraindicated in this patient, and why?",
        "correct": "5-HT1B/1D agonism; due to the risk of precipitating coronary artery vasospasm",
        "distractors": [
            "Calcitonin gene-related peptide (CGRP) antagonism; due to profound systemic vasodilation",
            "Non-selective beta-adrenergic blockade; due to the risk of bronchospasm",
            "Cyclooxygenase-2 inhibition; due to the risk of altering platelet aggregation",
            "Dopamine D2 receptor antagonism; due to the risk of extrapyramidal symptoms"
        ],
        "ans": "A",
        "exp": "The patient's history of early morning resting chest pain strongly suggests Prinzmetal (variant) angina, which is caused by coronary artery vasospasm. Triptans (e.g., sumatriptan) are 5-HT1B/1D agonists used for migraines but can cause vasoconstriction. They are strictly contraindicated in patients with ischemic heart disease or coronary vasospasm.",
        "ctx": "Neuropharmacology - Migraine"
    },

    # B (11-20)
    {
        "q": "A 65-year-old man with end-stage renal disease requires potent analgesia following orthopedic surgery. He is inadvertently administered repeated high doses of a synthetic phenylpiperidine opioid. On postoperative day 3, he experiences generalized tonic-clonic seizures. The accumulation of which of the following metabolites is responsible for this neurotoxic effect?",
        "correct": "A demethylated metabolite that causes CNS excitation",
        "distractors": [
            "A glucuronidated metabolite that acts as an NMDA receptor agonist",
            "An acetylated metabolite that blocks presynaptic GABA release",
            "A sulfated metabolite that directly inhibits the sodium-potassium pump",
            "An oxidized metabolite that intensely activates the kappa-opioid receptor"
        ],
        "ans": "B",
        "exp": "Meperidine (pethidine) is a synthetic opioid metabolized in the liver to normeperidine via N-demethylation. Normeperidine is a CNS stimulant that lowers the seizure threshold and is renally excreted. In patients with renal failure, normeperidine accumulates, leading to tremors, myoclonus, and seizures. Therefore, meperidine is contraindicated in chronic or severe renal impairment.",
        "ctx": "Neuropharmacology - Opioids"
    },
    {
        "q": "A 58-year-old man treated for early-onset Parkinson's disease presents for a follow-up. His wife reports that over the past six months, he has lost $50,000 at the casino and exhibits hypersexuality. The medication most likely responsible for these behavioral changes primarily exerts its action at which of the following receptors?",
        "correct": "Agonism at dopamine D3 receptors in the mesolimbic system",
        "distractors": [
            "Agonism at dopamine D1 receptors in the nigrostriatal tract",
            "Antagonism at dopamine D2 receptors in the tuberoinfundibular pathway",
            "Inhibition of monoamine oxidase B in the presynaptic terminal",
            "Antagonism at 5-HT2A receptors in the prefrontal cortex"
        ],
        "ans": "B",
        "exp": "The patient is experiencing an impulse control disorder (ICD), a well-known side effect of dopamine agonists (e.g., pramipexole, ropinirole) used in Parkinson's disease. These non-ergot agonists have a high affinity for the dopamine D3 receptor, which is heavily concentrated in the mesolimbic system (the reward pathway), leading to pathological gambling, hypersexuality, and compulsive shopping.",
        "ctx": "Neuropharmacology - Antiparkinsonian"
    },
    {
        "q": "An infant with tuberous sclerosis complex is prescribed an antiepileptic drug for the treatment of infantile spasms. Parents are advised that the child will need serial monitoring by an ophthalmologist. The mechanism of action of the prescribed drug is characterized by which of the following?",
        "correct": "Irreversible, suicide inhibition of GABA transaminase",
        "distractors": [
            "Reversible blockade of voltage-gated T-type calcium channels",
            "Allosteric enhancement of GABAA receptor channel opening frequency",
            "Inhibition of the GAT-1 presynaptic GABA transporter",
            "Modulation of the synaptic vesicle glycoprotein 2A (SV2A)"
        ],
        "ans": "B",
        "exp": "Vigabatrin is an irreversible (suicide) inhibitor of GABA transaminase (GABA-T), the enzyme responsible for the degradation of GABA, leading to increased CNS GABA levels. It is highly effective for infantile spasms, particularly in tuberous sclerosis. However, it carries a black-box warning for permanent, bilateral visual field constriction (retinal toxicity), necessitating serial ophthalmologic monitoring.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 24-year-old trauma patient arrives at the emergency department in hemorrhagic shock. Intubation is required, and an induction agent is chosen that will support the patient's hemodynamics. This agent achieves its anesthetic effect primarily through which of the following molecular mechanisms?",
        "correct": "Non-competitive antagonism at the N-methyl-D-aspartate (NMDA) receptor",
        "distractors": [
            "Positive allosteric modulation of the GABAA receptor complex",
            "Agonism at presynaptic alpha-2 adrenergic receptors",
            "Blockade of voltage-gated sodium channels in the cerebral cortex",
            "Activation of two-pore-domain potassium channels (K2P)"
        ],
        "ans": "B",
        "exp": "Ketamine is a unique intravenous anesthetic that acts as a non-competitive NMDA receptor antagonist. Unlike most anesthetics that depress cardiovascular function (e.g., propofol, thiopental), ketamine causes sympathetic stimulation by inhibiting catecholamine reuptake, increasing heart rate, blood pressure, and cardiac output, making it ideal for induction in patients with hemorrhagic shock.",
        "ctx": "Neuropharmacology - Anesthetics"
    },
    {
        "q": "A 40-year-old man undergoes general anesthesia with sevoflurane and succinylcholine. Shortly after induction, he develops masseter muscle rigidity, tachycardia, hypercarbia, and a rapid rise in body temperature. The drug required to treat this life-threatening condition acts by directly binding to which of the following intracellular targets?",
        "correct": "The ryanodine receptor (RyR1) on the sarcoplasmic reticulum",
        "distractors": [
            "The dihydropyridine receptor (DHPR) on the T-tubule membrane",
            "The SERCA pump on the sarcoplasmic reticulum membrane",
            "The nicotinic acetylcholine receptor at the neuromuscular junction",
            "The voltage-gated calcium channels in the presynaptic terminal"
        ],
        "ans": "B",
        "exp": "The patient has developed malignant hyperthermia, triggered by volatile anesthetics and succinylcholine in genetically susceptible individuals (often due to RyR1 mutations). The treatment is dantrolene, a direct-acting muscle relaxant that binds to the ryanodine receptor (RyR1) on the sarcoplasmic reticulum, blocking calcium release and halting the hypercatabolic cascade.",
        "ctx": "Neuropharmacology - Muscle Relaxants"
    },
    {
        "q": "A 9-year-old boy in the pediatric ICU requires prolonged sedation for acute respiratory distress syndrome. On day 4 of the infusion, he develops severe metabolic acidosis, rhabdomyolysis, hepatomegaly, and bradycardia. The pathophysiology of this drug-induced syndrome is primarily linked to which of the following mechanisms?",
        "correct": "Impairment of mitochondrial fatty acid oxidation and oxidative phosphorylation",
        "distractors": [
            "Direct block of myocardial fast sodium channels leading to QRS prolongation",
            "Massive histamine release causing profound capillary leak syndrome",
            "Accumulation of active metabolites resulting in central adrenergic outflow collapse",
            "Inhibition of the cytochrome P450 system causing toxic drug-drug interactions"
        ],
        "ans": "B",
        "exp": "The presentation is classic for Propofol Infusion Syndrome (PRIS), characterized by metabolic acidosis, rhabdomyolysis, hyperkalemia, hepatomegaly, and cardiovascular collapse. It occurs with high-dose, long-term propofol infusions, particularly in children. The underlying mechanism involves propofol-induced impairment of mitochondrial respiratory chain function and inhibition of fatty acid oxidation.",
        "ctx": "Neuropharmacology - Anesthetics"
    },
    {
        "q": "A 50-year-old woman undergoes a cholecystectomy using an older halogenated inhaled anesthetic. Five days postoperatively, she presents with jaundice, fever, and markedly elevated hepatic transaminases. Liver biopsy reveals massive centrilobular necrosis. Which of the following best explains the pathogenesis of her condition?",
        "correct": "Immune-mediated reaction against trifluoroacetylated hepatic proteins",
        "distractors": [
            "Direct toxic effect of excessive intracellular calcium release",
            "Inhibition of biliary excretion leading to cholestatic injury",
            "Depletion of hepatic glutathione due to a toxic reactive metabolite",
            "Activation of toll-like receptor 4 by gut-derived endotoxins"
        ],
        "ans": "B",
        "exp": "Halothane hepatitis is a rare, severe, immune-mediated hepatotoxicity. Halothane is metabolized by CYP2E1 to trifluoroacetyl chloride, which binds to liver proteins forming trifluoroacetylated neoantigens. In susceptible individuals, upon subsequent exposure, an immune response (IgG antibodies) is mounted against these modified proteins, causing massive centrilobular necrosis.",
        "ctx": "Neuropharmacology - Anesthetics"
    },
    {
        "q": "A 10-year-old boy is diagnosed with attention-deficit/hyperactivity disorder (ADHD). Because of a strong family history of substance abuse, the psychiatrist opts for a non-stimulant medication. The selected drug exerts its therapeutic effect via which of the following principal mechanisms?",
        "correct": "Selective inhibition of the presynaptic norepinephrine transporter (NET)",
        "distractors": [
            "Direct agonism of central alpha-2A adrenergic receptors",
            "Inhibition of both dopamine and norepinephrine reuptake",
            "Increased release of vesicular catecholamines into the synapse",
            "Selective agonism of trace amine-associated receptor 1 (TAAR1)"
        ],
        "ans": "B",
        "exp": "Atomoxetine is a non-stimulant used for ADHD, preferred in cases with a risk of substance abuse or severe tics. Its mechanism of action is selective inhibition of the presynaptic norepinephrine transporter (NET). While clonidine and guanfacine are alpha-2 agonists also used for ADHD, the wording points to atomoxetine as the prototypic non-stimulant reuptake inhibitor.",
        "ctx": "Psychopharmacology - ADHD"
    },
    {
        "q": "A 32-year-old man is prescribed a highly sedating antidepressant for insomnia associated with major depressive disorder. Two weeks later, he presents to the emergency department with a painful, prolonged erection lasting over 4 hours. The receptor blockade responsible for this specific adverse effect is:",
        "correct": "Alpha-1 adrenergic receptor",
        "distractors": [
            "Serotonin 5-HT2A receptor",
            "Histamine H1 receptor",
            "Dopamine D2 receptor",
            "Muscarinic M1 receptor"
        ],
        "ans": "B",
        "exp": "The patient has priapism secondary to trazodone use. Trazodone is a serotonin antagonist and reuptake inhibitor (SARI). Its adverse effect of priapism is primarily attributed to its strong antagonistic effect on peripheral alpha-1 adrenergic receptors, which disrupts sympathetic control of penile detumescence.",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 70-year-old severely depressed woman with profound anorexia, weight loss, and insomnia is started on an atypical antidepressant. Within weeks, her mood improves, she sleeps well, and she gains 10 lbs. The weight gain and sedation caused by this medication are primarily due to antagonism at which of the following receptor pairs?",
        "correct": "Histamine H1 and serotonin 5-HT2C receptors",
        "distractors": [
            "Alpha-2 adrenergic and serotonin 5-HT3 receptors",
            "Muscarinic M1 and dopamine D2 receptors",
            "Alpha-1 adrenergic and histamine H2 receptors",
            "Serotonin 5-HT1A and melatonin MT1 receptors"
        ],
        "ans": "B",
        "exp": "Mirtazapine is an atypical antidepressant that acts by blocking alpha-2 autoreceptors and heteroreceptors (enhancing NE and 5-HT release). However, its side effects of potent sedation and significant weight gain/increased appetite are mediated by strong antagonism at histamine H1 receptors and serotonin 5-HT2C receptors.",
        "ctx": "Psychopharmacology - Antidepressants"
    },

    # C (21-30)
    {
        "q": "A 26-year-old woman with new-onset focal seizures is started on an antiepileptic drug that is notably lacking in significant drug-drug interactions, as it is minimally metabolized by the hepatic cytochrome P450 system. Its exact mechanism of action involves binding to a synaptic vesicle glycoprotein. Which of the following is the drug and its target?",
        "correct": "Levetiracetam; SV2A",
        "distractors": [
            "Lacosamide; CRMP-2",
            "Zonisamide; voltage-gated calcium channels",
            "Perampanel; AMPA receptor",
            "Gabapentin; alpha-2-delta subunit of calcium channels"
        ],
        "ans": "C",
        "exp": "Levetiracetam is a widely used broad-spectrum antiepileptic drug known for its favorable pharmacokinetic profile and lack of CYP450 interactions. It exerts its effect by binding to the synaptic vesicle glycoprotein 2A (SV2A), modulating neurotransmitter release. Lacosamide modulates slow inactivation of sodium channels and binds CRMP-2. Gabapentin binds the alpha-2-delta subunit.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 45-year-old patient with partial seizures is taking a medication that specifically targets the synaptic reuptake of the primary inhibitory neurotransmitter in the CNS. By preventing its clearance, the synaptic residence time is prolonged. This drug specifically acts by inhibiting which of the following transporters?",
        "correct": "GAT-1",
        "distractors": [
            "VMAT2",
            "EAAT1",
            "NET",
            "SERT"
        ],
        "ans": "C",
        "exp": "Tiagabine is an antiepileptic drug used as an adjunctive treatment for partial seizures. It selectively blocks GAT-1, a GABA transporter on neurons and glia, thereby inhibiting GABA reuptake from the synaptic cleft and enhancing inhibitory neurotransmission. EAAT1 is a glutamate transporter.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 7-year-old girl is brought to the pediatrician by her teacher, who notes she frequently stares blankly into space for 10-15 seconds before resuming her activities as if nothing happened. EEG shows generalized 3-Hz spike-and-wave discharges. The first-line pharmacological treatment for this condition acts primarily on which of the following structures?",
        "correct": "T-type calcium channels in thalamic relay neurons",
        "distractors": [
            "Fast voltage-gated sodium channels in the motor cortex",
            "GABAA receptor chloride channels in the limbic system",
            "NMDA receptors in the hippocampus",
            "L-type calcium channels in the cardiac myocardium"
        ],
        "ans": "C",
        "exp": "The child has absence seizures, diagnosed clinically and by the classic 3-Hz spike-and-wave EEG pattern. The first-line drug is ethosuximide, which specifically suppresses seizures by blocking low-threshold (T-type) calcium channels in the thalamic relay neurons, breaking the thalamocortical oscillatory rhythms.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 65-year-old man requests a sleep aid. He has a history of severe COPD, and his physician wants to avoid any drugs that might depress respiratory drive or alter sleep architecture. The prescribed medication operates by acting as a highly selective agonist at receptors located in the suprachiasmatic nucleus. Which of the following is the drug?",
        "correct": "Ramelteon",
        "distractors": [
            "Zolpidem",
            "Suvorexant",
            "Eszopiclone",
            "Zaleplon"
        ],
        "ans": "C",
        "exp": "Ramelteon is a melatonin receptor agonist that binds with high affinity to MT1 and MT2 receptors in the suprachiasmatic nucleus of the hypothalamus. It is unique among sedative-hypnotics because it lacks affinity for the GABAA receptor, thereby lacking respiratory depression, abuse potential, and withdrawal symptoms, making it very safe for patients with COPD.",
        "ctx": "Neuropharmacology - Sedative-Hypnotics"
    },
    {
        "q": "A 29-year-old woman with generalized anxiety disorder is prescribed a non-sedating anxiolytic that has a delayed onset of action of roughly two weeks. It does not possess muscle relaxant or anticonvulsant properties, and does not potentiate the effects of alcohol. Its mechanism of action primarily involves which of the following?",
        "correct": "Partial agonism at the serotonin 5-HT1A receptor",
        "distractors": [
            "Positive allosteric modulation of the GABAA receptor",
            "Blockade of voltage-gated calcium channels via alpha-2-delta subunit",
            "Inhibition of the serotonin transporter (SERT)",
            "Antagonism at the histamine H1 receptor"
        ],
        "ans": "C",
        "exp": "Buspirone is an anxiolytic used for generalized anxiety disorder. Unlike benzodiazepines, it does not act on GABA receptors, has no sedative, muscle relaxant, or anticonvulsant properties, and does not interact with alcohol. Its mechanism of action is functioning as a partial agonist at the 5-HT1A receptor.",
        "ctx": "Psychopharmacology - Anxiolytics"
    },
    {
        "q": "A 60-year-old man with Parkinson's disease is treated with a medication that, at low doses, selectively inhibits an enzyme responsible for dopamine degradation in the striatum without restricting his diet. However, he is warned that if the dose is increased, the drug loses its selectivity, posing a risk of hypertensive crisis. Which enzyme does this drug target at low doses?",
        "correct": "Monoamine oxidase type B",
        "distractors": [
            "Catechol-O-methyltransferase (COMT)",
            "DOPA decarboxylase",
            "Tyrosine hydroxylase",
            "Monoamine oxidase type A"
        ],
        "ans": "C",
        "exp": "Selegiline and rasagiline are selective, irreversible inhibitors of MAO-B at low doses, prolonging dopamine action in the CNS without the need for dietary tyramine restrictions. However, at higher doses, they lose their selectivity and also inhibit MAO-A in the gut, creating a risk for the 'cheese reaction' (hypertensive crisis) upon tyramine ingestion.",
        "ctx": "Neuropharmacology - Antiparkinsonian"
    },
    {
        "q": "A patient with advanced Parkinson's disease experiences unpredictable 'wearing-off' periods with his levodopa/carbidopa regimen. A drug is added to increase the bioavailability of levodopa. This new drug strictly acts in the periphery and causes orange discoloration of the urine. What is its exact mechanism of action?",
        "correct": "Inhibition of peripheral catechol-O-methyltransferase (COMT)",
        "distractors": [
            "Inhibition of peripheral aromatic L-amino acid decarboxylase",
            "Inhibition of central monoamine oxidase type B",
            "Direct agonism of dopamine D2 receptors in the striatum",
            "Inhibition of central catechol-O-methyltransferase (COMT)"
        ],
        "ans": "C",
        "exp": "Entacapone is a COMT inhibitor that only acts peripherally (does not cross the blood-brain barrier), inhibiting the conversion of levodopa to 3-O-methyldopa. This increases the amount of levodopa available to enter the CNS. It classically causes a harmless brownish-orange discoloration of the urine. Tolcapone, conversely, acts both centrally and peripherally but is highly hepatotoxic.",
        "ctx": "Neuropharmacology - Antiparkinsonian"
    },
    {
        "q": "An antiviral drug is occasionally used to treat levodopa-induced dyskinesias in Parkinson's disease due to its NMDA antagonistic and dopaminergic effects. A distinct dermatological side effect of this medication presents as a painless, purplish, lace-like reticular discoloration of the lower extremities. Which of the following is the drug?",
        "correct": "Amantadine",
        "distractors": [
            "Pramipexole",
            "Benztropine",
            "Rotigotine",
            "Trihexyphenidyl"
        ],
        "ans": "C",
        "exp": "Amantadine, originally developed as an antiviral against Influenza A, has dopaminergic (enhances release, blocks reuptake) and NMDA antagonistic properties. A classic, benign but visually striking side effect is livedo reticularis, a lace-like purplish discoloration of the skin due to vasospasm of the dermal venules.",
        "ctx": "Neuropharmacology - Antiparkinsonian"
    },
    {
        "q": "A 35-year-old woman is found unresponsive with an empty bottle of amitriptyline. She exhibits a wide QRS complex on ECG, dry flushed skin, and dilated pupils. The emergency physician is considering using an antidote for presumed benzodiazepine co-ingestion but ultimately decides against it. Administration of this specific antidote in the setting of tricyclic antidepressant overdose carries a severe risk of which of the following?",
        "correct": "Precipitation of intractable seizures",
        "distractors": [
            "Exacerbation of lethal ventricular arrhythmias",
            "Development of sudden cardiovascular collapse",
            "Precipitation of severe hypertensive crisis",
            "Induction of profound respiratory depression"
        ],
        "ans": "C",
        "exp": "Flumazenil is a competitive antagonist at the GABAA benzodiazepine binding site. In patients with a mixed overdose or an overdose of tricyclic antidepressants (which lower the seizure threshold), antagonizing the protective inhibitory effects of endogenous or exogenous GABA/benzodiazepines with flumazenil frequently precipitates intractable, life-threatening seizures.",
        "ctx": "Toxicology - Antidotes"
    },
    {
        "q": "A 48-year-old man wishes to quit smoking. He is prescribed a medication that reduces his cravings and prevents the rewarding effects if he lapses and smokes a cigarette. This drug exerts its action by functioning as a partial agonist at which of the following receptors?",
        "correct": "Alpha-4-beta-2 nicotinic acetylcholine receptor",
        "distractors": [
            "Alpha-7 nicotinic acetylcholine receptor",
            "Muscarinic M1 acetylcholine receptor",
            "Dopamine D2 receptor",
            "N-methyl-D-aspartate (NMDA) receptor"
        ],
        "ans": "C",
        "exp": "Varenicline is a smoking cessation aid. It acts as a partial agonist specifically at the alpha-4-beta-2 (α4β2) neuronal nicotinic acetylcholine receptors. As a partial agonist, it provides enough basal stimulation to reduce cravings and withdrawal symptoms, while simultaneously acting as an antagonist by preventing the binding of nicotine from cigarettes, blunting the reward pathway.",
        "ctx": "Neuropharmacology - Substance Abuse"
    },

    # D (31-40)
    {
        "q": "A 22-year-old man with acute schizophrenia is to be started on an atypical antipsychotic. The psychiatrist prefers a medication that is weight-neutral. However, baseline ECG testing is strictly required before initiation due to the drug's known high propensity for a specific adverse effect. Which of the following is the most likely medication?",
        "correct": "Ziprasidone",
        "distractors": [
            "Olanzapine",
            "Quetiapine",
            "Risperidone",
            "Aripiprazole"
        ],
        "ans": "D",
        "exp": "Ziprasidone is an atypical antipsychotic known for having a very low risk of metabolic syndrome and weight gain. However, among the atypical antipsychotics, it carries one of the highest risks for dose-related QT interval prolongation, which can predispose to Torsades de Pointes. Baseline and serial ECGs are often recommended.",
        "ctx": "Psychopharmacology - Antipsychotics"
    },
    {
        "q": "A 30-year-old woman with major depressive disorder is prescribed an adjunctive atypical antipsychotic. Unlike most drugs in its class, which are pure antagonists at the D2 receptor, this medication functions uniquely at the D2 receptor, reducing risk of hyperprolactinemia. What is its mechanism of action?",
        "correct": "Partial agonism at dopamine D2 receptors",
        "distractors": [
            "Selective antagonism at dopamine D4 receptors",
            "Partial agonism at dopamine D1 receptors",
            "Antagonism at presynaptic dopamine D3 autoreceptors",
            "Irreversible inhibition of monoamine oxidase A"
        ],
        "ans": "D",
        "exp": "Aripiprazole is a unique atypical antipsychotic. While other atypicals are pure antagonists at D2 and 5-HT2A receptors, aripiprazole acts as a partial agonist at D2 and 5-HT1A receptors, and an antagonist at 5-HT2A receptors. This partial agonism prevents complete dopamine blockade in the tuberoinfundibular pathway, minimizing the risk of hyperprolactinemia.",
        "ctx": "Psychopharmacology - Antipsychotics"
    },
    {
        "q": "A 34-year-old woman with trigeminal neuralgia is started on a first-line antiepileptic drug. Three weeks later, her serum concentration of the drug drops subtherapeutically despite perfect compliance. The physician notes that the drug has induced its own metabolism. Which of the following cytochrome P450 enzymes is primarily responsible for this autoinduction phenomenon?",
        "correct": "CYP3A4",
        "distractors": [
            "CYP2D6",
            "CYP2C9",
            "CYP1A2",
            "CYP2E1"
        ],
        "ans": "D",
        "exp": "Carbamazepine is the drug of choice for trigeminal neuralgia. It is a potent inducer of several hepatic enzymes, most notably CYP3A4. Uniquely, it induces the very enzyme responsible for its own metabolism (autoinduction). This causes its half-life to progressively shorten over the first 3-4 weeks of therapy, often requiring a dose increase.",
        "ctx": "Neuropharmacology - Antiepileptics"
    },
    {
        "q": "A 25-year-old man on a maintenance dose of an antiepileptic drug for generalized tonic-clonic seizures experiences a breakthrough seizure. The physician increases the dose slightly, but the patient rapidly develops nystagmus, ataxia, and confusion. Blood tests reveal toxic levels of the drug. The pharmacokinetic principle underlying this rapid toxicity after a minor dose adjustment is:",
        "correct": "Zero-order kinetics due to saturation of hepatic enzymes",
        "distractors": [
            "First-pass effect saturation leading to massive absorption",
            "Displacement from plasma binding proteins by an endogenous ligand",
            "Rapid autoinduction of renal clearance mechanisms",
            "Irreversible binding to voltage-gated sodium channels in the CNS"
        ],
        "ans": "D",
        "exp": "Phenytoin exhibits Michaelis-Menten (non-linear or zero-order) pharmacokinetics at therapeutic doses because the hepatic enzymes responsible for its metabolism become saturated. Once saturated, a fixed amount (rather than a fixed proportion) is eliminated per unit time. Therefore, even small increases in dose can lead to disproportionately massive increases in serum concentration, precipitating severe toxicity (nystagmus, ataxia).",
        "ctx": "Pharmacokinetics - Antiepileptics"
    },
    {
        "q": "A pregnant woman taking medication for bipolar disorder gives birth to an infant with spina bifida. The drug implicated in this teratogenic effect disrupts embryonic development via two main proposed mechanisms: antagonism of folate and direct inhibition of which of the following intracellular enzymes?",
        "correct": "Histone deacetylase (HDAC)",
        "distractors": [
            "DNA topoisomerase II",
            "Dihydrofolate reductase",
            "Glutathione S-transferase",
            "RNA polymerase II"
        ],
        "ans": "D",
        "exp": "Valproic acid (valproate) is a known teratogen carrying a high risk of neural tube defects (e.g., spina bifida). The mechanism of teratogenicity is multifactorial, including interference with folate metabolism and direct, potent inhibition of histone deacetylase (HDAC). HDAC inhibition drastically alters gene transcription during critical periods of neural tube closure.",
        "ctx": "Toxicology - Teratogens"
    },
    {
        "q": "A patient undergoes a minor surgical procedure using lidocaine infiltration. The local anesthetic must penetrate the nerve bundle to block action potentials. Which of the following nerve fiber types are blocked first and are most sensitive to local anesthetics?",
        "correct": "Small, unmyelinated C fibers and small, myelinated B fibers",
        "distractors": [
            "Large, heavily myelinated A-alpha fibers",
            "Large, heavily myelinated A-beta fibers",
            "Medium, myelinated A-gamma fibers",
            "Small, unmyelinated A-delta fibers"
        ],
        "ans": "D",
        "exp": "Local anesthetics block voltage-gated sodium channels. Sensitivity to block is determined by fiber diameter and myelination. Small diameter and high firing frequencies increase sensitivity. Therefore, small autonomic fibers (Type B) and small unmyelinated pain fibers (Type C) are blocked first, followed by A-delta, A-gamma, A-beta, and finally A-alpha (motor) fibers.",
        "ctx": "Neuropharmacology - Local Anesthetics"
    },
    {
        "q": "A 30-year-old woman in labor is receiving an epidural anesthetic using a long-acting amide local anesthetic. The catheter inadvertently migrates intravenously, and she rapidly develops severe refractory ventricular arrhythmias leading to cardiac arrest. The extreme cardiotoxicity of this specific agent is attributed to its high lipid solubility and which of the following features at the cardiac sodium channel?",
        "correct": "Slow rate of dissociation from the fast sodium channel during diastole",
        "distractors": [
            "Irreversible covalent binding to the inactivation gate of the sodium channel",
            "Selective blockade of the rapid component of the delayed rectifier potassium current (IKr)",
            "Potent activation of the calcium-induced calcium release mechanism",
            "Inhibition of the sodium-calcium exchanger leading to intracellular calcium overload"
        ],
        "ans": "D",
        "exp": "Bupivacaine is highly lipid-soluble and potent. If injected intravenously, it causes profound cardiotoxicity (refractory arrhythmias and cardiovascular collapse). The primary mechanism is that bupivacaine intensely blocks cardiac fast sodium channels and dissociates extremely slowly during diastole, resulting in accumulated block and severe conduction depression. Lipid emulsion therapy is the antidote.",
        "ctx": "Neuropharmacology - Local Anesthetics"
    },
    {
        "q": "A patient in the intensive care unit requires sedation while remaining easily rousable to follow commands (cooperative sedation). The drug infused achieves this state without causing significant respiratory depression. Its mechanism of action involves stimulation of receptors located primarily in the locus coeruleus. What is the drug?",
        "correct": "Dexmedetomidine",
        "distractors": [
            "Midazolam",
            "Propofol",
            "Ketamine",
            "Fentanyl"
        ],
        "ans": "D",
        "exp": "Dexmedetomidine is a highly selective alpha-2 adrenergic receptor agonist. It provides 'cooperative sedation' and analgesia without respiratory depression. Its primary site of action is the locus coeruleus in the pons, where alpha-2 agonism decreases sympathetic outflow, promoting a state resembling natural sleep.",
        "ctx": "Neuropharmacology - Sedatives"
    },
    {
        "q": "A 75-year-old man with mild-to-moderate Alzheimer's disease is treated with a medication extracted from daffodil bulbs. This drug not only acts as a reversible competitive inhibitor of acetylcholinesterase but also possesses a secondary mechanism that enhances cholinergic transmission. What is this secondary mechanism?",
        "correct": "Positive allosteric modulation of presynaptic and postsynaptic nicotinic receptors",
        "distractors": [
            "Direct agonism of muscarinic M1 receptors in the hippocampus",
            "Inhibition of butyrylcholinesterase in the peripheral circulation",
            "Uncompetitive antagonism of NMDA glutamate receptors",
            "Irreversible inhibition of monoamine oxidase type B"
        ],
        "ans": "D",
        "exp": "Galantamine, used for Alzheimer's disease, has a dual mechanism of action. It is a competitive, reversible acetylcholinesterase inhibitor (AChEI). Additionally, it acts as a positive allosteric modulator (PAM) at nicotinic acetylcholine receptors, sensitizing them to the action of acetylcholine, which may theoretically further enhance cognitive function.",
        "ctx": "Neuropharmacology - Neurodegenerative Diseases"
    },
    {
        "q": "An 80-year-old woman with advanced Alzheimer's disease is started on an additional medication to manage her severe cognitive decline. This drug is an open-channel blocker that only inhibits pathological, sustained activation of the receptor while allowing physiological transmission to occur. What is the drug's specific mechanism of action?",
        "correct": "Uncompetitive, low-affinity antagonism at the NMDA receptor",
        "distractors": [
            "Competitive, high-affinity antagonism at the AMPA receptor",
            "Irreversible inhibition of central acetylcholinesterase",
            "Positive allosteric modulation of the GABAA receptor",
            "Selective agonism of the serotonin 5-HT4 receptor"
        ],
        "ans": "D",
        "exp": "Memantine is used for moderate to severe Alzheimer's disease. It is a low-affinity, uncompetitive antagonist at the NMDA receptor. It blocks the ion channel pore only when it is excessively open (pathological tonic glutamate release, which causes excitotoxicity), but its low affinity allows it to be displaced during transient, physiological high-frequency bursts of glutamate (essential for memory and learning).",
        "ctx": "Neuropharmacology - Neurodegenerative Diseases"
    },

    # E (41-50)
    {
        "q": "A 60-year-old man is newly diagnosed with Parkinson's disease. To delay the introduction of levodopa and the subsequent motor complications, his neurologist starts him on a monotherapy. The chosen drug directly stimulates dopamine receptors but is structurally distinct from ergot derivatives, lacking the risk of pleuropulmonary fibrotic complications. Which of the following accurately describes this drug?",
        "correct": "A non-ergot dopamine agonist with high affinity for D2 and D3 receptors",
        "distractors": [
            "An ergot-derived dopamine agonist with high affinity for D1 receptors",
            "An irreversible inhibitor of monoamine oxidase B in the striatum",
            "A competitive antagonist at central muscarinic acetylcholine receptors",
            "A metabolic precursor to dopamine that crosses the blood-brain barrier"
        ],
        "ans": "E",
        "exp": "The patient is started on a non-ergot dopamine agonist (e.g., pramipexole, ropinirole). Unlike older ergot-derived agonists (e.g., bromocriptine), non-ergot agonists do not carry the risk of retroperitoneal, pleural, or cardiac valve fibrosis. They work by directly stimulating post-synaptic D2 and D3 receptors.",
        "ctx": "Neuropharmacology - Antiparkinsonian"
    },
    {
        "q": "In the mid-20th century, a plant alkaloid extracted from Rauwolfia serpentina was used as an antihypertensive and antipsychotic. Its use was abandoned due to profound severe depression and suicidality. At a molecular level, this drug exerted its effect through irreversible inhibition of which of the following?",
        "correct": "The vesicular monoamine transporter (VMAT)",
        "distractors": [
            "The dopamine transporter (DAT)",
            "Monoamine oxidase type A (MAO-A)",
            "Catechol-O-methyltransferase (COMT)",
            "The norepinephrine transporter (NET)"
        ],
        "ans": "E",
        "exp": "Reserpine irreversibly inhibits the vesicular monoamine transporter (VMAT1 and VMAT2), preventing the packaging of biogenic amines (norepinephrine, dopamine, serotonin) into presynaptic vesicles. This leads to profound depletion of these neurotransmitters, causing vasodilation/bradycardia (antihypertensive effect) and severe, sometimes suicidal, depression.",
        "ctx": "Psychopharmacology - Historical Agents"
    },
    {
        "q": "A 45-year-old man with Huntington's disease presents with debilitating chorea. To manage his excessive hyperkinetic movements, a drug is prescribed that specifically and reversibly depletes monoamines from nerve terminals in the CNS without affecting peripheral stores significantly. Which of the following is the drug?",
        "correct": "Tetrabenazine",
        "distractors": [
            "Haloperidol",
            "Riluzole",
            "Benztropine",
            "Baclofen"
        ],
        "ans": "E",
        "exp": "Tetrabenazine is approved for the treatment of chorea in Huntington's disease. It acts as a highly selective, reversible inhibitor of central VMAT2, causing presynaptic depletion of dopamine and thereby reducing the hyperkinetic movements caused by dopaminergic overactivity in the striatum.",
        "ctx": "Neuropharmacology - Movement Disorders"
    },
    {
        "q": "A 38-year-old woman with bipolar disorder has been well-controlled on lithium for years. She develops mild hypertension and is prescribed a new medication by her primary care physician. Two weeks later, she presents with severe coarse tremors, ataxia, and confusion. The new medication most likely increased lithium levels by promoting sodium depletion. Which of the following classes does the new medication belong to?",
        "correct": "Thiazide diuretics",
        "distractors": [
            "Beta-blockers",
            "Calcium channel blockers",
            "Alpha-1 antagonists",
            "Potassium-sparing diuretics"
        ],
        "ans": "E",
        "exp": "Lithium is handled by the kidneys similarly to sodium. It is filtered and reabsorbed primarily in the proximal tubule. Thiazide diuretics cause mild volume and sodium depletion by blocking the Na/Cl cotransporter in the DCT. This volume contraction triggers a compensatory increase in proximal tubular reabsorption of both sodium and lithium, rapidly leading to lithium toxicity.",
        "ctx": "Psychopharmacology - Drug Interactions"
    },
    {
        "q": "A 42-year-old woman with severe depression and chronic neuropathic pain is prescribed a medication that inhibits the reuptake of two distinct monoamines. The physician notes that at lower doses, the drug primarily inhibits serotonin reuptake, but its norepinephrine reuptake inhibition only becomes clinically significant at higher doses. Which of the following drugs exhibits this dose-dependent dual mechanism?",
        "correct": "Venlafaxine",
        "distractors": [
            "Duloxetine",
            "Milnacipran",
            "Levomilnacipran",
            "Desvenlafaxine"
        ],
        "ans": "E",
        "exp": "Venlafaxine is a serotonin-norepinephrine reuptake inhibitor (SNRI) known for its distinct dose-dependent target affinity. At low doses (<150 mg/day), it acts essentially as an SSRI. Only at higher doses does its blockade of the norepinephrine transporter (NET) become significant, which is necessary for its efficacy in treating neuropathic pain and refractory depression.",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 24-year-old man is brought to the ER following an intentional overdose of a tricyclic antidepressant (TCA). His ECG shows a progressively widening QRS complex, indicating severe cardiotoxicity. This specific, lethal cardiac effect of TCAs is mediated directly by the blockade of which of the following?",
        "correct": "Fast voltage-gated sodium channels in the His-Purkinje system",
        "distractors": [
            "L-type calcium channels in the sinoatrial node",
            "Delayed rectifier potassium channels in the ventricular myocardium",
            "Beta-1 adrenergic receptors in the ventricular myocardium",
            "Muscarinic M2 receptors in the atrioventricular node"
        ],
        "ans": "E",
        "exp": "TCA mortality is largely driven by cardiotoxicity. The hallmark wide QRS complex is caused by direct blockade of the fast inward sodium channels (Phase 0 depolarization) in the His-Purkinje system and ventricular myocardium. This quinidine-like effect leads to slowed conduction, broad QRS, and risk of lethal ventricular arrhythmias. Sodium bicarbonate is the treatment of choice.",
        "ctx": "Toxicology - Antidepressants"
    },
    {
        "q": "A 70-year-old man is prescribed amitriptyline for painful diabetic neuropathy. Shortly after initiating therapy, he complains of blurred vision, severe dry mouth, constipation, and difficulty initiating micturition. These side effects are directly attributable to the drug's high affinity for and antagonism of which of the following receptors?",
        "correct": "Muscarinic M1, M2, and M3 receptors",
        "distractors": [
            "Histamine H1 and H2 receptors",
            "Serotonin 5-HT2A and 5-HT2C receptors",
            "Alpha-1 and Alpha-2 adrenergic receptors",
            "Dopamine D2 and D3 receptors"
        ],
        "ans": "E",
        "exp": "Amitriptyline is a tertiary amine TCA with extremely potent anticholinergic (antimuscarinic) properties. Blockade of peripheral muscarinic receptors (M3 primarily) leads to reduced salivary secretion (dry mouth), decreased gut motility (constipation), detrusor muscle relaxation (urinary retention), and impaired ciliary muscle accommodation (blurred vision).",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 19-year-old college student presents with worsening depression. She also reveals a history of inducing vomiting to maintain her low body weight and electrolyte derangements noted in her chart. Which of the following antidepressants is absolutely contraindicated in this patient due to an unacceptably high risk of a specific neurological adverse event?",
        "correct": "Bupropion",
        "distractors": [
            "Fluoxetine",
            "Sertraline",
            "Mirtazapine",
            "Escitalopram"
        ],
        "ans": "E",
        "exp": "Bupropion is an NDRI (norepinephrine-dopamine reuptake inhibitor) that strongly lowers the seizure threshold. It is absolutely contraindicated in patients with anorexia nervosa or bulimia nervosa. These patients often have significant electrolyte imbalances (e.g., hypokalemia, hyponatremia) that independently lower the seizure threshold, creating an extreme risk for generalized seizures when combined with bupropion.",
        "ctx": "Psychopharmacology - Antidepressants"
    },
    {
        "q": "A 55-year-old man with progressive muscle weakness, fasciculations, and spasticity is diagnosed with amyotrophic lateral sclerosis (ALS). He is prescribed the only medication known to modestly prolong survival in this disease. The drug's neuroprotective effect is believed to stem from its ability to decrease the presynaptic release of which of the following neurotransmitters?",
        "correct": "Glutamate",
        "distractors": [
            "Acetylcholine",
            "Gamma-aminobutyric acid (GABA)",
            "Dopamine",
            "Substance P"
        ],
        "ans": "E",
        "exp": "Riluzole is an FDA-approved treatment that extends survival in ALS by a few months. Its precise mechanism is debated, but it primarily acts to decrease glutamate-induced excitotoxicity. It is thought to block presynaptic voltage-gated sodium channels, thereby reducing the release of glutamate into the synaptic cleft, protecting upper and lower motor neurons.",
        "ctx": "Neuropharmacology - Neurodegenerative Diseases"
    },
    {
        "q": "A 30-year-old woman with relapsing-remitting multiple sclerosis is prescribed an oral disease-modifying therapy. Following the first dose, she is required to stay in the clinic for 6 hours with continuous heart rate monitoring due to a risk of severe bradycardia. This drug acts by modulating receptors that trap lymphocytes in which of the following anatomical locations?",
        "correct": "Lymph nodes",
        "distractors": [
            "Bone marrow",
            "Spleen",
            "Thymus",
            "Circulating blood"
        ],
        "ans": "E",
        "exp": "Fingolimod is a sphingosine-1-phosphate (S1P) receptor modulator used in multiple sclerosis. By downregulating S1P receptors on lymphocytes, it traps them within secondary lymphoid organs (lymph nodes), preventing their egress and migration into the central nervous system. Its first-dose effect involves agonism of S1P receptors in the cardiac conduction system, carrying a high risk of symptomatic bradycardia or AV block.",
        "ctx": "Neuropharmacology - Multiple Sclerosis"
    }
]

formatted_mcqs = []

for item in raw_data:
    ans_letter = item["ans"]
    target_idx = ord(ans_letter) - ord('A')
    
    # We have 4 distractors. Let's arrange the options to place the correct answer exactly at target_idx
    distractors = item["distractors"].copy()
    options = []
    for i in range(5):
        if i == target_idx:
            options.append(item["correct"])
        else:
            options.append(distractors.pop(0))
    
    formatted_mcq = {
        "question": item["q"],
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "option_e": options[4],
        "correct_answer": ans_letter,
        "explanation": item["exp"],
        "source_context": item["ctx"]
    }
    formatted_mcqs.append(formatted_mcq)

output_path = r"E:\USAMA\MBBS Books\MCQ_Generator\batches\bank_batch_neuropharm.json"

import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(formatted_mcqs, f, indent=2, ensure_ascii=False)

print(f"Written {len(formatted_mcqs)} MCQs to {output_path}")
