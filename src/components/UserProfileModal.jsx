import React, { useEffect } from 'react';
import { getUserGamificationData, getCurrentRank } from '../utils/gamification';

export default function UserProfileModal({ isOpen, onClose, user, stats, history, onLogout, resetProgress, addToast, updateUserPreference }) {
  useEffect(() => {
    const handleEsc = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen || !user) return null;

  const attempted = stats?.attemptedCount ?? 0;
  const accuracy = (stats?.attemptedCount && stats.attemptedCount > 0) 
    ? Math.round(((stats?.correctCount || 0) / stats.attemptedCount) * 100) 
    : 0;
  const mockCount = Array.isArray(history) ? history.length : 0;
  const gamification = getUserGamificationData();
  const rank = getCurrentRank(gamification?.xp || 0);

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all test statistics and mistakes bank? This action cannot be undone.')) {
      resetProgress();
      addToast('All progress statistics have been reset', 'info');
      onClose();
    }
  };

  const handleLogoutClick = () => {
    onLogout();
    addToast('Logged out successfully', 'info');
    onClose();
  };

  return (
    <div 
      onClick={onClose}
      style={{
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        zIndex: 9999,
        background: 'rgba(9, 13, 22, 0.85)',
        backdropFilter: 'blur(14px)',
        WebkitBackdropFilter: 'blur(14px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1.25rem'
      }}
    >
      <div
        className="animate-slide-up"
        onClick={e => e.stopPropagation()}
        style={{
          maxWidth: '520px',
          width: '100%',
          padding: '2.25rem 1.75rem',
          position: 'relative',
          background: 'var(--bg-card)',
          color: 'var(--text-main)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          boxShadow: 'var(--shadow-card)',
          maxHeight: '90vh',
          overflowY: 'auto'
        }}
      >
        {/* Close Button */}
        <button
          className="submit-modal-close"
          onClick={onClose}
          title="Close profile"
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        {/* Doctor Hero Avatar & Header */}
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{
            width: '76px',
            height: '76px',
            borderRadius: '50%',
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontSize: '2rem',
            fontWeight: 800,
            margin: '0 auto 1rem',
            boxShadow: 'var(--shadow-glow)',
            border: '3px solid rgba(6, 182, 212, 0.3)'
          }}>
            {user.name ? user.name.charAt(0).toUpperCase() : 'D'}
          </div>

          <h2 style={{ fontSize: '1.4rem', fontWeight: 800, margin: '0 0 0.2rem', color: 'var(--text-main)' }}>
            Dr. {user.name || 'Candidate'}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', margin: '0 0 0.75rem' }}>
            {user.email}
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span className="badge" style={{
              background: 'rgba(16, 185, 129, 0.12)',
              color: 'var(--accent-emerald)',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              fontSize: '0.75rem',
              fontWeight: 700
            }}>
              <i className="fa-solid fa-circle-check" style={{ marginRight: '0.3rem' }}></i> Verified Candidate
            </span>

            <span className="badge" style={{
              background: `${rank.color}20`,
              color: rank.color,
              border: `1px solid ${rank.color}40`,
              fontSize: '0.75rem',
              fontWeight: 700
            }}>
              <i className={`fa-solid ${rank.icon}`} style={{ marginRight: '0.3rem' }}></i> {rank.title}
            </span>
          </div>
        </div>

        {/* Change Target Exam Track */}
        <div style={{
          marginBottom: '1.5rem',
          padding: '1.1rem 1.25rem',
          background: 'var(--bg-card-hover)',
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--border-subtle)'
        }}>
          <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 800, marginBottom: '0.45rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <i className="fa-solid fa-graduation-cap" style={{ marginRight: '0.35rem' }}></i> TARGET BOARD EXAM TRACK
          </label>
          <select
            value={user.examPreference || 'FCPS Part 1'}
            onChange={e => updateUserPreference && updateUserPreference(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              background: 'var(--bg-card)',
              color: 'var(--text-main)',
              fontSize: '0.92rem',
              fontWeight: 700,
              cursor: 'pointer',
              outline: 'none'
            }}
          >
            <option value="FCPS Part 1">FCPS Part 1 (Pakistan)</option>
            <option value="USMLE Step 1">USMLE Step 1 (USA)</option>
            <option value="USMLE Step 2 CK">USMLE Step 2 CK (USA)</option>
            <option value="PLAB / UKMLA">PLAB / UKMLA (UK)</option>
            <option value="NEET PG">NEET PG / INI-CET (India)</option>
            <option value="MRCS Surgery">MRCS Part A Surgery (UK/Intl)</option>
          </select>
        </div>

        {/* User Quick Stats Summary Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '0.75rem',
          marginBottom: '1.75rem'
        }}>
          <div style={{
            padding: '1rem 0.5rem',
            background: 'var(--bg-card-hover)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)',
            textAlign: 'center'
          }}>
            <i className="fa-solid fa-circle-check" style={{ color: 'var(--accent-cyan)', fontSize: '1.1rem', marginBottom: '0.2rem' }}></i>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', fontWeight: 700, textTransform: 'uppercase' }}>Attempted</span>
            <strong style={{ fontSize: '1.3rem', color: 'var(--accent-cyan)', fontWeight: 800 }}>{attempted}</strong>
          </div>

          <div style={{
            padding: '1rem 0.5rem',
            background: 'var(--bg-card-hover)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)',
            textAlign: 'center'
          }}>
            <i className="fa-solid fa-bullseye" style={{ color: 'var(--accent-emerald)', fontSize: '1.1rem', marginBottom: '0.2rem' }}></i>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', fontWeight: 700, textTransform: 'uppercase' }}>Accuracy</span>
            <strong style={{ fontSize: '1.3rem', color: 'var(--accent-emerald)', fontWeight: 800 }}>{accuracy}%</strong>
          </div>

          <div style={{
            padding: '1rem 0.5rem',
            background: 'var(--bg-card-hover)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)',
            textAlign: 'center'
          }}>
            <i className="fa-solid fa-award" style={{ color: 'var(--accent-purple)', fontSize: '1.1rem', marginBottom: '0.2rem' }}></i>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', fontWeight: 700, textTransform: 'uppercase' }}>Mocks</span>
            <strong style={{ fontSize: '1.3rem', color: 'var(--accent-purple)', fontWeight: 800 }}>{mockCount}</strong>
          </div>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <button
            onClick={handleReset}
            className="btn-secondary"
            style={{ width: '100%', justifyContent: 'center', color: 'var(--accent-rose)', borderColor: 'rgba(244, 63, 94, 0.4)', minHeight: '44px', fontSize: '0.9rem', fontWeight: 700 }}
          >
            <i className="fa-solid fa-arrows-rotate"></i> Reset All Test Statistics
          </button>

          <button
            onClick={handleLogoutClick}
            className="btn-primary"
            style={{ width: '100%', justifyContent: 'center', background: 'var(--gradient-danger)', minHeight: '44px', fontSize: '0.9rem', fontWeight: 700 }}
          >
            <i className="fa-solid fa-right-from-bracket"></i> Sign Out Account
          </button>
        </div>
      </div>
    </div>
  );
}
