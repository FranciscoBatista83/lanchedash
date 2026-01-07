from sqlalchemy.orm import Session
from app.models.produto import Produto as ProdutoModel
from app.schemas.produto import ProdutoCreate

def create_produto(db: Session, produto: ProdutoCreate):
    # Lógica de negócio (poderia ter validações extras aqui)
    novo_produto = ProdutoModel(**produto.model_dump())
    
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    return novo_produto

def get_produtos(db: Session):
    return db.query(ProdutoModel).all()

def get_produto_by_id(db: Session, produto_id: int):
    return db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

def update_produto(db: Session, produto_id: int, produto: ProdutoCreate):
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    
    if db_produto is None:
        return None
    
    # Atualiza cada campo que veio no schema
    for key, value in produto.model_dump().items():
        setattr(db_produto, key, value)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
        return True
    return False
