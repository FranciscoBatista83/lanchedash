from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LancheDash API",
    description="API para sistema de delivery de lanches",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raiz - verifica se a API está funcionando"""
    return {
        "message": "Bem-vindo ao LancheDash API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}

@app.get("/api/v1/lanches")
async def listar_lanches():
    """Lista todos os lanches disponíveis (exemplo)"""
    lanches_exemplo = [
        {
            "id": 1,
            "nome": "X-Burger",
            "descricao": "Hambúrguer com queijo, alface e tomate",
            "preco": 15.90
        },
        {
            "id": 2,
            "nome": "X-Bacon",
            "descricao": "Hambúrguer com queijo e bacon crocante",
            "preco": 18.90
        },
        {
            "id": 3,
            "nome": "X-Salada",
            "descricao": "Hambúrguer com queijo, alface, tomate e milho",
            "preco": 16.90
        }
    ]
    return {"lanches": lanches_exemplo}
