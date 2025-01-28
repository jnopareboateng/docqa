# Document QA Web App Architecture

## Overview
This document outlines the architecture of our Document QA Web App, which consists of a Next.js frontend and Python backend. The application allows users to upload documents, process them, and interact with them through a chat interface powered by Google's Gemini API.

## System Architecture

### Frontend (Next.js)
- **Framework**: Next.js with TypeScript
- **Project Structure**:
  - `src/app`: Next.js App Router pages and layouts
  - `src/components`: Reusable React components
  - `src/lib`: Utilities and contexts
  - `src/hooks`: Custom React hooks
- **State Management**:
  - React Context for document state
  - Local state for UI components
- **UI Components**: 
  - shadcn/ui for consistent design
  - Chat components:
    - `ChatInterface`: Main chat container with message input and history
    - `MessageList`: Displays chat messages with user/assistant styling
  - Document components:
    - `FileUpload`: Handles document upload with progress state
    - `DocumentViewer`: PDF viewer with page navigation
- **Page Layout**:
  - Two-column responsive design
  - Left column: Document upload and preview
  - Right column: Chat interface for Q&A
  - Mobile-first approach with stacked layout
- **Key Features**:
  - Document upload interface with progress indicator
  - Document viewer
  - Chat interface for document Q&A
  - Real-time response streaming
  - Toast notifications for user feedback
  - Dark/Light theme support

### Backend (Python)
- **Framework**: FastAPI
- **Project Structure**:
  - `backend/main.py`: FastAPI application entry point
  - `backend/utils`: Utility modules
  - `storage`: Document storage directory
- **Document Processing**:
  - PDF parsing with pypdf
  - Text extraction and chunking
  - Document storage management
- **API Integration**: 
  - Google Gemini API for:
    - Text embeddings
    - Question answering
    - Context-aware responses
- **Storage**:
  - Local file system for documents
  - JSON-based metadata storage
- **Error Handling**:
  - Centralized error handling middleware
  - Custom error types
  - Consistent error responses

## Data Flow
1. User uploads document through Next.js frontend
2. Document is sent to Python backend for processing
3. Backend:
   - Saves document to storage
   - Processes document for text extraction
   - Updates metadata
4. Frontend updates document context
5. User asks questions through chat interface
6. Backend:
   - Retrieves document context
   - Sends to Gemini API with question
   - Returns AI-generated response
7. Frontend displays response in chat

## Security Considerations
- CORS configuration
- File type validation
- Size limits on uploads
- API key protection
- Error message sanitization
- Input validation

## Performance Optimization
- Document chunking for large files
- Progress indicators for uploads
- Async file processing
- Response streaming
- UI optimizations for mobile

## Development Setup
- Python virtual environment
- Node.js dependencies
- Environment variables
- Development script for running services
