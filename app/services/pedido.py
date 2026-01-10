from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.models.pedido import Pedido, ItemPedido
from app.models.produto import Produto
from app.schemas.pedido import PedidoCreate, ItemCreate, PedidoFinalizar

def criar_pedido(db: Session, usuario_id: int, dados: PedidoCreate) -> Pedido:
    """Abre um novo pedido vazio."""
    novo_pedido = Pedido(
        usuario_id=usuario_id,
        cliente_nome=dados.cliente_nome,
        status="ABERTO",
        total=0.0
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

def get_pedido(db: Session, pedido_id: int) -> Pedido:
    """Busca pedido por ID."""
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def listar_pedidos(db: Session, apenas_abertos: bool = False):
    """Lista pedidos. Se apenas_abertos=True, filtra por status."""
    query = db.query(Pedido)
    if apenas_abertos:
        query = query.filter(Pedido.status == "ABERTO")
    # Ordenar por mais recentes primeiro
    return query.order_by(Pedido.data_criacao.desc()).all()

from app.models.estoque import EstoqueMovimentacao

# ... (resto das funções acima iguais)

def adicionar_item(db: Session, pedido_id: int, item: ItemCreate) -> Pedido:
    """
    Adiciona um item ao pedido e baixa o estoque.
    """
    pedido = get_pedido(db, pedido_id)
    if not pedido or pedido.status != "ABERTO":
        raise ValueError("Pedido não encontrado ou já fechado")

    produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
    if not produto:
        raise ValueError("Produto não encontrado")
    
    if produto.estoque_atual < item.quantidade:
        raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque_atual}")
    
    # 1. Cria o item
    novo_item = ItemPedido(
        pedido_id=pedido.id,
        produto_id=produto.id,
        quantidade=item.quantidade,
        preco_unitario=produto.preco,
        observacao=item.observacao
    )
    db.add(novo_item)
    
    # 2. Atualiza estoque do produto
    produto.estoque_atual -= item.quantidade
    
    # 3. Registra movimentação de estoque
    mov = EstoqueMovimentacao(
        produto_id=produto.id,
        tipo="SAIDA_VENDA",
        quantidade=item.quantidade,
        motivo=f"Venda Pedido #{pedido.id}"
    )
    db.add(mov)
    
    # 4. Atualiza total do pedido
    pedido.total += (produto.preco * item.quantidade)
    
    db.commit()
    db.refresh(pedido)
    return pedido

def remover_item(db: Session, pedido_id: int, item_id: int) -> Pedido:
    """Remove item e devolve ao estoque."""
    pedido = get_pedido(db, pedido_id)
    if not pedido or pedido.status != "ABERTO":
        raise ValueError("Pedido não encontrado ou fechado")
    
    item = db.query(ItemPedido).filter(ItemPedido.id == item_id, ItemPedido.pedido_id == pedido_id).first()
    if not item:
        raise ValueError("Item não encontrado")
    
    # 1. Devolve ao estoque
    produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
    if produto:
        produto.estoque_atual += item.quantidade
        # Registra devolução
        mov = EstoqueMovimentacao(
            produto_id=produto.id,
            tipo="ENTRADA_CANCELAMENTO_ITEM",
            quantidade=item.quantidade,
            motivo=f"Remoção Item Pedido #{pedido.id}"
        )
        db.add(mov)

    # 2. Atualiza total e deleta item
    pedido.total -= (item.preco_unitario * item.quantidade)
    if pedido.total < 0: pedido.total = 0
        
    db.delete(item)
    db.commit()
    db.refresh(pedido)
    return pedido


def finalizar_pedido(db: Session, pedido_id: int, dados: PedidoFinalizar) -> Pedido:
    """Fecha o pedido."""
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise ValueError("Pedido não encontrado")
        
    if pedido.status != "ABERTO":
        raise ValueError("Pedido já está finalizado")
        
    if not pedido.itens:
        raise ValueError("Não é possível fechar um pedido vazio")
        
    pedido.status = "FINALIZADO"
    pedido.forma_pagamento = dados.forma_pagamento
    pedido.data_finalizacao = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(pedido)
    return pedido

def reabrir_pedido(db: Session, pedido_id: int) -> Pedido:
    """Exclusivo Admin: Reabre pedido para correção."""
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise ValueError("Pedido não encontrado")
        
    pedido.status = "ABERTO"
    pedido.data_finalizacao = None
    
    db.commit()
    db.refresh(pedido)
    return pedido
