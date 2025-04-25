from pydantic import BaseModel, ConfigDict

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
