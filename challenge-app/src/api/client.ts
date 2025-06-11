import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');

  // Evita incluir o token em rotas públicas
  if (token && !config.url?.includes('/login')) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});


export default api;
