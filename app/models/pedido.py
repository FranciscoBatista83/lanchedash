from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_nome = Column(String(100), nullable=True)
    
    # Status: ABERTO, FINALIZADO, CANCELADO
    status = Column(String(20), default="ABERTO", nullable=False)
    
    total = Column(Float, default=0.0)
    forma_pagamento = Column(String(50), nullable=True) # Dinheiro, PIX, Cartão
    
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    data_finalizacao = Column(DateTime, nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False) # Preço congelado no momento da venda
    observacao = Column(String(200), nullable=True)

    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")
