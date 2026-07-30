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
    const limit = config?.timeLimitMinutes ?? config?.limit ?? null;
    if (limit !== null) {
      return limit * 60;
    }
    return null;
  });

  const [showPalette, setShowPalette] = useState(false);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [examResult, setExamResult] = useState(null);
  const [startTime] = useState(Date.now());
  const [showOnlyIncorrect, setShowOnlyIncorrect] = useState(false);

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

  const handleFinalSubmit = useCallback((auto = false) => {
    setShowSubmitModal(false);
    setIsCompleted(true);

    const totalQ = safeList.length;
    let correctCount = 0;
    let attemptedCount = 0;
    const currentAnswersMap = userAnswersRef.current;

    const details = safeList.map((q, idx) => {
      const iterQKey = q.id ?? `q_${idx}`;
      const ans = currentAnswersMap[iterQKey];
      const selected = ans?.selected ?? null;
      const isCorrect = selected && q.correct_answer 
        ? selected.toUpperCase() === String(q.correct_answer).toUpperCase()
        : false;

      if (selected !== null && selected !== undefined) {
        attemptedCount++;
        if (isCorrect) correctCount++;
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
      totalQuestions: totalQ,
      attemptedCount,
      skippedCount: totalQ - attemptedCount,
      correctCount,
      scorePercentage,
      accuracyPercentage,
      timeTaken: timeTakenStr,
      details,
      date: new Date().toLocaleDateString()
    };

    setExamResult(resultObj);
    if (onRecordResult) {
      onRecordResult(resultObj);
    }

    if (auto) {
      addToast?.('Time expired! Exam auto-submitted.', 'warning');
    } else if (scorePercentage >= 70 && attemptedCount > 0) {
      confetti({ particleCount: 120, spread: 80, origin: { y: 0.5 } });
      addToast?.(`Passed! Score: ${scorePercentage}% (${correctCount}/${totalQ} Solved)`, 'success');
    } else {
      addToast?.(`Exam Submitted. Score: ${scorePercentage}% (${correctCount}/${totalQ} Solved)`, 'warning');
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
    const isPass = examResult.scorePercentage >= 70;
    const filteredDetails = showOnlyIncorrect
      ? examResult.details.filter(d => !d.isCorrect)
      : examResult.details;

    const getOptionText = (q, key) => {
      if (!key || key === 'Unattempted') return 'Not Answered';
      const optKey = `option_${key.toLowerCase()}`;
      return q[optKey] ? `${key}: ${q[optKey]}` : key;
    };

    return (
      <div className="animate-fade-in" style={{ padding: '1rem 0', maxWidth: '960px', margin: '0 auto' }}>
        {/* Results Overview Hero Header */}
        <div className="glass-panel text-center" style={{
          padding: '2rem 1.25rem',
          marginBottom: '1.5rem',
          borderLeft: `5px solid ${isPass ? 'var(--accent-emerald)' : 'var(--accent-amber)'}`,
          background: isPass ? 'rgba(16, 185, 129, 0.08)' : 'rgba(245, 158, 11, 0.08)'
        }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: isPass ? 'rgba(16, 185, 129, 0.18)' : 'rgba(245, 158, 11, 0.18)',
            color: isPass ? 'var(--accent-emerald)' : 'var(--accent-amber)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.8rem',
            margin: '0 auto 1rem'
          }}>
            <i className={`fa-solid ${isPass ? 'fa-award' : 'fa-clipboard-check'}`}></i>
          </div>

          <h1 style={{ fontSize: '1.6rem', marginBottom: '0.35rem', fontWeight: 800 }}>
            {examResult.title} Complete
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
            Board Examination Results Logged
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
            <div>
              <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>ACCURACY</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: isPass ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                {examResult.scorePercentage}%
              </span>
            </div>
            <div>
              <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>CORRECT</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-main)' }}>
                {examResult.correctCount} <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/ {examResult.attemptedCount}</span>
              </span>
            </div>
            <div>
              <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>TIME</span>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                {examResult.timeTaken}
              </span>
            </div>
          </div>

          <button className="btn-primary" onClick={() => onFinish && onFinish(examResult)} style={{ padding: '0.75rem 1.8rem', fontSize: '0.92rem' }}>
            <i className="fa-solid fa-house"></i> Return to Candidate Hub
          </button>
        </div>

        {/* Detailed Question Review Section */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
            Rationale Review ({filteredDetails.length})
          </h3>

          <button
            className="btn-secondary"
            onClick={() => setShowOnlyIncorrect(!showOnlyIncorrect)}
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', minHeight: '36px', width: 'auto' }}
          >
            <i className={`fa-solid ${showOnlyIncorrect ? 'fa-eye' : 'fa-filter'}`}></i>
            {showOnlyIncorrect ? 'Show All' : 'Incorrect Only'}
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredDetails.length === 0 && showOnlyIncorrect && (
            <div className="glass-panel text-center" style={{ padding: '2.5rem', marginTop: '1rem' }}>
              <i className="fa-solid fa-face-grin-stars" style={{ fontSize: '3rem', color: 'var(--accent-emerald)', marginBottom: '1rem' }}></i>
              <h3 style={{ color: 'var(--accent-emerald)' }}>Perfect Score!</h3>
              <p style={{ color: 'var(--text-muted)' }}>You didn't get any questions wrong.</p>
            </div>
          )}
          {filteredDetails.map((det) => (
            <div
              key={det.q.id ?? `review_q_${det.index}`}
              className="glass-panel"
              style={{
                padding: '1.25rem',
                borderLeft: `4px solid ${det.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'}`
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.65rem', flexWrap: 'wrap', gap: '0.4rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.82rem', color: 'var(--accent-cyan)' }}>
                  Q#{det.index} &bull; {det.q.category || 'General'}
                </span>
                <span className="badge" style={{
                  padding: '0.2rem 0.6rem',
                  fontSize: '0.72rem',
                  background: det.isCorrect ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                  color: det.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                  borderColor: det.isCorrect ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'
                }}>
                  {det.isCorrect ? 'CORRECT' : 'INCORRECT'}
                </span>
              </div>

              <h4 style={{ fontSize: '0.95rem', fontWeight: 500, lineHeight: 1.5, marginBottom: '1rem' }}>
                {det.q.question}
              </h4>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '0.65rem', marginBottom: '1rem' }}>
                <div style={{ padding: '0.6rem 0.85rem', borderRadius: 'var(--radius-sm)', background: det.isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(244, 63, 94, 0.1)', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)' }}>YOUR ANSWER</span>
                  <strong style={{ fontSize: '0.88rem', color: det.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                    {getOptionText(det.q, det.selected)}
                  </strong>
                </div>

                <div style={{ padding: '0.6rem 0.85rem', borderRadius: 'var(--radius-sm)', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)' }}>CORRECT ANSWER</span>
                  <strong style={{ fontSize: '0.88rem', color: 'var(--accent-emerald)' }}>
                    {getOptionText(det.q, det.correctAnswer)}
                  </strong>
                </div>
              </div>

              {det.explanation && (
                <div style={{ padding: '0.85rem 1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.88rem', lineHeight: 1.5 }}>
                  <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '0.25rem' }}>
                    <i className="fa-solid fa-lightbulb"></i> Clinical Explanation:
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
    <div className="animate-fade-in" style={{ padding: '0.5rem 0 4.5rem', maxWidth: '1000px', margin: '0 auto', position: 'relative' }}>
      {/* Top Exam Header Bar */}
      <div className="glass-panel" style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        padding: '0.65rem 0.85rem', 
        marginBottom: '0.85rem', 
        flexWrap: 'wrap', 
        gap: '0.5rem',
        borderLeft: '4px solid var(--accent-cyan)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', flexWrap: 'wrap' }}>
          <span style={{ fontWeight: 800, fontSize: '0.95rem', color: 'var(--text-main)' }}>
            Q{currentIndex + 1} <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>/ {safeList.length}</span>
          </span>
          <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontWeight: 700, background: 'rgba(6,182,212,0.12)', padding: '0.15rem 0.55rem', borderRadius: '6px' }}>
            {currentQ?.category || 'General'}
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
          {timerSeconds !== null && (
            <div style={{ 
              background: 'rgba(245, 158, 11, 0.12)', 
              color: 'var(--accent-amber)', 
              border: '1px solid rgba(245, 158, 11, 0.3)', 
              borderRadius: 'var(--radius-sm)',
              padding: '0.25rem 0.55rem', 
              fontSize: '0.8rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}>
              <i className="fa-solid fa-clock"></i> {formatTimer(timerSeconds)}
            </div>
          )}

          <button
            className="btn-secondary"
            onClick={() => setShowPalette(!showPalette)}
            style={{ padding: '0.3rem 0.6rem', fontSize: '0.78rem', minHeight: '34px', width: 'auto' }}
          >
            <i className="fa-solid fa-grid-2"></i> ({answeredCount}/{safeList.length})
          </button>

          <button
            className="btn-secondary desktop-only"
            onClick={toggleMarkForReview}
            style={{
              padding: '0.3rem 0.6rem',
              fontSize: '0.78rem',
              minHeight: '34px',
              width: 'auto',
              background: isMarked ? 'rgba(168, 85, 247, 0.2)' : 'transparent',
              color: isMarked ? 'var(--accent-purple)' : 'var(--text-main)',
              borderColor: isMarked ? 'var(--accent-purple)' : 'var(--border-subtle)'
            }}
          >
            <i className="fa-solid fa-bookmark"></i> {isMarked ? 'Marked' : 'Mark'}
          </button>

          <button
            className="btn-primary"
            onClick={() => setShowSubmitModal(true)}
            style={{ padding: '0.3rem 0.75rem', fontSize: '0.78rem', minHeight: '34px', width: 'auto', background: 'var(--gradient-primary)' }}
          >
            Submit
          </button>
        </div>
      </div>

      {/* Question Palette Grid Drawer */}
      {showPalette && (
        <div className="glass-panel animate-fade-in" style={{ padding: '1rem', marginBottom: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <h4 style={{ fontSize: '0.88rem', fontWeight: 600 }}>Question Navigator</h4>
            <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
              <span><i className="fa-solid fa-circle" style={{ color: 'var(--accent-cyan)' }}></i> Solved ({answeredCount})</span>
              <span><i className="fa-solid fa-circle" style={{ color: 'var(--accent-purple)' }}></i> Marked ({markedCount})</span>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(42px, 1fr))', gap: '0.4rem', maxHeight: '180px', overflowY: 'auto' }}>
            {safeList.map((q, idx) => {
              const iterQKey = q.id ?? `q_${idx}`;
              const isAns = !!userAnswers[iterQKey];
              const isM = !!markedForReview[iterQKey];
              const isCurr = idx === currentIndex;

              let bg = 'rgba(255,255,255,0.04)';
              let color = 'var(--text-muted)';
              let border = '1px solid var(--border-subtle)';

              if (isM && isAns) {
                bg = 'rgba(168, 85, 247, 0.2)';
                color = 'var(--accent-cyan)';
                border = '1px solid var(--accent-purple)';
              } else if (isM) {
                bg = 'rgba(168, 85, 247, 0.2)';
                color = 'var(--accent-purple)';
                border = '1px solid var(--accent-purple)';
              } else if (isAns) {
                bg = 'rgba(6, 182, 212, 0.15)';
                color = 'var(--accent-cyan)';
                border = '1px solid var(--accent-cyan)';
              }

              if (isCurr) {
                border = '2px solid #ffffff';
              }

              return (
                <button
                  key={q.id || idx}
                  onClick={() => { setCurrentIndex(idx); setShowPalette(false); }}
                  style={{
                    height: '40px',
                    borderRadius: 'var(--radius-sm)',
                    background: bg,
                    color,
                    border,
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer'
                  }}
                >
                  {idx + 1}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Progress Bar */}
      <div style={{ height: '5px', background: 'rgba(255,255,255,0.06)', borderRadius: '99px', marginBottom: '0.85rem', overflow: 'hidden' }}>
        <div style={{
          height: '100%',
          width: `${((currentIndex + 1) / safeList.length) * 100}%`,
          background: 'var(--gradient-primary)',
          transition: 'width 0.25s ease'
        }}></div>
      </div>

      {/* Main Vignette Question Card */}
      <div className="glass-panel" style={{ padding: '1.25rem 1rem', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '0.98rem', lineHeight: 1.6, fontWeight: 500, color: 'var(--text-main)', marginBottom: '1.25rem' }}>
          {currentQ.question}
        </h3>

        {/* Answer Options A-E */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
          {options.map((opt) => {
            const isSelected = currentAnswer?.selected === opt.key;

            return (
              <div
                key={opt.key}
                className={`option-card ${isSelected ? 'selected' : ''}`}
                onClick={() => handleSelectOption(opt.key)}
                role="button"
                tabIndex={0}
                aria-selected={isSelected}
                onKeyDown={e => (e.key === 'Enter' || e.key === ' ') && handleSelectOption(opt.key)}
              >
                <div className="option-badge">
                  {opt.key}
                </div>

                <span style={{ fontSize: '0.9rem', fontWeight: isSelected ? 600 : 400, lineHeight: 1.45, color: isSelected ? 'var(--accent-cyan)' : 'var(--text-main)' }}>
                  {opt.text}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Desktop Footer Navigation */}
      <div className="desktop-only" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.5rem' }}>
        <button
          className="btn-secondary"
          onClick={() => setCurrentIndex(p => Math.max(0, p - 1))}
          disabled={currentIndex === 0}
          style={{ opacity: currentIndex === 0 ? 0.4 : 1, padding: '0.6rem 1rem', fontSize: '0.85rem', width: 'auto', minHeight: '40px' }}
        >
          <i className="fa-solid fa-chevron-left"></i> Prev
        </button>

        <div style={{ display: 'flex', gap: '0.45rem' }}>
          <button
            className="btn-secondary"
            onClick={toggleMarkForReview}
            style={{
              padding: '0.6rem 0.9rem',
              fontSize: '0.85rem',
              width: 'auto',
              minHeight: '40px',
              background: isMarked ? 'rgba(168, 85, 247, 0.2)' : 'transparent',
              color: isMarked ? 'var(--accent-purple)' : 'var(--text-main)',
              borderColor: isMarked ? 'var(--accent-purple)' : 'var(--border-subtle)'
            }}
          >
            <i className="fa-solid fa-bookmark"></i> {isMarked ? 'Marked' : 'Mark'}
          </button>

          <button
            className="btn-secondary"
            onClick={() => currentIndex < safeList.length - 1 
              ? setCurrentIndex(p => Math.min(safeList.length - 1, p + 1))
              : setShowSubmitModal(true)}
            style={{ padding: '0.6rem 0.9rem', fontSize: '0.85rem', width: 'auto', minHeight: '40px' }}
          >
            {currentIndex < safeList.length - 1 ? 'Skip' : 'Review'}
          </button>

          {currentIndex < safeList.length - 1 ? (
            <button className="btn-primary" onClick={() => setCurrentIndex(p => p + 1)} style={{ padding: '0.6rem 1.1rem', fontSize: '0.85rem', width: 'auto', minHeight: '40px' }}>
              Next <i className="fa-solid fa-chevron-right"></i>
            </button>
          ) : (
            <button className="btn-primary" style={{ background: 'var(--gradient-success)', padding: '0.6rem 1.1rem', fontSize: '0.85rem', width: 'auto', minHeight: '40px' }} onClick={() => setShowSubmitModal(true)}>
              Submit <i className="fa-solid fa-check"></i>
            </button>
          )}
        </div>
      </div>

      {/* Mobile Sticky Action Bar */}
      <div className="exam-mobile-footer">
        <button
          className="btn-secondary"
          onClick={() => setCurrentIndex(p => Math.max(0, p - 1))}
          disabled={currentIndex === 0}
          style={{ flex: 1, opacity: currentIndex === 0 ? 0.4 : 1 }}
        >
          <i className="fa-solid fa-chevron-left"></i> Prev
        </button>

        <button
          className="btn-secondary"
          onClick={() => currentIndex < safeList.length - 1 
            ? setCurrentIndex(p => Math.min(safeList.length - 1, p + 1))
            : setShowSubmitModal(true)}
          style={{ flex: 1 }}
        >
          {currentIndex < safeList.length - 1 ? 'Skip' : 'Review'}
        </button>

        <button
          className="btn-secondary"
          onClick={toggleMarkForReview}
          style={{
            flex: 1,
            background: isMarked ? 'rgba(168, 85, 247, 0.25)' : 'rgba(255,255,255,0.05)',
            color: isMarked ? 'var(--accent-purple)' : 'var(--text-main)',
            borderColor: isMarked ? 'var(--accent-purple)' : 'var(--border-subtle)'
          }}
        >
          <i className="fa-solid fa-bookmark"></i> {isMarked ? 'Marked' : 'Mark'}
        </button>

        {currentIndex < safeList.length - 1 ? (
          <button className="btn-primary" onClick={() => setCurrentIndex(p => p + 1)} style={{ flex: 1.2 }}>
            Next <i className="fa-solid fa-chevron-right"></i>
          </button>
        ) : (
          <button className="btn-primary" style={{ flex: 1.2, background: 'var(--gradient-success)' }} onClick={() => setShowSubmitModal(true)}>
            Finish <i className="fa-solid fa-check"></i>
          </button>
        )}
      </div>

      {/* Submit Modal Overlay */}
      {showSubmitModal && (
        <div 
          onClick={() => setShowSubmitModal(false)}
          style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(10px)',
          zIndex: 999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1rem'
        }}>
          <div className="glass-panel animate-fade-in text-center" 
               onClick={e => e.stopPropagation()}
               style={{ padding: '1.75rem 1.25rem', maxWidth: '440px', width: '100%' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Submit Examination Session?</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
              You have answered <strong>{answeredCount}</strong> out of <strong>{safeList.length}</strong> questions.
              {unansweredCount > 0 && ` (${unansweredCount} unattempted).`}
            </p>

            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
              <button className="btn-secondary" onClick={() => setShowSubmitModal(false)} style={{ width: 'auto', minHeight: '40px' }}>
                Continue Exam
              </button>
              <button className="btn-primary" style={{ background: 'var(--gradient-success)', width: 'auto', minHeight: '40px' }} onClick={() => handleFinalSubmit(false)}>
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
