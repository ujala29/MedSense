import { useState, useCallback } from 'react';

interface StreamingState {
  analysis: string;
  diet: string;
  comparison: string;
  sources: string[];
  isLoading: boolean;
  error: string | null;
}

export const useStreamingResponse = () => {
  const [state, setState] = useState<StreamingState>({
    analysis: '',
    diet: '',
    comparison: '',
    sources: [],
    isLoading: false,
    error: null,
  });

  const startAnalysis = useCallback(async (
    reportId: string,
    patientId: string,
    language: string = 'en'
  ) => {
    setState({ analysis: '', diet: '', comparison: '', sources: [], isLoading: true, error: null });

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ report_id: reportId, patient_id: patientId, language }),
      });

      if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data: ')) continue;

          const jsonStr = trimmed.slice(6);
          if (!jsonStr || jsonStr === '[DONE]') continue;

          try {
            const event = JSON.parse(jsonStr);
            if (event.type === 'analysis' && event.content) {
              setState(prev => ({ ...prev, analysis: prev.analysis + event.content }));
            } else if (event.type === 'diet') {
              setState(prev => ({ ...prev, diet: prev.diet + (event.content || '') }));
            } else if (event.type === 'comparison') {
              setState(prev => ({ ...prev, comparison: prev.comparison + (event.content || '') }));
            } else if (event.type === 'sources') {
              setState(prev => ({ ...prev, sources: event.sources || [] }));
            } else if (event.type === 'done') {
              setState(prev => ({ ...prev, isLoading: false }));
            } else if (event.type === 'error') {
              setState(prev => ({ ...prev, error: event.message, isLoading: false }));
            }
          } catch (parseError) {
            console.warn('SSE parse error:', parseError, 'line:', jsonStr);
          }
        }
      }
    } catch (err) {
      setState(prev => ({ ...prev, error: err instanceof Error ? err.message : 'Unknown error', isLoading: false }));
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  return { ...state, startAnalysis };
};
