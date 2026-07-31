import React, { useEffect } from 'react';

export default function ExamLaunchModal({ isOpen, onClose, examTrack, onLaunchBlock }) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      const handleEsc = (e) => { if (e.key === 'Escape') onClose(); };
      document.addEventListener('keydown', handleEsc);
      return () => {
        document.body.style.overflow = 'auto';
        document.removeEventListener('keydown', handleEsc);
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen || !examTrack) return null;

  const getExamStructure = (track) => {
    switch (track) {
      case 'FCPS Part 1':
        return {
          title: 'FCPS Part 1 Board Examination',
          total: 200,
          blocks: [
            { id: 1, name: 'Paper 1', limit: 100, timeLimitMinutes: 150 },
            { id: 2, name: 'Paper 2', limit: 100, timeLimitMinutes: 150 }
          ]
        };
      case 'USMLE Step 1':
        return {
          title: 'USMLE Step 1',
          total: 280,
          blocks: Array.from({ length: 7 }, (_, i) => ({
            id: i + 1, name: `Block ${i + 1}`, limit: 40, timeLimitMinutes: 60
          }))
        };
      case 'USMLE Step 2 CK':
        return {
          title: 'USMLE Step 2 CK',
          total: 320,
          blocks: Array.from({ length: 8 }, (_, i) => ({
            id: i + 1, name: `Block ${i + 1}`, limit: 40, timeLimitMinutes: 60
          }))
        };
      case 'PLAB / UKMLA':
        return {
          title: 'PLAB / UKMLA Part 1',
          total: 180,
          blocks: [
            { id: 1, name: 'Full Paper', limit: 180, timeLimitMinutes: 180 }
          ]
        };
      case 'NEET PG':
        return {
          title: 'NEET PG / INI-CET',
          total: 200,
          blocks: [
            { id: 1, name: 'Full Exam', limit: 200, timeLimitMinutes: 210 }
          ]
        };
      case 'MRCS Surgery':
        return {
          title: 'MRCS Part A (Surgery)',
          total: 300,
          blocks: [
            { id: 1, name: 'Paper 1 (Applied Basic Science)', limit: 100, timeLimitMinutes: 120 },
            { id: 2, name: 'Paper 2 (Principles of Surgery)', limit: 200, timeLimitMinutes: 150 }
          ]
        };
      default:
        return {
          title: `${track} Examination`,
          total: 100,
          blocks: [
            { id: 1, name: 'Standard Block', limit: 100, timeLimitMinutes: 120 }
          ]
        };
    }
  };

  const structure = getExamStructure(examTrack);

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.75)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      zIndex: 9999,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }} onClick={onClose}>
      
      <div 
        className="glass-panel animate-slide-up" 
        onClick={e => e.stopPropagation()}
        style={{
          width: '100%',
          maxWidth: '520px',
          padding: '2rem 1.5rem',
          position: 'relative',
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-lg)',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <button 
          onClick={onClose}
          style={{
            position: 'absolute', top: '1rem', right: '1rem',
            background: 'transparent', border: 'none', color: 'var(--text-muted)',
            cursor: 'pointer', fontSize: '1.2rem', padding: '0.5rem', zIndex: 10
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        <div style={{ textAlign: 'center', marginBottom: '1.5rem', flexShrink: 0 }}>
          <div style={{
            width: '64px', height: '64px', margin: '0 auto 1rem',
            background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)',
            borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.8rem', border: '1px solid rgba(6, 182, 212, 0.3)'
          }}>
            <i className="fa-solid fa-file-medical"></i>
          </div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-main)' }}>
            {structure.title}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Official Format • {structure.total} Total MCQs
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', overflowY: 'auto', paddingRight: '0.5rem' }}>
          {structure.blocks.map((block) => (
            <div 
              key={block.id}
              style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '1rem 1.25rem', background: 'rgba(255,255,255,0.03)',
                border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-sm)',
                transition: 'border-color 0.2s', flexWrap: 'wrap', gap: '1rem'
              }}
            >
              <div>
                <h4 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '0.2rem' }}>
                  {block.name}
                </h4>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', gap: '1rem' }}>
                  <span><i className="fa-solid fa-list-ol"></i> {block.limit} MCQs</span>
                  <span><i className="fa-regular fa-clock"></i> {block.timeLimitMinutes} Mins</span>
                </div>
              </div>

              <button 
                className="btn-primary"
                onClick={() => onLaunchBlock(examTrack, block.limit, block.timeLimitMinutes, block.name)}
                style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem', whiteSpace: 'nowrap' }}
              >
                Launch Block <i className="fa-solid fa-arrow-right"></i>
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
