import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

print("="*70)
print("TESTANDO ENDPOINTS DA API PULMOVISION")
print("="*70)

# Teste 1: Health Check
print("\n[1/4] Testando GET /health")
try:
    response = requests.get(f'{BASE_URL}/health', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ SUCESSO!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("❌ ERRO!")
        print(response.text)
except Exception as e:
    print(f"❌ FALHA: {e}")

# Teste 2: Modelo Info
print("\n[2/4] Testando GET /modelo/info")
try:
    response = requests.get(f'{BASE_URL}/modelo/info', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ SUCESSO!")
        data = response.json()
        print(f"  Modelo: {data.get('nome')}")
        print(f"  Versão: {data.get('versao')}")
        print(f"  Arquitetura: {data.get('arquitetura')}")
    else:
        print("❌ ERRO!")
        print(response.text)
except Exception as e:
    print(f"❌ FALHA: {e}")

# Teste 3: Limitações
print("\n[3/4] Testando GET /limitacoes")
try:
    response = requests.get(f'{BASE_URL}/limitacoes', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ SUCESSO!")
        data = response.json()
        print(f"  Limitações encontradas: {len(data.get('limitacoes', []))}")
    else:
        print("❌ ERRO!")
        print(response.text)
except Exception as e:
    print(f"❌ FALHA: {e}")

# Teste 4: Predição (sem imagem, só para verificar validação)
print("\n[4/4] Testando POST /predicao (sem arquivo)")
try:
    response = requests.post(f'{BASE_URL}/predicao', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("✅ VALIDAÇÃO FUNCIONANDO!")
        print(response.json())
    else:
        print(f"Status inesperado: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ FALHA: {e}")

print("\n" + "="*70)
print("TESTES CONCLUÍDOS")
print("="*70)
