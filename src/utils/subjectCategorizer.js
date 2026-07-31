export const SUBJECT_METADATA = {
  Anatomy: {
    id: 'Anatomy',
    name: 'Anatomy & Embryology',
    icon: 'fa-bone',
    color: '#06b6d4',
    bg: 'rgba(6, 182, 212, 0.12)',
    description: 'Gross anatomy, histology, embryology & neuroanatomy high-yield concepts.'
  },
  Physiology: {
    id: 'Physiology',
    name: 'Physiology',
    icon: 'fa-heart-pulse',
    color: '#3b82f6',
    bg: 'rgba(59, 130, 246, 0.12)',
    description: 'Organ systems, cellular mechanisms, hemodynamics & acid-base regulation.'
  },
  Pathology: {
    id: 'Pathology',
    name: 'Pathology',
    icon: 'fa-microscope',
    color: '#ef4444',
    bg: 'rgba(239, 68, 68, 0.12)',
    description: 'General pathology, neoplasia, inflammation & systemic pathology.'
  },
  Pharmacology: {
    id: 'Pharmacology',
    name: 'Pharmacology',
    icon: 'fa-pills',
    color: '#10b981',
    bg: 'rgba(16, 185, 129, 0.12)',
    description: 'Pharmacokinetics, mechanism of action, side effects & clinical drugs.'
  },
  Surgery: {
    id: 'Surgery',
    name: 'Surgery & Trauma',
    icon: 'fa-scalpel',
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.12)',
    description: 'General surgery, surgical anatomy, perioperative care & trauma management.'
  },
  Cardiology: {
    id: 'Cardiology',
    name: 'Cardiology & CVS',
    icon: 'fa-heart-circle-check',
    color: '#ec4899',
    bg: 'rgba(236, 72, 153, 0.12)',
    description: 'ECG interpretation, valvular heart disease, ischemic heart disease & CHF.'
  },
  Neurology: {
    id: 'Neurology',
    name: 'Neurology & CNS',
    icon: 'fa-brain',
    color: '#8b5cf6',
    bg: 'rgba(139, 92, 246, 0.12)',
    description: 'Cranial nerves, stroke syndromes, neurodegenerative disorders & localization.'
  },
  'Internal Medicine': {
    id: 'Internal Medicine',
    name: 'Internal Medicine',
    icon: 'fa-user-doctor',
    color: '#14b8a6',
    bg: 'rgba(20, 184, 166, 0.12)',
    description: 'Nephrology, Gastroenterology, Endocrinology, Pulmonology & Rheumatology.'
  },
  'General Medicine': {
    id: 'General Medicine',
    name: 'General & Clinical Practice',
    icon: 'fa-notes-medical',
    color: '#6366f1',
    bg: 'rgba(99, 102, 241, 0.12)',
    description: 'Epidemiology, biostatistics, medical ethics, microbiology & immunology.'
  }
};

export function getQuestionSubject(item) {
  if (!item) return 'General Medicine';
  const cat = (item.category || '').toLowerCase();
  const src = (item.book_source || '').toLowerCase();

  if (src.includes('snell') || cat.includes('anatomy')) return 'Anatomy';
  if (src.includes('guyton') || cat.includes('physiology')) return 'Physiology';
  if (src.includes('pathoma') || cat.includes('pathology')) return 'Pathology';
  if (src.includes('pharmacology') || src.includes('garg') || cat.includes('pharmacology')) return 'Pharmacology';
  if (src.includes('bailey') || cat.includes('surgery')) return 'Surgery';
  if (cat.includes('cardio')) return 'Cardiology';
  if (cat.includes('neuro')) return 'Neurology';
  if (cat.includes('gastro') || cat.includes('renal') || cat.includes('endo')) return 'Internal Medicine';
  
  return 'General Medicine';
}

export function groupQuestionsBySubject(questionsList) {
  const grouped = {
    Anatomy: [],
    Physiology: [],
    Pathology: [],
    Pharmacology: [],
    Surgery: [],
    Cardiology: [],
    Neurology: [],
    'Internal Medicine': [],
    'General Medicine': []
  };

  if (!Array.isArray(questionsList)) return grouped;

  questionsList.forEach(q => {
    const subj = getQuestionSubject(q);
    if (grouped[subj]) {
      grouped[subj].push(q);
    } else {
      grouped['General Medicine'].push(q);
    }
  });

  return grouped;
}
