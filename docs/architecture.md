# ChatSynth System Architecture

## Technology Stack

### Frontend
- **Framework**: React.js
- **UI Library**: Material-UI
- **State Management**: Redux
- **API Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python)
- **Authentication**: JWT
- **API Documentation**: OpenAPI/Swagger
- **Data Validation**: Pydantic

### Database
- **Primary Database**: PostgreSQL
  - User data
  - Chat logs
  - Metadata
  - Search indices

### Infrastructure
- **Hosting**: Vercel (Frontend), Railway (Backend)
- **Database Hosting**: Railway
- **File Storage**: Local filesystem (development) / S3 (production)
- **Caching**: Redis

## System Components

### 1. Frontend Layer
```
├── components/
│   ├── auth/         # Authentication components
│   ├── dashboard/    # Main dashboard views
│   ├── chat/         # Chat log display components
│   └── common/       # Reusable UI components
├── services/         # API integration
├── store/           # Redux state management
└── utils/           # Helper functions
```

### 2. Backend Layer
```
├── api/
│   ├── auth/         # Authentication endpoints
│   ├── chat/         # Chat log management
│   ├── search/       # Search functionality
│   └── users/        # User management
├── core/            # Core application logic
├── models/          # Database models
└── utils/           # Helper functions
```

### 3. Database Schema
```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Logs
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    source VARCHAR(100),
    content JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES users(id)
);

-- Chat Log Tags
CREATE TABLE chat_log_tags (
    chat_log_id INTEGER REFERENCES chat_logs(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (chat_log_id, tag_id)
);
```

## Data Flow

1. **User Authentication**
   ```
   Client -> API Gateway -> Auth Service -> Database
   ```

2. **Chat Log Import**
   ```
   Client -> API Gateway -> Import Service -> Parser -> Database
   ```

3. **Search & Filter**
   ```
   Client -> API Gateway -> Search Service -> Database
   ```

## Security Measures

1. **Authentication**
   - JWT-based authentication
   - Secure password hashing (bcrypt)
   - Rate limiting on auth endpoints

2. **Data Protection**
   - HTTPS encryption
   - Input validation
   - SQL injection prevention
   - XSS protection

3. **API Security**
   - API key authentication
   - Request validation
   - CORS configuration
