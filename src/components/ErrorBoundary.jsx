import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught application error:", error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  handleResetStorage = () => {
    if (window.confirm('This will reset corrupt cached data and reload. Your account remains intact. Continue?')) {
      const keysToRemove = ['fcps_stats', 'fcps_history', 'fcps_bookmarks'];
      keysToRemove.forEach(key => localStorage.removeItem(key));
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          background: '#0b0f19',
          color: '#f8fafc',
          fontFamily: 'system-ui, sans-serif'
        }}>
          <div style={{
            maxWidth: '500px',
            width: '100%',
            padding: '2.5rem',
            borderRadius: '14px',
            background: 'rgba(21, 28, 44, 0.95)',
            border: '1px solid rgba(244, 63, 94, 0.4)',
            textAlign: 'center',
            boxShadow: '0 10px 30px rgba(0,0,0,0.5)'
          }}>
            <div style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'rgba(244, 63, 94, 0.15)',
              color: '#f43f5e',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.8rem',
              margin: '0 auto 1.25rem'
            }}>
              ⚠️
            </div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Application Error Encountered</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.92rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
              MedPrep Pro encountered an unexpected runtime error. We have safely prevented a full application crash.
            </p>
            <div style={{
              background: 'rgba(0,0,0,0.3)',
              padding: '0.75rem',
              borderRadius: '8px',
              fontSize: '0.8rem',
              fontFamily: 'monospace',
              color: '#f43f5e',
              marginBottom: '1.5rem',
              wordBreak: 'break-all'
            }}>
              {this.state.error?.toString() || 'Unknown Error'}
            </div>
            {this.state.errorInfo && (
              <details style={{ marginBottom: '1rem', textAlign: 'left' }}>
                <summary style={{ cursor: 'pointer', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.5rem' }}>Show Technical Details</summary>
                <pre style={{
                  background: 'rgba(0,0,0,0.3)',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  fontSize: '0.72rem',
                  color: '#f43f5e',
                  overflow: 'auto',
                  maxHeight: '150px',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-all'
                }}>
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
                style={{
                  padding: '0.65rem 1.2rem',
                  borderRadius: '8px',
                  border: '1px solid rgba(6, 182, 212, 0.4)',
                  background: 'transparent',
                  color: '#06b6d4',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Try Again
              </button>
              <button
                onClick={this.handleReload}
                style={{
                  padding: '0.65rem 1.2rem',
                  borderRadius: '8px',
                  border: 'none',
                  background: '#06b6d4',
                  color: '#fff',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Reload App
              </button>
              <button
                onClick={this.handleResetStorage}
                style={{
                  padding: '0.65rem 1.2rem',
                  borderRadius: '8px',
                  border: '1px solid rgba(255,255,255,0.1)',
                  background: 'transparent',
                  color: '#94a3b8',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Clear Storage & Reset
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
