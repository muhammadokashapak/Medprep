export default function Dashboard({ questions, stats, history, startQuiz, currentUser, onOpenAuth, onOpenCompareModal, onOpenRankModal, onOpenGoalModal, dailyGoal = 50 }) {
  const [selectedMockLimit, setSelectedMockLimit] = useState(50);

  const accuracy = stats.attemptedCount > 0 
    ? Math.round((stats.correctCount / stats.attemptedCount) * 100) 
    : 0;

  // Calculate Best & Average Score from attempt history
  const totalTests = history ? history.length : 0;
  const scores = history && history.length > 0 ? history.map(h => h.scorePercentage) : [accuracy];
  const bestScore = scores.length > 0 ? Math.max(...scores) : 0;
  const avgScore = scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;

  // Calculate real-time subject breakdown accuracy dynamically from history details
  const subjectAccuracyMap = React.useMemo(() => {
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
  const weakSubjects = React.useMemo(() => {
    if (!stats.mistakesList || stats.mistakesList.length === 0) return [];
    const counts = {};
    stats.mistakesList.forEach(m => {
      const subj = m.category.split('-')[0].trim();
      counts[subj] = (counts[subj] || 0) + 1;
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 4);
  }, [stats.mistakesList]);

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

  // General Unauthenticated Guest View
  if (!currentUser) {
    return (
      <div className="animate-fade-in" style={{ padding: '1.25rem 0' }}>
        {/* General Welcome Hero Banner */}
        <div className="glass-panel" style={{
          padding: '2.5rem 1.25rem',
          marginBottom: '2rem',
          background: 'var(--gradient-card-hero)',
          border: '1px solid var(--border-glow)',
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div className="badge" style={{ marginBottom: '1rem', fontSize: '0.78rem' }}>
            <i className="fa-solid fa-circle-check"></i> 48,000+ High-Yield MCQs
          </div>
          <h1 style={{ fontSize: '1.8rem', marginBottom: '0.85rem', fontWeight: 800, lineHeight: 1.25 }}>
            Global Medical Board <span className="gradient-text">Exam Suite</span>
          </h1>
          <p style={{ color: 'var(--text-muted)', maxWidth: '820px', margin: '0 auto 1.75rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
            Master medical licensing boards with real-world timed simulations, subject mastery analytics, and anti-trick distractor verification.
          </p>
          <button className="btn-primary" onClick={onOpenAuth} style={{ margin: '0 auto', padding: '0.8rem 1.8rem', fontSize: '0.95rem' }}>
            <i className="fa-solid fa-user-doctor"></i> Sign In / Register Account
          </button>
        </div>

        {/* Clean Exam Tracks Grid */}
        <h2 style={{ fontSize: '1.4rem', marginBottom: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <i className="fa-solid fa-graduation-cap" style={{ color: 'var(--accent-cyan)' }}></i>
          Official Medical Board Examination Tracks
        </h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '1.15rem',
          marginBottom: '2.5rem'
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
                    background: 'rgba(255,255,255,0.04)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: track.color,
                    fontSize: '1.2rem',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <i className={`fa-solid ${track.icon}`}></i>
                  </div>
                  <span className="badge" style={{ background: 'rgba(255,255,255,0.04)', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
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

              <button className="btn-secondary" onClick={onOpenAuth} style={{ width: '100%', justifyContent: 'center', marginTop: '1rem' }}>
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
        <div style={{ maxWidth: '700px', flex: 1, minWidth: '240px' }}>
          <div className="badge" style={{ marginBottom: '0.65rem', fontSize: '0.78rem' }}>
            <i className="fa-solid fa-user-check"></i> Registered Candidate &bull; {userTrack} Track
          </div>
          <h1 style={{ fontSize: '1.65rem', marginBottom: '0.45rem', fontWeight: 800, lineHeight: 1.3 }}>
            Welcome back, <span className="gradient-text">Dr. {currentUser.name}</span>
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', lineHeight: 1.5 }}>
            Select an official medical board exam block or custom timed mock session below to start.
          </p>
        </div>

        <div style={{ width: '100%', maxWidth: '280px' }}>
          <button 
            className="btn-primary" 
            onClick={() => startQuiz({ mode: 'full_official', examTrack: userTrack })}
            style={{ width: '100%', justifyContent: 'center', padding: '0.8rem 1.2rem', fontSize: '0.95rem' }}
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
            onClick={() => onOpenGoalModal && onOpenGoalModal()}
            style={{
              background: 'rgba(255,255,255,0.03)',
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
                  stroke="rgba(255,255,255,0.08)"
                  strokeWidth="3.5"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="var(--accent-cyan)"
                  strokeWidth="3.5"
                  strokeDasharray={`${Math.min(100, Math.round(((stats.attemptedCount % dailyGoal) / dailyGoal) * 100))}, 100`}
                />
              </svg>
              <span style={{ position: 'absolute', fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                {stats.attemptedCount % dailyGoal}/{dailyGoal}
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
            onClick={() => onOpenRankModal && onOpenRankModal()}
            style={{
              background: 'rgba(255,255,255,0.03)',
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
            {(history && history.length > 0 ? history.slice(0, 7).reverse() : [{ scorePercentage: accuracy || 65 }, { scorePercentage: 72 }, { scorePercentage: 80 }]).map((item, idx) => {
              const hPct = Math.max(15, Math.min(100, item.scorePercentage || 50));
              return (
                <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.35rem', height: '100%', justifyContent: 'flex-end' }}>
                  <span style={{ fontSize: '0.7rem', fontWeight: 700, color: item.scorePercentage >= 70 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                    {item.scorePercentage}%
                  </span>
                  <div style={{
                    width: '100%',
                    maxWidth: '32px',
                    height: `${hPct}%`,
                    background: item.scorePercentage >= 70 ? 'var(--gradient-success)' : 'var(--gradient-gold)',
                    borderRadius: '6px 6px 0 0',
                    transition: 'height 0.4s ease'
                  }}></div>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-subdued)' }}>T#{idx + 1}</span>
                </div>
              );
            })}
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
              const score = data.total > 0 ? Math.round((data.correct / data.total) * 100) : (accuracy > 0 ? accuracy : 70);

              return (
                <div key={item.subject}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '0.25rem' }}>
                    <span style={{ color: 'var(--text-main)', fontWeight: 500 }}>{item.subject}</span>
                    <strong style={{ color: item.color }}>{score}% ({data.correct}/{data.total || 10})</strong>
                  </div>
                  <div style={{ height: '6px', background: 'rgba(255,255,255,0.06)', borderRadius: '99px', overflow: 'hidden' }}>
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
              onClick={() => startQuiz({ mode: 'mistakes' })}
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
                <span style={{ background: 'rgba(0,0,0,0.25)', padding: '0.1rem 0.4rem', borderRadius: '99px', fontSize: '0.7rem' }}>
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
          const isSelected = track.id === userTrack;
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
                    background: 'rgba(255,255,255,0.04)',
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
                    <span className="badge" style={{ background: 'rgba(255,255,255,0.04)', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
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
                onClick={() => startQuiz({ mode: 'full_official', examTrack: track.id })} 
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
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem' }}>
            {[25, 50, 100, 150].map(count => (
              <button
                key={count}
                onClick={() => setSelectedMockLimit(count)}
                style={{
                  padding: '0.5rem 0.2rem',
                  borderRadius: 'var(--radius-sm)',
                  border: `1px solid ${selectedMockLimit === count ? 'var(--accent-purple)' : 'var(--border-subtle)'}`,
                  background: selectedMockLimit === count ? 'rgba(168, 85, 247, 0.18)' : 'rgba(255,255,255,0.03)',
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
            onClick={() => startQuiz({ mode: 'mock', limit: selectedMockLimit })}
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
        <div className="glass-panel text-center" style={{ padding: '2rem 1rem', color: 'var(--text-muted)' }}>
          <i className="fa-solid fa-folder-open" style={{ fontSize: '1.8rem', color: 'var(--text-subdued)', marginBottom: '0.5rem', display: 'block' }}></i>
          No exam attempts recorded yet. Launch an official exam to track progress!
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {history.slice(0, 8).map((h, i) => (
            <div key={h.id || `${h.title || 'exam'}-${h.date}-${i}`} className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 1.1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <strong style={{ fontSize: '0.95rem', color: 'var(--text-main)' }}>{h.title || `${userTrack} Exam`}</strong>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                  {h.date} &bull; {h.attemptedCount || h.totalQuestions} Questions Solved
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
    </div>
  );
}
