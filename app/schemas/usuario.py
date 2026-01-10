from pydantic import BaseModel, field_validator
from typing import Literal

class UsuarioBase(BaseModel):
    login: str
    papel: str

class UsuarioCreate(UsuarioBase):
    senha: str  # Senha em texto plano (será hasheada no service)
    
    @field_validator('login')
    @classmethod
    def validar_login(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError('Login deve ter pelo menos 3 caracteres')
        if len(v) > 50:
            raise ValueError('Login deve ter no máximo 50 caracteres')
        return v.strip()
    
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return v
    
    @field_validator('papel')
    @classmethod
    def validar_papel(cls, v: str) -> str:
        papeis_validos = ['administrador', 'caixa']
        if v not in papeis_validos:
            raise ValueError(f'Papel deve ser um de: {", ".join(papeis_validos)}')
        return v

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
