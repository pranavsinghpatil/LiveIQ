# ChatSynth Project Overview

*Last Updated: 2025-03-17*

## What is ChatSynth?
ChatSynth is an AI chat log aggregator that helps users consolidate and analyze conversations from various AI platforms. Think of it as a "unified inbox" for all your AI chat interactions.

## Key Features
1. **Chat Log Management**
   - Import chat logs from multiple sources
   - Organize conversations by topic, date, or AI model
   - Search across all conversations

2. **Analysis Tools**
   - Generate summaries of conversations
   - Extract key insights
   - Track conversation patterns

3. **User Experience**
   - Clean, intuitive interface
   - Real-time updates
   - Cross-platform compatibility

## Project Structure
```
ChatSynth/
├── backend/               # FastAPI backend server
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Database models
│   │   └── utils/        # Helper functions
│   └── tests/            # Backend tests
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   ├── store/        # State management
│   │   └── utils/        # Helper functions
└── docs/                 # Project documentation

```

## Getting Started
1. Review the [Technology Stack](./02_technology_stack.md) document
2. Follow the setup instructions in [Development Workflow](./07_development_workflow.md)
3. Understand the system design in [Architecture Guide](./03_architecture_guide.md)

## Key Concepts to Understand

### 1. Chat Log Processing
- Chat logs are parsed and normalized into a standard format
- Each log entry contains metadata about the AI model, timestamp, and context
- Logs are stored in a structured format for efficient querying

### 2. User Authentication
- JWT-based authentication system
- Role-based access control
- Secure password handling

### 3. Data Flow
- Frontend makes API calls to backend services
- Backend processes requests and interacts with database
- Real-time updates using WebSocket connections

## Common Questions

### "Where do I start?"
Begin by understanding the project structure and setting up your development environment. The [Development Workflow](./07_development_workflow.md) guide will walk you through this.

### "How do I add new features?"
1. Understand the relevant components in the architecture
2. Review existing code patterns
3. Follow the development workflow for adding new features

### "What are the coding standards?"
- Python: PEP 8 guidelines
- JavaScript: ESLint with Airbnb config
- Documentation: Clear, concise, with examples

## Next Steps
- Review the [Technology Stack](./02_technology_stack.md) document
- Set up your development environment
- Try running the application locally
