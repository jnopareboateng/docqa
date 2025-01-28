# Setup Guide

## Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.8+ for backend
- Google Cloud account for Gemini API access

## Project Structure
```
election-analysis/
├── src/                    # Frontend source code
│   ├── app/               # Next.js app directory
│   │   ├── layout.tsx    # Root layout with providers
│   │   └── page.tsx      # Main page component
│   ├── components/        # React components
│   │   ├── chat/         # Chat-related components
│   │   ├── doc/          # Document-related components
│   │   └── ui/           # UI components (shadcn)
│   ├── lib/              # Frontend utilities
│   │   ├── context/      # React contexts
│   │   └── utils/        # Helper functions
│   └── hooks/            # Custom React hooks
├── backend/               # Python backend
│   ├── utils/            # Backend utilities
│   │   ├── document_processor.py
│   │   ├── storage.py
│   │   └── error_handlers.py
│   └── main.py           # FastAPI application
├── docs/                 # Documentation
│   ├── architecture.md   # System architecture
│   └── setup.md         # Setup instructions
├── public/              # Static assets
└── storage/             # Document storage (created on first run)
    ├── documents/       # Uploaded files
    └── metadata.json    # Document metadata
```

## Environment Setup

1. **Backend Environment**
Create `backend/.env`:
```
GOOGLE_API_KEY=your_gemini_api_key
CORS_ORIGINS=http://localhost:3000
```

2. **Frontend Environment**
Create `.env.local` in project root:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Installation

1. **Install Frontend Dependencies**
```bash
npm install
```

2. **Install Backend Dependencies**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Development Workflow

1. **Start Development Servers**
Run the provided development script:
```bash
.\dev.ps1
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

Or start servers individually:

Frontend:
```bash
npm run dev
```

Backend:
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

## Production Deployment

1. **Build Frontend**
```bash
npm run build
npm run start
```

2. **Run Backend Server**
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation
Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

1. **Document Upload Issues**
- Ensure storage directory exists and has write permissions
- Check file size limits in your environment
- Verify supported file types (.pdf, .doc, .docx, .txt)

2. **API Connection Issues**
- Verify CORS settings in backend .env
- Check if backend server is running
- Ensure correct API URL in frontend .env.local

3. **Chat Not Working**
- Verify Google Gemini API key is valid
- Check if a document is uploaded before asking questions
- Monitor backend logs for error messages
