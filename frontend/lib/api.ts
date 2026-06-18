import axios from 'axios';

// Public tunnel URL from localhost.run - points to the locally running backend
const API_URL = 'https://41dc982fc67a2b.lhr.life/api/v1';

export const api = axios.create({
  // Make sure axios doesn't hang forever in the browser
  adapter: undefined as any,
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Prevent “infinite buffering / white screen” when backend is unreachable
  timeout: 15000,
});


// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // axios timeout / network failures
    if (error?.code === 'ECONNABORTED' || error?.message?.toLowerCase().includes('timeout')) {
      return Promise.reject({
        ...error,
        message: 'Request timed out. Check backend connectivity.',
      });
    }

    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);


// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  register: async (data: any) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
};

// Upload API
export const uploadAPI = {
  uploadFile: async (file: File, fileType: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);
    
    const response = await api.post('/upload/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  getHistory: async () => {
    const response = await api.get('/upload/history');
    return response.data;
  },
};

// Customer API
export const customerAPI = {
  validate: async (fileId: string) => {
    const response = await api.post(`/customers/validate?file_id=${fileId}`);
    return response.data;
  },
  clean: async (fileId: string, removeInvalid: boolean = true) => {
    const response = await api.post(`/customers/clean?file_id=${fileId}&remove_invalid=${removeInvalid}`);
    return response.data;
  },
  import: async (fileId: string) => {
    const response = await api.post(`/customers/import?file_id=${fileId}`);
    return response.data;
  },
  getAll: async (params?: any) => {
    const response = await api.get('/customers/', { params });
    return response.data;
  },
  getById: async (customerId: string) => {
    const response = await api.get(`/customers/${customerId}`);
    return response.data;
  },
};

// Analytics API
export const analyticsAPI = {
  getCustomerAnalytics: async () => {
    const response = await api.get('/analytics/customers');
    return response.data;
  },
  getTransactionAnalytics: async () => {
    const response = await api.get('/analytics/transactions');
    return response.data;
  },
  getSqlInsights: async () => {
    const response = await api.get('/analytics/sql-insights');
    return response.data;
  },
};

// VIP API
export const vipAPI = {
  generate: async () => {
    const response = await api.post('/vip/generate');
    return response.data;
  },
  getAll: async () => {
    const response = await api.get('/vip/');
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/vip/stats');
    return response.data;
  },
};