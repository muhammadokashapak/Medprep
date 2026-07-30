import React, { useState } from 'react';
import { getQuestionsForTrack } from '../utils/security';

const ALL_EXAM_TRACKS = [
  { id: 'FCPS Part 1', title: 'FCPS Part 1 (Pakistan)', icon: 'fa-user-doctor', targetQs: 1500, passRate: 70 },
  { id: 'USMLE Step 1', title: 'USMLE Step 1 (USA)', icon: 'fa-microscope', targetQs: 2000, passRate: 75 },
  { id: 'USMLE Step 2 CK', title: 'USMLE Step 2 CK (USA)', icon: 'fa-hospital-user', targetQs: 1800, passRate: 75 },
  { id: 'PLAB / UKMLA', title: 'PLAB 1 / UKMLA (UK)', icon: 'fa-notes-medical', targetQs: 1200, passRate: 68 },
  { id: 'NEET PG', title: 'NEET PG / INI-CET (India)', icon: 'fa-book-medical', targetQs: 1500, passRate: 72 },
  { id: 'MRCS Surgery', title: 'MRCS Part A (UK/Intl)', icon: 'fa-scalpel', targetQs: 1000, passRate: 70 }
];

export default function ExamComparisonModal({ isOpen, onClose, history = [], currentUser, questions = [] }) {
  const [selectedTrackFilter, setSelectedTrackFilter] = useState('all');

  if (!isOpen) return null;

  // Calculate statistics for each exam track based on candidate exam history
  const trackAnalytics = ALL_EXAM_TRACKS.map(track => {
    const questionsForTrack = getQuestionsForTrack(questions, track.id);
    const totalAvailable = questionsForTrack.length;

    // Filter history entries matching this track
    const trackHistory = history.filter(h => 
      h.examTrack === track.id ||
      (h.title && h.title.toLowerCase().includes(track.id.toLowerCase()))
    );

    let totalAttempted = 0;
    let totalCorrect = 0;

    trackHistory.forEach(h => {
      totalAttempted += (h.attemptedCount || 0);
      totalCorrect += (h.correctCount || 0);
    });

    const accuracy = totalAttempted > 0 ? Math.round((totalCorrect / totalAttempted) * 100) : 0;
    const completionRate = totalAvailable > 0 ? Math.min(100, Math.round((totalAttempted / totalAvailable) * 100)) : 0;
    
    // Readiness Score algorithm: Weighted combination of Accuracy (70%) and Completion Rate (30%)
    const readinessScore = totalAttempted >= 20 
      ? Math.min(100, Math.round((accuracy * 0.7) + (completionRate * 0.3)))
      : 0;

    let readinessStatus = 'Not Started';
    let statusColor = 'var(--text-muted)';
    if (readinessScore >= 80) {
      readinessStatus = 'Exam Ready';
      statusColor = 'var(--accent-emerald)';
    } else if (readinessScore >= 50) {
      readinessStatus = 'Moderate Prep';
      statusColor = 'var(--accent-cyan)';
    } else if (readinessScore > 0) {
      readinessStatus = 'Early Stage';
      statusColor = 'var(--accent-amber)';
    }

    return {
      ...track,
      totalAvailable,
      totalAttempted,
      totalCorrect,
      accuracy,
      completionRate,
      readinessScore,
      readinessStatus,
      statusColor,
      examsTaken: trackHistory.length
    };
  });

  const filteredTracks = selectedTrackFilter === 'all'
    ? trackAnalytics
    : trackAnalytics.filter(t => t.id === currentUser?.examPreference);

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
        maxWidth: '920px',
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

        {/* Header */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '12px',
              background: 'var(--gradient-primary)',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.3rem'
            }}>
              <i className="fa-solid fa-scale-balanced"></i>
            </div>
            <div>
              <h2 style={{ fontSize: '1.4rem' }} className="gradient-text">
                Multi-Exam Track Comparison & Readiness Hub
              </h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Compare your accuracy, completion rate, and pass probability across international medical board exams.
              </p>
            </div>
          </div>
        </div>

        {/* Track Filter Switcher */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
          <button
            className={selectedTrackFilter === 'all' ? 'btn-primary' : 'btn-secondary'}
            onClick={() => setSelectedTrackFilter('all')}
            style={{ padding: '0.4rem 0.9rem', fontSize: '0.82rem', minHeight: '36px' }}
          >
            <i className="fa-solid fa-layer-group"></i> All Medical Boards ({ALL_EXAM_TRACKS.length})
          </button>

          {currentUser?.examPreference && (
            <button
              className={selectedTrackFilter !== 'all' ? 'btn-primary' : 'btn-secondary'}
              onClick={() => setSelectedTrackFilter('current')}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.82rem', minHeight: '36px' }}
            >
              <i className="fa-solid fa-user-doctor"></i> My Primary Exam ({currentUser.examPreference})
            </button>
          )}
        </div>

        {/* Comparative Overview Grid Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '1rem',
          marginBottom: '1.5rem'
        }}>
          {filteredTracks.map(t => (
            <div
              key={t.id}
              className="glass-panel"
              style={{
                padding: '1.15rem',
                borderLeft: `4px solid ${t.statusColor}`,
                background: t.id === currentUser?.examPreference ? 'rgba(6, 182, 212, 0.06)' : 'var(--bg-card)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <i className={`fa-solid ${t.icon}`} style={{ color: 'var(--accent-cyan)', fontSize: '1.1rem' }}></i>
                  <strong style={{ fontSize: '0.95rem' }}>{t.id}</strong>
                </div>
                <span className="badge" style={{
                  fontSize: '0.7rem',
                  background: `${t.statusColor}20`,
                  color: t.statusColor,
                  borderColor: `${t.statusColor}40`
                }}>
                  {t.readinessStatus}
                </span>
              </div>

              {/* Readiness Progress Bar */}
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>
                  <span>Board Readiness Score</span>
                  <strong style={{ color: t.statusColor }}>{t.readinessScore}%</strong>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '99px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${t.readinessScore}%`,
                    background: t.statusColor,
                    transition: 'width 0.4s ease'
                  }}></div>
                </div>
              </div>

              {/* Stats Breakdown */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.8rem' }}>
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.5rem 0.65rem', borderRadius: 'var(--radius-sm)' }}>
                  <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)' }}>ACCURACY</span>
                  <strong style={{ color: t.accuracy >= t.passRate ? 'var(--accent-emerald)' : 'var(--text-main)', fontSize: '0.95rem' }}>
                    {t.accuracy}%
                  </strong>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-subdued)', display: 'block' }}>Target: {t.passRate}%</span>
                </div>

                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.5rem 0.65rem', borderRadius: 'var(--radius-sm)' }}>
                  <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)' }}>QBANK COVERAGE</span>
                  <strong style={{ fontSize: '0.95rem' }}>
                    {t.totalAttempted} <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>/ {t.totalAvailable}</span>
                  </strong>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-subdued)', display: 'block' }}>{t.completionRate}% Done</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Detailed Side-by-Side Comparison Table */}
        <div style={{ overflowX: 'auto', marginBottom: '1rem' }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            fontSize: '0.85rem',
            textAlign: 'left'
          }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                <th style={{ padding: '0.75rem' }}>EXAM BOARD</th>
                <th style={{ padding: '0.75rem' }}>ACCURACY</th>
                <th style={{ padding: '0.75rem' }}>ATTEMPTED</th>
                <th style={{ padding: '0.75rem' }}>PASS TARGET</th>
                <th style={{ padding: '0.75rem' }}>READINESS</th>
                <th style={{ padding: '0.75rem', textAlign: 'right' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {filteredTracks.map(t => (
                <tr key={t.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                  <td style={{ padding: '0.75rem', fontWeight: 600 }}>
                    <i className={`fa-solid ${t.icon}`} style={{ marginRight: '0.4rem', color: 'var(--accent-cyan)' }}></i>
                    {t.id}
                  </td>
                  <td style={{ padding: '0.75rem', fontWeight: 700, color: t.accuracy >= t.passRate ? 'var(--accent-emerald)' : 'var(--text-main)' }}>
                    {t.accuracy}%
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    {t.totalAttempted} / {t.totalAvailable}
                  </td>
                  <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>
                    {t.passRate}%
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <div style={{ width: '100px', height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '99px', overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${t.readinessScore}%`, background: t.statusColor }}></div>
                    </div>
                  </td>
                  <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                    <span style={{ color: t.statusColor, fontWeight: 700, fontSize: '0.8rem' }}>
                      {t.readinessStatus}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <button className="btn-primary" onClick={onClose} style={{ padding: '0.75rem 2rem' }}>
            <i className="fa-solid fa-check"></i> Return to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
