from fastapi.testclient import TestClient
from app.main import app
from app import crud, models, schemas
from app.database import SessionLocal, engine
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_criar_usuario():
    email_unico = f"teste_{uuid.uuid4().hex[:6]}@dominio.com"
    usuario_data = {"email": email_unico, "senha": "senha123"}
    
    response = client.post("/usuarios/", json=usuario_data)

    print(response.status_code, response.json())  # debug
    assert response.status_code == 200
    assert response.json()["email"] == usuario_data["email"]

def test_login_usuario():
    login_data = {"username": "teste@dominio.com", "password": "senha123"}

    response = client.post("/token", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

