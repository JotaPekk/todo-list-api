import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base


# banco SQLite em memória, só para os testes
engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(bind=engine_teste, autoflush=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine_teste)

    def get_db_teste():
        db = SessionTeste()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_teste)


def test_criar_tarefa(client):
    resposta = client.post("/tarefas", json={"titulo": "Estudar"})
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Estudar"
    assert resposta.json()["id"] == 1


def test_buscar_inexistente(client):
    resposta = client.get("/tarefas/999")
    assert resposta.status_code == 404


def test_listar_vazio(client):
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_com_itens(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    client.post("/tarefas", json={"titulo": "Dormir"})
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_buscar_existente(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.get("/tarefas/1")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Estudar"


def test_criar_sem_titulo(client):
    resposta = client.post("/tarefas", json={})
    assert resposta.status_code == 422


def test_put(client):
    client.post("/tarefas", json={"titulo": "Estudar", "descricao": "FastAPI"})
    resposta = client.put("/tarefas/1", json={"titulo": "Dormir", "concluida": True})
    assert resposta.status_code == 200
    assert resposta.json()["id"] == 1
    assert resposta.json()["titulo"] == "Dormir"
    assert resposta.json()["descricao"] == ""
    assert resposta.json()["concluida"] is True


def test_put_inexistente(client):
    resposta = client.put("/tarefas/999", json={"titulo": "Dormir"})
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Tarefa não encontrada"


def test_put_sem_titulo(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.put("/tarefas/1", json={"concluida": True})
    assert resposta.status_code == 422


def test_patch_parcial(client):
    client.post("/tarefas", json={"titulo": "Estudar", "descricao": "FastAPI"})
    resposta = client.patch("/tarefas/1", json={"concluida": True})
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Estudar"
    assert resposta.json()["descricao"] == "FastAPI"
    assert resposta.json()["concluida"] is True


def test_patch_inexistente(client):
    resposta = client.patch("/tarefas/999", json={"concluida": True})
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Tarefa não encontrada"


def test_patch_titulo_nulo(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.patch("/tarefas/1", json={"titulo": None})
    assert resposta.status_code == 422


def test_patch_concluida_nula(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.patch("/tarefas/1", json={"concluida": None})
    assert resposta.status_code == 422


def test_delete(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.delete("/tarefas/1")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Tarefa removida com sucesso"
    resposta_get = client.get("/tarefas/1")
    assert resposta_get.status_code == 404


def test_delete_duas_vezes(client):
    client.post("/tarefas", json={"titulo": "Estudar"})
    resposta = client.delete("/tarefas/1")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Tarefa removida com sucesso"
    resposta2 = client.delete("/tarefas/1")
    assert resposta2.status_code == 404


def test_raiz_redireciona_para_docs(client):
    resposta = client.get("/", follow_redirects=False)
    assert resposta.status_code == 307
    assert resposta.headers["location"] == "/docs"