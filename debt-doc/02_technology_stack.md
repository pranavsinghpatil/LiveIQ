# Technology Stack Documentation

*Last Updated: 2025-03-17*

## Backend Technologies

### Core Framework: FastAPI
- **Version**: 0.104.1
- **Purpose**: High-performance web framework for building APIs
- **Key Features Used**:
  - Automatic OpenAPI documentation
  - Type hints and validation using Pydantic
  - Async support for better performance
- **Location**: `backend/app/main.py`
- **Learning Resources**:
  - [FastAPI Documentation](https://fastapi.tiangolo.com/)
  - [Async in FastAPI](https://fastapi.tiangolo.com/async/)

### Database: PostgreSQL
- **Version**: Latest (14+)
- **ORM**: SQLAlchemy 2.0.23
- **Key Components**:
  - Models defined in `backend/app/models/`
  - Database configuration in `backend/app/core/database.py`
  - Migration management with Alembic
- **Important Concepts**:
  ```python
  # Example model definition
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
      email = Column(String, unique=True)
  ```

### Authentication: JWT
- **Library**: python-jose 3.3.0
- **Password Hashing**: passlib[bcrypt] 1.7.4
- **Implementation**: `backend/app/core/auth.py`
- **Key Features**:
  - Token-based authentication
  - Secure password hashing
  - Role-based access control

### Caching: Redis
- **Version**: 5.0.1
- **Purpose**: Session management and data caching
- **Implementation**: `backend/app/core/cache.py`
- **Usage Examples**:
  ```python
  # Caching example
  await redis.set(key, value, expire=3600)
  ```

## Frontend Technologies

### Core Framework: React with TypeScript
- **Build Tool**: Vite
- **State Management**: Redux Toolkit
- **Key Features**:
  - Functional components with hooks
  - Type-safe development
  - Modern build system

### UI Components
- **Framework**: Material-UI (MUI)
- **Styling**: Emotion (CSS-in-JS)
- **Layout**: CSS Grid and Flexbox
- **Component Structure**:
  ```
  components/
  ├── common/          # Reusable components
  ├── layout/          # Layout components
  ├── auth/            # Authentication components
  └── features/        # Feature-specific components
  ```

### API Integration
- **HTTP Client**: Axios
- **Implementation**: `frontend/src/services/api.ts`
- **Key Features**:
  - Request/response interceptors
  - Error handling
  - Authentication header management

## Development Tools

### Version Control
- **System**: Git
- **Hosting**: GitHub
- **Branch Strategy**:
  - `main`: Production code
  - `develop`: Development branch
  - Feature branches: `feature/*`

### Code Quality
- **Backend**:
  - Black (code formatting)
  - Flake8 (linting)
  - Pytest (testing)
- **Frontend**:
  - ESLint
  - Prettier
  - Jest

### Development Environment
- **Required**:
  - Python 3.8+
  - Node.js 16+
  - PostgreSQL
  - Redis
- **Recommended IDE**: VS Code with extensions:
  - Python
  - ESLint
  - Prettier
  - GitLens

## Deployment Stack

### Container Platform
- **Technology**: Docker
- **Orchestration**: Docker Compose (development)
- **Key Files**:
  - `Dockerfile`
  - `docker-compose.yml`

### Cloud Services
- **Object Storage**: AWS S3
  - Used for storing chat log files
  - Implementation in `backend/app/core/storage.py`
- **Monitoring**: CloudWatch
  - Application logs
  - Performance metrics

## Getting Started

1. **Install Dependencies**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend && npm install
   ```

2. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Configure database connection
   - Set up Redis connection

3. **Run Development Servers**
   ```bash
   # Backend
   uvicorn backend.app.main:app --reload
   
   # Frontend
   npm run dev
   ```

## Common Issues & Solutions

1. **Database Connection**
   - Check PostgreSQL service is running
   - Verify credentials in `.env`
   - Ensure database exists

2. **Redis Connection**
   - Verify Redis server is running
   - Check connection string in `.env`

3. **Frontend Build Issues**
   - Clear `node_modules` and reinstall
   - Check Node.js version
   - Verify TypeScript configuration

## Next Steps
- Review [Architecture Guide](./03_architecture_guide.md)
- Set up your local development environment
- Try running the basic application
