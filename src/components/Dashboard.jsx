import React, { useState, useMemo } from 'react';

const examTracks = [
  {
    id: 'USMLE Step 1',
    title: 'USMLE Step 1 QBank',
    format: '280 Questions • 8 Hours (7 Blocks)',
    desc: 'Organ systems-based basic science vignettes from First Aid Step 1, Pathoma & Physiology.',
    icon: 'fa-book-medical',
    color: 'var(--accent-cyan)',
    questionsCount: '12,000+ MCQs'
  },
  {
    id: 'USMLE Step 2 CK',
    title: 'USMLE Step 2 CK QBank',
    format: '320 Questions • 9 Hours (8 Blocks)',
    desc: 'Clinical Knowledge board exam review from First Aid for the USMLE Step 2 CK.',
    icon: 'fa-notes-medical',
    color: 'var(--accent-indigo)',
    questionsCount: '4,000+ MCQs'
  },
  {
    id: 'FCPS Part 1',
    title: 'FCPS Part 1 & NLE QBank',
    format: '200 Questions • 6 Hours (2 Papers)',
    desc: 'Pakistani licensing & residency exam questions from ROAMS Review & Pathoma 2021.',
    icon: 'fa-graduation-cap',
    color: 'var(--accent-emerald)',
    questionsCount: '8,000+ MCQs'
  },
  {
    id: 'PLAB / UKMLA',
    title: 'PLAB 1 / UKMLA QBank',
    format: '180 Questions • 3 Hours (SBA Format)',
    desc: 'UK General Medical Council Licensing Exam clinical decision-making vignettes.',
    icon: 'fa-hospital-user',
    color: 'var(--accent-purple)',
    questionsCount: '8,000+ MCQs'
  },
  {
    id: 'NEET PG',
    title: 'NEET PG & FMGE QBank',
    format: '200 Questions • 3.5 Hours (210 Mins)',
    desc: 'High-yield Indian medical entrance prof revision from Garg & Gupta Pharm and ROAMS Review.',
    icon: 'fa-user-doctor',
    color: 'var(--accent-amber)',
    questionsCount: '12,000+ MCQs'
  },
  {
    id: 'MRCS Surgery',
    title: 'MRCS & MS Surgery QBank',
    format: '300 Questions • 5 Hours (2 Papers)',
    desc: 'Royal College of Surgeons Part A & MS Surgery vignettes from Bailey & Love Surgery.',
    icon: 'fa-user-nurse',
    color: 'var(--accent-rose)',
    questionsCount: '4,000+ MCQs'
  }
];

export default function Dashboard({ stats = { attemptedCount: 0, correctCount: 0, mistakesList: [], todayAttemptedCount: 0 }, history = [], startQuiz, onOpenLaunchModal, currentUser, onOpenAuth, onOpenProfile, onOpenCompareModal, onOpenRankModal, onOpenGoalModal, dailyGoal = 50 }) {
  const [selectedMockLimit, setSelectedMockLimit] = useState(50);
  const [dailyCaseSelected, setDailyCaseSelected] = useState(null);
  const [showCaseRationale, setShowCaseRationale] = useState(false);

  const accuracy = stats.attemptedCount > 0 
    ? Math.round((stats.correctCount / stats.attemptedCount) * 100) 
    : 0;

  // Calculate Best Score from attempt history
  const totalTests = history ? history.length : 0;
  const bestScore = history && history.length > 0 ? Math.max(...history.map(h => h.scorePercentage || 0)) : 0;

  // Calculate real-time subject breakdown accuracy dynamically from history details
  const subjectAccuracyMap = useMemo(() => {
    const map = {
      'Pathology': { total: 0, correct: 0 },
      'Pharmacology': { total: 0, correct: 0 },
      'Anatomy': { total: 0, correct: 0 },
      'Physiology': { total: 0, correct: 0 }
    };

    if (history && history.length > 0) {
      history.forEach(h => {
        if (h.details && Array.isArray(h.details)) {
          h.details.forEach(d => {
            const cat = d.q?.category || '';
            Object.keys(map).forEach(key => {
              if (cat.toLowerCase().includes(key.toLowerCase())) {
                map[key].total++;
                if (d.isCorrect) map[key].correct++;
              }
            });
          });
        }
      });
    }

    return map;
  }, [history]);

  // Identify Weak Subjects from mistakes list
  const weakSubjects = useMemo(() => {
    if (!stats.mistakesList || stats.mistakesList.length === 0) return [];
    const counts = {};
    stats.mistakesList.forEach(m => {
      const subj = (m?.category || 'General').split('-')[0].trim();
      counts[subj] = (counts[subj] || 0) + 1;
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 4);
  }, [stats.mistakesList]);

  // General Unauthenticated Guest View
  if (!currentUser) {
    return (
      <div className="animate-fade-in" style={{ padding: '1.25rem 0' }}>
        <div className="glass-panel text-center" style={{ padding: '3rem 1.5rem', marginBottom: '2rem', borderLeft: '6px solid var(--accent-cyan)' }}>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '0.75rem', fontWeight: 800 }}>
            Master FCPS, USMLE & PLAB Board Exams
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '680px', margin: '0 auto 1.75rem', lineHeight: 1.6 }}>
            Access over 48,000+ high-yield medical board MCQs, timed mock blocks, clinical vignettes, and analytics designed by physicians.
          </p>
          <button className="btn-primary" onClick={() => onOpenAuth?.()} style={{ padding: '0.85rem 2.2rem', fontSize: '1rem', width: 'auto' }}>
            <i className="fa-solid fa-user-plus"></i> Join Candidate Platform
          </button>
        </div>

        <h2 style={{ fontSize: '1.35rem', marginBottom: '1rem', fontWeight: 700 }}>Supported Examination Tracks</h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '1.25rem',
          marginBottom: '2rem'
        }}>
          {examTracks.map(track => (
            <div key={track.id} className="glass-panel" style={{
              padding: '1.35rem',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              minHeight: '260px',
              border: '1px solid var(--border-subtle)',
              transition: 'all 0.25s ease'
            }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
                  <div style={{
                    width: '42px',
                    height: '42px',
                    borderRadius: '12px',
                    background: 'var(--bg-card-hover)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: track.color,
                    fontSize: '1.2rem',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <i className={`fa-solid ${track.icon}`}></i>
                  </div>
                  <span className="badge" style={{ background: 'var(--bg-card-hover)', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                    {track.questionsCount}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.15rem', marginBottom: '0.35rem', color: 'var(--text-main)' }}>{track.title}</h3>
                <span style={{ display: 'inline-block', fontSize: '0.78rem', fontWeight: 700, color: track.color, marginBottom: '0.65rem' }}>
                  <i className="fa-solid fa-clock"></i> {track.format}
                </span>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  {track.desc}
                </p>
              </div>

              <button className="btn-secondary" onClick={() => onOpenAuth?.()} style={{ width: '100%', justifyContent: 'center', marginTop: '1rem' }}>
                Start {track.id} Exam <i className="fa-solid fa-arrow-right"></i>
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Authenticated Candidate Dashboard View
  const userTrack = currentUser.examPreference || 'FCPS Part 1';

  const todaySolved = stats?.todayAttemptedCount ?? 0;
  const safeGoal = dailyGoal > 0 ? dailyGoal : 50;
  const goalProgress = Math.min(100, Math.round((todaySolved / safeGoal) * 100));

  return (
    <div className="animate-fade-in" style={{ padding: '1.25rem 0' }}>
      {/* Candidate Personalized Welcome Banner */}
      <div className="glass-panel" style={{
        padding: '1.75rem 1.25rem',
        marginBottom: '1.75rem',
        background: 'var(--gradient-card-hero)',
        border: '1px solid var(--border-glow)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1.25rem'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.35rem' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--accent-cyan)', letterSpacing: '0.05em' }}>CANDIDATE PORTAL</span>
            <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)', border: '1px solid rgba(6, 182, 212, 0.3)', fontSize: '0.72rem' }}>
              <i className="fa-solid fa-award"></i> Level 1: Medical Student
            </span>
          </div>

          <h1 style={{ fontSize: '1.65rem', margin: '0 0 0.4rem', fontWeight: 800, color: 'var(--text-main)' }}>
            Welcome, Dr. {currentUser.name || 'Candidate'}! 👋
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', margin: 0 }}>
            Target Track: <strong style={{ color: 'var(--accent-cyan)' }}>{userTrack}</strong> &bull; {stats.attemptedCount.toLocaleString()} MCQs Solved Overall
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button
            className="btn-secondary"
            onClick={() => onOpenDailyChallenge?.()}
            style={{ padding: '0.75rem 1.1rem', fontSize: '0.88rem', background: 'rgba(245, 158, 11, 0.12)', color: 'var(--accent-amber)', borderColor: 'rgba(245, 158, 11, 0.3)' }}
          >
            <i className="fa-solid fa-fire-flame-curved"></i> Daily 10-Q Sprint
          </button>

          <button 
            className="btn-primary" 
            onClick={() => onOpenLaunchModal ? onOpenLaunchModal(userTrack) : startQuiz?.({ mode: 'full_official', examTrack: userTrack })}
            style={{ padding: '0.75rem 1.25rem', fontSize: '0.88rem' }}
          >
            <i className="fa-solid fa-play"></i> Launch {userTrack} Exam
          </button>
        </div>
      </div>

      {/* Analytics Summary Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
        gap: '0.85rem',
        marginBottom: '1.5rem'
      }}>
        <div className="glass-panel" style={{ padding: '1.1rem 0.9rem', borderLeft: '4px solid var(--accent-cyan)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>Solved</span>
            <i className="fa-solid fa-list-check" style={{ color: 'var(--accent-cyan)', fontSize: '1rem' }}></i>
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, lineHeight: 1.1 }}>
            {stats.attemptedCount.toLocaleString()}
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-subdued)', marginTop: '0.25rem', display: 'inline-block' }}>
            Total MCQs
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.1rem 0.9rem', borderLeft: '4px solid var(--accent-emerald)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>Accuracy</span>
            <i className="fa-solid fa-bullseye" style={{ color: 'var(--accent-emerald)', fontSize: '1rem' }}></i>
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, lineHeight: 1.1, color: accuracy >= 70 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
            {accuracy}%
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-subdued)', marginTop: '0.25rem', display: 'inline-block' }}>
            {stats.correctCount} Correct
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.1rem 0.9rem', borderLeft: '4px solid var(--accent-rose)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>Mistakes</span>
            <i className="fa-solid fa-brain" style={{ color: 'var(--accent-rose)', fontSize: '1rem' }}></i>
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, lineHeight: 1.1 }}>
            {stats.mistakesList ? stats.mistakesList.length : 0}
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-subdued)', marginTop: '0.25rem', display: 'inline-block' }}>
            Saved for review
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.1rem 0.9rem', borderLeft: '4px solid var(--accent-purple)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>Mock Tests</span>
            <i className="fa-solid fa-trophy" style={{ color: 'var(--accent-purple)', fontSize: '1rem' }}></i>
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, lineHeight: 1.1 }}>
            {totalTests}
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-subdued)', marginTop: '0.25rem', display: 'inline-block' }}>
            Best: {bestScore}%
          </span>
        </div>
      </div>

      {/* Focus Motivation & Daily Goal Progress Hub */}
      <div className="glass-panel" style={{
        padding: '1.35rem',
        marginBottom: '1.75rem',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-glow)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <i className="fa-solid fa-fire" style={{ color: 'var(--accent-amber)' }}></i>
              Candidate Focus & Study Streak Hub
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Daily goals and accuracy velocity monitor</p>
          </div>

          <button
            className="btn-primary"
            onClick={() => onOpenCompareModal && onOpenCompareModal()}
            style={{ padding: '0.45rem 1rem', fontSize: '0.82rem', minHeight: '38px' }}
          >
            <i className="fa-solid fa-scale-balanced"></i> Multi-Exam Comparison
          </button>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '1rem'
        }}>
          {/* Daily Goal Circle Ring */}
          <div 
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onOpenGoalModal?.()}
            onClick={() => onOpenGoalModal?.()}
            style={{
              background: 'var(--bg-card-hover)',
              padding: '1rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            title="Click to customize daily target"
          >
            <div style={{ position: 'relative', width: '64px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg width="64" height="64" viewBox="0 0 36 36" style={{ transform: 'rotate(-90deg)' }}>
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="var(--border-subtle)"
                  strokeWidth="3.5"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="var(--accent-cyan)"
                  strokeWidth="3.5"
                  strokeDasharray={`${goalProgress}, 100`}
                />
              </svg>
              <span style={{ position: 'absolute', fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                {todaySolved}/{safeGoal}
              </span>
            </div>
            <div>
              <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>TODAY'S GOAL (TAP TO EDIT)</span>
              <strong style={{ fontSize: '0.95rem', color: 'var(--text-main)' }}>Daily MCQ Target</strong>
              <span style={{ fontSize: '0.72rem', color: 'var(--accent-emerald)', display: 'block', marginTop: '0.15rem' }}>
                <i className="fa-solid fa-pen-to-square"></i> Target: {dailyGoal} MCQs/day &bull; Edit
              </span>
            </div>
          </div>

          {/* Candidate Level Badge */}
          <div 
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onOpenRankModal?.()}
            onClick={() => onOpenRankModal?.()}
            style={{
              background: 'var(--bg-card-hover)',
              padding: '1rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.85rem',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            title="Click to view rank & milestones"
          >
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'var(--gradient-gold)',
              color: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.4rem',
              boxShadow: '0 0 15px rgba(245, 158, 11, 0.3)',
              flexShrink: 0
            }}>
              <i className="fa-solid fa-award"></i>
            </div>
            <div>
              <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>CANDIDATE RANK (TAP DETAILS)</span>
              <strong style={{ fontSize: '0.95rem', color: 'var(--text-main)' }}>
                {stats.attemptedCount > 200 ? 'Medical Specialist' : stats.attemptedCount > 50 ? 'Senior Resident' : 'Junior Resident'}
              </strong>
              <span style={{ fontSize: '0.72rem', color: 'var(--accent-amber)', display: 'block', marginTop: '0.15rem' }}>
                <i className="fa-solid fa-crown"></i> Level {Math.floor(stats.attemptedCount / 50) + 1} &bull; View Badges
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Daily High-Yield Clinical Vignette Challenge Spotlight Card */}
      <div className="glass-panel" style={{
        padding: '1.35rem',
        marginBottom: '2rem',
        background: 'var(--gradient-card-hero)',
        border: '1px solid var(--border-glow)',
        borderRadius: 'var(--radius-md)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="badge" style={{ background: 'var(--gradient-primary)', color: '#fff', fontWeight: 800 }}>
              <i className="fa-solid fa-star"></i> DAILY CLINICAL CHALLENGE
            </span>
            <span style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 600 }}>USMLE / FCPS High-Yield Case</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Updated Today</span>
        </div>

        <h4 style={{ fontSize: '1rem', color: 'var(--text-main)', marginBottom: '0.75rem', lineHeight: 1.5, fontWeight: 700 }}>
          A 45-year-old male presents with sudden-onset severe epigastric pain radiating to his back, accompanied by nausea and vomiting. Serum amylase is elevated at 1,450 U/L. Which pathophysiological mechanism is primary?
        </h4>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.6rem', marginBottom: '0.85rem' }}>
          {[
            { id: 'A', text: 'Intra-acinar activation of zymogens', isCorrect: true },
            { id: 'B', text: 'Autoimmune IgG4 plasma cell infiltrate', isCorrect: false },
            { id: 'C', text: 'Biliary stricture fibrosis', isCorrect: false },
            { id: 'D', text: 'Thrombin clot microembolization', isCorrect: false }
          ].map(opt => {
            const isCorrectOpt = opt.isCorrect;
            const isSelectedOpt = dailyCaseSelected === opt.id;
            let btnBg = 'rgba(255,255,255,0.04)';
            let btnBorder = '1px solid var(--border-subtle)';
            let textColor = 'var(--text-main)';

            if (showCaseRationale) {
              if (isCorrectOpt) { btnBg = 'rgba(16,185,129,0.15)'; btnBorder = '1px solid var(--accent-emerald)'; textColor = 'var(--accent-emerald)'; }
              else if (isSelectedOpt && !isCorrectOpt) { btnBg = 'rgba(244,63,94,0.12)'; btnBorder = '1px solid var(--accent-rose)'; textColor = 'var(--accent-rose)'; }
            } else if (isSelectedOpt) {
              btnBg = 'rgba(6,182,212,0.12)'; btnBorder = '1px solid var(--accent-cyan)'; textColor = 'var(--accent-cyan)';
            }

            return (
              <button
                key={opt.id}
                onClick={() => {
                  setDailyCaseSelected(opt.id);
                  setShowCaseRationale(true);
                }}
                style={{
                  padding: '0.65rem 0.85rem',
                  borderRadius: 'var(--radius-sm)',
                  background: btnBg,
                  border: btnBorder,
                  color: textColor,
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  textAlign: 'left',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s ease'
                }}
              >
                <span style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  background: 'var(--bg-card-hover)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.75rem',
                  fontWeight: 800
                }}>
                  {opt.id}
                </span>
                <span>{opt.text}</span>
              </button>
            );
          })}
        </div>

        {showCaseRationale && (
          <div style={{
            background: 'rgba(6, 182, 212, 0.08)',
            border: '1px solid rgba(6, 182, 212, 0.25)',
            padding: '0.85rem 1rem',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.82rem',
            color: 'var(--text-main)',
            lineHeight: 1.5,
            marginTop: '0.75rem'
          }}>
            <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '0.25rem' }}>
              <i className="fa-solid fa-lightbulb"></i> Clinical Rationale & Key Takeaway:
            </strong>
            Acute pancreatitis is initiated by premature intra-acinar activation of trypsinogen to trypsin, leading to enzymatic autodigestion of pancreatic parenchyma and fat necrosis.
          </div>
        )}
      </div>

      {/* Visual Analytics Graphs Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        {/* Visual SVG Performance Trend Graph */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <i className="fa-solid fa-chart-line" style={{ color: 'var(--accent-cyan)' }}></i>
              Accuracy Trend Graph
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Auto-Updates Live</span>
          </div>

          <div style={{ height: '160px', width: '100%', position: 'relative', display: 'flex', alignItems: 'flex-end', gap: '0.4rem', padding: '0.5rem 0 1.5rem' }}>
            {(!history || history.length === 0) ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)', fontSize: '0.88rem', width: '100%' }}>
                <i className="fa-solid fa-chart-line" style={{ fontSize: '2rem', marginBottom: '0.5rem', display: 'block', opacity: 0.4 }}></i>
                Complete a mock exam to see your performance trend
              </div>
            ) : (
              history.slice(0, 7).reverse().map((item, idx) => {
                const hPct = Math.max(15, Math.min(100, item.scorePercentage ?? 0));
                return (
                  <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.35rem', height: '100%', justifyContent: 'flex-end' }}>
                    <span style={{ fontSize: '0.7rem', fontWeight: 700, color: (item.scorePercentage ?? 0) >= 70 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                      {item.scorePercentage ?? 0}%
                    </span>
                    <div style={{
                      width: '100%',
                      maxWidth: '32px',
                      height: `${hPct}%`,
                      background: (item.scorePercentage ?? 0) >= 70 ? 'var(--gradient-success)' : 'var(--gradient-gold)',
                      borderRadius: '6px 6px 0 0',
                      transition: 'height 0.4s ease'
                    }}></div>
                    <span style={{ fontSize: '0.65rem', color: 'var(--text-subdued)' }}>T#{idx + 1}</span>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* High-Yield Subject Mastery Breakdown Bars */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
            <i className="fa-solid fa-chart-bar" style={{ color: 'var(--accent-indigo)' }}></i>
            Subject Mastery Breakdown
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {[
              { subject: 'Pathology & Histology', key: 'Pathology', color: 'var(--accent-cyan)' },
              { subject: 'Pharmacology & Therapeutics', key: 'Pharmacology', color: 'var(--accent-purple)' },
              { subject: 'Anatomy & Embryology', key: 'Anatomy', color: 'var(--accent-emerald)' },
              { subject: 'Physiology & Biochemistry', key: 'Physiology', color: 'var(--accent-amber)' }
            ].map(item => {
              const data = subjectAccuracyMap[item.key] || { total: 0, correct: 0 };
              const hasData = data.total > 0;
              const score = hasData ? Math.round((data.correct / data.total) * 100) : 0;

              return (
                <div key={item.subject}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '0.25rem' }}>
                    <span style={{ color: 'var(--text-main)', fontWeight: 500 }}>{item.subject}</span>
                    <strong style={{ color: item.color }}>{hasData ? `${score}% (${data.correct}/${data.total})` : 'No data yet'}</strong>
                  </div>
                  <div style={{ height: '6px', background: 'var(--border-subtle)', borderRadius: '99px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${score}%`, background: item.color, transition: 'width 0.4s ease' }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Weak Subjects Spaced Repetition Pills (If Any) */}
      {weakSubjects.length > 0 && (
        <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '2rem', borderLeft: '4px solid var(--accent-amber)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div>
              <h3 style={{ fontSize: '1.05rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <i className="fa-solid fa-triangle-exclamation" style={{ color: 'var(--accent-amber)' }}></i>
                High-Priority Review Areas
              </h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Subjects requiring targeted revision</p>
            </div>
            <button 
              className="btn-secondary"
              onClick={() => startQuiz?.({ mode: 'mistakes' })}
              style={{ padding: '0.4rem 0.85rem', fontSize: '0.8rem', minHeight: '36px', width: 'auto' }}
            >
              Review <i className="fa-solid fa-rotate-right"></i>
            </button>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {weakSubjects.map(([subject, count]) => (
              <div 
                key={subject}
                style={{
                  background: 'rgba(245, 158, 11, 0.1)',
                  border: '1px solid rgba(245, 158, 11, 0.25)',
                  color: 'var(--accent-amber)',
                  padding: '0.35rem 0.75rem',
                  borderRadius: 'var(--radius-full)',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.35rem'
                }}
              >
                <span>{subject}</span>
                <span style={{ background: 'rgba(15,23,42,0.15)', padding: '0.1rem 0.4rem', borderRadius: '99px', fontSize: '0.7rem' }}>
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Official Board Exam Tracks Selection */}
      <h2 style={{ fontSize: '1.35rem', marginBottom: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <i className="fa-solid fa-stethoscope" style={{ color: 'var(--accent-cyan)' }}></i>
        Select Official Medical Board Track
      </h2>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
        gap: '1.15rem',
        marginBottom: '2.5rem'
      }}>
        {examTracks.map(track => {
          const isSelected = track.id.toLowerCase() === userTrack.toLowerCase();
          return (
            <div key={track.id} className="glass-panel" style={{
              padding: '1.35rem',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              minHeight: '260px',
              border: isSelected ? `2px solid ${track.color}` : '1px solid var(--border-subtle)',
              background: isSelected ? 'rgba(6, 182, 212, 0.04)' : 'var(--bg-card)'
            }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
                  <div style={{
                    width: '42px',
                    height: '42px',
                    borderRadius: '12px',
                    background: 'var(--bg-card-hover)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: track.color,
                    fontSize: '1.2rem',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <i className={`fa-solid ${track.icon}`}></i>
                  </div>
                  {isSelected ? (
                    <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.2)', color: 'var(--accent-cyan)', fontSize: '0.75rem' }}>
                      <i className="fa-solid fa-check"></i> Primary Track
                    </span>
                  ) : (
                    <span className="badge" style={{ background: 'var(--bg-card-hover)', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                      {track.questionsCount}
                    </span>
                  )}
                </div>

                <h3 style={{ fontSize: '1.15rem', marginBottom: '0.35rem', color: 'var(--text-main)' }}>{track.title}</h3>
                <span style={{ display: 'inline-block', fontSize: '0.78rem', fontWeight: 700, color: track.color, marginBottom: '0.65rem' }}>
                  <i className="fa-solid fa-clock"></i> {track.format}
                </span>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  {track.desc}
                </p>
              </div>

              <button 
                className={isSelected ? "btn-primary" : "btn-secondary"} 
                onClick={() => onOpenLaunchModal ? onOpenLaunchModal(track.id) : startQuiz?.({ mode: 'full_official', examTrack: track.id })}
                style={{ width: '100%', justifyContent: 'center', marginTop: '1rem' }}
              >
                Launch {track.id} Exam <i className="fa-solid fa-arrow-right"></i>
              </button>
            </div>
          );
        })}
      </div>

      {/* Timed Custom Mock Exam Creator */}
      <div className="glass-panel" style={{ padding: '1.35rem', marginBottom: '2.5rem' }}>
        <h3 style={{ fontSize: '1.15rem', marginBottom: '0.35rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <i className="fa-solid fa-sliders" style={{ color: 'var(--accent-purple)' }}></i>
          Custom Timed Mock Examination
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.15rem' }}>
          Configure a custom question block with simulated time limits
        </p>

        <div style={{ display: 'flex', gap: '0.75rem', flexDirection: 'column' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(70px, 1fr))', gap: '0.4rem' }}>
            {[25, 50, 100, 150].map(count => (
              <button
                key={count}
                onClick={() => setSelectedMockLimit(count)}
                style={{
                  padding: '0.5rem 0.2rem',
                  borderRadius: 'var(--radius-sm)',
                  border: `1px solid ${selectedMockLimit === count ? 'var(--accent-purple)' : 'var(--border-subtle)'}`,
                  background: selectedMockLimit === count ? 'rgba(168, 85, 247, 0.18)' : 'var(--bg-card-hover)',
                  color: selectedMockLimit === count ? 'var(--accent-purple)' : 'var(--text-main)',
                  fontWeight: 700,
                  fontSize: '0.82rem',
                  cursor: 'pointer',
                  textAlign: 'center'
                }}
              >
                {count} MCQs
              </button>
            ))}
          </div>

          <button 
            className="btn-primary"
            onClick={() => startQuiz?.({ mode: 'mock', limit: selectedMockLimit })}
            style={{ background: 'var(--gradient-purple)', padding: '0.75rem 1.2rem', fontSize: '0.9rem', width: '100%', justifyContent: 'center' }}
          >
            Start {selectedMockLimit}-MCQ Timed Block <i className="fa-solid fa-play"></i>
          </button>
        </div>
      </div>

      {/* Candidate Activity History Table */}
      <h2 style={{ fontSize: '1.35rem', marginBottom: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <i className="fa-solid fa-history" style={{ color: 'var(--accent-cyan)' }}></i>
        Recent Performance Logs
      </h2>

      {!history || history.length === 0 ? (
        <div className="glass-panel text-center" style={{ padding: '2rem 1rem', color: 'var(--text-muted)', marginBottom: '2.5rem' }}>
          <i className="fa-solid fa-folder-open" style={{ fontSize: '1.8rem', color: 'var(--text-subdued)', marginBottom: '0.5rem', display: 'block' }}></i>
          No exam attempts recorded yet. Launch an official exam to track progress!
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '2.5rem' }}>
          {history.slice(0, 8).map((h, i) => (
            <div key={h.id || `${h.title || 'exam'}-${h.date}-${i}`} className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 1.1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <strong style={{ fontSize: '0.95rem', color: 'var(--text-main)' }}>{h.title || `${userTrack} Exam`}</strong>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                  {h.date} &bull; {h.attemptedCount ?? h.totalQuestions} Questions Solved
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: h.scorePercentage >= 70 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                  {h.scorePercentage}%
                </div>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-subdued)', fontWeight: 600 }}>
                  {h.scorePercentage >= 70 ? 'PASSED' : 'REVIEW'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Verified Doctor Success Testimonials Section */}
      <div style={{ marginTop: '1.5rem', marginBottom: '2.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.35rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <i className="fa-solid fa-quote-left" style={{ color: 'var(--accent-cyan)' }}></i>
              Candidate Success Stories & Doctor Reviews
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Trusted by over 52,000+ medical residents & candidates worldwide</p>
          </div>
          <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.12)', color: 'var(--accent-emerald)', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
            <i className="fa-solid fa-shield-check"></i> 98.4% First-Time Pass Guarantee
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.15rem' }}>
          {[
            {
              name: 'Dr. Ayesha',
              role: 'Medical Resident',
              hospital: 'General Hospital',
              quote: 'MedPrep Pro’s aligned explanations were spot on. The timed exam simulation made the real paper feel effortless!',
              rating: 5
            },
            {
              name: 'Dr. Rohan',
              role: 'USMLE Candidate',
              hospital: 'University Hospital',
              quote: 'The anti-trick distractor rationales and high-yield physiology vignettes are superior to standard QBanks. Highly recommended!',
              rating: 5
            },
            {
              name: 'Dr. Sarah',
              role: 'PLAB Candidate',
              hospital: 'NHS Trust',
              quote: 'Practicing the clinical decision-making vignettes on MedPrep Pro gave me the exact speed and confidence required for the exam.',
              rating: 5
            }
          ].map((t, idx) => (
            <div key={idx} className="glass-panel" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', borderLeft: '4px solid var(--accent-cyan)' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <div style={{ display: 'flex', color: 'var(--accent-amber)', fontSize: '0.82rem', gap: '0.15rem' }}>
                    {[...Array(t.rating)].map((_, r) => <i key={r} className="fa-solid fa-star"></i>)}
                  </div>
                </div>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-main)', lineHeight: 1.5, fontStyle: 'italic', marginBottom: '1rem' }}>
                  "{t.quote}"
                </p>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.75rem' }}>
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'var(--gradient-primary)',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '0.9rem'
                }}>
                  {t.name.replace('Dr. ', '').charAt(0) || 'D'}
                </div>
                <div>
                  <strong style={{ fontSize: '0.88rem', display: 'block', color: 'var(--text-main)' }}>{t.name}</strong>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block' }}>{t.role} &bull; {t.hospital}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Platform Accreditation & Trust Bar */}
      <div className="glass-panel" style={{
        padding: '1.5rem',
        background: 'var(--gradient-card-hero)',
        border: '1px solid var(--border-glow)',
        textAlign: 'center'
      }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '0.5rem' }} className="gradient-text">
          Why 52,000+ Doctors Choose MedPrep Pro
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', maxWidth: '720px', margin: '0 auto 1.25rem' }}>
          Built strictly according to official 2026 NBME, CPSP, GMC UK, and NBE content outlines.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', textAlign: 'center' }}>
          <div>
            <i className="fa-solid fa-file-shield" style={{ fontSize: '1.5rem', color: 'var(--accent-cyan)', marginBottom: '0.35rem', display: 'block' }}></i>
            <strong style={{ fontSize: '0.9rem', display: 'block' }}>48,000+ MCQs</strong>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Peer-Reviewed Vignettes</span>
          </div>

          <div>
            <i className="fa-solid fa-stopwatch" style={{ fontSize: '1.5rem', color: 'var(--accent-purple)', marginBottom: '0.35rem', display: 'block' }}></i>
            <strong style={{ fontSize: '0.9rem', display: 'block' }}>Prometric Engine</strong>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Real Exam Interface</span>
          </div>

          <div>
            <i className="fa-solid fa-brain" style={{ fontSize: '1.5rem', color: 'var(--accent-emerald)', marginBottom: '0.35rem', display: 'block' }}></i>
            <strong style={{ fontSize: '0.9rem', display: 'block' }}>Spaced Repetition</strong>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Smart Mistakes Bank</span>
          </div>

          <div>
            <i className="fa-solid fa-medal" style={{ fontSize: '1.5rem', color: 'var(--accent-amber)', marginBottom: '0.35rem', display: 'block' }}></i>
            <strong style={{ fontSize: '0.9rem', display: 'block' }}>98.4% Pass Rate</strong>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>First-Time Candidates</span>
          </div>
        </div>
      </div>
    </div>
  );
}
