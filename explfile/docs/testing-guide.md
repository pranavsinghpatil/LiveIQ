# VoxStitch Testing Guide

## Testing Strategy

### 1. Test Types

#### Unit Tests
- Component testing
- Service testing
- Utility function testing
- State management testing

#### Integration Tests
- API endpoint testing
- Service integration testing
- Database interaction testing
- External service integration

#### End-to-End Tests
- User journey testing
- Cross-browser testing
- Mobile responsiveness
- Performance testing

### 2. Test Coverage Goals
- Frontend: 80%+ coverage
- Backend: 90%+ coverage
- Critical paths: 100% coverage

## Frontend Testing

### 1. Component Tests

#### ImportChat Component
```typescript
describe('ImportChat', () => {
  it('renders import dialog', () => {
    render(<ImportChat />);
    expect(screen.getByText('Import Chat')).toBeInTheDocument();
  });

  it('handles file upload', async () => {
    render(<ImportChat />);
    const file = new File(['chat content'], 'chat.txt', { type: 'text/plain' });
    const input = screen.getByLabelText('Upload File');
    
    await userEvent.upload(input, file);
    expect(screen.getByText('chat.txt')).toBeInTheDocument();
  });

  it('validates file types', async () => {
    render(<ImportChat />);
    const file = new File(['invalid'], 'doc.exe', { type: 'application/x-msdownload' });
    const input = screen.getByLabelText('Upload File');
    
    await userEvent.upload(input, file);
    expect(screen.getByText('Unsupported file type')).toBeInTheDocument();
  });
});
```

#### SearchBar Component
```typescript
describe('SearchBar', () => {
  it('performs search', async () => {
    render(<SearchBar />);
    const input = screen.getByPlaceholderText('Search chats...');
    
    await userEvent.type(input, 'test query');
    await userEvent.click(screen.getByText('Search'));
    
    expect(mockSearchFunction).toHaveBeenCalledWith('test query');
  });

  it('applies filters', async () => {
    render(<SearchBar />);
    await userEvent.click(screen.getByText('Filters'));
    await userEvent.click(screen.getByText('ChatGPT'));
    
    expect(screen.getByText('Platform: ChatGPT')).toBeInTheDocument();
  });
});
```

#### ChatList Component
```typescript
describe('ChatList', () => {
  it('renders chat items', () => {
    const chats = [
      { id: '1', title: 'Chat 1' },
      { id: '2', title: 'Chat 2' }
    ];
    
    render(<ChatList chats={chats} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(2);
  });

  it('handles chat selection', async () => {
    const chats = [{ id: '1', title: 'Chat 1' }];
    render(<ChatList chats={chats} />);
    
    await userEvent.click(screen.getByText('Chat 1'));
    expect(mockSelectChat).toHaveBeenCalledWith('1');
  });
});
```

### 2. Store Tests

#### Auth Store
```typescript
describe('authStore', () => {
  it('handles login', () => {
    const store = useAuthStore();
    store.login({ token: 'test-token', user: testUser });
    
    expect(store.isAuthenticated).toBe(true);
    expect(store.user).toEqual(testUser);
  });

  it('tracks guest limits', () => {
    const store = useAuthStore();
    store.login({ token: 'test-token', user: guestUser });
    store.decrementGuestImports();
    
    expect(store.guestImportsRemaining).toBe(1);
  });
});
```

### 3. E2E Tests

#### User Journey
```typescript
describe('User Journey', () => {
  it('completes guest user flow', async () => {
    // Start as guest
    await page.goto('/');
    await page.click('text=Try as Guest');
    
    // Import chat
    await page.click('text=Import Chat');
    await page.setInputFiles('input[type="file"]', 'test-chat.txt');
    await page.click('text=Import');
    
    // Verify import
    expect(await page.textContent('.chat-list')).toContain('test-chat.txt');
    
    // Search
    await page.fill('[placeholder="Search chats..."]', 'test');
    await page.click('text=Search');
    
    // Verify search results
    expect(await page.$$('.chat-item')).toHaveLength(1);
  });
});
```

## Backend Testing

### 1. API Tests

#### Auth Endpoints
```python
def test_login():
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_guest_limits():
    # Login as guest
    response = client.post("/api/auth/guest")
    token = response.json()["token"]
    
    # Import chats until limit
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(3):
        response = client.post("/api/chats/import", json={
            "title": "Test Chat"
        }, headers=headers)
        
    assert response.status_code == 403
    assert "Guest import limit reached" in response.json()["detail"]
```

#### Chat Processing
```python
def test_chat_import():
    response = client.post("/api/chats/import", json={
        "platform": "chatgpt",
        "messages": [
            {"sender": "user", "content": "Hello"},
            {"sender": "assistant", "content": "Hi"}
        ]
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert "id" in response.json()
    assert "summary" in response.json()

def test_media_processing():
    with open("test.mp3", "rb") as f:
        response = client.post(
            "/api/media/upload",
            files={"file": f},
            headers=auth_headers
        )
        
    assert response.status_code == 200
    assert "transcript" in response.json()
```

### 2. Service Tests

#### Chat Processor
```python
def test_chat_analysis():
    processor = ChatProcessor()
    result = await processor.process_chat({
        "messages": [
            {"sender": "user", "content": "How does AI work?"},
            {"sender": "assistant", "content": "AI uses machine learning..."}
        ]
    })
    
    assert "summary" in result
    assert "topics" in result
    assert "sentiment" in result

def test_media_processing():
    processor = MediaProcessor()
    result = await processor.process_media("test.mp4", "video")
    
    assert "transcript" in result
    assert "visual_analysis" in result
```

### 3. Integration Tests

#### Database Operations
```python
def test_chat_storage():
    # Create chat
    chat_id = await db.create_chat(test_chat_data)
    
    # Verify retrieval
    chat = await db.get_chat(chat_id)
    assert chat["title"] == test_chat_data["title"]
    
    # Update chat
    await db.update_chat(chat_id, {"title": "New Title"})
    chat = await db.get_chat(chat_id)
    assert chat["title"] == "New Title"
    
    # Delete chat
    await db.delete_chat(chat_id)
    chat = await db.get_chat(chat_id)
    assert chat is None
```

## Performance Testing

### 1. Load Tests
```python
def test_chat_import_performance():
    async def import_chat():
        return await client.post("/api/chats/import", json=test_chat_data)
    
    results = await run_concurrent(import_chat, count=100)
    
    assert max(r.elapsed for r in results) < 2.0  # Max 2 seconds
    assert statistics.mean(r.elapsed for r in results) < 0.5  # Mean 0.5 seconds
```

### 2. Stress Tests
```python
def test_concurrent_media_processing():
    async def process_media():
        return await client.post("/api/media/upload", files={"file": test_file})
    
    results = await run_concurrent(process_media, count=50)
    assert all(r.status_code == 200 for r in results)
```

## Test Configuration

### 1. Jest Configuration
```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy'
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx'
  ]
};
```

### 2. Pytest Configuration
```python
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=app --cov-report=html

# conftest.py
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def auth_headers():
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}
```

## CI/CD Integration

### 1. GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
        
    - name: Install Frontend Dependencies
      run: |
        cd frontend
        npm install
        
    - name: Run Frontend Tests
      run: |
        cd frontend
        npm test
        
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
        
    - name: Install Backend Dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        
    - name: Run Backend Tests
      run: |
        cd backend
        pytest
```

## Test Reports

### 1. Coverage Reports
- Frontend: Jest coverage
- Backend: Pytest coverage
- Combined reports in CI/CD

### 2. Performance Reports
- Load test results
- Response time metrics
- Error rates
- Resource usage

### 3. Test Documentation
- Test cases
- Test scenarios
- Expected results
- Actual results
