# api.ts

## Purpose
Provides a centralized API client configuration for VoxStitch, handling HTTP requests, authentication, and error management.

## Core Features

### Axios Instance Configuration
```typescript
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Request Interceptors

#### Authentication
```typescript
api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### Error Handling
```typescript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
```

## API Endpoints

### Authentication
```typescript
export const authApi = {
  login: (credentials: LoginCredentials) => 
    api.post('/auth/login', credentials),
  register: (userData: RegisterData) => 
    api.post('/auth/register', userData),
  loginAsGuest: () => 
    api.post('/auth/guest'),
};
```

### Chat Management
```typescript
export const chatApi = {
  importChat: (data: FormData) => 
    api.post('/chats/import', data),
  getChatList: () => 
    api.get('/chats'),
  getChatById: (id: string) => 
    api.get(`/chats/${id}`),
};
```

### User Management
```typescript
export const userApi = {
  updateProfile: (data: UserProfile) => 
    api.put('/users/profile', data),
  getUsageStats: () => 
    api.get('/users/usage'),
};
```

## Error Handling

### Error Types
```typescript
export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, any>;
};
```

### Error Processing
```typescript
const processApiError = (error: AxiosError): ApiError => {
  return {
    code: error.response?.data?.code || 'UNKNOWN_ERROR',
    message: error.response?.data?.message || 'An unknown error occurred',
    details: error.response?.data?.details,
  };
};
```

## Integration with Components

### Usage Example
```typescript
// In components
const importChat = async (formData: FormData) => {
  try {
    const response = await chatApi.importChat(formData);
    return response.data;
  } catch (error) {
    const apiError = processApiError(error);
    throw apiError;
  }
};
```

## Security Features

### Token Management
- Automatic token injection
- Token refresh handling
- Secure token storage

### Request Security
- CSRF protection
- XSS prevention
- Rate limiting handling

## Performance Optimizations

### Request Caching
```typescript
const cache = new Map<string, any>();

const getCachedData = async (key: string, fetcher: () => Promise<any>) => {
  if (cache.has(key)) {
    return cache.get(key);
  }
  const data = await fetcher();
  cache.set(key, data);
  return data;
};
```

### Request Deduplication
- Implements request queuing
- Prevents duplicate requests
- Optimizes network usage

## File Upload Handling

### MultiPart Requests
```typescript
const uploadFile = async (file: File, onProgress?: (progress: number) => void) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      const progress = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      onProgress?.(progress);
    },
  });
};
```

## Related Components
- `ImportChat.tsx`: Uses chat API endpoints
- `AuthProvider`: Uses auth API endpoints
- `UserProfile`: Uses user API endpoints

## Testing
```typescript
describe('api client', () => {
  it('handles authentication correctly', async () => {
    const response = await authApi.login({
      email: 'test@example.com',
      password: 'password',
    });
    expect(response.status).toBe(200);
  });
});
```

## Error Codes
```typescript
export enum ApiErrorCode {
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  RATE_LIMITED = 'RATE_LIMITED',
  SERVER_ERROR = 'SERVER_ERROR',
}
```

## Recent Updates
- Added request deduplication
- Improved error handling
- Enhanced file upload progress tracking
- Added request caching
- Improved type safety
