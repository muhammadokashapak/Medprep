import React, { useState, useMemo, useEffect } from 'react';

export default function MistakesBank({ mistakesList, startMistakesQuiz, clearMistakes, removeSingleMistake }) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 20;

  // Extract categories with counts
  const categoriesMap = useMemo(() => {
    if (!mistakesList) return {};
    const map = {};
    mistakesList.forEach(m => {
      const cat = m.category || 'General';
      map[cat] = (map[cat] || 0) + 1;
    });
    return map;
  }, [mistakesList]);

  // Filtered mistakes
  const filteredMistakes = useMemo(() => {
    if (!mistakesList) return [];
    return mistakesList.filter(m => {
      const matchesCat = selectedCategory === 'all' || (m.category || 'General') === selectedCategory;
      const matchesSearch = !searchTerm || 
        (m.question || '').toLowerCase().includes(searchTerm.toLowerCase()) || 
        (m.category || '').toLowerCase().includes(searchTerm.toLowerCase());
      return matchesCat && matchesSearch;
    });
  }, [mistakesList, selectedCategory, searchTerm]);

  useEffect(() => {
    setPage(1);
  }, [selectedCategory, searchTerm]);

  const paginatedMistakes = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return filteredMistakes.slice(start, start + PAGE_SIZE);
  }, [filteredMistakes, page]);
  
  const totalPages = Math.ceil(filteredMistakes.length / PAGE_SIZE);

  if (!mistakesList || mistakesList.length === 0) {
    return (
      <div className="animate-fade-in" style={{ padding: '2rem 0', maxWidth: '800px', margin: '0 auto' }}>
        <div className="glass-panel text-center" style={{ padding: '2.5rem 1.25rem' }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            background: 'rgba(16, 185, 129, 0.15)',
            color: 'var(--accent-emerald)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2rem',
            margin: '0 auto 1.25rem'
          }}>
            <i className="fa-solid fa-circle-check"></i>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '0.65rem', fontWeight: 800 }}>
            Mistakes Bank is Empty!
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '520px', margin: '0 auto 1.5rem', lineHeight: 1.5 }}>
            You currently have no unreviewed mistakes stored. Any incorrect question from board practice tests will automatically be logged here.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '1.25rem 0' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{
        padding: '1.5rem 1.25rem',
        marginBottom: '1.5rem',
        background: 'linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(168, 85, 247, 0.1) 100%)',
        border: '1px solid rgba(244, 63, 94, 0.25)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div>
          <div className="badge" style={{ background: 'rgba(244, 63, 94, 0.15)', color: 'var(--accent-rose)', borderColor: 'rgba(244, 63, 94, 0.3)', marginBottom: '0.5rem', fontSize: '0.78rem' }}>
            <i className="fa-solid fa-brain"></i> Spaced Repetition Bank
          </div>
          <h1 style={{ fontSize: '1.65rem', marginBottom: '0.35rem', fontWeight: 800 }}>
            Review Queue ({mistakesList.length})
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
            Review clinical vignettes you missed during prior attempts
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', width: '100%', maxWidth: '320px' }}>
          <button className="btn-primary" onClick={startMistakesQuiz} style={{ flex: 1, padding: '0.65rem 1rem', fontSize: '0.88rem', minHeight: '40px', justifyContent: 'center' }}>
            <i className="fa-solid fa-play"></i> Practice ({mistakesList.length})
          </button>
          <button className="btn-secondary" onClick={() => {
            if (window.confirm('Are you sure you want to clear your entire Mistakes Bank? This cannot be undone.')) {
              clearMistakes();
            }
          }} style={{ color: 'var(--accent-rose)', borderColor: 'rgba(244, 63, 94, 0.3)', padding: '0.65rem 1rem', fontSize: '0.88rem', minHeight: '40px', width: 'auto' }}>
            <i className="fa-solid fa-trash"></i> Reset
          </button>
        </div>
      </div>

      {/* Controls Bar: Search & Category Chips */}
      <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ marginBottom: '0.85rem' }}>
          <div style={{ position: 'relative' }}>
            <i className="fa-solid fa-search" style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}></i>
            <input
              type="text"
              placeholder="Search mistakes by keyword..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem 0.65rem 2.4rem',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
                background: 'rgba(255,255,255,0.03)',
                color: 'var(--text-main)',
                outline: 'none',
                fontSize: '0.88rem'
              }}
            />
          </div>
        </div>

        {/* Category Chips Filter */}
        <div style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', paddingBottom: '0.2rem' }}>
          <button
            onClick={() => setSelectedCategory('all')}
            style={{
              padding: '0.3rem 0.75rem',
              borderRadius: 'var(--radius-full)',
              border: `1px solid ${selectedCategory === 'all' ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
              background: selectedCategory === 'all' ? 'rgba(6, 182, 212, 0.18)' : 'rgba(255,255,255,0.03)',
              color: selectedCategory === 'all' ? 'var(--accent-cyan)' : 'var(--text-muted)',
              fontSize: '0.78rem',
              fontWeight: 600,
              cursor: 'pointer',
              whiteSpace: 'nowrap'
            }}
          >
            All ({mistakesList.length})
          </button>

          {Object.entries(categoriesMap).map(([cat, count]) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              style={{
                padding: '0.3rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                border: `1px solid ${selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
                background: selectedCategory === cat ? 'rgba(6, 182, 212, 0.18)' : 'rgba(255,255,255,0.03)',
                color: selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--text-muted)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              {cat} ({count})
            </button>
          ))}
        </div>
      </div>

      {/* Filtered Mistakes Cards List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredMistakes.length === 0 && mistakesList.length > 0 && (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
            No mistakes match your search.
          </div>
        )}
        {paginatedMistakes.map((item, idx) => (
          <div
            key={item.id || idx}
            className="glass-panel"
            style={{ padding: '1.25rem', borderLeft: '4px solid var(--accent-rose)' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
              <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.12)', color: 'var(--accent-cyan)', fontSize: '0.75rem' }}>
                {item.category}
              </span>
              <button
                onClick={() => removeSingleMistake && removeSingleMistake(item.id)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-subdued)',
                  cursor: 'pointer',
                  fontSize: '0.82rem'
                }}
                title="Remove from Mistakes Bank"
              >
                <i className="fa-solid fa-xmark"></i> Remove
              </button>
            </div>

            <h3 style={{ fontSize: '0.98rem', fontWeight: 500, lineHeight: 1.5, marginBottom: '1rem', color: 'var(--text-main)' }}>
              {item.question}
            </h3>

            {item.explanation && (
              <div style={{
                padding: '0.85rem 1rem',
                background: 'rgba(255, 255, 255, 0.02)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
                fontSize: '0.88rem',
                lineHeight: 1.5
              }}>
                <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '0.25rem' }}>
                  <i className="fa-solid fa-lightbulb"></i> Clinical Explanation ({item.correct_answer}):
                </strong>
                {item.explanation}
              </div>
            )}
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', alignItems: 'center', marginTop: '1.5rem' }}>
          <button className="btn-secondary" disabled={page === 1} onClick={() => setPage(p => p - 1)}>
            <i className="fa-solid fa-chevron-left"></i> Prev
          </button>
          <span style={{ padding: '0 1rem', fontSize: '0.95rem', color: 'var(--text-muted)' }}>
            Page {page} of {totalPages}
          </span>
          <button className="btn-secondary" disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>
            Next <i className="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      )}
    </div>
  );
}
