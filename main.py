from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
import database

app = FastAPI(
    title="To-Do List API",
    description="API REST para criação e acompanhamento de tarefas.",
    version="1.0.0",)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Tarefa(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False

tarefas = []
proximo_id = 1


def encontrar_tarefa(tarefa_id: int, db: Session):
    tarefa = db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@app.get("/tarefas")
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.TarefaDB).all()

@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    return encontrar_tarefa(tarefa_id, db)

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa, db: Session = Depends(get_db)):
    nova = models.TarefaDB(**tarefa.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: Tarefa, db: Session = Depends(get_db)):
    tarefa = encontrar_tarefa(tarefa_id, db)
    for campo, valor in dados.model_dump().items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{tarefa_id}")
def remover_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = encontrar_tarefa(tarefa_id, db)
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa removida com sucesso"}