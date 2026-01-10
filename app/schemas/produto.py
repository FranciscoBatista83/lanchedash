from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    categoria: Optional[str] = None
    ativo: bool = True
    estoque_atual: int = 0
    estoque_minimo: int = 0

class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
