from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Caixa(Base):
    __tablename__ = "caixas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Status: ABERTO, FECHADO
    status = Column(String(20), default="ABERTO", nullable=False)
    
    valor_abertura = Column(Float, nullable=False)
    valor_fechamento = Column(Float, nullable=True)
    valor_esperado = Column(Float, nullable=True) # Calculado pelo sistema
    
    data_abertura = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    data_fechamento = Column(DateTime, nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario")
    movimentacoes = relationship("MovimentacaoCaixa", back_populates="caixa")

class MovimentacaoCaixa(Base):
    __tablename__ = "movimentacoes_caixa"

    id = Column(Integer, primary_key=True, index=True)
    caixa_id = Column(Integer, ForeignKey("caixas.id"), nullable=False)
    
    # Tipo: SANGRIA (retirada), SUPRIMENTO (entrada extra), VENDA (opcional se quiser detalhar)
    tipo = Column(String(20), nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String(200), nullable=True)
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    caixa = relationship("Caixa", back_populates="movimentacoes")
