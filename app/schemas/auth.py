from pydantic import BaseModel
from typing import Optional

# 🏫 Aula do Professor: Schemas de Autenticação
# Pense nos Schemas como os "formulários oficiais" da nossa API.
# Eles definem exatamente como os dados entram e saem.

class Token(BaseModel):
    """
    Este é o formato da resposta que enviamos quando o usuário faz login com sucesso.
    É a entrega do 'Crachá Digital'.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Este schema descreve o que está 'dentro' do token quando o validamos.
    Geralmente contém a identificação do dono do crachá.
    """
    login: Optional[str] = None

class LoginRequest(BaseModel):
    """
    Formato para quando o usuário envia login e senha (texto plano).
    """
    login: str
    senha: str
