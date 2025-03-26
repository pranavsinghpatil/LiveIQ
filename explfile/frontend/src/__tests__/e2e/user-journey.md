# End-to-End Test Suite

## Purpose
The End-to-End test suite validates complete user journeys through VoxStitch, ensuring that critical user flows work correctly from start to finish.

## Test Structure

### Test Setup
```typescript
import { test, expect } from '@playwright/test';
import { mockAuthService } from '../../mocks/auth';
import { mockChatService } from '../../mocks/chat';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await mockAuthService.setup(page);
  await mockChatService.setup(page);
});
```

## Test Cases

### 1. Guest User Journey
```typescript
test('guest user can browse and import chats', async ({ page }) => {
  // Start as guest
  await page.click('text=Continue as Guest');
  await expect(page).toHaveURL('/dashboard');

  // Verify guest limitations
  const importButton = page.locator('button:has-text("Import Chat")');
  await expect(importButton).toBeEnabled();
  await expect(page.locator('text=2 imports remaining')).toBeVisible();

  // Import a chat
  await importButton.click();
  await page.fill('[placeholder="Paste chat link"]', 'https://chat.example.com/123');
  await page.click('text=Import');
  await expect(page.locator('text=Chat imported successfully')).toBeVisible();

  // Verify import count decreased
  await expect(page.locator('text=1 import remaining')).toBeVisible();

  // Try to view imported chat
  await page.click('text=Example Chat');
  await expect(page).toHaveURL(/\/chats\/\d+/);
});
```

### 2. User Registration Flow
```typescript
test('user can register and access full features', async ({ page }) => {
  // Start registration
  await page.click('text=Sign Up');
  await expect(page).toHaveURL('/register');

  // Fill registration form
  await page.fill('input[name="name"]', 'Test User');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'Password123!');
  await page.fill('input[name="confirmPassword"]', 'Password123!');
  await page.check('text=I agree to the Terms');

  // Submit form
  await page.click('button:has-text("Create Account")');
  await expect(page).toHaveURL('/dashboard');

  // Verify full access
  await expect(page.locator('text=imports remaining')).not.toBeVisible();
  await expect(page.locator('text=Upgrade Account')).not.toBeVisible();
});
```

### 3. Chat Import and Management
```typescript
test('user can import and manage chats', async ({ page }) => {
  // Login as registered user
  await mockAuthService.login(page);

  // Import multiple chats
  for (const link of chatLinks) {
    await page.click('text=Import Chat');
    await page.fill('[placeholder="Paste chat link"]', link);
    await page.click('text=Import');
    await expect(page.locator('text=Chat imported successfully')).toBeVisible();
  }

  // Verify chat list
  const chatList = page.locator('[data-testid="chat-list"]');
  await expect(chatList.locator('li')).toHaveCount(chatLinks.length);

  // Search chats
  await page.fill('[placeholder="Search chats"]', 'example');
  await expect(chatList.locator('li')).toHaveCount(1);

  // Delete chat
  await page.click('[data-testid="chat-actions"]');
  await page.click('text=Delete');
  await page.click('text=Confirm');
  await expect(chatList.locator('li')).toHaveCount(0);
});
```

### 4. Chat Annotation Flow
```typescript
test('user can annotate chat messages', async ({ page }) => {
  // Login and navigate to chat
  await mockAuthService.login(page);
  await page.goto('/chats/123');

  // Add annotation
  await page.click('[data-testid="message"] [data-testid="annotate"]');
  await page.fill('[placeholder="Add annotation"]', 'Test annotation');
  await page.click('text=Save');

  // Verify annotation
  await expect(page.locator('text=Test annotation')).toBeVisible();

  // Edit annotation
  await page.click('[data-testid="annotation"] [data-testid="edit"]');
  await page.fill('[placeholder="Edit annotation"]', 'Updated annotation');
  await page.click('text=Save');

  // Verify updated annotation
  await expect(page.locator('text=Updated annotation')).toBeVisible();
});
```

## Test Utilities

### 1. Authentication Mocks
```typescript
export const mockAuthService = {
  setup: async (page: Page) => {
    await page.route('**/api/auth/**', (route) => {
      const url = route.request().url();
      if (url.includes('/login')) {
        return route.fulfill({
          status: 200,
          body: JSON.stringify({
            token: 'mock-token',
            user: {
              id: 1,
              name: 'Test User',
              email: 'test@example.com',
              isGuest: false
            }
          })
        });
      }
    });
  },

  login: async (page: Page) => {
    await page.evaluate(() => {
      localStorage.setItem('token', 'mock-token');
    });
    await page.reload();
  }
};
```

### 2. Chat Service Mocks
```typescript
export const mockChatService = {
  setup: async (page: Page) => {
    await page.route('**/api/chats/**', (route) => {
      const url = route.request().url();
      if (url.endsWith('/chats')) {
        return route.fulfill({
          status: 200,
          body: JSON.stringify(mockChats)
        });
      }
    });
  },

  mockChats: [
    {
      id: 1,
      title: 'Example Chat',
      platform: 'chatgpt',
      messageCount: 10,
      createdAt: new Date().toISOString()
    }
  ]
};
```

## Test Configuration

### Playwright Config
```typescript
import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'Chrome',
      use: { browserName: 'chromium' }
    },
    {
      name: 'Firefox',
      use: { browserName: 'firefox' }
    },
    {
      name: 'Safari',
      use: { browserName: 'webkit' }
    }
  ]
};

export default config;
```

## Test Helpers

### 1. User Actions
```typescript
export const userActions = {
  login: async (page: Page, email: string, password: string) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.click('button:has-text("Sign In")');
  },

  importChat: async (page: Page, link: string) => {
    await page.click('text=Import Chat');
    await page.fill('[placeholder="Paste chat link"]', link);
    await page.click('text=Import');
    await page.waitForSelector('text=Chat imported successfully');
  }
};
```

### 2. Assertions
```typescript
export const assertions = {
  expectToBeOnDashboard: async (page: Page) => {
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Your Chats');
  },

  expectChatCount: async (page: Page, count: number) => {
    await expect(page.locator('[data-testid="chat-list"] li')).toHaveCount(count);
  }
};
```

## Recent Updates
- Added cross-browser testing
- Improved test stability
- Enhanced error reporting
- Added visual regression tests
- Improved test utilities

## Best Practices
- Isolated test data
- Consistent naming
- Proper cleanup
- Error handling
- Performance optimization

## Test Coverage
- Authentication flows
- Chat management
- Search functionality
- Annotations
- User settings
