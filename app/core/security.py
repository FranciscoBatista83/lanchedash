import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from dotenv import load_dotenv

# 🏫 Aula do Professor: Variáveis de Ambiente
# Agora estamos lendo os segredos de um arquivo externo (.env).
# Isso é como guardar a senha do cofre em um bilhete no bolso, em vez de escrever na porta do cofre!

load_dotenv()

# Pegamos a chave do ambiente, se não existir, usamos uma gerada (mas o ideal é sempre ter no .env)
SECRET_KEY = os.getenv("SECRET_KEY", "chave_temporaria_e_insegura_de_fallback")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Professor explica: Esta função cria o 'Crachá Digital' (JWT).
    Ela pega os dados do usuário, adiciona uma data de validade e carimba com nossa chave secreta.
    """
    to_encode = data.copy()
    
    # Define quando o token expira
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adicionamos o campo 'exp' (expiration) ao dicionário de dados
    to_encode.update({"exp": expire})
    
    # O comando jwt.encode faz a mágica: mistura os dados com a SECRET_KEY usando o ALGORITHM
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
