import React, { useState, useMemo, useEffect } from 'react';
import { SUBJECT_METADATA, groupQuestionsBySubject } from '../utils/subjectCategorizer';

export default function SubjectBrowser({ questions = [], startSubjectQuiz }) {
  const [selectedLimit, setSelectedLimit] = useState(25);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const subjectGroups = useMemo(() => {
    return groupQuestionsBySubject(questions);
  }, [questions]);

  const filteredSubjects = useMemo(() => {
    return Object.keys(SUBJECT_METADATA).filter(subjKey => {
      const meta = SUBJECT_METADATA[subjKey];
      return meta.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
             meta.description.toLowerCase().includes(searchTerm.toLowerCase());
    });
  }, [searchTerm]);

  return (
    <div className="animate-fade-in" style={{ padding: '1rem 0', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{
        padding: '2rem 1.5rem',
        marginBottom: '1.5rem',
        background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%)',
        borderLeft: '5px solid var(--accent-cyan)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-cyan)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
              SUBJECT-WISE STUDY MODE
            </span>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, margin: '0.2rem 0 0.4rem', color: 'var(--text-main)' }}>
              Medical Discipline Modules
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>
              Master targeted subjects with high-yield clinical MCQs and comprehensive static rationales.
            </p>
          </div>

          {/* Question Count Limit Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(0,0,0,0.2)', padding: '0.4rem 0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>BLOCK SIZE:</span>
            {[10, 25, 50, 100].map(limit => (
              <button
                key={limit}
                onClick={() => setSelectedLimit(limit)}
                style={{
                  padding: '0.35rem 0.65rem',
                  borderRadius: '4px',
                  border: 'none',
                  fontSize: '0.8rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  background: selectedLimit === limit ? 'var(--accent-cyan)' : 'transparent',
                  color: selectedLimit === limit ? '#fff' : 'var(--text-muted)',
                  transition: 'all 0.2s'
                }}
              >
                {limit} Qs
              </button>
            ))}
          </div>
        </div>

        {/* Search Bar */}
        <div style={{ marginTop: '1.25rem', position: 'relative', maxWidth: '400px' }}>
          <i className="fa-solid fa-magnifying-glass" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}></i>
          <input
            type="text"
            placeholder="Search subjects (e.g. Pathology, Anatomy)..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 1rem 0.65rem 2.6rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              background: 'rgba(0,0,0,0.3)',
              color: 'var(--text-main)',
              fontSize: '0.88rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Grid of Subject Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
        {filteredSubjects.map(subjKey => {
          const meta = SUBJECT_METADATA[subjKey];
          const questionsInSubj = subjectGroups[subjKey] || [];
          const count = questionsInSubj.length;

          return (
            <div
              key={subjKey}
              className="glass-panel"
              style={{
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.2s, box-shadow 0.2s',
                borderTop: `4px solid ${meta.color}`
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', marginBottom: '1rem' }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: meta.bg,
                    color: meta.color,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.4rem'
                  }}>
                    <i className={`fa-solid ${meta.icon}`}></i>
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: 'var(--text-main)' }}>
                      {meta.name}
                    </h3>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                      {count.toLocaleString()} MCQs Available
                    </span>
                  </div>
                </div>

                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5, marginBottom: '1.5rem' }}>
                  {meta.description}
                </p>
              </div>

              <button
                className="btn-primary"
                onClick={() => startSubjectQuiz?.(subjKey, questionsInSubj, selectedLimit)}
                style={{
                  width: '100%',
                  justifyContent: 'center',
                  padding: '0.75rem',
                  fontSize: '0.88rem',
                  background: `linear-gradient(135deg, ${meta.color} 0%, rgba(0,0,0,0.8) 100%)`,
                  border: 'none'
                }}
              >
                <i className="fa-solid fa-play"></i> Start {selectedLimit} Q Practice Block
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
