# ChatSynth Setup Guide

ChatSynth is a powerful chat log aggregator that consolidates conversations from multiple platforms into a unified interface. This guide will help you set up and run the project locally.

## Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (v18 or higher)
- **Python** (v3.9 or higher)
- **PostgreSQL** (v13 or higher)
- **Git**

## Project Structure

```plaintext
ChatSynth/
├── frontend/         # React TypeScript frontend
├── backend/         # Python FastAPI backend
├── docs/           # Documentation
└── Mandates/       # Project requirements and protocols
```

## Frontend Setup

1. **Open a new terminal window**.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a `.env.development` file with the following content:
   ```plaintext
   VITE_API_URL=http://localhost:8000
   VITE_AUTH_TOKEN_KEY=chatsynth_auth_token
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3001`

## Backend Setup

1. **Open a new terminal window**.
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file with the following content:
   ```plaintext
   DATABASE_URL=postgresql://user:password@localhost:5432/chatsynth
   SECRET_KEY=your_secret_key_here
   CORS_ORIGINS=http://localhost:3001
   ```
6. Initialize the database:
   ```bash
   alembic upgrade head
   ```
7. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`

## Alembic Setup

To set up Alembic for managing database migrations, follow these steps:

1. **Create the `alembic.ini` file** in the backend directory:
   ```ini
   [alembic]
   script_location = alembic
   sqlalchemy.url = postgresql://user:password@localhost:5432/chatsynth
   ```
   Replace `user` and `password` with your actual database credentials.

2. **Create the Alembic directory**:
   ```bash
   mkdir alembic
   ```

3. **Initialize Alembic** (if not already done):
   ```bash
   alembic init alembic
   ```
   This command will create the necessary directory structure and configuration files.

4. **Update the `env.py` file** in the `alembic` directory to ensure the connection string is set correctly.

5. **Run the migration command** to apply the migrations:
   ```bash
   alembic upgrade head
   ```
   This command will apply all migrations to the database.

## Database Setup

1. **Open a new terminal window**.
2. Create a PostgreSQL database:
   ```bash
   createdb chatsynth
   ```
3. The database migrations will be applied automatically when running `alembic upgrade head`

## Development Tools

- **React DevTools**: Install the browser extension for better debugging.
- **PostgreSQL client** (e.g., pgAdmin, DBeaver) for database management.
- **VS Code** with recommended extensions:
  - ESLint
  - Prettier
  - Python
  - TypeScript and JavaScript Language Features

## Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest
```

## Common Issues and Solutions

1. **Database Connection Issues**
   - Ensure PostgreSQL is running.
   - Check database credentials in `.env`.
   - Verify database exists: `psql -l`.

2. **CORS Errors**
   - Verify `CORS_ORIGINS` in backend `.env`.
   - Check frontend API URL in `.env.development`.

3. **Authentication Issues**
   - Clear browser local storage.
   - Check if backend JWT secret is set.
   - Verify token expiration settings.

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## Contributing

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Follow the coding standards:
   - Use TypeScript for frontend.
   - Follow PEP 8 for Python code.
   - Write tests for new features.

3. Submit a pull request with:
   - Clear description of changes.
   - Any related issue numbers.
   - Screenshots for UI changes.
