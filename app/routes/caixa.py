from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.caixa import CaixaRead, CaixaAbrir, CaixaFechar, MovimentacaoRead, MovimentacaoCreate, CaixaStatus
from app.services import caixa as caixa_service
from app.core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/caixa", tags=["Fluxo de Caixa"])

@router.get("/status", response_model=CaixaStatus)
def ver_status(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """Verifica se existe um caixa aberto no momento."""
    caixa = caixa_service.get_caixa_aberto(db)
    if not caixa:
        return {"is_aberto": False, "caixa_atual": None}
    
    return {
        "is_aberto": True, 
        "caixa_atual": {
            "id": caixa.id,
            "valor_abertura": caixa.valor_abertura,
            "data_abertura": caixa.data_abertura,
            "operador": caixa.usuario.login
        }
    }

@router.post("/abrir", response_model=CaixaRead)
def abrir_caixa(
    dados: CaixaAbrir, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Abre o caixa diário."""
    try:
        return caixa_service.abrir_caixa(db, current_user.id, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fechar", response_model=CaixaRead)
def fechar_caixa(
    dados: CaixaFechar, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Fecha o caixa e mostra divergências (se houver)."""
    try:
        return caixa_service.fechar_caixa(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sangria", response_model=MovimentacaoRead)
def registrar_sangria(
    dados: MovimentacaoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Retirada de dinheiro para pagamentos ou segurança."""
    caixa = caixa_service.get_caixa_aberto(db)
    if not caixa:
        raise HTTPException(status_code=400, detail="Não há caixa aberto.")
    return caixa_service.registrar_movimentacao(db, caixa.id, "SANGRIA", dados)

@router.post("/suprimento", response_model=MovimentacaoRead)
def registrar_suprimento(
    dados: MovimentacaoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Entrada de dinheiro (ex: reforço de troco)."""
    caixa = caixa_service.get_caixa_aberto(db)
    if not caixa:
        raise HTTPException(status_code=400, detail="Não há caixa aberto.")
    return caixa_service.registrar_movimentacao(db, caixa.id, "SUPRIMENTO", dados)

@router.get("/historico", response_model=List[CaixaRead])
def ver_historico(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """⚠️ ADMIN: Lista todos os fechamentos passados."""
    return caixa_service.listar_historico(db)
