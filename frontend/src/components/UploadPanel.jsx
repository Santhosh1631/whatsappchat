import { useState } from 'react';
import { uploadChat } from '../services/api';

function UploadPanel({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('idle');
  const [message, setMessage] = useState('Upload an exported WhatsApp .txt file');

  const handleUpload = async () => {
    if (!file) {
      setStatus('error');
      setMessage('Please select a .txt file first.');
      return;
    }

    try {
      setStatus('uploading');
      setMessage('Uploading and parsing...');
      setProgress(0);

      const result = await uploadChat(file, (evt) => {
        const total = evt.total || 1;
        setProgress(Math.round((evt.loaded * 100) / total));
      });

      setStatus('success');
      setMessage(
        `Imported ${result.insert_stats.messages_inserted} messages with ${result.parse_stats.parse_errors} parse warnings.`
      );
      onUploaded();
    } catch (error) {
      setStatus('error');
      const errMessage = error?.response?.data?.error || error.message;
      setMessage(`Upload failed: ${errMessage}`);
    }
  };

  return (
    <div className="upload-card">
      <h2>Chat Importer</h2>
      <p>{message}</p>
      <input
        type="file"
        accept=".txt,text/plain"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload} disabled={status === 'uploading'}>
        {status === 'uploading' ? 'Importing...' : 'Upload Another Chat History'}
      </button>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>
      <span className={`status-pill ${status}`}>{status.toUpperCase()}</span>
    </div>
  );
}

export default UploadPanel;
