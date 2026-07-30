import React, { useEffect } from 'react';

export default function UserProfileModal({ isOpen, onClose, user, stats, history, onLogout, resetProgress, addToast, updateUserPreference }) {
  useEffect(() => {
    const handleEsc = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen || !user) return null;

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
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1000,
      background: 'rgba(11, 15, 25, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }}>
      <div className="glass-panel animate-fade-in" onClick={e => e.stopPropagation()} style={{
        maxWidth: '500px',
        width: '100%',
        padding: '1.5rem 1.25rem',
        position: 'relative',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-glow)',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            fontSize: '1.1rem'
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        {/* Profile Avatar & Info Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: '50%',
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontSize: '1.5rem',
            fontWeight: 700,
            boxShadow: 'var(--shadow-glow)',
            flexShrink: 0
          }}>
            {user.name ? user.name.charAt(0).toUpperCase() : 'D'}
          </div>

          <div style={{ overflow: 'hidden' }}>
            <h3 title={user.name} style={{ fontSize: '1.25rem', marginBottom: '0.15rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user.name}</h3>
            <p title={user.email} style={{ color: 'var(--text-muted)', fontSize: '0.82rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user.email}</p>
            <span className="badge" style={{ marginTop: '0.35rem', fontSize: '0.72rem' }}>
              {user.examPreference || 'General Track'} Candidate
            </span>
          </div>
        </div>

        {/* Change Exam Track */}
        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
          <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '0.5rem' }}>CHANGE TARGET EXAM</label>
          <select
            value={user.examPreference || 'FCPS Part 1'}
            onChange={e => updateUserPreference && updateUserPreference(e.target.value)}
            style={{
              width: '100%',
              padding: '0.6rem 0.85rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              background: 'var(--bg-card)',
              color: 'var(--text-main)',
              fontSize: '0.88rem',
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

        {/* User Quick Stats Summary */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '0.65rem',
          marginBottom: '1.5rem',
          background: 'rgba(255,255,255,0.03)',
          padding: '1rem 0.75rem',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
          textAlign: 'center'
        }}>
          <div>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block' }}>Attempted</span>
            <strong style={{ fontSize: '1.15rem', color: 'var(--accent-cyan)' }}>{stats?.attemptedCount ?? 0}</strong>
          </div>

          <div>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block' }}>Accuracy</span>
            <strong style={{ fontSize: '1.15rem', color: 'var(--accent-emerald)' }}>
              {(stats?.attemptedCount && stats.attemptedCount > 0) ? Math.round(((stats?.correctCount || 0) / stats.attemptedCount) * 100) : 0}%
            </strong>
          </div>

          <div>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block' }}>Mocks</span>
            <strong style={{ fontSize: '1.15rem', color: 'var(--accent-purple)' }}>{Array.isArray(history) ? history.length : 0}</strong>
          </div>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <button
            onClick={handleReset}
            className="btn-secondary"
            style={{ width: '100%', justifyContent: 'center', color: 'var(--accent-rose)', borderColor: 'rgba(244,63,94,0.3)', minHeight: '42px', fontSize: '0.88rem' }}
          >
            <i className="fa-solid fa-rotate-left"></i> Reset All Test Statistics
          </button>

          <button
            onClick={handleLogoutClick}
            className="btn-primary"
            style={{ width: '100%', justifyContent: 'center', background: 'var(--gradient-danger)', minHeight: '42px', fontSize: '0.88rem' }}
          >
            <i className="fa-solid fa-right-from-bracket"></i> Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}
