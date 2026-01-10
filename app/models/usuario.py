from sqlalchemy import Column, Integer, String
from app.database import Base

from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    papel = Column(String(50), nullable=False)  # "administrador" ou "caixa"

    pedidos = relationship("Pedido", back_populates="usuario")
