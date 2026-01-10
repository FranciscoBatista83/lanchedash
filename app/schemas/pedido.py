from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.produto import Produto as ProdutoSchema

# --- Schemas de ITENS ---

class ItemBase(BaseModel):
    produto_id: int
    quantidade: int
    observacao: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    preco_unitario: float
    # Podemos incluir o produto completo aqui para facilitar o frontend
    # produto: ProdutoSchema 
    
    class Config:
        from_attributes = True

# --- Schemas de PEDIDOS ---

class PedidoBase(BaseModel):
    cliente_nome: Optional[str] = None

class PedidoCreate(PedidoBase):
    """Usado para abrir um novo pedido. Itens são adicionados depois ou junto."""
    pass

class PedidoFinalizar(BaseModel):
    forma_pagamento: str

class PedidoRead(PedidoBase):
    id: int
    usuario_id: int
    status: str
    total: float
    forma_pagamento: Optional[str] = None
    data_criacao: datetime
    data_finalizacao: Optional[datetime] = None
    
    # Lista de itens do pedido
    itens: List[ItemRead] = []

    class Config:
        from_attributes = True
