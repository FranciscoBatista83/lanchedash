from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.produto import Produto as ProdutoModel
from app.schemas.produto import Produto, ProdutoCreate

from app.services import produto as produto_service

from app.core.deps import get_current_user, get_current_admin
from app.models.usuario import Usuario as UsuarioModel

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Cadastra novo produto.
    🔒 Apenas ADMINISTRADORES.
    """
    return produto_service.create_produto(db, produto)

@router.get("/", response_model=List[Produto])
def listar_produtos(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Lista cardápio.
    🔓 Autenticado (Admin/Caixa).
    """
    return produto_service.get_produtos(db)

@router.get("/{produto_id}", response_model=Produto)
def obter_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Detalhes do produto.
    🔓 Autenticado (Admin/Caixa).
    """
    produto = produto_service.get_produto_by_id(db, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(
    produto_id: int, 
    produto: ProdutoCreate, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Edita produto.
    🔒 Apenas ADMINISTRADORES.
    """
    produto_atualizado = produto_service.update_produto(db, produto_id, produto)
    if not produto_atualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto_atualizado

@router.delete("/{produto_id}" , status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Remove produto.
    🔒 Apenas ADMINISTRADORES.
    """
    sucesso = produto_service.delete_produto(db, produto_id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return
    