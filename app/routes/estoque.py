from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.estoque import EstoqueAjuste, EstoqueMovimentacaoRead, ProdutoEstoqueAlerta
from app.services import estoque as estoque_service
from app.core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/estoque", tags=["Controle de Estoque"])

@router.get("/alertas", response_model=List[ProdutoEstoqueAlerta])
def ver_alertas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista produtos que precisam de reposição."""
    return estoque_service.listar_alertas(db)

@router.post("/ajuste", status_code=status.HTTP_200_OK)
def ajustar_estoque(
    dados: EstoqueAjuste,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """⚠️ ADMIN: Correção manual de estoque."""
    try:
        return estoque_service.ajustar_estoque(db, admin.id, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/movimentacoes", response_model=List[EstoqueMovimentacaoRead])
def ver_movimentacoes(
    produto_id: int = None,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """⚠️ ADMIN: Histórico completo de entradas e saídas."""
    return estoque_service.listar_movimentacoes(db, produto_id)
