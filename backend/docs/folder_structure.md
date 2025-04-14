# VoxStitch Backend Folder Structure

## 📁 Root Directory
```
backend/
├── .env                  # Environment variables
├── .env.template         # Template for environment variables
├── __init__.py          # Python package initialization
├── main.py              # Main application entry point
├── models.py            # Base models and schemas
├── requirements.txt      # Python dependencies
├── uploads/             # Directory for file uploads
├── venv/                # Python virtual environment
├── .venv/               # Alternative virtual environment
├── app/                 # FastAPI application code
└── core/                # Core business logic and services
```

## 📁 app/ Directory
```
app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application setup
├── models/              # Application models
│   ├── __init__.py
│   ├── user_models.py   # User-related models
│   ├── chat.py         # Chat models
│   └── group.py        # Thread group models
├── routes/              # API routes
│   ├── __init__.py
│   ├── auth_routes.py   # Authentication routes
│   ├── chat_routes.py   # Chat management routes
│   ├── podcast_simulator.py  # Podcast simulation routes
│   └── process_routes.py    # Processing routes
├── services/            # Business logic services
│   ├── __init__.py
│   ├── auth_service.py   # Authentication service
│   ├── supabase_client.py  # Supabase database client
│   └── podcast_simulator.py  # Podcast simulation service
└── utils/              # Utility functions and helpers
    ├── __init__.py
    └── functions.py     # Common utility functions
```

## 📁 core/ Directory
```
core/
├── __init__.py          # Package initialization
├── models.py            # Core data models
├── llm_client.py        # LLM integration client
├── podcast_simulator/   # Podcast simulation module
│   ├── __init__.py
│   ├── podcast_simulator.py  # Main simulator class
│   ├── speaker_personas.py   # Speaker persona management
│   └── transcript_parser.py  # Transcript parsing utilities
├── hybrid_assistant.py  # Hybrid AI assistant implementation
└── thread_manager.py    # Thread management utilities
```

## 📁 uploads/ Directory
```
uploads/
└── media/              # Media files (images, audio, etc.)
```

## 📄 Key Files

### main.py
- Main application entry point
- Configures FastAPI app
- Sets up middleware and routes

### models.py
- Base Pydantic models
- Shared schemas
- Type definitions

### requirements.txt
- Lists all Python dependencies
- Specifies package versions

### .env and .env.template
- Environment configuration
- Secure storage of API keys
- Database credentials
- Application settings

## 📦 Dependencies
- FastAPI: Web framework
- Pydantic: Data validation
- SQLAlchemy: Database ORM
- Supabase: Database client
- OpenAI: LLM integration
- Google Gemini: LLM integration
- Claude: LLM integration
- Mistral: LLM integration
- DeepSeek: LLM integration

## 📝 Notes
- All routes are organized in the `app/routes/` directory
- Business logic is separated into services in `app/services/`
- Core functionality is in the `core/` directory
- Models are organized by feature in `app/models/`
- Environment variables should be copied from `.env.template` to `.env`
- The application uses a virtual environment for dependency management
