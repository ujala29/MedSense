import { useState, useEffect } from 'react';

const LanguageToggle = () => {
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  return (
    <button onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}>
      {language === 'en' ? 'English' : 'हिंदी'}
    </button>
  );
};

export default LanguageToggle;