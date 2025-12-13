# ==================== app/utils/exceptions.py ====================
"""Exceções customizadas"""
from fastapi import HTTPException

class PulmoVisionException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str = "error"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type

class InvalidImageException(PulmoVisionException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail, error_type="invalid_image")

class ImageTooLargeException(PulmoVisionException):
    def __init__(self, detail: str):
        super().__init__(status_code=413, detail=detail, error_type="image_too_large")

class PredictionException(PulmoVisionException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail, error_type="prediction_error")
