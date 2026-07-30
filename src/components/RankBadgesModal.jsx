import React from 'react';

const BADGES = [
  { id: 'first_quiz', name: 'First Step Doctor', icon: 'fa-user-nurse', desc: 'Completed 1st practice question block', minQs: 1, color: 'var(--accent-cyan)' },
  { id: 'fifty_qs', name: 'Dedicated Scholar', icon: 'fa-book-open-reader', desc: 'Solved 50+ board MCQs', minQs: 50, color: 'var(--accent-blue)' },
  { id: 'century', name: 'Century Master', icon: 'fa-award', desc: 'Solved 100+ board MCQs', minQs: 100, color: 'var(--accent-indigo)' },
  { id: 'high_accuracy', name: 'Precision Specialist', icon: 'fa-bullseye', desc: 'Achieved 80%+ accuracy in an exam', minAcc: 80, minQs: 10, color: 'var(--accent-emerald)' },
  { id: 'mock_champion', name: 'Board Exam Ready', icon: 'fa-trophy', desc: 'Passed a full 50+ MCQ timed mock exam', requiresMock: true, color: 'var(--accent-purple)' },
  { id: 'grand_doctor', name: 'Medical Fellow', icon: 'fa-crown', desc: 'Solved 250+ board MCQs', minQs: 250, color: 'var(--accent-amber)' }
];

export default function RankBadgesModal({ isOpen, onClose, stats, history }) {
  if (!isOpen) return null;

  const totalAttempted = stats?.attemptedCount || 0;
  const accuracy = totalAttempted > 0 ? Math.round((stats.correctCount / totalAttempted) * 100) : 0;
  const passedMocks = history ? history.filter(h => h.scorePercentage >= 70).length : 0;

  // Calculate Level and XP
  const xpPerQ = 10;
  const totalXP = totalAttempted * xpPerQ + passedMocks * 50;
  const level = Math.floor(totalXP / 200) + 1;
  const xpInCurrentLevel = totalXP % 200;
  const xpForNextLevel = 200;
  const progressPct = Math.min(100, Math.round((xpInCurrentLevel / xpForNextLevel) * 100));

  let rankTitle = 'Junior Medical Resident';
  if (level >= 10) rankTitle = 'Chief Medical Fellow';
  else if (level >= 5) rankTitle = 'Senior Specialist Resident';
  else if (level >= 3) rankTitle = 'Medical Resident';

  return (
    <div style={{
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
      <div className="glass-panel animate-fade-in" style={{
        maxWidth: '680px',
        width: '100%',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '1.5rem',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-glow)',
        position: 'relative',
        borderRadius: 'var(--radius-md)'
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '1.25rem',
            right: '1.25rem',
            background: 'rgba(255,255,255,0.06)',
            border: 'none',
            color: 'var(--text-muted)',
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.1rem'
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        {/* Hero Header */}
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '18px',
            background: 'var(--gradient-gold)',
            color: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2rem',
            margin: '0 auto 0.85rem',
            boxShadow: '0 0 25px rgba(245, 158, 11, 0.4)'
          }}>
            <i className="fa-solid fa-crown"></i>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }} className="gradient-text">
            Level {level} &bull; {rankTitle}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
            Earn XP by solving questions and passing mock examinations
          </p>
        </div>

        {/* Level XP Progress Bar */}
        <div className="glass-panel" style={{ padding: '1.15rem', marginBottom: '1.5rem', background: 'rgba(255,255,255,0.02)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.4rem' }}>
            <span>Level {level} Progress ({totalXP} Total XP)</span>
            <strong style={{ color: 'var(--accent-amber)' }}>{xpInCurrentLevel} / {xpForNextLevel} XP</strong>
          </div>
          <div style={{ height: '10px', background: 'rgba(255,255,255,0.08)', borderRadius: '99px', overflow: 'hidden' }}>
            <div style={{
              height: '100%',
              width: `${progressPct}%`,
              background: 'var(--gradient-gold)',
              transition: 'width 0.4s ease'
            }}></div>
          </div>
        </div>

        {/* Badges Grid */}
        <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <i className="fa-solid fa-award" style={{ color: 'var(--accent-cyan)' }}></i>
          Unlocked Milestones & Badges
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.85rem', marginBottom: '1.5rem' }}>
          {BADGES.map(badge => {
            let isUnlocked = false;
            if (badge.minQs && totalAttempted >= badge.minQs) isUnlocked = true;
            if (badge.minAcc && accuracy >= badge.minAcc && totalAttempted >= (badge.minQs || 1)) isUnlocked = true;
            if (badge.requiresMock && passedMocks > 0) isUnlocked = true;

            return (
              <div
                key={badge.id}
                style={{
                  padding: '1rem',
                  borderRadius: 'var(--radius-sm)',
                  background: isUnlocked ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.01)',
                  border: `1px solid ${isUnlocked ? badge.color : 'var(--border-subtle)'}`,
                  opacity: isUnlocked ? 1 : 0.45,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.85rem'
                }}
              >
                <div style={{
                  width: '42px',
                  height: '42px',
                  borderRadius: '12px',
                  background: isUnlocked ? `${badge.color}25` : 'rgba(255,255,255,0.05)',
                  color: isUnlocked ? badge.color : 'var(--text-muted)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.2rem',
                  flexShrink: 0
                }}>
                  <i className={`fa-solid ${badge.icon}`}></i>
                </div>

                <div>
                  <strong style={{ fontSize: '0.9rem', display: 'block', color: isUnlocked ? 'var(--text-main)' : 'var(--text-muted)' }}>
                    {badge.name}
                  </strong>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '0.1rem' }}>
                    {badge.desc}
                  </span>
                  <span style={{ fontSize: '0.68rem', fontWeight: 700, color: isUnlocked ? badge.color : 'var(--text-subdued)', marginTop: '0.2rem', display: 'block' }}>
                    {isUnlocked ? '✓ UNLOCKED' : '🔒 LOCKED'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ textAlign: 'center' }}>
          <button className="btn-primary" onClick={onClose} style={{ padding: '0.7rem 2rem' }}>
            <i className="fa-solid fa-check"></i> Close Milestone Drawer
          </button>
        </div>
      </div>
    </div>
  );
}
