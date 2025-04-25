from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .models import Usuario

def get_produto(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, produto: schemas.ProdutoCreate):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto:
        db_produto.nome = produto.nome
        db_produto.descricao = produto.descricao
        db_produto.preco = produto.preco
        db_produto.quantidade = produto.quantidade
        db.commit()
        db.refresh(db_produto)
        return db_produto
    return None

def delete_produto(db: Session, produto_id: int):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
        return db_produto
    return None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = pwd_context.hash(usuario.senha)
    db_usuario = Usuario(email=usuario.email, senha=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def verificar_senha(senha_plain: str, senha_hash: str):
    return pwd_context.verify(senha_plain, senha_hash)