# 🍔 LancheDash

API para sistema de delivery de lanches desenvolvida com FastAPI.

## 📋 Descrição

LancheDash é uma API REST moderna para gerenciamento de pedidos de lanches, desenvolvida com FastAPI e Python 3.13.

## 🚀 Tecnologias

- **Python** 3.13.7
- **FastAPI** 0.128.0
- **Uvicorn** 0.40.0
- **Pydantic** 2.12.5

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/FranciscoBatista83/lanchedash.git
cd lanchedash
```

### 2. Crie e ative o ambiente virtual

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ▶️ Como executar

Com o ambiente virtual ativado, execute:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛣️ Endpoints disponíveis

### Raiz
- `GET /` - Informações básicas da API

### Health Check
- `GET /health` - Verifica o status da API

### Lanches
- `GET /api/v1/lanches` - Lista todos os lanches disponíveis

## 📁 Estrutura do projeto

```
lanchedash/
├── app/
│   ├── models/
│   └── main.py
├── venv/
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Desenvolvimento

### Desativar o ambiente virtual

```bash
deactivate
```

### Atualizar dependências

```bash
pip freeze > requirements.txt
```

## 📝 Licença

Este projeto está em desenvolvimento.

## 👤 Autor

Francisco Batista - [GitHub](https://github.com/FranciscoBatista83)
