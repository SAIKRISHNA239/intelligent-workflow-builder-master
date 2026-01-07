import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Workflow APIs
export const workflowAPI = {
  create: (data) => api.post('/api/workflows', data),
  list: () => api.get('/api/workflows'),
  get: (id) => api.get(`/api/workflows/${id}`),
  update: (id, data) => api.put(`/api/workflows/${id}`, data),
  delete: (id) => api.delete(`/api/workflows/${id}`),
  validate: (id) => api.post(`/api/workflows/${id}/validate`),
  execute: (id, query) => api.post(`/api/workflows/${id}/execute`, { query, workflow_id: id }),
};

// Document APIs
export const documentAPI = {
  upload: (file, knowledgebaseId) => {
    const formData = new FormData();
    formData.append('file', file);
    if (knowledgebaseId) {
      formData.append('knowledgebase_id', knowledgebaseId);
    }
    return api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  list: (knowledgebaseId) => {
    const params = knowledgebaseId ? { knowledgebase_id: knowledgebaseId } : {};
    return api.get('/api/documents', { params });
  },
  get: (id) => api.get(`/api/documents/${id}`),
  delete: (id) => api.delete(`/api/documents/${id}`),
};

// Chat APIs
export const chatAPI = {
  sendMessage: (workflowId, sessionId, message) =>
    api.post('/api/chat', {
      workflow_id: workflowId,
      session_id: sessionId,
      message,
      role: 'user',
    }),
  getHistory: (sessionId) => api.get(`/api/chat/sessions/${sessionId}`),
  listSessions: (workflowId) => api.get(`/api/chat/workflows/${workflowId}/sessions`),
};

export default api;

