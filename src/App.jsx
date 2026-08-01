import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import QuizEngine from './components/QuizEngine';
import MistakesBank from './components/MistakesBank';
import ToastNotification from './components/ToastNotification';
import AuthModal from './components/AuthModal';
import UserProfileModal from './components/UserProfileModal';
import ExamComparisonModal from './components/ExamComparisonModal';
import ExamLaunchModal from './components/ExamLaunchModal';
import RankBadgesModal from './components/RankBadgesModal';
import DailyGoalModal from './components/DailyGoalModal';
import QBankExplorer from './components/QBankExplorer';
import SubjectBrowser from './components/SubjectBrowser';
import Flashcards from './components/Flashcards';
import MnemonicsLibrary from './components/MnemonicsLibrary';
import DailyChallengeModal from './components/DailyChallengeModal';
import { updateDailyStreak, addXP, getUserGamificationData } from './utils/gamification';
import questionsData from './data/questions.json';
import { safeStorageGet, safeStorageSet, sanitizeUserSession, fisherYatesShuffle, getQuestionsForTrack } from './utils/security';
import { syncStatsNeon, saveExamResultNeon } from './services/neonDb';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [theme, setTheme] = useState(() => safeStorageGet('fcps_theme', 'dark'));
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

  const [bookmarks, setBookmarks] = useState(() => safeStorageGet('fcps_bookmarks', {}));

  const [launchExamTrack, setLaunchExamTrack] = useState(null);
  const [isDailyChallengeOpen, setIsDailyChallengeOpen] = useState(false);
  const [gamification, setGamification] = useState(() => getUserGamificationData());

  useEffect(() => {
    // Check daily streak on mount
    const res = updateDailyStreak();
    setGamification(res.data);
    if (res.streakIncremented) {
      addToast(`🔥 Daily Streak Maintained! +50 XP Bonus`, 'success');
    }
  }, []);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (!window.history.state || window.history.state.tab !== activeTab) {
      window.history.pushState({ tab: activeTab }, '', `#${activeTab}`);
    }
  }, [activeTab]);

  // Native Mobile History & Back Gesture Navigation
  useEffect(() => {
    const handlePopState = (e) => {
      // 1. Close open modals first
      if (launchExamTrack) {
        setLaunchExamTrack(null);
        return;
      }
      if (isDailyChallengeOpen) {
        setIsDailyChallengeOpen(false);
        return;
      }
      if (isProfileOpen) {
        setIsProfileOpen(false);
        return;
      }
      if (isCompareOpen) {
        setIsCompareOpen(false);
        return;
      }
      if (isRankModalOpen) {
        setIsRankModalOpen(false);
        return;
      }
      if (isDailyGoalModalOpen) {
        setIsDailyGoalModalOpen(false);
        return;
      }

      // 2. Intercept active quiz session
      if (quizState) {
        if (window.confirm('Exit active examination session?')) {
          setQuizState(null);
          setActiveTab('dashboard');
        } else {
          window.history.pushState({ tab: activeTab }, '', `#${activeTab}`);
        }
        return;
      }

      // 3. Return to Dashboard tab from any sub-tab
      if (activeTab !== 'dashboard') {
        setActiveTab('dashboard');
        return;
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [
    activeTab, quizState, launchExamTrack, isDailyChallengeOpen,
    isProfileOpen, isCompareOpen, isRankModalOpen, isDailyGoalModalOpen
  ]);

  const toggleBookmark = (qId) => {
    setBookmarks(prev => {
      const next = { ...prev };
      if (next[qId]) delete next[qId];
      else next[qId] = true;
      safeStorageSet('fcps_bookmarks', next);
      return next;
    });
  };

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
      mistakesList: [],
      todayAttemptedCount: 0,
      lastResetDate: ''
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

  // Save Stats & History Safely & Sync to Neon Cloud DB
  useEffect(() => {
    safeStorageSet('fcps_stats', stats);
    if (currentUser?.email) {
      syncStatsNeon(currentUser.email, stats);
    }
  }, [stats, currentUser]);

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
  const startQuiz = ({ mode, examTrack, limit, timeLimitMinutes } = {}) => {
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
      const mistakesList = Array.isArray(stats?.mistakesList) ? stats.mistakesList : [];
      const mistakesIds = new Set(mistakesList.map(m => m.id));
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
        title: mode === 'full_official' ? `${activeExamTrack} Official Exam Block` : `${activeExamTrack} Practice`,
        limit: selectedQuestions.length,
        timeLimitMinutes: timeLimitMinutes ?? null,
        isMock: mode === 'mock' || mode === 'full_official'
      }
    });

    setActiveTab('practice');
    addToast(`Loaded ${selectedQuestions.length} Questions for ${activeExamTrack}`, 'success');
  };

  const handleLaunchBlock = (examTrack, limit, timeLimitMinutes, blockName) => {
    setLaunchExamTrack(null); // Close modal
    startQuiz({ mode: 'full_official', examTrack, limit, timeLimitMinutes });
  };

  const startSubjectQuiz = (subjectName, subjectQuestions, limit = 25) => {
    if (!currentUser) {
      addToast('Please Sign In or Register to access Subject practice blocks', 'warning');
      setIsAuthOpen(true);
      return;
    }

    if (!subjectQuestions || subjectQuestions.length === 0) {
      addToast(`No questions found for ${subjectName}`, 'error');
      return;
    }

    const shuffled = fisherYatesShuffle(subjectQuestions);
    const selected = shuffled.slice(0, Math.min(limit, shuffled.length));

    setQuizState({
      list: selected,
      config: {
        mode: 'subject_practice',
        examTrack: userTrack,
        title: `${subjectName} — Practice Block (${selected.length} Qs)`,
        limit: selected.length,
        timeLimitMinutes: Math.round(selected.length * 1.2), // ~1.2 mins per question
        isMock: false
      }
    });

    setActiveTab('practice');
    addToast(`Loaded ${selected.length} ${subjectName} MCQs!`, 'success');
  };

  const startDailyChallengeSprint = () => {
    setIsDailyChallengeOpen(false);
    const pool = getQuestionsForTrack(questionsData, userTrack);
    const shuffled = fisherYatesShuffle(pool);
    const selected = shuffled.slice(0, 10);

    setQuizState({
      list: selected,
      config: {
        mode: 'daily_challenge',
        examTrack: userTrack,
        title: `🔥 Daily 10-MCQ Challenge Sprint`,
        limit: 10,
        timeLimitMinutes: 10,
        isMock: true
      }
    });

    setActiveTab('practice');
    addToast('Daily 10-Q Sprint Launched! Good luck!', 'success');
  };

  const recordExamResult = (examResultObj) => {
    if (!examResultObj) return;

    setHistory(prev => [examResultObj, ...prev]);

    if (currentUser?.email) {
      saveExamResultNeon(currentUser.email, examResultObj);
    }

    setStats(prev => {
      const safePrev = prev || { attemptedCount: 0, correctCount: 0, mistakesCount: 0, mistakesList: [], todayAttemptedCount: 0, lastResetDate: '' };
      const today = new Date().toISOString().split('T')[0];
      const isNewDay = safePrev.lastResetDate !== today;
      const todayCount = isNewDay ? (examResultObj.attemptedCount || 0) : ((safePrev.todayAttemptedCount || 0) + (examResultObj.attemptedCount || 0));
      
      const newAttempted = (safePrev.attemptedCount || 0) + (examResultObj.attemptedCount || 0);
      const newCorrect = (safePrev.correctCount || 0) + (examResultObj.correctCount || 0);
      let updatedMistakes = Array.isArray(safePrev.mistakesList) ? [...safePrev.mistakesList] : [];

      if (examResultObj.details && Array.isArray(examResultObj.details)) {
        examResultObj.details.forEach(item => {
          if (!item?.q?.id) return;
          if (!item.isCorrect && item.selected && item.selected !== 'Unattempted') {
            if (!updatedMistakes.some(m => m && m.id === item.q.id)) {
              updatedMistakes.push(item.q);
            }
          } else if (item.isCorrect) {
            updatedMistakes = updatedMistakes.filter(m => m && m.id !== item.q.id);
          }
        });
      }

      return {
        attemptedCount: newAttempted,
        correctCount: newCorrect,
        mistakesCount: updatedMistakes.length,
        mistakesList: updatedMistakes,
        todayAttemptedCount: todayCount,
        lastResetDate: today
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
      const filtered = prev.mistakesList.filter(m => m && m.id !== qId);
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
    setQuizState(null);
    setStats({
      attemptedCount: 0,
      correctCount: 0,
      mistakesCount: 0,
      mistakesList: [],
      todayAttemptedCount: 0,
      lastResetDate: ''
    });
    setHistory([]);
    localStorage.removeItem('fcps_stats');
    localStorage.removeItem('fcps_history');
  };

  const handleLogin = (userObj, rememberMe, cloudStats = null, cloudHistory = null) => {
    if (!userObj) return;
    const safeUser = sanitizeUserSession(userObj) || { name: 'Candidate', email: userObj.email || '', examPreference: userObj.examPreference || 'FCPS Part 1' };
    setCurrentUser(safeUser);
    setIsAuthOpen(false);

    if (cloudStats) {
      setStats(cloudStats);
    }
    if (cloudHistory && Array.isArray(cloudHistory)) {
      setHistory(cloudHistory);
    }

    if (rememberMe) {
      safeStorageSet('medprep_user', safeUser);
    } else {
      localStorage.removeItem('medprep_user');
    }
    const doctorName = safeUser.name || 'Candidate';
    const pref = safeUser.examPreference || 'FCPS Part 1';
    addToast(`Welcome, Dr. ${doctorName}! Loading ${pref} QBank.`, 'success');
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setQuizState(null);
    setActiveTab('dashboard');
    setStats({ attemptedCount: 0, correctCount: 0, mistakesCount: 0, mistakesList: [], todayAttemptedCount: 0, lastResetDate: '' });
    setHistory([]);
    localStorage.removeItem('medprep_user');
    setIsAuthOpen(true);
  };

  const updateUserPreference = (newPreference) => {
    if (!currentUser) return;
    const updatedUser = { ...currentUser, examPreference: newPreference };
    setCurrentUser(updatedUser);
    safeStorageSet('medprep_user', updatedUser);
    // Also update in users list
    const rawUsers = safeStorageGet('fcps_users', []);
    const users = Array.isArray(rawUsers) ? rawUsers : [];
    const idx = users.findIndex(u => u && u.email === currentUser.email);
    if (idx !== -1) {
      users[idx].examPreference = newPreference;
      safeStorageSet('fcps_users', users);
    }
    addToast(`Exam track updated to ${newPreference}`, 'success');
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
        onLeaveExam={handleFinishQuiz}
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
                onOpenLaunchModal={(trackId) => setLaunchExamTrack(trackId)}
                onOpenDailyChallenge={() => setIsDailyChallengeOpen(true)}
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
                quizList={quizState?.list || trackQuestions.slice(0, 100)} 
                onRecordResult={recordExamResult} 
                onFinish={handleFinishQuiz} 
                config={quizState?.config || { title: `${userTrack} Practice Block`, isMock: false, limit: 100 }} 
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

            {activeTab === 'subjects' && (
              <SubjectBrowser 
                questions={trackQuestions} 
                startSubjectQuiz={startSubjectQuiz} 
              />
            )}

            {activeTab === 'flashcards' && (
              <Flashcards addToast={addToast} />
            )}

            {activeTab === 'mnemonics' && (
              <MnemonicsLibrary />
            )}

            {activeTab === 'qbank' && (
              <QBankExplorer
                questions={trackQuestions}
                bookmarks={bookmarks}
                toggleBookmark={toggleBookmark}
                addToast={addToast}
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
        updateUserPreference={updateUserPreference}
      />

      <ExamComparisonModal
        isOpen={isCompareOpen}
        onClose={() => setIsCompareOpen(false)}
        history={history}
        currentUser={currentUser}
        addToast={addToast}
        questions={questionsData}
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
        onSaveGoal={(g) => {
          setDailyGoal(g);
          safeStorageSet('fcps_daily_goal', g);
          addToast(`Daily MCQ target set to ${g} questions!`, 'success');
        }}
      />

      {/* Exam Launch Modal */}
      <ExamLaunchModal
        isOpen={!!launchExamTrack}
        onClose={() => setLaunchExamTrack(null)}
        examTrack={launchExamTrack}
        onLaunchBlock={handleLaunchBlock}
      />

      {/* Daily Challenge Sprint Modal */}
      <DailyChallengeModal
        isOpen={isDailyChallengeOpen}
        onClose={() => setIsDailyChallengeOpen(false)}
        onStartChallenge={startDailyChallengeSprint}
        streak={gamification.streak}
      />
    </div>
  );
}
