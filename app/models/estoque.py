from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class EstoqueMovimentacao(Base):
    __tablename__ = "estoque_movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True) # Quem fez o ajuste (opcional para auto)
    
    # Tipo: ENTRADA, SAIDA, AJUSTE_SUBTRACAO, AJUSTE_SOMA
    tipo = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(200), nullable=True) # ex: "Venda #123", "Produto vencido"
    
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    produto = relationship("Produto")
    usuario = relationship("Usuario")
