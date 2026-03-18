import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadChat = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload-chat', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  });

  return response.data;
};

export const fetchMessages = async (search = '', limit = 500, offset = 0) => {
  const response = await api.get('/messages', { params: { search, limit, offset } });
  return response.data;
};

export const fetchUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};

export const fetchAnalytics = async () => {
  const response = await api.get('/analytics');
  return response.data;
};

export const fetchSummary = async () => {
  const response = await api.get('/ai-summary');
  return response.data;
};

export const fetchSentiment = async () => {
  const response = await api.get('/sentiment');
  return response.data;
};

export const exportJson = async () => {
  const response = await api.get('/export-json');
  return response.data;
};
