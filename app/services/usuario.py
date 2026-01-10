import bcrypt
from sqlalchemy.orm import Session
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.usuario import UsuarioCreate

def hash_senha(senha: str) -> str:
    """Gera o hash da senha usando bcrypt nativo"""
    salt = bcrypt.gensalt()
    senha_hasheada = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hasheada.decode('utf-8')

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se a senha plana corresponde ao hash usando bcrypt nativo"""
    try:
        return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_hash.encode('utf-8'))
    except Exception:
        return False

def create_usuario(db: Session, usuario: UsuarioCreate):
    """Cria um novo usuário com senha hasheada"""
    # Verifica se o login já existe
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.login == usuario.login).first()
    if usuario_existente:
        raise ValueError(f"Login '{usuario.login}' já está em uso")
    
    # Cria o hash da senha
    senha_hasheada = hash_senha(usuario.senha)
    
    # Cria o usuário (sem incluir a senha plana)
    dados_usuario = usuario.model_dump(exclude={'senha'})
    novo_usuario = UsuarioModel(
        **dados_usuario,
        senha_hash=senha_hasheada
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

def get_usuarios(db: Session):
    """Retorna todos os usuários"""
    return db.query(UsuarioModel).all()

def get_usuario_by_id(db: Session, usuario_id: int):
    """Busca um usuário por ID"""
    return db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()

def get_usuario_by_login(db: Session, login: str):
    """Busca um usuário por login"""
    return db.query(UsuarioModel).filter(UsuarioModel.login == login).first()

def update_usuario(db: Session, usuario_id: int, usuario: UsuarioCreate):
    """Atualiza um usuário existente"""
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    
    if db_usuario is None:
        return None
    
    # Verifica se está tentando mudar para um login já existente
    if usuario.login != db_usuario.login:
        usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.login == usuario.login).first()
        if usuario_existente:
            raise ValueError(f"Login '{usuario.login}' já está em uso")
    
    # Atualiza os campos
    db_usuario.login = usuario.login
    db_usuario.papel = usuario.papel
    
    # Se a senha foi fornecida, atualiza o hash
    if usuario.senha:
        db_usuario.senha_hash = hash_senha(usuario.senha)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    """Deleta um usuário"""
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

def autenticar_usuario(db: Session, login: str, senha: str):
    """Autentica um usuário verificando login e senha"""
    usuario = get_usuario_by_login(db, login)
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario
