import React, { useState, useMemo, useEffect } from 'react';

export default function QBankExplorer({ questions = [], bookmarks = {}, toggleBookmark, addToast }) {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [showBookmarksOnly, setShowBookmarksOnly] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [page, setPage] = useState(1);
  const pageSize = 20;

  // Extract categories
  const categories = useMemo(() => {
    const set = new Set();
    questions.forEach(q => {
      const cat = (q.category || '').split('-')[0].trim();
      set.add(cat);
    });
    return Array.from(set).sort();
  }, [questions]);

  // Filtered list
  const filtered = useMemo(() => {
    return questions.filter(q => {
      const matchBookmark = !showBookmarksOnly || !!(bookmarks?.[q.id]);
      const matchCat = selectedCategory === 'ALL' || (q.category && q.category.toLowerCase().includes(selectedCategory.toLowerCase()));
      const matchQuery = !search.trim() || 
        (q.question || '').toLowerCase().includes(search.toLowerCase()) || 
        (q.explanation && q.explanation.toLowerCase().includes(search.toLowerCase())) ||
        (q.category || '').toLowerCase().includes(search.toLowerCase());
      return matchBookmark && matchCat && matchQuery;
    });
  }, [questions, selectedCategory, search, showBookmarksOnly, bookmarks]);

  const paginated = useMemo(() => {
    const start = (page - 1) * pageSize;
    return filtered.slice(start, start + pageSize);
  }, [filtered, page]);

  const totalPages = Math.ceil(filtered.length / pageSize);

  useEffect(() => {
    if (page > totalPages && totalPages > 0) setPage(1);
  }, [totalPages, page]);

  const copyExplanation = (text) => {
    navigator.clipboard.writeText(text);
    addToast('Explanation copied to clipboard', 'info');
  };

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      {/* Search & Filter Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>QBank Catalog Explorer</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
          Instantly search through all 3,967 FCPS & MBBS clinical questions, categories, and explanations.
        </p>

        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {/* Search bar */}
          <div style={{ flex: 1, minWidth: '280px', position: 'relative' }}>
            <i className="fa-solid fa-magnifying-glass" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}></i>
            <input
              type="text"
              placeholder="Search by topic, symptom, diagnosis, or keyword (e.g. Posterior Triangle, Nerve, Stab wound)..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              style={{
                width: '100%',
                padding: '0.85rem 1rem 0.85rem 2.8rem',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
                background: 'var(--bg-card)',
                color: 'var(--text-main)',
                fontSize: '0.95rem',
                outline: 'none'
              }}
            />
          </div>

          {/* Category Dropdown */}
          <select
            value={selectedCategory}
            onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}
            style={{
              padding: '0.85rem 1.25rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              background: 'var(--bg-card)',
              color: 'var(--text-main)',
              fontSize: '0.95rem',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            <option value="ALL">All Subjects ({categories.length})</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          {/* Bookmark filter toggle */}
          <button
            className="btn-secondary"
            onClick={() => { setShowBookmarksOnly(!showBookmarksOnly); setPage(1); }}
            style={{
              background: showBookmarksOnly ? 'rgba(245, 158, 11, 0.2)' : 'var(--bg-card)',
              color: showBookmarksOnly ? 'var(--accent-amber)' : 'var(--text-main)',
              borderColor: showBookmarksOnly ? 'var(--accent-amber)' : 'var(--border-subtle)'
            }}
          >
            <i className="fa-solid fa-bookmark"></i> {showBookmarksOnly ? 'All Questions' : 'Saved Bookmarks'}
          </button>
        </div>
      </div>

      {/* Result Stats */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
        <span>Showing {filtered.length.toLocaleString()} matching questions</span>
        <span>Page {page} of {totalPages || 1}</span>
      </div>

      {/* Questions List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '2rem' }}>
        {paginated.map((q) => {
          const isExpanded = expandedId === q.id;
          const isBookmarked = !!bookmarks[q.id];

          return (
            <div key={q.id} className="glass-panel" style={{ padding: '1.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
                <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.12)', color: 'var(--accent-cyan)', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                  <i className="fa-solid fa-file-medical" style={{ marginRight: '0.35rem' }}></i> QBank Question
                </span>
                
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-subdued)', fontWeight: 600 }}>MCQ #{q.id}</span>
                  
                  <button
                    onClick={() => toggleBookmark(q.id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: isBookmarked ? 'var(--accent-amber)' : 'var(--text-subdued)',
                      cursor: 'pointer',
                      fontSize: '1.1rem'
                    }}
                    title={isBookmarked ? 'Remove Bookmark' : 'Save Bookmark'}
                  >
                    <i className={`fa-${isBookmarked ? 'solid' : 'regular'} fa-bookmark`}></i>
                  </button>
                </div>
              </div>

              <h4 style={{ fontSize: '1.1rem', lineHeight: 1.5, marginBottom: '1.25rem' }}>{q.question}</h4>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.65rem', marginBottom: '1rem' }}>
                {['A', 'B', 'C', 'D', 'E'].map(letter => {
                  const optText = q[`option_${letter.toLowerCase()}`];
                  if (!optText) return null;
                  const isCorrect = letter.toUpperCase() === String(q.correct_answer || '').toUpperCase();
                  return (
                    <div
                      key={letter}
                      style={{
                        padding: '0.65rem 0.85rem',
                        borderRadius: 'var(--radius-sm)',
                        background: isCorrect && isExpanded ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255,255,255,0.04)',
                        border: isCorrect && isExpanded ? '1px solid var(--accent-emerald)' : '1px solid var(--border-subtle)',
                        fontSize: '0.9rem',
                        color: isCorrect && isExpanded ? 'var(--accent-emerald)' : 'var(--text-main)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.6rem'
                      }}
                    >
                      <strong style={{ opacity: 0.7 }}>{letter}.</strong> {optText}
                    </div>
                  );
                })}
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
                <button
                  onClick={() => setExpandedId(isExpanded ? null : q.id)}
                  className="btn-secondary"
                  style={{ padding: '0.4rem 0.85rem', fontSize: '0.85rem' }}
                >
                  <i className={`fa-solid ${isExpanded ? 'fa-chevron-up' : 'fa-lightbulb'}`} style={{ color: 'var(--accent-cyan)' }}></i>
                  {isExpanded ? 'Hide Answer & Explanation' : 'Reveal Answer & Explanation'}
                </button>
              </div>

              {isExpanded && (
                <div className="animate-fade-in" style={{
                  marginTop: '1.25rem',
                  padding: '1.25rem',
                  borderRadius: 'var(--radius-sm)',
                  background: 'rgba(6, 182, 212, 0.08)',
                  borderLeft: '4px solid var(--accent-cyan)',
                  position: 'relative'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                    <div style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>
                      Correct Answer: Option {q.correct_answer.toUpperCase()}
                    </div>
                    {q.explanation && (
                      <button
                        onClick={() => copyExplanation(q.explanation)}
                        style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '0.85rem' }}
                        title="Copy explanation"
                      >
                        <i className="fa-regular fa-copy"></i> Copy
                      </button>
                    )}
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: 1.6 }}>
                    {q.explanation || 'Detailed clinical vignette explanation.'}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', alignItems: 'center' }}>
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
