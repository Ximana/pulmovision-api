# Modelos

Coloque o modelo treinado do PulmoVision neste diretório.

## Arquivo Necessário

```
modelo_pulmonares.keras
```

## Como Obter

1. Treinar o modelo usando o projeto principal PulmoVision
2. Copiar o arquivo .keras gerado para este diretório
3. Ou baixar modelo pré-treinado

## Verificação

O modelo deve:
- Ter extensão .keras
- Ser compatível com TensorFlow 2.13+
- Aceitar input shape (None, 224, 224, 3)
- Retornar output shape (None, 3)

## Tamanho Esperado

~5-20 MB dependendo da arquitetura