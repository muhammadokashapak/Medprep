import React, { useState, useEffect } from 'react';

export default function DailyGoalModal({ isOpen, onClose, currentGoal, onSetGoal }) {
  const [customValue, setCustomValue] = useState('');

  useEffect(() => {
    const handleEsc = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const goalOptions = [20, 35, 50, 75, 100];

  return (
    <div role="dialog" aria-modal="true" aria-label="Set Daily Goal" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1100,
      background: 'rgba(11, 15, 25, 0.85)',
      backdropFilter: 'blur(10px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }}>
      <div className="glass-panel animate-fade-in text-center" style={{
        maxWidth: '440px',
        width: '100%',
        padding: '1.75rem 1.25rem',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-glow)',
        position: 'relative'
      }}>
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '1.25rem',
            right: '1.25rem',
            background: 'rgba(255,255,255,0.06)',
            border: 'none',
            color: 'var(--text-muted)',
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        <div style={{
          width: '52px',
          height: '52px',
          borderRadius: '16px',
          background: 'var(--gradient-primary)',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.5rem',
          margin: '0 auto 1rem'
        }}>
          <i className="fa-solid fa-bullseye"></i>
        </div>

        <h3 style={{ fontSize: '1.3rem', marginBottom: '0.35rem' }} className="gradient-text">
          Customize Daily Target
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1.5rem' }}>
          Select how many board MCQs you aim to complete each day to maintain your study velocity.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(70px, 1fr))', gap: '0.65rem', marginBottom: '1.5rem' }}>
          {goalOptions.map(option => {
            const isSel = currentGoal === option;
            return (
              <button
                key={option}
                onClick={() => {
                  onSetGoal(option);
                  onClose();
                }}
                style={{
                  padding: '0.75rem 0.5rem',
                  borderRadius: 'var(--radius-sm)',
                  border: `1.5px solid ${isSel ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
                  background: isSel ? 'rgba(6, 182, 212, 0.18)' : 'rgba(255,255,255,0.03)',
                  color: isSel ? 'var(--accent-cyan)' : 'var(--text-main)',
                  fontWeight: 800,
                  fontSize: '0.95rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                {option}
              </button>
            );
          })}
        </div>

        {/* Custom Goal Input */}
        <div style={{ marginBottom: '1.5rem', textAlign: 'left' }}>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Or set a custom goal:</p>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="number"
              min="1"
              max="500"
              placeholder="e.g. 30"
              value={customValue}
              onChange={e => setCustomValue(e.target.value)}
              style={{
                flex: 1,
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
                background: 'rgba(255,255,255,0.04)',
                color: 'var(--text-main)',
                outline: 'none',
                fontSize: '0.9rem'
              }}
            />
            <button
              className="btn-primary"
              onClick={() => {
                const val = parseInt(customValue, 10);
                if (val >= 1 && val <= 500) {
                  onSetGoal(val);
                  onClose();
                }
              }}
              style={{ padding: '0.65rem 1rem', width: 'auto' }}
            >
              Set
            </button>
          </div>
        </div>

        <button className="btn-secondary" onClick={onClose} style={{ width: '100%', justifyContent: 'center' }}>
          Cancel
        </button>
      </div>
    </div>
  );
}
