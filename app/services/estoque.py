from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.estoque import EstoqueMovimentacao
from app.schemas.estoque import EstoqueAjuste

def listar_alertas(db: Session):
    """Retorna produtos que estão com estoque abaixo do mínimo."""
    return db.query(Produto).filter(Produto.estoque_atual <= Produto.estoque_minimo).all()

def ajustar_estoque(db: Session, usuario_id: int, dados: EstoqueAjuste):
    """Realiza um ajuste manual no estoque."""
    produto = db.query(Produto).filter(Produto.id == dados.produto_id).first()
    if not produto:
        raise ValueError("Produto não encontrado")
    
    if dados.is_acrescimo:
        produto.estoque_atual += dados.quantidade
        tipo = "AJUSTE_SOMA"
    else:
        produto.estoque_atual -= dados.quantidade
        tipo = "AJUSTE_SUBTRACAO"
        
    mov = EstoqueMovimentacao(
        produto_id=produto.id,
        usuario_id=usuario_id,
        tipo=tipo,
        quantidade=dados.quantidade,
        motivo=dados.motivo
    )
    db.add(mov)
    db.commit()
    db.refresh(produto)
    return produto

def listar_movimentacoes(db: Session, produto_id: int = None):
    """Lista o histórico de movimentações (opcional por produto)."""
    query = db.query(EstoqueMovimentacao)
    if produto_id:
        query = query.filter(EstoqueMovimentacao.produto_id == produto_id)
    return query.order_by(EstoqueMovimentacao.data.desc()).all()
