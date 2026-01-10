from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoRead, PedidoCreate, ItemCreate, PedidoFinalizar
from app.services import pedido as pedido_service
from app.core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/pedidos", tags=["Vendas & Pedidos"])

# --- Rotas Abertas (Caixa e Admin) ---

@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def abrir_pedido(
    pedido: PedidoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Abre um novo pedido."""
    return pedido_service.criar_pedido(db, current_user.id, pedido)

@router.get("/", response_model=List[PedidoRead])
def listar_pedidos(
    apenas_abertos: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista pedidos recentes."""
    return pedido_service.listar_pedidos(db, apenas_abertos)

@router.get("/{pedido_id}", response_model=PedidoRead)
def ver_pedido(
    pedido_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Detalhes de um pedido."""
    pedido = pedido_service.get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/{pedido_id}/itens", response_model=PedidoRead)
def adicionar_item(
    pedido_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Adiciona item ao carrinho."""
    try:
        return pedido_service.adicionar_item(db, pedido_id, item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pedido_id}/itens/{item_id}", response_model=PedidoRead)
def remover_item(
    pedido_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Remove item do carrinho."""
    try:
        return pedido_service.remover_item(db, pedido_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{pedido_id}/finalizar", response_model=PedidoRead)
def finalizar_pedido(
    pedido_id: int,
    dados: PedidoFinalizar,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Fecha a conta e define pagamento."""
    try:
        return pedido_service.finalizar_pedido(db, pedido_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Rotas Restritas (Admin) ---

@router.put("/{pedido_id}/reabrir", response_model=PedidoRead)
def reabrir_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    ⚠️ ADMIN: Reabre um pedido finalizado para correção.
    """
    try:
        return pedido_service.reabrir_pedido(db, pedido_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
