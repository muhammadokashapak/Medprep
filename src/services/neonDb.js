import { neon } from '@neondatabase/serverless';
import { hashPassword, safeStorageGet, safeStorageSet, sanitizeUserSession } from '../utils/security';

// Retrieve Neon connection string from environment variables or local storage configuration
export function getNeonUrl() {
  return import.meta.env.VITE_NEON_DATABASE_URL || localStorage.getItem('medprep_neon_url') || '';
}

export function isNeonConfigured() {
  const url = getNeonUrl();
  return typeof url === 'string' && url.trim().length > 10 && url.includes('neon.tech');
}

function getSql() {
  const url = getNeonUrl();
  if (!url) return null;
  return neon(url);
}

// Auto-initialize Neon PostgreSQL tables
export async function initNeonTables() {
  const sql = getSql();
  if (!sql) return false;

  try {
    // 1. Users Table
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        exam_preference VARCHAR(100) DEFAULT 'FCPS Part 1',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // 2. User Stats Table
    await sql`
      CREATE TABLE IF NOT EXISTS user_stats (
        email VARCHAR(255) PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
        attempted_count INT DEFAULT 0,
        correct_count INT DEFAULT 0,
        mistakes_count INT DEFAULT 0,
        mistakes_list JSONB DEFAULT '[]'::jsonb,
        today_attempted_count INT DEFAULT 0,
        last_reset_date VARCHAR(50) DEFAULT '',
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // 3. User History Table
    await sql`
      CREATE TABLE IF NOT EXISTS user_history (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
        title VARCHAR(255),
        exam_track VARCHAR(100),
        score_percentage INT,
        accuracy_percentage INT,
        attempted_count INT,
        total_questions INT,
        time_taken VARCHAR(50),
        details JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `;

    console.log('✅ Neon PostgreSQL tables initialized successfully!');
    return true;
  } catch (err) {
    console.error('❌ Error initializing Neon tables:', err);
    return false;
  }
}

// Register user permanently on Neon PostgreSQL
export async function registerUserNeon({ name, email, password, examPreference }) {
  const sql = getSql();
  const cleanEmail = email.trim().toLowerCase();
  const hashedPassword = await hashPassword(password);

  if (sql) {
    try {
      await initNeonTables();

      // Check if user already exists
      const existing = await sql`SELECT email FROM users WHERE LOWER(email) = ${cleanEmail}`;
      if (existing && existing.length > 0) {
        throw new Error('An account with this email address already exists on Neon.');
      }

      // Insert new user
      const result = await sql`
        INSERT INTO users (name, email, password, exam_preference)
        VALUES (${name}, ${cleanEmail}, ${hashedPassword}, ${examPreference || 'FCPS Part 1'})
        RETURNING name, email, exam_preference, created_at
      `;

      // Initialize stats row
      await sql`
        INSERT INTO user_stats (email, attempted_count, correct_count, mistakes_count, mistakes_list, today_attempted_count, last_reset_date)
        VALUES (${cleanEmail}, 0, 0, 0, '[]'::jsonb, 0, '')
        ON CONFLICT (email) DO NOTHING
      `;

      const newUser = result[0];
      return {
        name: newUser.name,
        email: newUser.email,
        examPreference: newUser.exam_preference,
        joined: new Date(newUser.created_at).toLocaleDateString()
      };
    } catch (err) {
      console.error('Neon Registration Error:', err);
      throw err;
    }
  }

  // LocalStorage Fallback if Neon is not configured yet
  const rawUsers = safeStorageGet('fcps_users', []);
  const users = Array.isArray(rawUsers) ? rawUsers : [];
  if (users.some(u => u && u.email && u.email.toLowerCase() === cleanEmail)) {
    throw new Error('An account with this email address already exists.');
  }

  const newUser = {
    name,
    email: cleanEmail,
    password: hashedPassword,
    examPreference: examPreference || 'FCPS Part 1',
    joined: new Date().toLocaleDateString()
  };
  users.push(newUser);
  safeStorageSet('fcps_users', users);
  return sanitizeUserSession(newUser);
}

// Login user permanently against Neon PostgreSQL
export async function loginUserNeon({ email, password }) {
  const sql = getSql();
  const cleanEmail = email.trim().toLowerCase();
  const hashedPassword = await hashPassword(password);

  if (sql) {
    try {
      await initNeonTables();

      const users = await sql`
        SELECT name, email, password, exam_preference, created_at
        FROM users
        WHERE LOWER(email) = ${cleanEmail}
      `;

      if (!users || users.length === 0) {
        throw new Error('No candidate account found with this email.');
      }

      const user = users[0];
      if (user.password !== hashedPassword) {
        throw new Error('Incorrect password.');
      }

      // Fetch user stats from Neon
      const statsRows = await sql`SELECT * FROM user_stats WHERE email = ${cleanEmail}`;
      let statsData = { attemptedCount: 0, correctCount: 0, mistakesCount: 0, mistakesList: [], todayAttemptedCount: 0, lastResetDate: '' };
      if (statsRows && statsRows.length > 0) {
        const row = statsRows[0];
        statsData = {
          attemptedCount: row.attempted_count || 0,
          correctCount: row.correct_count || 0,
          mistakesCount: row.mistakes_count || 0,
          mistakesList: Array.isArray(row.mistakes_list) ? row.mistakes_list : [],
          todayAttemptedCount: row.today_attempted_count || 0,
          lastResetDate: row.last_reset_date || ''
        };
      }

      // Fetch user history from Neon
      const historyRows = await sql`
        SELECT title, exam_track, score_percentage, accuracy_percentage, attempted_count, total_questions, time_taken, details, created_at
        FROM user_history
        WHERE email = ${cleanEmail}
        ORDER BY created_at DESC
        LIMIT 50
      `;

      const historyData = (historyRows || []).map(h => ({
        title: h.title,
        examTrack: h.exam_track,
        scorePercentage: h.score_percentage,
        accuracyPercentage: h.accuracy_percentage,
        attemptedCount: h.attempted_count,
        totalQuestions: h.total_questions,
        timeTaken: h.time_taken,
        details: Array.isArray(h.details) ? h.details : [],
        date: new Date(h.created_at).toLocaleDateString()
      }));

      return {
        user: {
          name: user.name,
          email: user.email,
          examPreference: user.exam_preference,
          joined: new Date(user.created_at).toLocaleDateString()
        },
        stats: statsData,
        history: historyData
      };
    } catch (err) {
      console.error('Neon Login Error:', err);
      throw err;
    }
  }

  // LocalStorage Fallback
  const rawUsers = safeStorageGet('fcps_users', []);
  const users = Array.isArray(rawUsers) ? rawUsers : [];
  const found = users.find(u => u && u.email && u.email.toLowerCase() === cleanEmail);

  if (!found) throw new Error('No candidate account found with this email.');
  if (found.password !== hashedPassword) throw new Error('Incorrect password.');

  const safeUser = sanitizeUserSession(found);
  return { user: safeUser, stats: null, history: null };
}

// Sync stats to Neon PostgreSQL
export async function syncStatsNeon(email, stats) {
  const sql = getSql();
  if (!sql || !email) return;

  try {
    const cleanEmail = email.trim().toLowerCase();
    const mistakesJson = JSON.stringify(stats.mistakesList || []);

    await sql`
      INSERT INTO user_stats (email, attempted_count, correct_count, mistakes_count, mistakes_list, today_attempted_count, last_reset_date, updated_at)
      VALUES (${cleanEmail}, ${stats.attemptedCount || 0}, ${stats.correctCount || 0}, ${stats.mistakesCount || 0}, ${mistakesJson}::jsonb, ${stats.todayAttemptedCount || 0}, ${stats.lastResetDate || ''}, CURRENT_TIMESTAMP)
      ON CONFLICT (email) DO UPDATE SET
        attempted_count = EXCLUDED.attempted_count,
        correct_count = EXCLUDED.correct_count,
        mistakes_count = EXCLUDED.mistakes_count,
        mistakes_list = EXCLUDED.mistakes_list,
        today_attempted_count = EXCLUDED.today_attempted_count,
        last_reset_date = EXCLUDED.last_reset_date,
        updated_at = CURRENT_TIMESTAMP;
    `;
  } catch (err) {
    console.error('Neon Sync Stats Error:', err);
  }
}

// Save Exam Result to Neon PostgreSQL
export async function saveExamResultNeon(email, examResult) {
  const sql = getSql();
  if (!sql || !email) return;

  try {
    const cleanEmail = email.trim().toLowerCase();
    const detailsJson = JSON.stringify(examResult.details || []);

    await sql`
      INSERT INTO user_history (
        email, title, exam_track, score_percentage, accuracy_percentage,
        attempted_count, total_questions, time_taken, details
      ) VALUES (
        ${cleanEmail},
        ${examResult.title || 'Practice Exam'},
        ${examResult.examTrack || 'FCPS Part 1'},
        ${examResult.scorePercentage || 0},
        ${examResult.accuracyPercentage || 0},
        ${examResult.attemptedCount || 0},
        ${examResult.totalQuestions || 0},
        ${examResult.timeTaken || ''},
        ${detailsJson}::jsonb
      );
    `;
  } catch (err) {
    console.error('Neon Save Exam History Error:', err);
  }
}
