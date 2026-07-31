import React from 'react';

export default function Navbar({ activeTab, setActiveTab, stats, theme, toggleTheme, currentUser, onOpenAuth, onOpenProfile, onLeaveExam, totalQuestions = 48000 }) {
  const isExamActive = activeTab === 'practice';

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: 'fa-table-columns' },
    { id: 'subjects', label: 'Subjects', icon: 'fa-shapes' },
    { id: 'mistakes', label: 'Mistakes', icon: 'fa-brain' }
  ];

  const handleTabChange = (tabId) => {
    if (isExamActive) {
      if (!window.confirm('Leave active examination session? Your progress up to your last answered question is recorded.')) {
        return;
      }
      onLeaveExam?.();
    }
    setActiveTab(tabId);
  };

  return (
    <>
      <header style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        background: 'var(--bg-glass)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid var(--border-subtle)',
        padding: '0.65rem 1rem',
        transition: 'background 0.3s ease'
      }}>
        <div style={{
          maxWidth: '1300px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '0.5rem'
        }}>
          {/* Brand Emblem & App Title */}
          <div 
            onClick={() => handleTabChange('dashboard')} 
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && handleTabChange('dashboard')}
            style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', cursor: 'pointer' }}
          >
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'var(--gradient-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--shadow-glow)',
              flexShrink: 0
            }}>
              <i className="fa-solid fa-stethoscope" style={{ fontSize: '1.1rem' }}></i>
            </div>
            <div>
              <h2 style={{ fontSize: '1.18rem', lineHeight: 1, letterSpacing: '-0.02em' }} className="gradient-text">
                MedPrep Pro
              </h2>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 500 }} className="desktop-only">
                {isExamActive ? 'Secure Board Testing Mode' : 'Global Medical Licensing Platform'}
              </span>
            </div>
          </div>

          {/* Desktop Navigation Tabs */}
          {!isExamActive && currentUser && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
              background: 'rgba(255,255,255,0.03)',
              padding: '0.25rem',
              borderRadius: 'var(--radius-full)',
              border: '1px solid var(--border-subtle)'
            }} className="desktop-only">
              {navItems.map(item => {
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => handleTabChange(item.id)}
                    style={{
                      padding: '0.45rem 1.1rem',
                      borderRadius: 'var(--radius-full)',
                      border: 'none',
                      background: isActive ? 'var(--gradient-primary)' : 'transparent',
                      color: isActive ? '#ffffff' : 'var(--text-muted)',
                      fontWeight: 600,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.45rem',
                      transition: 'all 0.2s ease',
                      boxShadow: isActive ? 'var(--shadow-glow)' : 'none'
                    }}
                  >
                    <i className={`fa-solid ${item.icon}`}></i>
                    {item.label}
                  </button>
                );
              })}
            </div>
          )}

          {/* Right Controls & Profile */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {isExamActive && (
              <button 
                onClick={() => {
                  if (window.confirm('Leave active examination session? Your progress up to your last answered question is recorded.')) {
                    onLeaveExam?.();
                    setActiveTab('dashboard');
                  }
                }}
                style={{
                  padding: '0.4rem 0.85rem',
                  fontSize: '0.82rem',
                  background: 'rgba(239, 68, 68, 0.1)',
                  color: 'var(--accent-rose)',
                  border: '1px solid rgba(239, 68, 68, 0.2)',
                  borderRadius: 'var(--radius-full)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  fontWeight: 600
                }}
              >
                <i className="fa-solid fa-arrow-right-from-bracket"></i>
                <span className="desktop-only">Exit Exam</span>
              </button>
            )}
            {!isExamActive && (
              <div className="badge desktop-only" style={{ padding: '0.4rem 0.9rem', fontSize: '0.82rem' }}>
                <i className="fa-solid fa-fire" style={{ color: 'var(--accent-amber)' }}></i>
                <span>{(stats?.attemptedCount ?? 0).toLocaleString()} / {totalQuestions.toLocaleString()} Solved</span>
              </div>
            )}

            {currentUser ? (
              <div 
                onClick={onOpenProfile}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onOpenProfile?.()}
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.5rem', 
                  cursor: 'pointer', 
                  background: 'rgba(255,255,255,0.05)', 
                  padding: '0.3rem 0.65rem', 
                  borderRadius: 'var(--radius-full)',
                  border: '1px solid var(--border-subtle)',
                  transition: 'border-color 0.2s'
                }}
              >
                <div style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  background: 'var(--gradient-primary)',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.82rem'
                }}>
                  {currentUser.name ? currentUser.name.charAt(0).toUpperCase() : 'D'}
                </div>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, maxWidth: '130px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} className="desktop-only">{currentUser.name}</span>
                <i className="fa-solid fa-chevron-down desktop-only" style={{ fontSize: '0.7rem', color: 'var(--text-subdued)' }}></i>
              </div>
            ) : (
              <button 
                className="btn-primary" 
                onClick={onOpenAuth}
                style={{ padding: '0.4rem 0.85rem', fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: '0.45rem', minHeight: '36px' }}
              >
                <i className="fa-solid fa-user-doctor"></i> <span>Sign In</span>
              </button>
            )}

            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              style={{
                width: '36px',
                height: '36px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
                background: 'var(--bg-card)',
                color: 'var(--text-main)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.92rem',
                transition: 'border-color 0.2s',
                flexShrink: 0
              }}
              title="Toggle Light/Dark Theme"
            >
              <i className={`fa-solid ${theme === 'dark' ? 'fa-sun' : 'fa-moon'}`}></i>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Bottom Navigation Bar */}
      {!isExamActive && currentUser && (
        <nav className="mobile-bottom-nav">
          <button 
            className={`mobile-nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => handleTabChange('dashboard')}
          >
            <i className="fa-solid fa-table-columns"></i>
            <span>Dashboard</span>
          </button>

          <button 
            className={`mobile-nav-item ${activeTab === 'mistakes' ? 'active' : ''}`}
            onClick={() => handleTabChange('mistakes')}
          >
            <i className="fa-solid fa-brain"></i>
            <span>Mistakes</span>
          </button>
          <button 
            className="mobile-nav-item"
            onClick={onOpenProfile}
          >
            <i className="fa-solid fa-user-doctor"></i>
            <span>Profile</span>
          </button>
        </nav>
      )}
    </>
  );
}
