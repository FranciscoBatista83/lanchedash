from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- MOVIMENTAÇÕES ---

class MovimentacaoBase(BaseModel):
    valor: float
    descricao: Optional[str] = None

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoRead(MovimentacaoBase):
    id: int
    caixa_id: int
    tipo: str
    data: datetime

    class Config:
        from_attributes = True

# --- CAIXA ---

class CaixaBase(BaseModel):
    valor_abertura: float

class CaixaAbrir(CaixaBase):
    pass

class CaixaFechar(BaseModel):
    valor_fechamento: float

class CaixaStatus(BaseModel):
    is_aberto: bool
    caixa_atual: Optional[dict] = None

class CaixaRead(BaseModel):
    id: int
    usuario_id: int
    status: str
    valor_abertura: float
    valor_fechamento: Optional[float] = None
    valor_esperado: Optional[float] = None
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    
    class Config:
        from_attributes = True
