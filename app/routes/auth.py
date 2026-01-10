from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.services import usuario as usuario_service
from app.core import security
from app.schemas.auth import Token

# 🏫 Aula do Professor: Rota de Autenticação
# Esta é a porta de entrada principal da nossa segurança.
# É aqui que o usuário apresenta suas credenciais para receber o crachá (Token).

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token)
async def login_para_obter_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de Login oficial.
    Recebe 'username' e 'password' do formulário OAuth2.
    """
    # 1. Tenta autenticar o usuário
    # Professor explica: Usamos o service para checar se o login existe e a senha bate.
    usuario = usuario_service.autenticar_usuario(db, form_data.username, form_data.password)
    
    if not usuario:
        # Se falhar, retornamos 401 (Unauthorized) com um cabeçalho padrão de segurança.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Se autenticou, gera o crachá digital (Token)
    # Incluímos o login e o papel (administrador/caixa) dentro do token.
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": usuario.login, "papel": usuario.papel},
        expires_delta=access_token_expires
    )
    
    # 3. Entrega o crachá!
    return {"access_token": access_token, "token_type": "bearer"}
