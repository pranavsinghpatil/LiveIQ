# ChatSynth Project Setup

## Backend Setup

1. Install Python dependencies:
```bash
pip install fastapi uvicorn sqlalchemy passlib python-jose[cryptography] bcrypt python-multipart
```

2. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

The backend server will run at http://localhost:8000 with API documentation available at http://localhost:8000/docs.

## Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend application will run at http://localhost:3000 (or next available port).

## Project Structure

```
ChatSynth/
├── backend/
│   ├── main.py           # FastAPI application and endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic models for request/response
│   ├── database.py       # Database configuration
│   ├── auth.py          # Authentication utilities
│   └── chatsynth.db     # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── store/       # State management
│   │   ├── utils/       # Utility functions
│   │   ├── App.tsx     # Main application component
│   │   └── main.tsx    # Application entry point
│   ├── package.json
│   └── index.html
└── README.md
```

## Authentication

Three user roles are supported:

1. Admin:
   - Username: admin
   - Password: admin123
   - Full access to all features

2. Regular User:
   - Register with email/password
   - Unlimited chat imports
   - Full feature access

3. Guest User:
   - No registration required
   - Limited to 2 chat imports
   - Basic feature access

## Development Workflow

1. Backend Development:
   - Edit FastAPI endpoints in `main.py`
   - Update database models in `models.py`
   - Add new schemas in `schemas.py`
   - Restart server to apply changes

2. Frontend Development:
   - Components in `src/components`
   - Pages in `src/pages`
   - State management in `src/store`
   - Hot reload enabled for instant updates

## Testing

1. Backend Tests:
   - Use pytest for API testing
   - Test authentication flows
   - Verify database operations

2. Frontend Tests:
   - Jest + React Testing Library
   - Component unit tests
   - Integration tests
   - End-to-end testing

## Deployment

1. Backend:
   - Use production WSGI server (e.g., Gunicorn)
   - Set up environment variables
   - Configure database URL

2. Frontend:
   - Build production bundle: `npm run build`
   - Serve static files
   - Configure API base URL
