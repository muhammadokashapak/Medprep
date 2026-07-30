import React, { useState } from 'react';
import { hashPassword, safeStorageGet, safeStorageSet, sanitizeUserSession, validateEmail, sanitizeInputString } from '../utils/security';

export default function AuthModal({ isOpen, onClose, onLogin, addToast }) {
  const [view, setView] = useState('login'); // 'login' | 'register' | 'forgot'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [name, setName] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [examPreference, setExamPreference] = useState('FCPS Part 1');

  if (!isOpen) return null;

  // Password strength logic
  const getPasswordStrength = (pass) => {
    if (!pass) return { score: 0, text: '', color: '' };
    let score = 0;
    if (pass.length >= 6) score++;
    if (pass.length >= 10) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;

    if (score <= 2) return { score: 33, text: 'Weak', color: 'var(--accent-rose)' };
    if (score <= 4) return { score: 66, text: 'Medium', color: 'var(--accent-amber)' };
    return { score: 100, text: 'Strong', color: 'var(--accent-emerald)' };
  };

  const strength = getPasswordStrength(password);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      addToast('Please fill in all fields', 'error');
      return;
    }

    if (!validateEmail(email)) {
      addToast('Please enter a valid email address', 'error');
      return;
    }

    setLoading(true);
    try {
      const hashedPassword = await hashPassword(password);
      const users = safeStorageGet('fcps_users', []);
      const found = users.find(u => u.email.toLowerCase() === email.trim().toLowerCase());

      if (found) {
        if (found.password === hashedPassword || found.password === password) {
          const safeUser = sanitizeUserSession(found);
          onLogin(safeUser, rememberMe);
          addToast(`Welcome back, ${safeUser.name}!`, 'success');
          onClose();
        } else {
          addToast('Incorrect password', 'error');
        }
      } else {
        addToast('No candidate account found with this email. Please register first.', 'error');
      }
    } catch (err) {
      console.error('[Auth Error]', err);
      addToast('Login failed. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    const cleanName = sanitizeInputString(name, 60);
    const cleanEmail = email.trim().toLowerCase();

    if (!cleanName || !cleanEmail || !password || !confirmPassword) {
      addToast('Please fill in all registration fields', 'error');
      return;
    }

    if (!validateEmail(cleanEmail)) {
      addToast('Please enter a valid email address', 'error');
      return;
    }

    if (password !== confirmPassword) {
      addToast('Passwords do not match', 'error');
      return;
    }

    if (password.length < 6) {
      addToast('Password must be at least 6 characters', 'error');
      return;
    }

    setLoading(true);
    try {
      const hashedPassword = await hashPassword(password);
      const users = safeStorageGet('fcps_users', []);

      if (users.some(u => u.email.toLowerCase() === cleanEmail)) {
        addToast('An account with this email address already exists', 'error');
        return;
      }

      const newUser = {
        name: cleanName,
        email: cleanEmail,
        password: hashedPassword,
        examPreference,
        joined: new Date().toLocaleDateString()
      };

      users.push(newUser);
      safeStorageSet('fcps_users', users);

      const safeUser = sanitizeUserSession(newUser);
      onLogin(safeUser, rememberMe);
      addToast('Candidate account created successfully!', 'success');
      onClose();
    } catch (err) {
      console.error('[Registration Error]', err);
      addToast('Registration failed. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotSubmit = async (e) => {
    e.preventDefault();
    if (!email || !validateEmail(email)) {
      addToast('Please enter a valid registered email address', 'error');
      return;
    }
    if (!newPassword || newPassword.length < 6) {
      addToast('New password must be at least 6 characters long', 'error');
      return;
    }

    setLoading(true);
    try {
      const hashedPassword = await hashPassword(newPassword);
      const users = safeStorageGet('fcps_users', []);
      const userIndex = users.findIndex(u => u.email.toLowerCase() === email.trim().toLowerCase());

      if (userIndex !== -1) {
        users[userIndex].password = hashedPassword;
        safeStorageSet('fcps_users', users);
        addToast(`Password updated successfully for ${email}. You can now sign in.`, 'success');
        setView('login');
      } else {
        addToast('No candidate account found matching that email address', 'error');
      }
    } catch (err) {
      console.error('[Forgot Password Error]', err);
      addToast('Failed to reset password. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1000,
      background: 'rgba(11, 15, 25, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1.5rem'
    }}>
      <div className="glass-panel animate-fade-in" style={{
        maxWidth: '460px',
        width: '100%',
        padding: '1.5rem',
        position: 'relative',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-glow)',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '1.25rem',
            right: '1.25rem',
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            fontSize: '1.2rem'
          }}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>

        {/* Brand Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '50px',
            height: '50px',
            borderRadius: '14px',
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            margin: '0 auto 1rem',
            boxShadow: 'var(--shadow-glow)'
          }}>
            <i className="fa-solid fa-user-doctor" style={{ fontSize: '1.5rem' }}></i>
          </div>
          <h2 style={{ fontSize: '1.6rem' }} className="gradient-text">
            {view === 'login' && 'Medical Portal Sign In'}
            {view === 'register' && 'Create Candidate Account'}
            {view === 'forgot' && 'Reset Password'}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            {view === 'login' && 'Access your FCPS Part 1 QBank & Mock History'}
            {view === 'register' && 'Join thousands of doctors preparing for FCPS Part 1'}
            {view === 'forgot' && 'Enter your email to receive password recovery steps'}
          </p>
        </div>

        {/* LOGIN FORM */}
        {view === 'login' && (
          <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Email Address
              </label>
              <input
                type="email"
                placeholder="dr.name@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Password</label>
                <span
                  onClick={() => setView('forgot')}
                  style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', cursor: 'pointer', fontWeight: 500 }}
                >
                  Forgot password?
                </span>
              </div>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '0.8rem 2.8rem 0.8rem 1rem',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-subtle)',
                    background: 'rgba(255,255,255,0.04)',
                    color: 'var(--text-main)',
                    outline: 'none'
                  }}
                />
                <i
                  className={`fa-solid ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '1rem',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: 'var(--text-muted)',
                    cursor: 'pointer'
                  }}
                ></i>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
              <input
                type="checkbox"
                id="remember"
                checked={rememberMe}
                onChange={e => setRememberMe(e.target.checked)}
                style={{ cursor: 'pointer', accentColor: 'var(--accent-cyan)' }}
              />
              <label htmlFor="remember" style={{ cursor: 'pointer' }}>Keep me logged in on this device</label>
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ justifyContent: 'center', marginTop: '0.5rem' }}>
              {loading ? <i className="fa-solid fa-circle-notch fa-spin"></i> : <i className="fa-solid fa-right-to-bracket"></i>}
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>

            <div style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Don't have an account?{' '}
              <span onClick={() => setView('register')} style={{ color: 'var(--accent-cyan)', fontWeight: 600, cursor: 'pointer' }}>
                Create one now
              </span>
            </div>
          </form>
        )}

        {/* REGISTER FORM */}
        {view === 'register' && (
          <form onSubmit={handleRegisterSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Full Name & Title
              </label>
              <input
                type="text"
                placeholder="Dr. Ahmed Khan"
                value={name}
                onChange={e => setName(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Email Address
              </label>
              <input
                type="email"
                placeholder="dr.ahmed@hospital.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Target Medical Examination
              </label>
              <select
                value={examPreference}
                onChange={e => setExamPreference(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-glow)',
                  background: '#0f172a',
                  color: '#ffffff',
                  outline: 'none',
                  cursor: 'pointer',
                  fontSize: '0.95rem',
                  fontWeight: 600
                }}
              >
                <option value="FCPS Part 1" style={{ background: '#0f172a', color: '#ffffff' }}>FCPS Part 1 (Pakistan)</option>
                <option value="USMLE Step 1" style={{ background: '#0f172a', color: '#ffffff' }}>USMLE Step 1 (USA)</option>
                <option value="USMLE Step 2 CK" style={{ background: '#0f172a', color: '#ffffff' }}>USMLE Step 2 CK (USA)</option>
                <option value="PLAB / UKMLA" style={{ background: '#0f172a', color: '#ffffff' }}>PLAB / UKMLA (UK)</option>
                <option value="NEET PG" style={{ background: '#0f172a', color: '#ffffff' }}>NEET PG / INI-CET (India)</option>
                <option value="MRCS Surgery" style={{ background: '#0f172a', color: '#ffffff' }}>MRCS Part A Surgery (UK/Intl)</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Password
              </label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
              {password && (
                <div style={{ marginTop: '0.4rem' }}>
                  <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '99px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${strength.score}%`, background: strength.color, transition: 'all 0.3s' }}></div>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: strength.color, fontWeight: 600, marginTop: '0.2rem', display: 'block' }}>
                    Password Strength: {strength.text}
                  </span>
                </div>
              )}
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Confirm Password
              </label>
              <input
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ justifyContent: 'center', marginTop: '0.5rem' }}>
              {loading ? <i className="fa-solid fa-circle-notch fa-spin"></i> : <i className="fa-solid fa-user-plus"></i>}
              {loading ? 'Registering...' : 'Register Account'}
            </button>

            <div style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Already registered?{' '}
              <span onClick={() => setView('login')} style={{ color: 'var(--accent-cyan)', fontWeight: 600, cursor: 'pointer' }}>
                Sign in here
              </span>
            </div>
          </form>
        )}

        {/* FORGOT PASSWORD FORM */}
        {view === 'forgot' && (
          <form onSubmit={handleForgotSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Registered Email Address
              </label>
              <input
                type="email"
                placeholder="dr.name@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Enter New Password
              </label>
              <input
                type="password"
                placeholder="••••••••"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                required
                minLength={6}
                style={{
                  width: '100%',
                  padding: '0.8rem 1rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'var(--text-main)',
                  outline: 'none'
                }}
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ justifyContent: 'center', marginTop: '0.5rem' }}>
              {loading ? <i className="fa-solid fa-circle-notch fa-spin"></i> : <i className="fa-solid fa-key"></i>}
              {loading ? 'Updating Password...' : 'Reset Account Password'}
            </button>

            <div style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              <span onClick={() => setView('login')} style={{ color: 'var(--accent-cyan)', fontWeight: 600, cursor: 'pointer' }}>
                Back to Sign In
              </span>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
