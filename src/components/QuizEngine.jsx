import React, { useState, useEffect, useRef, useCallback } from 'react';
import confetti from 'canvas-confetti';

export default function QuizEngine({ quizList, onAnswer, onRecordResult, onFinish, config, addToast }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const userAnswersRef = useRef(userAnswers);
  userAnswersRef.current = userAnswers;

  const [markedForReview, setMarkedForReview] = useState({});
  const examStartRef = useRef(Date.now());
  const endTimeRef = useRef(null);
  const [timerSeconds, setTimerSeconds] = useState(() => {
    const timeLimit = config?.timeLimitMinutes ?? null;
    if (timeLimit !== null && !isNaN(timeLimit)) {
      return timeLimit * 60;
    }
    return null;
  });

  const [showPalette, setShowPalette] = useState(false);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [examResult, setExamResult] = useState(null);
  const [startTime] = useState(Date.now());
  const [reviewFilter, setReviewFilter] = useState('attempted'); // 'attempted' | 'incorrect' | 'correct' | 'all'
  const [strikedOptions, setStrikedOptions] = useState({}); // { [qKey]: { A: true } }
  const [isFlashcardMode, setIsFlashcardMode] = useState(false); // Mode switch: Standard vs 3D Flashcard MCQ
  const [isMcqCardFlipped, setIsMcqCardFlipped] = useState(false);

  const safeList = Array.isArray(quizList) ? quizList : [];

  if (safeList.length === 0 && !isCompleted) {
    return (
      <div className="animate-fade-in" style={{ padding: '2rem', textAlign: 'center' }}>
        <div className="glass-panel" style={{ padding: '2.5rem' }}>
          <i className="fa-solid fa-circle-xmark" style={{ fontSize: '3rem', color: 'var(--accent-rose)', marginBottom: '1rem', display: 'block' }}></i>
          <h3>No Questions Found</h3>
          <p style={{ color: 'var(--text-muted)', margin: '0.5rem 0 1.5rem' }}>No questions available for this exam track.</p>
          <button className="btn-primary" onClick={onFinish}>Return to Dashboard</button>
        </div>
      </div>
    );
  }

  const currentQ = safeList[currentIndex];
  const qKey = currentQ ? (currentQ.id ?? `q_${currentIndex}`) : null;

  const toggleStrikeOption = (optKey) => {
    if (!qKey) return;
    setStrikedOptions(prev => {
      const qStriked = prev[qKey] || {};
      return {
        ...prev,
        [qKey]: {
          ...qStriked,
          [optKey]: !qStriked[optKey]
        }
      };
    });
  };

  const handleFinalSubmit = useCallback((auto = false) => {
    setShowSubmitModal(false);
    setIsCompleted(true);

    const totalQ = safeList.length;
    let correctCount = 0;
    let attemptedCount = 0;
    const currentAnswersMap = userAnswersRef.current;

    const subjectStats = {};

    const details = safeList.map((q, idx) => {
      const iterQKey = q.id ?? `q_${idx}`;
      const ans = currentAnswersMap[iterQKey];
      const selected = ans?.selected ?? null;
      const isCorrect = selected && q.correct_answer 
        ? selected.toUpperCase() === String(q.correct_answer).toUpperCase()
        : false;

      const rawSubj = (q.category || 'General').split('-')[0].trim();

      if (!subjectStats[rawSubj]) {
        subjectStats[rawSubj] = { total: 0, attempted: 0, correct: 0 };
      }
      subjectStats[rawSubj].total++;

      if (selected !== null && selected !== undefined) {
        attemptedCount++;
        subjectStats[rawSubj].attempted++;
        if (isCorrect) {
          correctCount++;
          subjectStats[rawSubj].correct++;
        }
      }

      return {
        q,
        index: idx + 1,
        selected: selected ?? 'Unattempted',
        isCorrect,
        wasAttempted: !!selected,
        correctAnswer: q.correct_answer,
        explanation: q.explanation
      };
    });

    const scorePercentage = totalQ > 0 ? Math.round((correctCount / totalQ) * 100) : 0;
    const accuracyPercentage = attemptedCount > 0 ? Math.round((correctCount / attemptedCount) * 100) : 0;

    const elapsedMs = Date.now() - startTime;
    const elapsedMins = Math.floor(elapsedMs / 60000);
    const elapsedSecs = Math.floor((elapsedMs % 60000) / 1000);
    const timeTakenStr = `${elapsedMins}m ${elapsedSecs}s`;

    const resultObj = {
      title: config?.title || (config?.isMock ? 'Official Board Examination' : 'Practice Exam'),
      examTrack: config?.examTrack || 'FCPS Part 1',
      totalQuestions: totalQ,
      attemptedCount,
      skippedCount: totalQ - attemptedCount,
      correctCount,
      scorePercentage,
      accuracyPercentage,
      timeTaken: timeTakenStr,
      subjectStats,
      details,
      date: new Date().toLocaleDateString()
    };

    setExamResult(resultObj);
    if (onRecordResult) {
      onRecordResult(resultObj);
    }

    if (auto) {
      addToast?.('Time expired! Exam auto-submitted.', 'warning');
    } else if (scorePercentage >= 60 && attemptedCount > 0) {
      confetti({ particleCount: 140, spread: 90, origin: { y: 0.5 } });
      addToast?.(`PASSED! Score: ${scorePercentage}% (${correctCount}/${totalQ})`, 'success');
    } else {
      addToast?.(`Exam Submitted. Score: ${scorePercentage}% (${correctCount}/${totalQ})`, 'warning');
    }
  }, [safeList, startTime, config, onRecordResult, addToast]);

  useEffect(() => {
    if (timerSeconds === null || isCompleted) return;
    endTimeRef.current = Date.now() + timerSeconds * 1000;
    const interval = setInterval(() => {
      const remaining = Math.max(0, Math.ceil((endTimeRef.current - Date.now()) / 1000));
      setTimerSeconds(remaining);
      if (remaining <= 0) {
        clearInterval(interval);
      }
    }, 500);
    return () => clearInterval(interval);
  }, []); // only run once on mount

  useEffect(() => {
    if (timerSeconds === 0 && !isCompleted) {
      handleFinalSubmit(true);
    }
  }, [timerSeconds, isCompleted, handleFinalSubmit]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setIsMcqCardFlipped(false);
  }, [currentIndex]);

  if (!currentQ && !isCompleted) {
    return (
      <div className="glass-panel text-center" style={{ padding: '2rem 1.25rem', margin: '2rem auto', maxWidth: '600px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>No questions found for the selected criteria.</h2>
        <button className="btn-primary" onClick={() => onFinish && onFinish({})}>
          <i className="fa-solid fa-arrow-left"></i> Return to Candidate Hub
        </button>
      </div>
    );
  }

  const formatTimer = (seconds) => {
    if (seconds === null) return null;
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // COMPLETED EXAM PERFORMANCE SUMMARY VIEW
  if (isCompleted && examResult) {
    const isPass = examResult.scorePercentage >= 60;

    const filteredDetails = examResult.details.filter(d => {
      if (reviewFilter === 'attempted') return d.wasAttempted;
      if (reviewFilter === 'incorrect') return d.wasAttempted && !d.isCorrect;
      if (reviewFilter === 'correct') return d.wasAttempted && d.isCorrect;
      return true; // 'all'
    });

    const getOptionText = (q, key) => {
      if (!key || key === 'Unattempted') return 'Not Answered';
      const optKey = `option_${key.toLowerCase()}`;
      return q[optKey] ? `${key}: ${q[optKey]}` : key;
    };

    const subjectEntries = Object.entries(examResult.subjectStats || {});

    return (
      <div className="animate-fade-in" style={{ padding: '1.5rem 0', maxWidth: '980px', margin: '0 auto' }}>
        {/* Results Overview Hero Header */}
        <div className={`results-hero-panel ${isPass ? 'pass' : 'fail'} text-center`}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            padding: '0.35rem 1.1rem',
            borderRadius: '99px',
            fontSize: '0.82rem',
            fontWeight: 800,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '1rem',
            background: isPass ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)',
            color: isPass ? 'var(--accent-emerald)' : 'var(--accent-rose)',
            border: `1px solid ${isPass ? 'rgba(16, 185, 129, 0.4)' : 'rgba(244, 63, 94, 0.4)'}`
          }}>
            <i className={`fa-solid ${isPass ? 'fa-circle-check' : 'fa-triangle-exclamation'}`}></i>
            {isPass ? 'OFFICIAL PASS • GRADE A' : 'UNMET THRESHOLD • REVISION REQUIRED'}
          </div>

          <h1 style={{ fontSize: '1.9rem', marginBottom: '0.35rem', fontWeight: 800, color: 'var(--text-main)' }}>
            {examResult.title}
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', marginBottom: '2rem' }}>
            Board Standard Performance Scorecard &bull; Cutoff Threshold: 60%
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
            <div className="results-metric-card">
              <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>FINAL SCORE</span>
              <span style={{ fontSize: '2.2rem', fontWeight: 800, color: isPass ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                {examResult.scorePercentage}%
              </span>
            </div>

            <div className="results-metric-card">
              <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>ATTEMPTED</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                {examResult.attemptedCount} <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/ {examResult.totalQuestions}</span>
              </span>
            </div>

            <div className="results-metric-card">
              <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>ACCURACY</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
                {examResult.accuracyPercentage}%
              </span>
            </div>

            <div className="results-metric-card">
              <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase' }}>TIME ELAPSED</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-purple)' }}>
                {examResult.timeTaken}
              </span>
            </div>
          </div>

          <button className="btn-primary" onClick={() => onFinish && onFinish(examResult)} style={{ padding: '0.8rem 2.5rem', fontSize: '0.95rem' }}>
            <i className="fa-solid fa-house"></i> Return to Candidate Hub
          </button>
        </div>

        {/* Subject-Wise Performance Breakdown */}
        {subjectEntries.length > 0 && (
          <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.75rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <i className="fa-solid fa-chart-pie" style={{ color: 'var(--accent-cyan)' }}></i> Subject Performance Breakdown
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {subjectEntries.map(([subj, data]) => {
                const pct = data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0;
                const isSubjPass = pct >= 60;
                return (
                  <div key={subj} style={{ background: 'rgba(255,255,255,0.02)', padding: '0.85rem 1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                      <span>{subj}</span>
                      <span style={{ color: isSubjPass ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                        {pct}% ({data.correct}/{data.total})
                      </span>
                    </div>
                    <div style={{ height: '6px', background: 'rgba(255,255,255,0.06)', borderRadius: '99px', overflow: 'hidden' }}>
                      <div style={{
                        height: '100%',
                        width: `${pct}%`,
                        background: isSubjPass ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                        transition: 'width 0.4s ease'
                      }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filtered Question Review Section */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0 }}>
            <i className="fa-solid fa-clipboard-check" style={{ color: 'var(--accent-cyan)', marginRight: '0.4rem' }}></i>
            Attempted Questions Review ({filteredDetails.length})
          </h3>

          {/* Filter Pills */}
          <div style={{ display: 'flex', gap: '0.4rem', background: 'rgba(0,0,0,0.2)', padding: '0.3rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            {[
              { id: 'attempted', label: 'Attempted Only' },
              { id: 'incorrect', label: 'Incorrect' },
              { id: 'correct', label: 'Correct' },
              { id: 'all', label: 'All Questions' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setReviewFilter(tab.id)}
                style={{
                  padding: '0.35rem 0.75rem',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  borderRadius: '4px',
                  border: 'none',
                  cursor: 'pointer',
                  background: reviewFilter === tab.id ? 'var(--accent-cyan)' : 'transparent',
                  color: reviewFilter === tab.id ? '#fff' : 'var(--text-muted)',
                  transition: 'all 0.2s'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredDetails.length === 0 && (
            <div className="glass-panel text-center" style={{ padding: '2.5rem', marginTop: '0.5rem' }}>
              <i className="fa-solid fa-clipboard-question" style={{ fontSize: '2.5rem', color: 'var(--accent-cyan)', marginBottom: '0.75rem' }}></i>
              <h4 style={{ color: 'var(--text-main)', margin: '0 0 0.25rem' }}>No Questions to Display</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', margin: 0 }}>
                {reviewFilter === 'attempted' ? 'No questions were attempted during this exam block.' : 'No questions match the selected filter.'}
              </p>
            </div>
          )}
          {filteredDetails.map((det) => (
            <div
              key={det.q.id ?? `review_q_${det.index}`}
              className="glass-panel"
              style={{
                padding: '1.5rem',
                borderLeft: `4px solid ${det.isCorrect ? 'var(--accent-emerald)' : (det.wasAttempted ? 'var(--accent-rose)' : 'var(--text-muted)')}`
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.4rem' }}>
                <span style={{ fontWeight: 800, fontSize: '0.85rem', color: 'var(--accent-cyan)' }}>
                  Question #{det.index}
                </span>
                <span className="badge" style={{
                  padding: '0.25rem 0.65rem',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  background: det.isCorrect 
                    ? 'rgba(16, 185, 129, 0.15)' 
                    : (det.wasAttempted ? 'rgba(244, 63, 94, 0.15)' : 'rgba(255,255,255,0.08)'),
                  color: det.isCorrect 
                    ? 'var(--accent-emerald)' 
                    : (det.wasAttempted ? 'var(--accent-rose)' : 'var(--text-muted)'),
                  border: `1px solid ${det.isCorrect ? 'rgba(16, 185, 129, 0.3)' : (det.wasAttempted ? 'rgba(244, 63, 94, 0.3)' : 'var(--border-subtle)')}`
                }}>
                  {det.isCorrect ? '✓ CORRECT' : (det.wasAttempted ? '✗ INCORRECT' : 'UNATTEMPTED')}
                </span>
              </div>

              <h4 style={{ fontSize: '0.98rem', fontWeight: 500, lineHeight: 1.6, marginBottom: '1.25rem', color: 'var(--text-main)' }}>
                {det.q.question}
              </h4>

              <div className="choice-pill-container">
                <div className={`choice-pill ${det.isCorrect ? 'correct' : 'incorrect'}`}>
                  <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase', marginBottom: '0.2rem' }}>YOUR SELECTION</span>
                  <strong style={{ fontSize: '0.92rem', color: det.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                    {getOptionText(det.q, det.selected)}
                  </strong>
                </div>

                <div className="choice-pill correct">
                  <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 800, textTransform: 'uppercase', marginBottom: '0.2rem' }}>CORRECT ANSWER</span>
                  <strong style={{ fontSize: '0.92rem', color: 'var(--accent-emerald)' }}>
                    {getOptionText(det.q, det.correctAnswer)}
                  </strong>
                </div>
              </div>

              {det.explanation && (
                <div className="clinical-rationale-box">
                  <strong style={{ color: 'var(--accent-cyan)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem', fontSize: '0.88rem' }}>
                    <i className="fa-solid fa-lightbulb"></i> Clinical Rationale & Explanation:
                  </strong>
                  {det.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ACTIVE EXAM ENGINE VIEW
  const options = currentQ ? [
    { key: 'A', text: currentQ.option_a },
    { key: 'B', text: currentQ.option_b },
    { key: 'C', text: currentQ.option_c },
    { key: 'D', text: currentQ.option_d },
    { key: 'E', text: currentQ.option_e }
  ].filter(o => String(o.text ?? '').trim() !== '') : [];

  const currentAnswer = currentQ ? userAnswers[qKey] : null;
  const isMarked = currentQ ? markedForReview[qKey] : false;

  const answeredCount = Object.keys(userAnswers).length;
  const markedCount = Object.keys(markedForReview).filter(k => markedForReview[k]).length;
  const unansweredCount = safeList.length - answeredCount;

  const handleSelectOption = (key) => {
    if (isCompleted || !currentQ) return;
    const isCorrect = currentQ.correct_answer 
      ? key.toUpperCase() === String(currentQ.correct_answer).toUpperCase()
      : false;
    
    const updatedAnswers = {
      ...userAnswers,
      [qKey]: { selected: key, isCorrect }
    };
    setUserAnswers(updatedAnswers);
    if (typeof onAnswer === 'function') {
      onAnswer(currentQ, key, isCorrect);
    }
  };

  const toggleMarkForReview = () => {
    if (!currentQ) return;
    setMarkedForReview(prev => {
      const next = { ...prev, [qKey]: !prev[qKey] };
      if (!prev[qKey]) addToast?.(`Question #${currentIndex + 1} marked for review`, 'info');
      return next;
    });
  };

  return (
    <div className="exam-engine-container animate-fade-in">
      {/* Top Header - Clean & Focused */}
      <header className="exam-header">
        <div className="exam-header-left">
          <div className="exam-q-info">
            <span className="exam-q-number">Question {currentIndex + 1} of {safeList.length}</span>
          </div>
        </div>

        <div className="exam-header-center">
          {timerSeconds !== null && (
            <div className={`exam-timer ${timerSeconds < 300 ? 'timer-danger' : ''}`}>
              <i className="fa-regular fa-clock"></i>
              <span>{formatTimer(timerSeconds)}</span>
            </div>
          )}
        </div>

        <div className="exam-header-right">
          <button
            className="exam-btn-icon btn-danger-outline"
            onClick={() => setShowSubmitModal(true)}
            title="End Exam"
          >
            <i className="fa-solid fa-power-off"></i>
            <span className="desktop-only">End Block</span>
          </button>
        </div>
      </header>

      <div className="exam-progress-bar">
        <div 
          className="exam-progress-fill" 
          style={{ width: `${((currentIndex + 1) / safeList.length) * 100}%` }}
        ></div>
      </div>

      <div className="exam-main-content">
        {/* Main Vignette and Options */}
        <div className="exam-vignette-area">
          <div className="question-stem-container">
            <p className="question-stem-text">
              {currentQ.question}
            </p>
          </div>

          <div className="options-container">
            {options.map((opt) => {
              const isSelected = currentAnswer?.selected === opt.key;
              const isStriked = !!(strikedOptions[qKey]?.[opt.key]);

              return (
                <div
                  key={opt.key}
                  className={`exam-option-card ${isSelected ? 'selected' : ''} ${isStriked ? 'striked' : ''}`}
                  onClick={() => handleSelectOption(opt.key)}
                  onContextMenu={(e) => {
                    e.preventDefault();
                    toggleStrikeOption(opt.key);
                  }}
                  role="button"
                  tabIndex={0}
                  aria-selected={isSelected}
                  onKeyDown={e => (e.key === 'Enter' || e.key === ' ') && handleSelectOption(opt.key)}
                >
                  <div className="exam-option-letter">{opt.key}</div>
                  <div className="exam-option-text">{opt.text}</div>

                  {/* Strike-Through Action Button */}
                  <button
                    type="button"
                    className={`strike-btn ${isStriked ? 'active' : ''}`}
                    title={isStriked ? "Restore Option" : "Eliminate Option (Right Click)"}
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleStrikeOption(opt.key);
                    }}
                  >
                    <i className="fa-solid fa-strikethrough"></i>
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Unified Bottom Navigation Footer */}
      <footer className="exam-footer">
        <div className="footer-left">
          <button
            className="exam-nav-btn"
            onClick={() => setCurrentIndex(p => Math.max(0, p - 1))}
            disabled={currentIndex === 0}
          >
            <i className="fa-solid fa-chevron-left"></i> <span className="desktop-only">Previous</span>
          </button>
        </div>

        <div className="footer-center">
          <button
            className={`exam-nav-btn mark-btn ${isMarked ? 'is-marked' : ''}`}
            onClick={toggleMarkForReview}
          >
            <i className={isMarked ? "fa-solid fa-bookmark" : "fa-regular fa-bookmark"}></i>
            <span className="desktop-only">{isMarked ? 'Marked' : 'Mark'}</span>
          </button>
        </div>

        <div className="footer-right">
          {currentIndex < safeList.length - 1 ? (
            <button 
              className="exam-nav-btn next-btn" 
              onClick={() => setCurrentIndex(p => p + 1)}
            >
              <span className="desktop-only">Next</span> <i className="fa-solid fa-chevron-right"></i>
            </button>
          ) : (
            <button 
              className="exam-nav-btn submit-btn" 
              onClick={() => setShowSubmitModal(true)}
            >
              Finish Block <i className="fa-solid fa-flag-checkered"></i>
            </button>
          )}
        </div>
      </footer>

      {/* Redesigned Submit Modal Overlay */}
      {showSubmitModal && (
        <div className="exam-modal-overlay" onClick={() => setShowSubmitModal(false)}>
          <div className="exam-modal-content animate-slide-up" onClick={e => e.stopPropagation()}>
            <button
              className="submit-modal-close"
              onClick={() => setShowSubmitModal(false)}
              title="Close modal"
            >
              <i className="fa-solid fa-xmark"></i>
            </button>

            <div className="modal-icon-header">
              <i className="fa-solid fa-flag-checkered"></i>
            </div>
            
            <h3>Finish Examination Block?</h3>
            <p className="modal-subtitle">Review your question summary below before submitting for scoring.</p>
            
            <div className="modal-stats-grid">
              <div className="modal-stat-card">
                <i className="fa-solid fa-circle-check" style={{ color: 'var(--accent-cyan)' }}></i>
                <span className="stat-label">Attempted</span>
                <span className="stat-value" style={{ color: 'var(--accent-cyan)' }}>{answeredCount}</span>
              </div>
              <div className="modal-stat-card">
                <i className="fa-solid fa-circle-question" style={{ color: unansweredCount > 0 ? 'var(--accent-amber)' : 'var(--text-muted)' }}></i>
                <span className="stat-label">Unanswered</span>
                <span className="stat-value" style={{ color: unansweredCount > 0 ? 'var(--accent-amber)' : 'var(--text-muted)' }}>{unansweredCount}</span>
              </div>
              <div className="modal-stat-card">
                <i className="fa-solid fa-bookmark" style={{ color: 'var(--accent-purple)' }}></i>
                <span className="stat-label">Marked</span>
                <span className="stat-value" style={{ color: 'var(--accent-purple)' }}>{markedCount}</span>
              </div>
            </div>

            <div className={`modal-alert-box ${unansweredCount > 0 ? 'warning' : 'success'}`}>
              <i className={`fa-solid ${unansweredCount > 0 ? 'fa-triangle-exclamation' : 'fa-shield-check'}`} style={{ fontSize: '1.2rem' }}></i>
              <div>
                {unansweredCount > 0 
                  ? `You have ${unansweredCount} unanswered questions remaining. Unanswered items will be scored as incorrect.` 
                  : `Excellent! All ${safeList.length} questions completed. Ready to submit for instant scoring.`}
              </div>
            </div>

            <div className="modal-actions">
              <button className="exam-btn-secondary" onClick={() => setShowSubmitModal(false)} style={{ flex: 1 }}>
                <i className="fa-solid fa-arrow-left"></i> Return
              </button>
              <button className="exam-btn-primary" onClick={() => handleFinalSubmit(false)} style={{ flex: 1 }}>
                <i className="fa-solid fa-check-double"></i> Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
