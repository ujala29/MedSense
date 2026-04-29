import { useState } from 'react';
import UploadZone from '../components/UploadZone';
import InsightCard from '../components/InsightCard';
import LanguageToggle from '../components/LanguageToggle';
import { useStreamingResponse } from '../hooks/useStreamingResponse';

const Home = () => {
  const [patientId] = useState('patient123');
  const { analysis, diet, comparison, sources, isLoading, error, startAnalysis } = useStreamingResponse();

  const handleUpload = (id: string) => {
    const language = localStorage.getItem('language') || 'en';
    startAnalysis(id, patientId, language);
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 24 }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 28, margin: 0 }}>MedSense AI</h1>
        <LanguageToggle />
      </header>

      <UploadZone onUpload={handleUpload} />

      {error && (
        <div style={{ color: 'red', padding: 12, marginTop: 16, background: '#fff0f0', borderRadius: 8 }}>
          Error: {error}
        </div>
      )}

      {(isLoading || analysis || diet || comparison) && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16, marginTop: 24 }}>
          <InsightCard type="analysis" content={analysis} sources={sources} isLoading={isLoading && !analysis} />
          <InsightCard type="diet" content={diet} sources={[]} isLoading={isLoading && !diet} />
          <InsightCard type="comparison" content={comparison} sources={[]} isLoading={isLoading && !comparison} />
        </div>
      )}
    </div>
  );
};

export default Home;
