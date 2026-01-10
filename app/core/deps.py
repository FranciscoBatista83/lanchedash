from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import security
from app.services import usuario as usuario_service
from app.schemas.auth import TokenData
from app.models.usuario import Usuario

# 🏫 Aula do Professor: O Segurança (Middleware de Autenticação)
# Este arquivo contém as 'Dependências'. No FastAPI, dependências são como 
# postos de controle onde o usuário deve passar antes de chegar na rota.

# Definimos onde o FastAPI deve procurar o token (no endpoint /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    """
    Esta função é o nosso 'Segurança da Porta'.
    Ela pega o crachá (token), verifica se a assinatura é válida e se não expirou.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. 'Abrimos' o crachá usando nossa chave secreta
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        login: str = payload.get("sub")
        
        if login is None:
            raise credentials_exception
            
        token_data = TokenData(login=login)
    except JWTError:
        # Se a assinatura estiver errada ou o token expirado, barramos a entrada!
        raise credentials_exception
        
    # 2. Verificamos se o usuário dono do crachá ainda existe no banco
    user = usuario_service.get_usuario_by_login(db, login=token_data.login)
    
    if user is None:
        raise credentials_exception
        
    # 3. Se tudo estiver OK, o usuário pode passar!
    return user

async def get_current_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Professor explica: Este é o segurança da 'Área VIP'.
    Ele primeiro chama o segurança da porta (get_current_user).
    Se o usuário passar pela porta, ele checa se o papel é 'administrador'.
    """
    if current_user.papel != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar esta operação. Apenas administradores."
        )
    return current_user
