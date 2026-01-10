from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstoqueAjuste(BaseModel):
    produto_id: int
    quantidade: int
    motivo: Optional[str] = None
    # True para somar, False para subtrair
    is_acrescimo: bool = True

class EstoqueMovimentacaoRead(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str] = None
    data: datetime
    
    class Config:
        from_attributes = True

class ProdutoEstoqueAlerta(BaseModel):
    id: int
    nome: str
    estoque_atual: int
    estoque_minimo: int
    
    class Config:
        from_attributes = True
