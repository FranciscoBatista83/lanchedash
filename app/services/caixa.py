from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional
from app.models.caixa import Caixa, MovimentacaoCaixa
from app.models.pedido import Pedido
from app.schemas.caixa import CaixaAbrir, CaixaFechar, MovimentacaoCreate

def get_caixa_aberto(db: Session) -> Optional[Caixa]:
    """Retorna o caixa atualmente aberto, se houver."""
    return db.query(Caixa).filter(Caixa.status == "ABERTO").first()

def abrir_caixa(db: Session, usuario_id: int, dados: CaixaAbrir) -> Caixa:
    """Abre um novo caixa diário."""
    # Verifica se já existe um aberto
    if get_caixa_aberto(db):
        raise ValueError("Já existe um caixa aberto. Feche o atual antes de abrir um novo.")
    
    novo_caixa = Caixa(
        usuario_id=usuario_id,
        valor_abertura=dados.valor_abertura,
        status="ABERTO"
    )
    db.add(novo_caixa)
    db.commit()
    db.refresh(novo_caixa)
    return novo_caixa

def calcular_valor_esperado(db: Session, caixa: Caixa) -> float:
    """Calcula quanto dinheiro deveria ter no caixa baseado nas vendas e movimentações."""
    # 1. Valor inicial
    total = caixa.valor_abertura
    
    # 2. Somar Movimentações (Suprimentos - Sangrias)
    movimentacoes = db.query(MovimentacaoCaixa).filter(MovimentacaoCaixa.caixa_id == caixa.id).all()
    for mov in movimentacoes:
        if mov.tipo == "SUPRIMENTO":
            total += mov.valor
        elif mov.tipo == "SANGRIA":
            total -= mov.valor
            
    # 3. Somar Vendas Finalizadas APÓS a abertura do caixa em DINHEIRO (ou todas se for controle total)
    # Por simplicidade, vamos somar todas as vendas finalizadas enquanto este caixa estivesse aberto.
    # Em um sistema real, filtraríamos por forma_pagamento == "DINHEIRO" para bater o físico.
    vendas = db.query(Pedido).filter(
        Pedido.status == "FINALIZADO",
        Pedido.data_finalizacao >= caixa.data_abertura
    ).all()
    
    for venda in vendas:
        # Só somamos se a venda ocorreu antes do fechamento (caso já tenha fechado)
        if caixa.data_fechamento and venda.data_finalizacao > caixa.data_fechamento:
            continue
        total += venda.total
        
    return total

def fechar_caixa(db: Session, dados: CaixaFechar) -> Caixa:
    """Fecha o caixa atual e calcula a diferença."""
    caixa = get_caixa_aberto(db)
    if not caixa:
        raise ValueError("Não há caixa aberto para fechar.")
    
    caixa.status = "FECHADO"
    caixa.data_fechamento = datetime.now(timezone.utc)
    caixa.valor_fechamento = dados.valor_fechamento
    caixa.valor_esperado = calcular_valor_esperado(db, caixa)
    
    db.commit()
    db.refresh(caixa)
    return caixa

def registrar_movimentacao(db: Session, caixa_id: int, tipo: str, dados: MovimentacaoCreate) -> MovimentacaoCaixa:
    """Registra uma Sangria ou Suprimento."""
    nova_mov = MovimentacaoCaixa(
        caixa_id=caixa_id,
        tipo=tipo,
        valor=dados.valor,
        descricao=dados.descricao
    )
    db.add(nova_mov)
    db.commit()
    db.refresh(nova_mov)
    return nova_mov

def listar_historico(db: Session):
    """Retorna todos os fechamentos de caixa."""
    return db.query(Caixa).order_by(Caixa.data_abertura.desc()).all()
