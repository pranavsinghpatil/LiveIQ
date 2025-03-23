# ChatSynth Frontend Components

## Layout Components

### 1. MainLayout
- Main application layout with sidebar and header
- Dark mode support
- Responsive design
- Location: `src/layouts/MainLayout.tsx`

### 2. Header
- Application header with search and user menu
- Theme toggle button
- Profile dropdown
- Location: `src/components/layout/Header.tsx`

### 3. Sidebar
- Navigation menu
- Platform filters
- New chat button
- Location: `src/components/layout/Sidebar.tsx`

## Authentication Components

### 1. Login
- Email/password login form
- Guest login option
- Social login buttons (UI only)
- Location: `src/pages/Login.tsx`

### 2. Register
- User registration form
- Password validation
- Error handling
- Location: `src/pages/Register.tsx`

### 3. PrivateRoute
- Route protection for authenticated users
- Role-based access control
- Location: `src/components/auth/PrivateRoute.tsx`

## Chat Components

### 1. ChatList
- List of imported chats
- Platform-based filtering
- Search functionality
- Location: `src/components/chat/ChatList.tsx`

### 2. ChatView
- Detailed chat view
- Message thread display
- Annotations and tags
- Location: `src/pages/ChatView.tsx`

### 3. ImportChat
- Chat import modal
- Platform selection
- File upload/link input
- Location: `src/components/chat/ImportChat.tsx`

## UI Components

### 1. ThemeToggle
- Dark/light mode toggle
- System preference detection
- Smooth transitions
- Location: `src/components/ui/ThemeToggle.tsx`

### 2. Button
- Reusable button component
- Multiple variants
- Loading state
- Location: `src/components/ui/Button.tsx`

### 3. Input
- Form input component
- Validation states
- Error messages
- Location: `src/components/ui/Input.tsx`

## State Management

### 1. Auth Store
```typescript
// src/store/auth.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}
```

### 2. Chat Store
```typescript
// src/store/chat.ts
interface ChatState {
  chats: Chat[];
  selectedPlatforms: string[];
  searchQuery: string;
  importChat: (data: ImportData) => Promise<void>;
  deleteChat: (id: number) => Promise<void>;
  filterByPlatform: (platform: string) => void;
}
```

## Styling

### 1. Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: { /* ... */ },
        accent: { /* ... */ },
        dark: { /* ... */ },
        light: { /* ... */ },
      }
    }
  }
}
```

### 2. Global Styles
```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  /* Custom CSS variables */
}

/* Dark mode styles */
.dark { /* ... */ }
```

## Testing

### 1. Component Tests
```typescript
// src/components/auth/Login.test.tsx
describe('Login Component', () => {
  it('renders login form', () => {
    // Test implementation
  });

  it('handles successful login', async () => {
    // Test implementation
  });

  it('displays error messages', async () => {
    // Test implementation
  });
});
```

### 2. Integration Tests
```typescript
// src/tests/chat-import.test.tsx
describe('Chat Import Flow', () => {
  it('imports chat successfully', async () => {
    // Test implementation
  });

  it('handles import errors', async () => {
    // Test implementation
  });
});
```

## Component Props

### 1. Button Props
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

### 2. Input Props
```typescript
interface InputProps {
  type: 'text' | 'email' | 'password';
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  label?: string;
  placeholder?: string;
  required?: boolean;
}
```

### 3. Chat Props
```typescript
interface ChatProps {
  chat: Chat;
  onDelete?: (id: number) => void;
  onEdit?: (id: number) => void;
  showActions?: boolean;
}
```
