from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, time, timedelta, timezone
from typing import List, Optional

from app.models.pedido import Pedido, ItemPedido
from app.models.produto import Produto
from app.models.usuario import Usuario

def get_dashboard_resumo(db: Session):
    """Gera um resumo rápido do dia (Dashboard)."""
    hoje_inicio = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 1. Total e Qtd de Vendas HOJE
    vendas_hoje = db.query(
        func.sum(Pedido.total).label("faturamento"),
        func.count(Pedido.id).label("quantidade")
    ).filter(
        Pedido.status == "FINALIZADO",
        Pedido.data_finalizacao >= hoje_inicio
    ).first()
    
    faturamento = vendas_hoje.faturamento or 0.0
    quantidade = vendas_hoje.quantidade or 0
    ticket_medio = faturamento / quantidade if quantidade > 0 else 0.0
    
    # 2. Top Produtos (Geral)
    top_prod = db.query(
        Produto.nome,
        func.sum(ItemPedido.quantidade).label("total")
    ).join(ItemPedido).join(Pedido).filter(
        Pedido.status == "FINALIZADO"
    ).group_by(Produto.nome).order_by(desc("total")).limit(5).all()
    
    return {
        "vendas_hoje_total": faturamento,
        "quantidade_pedidos_hoje": quantidade,
        "ticket_medio_hoje": ticket_medio,
        "top_produtos": [{"nome": p.nome, "total_vendido": p.total} for p in top_prod]
    }

def get_relatorio_vendas(db: Session, data_inicio: datetime, data_fim: datetime):
    """Lista vendas detalhadas em um período."""
    vendas = db.query(Pedido).filter(
        Pedido.status == "FINALIZADO",
        Pedido.data_finalizacao >= data_inicio,
        Pedido.data_finalizacao <= data_fim
    ).order_by(Pedido.data_finalizacao.desc()).all()
    
    return [
        {
            "data": v.data_finalizacao,
            "id_pedido": v.id,
            "usuario": v.usuario.login,
            "total": v.total,
            "status": v.status,
            "forma_pagamento": v.forma_pagamento
        } for v in vendas
    ]

def get_ranking_produtos(db: Session):
    """Ranking de produtos mais lucrativos/vendidos."""
    ranking = db.query(
        Produto.nome.label("produto_nome"),
        func.sum(ItemPedido.quantidade).label("quantidade_total"),
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).label("faturamento_total")
    ).join(ItemPedido).join(Pedido).filter(
        Pedido.status == "FINALIZADO"
    ).group_by(Produto.nome).order_by(desc("quantidade_total")).all()
    
    return [
        {
            "produto_nome": r.produto_nome,
            "quantidade_total": int(r.quantidade_total),
            "faturamento_total": float(r.faturamento_total)
        } for r in ranking
    ]

def get_relatorio_financeiro(db: Session, data_inicio: datetime, data_fim: datetime):
    """Total faturado por forma de pagamento."""
    financeiro = db.query(
        Pedido.forma_pagamento,
        func.sum(Pedido.total).label("total"),
        func.count(Pedido.id).label("quantidade")
    ).filter(
        Pedido.status == "FINALIZADO",
        Pedido.data_finalizacao >= data_inicio,
        Pedido.data_finalizacao <= data_fim
    ).group_by(Pedido.forma_pagamento).all()
    
    return [
        {
            "forma_pagamento": f.forma_pagamento or "Não Informado",
            "total": float(f.total),
            "quantidade_pedidos": int(f.quantidade)
        } for f in financeiro
    ]
