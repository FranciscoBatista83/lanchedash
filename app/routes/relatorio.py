from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.relatorio import DashboardResumo, RelatorioVendaItem, RelatorioProdutoRanking, RelatorioFinanceiro
from app.services import relatorio as relatorio_service
from app.core.deps import get_current_admin

router = APIRouter(prefix="/relatorios", tags=["📊 Relatórios & Gestão"])

@router.get("/dashboard", response_model=DashboardResumo)
def ver_dashboard(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Resumo rápido para a tela inicial do Admin.
    🔒 Apenas ADMINISTRADORES.
    """
    return relatorio_service.get_dashboard_resumo(db)

@router.get("/vendas", response_model=List[RelatorioVendaItem])
def relatorio_vendas(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Relatório detalhado de vendas finalizadas.
    Default: Últimos 30 dias.
    🔒 Apenas ADMINISTRADORES.
    """
    if not data_fim:
        data_fim = datetime.now(timezone.utc)
    if not data_inicio:
        data_inicio = data_fim - timedelta(days=30)
        
    return relatorio_service.get_relatorio_vendas(db, data_inicio, data_fim)

@router.get("/produtos", response_model=List[RelatorioProdutoRanking])
def ranking_produtos(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Lista dos produtos mais vendidos e faturamento gerado por cada um.
    🔒 Apenas ADMINISTRADORES.
    """
    return relatorio_service.get_ranking_produtos(db)

@router.get("/financeiro", response_model=List[RelatorioFinanceiro])
def relatorio_financeiro(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Resumo de faturamento agrupado por forma de pagamento.
    🔒 Apenas ADMINISTRADORES.
    """
    if not data_fim:
        data_fim = datetime.now(timezone.utc)
    if not data_inicio:
        # Default: Início do mês atual
        data_inicio = data_fim.replace(day=1, hour=0, minute=0, second=0)
        
    return relatorio_service.get_relatorio_financeiro(db, data_inicio, data_fim)
