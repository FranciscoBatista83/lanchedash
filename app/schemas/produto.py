from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    categoria: Optional[str] = None
    ativo: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
