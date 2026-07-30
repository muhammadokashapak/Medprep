import React from 'react';

export default function ToastNotification({ toasts, removeToast }) {
  if (!toasts || toasts.length === 0) return null;

  return (
    <div style={{
      position: 'fixed',
      top: '1rem',
      right: '1rem',
      zIndex: 9999,
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem',
      maxWidth: '360px',
      width: 'calc(100% - 2rem)'
    }}>
      {toasts.map(toast => {
        let bg = 'rgba(21, 28, 44, 0.95)';
        let border = 'var(--accent-cyan)';
        let icon = 'fa-info-circle';
        let color = 'var(--accent-cyan)';

        if (toast.type === 'success') {
          border = 'var(--accent-emerald)';
          icon = 'fa-circle-check';
          color = 'var(--accent-emerald)';
        } else if (toast.type === 'error') {
          border = 'var(--accent-rose)';
          icon = 'fa-circle-xmark';
          color = 'var(--accent-rose)';
        } else if (toast.type === 'warning') {
          border = 'var(--accent-amber)';
          icon = 'fa-triangle-exclamation';
          color = 'var(--accent-amber)';
        }

        return (
          <div
            key={toast.id}
            className="animate-fade-in"
            style={{
              background: bg,
              backdropFilter: 'blur(16px)',
              border: '1px solid var(--border-subtle)',
              borderLeft: `4px solid ${border}`,
              borderRadius: 'var(--radius-sm)',
              padding: '0.75rem 0.9rem',
              color: 'var(--text-main)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              boxShadow: 'var(--shadow-card)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
              <i className={`fa-solid ${icon}`} style={{ color, fontSize: '1rem', flexShrink: 0 }}></i>
              <span style={{ fontSize: '0.85rem', fontWeight: 500, lineHeight: 1.4 }}>{toast.message}</span>
            </div>

            <button
              onClick={() => removeToast(toast.id)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-subdued)',
                cursor: 'pointer',
                padding: '0.2rem',
                marginLeft: '0.5rem',
                flexShrink: 0
              }}
            >
              <i className="fa-solid fa-xmark"></i>
            </button>
          </div>
        );
      })}
    </div>
  );
}
