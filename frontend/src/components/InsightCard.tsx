import { useState } from 'react';

const TYPE_STYLES = {
  analysis: { border: '#ef4444', bg: '#fef2f2', icon: '🔬', label: 'Health Analysis' },
  diet:     { border: '#22c55e', bg: '#f0fdf4', icon: '🥗', label: 'Diet Plan' },
  comparison: { border: '#3b82f6', bg: '#eff6ff', icon: '📊', label: 'Report Comparison' },
};

interface InsightCardProps {
  type: 'analysis' | 'diet' | 'comparison';
  content: string;
  sources: string[];
  isLoading?: boolean;
}

const InsightCard = ({ type, content, sources, isLoading }: InsightCardProps) => {
  const [showSources, setShowSources] = useState(false);
  const style = TYPE_STYLES[type];

  return (
    <div style={{ border: `2px solid ${style.border}`, borderRadius: 12, padding: 20, background: style.bg, marginBottom: 16 }}>
      <h3 style={{ margin: '0 0 12px', fontSize: 18 }}>{style.icon} {style.label}</h3>

      {isLoading && !content ? (
        <p style={{ color: '#888' }}>Analyzing... ⏳</p>
      ) : content ? (
        <div style={{ fontSize: 14, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>{content}</div>
      ) : (
        <p style={{ color: '#aaa', fontStyle: 'italic' }}>No data yet.</p>
      )}

      {sources.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <button
            onClick={() => setShowSources(!showSources)}
            style={{ cursor: 'pointer', color: '#666', fontSize: 13, background: 'none', border: 'none' }}
          >
            📚 Sources ({sources.length}) {showSources ? '▲' : '▼'}
          </button>
          {showSources && (
            <ul style={{ marginTop: 8, fontSize: 12 }}>
              {sources.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default InsightCard;
