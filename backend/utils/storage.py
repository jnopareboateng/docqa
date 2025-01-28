import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import json
from .error_handlers import AppError

class DocumentStorage:
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        self.docs_dir = os.path.join(base_dir, "documents")
        self.metadata_file = os.path.join(base_dir, "metadata.json")
        self._ensure_directories()
        self._load_metadata()

    def _ensure_directories(self) -> None:
        """Ensure storage directories exist"""
        os.makedirs(self.docs_dir, exist_ok=True)

    def _load_metadata(self) -> None:
        """Load document metadata from file"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
            self._save_metadata()

    def _save_metadata(self) -> None:
        """Save document metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def save_document(self, file_content: bytes, filename: str, file_type: str) -> Dict:
        """Save a document and its metadata"""
        doc_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Save the file
        file_path = os.path.join(self.docs_dir, f"{doc_id}{os.path.splitext(filename)[1]}")
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Save metadata
        metadata = {
            'id': doc_id,
            'filename': filename,
            'type': file_type,
            'created_at': timestamp,
            'path': file_path
        }
        self.metadata[doc_id] = metadata
        self._save_metadata()

        return metadata

    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get document metadata by ID"""
        return self.metadata.get(doc_id)

    def get_document_content(self, doc_id: str) -> bytes:
        """Get document content by ID"""
        metadata = self.get_document(doc_id)
        if not metadata:
            raise AppError(f"Document {doc_id} not found", 404)
        
        try:
            with open(metadata['path'], 'rb') as f:
                return f.read()
        except Exception as e:
            raise AppError(f"Error reading document: {str(e)}")

    def list_documents(self) -> List[Dict]:
        """List all documents"""
        return list(self.metadata.values())

    def delete_document(self, doc_id: str) -> None:
        """Delete a document and its metadata"""
        metadata = self.get_document(doc_id)
        if not metadata:
            raise AppError(f"Document {doc_id} not found", 404)
        
        # Delete file
        try:
            os.remove(metadata['path'])
        except Exception:
            pass  # File might already be deleted

        # Delete metadata
        del self.metadata[doc_id]
        self._save_metadata()
