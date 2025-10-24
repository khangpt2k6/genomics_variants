
import axios from 'axios';
import { API_CONFIG, STORAGE_KEYS, ROUTES } from '../constants';
import { getStorageItem, removeStorageItem, getErrorMessage } from '../utils';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = getStorageItem(STORAGE_KEYS.AUTH_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add request timestamp for debugging
    config.metadata = { startTime: new Date() };
    
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Log successful requests in development
    if (import.meta.env.DEV) {
      const duration = new Date() - response.config.metadata?.startTime;
      console.log(`API ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status} (${duration}ms)`);
    }
    
    return response;
  },
  (error) => {
    // Log errors
    console.error('API Error:', getErrorMessage(error));
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Handle unauthorized access
      removeStorageItem(STORAGE_KEYS.AUTH_TOKEN);
      window.location.href = ROUTES.LOGIN || '/login';
    } else if (error.response?.status === 403) {
      // Handle forbidden access
      console.warn('Access forbidden - insufficient permissions');
    } else if (error.response?.status >= 500) {
      // Handle server errors
      console.error('Server error - please try again later');
    }
    
    return Promise.reject(error);
  }
);

// Add retry logic for failed requests
const retryRequest = async (config, retryCount = 0) => {
  try {
    return await api(config);
  } catch (error) {
    if (retryCount < API_CONFIG.RETRY_ATTEMPTS && 
        error.response?.status >= 500) {
      await new Promise(resolve => 
        setTimeout(resolve, API_CONFIG.RETRY_DELAY * (retryCount + 1))
      );
      return retryRequest(config, retryCount + 1);
    }
    throw error;
  }
};

// Export both the api instance and retry function
export { retryRequest };
export default api;
