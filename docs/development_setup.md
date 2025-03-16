# Development Setup Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL (optional, SQLite for development)
- Redis (optional)

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` file with your configuration

6. Start the backend server:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Database Setup

### Using SQLite (Development)
- No additional setup required
- SQLite database will be created automatically

### Using PostgreSQL (Recommended for Production)
1. Create a new database:
```sql
CREATE DATABASE chatsynth;
```

2. Update `.env` file with your PostgreSQL credentials

## Testing

### Backend Tests
```bash
pytest backend/tests
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Documentation
Once the backend server is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Workflow
1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Create a pull request

## Code Style
- Backend: Follow PEP 8 guidelines
- Frontend: Follow ESLint configuration

## Common Issues
1. Database connection errors:
   - Check if database service is running
   - Verify credentials in `.env` file

2. Port conflicts:
   - Change ports in configuration if 8000 or 3000 are in use

3. Dependencies issues:
   - Make sure virtual environment is activated
   - Update dependencies: `pip install -r requirements.txt --upgrade`
