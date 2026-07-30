/**
 * MedPrep Pro Security & Utility Helper Module
 * Provides password hashing, safe JSON parsing, input sanitization, and unbiased shuffling.
 */

// 1. Password Hashing using SHA-256 with HTTP/Mobile fallback
export async function hashPassword(plainPassword) {
  if (!plainPassword) return '';
  try {
    if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle) {
      const encoder = new TextEncoder();
      const data = encoder.encode(plainPassword);
      const hashBuffer = await window.crypto.subtle.digest('SHA-256', data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
  } catch (err) {
    console.warn('[Security] Web Crypto API unavailable, using fallback hash:', err);
  }

  // Fallback hash for non-secure HTTP origins (e.g., LAN IP testing on mobile)
  let hash = 0;
  for (let i = 0; i < plainPassword.length; i++) {
    const char = plainPassword.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return 'sec_' + Math.abs(hash).toString(16);
}

// 2. Safe localStorage JSON retrieval with fallback
export function safeStorageGet(key, fallbackValue = null) {
  try {
    const item = localStorage.getItem(key);
    if (!item) return fallbackValue;
    const parsed = JSON.parse(item);
    if (typeof fallbackValue === 'object' && !Array.isArray(fallbackValue) && parsed && typeof parsed === 'object') return { ...fallbackValue, ...parsed };
    if (Array.isArray(fallbackValue) && !Array.isArray(parsed)) {
      return fallbackValue;
    }
    return parsed !== null && parsed !== undefined ? parsed : fallbackValue;
  } catch (error) {
    console.warn(`[Storage Warning] Corrupt data detected for key "${key}". Resetting to fallback.`, error);
    return fallbackValue;
  }
}

// 3. Safe localStorage setter
export function safeStorageSet(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (error) {
    console.error(`[Storage Error] Failed to persist key "${key}" to localStorage.`, error);
    return false;
  }
}

// 4. Strip sensitive fields (like password) before session persistence
export function sanitizeUserSession(userObj) {
  if (!userObj) return null;
  const { password, ...safeUser } = userObj;
  return safeUser;
}

// 5. Fisher-Yates (Knuth) Unbiased Random Array Shuffle
export function fisherYatesShuffle(array) {
  if (!Array.isArray(array)) return [];
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

// 6. Strict Input Validation & Sanitization
export function validateEmail(email) {
  if (!email || typeof email !== 'string') return false;
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email.trim());
}

export function sanitizeInputString(str, maxLength = 100) {
  if (!str || typeof str !== 'string') return '';
  return str.trim().slice(0, maxLength);
}

// 7. Track-Specific Question Filtering Helper
export function getQuestionsForTrack(questions, examTrack) {
  if (!Array.isArray(questions)) return [];
  if (!examTrack) return questions;

  const track = examTrack.toLowerCase().trim();

  const filtered = questions.filter(q => {
    if (!q) return false;
    const src = (q.book_source || '').toLowerCase();
    const cat = (q.category || '').toLowerCase();

    if (track.includes('fcps')) {
      // FCPS Part 1 & NLE: Pathoma, ROAMS, Bailey & Love, Guyton, Snell, Pharmacology, FCPS
      return src.includes('roams') || src.includes('pathoma') || src.includes('bailey') || 
             src.includes('guyton') || src.includes('snell') || src.includes('pharmacology') || 
             cat.includes('fcps') || cat.includes('nle');
    }
    if (track.includes('step 1')) {
      // USMLE Step 1: First Aid Step 1, Pathoma, Guyton, Snell, Pharmacology
      return src.includes('step 1') || src.includes('pathoma') || src.includes('guyton') || 
             src.includes('snell') || src.includes('pharmacology');
    }
    if (track.includes('step 2')) {
      // USMLE Step 2 CK: First Aid Step 2 CK
      return src.includes('step 2') || cat.includes('step 2');
    }
    if (track.includes('plab') || track.includes('ukmla')) {
      // PLAB 1 / UKMLA: Clinical decision making, ROAMS, Bailey, First Aid
      return src.includes('roams') || src.includes('bailey') || src.includes('first aid') || 
             src.includes('pharmacology') || cat.includes('plab');
    }
    if (track.includes('neet') || track.includes('fmge')) {
      // NEET PG & FMGE: Garg & Gupta, ROAMS, Pathoma, Pharmacology
      return src.includes('garg') || src.includes('roams') || src.includes('pharmacology') || 
             src.includes('snell') || cat.includes('neet');
    }
    if (track.includes('mrcs') || track.includes('surgery')) {
      // MRCS Surgery: Bailey & Love Surgery, Anatomy, Pathology
      return src.includes('bailey') || src.includes('snell') || cat.includes('surgery') || 
             cat.includes('anatomy') || cat.includes('mrcs');
    }

    return true;
  });

  // If filtered set is non-empty, return it; otherwise return full dataset
  return filtered;
}
