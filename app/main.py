from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.pedido import Pedido, ItemPedido
from app.models.caixa import Caixa, MovimentacaoCaixa
from app.models.estoque import EstoqueMovimentacao

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LancheDash API",
    description="API para sistema de delivery de lanches",
    version="1.0.0"
)

from app.routes import produto, usuario, auth, pedido, caixa, estoque, relatorio

app.include_router(produto.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(pedido.router)
app.include_router(caixa.router)
app.include_router(estoque.router)
app.include_router(relatorio.router)

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
