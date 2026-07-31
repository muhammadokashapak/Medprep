import { safeStorageGet, safeStorageSet } from './security';

export const MEDICAL_RANKS = [
  { level: 1, title: 'Medical Student', minXP: 0, icon: 'fa-user-graduate', color: '#06b6d4' },
  { level: 2, title: 'Intern Doctor', minXP: 250, icon: 'fa-user-doctor', color: '#3b82f6' },
  { level: 3, title: 'Junior Resident', minXP: 750, icon: 'fa-stethoscope', color: '#10b981' },
  { level: 4, title: 'Senior Registrar', minXP: 2000, icon: 'fa-hospital-user', color: '#8b5cf6' },
  { level: 5, title: 'Consultant Specialist', minXP: 5000, icon: 'fa-crown', color: '#f59e0b' }
];

export function getUserGamificationData() {
  const defaultData = {
    xp: 0,
    streak: 0,
    lastStreakDate: '',
    completedChallenges: []
  };
  return safeStorageGet('medprep_gamification', defaultData);
}

export function saveUserGamificationData(data) {
  safeStorageSet('medprep_gamification', data);
}

export function getCurrentRank(xp) {
  let currentRank = MEDICAL_RANKS[0];
  for (let i = MEDICAL_RANKS.length - 1; i >= 0; i--) {
    if (xp >= MEDICAL_RANKS[i].minXP) {
      currentRank = MEDICAL_RANKS[i];
      break;
    }
  }
  return currentRank;
}

export function addXP(amount) {
  const data = getUserGamificationData();
  const oldRank = getCurrentRank(data.xp);
  data.xp += amount;
  const newRank = getCurrentRank(data.xp);
  saveUserGamificationData(data);
  return { data, leveledUp: newRank.level > oldRank.level, newRank };
}

export function updateDailyStreak() {
  const data = getUserGamificationData();
  const today = new Date().toISOString().split('T')[0];
  
  if (data.lastStreakDate === today) {
    return { data, streakIncremented: false };
  }

  const yesterdayDate = new Date();
  yesterdayDate.setDate(yesterdayDate.getDate() - 1);
  const yesterday = yesterdayDate.toISOString().split('T')[0];

  if (data.lastStreakDate === yesterday) {
    data.streak += 1;
  } else if (data.lastStreakDate !== today) {
    data.streak = 1;
  }

  data.lastStreakDate = today;
  data.xp += 50; // Daily check-in XP bonus
  saveUserGamificationData(data);

  return { data, streakIncremented: true };
}
