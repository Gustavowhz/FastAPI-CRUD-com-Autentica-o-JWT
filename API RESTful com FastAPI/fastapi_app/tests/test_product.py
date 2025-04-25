import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def token_autenticado():
    usuario_data = {"email": "teste@dominio.com", "senha": "senha123"}
    client.post("/usuarios/", json=usuario_data)

    login_data = {"username": usuario_data["email"], "password": usuario_data["senha"]}
    response = client.post("/token", data=login_data)
    return response.json()["access_token"]


def test_criar_usuario():
    usuario_data = {"email": "teste2@dominio.com", "senha": "senha123"}
    response = client.post("/usuarios/", json=usuario_data)

    assert response.status_code == 200 or response.status_code == 400 
    if response.status_code == 200:
        assert response.json()["email"] == usuario_data["email"]


def test_login_usuario():
    login_data = {"username": "teste@dominio.com", "password": "senha123"}
    response = client.post("/token", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_criar_produto(token_autenticado):
    produto_data = {
        "nome": "Mouse Gamer",
        "descricao": "Mouse com RGB",
        "preco": 199.90,
        "quantidade": 10
    }
    headers = {"Authorization": f"Bearer {token_autenticado}"}
    response = client.post("/produtos/", json=produto_data, headers=headers)

    assert response.status_code == 201
    assert response.json()["nome"] == produto_data["nome"]


def test_listar_produtos(token_autenticado):
    headers = {"Authorization": f"Bearer {token_autenticado}"}
    response = client.get("/produtos/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obter_produto_por_id(token_autenticado):
    headers = {"Authorization": f"Bearer {token_autenticado}"}
    response = client.get("/produtos/1", headers=headers)

    assert response.status_code == 200
    assert "id" in response.json()


def test_atualizar_produto(token_autenticado):
    atualizacao = {
        "nome": "Mouse Gamer Atualizado",
        "descricao": "Com mais RGB",
        "preco": 249.90,
        "quantidade": 8
    }
    headers = {"Authorization": f"Bearer {token_autenticado}"}
    response = client.put("/produtos/1", json=atualizacao, headers=headers)

    assert response.status_code == 200
    assert response.json()["nome"] == atualizacao["nome"]


def test_deletar_produto(token_autenticado):
    headers = {"Authorization": f"Bearer {token_autenticado}"}
    response = client.delete("/produtos/1", headers=headers)

    assert response.status_code == 204
