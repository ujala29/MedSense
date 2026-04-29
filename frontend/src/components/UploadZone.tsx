import { useState } from 'react';

const UploadZone = ({ onUpload }: { onUpload: (reportId: string) => void }) => {
  const [file, setFile] = useState<File | null>(null);
  const [patientId, setPatientId] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [language, setLanguage] = useState('en');

  const handleSubmit = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', patientId);
    formData.append('age', age);
    formData.append('gender', gender);
    formData.append('language', language);
    const res = await fetch('/upload', { method: 'POST', body: formData });
    const data = await res.json();
    onUpload(data.report_id);
  };

  return (
    <div className="border-2 border-dashed p-8 text-center">
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <div className="mt-4">
        <input placeholder="Patient ID" value={patientId} onChange={(e) => setPatientId(e.target.value)} />
        <input placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} />
        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option>Male</option>
          <option>Female</option>
        </select>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="en">English</option>
          <option value="hi">Hindi</option>
        </select>
      </div>
      <button onClick={handleSubmit} className="mt-4 bg-blue-500 text-white p-2">Upload</button>
    </div>
  );
};

export default UploadZone;