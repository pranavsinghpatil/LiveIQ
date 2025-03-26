import axios, { InternalAxiosRequestConfig, AxiosResponse, AxiosError, AxiosHeaders } from 'axios';
import { useAuthStore } from '../store/auth';

// Create axios instance with base config
export const api = axios.create({
  baseURL: 'http://localhost:8000',  // Explicitly set the base URL
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000'),
  withCredentials: false,  // Set to false since we're using * for CORS
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add auth token to requests
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().token;
  
  // Ensure headers object exists and is of correct type
  if (!config.headers) {
    config.headers = new AxiosHeaders();
  }
  
  // Add auth token if available
  if (token) {
    config.headers.set('Authorization', `Bearer ${token}`);
  }
  
  // Log request details for debugging
  console.log('Request URL:', config.url);
  console.log('Request Method:', config.method);
  console.log('Request Headers:', config.headers);
  console.log('Request Data:', config.data);
  return config;
}, (error) => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

// Handle auth errors
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log successful response for debugging
    console.log('Response Status:', response.status);
    console.log('Response Data:', response.data);
    return response;
  },
  (error: AxiosError) => {
    // Log error details for debugging
    console.error('Response error:', error);
    console.error('Error Response:', error.response);
    console.error('Error Message:', error.message);
    
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
