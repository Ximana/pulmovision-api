# ==================== scripts/test_api.py ====================
"""Script para testar API localmente"""
import requests
import sys

def test_health():
    print("Testando /health...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(response.json())
    print()

def test_predict(image_path):
    print(f"Testando /predict com {image_path}...")
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/predict", files=files)
    print(f"Status: {response.status_code}")
    print(response.json())
    print()

def test_model():
    print("Testando /model...")
    response = requests.get("http://localhost:8000/model")
    print(f"Status: {response.status_code}")
    print(response.json())
    print()

if __name__ == "__main__":
    test_health()
    test_model()
    
    if len(sys.argv) > 1:
        test_predict(sys.argv[1])
    else:
        print("Forneça caminho de imagem para testar predição")
        print("Uso: python test_api.py caminho/para/imagem.jpg")
