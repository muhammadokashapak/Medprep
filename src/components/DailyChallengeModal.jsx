import React from 'react';

export default function DailyChallengeModal({ isOpen, onClose, onStartChallenge, streak = 0 }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.8)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      zIndex: 9999,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }} onClick={onClose}>
      <div
        className="glass-panel animate-slide-up text-center"
        onClick={e => e.stopPropagation()}
        style={{
          maxWidth: '460px',
          width: '100%',
          padding: '2.5rem 1.5rem',
          position: 'relative',
          borderRadius: 'var(--radius-lg)',
          borderTop: '6px solid var(--accent-amber)'
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute', top: '1rem', right: '1rem',
            background: 'transparent', border: 'none', color: 'var(--text-muted)',
            cursor: 'pointer', fontSize: '1.2rem'
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        <div style={{
          width: '72px', height: '72px', borderRadius: '50%',
          background: 'rgba(245, 158, 11, 0.15)', color: 'var(--accent-amber)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '2.2rem', margin: '0 auto 1.25rem', border: '1px solid rgba(245, 158, 11, 0.3)'
        }}>
          <i className="fa-solid fa-fire-flame-curved"></i>
        </div>

        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '0.4rem', color: 'var(--text-main)' }}>
          Daily MCQ Sprint Challenge!
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
          Solve 10 mixed high-yield board questions in 10 minutes to maintain your study streak and earn <strong>+100 Bonus XP</strong>!
        </p>

        <div style={{
          background: 'rgba(255,255,255,0.03)',
          padding: '1rem',
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--border-subtle)',
          marginBottom: '1.75rem',
          display: 'flex',
          justifyContent: 'space-around'
        }}>
          <div>
            <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700 }}>CURRENT STREAK</span>
            <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-amber)' }}>
              🔥 {streak} Days
            </span>
          </div>
          <div style={{ borderLeft: '1px solid var(--border-subtle)' }}></div>
          <div>
            <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700 }}>REWARD</span>
            <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
              +100 XP
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
          <button className="btn-secondary" onClick={onClose} style={{ width: 'auto' }}>
            Later
          </button>
          <button className="btn-primary" onClick={onStartChallenge} style={{ width: 'auto', padding: '0.75rem 1.75rem', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }}>
            <i className="fa-solid fa-play"></i> Start 10-Q Sprint
          </button>
        </div>
      </div>
    </div>
  );
}
