# ==================== app/utils/image_processing.py ====================
"""Processamento de imagens"""
import numpy as np

def preprocess_image(img_array: np.ndarray) -> np.ndarray:
    """
    Aplica preprocessing do EfficientNet.
    Normaliza para range [-1, 1]
    """
    img_array = img_array / 127.5 - 1.0
    return img_array.astype(np.float32)
