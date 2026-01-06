from fastapi import APIRouter

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/")
async def listar_produtos():
    return {"id": 1, "nome": "Produto Exemplo"}