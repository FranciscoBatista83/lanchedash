from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DashboardResumo(BaseModel):
    vendas_hoje_total: float
    quantidade_pedidos_hoje: int
    ticket_medio_hoje: float
    top_produtos: List[dict] # [{ "nome": "X-Tudo", "total_vendido": 15 }]

class RelatorioVendaItem(BaseModel):
    data: datetime
    id_pedido: int
    usuario: str
    total: float
    status: str
    forma_pagamento: Optional[str]

class RelatorioProdutoRanking(BaseModel):
    produto_nome: str
    quantidade_total: int
    faturamento_total: float

class RelatorioFinanceiro(BaseModel):
    forma_pagamento: str
    total: float
    quantidade_pedidos: int
