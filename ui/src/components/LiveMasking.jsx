import { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, RefreshCw, AlertCircle, FileText, Download, Eye } from 'lucide-react';

const LiveMasking = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progressStage, setProgressStage] = useState(0);
  const fileInputRef = useRef(null);

  const handleMaskText = async () => {
    if (!inputText.trim()) return;
    setIsLoading(true);
    setError(null);
    setProgressStage(0);
    try {
      const response = await axios.post('http://localhost:8000/api/mask/text', {
        text: inputText
      });
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Failed to process text');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setResult(null);
    setProgressStage(1);
    
    // Simulate stages progressing through the 8 processing layers
    const stageInterval = setInterval(() => {
      setProgressStage(prev => (prev < 8 ? prev + 1 : prev));
    }, 900);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/mask/file', formData);
      clearInterval(stageInterval);
      setProgressStage(9);
      setResult(response.data);
      setInputText(response.data.original_text);
    } catch (err) {
      clearInterval(stageInterval);
      setProgressStage(0);
      setError(err.message || 'Failed to process file');
    } finally {
      setIsLoading(false);
      // Reset file input
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDownloadPDF = () => {
    if (!result || !result.pdf_base64) return;
    const link = document.createElement('a');
    link.href = `data:application/pdf;base64,${result.pdf_base64}`;
    link.download = 'masked_document.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleViewPDF = () => {
    if (!result || !result.pdf_base64) return;
    
    const byteCharacters = atob(result.pdf_base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
  };

  const renderProgress = () => {
    if (progressStage === 0) return null;
    
    const stages = [
      "Document Ingestion & Upload",
      "Adaptive Pre-processing & OCR",
      "Signature-based Document Classification",
      "Hybrid Candidate Generation (Context + NER)",
      "Entity Resolution & Overlap Merging",
      "PII Decision Engine Policy Filters",
      "Coordinate-based PDF Redaction",
      "Generating Audit Logs & Explanations",
      "Process Complete!"
    ];

    const percentage = Math.round((progressStage / stages.length) * 100);

    return (
      <div style={{ marginBottom: '24px', padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-muted)' }}>
          <span>{stages[progressStage - 1]}</span>
          <span>{percentage}%</span>
        </div>
        <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
          <div style={{ 
            height: '100%', 
            width: `${percentage}%`, 
            background: 'var(--primary)',
            transition: 'width 0.3s ease'
          }} />
        </div>
      </div>
    );
  };

  const renderHighlightedText = () => {
    if (!result || !result.masked_text) return '';
    
    let html = result.masked_text;
    
    // Escape HTML to prevent XSS
    html = html.replace(/&/g, "&amp;")
               .replace(/</g, "&lt;")
               .replace(/>/g, "&gt;")
               .replace(/"/g, "&quot;")
               .replace(/'/g, "&#039;");

    // Replace the [TYPE_001] style placeholders with highlighted spans
    // e.g. [PERSON_NAME_001] -> <span class="entity-highlight" data-type="PERSON_NAME">[PERSON_NAME_001]</span>
    const regex = /\[([A-Z_]+)_\d{3}\]/g;
    html = html.replace(regex, (match, type) => {
      return `<span class="entity-highlight" data-type="${type}">${match}</span>`;
    });

    return <div dangerouslySetInnerHTML={{ __html: html }} style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }} />;
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Live Masking</h1>
        <p className="page-subtitle">Test the pipeline on raw text or document uploads</p>
      </div>

      <div style={{ display: 'flex', gap: '24px', marginBottom: '32px' }}>
        <button 
          className="btn-primary" 
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading}
        >
          <Upload size={18} />
          Upload Document
        </button>
        <input 
          id="fileUpload"
          name="fileUpload"
          type="file" 
          ref={fileInputRef} 
          style={{ display: 'none' }} 
          onChange={handleFileUpload}
          accept=".txt,.pdf"
          title="Upload document"
        />
        
        <button 
          className="btn-secondary" 
          onClick={handleMaskText}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? <RefreshCw size={18} className="animate-spin" /> : <FileText size={18} />}
          Mask Text
        </button>

        {result && result.pdf_base64 && (
          <>
            <button 
              className="btn-primary" 
              style={{ background: '#10b981', marginLeft: 'auto' }}
              onClick={handleDownloadPDF}
            >
              <Download size={18} />
              Download Masked PDF
            </button>
            <button 
              className="btn-secondary" 
              style={{ background: 'rgba(16, 185, 129, 0.2)', borderColor: '#10b981', color: '#10b981' }}
              onClick={handleViewPDF}
            >
              <Eye size={18} />
              View PDF
            </button>
          </>
        )}
      </div>

      {renderProgress()}

      {error && (
        <div style={{ padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', borderRadius: '8px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px', color: '#fca5a5' }}>
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            Original Text
          </h3>
          <textarea 
            id="inputText"
            name="inputText"
            className="glass-input glass-textarea" 
            placeholder="Paste text here or upload a document..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary-light)' }}>
            Masked Output
          </h3>
          <div className="glass-input glass-textarea" style={{ overflowY: 'auto' }}>
            {result ? renderHighlightedText() : (
              <span style={{ color: 'var(--text-muted)' }}>Masked output will appear here...</span>
            )}
          </div>
        </div>
      </div>

      {result && result.entities && result.entities.length > 0 && (
        <div className="glass-panel" style={{ padding: '24px', marginTop: '24px' }}>
          <h3 style={{ marginBottom: '16px' }}>Enterprise Audit Trail ({result.entities.length} items analyzed)</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Type</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Value</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Section</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Role</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Risk Score</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Decision</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Source</th>
                  <th style={{ padding: '12px 8px', color: 'var(--text-muted)' }}>Policy Explanation</th>
                </tr>
              </thead>
              <tbody>
                {result.entities.map((entity, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '12px 8px' }}>
                      <span className="entity-highlight" data-type={entity.type}>{entity.type}</span>
                    </td>
                    <td style={{ padding: '12px 8px', fontFamily: 'monospace' }}>{entity.value}</td>
                    <td style={{ padding: '12px 8px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>{entity.section}</td>
                    <td style={{ padding: '12px 8px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>{entity.role}</td>
                    <td style={{ padding: '12px 8px', fontWeight: 500 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <div style={{ width: '40px', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                           <div style={{
                             height: '100%', 
                             width: `${(entity.risk_score || 0) * 100}%`,
                             background: entity.risk_score >= 0.7 ? '#ef4444' : entity.risk_score >= 0.4 ? '#f59e0b' : '#10b981'
                           }} />
                        </div>
                        <span style={{ fontSize: '0.85rem' }}>{(entity.risk_score || 0).toFixed(2)}</span>
                      </div>
                    </td>
                    <td style={{ padding: '12px 8px' }}>
                      <span style={{
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        background: entity.decision.includes('MASK') ? 'rgba(239, 68, 68, 0.15)' : entity.decision.includes('REVIEW') ? 'rgba(245, 158, 11, 0.15)' : 'rgba(16, 185, 129, 0.15)',
                        color: entity.decision.includes('MASK') ? '#f87171' : entity.decision.includes('REVIEW') ? '#fbbf24' : '#34d399',
                        border: entity.decision.includes('MASK') ? '1px solid rgba(239, 68, 68, 0.3)' : entity.decision.includes('REVIEW') ? '1px solid rgba(245, 158, 11, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)'
                      }}>
                        {entity.decision}
                      </span>
                    </td>
                    <td style={{ padding: '12px 8px', color: 'var(--text-muted)', textTransform: 'capitalize', fontSize: '0.85rem' }}>
                      {entity.source} ({typeof entity.confidence === 'number' ? `${(entity.confidence * 100).toFixed(0)}%` : 'N/A'})
                    </td>
                    <td style={{ padding: '12px 8px', color: 'var(--text-light)', fontSize: '0.875rem' }}>
                      {entity.matching_reason || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default LiveMasking;
