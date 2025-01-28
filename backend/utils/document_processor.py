from pypdf import PdfReader
from typing import List, Dict
import os

class DocumentProcessor:
    def __init__(self):
        self.supported_extensions = {'.pdf'}
    
    def process_document(self, file_path: str) -> Dict[str, any]:
        """
        Process a document and extract its content
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Dict containing processed document information
        """
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {extension}")
        
        if extension == '.pdf':
            return self._process_pdf(file_path)
        
    def _process_pdf(self, file_path: str) -> Dict[str, any]:
        """
        Process a PDF document
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Dict containing processed PDF information
        """
        try:
            reader = PdfReader(file_path)
            pages = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    pages.append(text)
            
            return {
                'type': 'pdf',
                'num_pages': len(pages),
                'pages': pages,
                'total_text': '\n'.join(pages)
            }
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text (str): Text to split
            chunk_size (int): Maximum size of each chunk
            overlap (int): Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # If this is not the first chunk, start from the overlap point
            if start > 0:
                start = start - overlap
            
            # If this is the last chunk, end at the text length
            if end >= text_length:
                chunks.append(text[start:])
                break
            
            # Find the last period in the chunk to break at a natural point
            last_period = text.rfind('.', start, end)
            if last_period != -1:
                end = last_period + 1
            
            chunks.append(text[start:end])
            start = end
        
        return chunks
