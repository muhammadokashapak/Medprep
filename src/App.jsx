import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import QuizEngine from './components/QuizEngine';
import MistakesBank from './components/MistakesBank';
import ToastNotification from './components/ToastNotification';
import AuthModal from './components/AuthModal';
import UserProfileModal from './components/UserProfileModal';
import ExamComparisonModal from './components/ExamComparisonModal';
import RankBadgesModal from './components/RankBadgesModal';
import DailyGoalModal from './components/DailyGoalModal';
import questionsData from './data/questions.json';
import { safeStorageGet, safeStorageSet, sanitizeUserSession, fisherYatesShuffle, getQuestionsForTrack } from './utils/security';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [theme, setTheme] = useState(() => localStorage.getItem('fcps_theme') || 'dark');
  const [quizState, setQuizState] = useState(null); // { list, config }

  // Safe Authentication State Initialization
  const [currentUser, setCurrentUser] = useState(() => {
    return safeStorageGet('medprep_user', null);
  });

  // If user is null, auth modal is ALWAYS open (Mandatory Gate)
  const [isAuthOpen, setIsAuthOpen] = useState(() => !currentUser);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isCompareOpen, setIsCompareOpen] = useState(false);
  const [isRankModalOpen, setIsRankModalOpen] = useState(false);
  const [isDailyGoalModalOpen, setIsDailyGoalModalOpen] = useState(false);

  const [dailyGoal, setDailyGoal] = useState(() => safeStorageGet('fcps_daily_goal', 50));

  // Global Toasts State
  const [toasts, setToasts] = useState([]);

  const addToast = (message, type = 'info') => {
    const id = Date.now() + Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3500);
  };

  const removeToast = (id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  // Persistent User Progress Stats with safe fallback
  const [stats, setStats] = useState(() => {
    return safeStorageGet('fcps_stats', {
      attemptedCount: 0,
      correctCount: 0,
      mistakesCount: 0,
      mistakesList: []
    });
  });

  // Persistent Exam History with safe fallback
  const [history, setHistory] = useState(() => {
    return safeStorageGet('fcps_history', []);
  });

  // Theme Sync
  useEffect(() => {
    document.body.className = theme === 'light' ? 'light-theme' : '';
    localStorage.setItem('fcps_theme', theme);
  }, [theme]);

  // Save Stats & History Safely
  useEffect(() => {
    safeStorageSet('fcps_stats', stats);
  }, [stats]);

  useEffect(() => {
    safeStorageSet('fcps_history', history);
  }, [history]);

  // Mandatory Auth Enforcement: If user logs out, force Auth modal open
  useEffect(() => {
    if (!currentUser) {
      setIsAuthOpen(true);
    }
  }, [currentUser]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  // Extract candidate's registered exam track and filter dataset strictly
  const userTrack = currentUser?.examPreference || 'FCPS Part 1';
  const trackQuestions = React.useMemo(() => {
    return getQuestionsForTrack(questionsData, userTrack);
  }, [userTrack]);

  // Launch Quiz Helper - Filtered strictly for candidate's registered track
  const startQuiz = ({ mode, examTrack, limit, timeLimitMinutes }) => {
    if (!currentUser) {
      addToast('Please Sign In or Register an Account to access QBank tests', 'warning');
      setIsAuthOpen(true);
      return;
    }

    const activeExamTrack = examTrack || userTrack;
    const pool = getQuestionsForTrack(questionsData, activeExamTrack);

    if (!pool || pool.length === 0) {
      addToast(`No questions found for ${activeExamTrack}`, 'error');
      return;
    }

    let selectedQuestions = [];

    if (mode === 'mistakes') {
      const mistakesIds = new Set(stats.mistakesList.map(m => m.id));
      selectedQuestions = pool.filter(q => mistakesIds.has(q.id));
      if (selectedQuestions.length === 0) {
        addToast('No mistake questions found for this exam track!', 'info');
        return;
      }
    } else {
      selectedQuestions = fisherYatesShuffle(pool);
    }

    if (limit && limit > 0 && limit < selectedQuestions.length) {
      selectedQuestions = selectedQuestions.slice(0, limit);
    }

    setQuizState({
      list: selectedQuestions,
      config: {
        mode,
        examTrack: activeExamTrack,
        title: `${activeExamTrack} Official Exam Block`,
        limit: selectedQuestions.length,
        isMock: mode === 'mock' || mode === 'full_official'
      }
    });

    setActiveTab('practice');
    addToast(`Loaded ${selectedQuestions.length} Questions for ${activeExamTrack}`, 'success');
  };

  const recordExamResult = (examResultObj) => {
    if (!examResultObj) return;

    setHistory(prev => [examResultObj, ...prev]);

    setStats(prev => {
      const newAttempted = prev.attemptedCount + (examResultObj.attemptedCount || 0);
      const newCorrect = prev.correctCount + (examResultObj.correctCount || 0);

      let updatedMistakes = [...prev.mistakesList];

      if (examResultObj.details && Array.isArray(examResultObj.details)) {
        examResultObj.details.forEach(item => {
          if (!item.isCorrect) {
            if (!updatedMistakes.some(m => m.id === item.q.id)) {
              updatedMistakes.push(item.q);
            }
          } else {
            updatedMistakes = updatedMistakes.filter(m => m.id !== item.q.id);
          }
        });
      }

      return {
        attemptedCount: newAttempted,
        correctCount: newCorrect,
        mistakesCount: updatedMistakes.length,
        mistakesList: updatedMistakes
      };
    });
  };

  const handleFinishQuiz = () => {
    setQuizState(null);
    setActiveTab('dashboard');
    addToast('Returned to Dashboard', 'info');
  };

  const removeSingleMistake = (qId) => {
    setStats(prev => {
      const filtered = prev.mistakesList.filter(m => m.id !== qId);
      return {
        ...prev,
        mistakesCount: filtered.length,
        mistakesList: filtered
      };
    });
    addToast('Question removed from Mistakes Bank', 'info');
  };

  const clearMistakesOnly = () => {
    setStats(prev => ({
      ...prev,
      mistakesCount: 0,
      mistakesList: []
    }));
    addToast('Mistakes Bank reset successfully', 'info');
  };

  const resetProgress = () => {
    setStats({
      attemptedCount: 0,
      correctCount: 0,
      mistakesCount: 0,
      mistakesList: []
    });
    setHistory([]);
    localStorage.removeItem('fcps_stats');
    localStorage.removeItem('fcps_history');
  };

  const handleLogin = (userObj, rememberMe) => {
    const safeUser = sanitizeUserSession(userObj);
    setCurrentUser(safeUser);
    setIsAuthOpen(false);
    if (rememberMe) {
      safeStorageSet('medprep_user', safeUser);
    }
    addToast(`Welcome, Dr. ${safeUser.name}! Loading ${safeUser.examPreference || 'FCPS Part 1'} QBank.`, 'success');
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('medprep_user');
    setIsAuthOpen(true);
    setActiveTab('dashboard');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <ToastNotification toasts={toasts} removeToast={removeToast} />

      <Navbar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          if (!currentUser) {
            setIsAuthOpen(true);
            return;
          }
          if (tab === 'practice' && !quizState) {
            startQuiz({ mode: 'full_official', examTrack: userTrack });
          } else {
            setActiveTab(tab);
          }
        }} 
        stats={stats} 
        theme={theme} 
        toggleTheme={toggleTheme} 
        currentUser={currentUser}
        onOpenAuth={() => setIsAuthOpen(true)}
        onOpenProfile={() => setIsProfileOpen(true)}
        totalQuestions={trackQuestions.length}
      />

      <main style={{ flex: 1, maxWidth: '1300px', width: '100%', margin: '0 auto', padding: '0 0.85rem' }}>
        {!currentUser ? (
          /* MANDATORY AUTHENTICATION GATE SCREEN */
          <div className="animate-fade-in text-center" style={{ padding: '2rem 0.5rem', maxWidth: '700px', margin: '0 auto' }}>
            <div className="glass-panel" style={{ padding: '2rem 1.25rem', background: 'var(--gradient-card-hero)', border: '1px solid var(--border-glow)' }}>
              <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '16px',
                background: 'var(--gradient-primary)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.6rem',
                margin: '0 auto 1.25rem',
                boxShadow: 'var(--shadow-glow)'
              }}>
                <i className="fa-solid fa-stethoscope"></i>
              </div>

              <h1 style={{ fontSize: '1.75rem', marginBottom: '0.75rem', fontWeight: 800 }}>
                MedPrep Pro <span className="gradient-text">Candidate Portal</span>
              </h1>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: 1.5, marginBottom: '1.75rem' }}>
                Sign in or create a candidate account to access your official medical board QBank, timed mock exams, and analytics.
              </p>

              <button className="btn-primary" onClick={() => setIsAuthOpen(true)} style={{ padding: '0.8rem 1.8rem', fontSize: '0.95rem', justifyContent: 'center' }}>
                <i className="fa-solid fa-user-lock"></i> Sign In / Register Account
              </button>
            </div>
          </div>
        ) : (
          /* LOGGED IN CANDIDATE CONTENT */
          <>
            {activeTab === 'dashboard' && (
              <Dashboard 
                questions={trackQuestions} 
                stats={stats} 
                history={history} 
                startQuiz={startQuiz} 
                currentUser={currentUser}
                onOpenAuth={() => setIsAuthOpen(true)}
                onOpenProfile={() => setIsProfileOpen(true)}
                onOpenCompareModal={() => setIsCompareOpen(true)}
                onOpenRankModal={() => setIsRankModalOpen(true)}
                onOpenGoalModal={() => setIsDailyGoalModalOpen(true)}
                dailyGoal={dailyGoal}
              />
            )}

            {activeTab === 'practice' && (
              <QuizEngine 
                quizList={quizState?.list || trackQuestions} 
                onRecordResult={recordExamResult} 
                onFinish={handleFinishQuiz} 
                config={quizState?.config} 
                addToast={addToast} 
              />
            )}

            {activeTab === 'mistakes' && (
              <MistakesBank 
                mistakesList={stats.mistakesList} 
                startMistakesQuiz={() => startQuiz({ mode: 'mistakes' })} 
                clearMistakes={clearMistakesOnly} 
                removeSingleMistake={removeSingleMistake} 
              />
            )}
          </>
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '1.25rem 1rem',
        color: 'var(--text-subdued)',
        borderTop: '1px solid var(--border-subtle)',
        marginTop: '2rem',
        fontSize: '0.8rem'
      }}>
        MedPrep Pro &bull; Medical Exam Prep Platform &bull; {currentUser ? `${userTrack} (${trackQuestions.length.toLocaleString()} Questions)` : '48,000+ Total MCQs'}
      </footer>

      <AuthModal 
        isOpen={isAuthOpen} 
        onClose={() => {
          if (currentUser) setIsAuthOpen(false);
        }} 
        onLogin={handleLogin} 
        addToast={addToast} 
      />

      <UserProfileModal 
        isOpen={isProfileOpen} 
        onClose={() => setIsProfileOpen(false)} 
        user={currentUser} 
        stats={stats} 
        history={history} 
        onLogout={handleLogout} 
        resetProgress={resetProgress} 
        addToast={addToast} 
      />

      <ExamComparisonModal
        isOpen={isCompareOpen}
        onClose={() => setIsCompareOpen(false)}
        history={history}
        currentUser={currentUser}
        addToast={addToast}
      />

      <RankBadgesModal
        isOpen={isRankModalOpen}
        onClose={() => setIsRankModalOpen(false)}
        stats={stats}
        history={history}
      />

      <DailyGoalModal
        isOpen={isDailyGoalModalOpen}
        onClose={() => setIsDailyGoalModalOpen(false)}
        currentGoal={dailyGoal}
        onSetGoal={(newGoal) => {
          setDailyGoal(newGoal);
          safeStorageSet('fcps_daily_goal', newGoal);
          addToast(`Daily MCQ target set to ${newGoal} questions!`, 'success');
        }}
      />
    </div>
  );
}
