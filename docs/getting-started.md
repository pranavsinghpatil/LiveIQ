# Getting Started with ChatSynth

ChatSynth is a unified chat aggregator that brings together conversations from multiple AI platforms (ChatGPT, Mistral, Gemini) into a single, searchable interface.

## Prerequisites

Before running ChatSynth, ensure you have the following installed:

1. Python 3.8 or higher
2. Node.js 16 or higher
3. npm (comes with Node.js)
4. Git (optional, for version control)

## Quick Start Guide

### 1. Clone the Repository (if using Git)

```bash
git clone https://github.com/pranavsinghpatil/ChatSynth.git
cd ChatSynth
```

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install fastapi uvicorn sqlalchemy passlib python-jose[cryptography] bcrypt python-multipart
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend server will start at http://localhost:8000

### 3. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend application will start at http://localhost:3001

## Verifying the Installation

1. Backend API:
   - Open http://localhost:8000/docs in your browser
   - You should see the FastAPI Swagger documentation
   - All endpoints should be listed and accessible

2. Frontend Application:
   - Open http://localhost:3001 in your browser
   - You should see the ChatSynth login page
   - Try the guest login to verify authentication

## Default User Accounts

1. Admin Account:
   - Username: admin
   - Password: admin123
   - Full access to all features

2. Guest Access:
   - Click "Continue as Guest" on the login page
   - Limited to 2 chat imports
   - Basic feature access

## Common Issues and Solutions

### Backend Issues

1. Port 8000 already in use:
```bash
uvicorn main:app --reload --port 8001
```

2. Database errors:
```bash
# Delete the existing database and let it recreate
rm chatsynth.db
```

3. Import errors:
```bash
# Make sure you're in the correct directory
cd backend
# Activate the virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Frontend Issues

1. Port 3000/3001 already in use:
```bash
# The development server will automatically try the next available port
```

2. Node modules errors:
```bash
# Remove node_modules and reinstall
rm -rf node_modules
npm install
```

3. TypeScript errors:
```bash
# Clear TypeScript cache
rm -rf node_modules/.cache
npm run dev
```

## Development Workflow

1. Backend Development:
   - Edit files in the `backend` directory
   - The server will automatically reload on changes
   - Check the console for error messages

2. Frontend Development:
   - Edit files in the `frontend/src` directory
   - Changes will hot-reload in the browser
   - Check the browser console for errors

## Testing

1. Backend Tests:
```bash
cd backend
pytest
```

2. Frontend Tests:
```bash
cd frontend
npm test
```

## Building for Production

1. Backend:
```bash
cd backend
pip install gunicorn  # Linux/macOS only
# Set environment variables for production
```

2. Frontend:
```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist` directory.

## Additional Resources

- [Project Setup Guide](../Mandates/project-setup.md)
- [API Documentation](../Mandates/api-documentation.md)
- [Frontend Components](../Mandates/frontend-components.md)

## Need Help?

If you encounter any issues:

1. Check the console logs (both backend and frontend)
2. Review the documentation in the `docs` and `Mandates` folders
3. Create an issue on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Error messages
   - Environment details
