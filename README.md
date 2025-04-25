# FastAPI CRUD com Autenticação JWT

Projeto completo de uma API RESTful desenvolvida com [FastAPI](https://fastapi.tiangolo.com/), incluindo:

- CRUD completo de produtos
- Autenticação JWT
- Testes automatizados com Pytest
- Banco de dados com SQLAlchemy
- Validações com Pydantic
- Documentação automática com Swagger
- Pronto para deploy no Render

---

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy
- SQLite (padrão, mas facilmente adaptável para PostgreSQL)
- PyJWT
- Passlib (hash de senhas)
- Uvicorn
- Pytest

---

## Instalação

bash
# Clone o repositório
git clone https://github.com/Gustavowhz/FastAPI-CRUD-com-Autentica-o-JWT.git
cd nome-do-repositorio

--- 
 
# Crie e ative o ambiente virtual
.venv\Scripts\activate

---

# Instale as dependências
pip install -r requirements.txt

---

# Rodar Localmente
uvicorn app.main:app --reload

---

# Documentação interativa
```http://127.0.0.1:8000/docs```

---

# Funcionalidades

 Criar usuário
 Login com JWT
 Criar, listar, atualizar e deletar produtos
 Proteção de rotas com JWT
 Testes automatizados com Pytest
 Documentação automática
 Deploy-ready

---

 Desenvolvido por Gustavo Basilio


