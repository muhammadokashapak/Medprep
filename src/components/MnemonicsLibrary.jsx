import React, { useState } from 'react';

const HIGH_YIELD_MNEMONICS = [
  {
    id: 1,
    title: 'MUDPILES',
    category: 'Biochemistry / Nephrology',
    concept: 'Causes of High Anion Gap Metabolic Acidosis (HAGMA)',
    breakdown: [
      { letter: 'M', word: 'Methanol' },
      { letter: 'U', word: 'Uremia' },
      { letter: 'D', word: 'Diabetic Ketoacidosis (DKA)' },
      { letter: 'P', word: 'Paraldehyde / Propylene Glycol' },
      { letter: 'I', word: 'Isoniazid / Iron' },
      { letter: 'L', word: 'Lactic Acidosis' },
      { letter: 'E', word: 'Ethylene Glycol' },
      { letter: 'S', word: 'Salicylates (Aspirin)' }
    ]
  },
  {
    id: 2,
    title: 'SAD PERSONS',
    category: 'Psychiatry',
    concept: 'Suicide Risk Assessment Factors',
    breakdown: [
      { letter: 'S', word: 'Sex (Male)' },
      { letter: 'A', word: 'Age (Young or >45)' },
      { letter: 'D', word: 'Depression' },
      { letter: 'P', word: 'Previous Attempt' },
      { letter: 'E', word: 'Ethanol / Substance Use' },
      { letter: 'R', word: 'Rational Thinking Loss' },
      { letter: 'S', word: 'Social Support Lacking' },
      { letter: 'O', word: 'Organized Plan' },
      { letter: 'N', word: 'No Spouse / Single' },
      { letter: 'S', word: 'Sickness (Chronic Illness)' }
    ]
  },
  {
    id: 3,
    title: 'CRAB',
    category: 'Hematology / Oncology',
    concept: 'Multiple Myeloma Clinical Features',
    breakdown: [
      { letter: 'C', word: 'HyperCalcemia' },
      { letter: 'R', word: 'Renal Insufficiency' },
      { letter: 'A', word: 'Anemia' },
      { letter: 'B', word: 'Bone Lytic Lesions / Pain' }
    ]
  },
  {
    id: 4,
    title: 'GET SMASHED',
    category: 'Gastroenterology',
    concept: 'Causes of Acute Pancreatitis',
    breakdown: [
      { letter: 'G', word: 'Gallstones' },
      { letter: 'E', word: 'Ethanol (Alcohol)' },
      { letter: 'T', word: 'Trauma' },
      { letter: 'S', word: 'Steroids' },
      { letter: 'M', word: 'Mumps' },
      { letter: 'A', word: 'Autoimmune' },
      { letter: 'S', word: 'Scorpion Sting' },
      { letter: 'H', word: 'Hypercalcemia / Hypertriglyceridemia' },
      { letter: 'E', word: 'ERCP' },
      { letter: 'D', word: 'Drugs (Thiazides, Azathioprine)' }
    ]
  },
  {
    id: 5,
    title: 'PALLOR',
    category: 'Vascular Surgery',
    concept: '6 Ps of Acute Limb Ischemia',
    breakdown: [
      { letter: 'P', word: 'Pain' },
      { letter: 'P', word: 'Pallor' },
      { letter: 'P', word: 'Pulselessness' },
      { letter: 'P', word: 'Paresthesia' },
      { letter: 'P', word: 'Paralysis' },
      { letter: 'P', word: 'Poikilothermia (Cold Limb)' }
    ]
  }
];

export default function MnemonicsLibrary() {
  const [openId, setOpenId] = useState(HIGH_YIELD_MNEMONICS[0].id);
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = HIGH_YIELD_MNEMONICS.filter(m =>
    m.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.concept.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="animate-fade-in" style={{ padding: '1rem 0', maxWidth: '900px', margin: '0 auto' }}>
      {/* Header */}
      <div className="glass-panel text-center" style={{ padding: '2rem 1.5rem', marginBottom: '1.5rem', borderLeft: '4px solid var(--accent-purple)' }}>
        <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-purple)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
          HIGH-YIELD RECALL TOOL
        </span>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, margin: '0.2rem 0 0.4rem', color: 'var(--text-main)' }}>
          Interactive Medical Mnemonics
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>
          Tap any mnemonic card to expand its letter-by-letter medical breakdown.
        </p>
      </div>

      {/* Search Input */}
      <div style={{ marginBottom: '1.5rem', position: 'relative' }}>
        <i className="fa-solid fa-magnifying-glass" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}></i>
        <input
          type="text"
          placeholder="Search mnemonics (e.g. MUDPILES, Acidosis, Pancreatitis)..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '0.75rem 1rem 0.75rem 2.6rem',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)',
            background: 'var(--bg-card)',
            color: 'var(--text-main)',
            fontSize: '0.9rem',
            outline: 'none'
          }}
        />
      </div>

      {/* Mnemonics Accordion Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filtered.map(item => {
          const isOpen = item.id === openId;
          return (
            <div
              key={item.id}
              className="glass-panel"
              style={{
                borderRadius: 'var(--radius-sm)',
                overflow: 'hidden',
                borderLeft: `4px solid ${isOpen ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
                transition: 'all 0.2s'
              }}
            >
              <div
                onClick={() => setOpenId(isOpen ? null : item.id)}
                style={{
                  padding: '1.25rem 1.5rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  cursor: 'pointer',
                  background: isOpen ? 'rgba(6, 182, 212, 0.05)' : 'transparent'
                }}
              >
                <div>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase' }}>
                    {item.category}
                  </span>
                  <h3 style={{ fontSize: '1.3rem', fontWeight: 800, margin: '0.1rem 0 0.2rem', color: 'var(--text-main)' }}>
                    {item.title}
                  </h3>
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', margin: 0 }}>
                    {item.concept}
                  </p>
                </div>

                <div style={{
                  width: '36px', height: '36px', borderRadius: '50%',
                  background: 'rgba(255,255,255,0.05)', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', color: 'var(--text-main)'
                }}>
                  <i className={`fa-solid ${isOpen ? 'fa-chevron-up' : 'fa-chevron-down'}`}></i>
                </div>
              </div>

              {isOpen && (
                <div style={{ padding: '0 1.5rem 1.5rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.65rem' }}>
                    {item.breakdown.map((row, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.75rem',
                          padding: '0.6rem 0.85rem',
                          background: 'rgba(255,255,255,0.02)',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--border-subtle)'
                        }}
                      >
                        <span style={{
                          width: '32px',
                          height: '32px',
                          borderRadius: '6px',
                          background: 'var(--gradient-primary)',
                          color: '#fff',
                          fontWeight: 800,
                          fontSize: '1rem',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0
                        }}>
                          {row.letter}
                        </span>
                        <span style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)' }}>
                          {row.word}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
