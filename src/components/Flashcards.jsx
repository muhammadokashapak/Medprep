import React, { useState } from 'react';
import { addXP } from '../utils/gamification';

const FLASHCARD_DECKS = [
  {
    id: 'pharmacology',
    name: 'Pharmacology Antidotes & MoA',
    icon: 'fa-pills',
    color: '#10b981',
    cards: [
      { id: 1, front: 'What is the specific antidote for Acetaminophen (Paracetamol) toxicity?', back: 'N-Acetylcysteine (NAC) — Restores hepatic glutathione stores.' },
      { id: 2, front: 'What is the mechanism of action of Warfarin?', back: 'Inhibits Vitamin K Epoxide Reductase (VKORC1), reducing factors II, VII, IX, X, Protein C & S.' },
      { id: 3, front: 'What is the antidote for Heparin overdose?', back: 'Protamine Sulfate (positively charged protein binding negative heparin).' },
      { id: 4, front: 'What drug is the first-line treatment for Anaphylaxis?', back: 'Intramuscular Epinephrine (1:1000 dilution, 0.3-0.5 mg IM in anterolateral thigh).' },
      { id: 5, front: 'What is the antidote for Organophosphate / Insecticide poisoning?', back: 'Atropine (muscarinic receptor antagonist) + Pralidoxime (2-PAM to reactivate AChE).' }
    ]
  },
  {
    id: 'pathology',
    name: 'Pathology High-Yield Triads',
    icon: 'fa-microscope',
    color: '#ef4444',
    cards: [
      { id: 1, front: 'Classic triad of Normal Pressure Hydrocephalus (NPH)?', back: 'Ataxia + Urinary Incontinence + Dementia ("Wet, Wobbly, Wacky").' },
      { id: 2, front: 'Beck\'s Triad for Cardiac Tamponade?', back: 'Hypotension + Distended Neck Veins (JVD) + Muffled Heart Sounds.' },
      { id: 3, front: 'Virchow\'s Triad for Venous Thrombosis?', back: 'Endothelial Injury + Stasis of Blood Flow + Hypercoagulability.' },
      { id: 4, front: 'Charcot\'s Triad for Acute Cholangitis?', back: 'Fever + Right Upper Quadrant Pain + Jaundice (Add Shock + Altered Mental Status for Reynolds Pentad).' },
      { id: 5, front: 'Triad of Wernicke Encephalopathy?', back: 'Ophthalmoplegia/Nystagmus + Ataxia + Confusion (Thiamine B1 deficiency).' }
    ]
  },
  {
    id: 'cardiology',
    name: 'Cardiology ECGs & Murmurs',
    icon: 'fa-heart-pulse',
    color: '#ec4899',
    cards: [
      { id: 1, front: 'Crescendo-decrescendo systolic murmur at 2nd right intercostal space radiating to carotids?', back: 'Aortic Stenosis (Pulsus parvus et tardus).' },
      { id: 2, front: 'ECG finding: ST-segment elevation in leads II, III, aVF?', back: 'Inferior Wall Myocardial Infarction (RCA occlusion).' },
      { id: 3, front: 'Holosystolic murmur at apex radiating to axilla?', back: 'Mitral Regurgitation.' },
      { id: 4, front: 'Classic ECG pattern of Wolff-Parkinson-White (WPW) Syndrome?', back: 'Delta wave (slurred upstroke of QRS), short PR interval (<0.12s), wide QRS.' },
      { id: 5, front: 'First-line drug for Paroxysmal Supraventricular Tachycardia (PSVT)?', back: 'IV Adenosine (rapid IV push followed by saline flush).' }
    ]
  },
  {
    id: 'anatomy',
    name: 'Anatomy & Surgical Landmarks',
    icon: 'fa-bone',
    color: '#06b6d4',
    cards: [
      { id: 1, front: 'Nerve injured in Midshaft Humerus fracture?', back: 'Radial Nerve (leads to Wrist Drop).' },
      { id: 2, front: 'Nerve injured in Surgical Neck Humerus fracture?', back: 'Axillary Nerve (leads to loss of deltoid sensation & abduction).' },
      { id: 3, front: 'Surgical landmark for McBurney\'s Point in Appendicitis?', back: '1/3rd distance from Right ASIS to Umbilicus.' },
      { id: 4, front: 'Structures passing through the Foramen Magnum?', back: 'Medulla oblongata, Vertebral arteries, Spinal accessory nerve (CN XI), Anterior/Posterior spinal arteries.' },
      { id: 5, front: 'Sensory nerve supplying skin of 1st web space of foot?', back: 'Deep Peroneal (Fibular) Nerve.' }
    ]
  }
];

export default function Flashcards({ addToast }) {
  const [activeDeckId, setActiveDeckId] = useState(FLASHCARD_DECKS[0].id);
  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [masteredCards, setMasteredCards] = useState({});

  const currentDeck = FLASHCARD_DECKS.find(d => d.id === activeDeckId) || FLASHCARD_DECKS[0];
  const currentCard = currentDeck.cards[cardIndex];

  const handleNext = (isMastered) => {
    setIsFlipped(false);

    if (isMastered) {
      setMasteredCards(prev => ({ ...prev, [`${activeDeckId}_${currentCard.id}`]: true }));
      const res = addXP(15);
      if (res.leveledUp) {
        addToast?.(`🎉 Level Up! You are now a ${res.newRank.title}!`, 'success');
      } else {
        addToast?.('+15 XP Mastered!', 'success');
      }
    }

    setTimeout(() => {
      setCardIndex(p => (p + 1) % currentDeck.cards.length);
    }, 150);
  };

  const masteredCount = currentDeck.cards.filter(c => masteredCards[`${activeDeckId}_${c.id}`]).length;

  return (
    <div className="animate-fade-in" style={{ padding: '1rem 0', maxWidth: '800px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div className="glass-panel text-center" style={{ padding: '1.75rem 1.25rem', marginBottom: '1.5rem', borderLeft: '4px solid var(--accent-cyan)' }}>
        <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-cyan)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
          ACTIVE RECALL ENGINE
        </span>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, margin: '0.2rem 0 0.4rem', color: 'var(--text-main)' }}>
          High-Yield Medical Flashcards
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>
          Tap cards to flip and test your memory before board exams.
        </p>
      </div>

      {/* Deck Selector Dropdown Menu */}
      <div style={{ marginBottom: '1.5rem', background: 'var(--bg-card-hover)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
        <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-cyan)', marginBottom: '0.45rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          <i className="fa-solid fa-layer-group" style={{ marginRight: '0.35rem' }}></i> SELECT FLASHCARD DECK MODULE
        </label>
        <select
          value={activeDeckId}
          onChange={(e) => {
            setActiveDeckId(e.target.value);
            setCardIndex(0);
            setIsFlipped(false);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
          style={{
            width: '100%',
            padding: '0.75rem 1rem',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)',
            background: 'var(--bg-card)',
            color: 'var(--text-main)',
            fontSize: '0.95rem',
            fontWeight: 700,
            cursor: 'pointer',
            outline: 'none'
          }}
        >
          {FLASHCARD_DECKS.map(deck => (
            <option key={deck.id} value={deck.id}>
              {deck.name} ({deck.cards.length} High-Yield Cards)
            </option>
          ))}
        </select>
      </div>

      {/* Progress Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>
        <span>Card {cardIndex + 1} of {currentDeck.cards.length}</span>
        <span style={{ color: 'var(--accent-emerald)' }}>{masteredCount} / {currentDeck.cards.length} Mastered</span>
      </div>
      <div style={{ height: '6px', background: 'var(--border-subtle)', borderRadius: '99px', overflow: 'hidden', marginBottom: '1.5rem' }}>
        <div style={{
          height: '100%',
          width: `${((cardIndex + 1) / currentDeck.cards.length) * 100}%`,
          background: currentDeck.color,
          transition: 'width 0.3s ease'
        }}></div>
      </div>

      {/* 3D Flip Flashcard Container */}
      <div
        onClick={() => setIsFlipped(!isFlipped)}
        style={{
          perspective: '1000px',
          cursor: 'pointer',
          marginBottom: '1.5rem',
          minHeight: '260px'
        }}
      >
        <div style={{
          position: 'relative',
          width: '100%',
          minHeight: '260px',
          textAlign: 'center',
          transition: 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)'
        }}>
          {/* Front Face */}
          <div className="glass-panel" style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            backfaceVisibility: 'hidden',
            WebkitBackfaceVisibility: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '2rem',
            borderTop: `5px solid ${currentDeck.color}`
          }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: currentDeck.color, textTransform: 'uppercase', marginBottom: '1rem' }}>
              QUESTION / PROMPT (TAP TO FLIP)
            </span>
            <h3 style={{ fontSize: '1.2rem', lineHeight: 1.6, fontWeight: 600, color: 'var(--text-main)', margin: 0 }}>
              {currentCard.front}
            </h3>
          </div>

          {/* Back Face */}
          <div className="glass-panel" style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            backfaceVisibility: 'hidden',
            WebkitBackfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '2rem',
            background: 'var(--bg-card-hover)',
            borderTop: '5px solid var(--accent-emerald)'
          }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-emerald)', textTransform: 'uppercase', marginBottom: '1rem' }}>
              ANSWER & CLINICAL PEARL
            </span>
            <p style={{ fontSize: '1.15rem', lineHeight: 1.6, fontWeight: 700, color: 'var(--accent-emerald)', margin: 0 }}>
              {currentCard.back}
            </p>
          </div>
        </div>
      </div>

      {/* Action Controls */}
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
        <button
          className="btn-secondary"
          onClick={() => handleNext(false)}
          style={{ flex: 1, padding: '0.8rem', justifyContent: 'center', borderColor: 'rgba(244, 63, 94, 0.4)', color: 'var(--accent-rose)' }}
        >
          <i className="fa-solid fa-rotate-left"></i> Needs Review
        </button>

        <button
          className="btn-primary"
          onClick={() => handleNext(true)}
          style={{ flex: 1, padding: '0.8rem', justifyContent: 'center', background: 'var(--gradient-success)' }}
        >
          <i className="fa-solid fa-circle-check"></i> Mastered (+15 XP)
        </button>
      </div>
    </div>
  );
}
