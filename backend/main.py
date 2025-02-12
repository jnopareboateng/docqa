from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import List, Optional
import json
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils.document_processor import DocumentProcessor
from utils.storage import DocumentStorage
from utils.error_handlers import handle_error, AppError

# Load environment variables
load_dotenv()

# Initialize services
doc_processor = DocumentProcessor()
doc_storage = DocumentStorage()

# Initialize Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure storage directories exist
    os.makedirs("storage/documents", exist_ok=True)
    yield
    # Shutdown: cleanup if needed
    pass

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],  # Be explicit about allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Error handler middleware
@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        error_msg = str(exc)
        return JSONResponse(
            status_code=400,
            content={"detail": error_msg}
        )

class QuestionRequest(BaseModel):
    question: str
    document_id: str

@app.post("/upload")
async def upload_document(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not file.filename:
        raise HTTPException(status_code=400, detail="File has no filename")
        
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")
            
        # Save the document
        doc_metadata = doc_storage.save_document(
            content,
            file.filename,
            file.content_type
        )
        
        # Process the document
        processed_doc = doc_processor.process_document(doc_metadata['path'])
        
        # Update metadata with processed content
        doc_metadata['num_pages'] = processed_doc.get('num_pages', 1)
        doc_metadata['content'] = processed_doc.get('total_text', '')
        
        return doc_metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/documents")
async def list_documents() -> List[dict]:
    """List all uploaded documents"""
    return doc_storage.list_documents()

@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get document metadata and content"""
    doc = doc_storage.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document"""
    try:
        doc_storage.delete_document(doc_id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        handle_error(e)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        logger.info(f"Processing question for document: {request.document_id}")
        
        # Get document content
        doc = doc_storage.get_document(request.document_id)
        if not doc:
            logger.error(f"Document not found: {request.document_id}")
            raise AppError("Document not found", 404)
        
        # Initialize Gemini model
        try:
            model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise AppError("Failed to initialize AI model", 500)
        
        # Prepare the prompt with document context
        prompt = f"""Context from document '{doc['filename']}':
{doc.get('content', '')}

Question: {request.question}

Please answer the question based on the given context. If the answer cannot be found in the context, say so."""
        
        # Generate response
        try:
            response = model.generate_content(prompt)
            if not response or not hasattr(response, 'text'):
                logger.error("Invalid response from Gemini API")
                raise AppError("Failed to generate response", 500)
            return {"answer": response.text}
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise AppError(f"Failed to generate response: {str(e)}", 500)
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
