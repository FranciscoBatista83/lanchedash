from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.usuario import Usuario, UsuarioCreate
from app.services import usuario as usuario_service

from app.core.deps import get_current_admin
from app.models.usuario import Usuario as UsuarioModel

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Cria um novo usuário.
    🔒 Apenas ADMINISTRADORES.
    """
    try:
        return usuario_service.create_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[Usuario])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Lista todos os usuários.
    🔒 Apenas para ADMINISTRADORES autenticados.
    """
    return usuario_service.get_usuarios(db)

@router.get("/{usuario_id}", response_model=Usuario)
def obter_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Busca usuário por ID.
    🔒 Apenas ADMINISTRADORES.
    """
    usuario = usuario_service.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

@router.get("/login/{login}", response_model=Usuario)
def obter_usuario_por_login(
    login: str, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Busca usuário por Login.
    🔒 Apenas ADMINISTRADORES.
    """
    usuario = usuario_service.get_usuario_by_login(db, login)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=Usuario)
def atualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Atualiza usuário.
    🔒 Apenas ADMINISTRADORES.
    """
    try:
        usuario_atualizado = usuario_service.update_usuario(db, usuario_id, usuario)
        if not usuario_atualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return usuario_atualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    admin: UsuarioModel = Depends(get_current_admin)
):
    """
    Deleta usuário.
    🔒 Apenas ADMINISTRADORES.
    """
    sucesso = usuario_service.delete_usuario(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return
