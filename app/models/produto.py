from sqlalchemy import Column, Integer, String, Numeric, Boolean
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(100), index=True)
    ativo = Column(Boolean, default=True)
    
    # Controle de Estoque
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=0)

