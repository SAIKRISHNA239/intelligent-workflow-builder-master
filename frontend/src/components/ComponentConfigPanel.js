import React, { useState, useEffect } from 'react';
import './ComponentConfigPanel.css';
import { documentAPI } from '../services/api';

function ComponentConfigPanel({ node, onConfigUpdate, onClose }) {
  const [config, setConfig] = useState(node.data.config || {});
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (node.type === 'knowledgebase') {
      loadDocuments();
    }
  }, [node]);

  const loadDocuments = async () => {
    try {
      const response = await documentAPI.list(node.id);
      setDocuments(response.data);
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const handleConfigChange = (key, value) => {
    const newConfig = { ...config, [key]: value };
    setConfig(newConfig);
    onConfigUpdate(node.id, newConfig);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      await documentAPI.upload(file, node.id);
      await loadDocuments();
      alert('Document uploaded successfully!');
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document: ' + (error.response?.data?.detail || error.message));
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const renderConfigFields = () => {
    if (node.type === 'user_query') {
      return (
        <div className="config-section">
          <p>User Query component accepts user input and passes it to connected components.</p>
        </div>
      );
    }

    if (node.type === 'knowledgebase') {
      return (
        <div className="config-section">
          <div className="config-field">
            <label>Collection Name</label>
            <input
              type="text"
              value={config.collection_name || 'documents'}
              onChange={(e) => handleConfigChange('collection_name', e.target.value)}
            />
          </div>
          <div className="config-field">
            <label>Number of Results</label>
            <input
              type="number"
              min="1"
              max="20"
              value={config.n_results || 5}
              onChange={(e) => handleConfigChange('n_results', parseInt(e.target.value))}
            />
          </div>
          <div className="config-field">
            <label>Embedding Provider</label>
            <select
              value={config.embedding_provider || 'openai'}
              onChange={(e) => handleConfigChange('embedding_provider', e.target.value)}
            >
              <option value="openai">OpenAI</option>
              <option value="gemini">Gemini</option>
            </select>
          </div>
          <div className="config-field">
            <label>Upload Documents</label>
            <input
              type="file"
              accept=".pdf,.txt,.doc,.docx"
              onChange={handleFileUpload}
              disabled={uploading}
            />
            {uploading && <p className="upload-status">Uploading...</p>}
          </div>
          {documents.length > 0 && (
            <div className="config-field">
              <label>Uploaded Documents ({documents.length})</label>
              <div className="document-list">
                {documents.map((doc) => (
                  <div key={doc.id} className="document-item">
                    <span>{doc.filename}</span>
                    <span className={`status-badge ${doc.processed}`}>
                      {doc.processed}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }

    if (node.type === 'llm_engine') {
      return (
        <div className="config-section">
          <div className="config-field">
            <label>Provider</label>
            <select
              value={config.provider || 'openai'}
              onChange={(e) => handleConfigChange('provider', e.target.value)}
            >
              <option value="openai">OpenAI</option>
              <option value="gemini">Gemini</option>
            </select>
          </div>
          <div className="config-field">
            <label>Model</label>
            <input
              type="text"
              value={config.model || (config.provider === 'gemini' ? 'gemini-pro' : 'gpt-3.5-turbo')}
              onChange={(e) => handleConfigChange('model', e.target.value)}
              placeholder={config.provider === 'gemini' ? 'gemini-pro' : 'gpt-3.5-turbo'}
            />
          </div>
          <div className="config-field">
            <label>Temperature</label>
            <input
              type="number"
              min="0"
              max="2"
              step="0.1"
              value={config.temperature || 0.7}
              onChange={(e) => handleConfigChange('temperature', parseFloat(e.target.value))}
            />
          </div>
          <div className="config-field">
            <label>Max Tokens</label>
            <input
              type="number"
              min="1"
              max="4000"
              value={config.max_tokens || 1000}
              onChange={(e) => handleConfigChange('max_tokens', parseInt(e.target.value))}
            />
          </div>
          <div className="config-field">
            <label>
              <input
                type="checkbox"
                checked={config.use_web_search || false}
                onChange={(e) => handleConfigChange('use_web_search', e.target.checked)}
              />
              Use Web Search (SerpAPI)
            </label>
          </div>
          <div className="config-field">
            <label>System Prompt (Optional)</label>
            <textarea
              value={config.system_prompt || ''}
              onChange={(e) => handleConfigChange('system_prompt', e.target.value)}
              rows="4"
              placeholder="Enter custom system prompt..."
            />
          </div>
        </div>
      );
    }

    if (node.type === 'output') {
      return (
        <div className="config-section">
          <p>Output component displays the final response to the user in the chat interface.</p>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="config-panel">
      <div className="config-panel-header">
        <h3>Configure {node.data.label}</h3>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      <div className="config-panel-content">
        {renderConfigFields()}
      </div>
    </div>
  );
}

export default ComponentConfigPanel;

