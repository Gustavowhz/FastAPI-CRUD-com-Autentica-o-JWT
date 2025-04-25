from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .auth import criar_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import get_db
from app.auth import verificar_token

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/produtos/", response_model=schemas.Produto, status_code=201)
def criar_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: dict = Depends(verificar_token)):
    db_produto = crud.create_produto(db=db, produto=produto)
    return db_produto

@router.put("/produtos/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(
    id: int,
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: dict = Depends(verificar_token)):
    db_produto = crud.update_produto(db, id=id, produto=produto)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return crud.update_produto(db, id=id, produto=produto)

@router.delete("/produtos/{produto_id}", status_code=204)
def deletar_produto(
    id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(verificar_token)):
    produto = crud.delete_produto(db, id=id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return crud.delete_produto(db, id=id)

@router.get("/produtos/", response_model=list[schemas.Produto])
def read_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    produtos = crud.get_produtos(db=db, skip=skip, limit=limit)
    return produtos

@router.get("/produtos/{produto_id}", response_model=schemas.Produto)
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.get_produto(db=db, produto_id=produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/usuarios/", response_model=schemas.Usuario)
def criar_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(verificar_token)):
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return crud.create_usuario(db, usuario)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_email(db, email=form_data.username)
    if not usuario or not crud.verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}