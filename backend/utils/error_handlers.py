from fastapi import HTTPException
from typing import Type, TypeVar, Dict, Any

T = TypeVar('T')

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def handle_error(error: Exception) -> Dict[str, Any]:
    """Convert different types of errors to a consistent format"""
    if isinstance(error, AppError):
        raise HTTPException(status_code=error.status_code, detail=error.message)
    elif isinstance(error, ValueError):
        raise HTTPException(status_code=400, detail=str(error))
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
