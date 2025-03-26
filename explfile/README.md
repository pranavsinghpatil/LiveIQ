# VoxStitch (formerly ChatSynth) - Project Overview

VoxStitch is an AI chat log aggregator that consolidates conversations from multiple platforms (ChatGPT, Mistral, Gemini, Claude, etc.) into a unified interface, making it easier to organize, search, and analyze AI conversations.

## Project Structure

The project is organized into several key directories:

- **frontend/**: React/TypeScript frontend application using Tailwind CSS for styling
- **backend/**: FastAPI Python backend that handles data processing, authentication, and API endpoints
- **docs/**: Project documentation including setup guides and API reference

## Key Features

1. **Multi-platform Chat Log Import**
   - URL import from various AI platforms
   - File upload (JSON, TXT, MD formats)
   - Video and audio content with optional transcripts

2. **Unified Dashboard**
   - Intuitive navigation
   - Chat grouping and organization
   - Recent and favorited conversations

3. **Advanced Search and Filtering**
   - Full-text search across all conversations
   - Filter by platform, date, content type
   - Tag-based organization

4. **Authentication System**
   - Flexible user access levels (admin, registered user, guest)
   - Guest mode with usage limits (2 chat imports, 5 messages)
   - Social login options (Google, GitHub, Apple) - UI prepared

5. **UI Design**
   - Consistent color scheme with gradients
   - Mobile-responsive design
   - Modern component styling and animations

## Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Zustand (state management)
- **Backend**: Python, FastAPI, SQLAlchemy
- **Authentication**: JWT, OAuth (planned)
- **Data Storage**: SQL database (specifics may vary)

## Relationship Between Components

The frontend communicates with the backend via RESTful API calls. The backend processes requests, interacts with the database, and returns appropriate responses. The authentication system manages user sessions and permissions throughout the application.

This documentation provides an overview of the entire project structure and detailed explanations of individual files and components.
