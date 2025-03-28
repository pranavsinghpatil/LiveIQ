# MainLayout Component Documentation

## Overview
The MainLayout component serves as the primary layout wrapper for VoxStitch, providing a consistent structure with header, sidebar, and content areas. It handles responsive layout adjustments and theme management.

## Component Implementation

### Component Structure
```typescript
interface MainLayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  showSidebar = true
}) => {
  const { isAuthenticated } = useAuthStore();
  const { isSidebarOpen, toggleSidebar } = useUIStore();
  
  return (
    <div className="main-layout">
      <Header onMenuClick={toggleSidebar} />
      
      <div className="layout-container">
        {showSidebar && isAuthenticated && (
          <Sidebar isOpen={isSidebarOpen} />
        )}
        
        <main
          className={clsx('main-content', {
            'with-sidebar': showSidebar && isAuthenticated && isSidebarOpen
          })}
        >
          {children}
        </main>
      </div>
      
      <Footer />
    </div>
  );
};
```

## Styling

### CSS Modules
```scss
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-background);
  
  .layout-container {
    display: flex;
    flex: 1;
    position: relative;
  }
  
  .main-content {
    flex: 1;
    padding: 1.5rem;
    transition: margin-left 0.3s ease;
    
    &.with-sidebar {
      margin-left: 250px;
      
      @media (max-width: 768px) {
        margin-left: 0;
      }
    }
    
    @media (max-width: 768px) {
      padding: 1rem;
    }
  }
}
```

## Usage Examples

### Basic Usage
```typescript
function App() {
  return (
    <MainLayout>
      <h1>Welcome to VoxStitch</h1>
      <p>Your AI chat log aggregator</p>
    </MainLayout>
  );
}
```

### Without Sidebar
```typescript
function LoginPage() {
  return (
    <MainLayout showSidebar={false}>
      <LoginForm />
    </MainLayout>
  );
}
```

### With Conditional Content
```typescript
function DashboardPage() {
  const { isAuthenticated, isLoading } = useAuthStore();
  
  return (
    <MainLayout>
      {isLoading ? (
        <LoadingSpinner />
      ) : isAuthenticated ? (
        <Dashboard />
      ) : (
        <Navigate to="/login" />
      )}
    </MainLayout>
  );
}
```

## Responsive Behavior

### Desktop View
On desktop screens (>768px):
- Sidebar is visible when open
- Main content has left margin when sidebar is open
- Header shows full navigation

### Mobile View
On mobile screens (≤768px):
- Sidebar appears as an overlay when toggled
- Main content uses full width
- Header shows mobile menu button

## Theme Integration

The MainLayout component integrates with the application's theme system:
- Background colors adapt to light/dark mode
- Sidebar and header styling changes with theme
- Content area padding adjusts for different screen sizes

## Layout Variants

### Default Layout
- Header at top
- Sidebar on left (when visible)
- Content area on right
- Footer at bottom

### Centered Layout (via CSS customization)
```typescript
function CenteredLayout({ children }) {
  return (
    <MainLayout showSidebar={false}>
      <div className="centered-content">
        {children}
      </div>
    </MainLayout>
  );
}
```

```scss
.centered-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 800px;
  margin: 0 auto;
  height: 100%;
}
```

## Footer Component

The Footer component is included in the MainLayout:

```typescript
const Footer: React.FC = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p className="copyright">
          © {new Date().getFullYear()} VoxStitch. All rights reserved.
        </p>
        
        <nav className="footer-nav">
          <a href="/privacy">Privacy Policy</a>
          <a href="/terms">Terms of Service</a>
          <a href="/contact">Contact</a>
        </nav>
      </div>
    </footer>
  );
};
```

```scss
.app-footer {
  padding: 1rem;
  background: var(--color-background-dark);
  border-top: 1px solid var(--color-border);
  
  .footer-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1200px;
    margin: 0 auto;
    
    @media (max-width: 768px) {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
  
  .copyright {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    margin: 0;
  }
  
  .footer-nav {
    display: flex;
    gap: 1.5rem;
    
    a {
      font-size: 0.875rem;
      color: var(--color-text-secondary);
      text-decoration: none;
      
      &:hover {
        color: var(--color-primary);
      }
    }
  }
}
```
