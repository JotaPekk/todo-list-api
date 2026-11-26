from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session


import schemas
import models
import database

app = FastAPI(
    title="To-Do List API",
    description="API REST para criação e acompanhamento de tarefas.",
    version="1.0.0",
)

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def encontrar_tarefa(tarefa_id: int, db: Session):
    tarefa = db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


def aplicar_alteracoes(tarefa, dados: dict, db: Session):
    for campo, valor in dados.items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@app.get("/tarefas")
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.TarefaDB).all()


@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    return encontrar_tarefa(tarefa_id, db)


@app.post("/tarefas")
def criar_tarefa(tarefa: schemas.Tarefa, db: Session = Depends(get_db)):
    nova = models.TarefaDB(**tarefa.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: schemas.TarefaAtualizar, db: Session = Depends(get_db)):
    tarefa = encontrar_tarefa(tarefa_id, db)
    return aplicar_alteracoes(tarefa, dados.model_dump(), db)


@app.patch("/tarefas/{tarefa_id}")
def atualizar_parcial(tarefa_id: int, dados: schemas.TarefaAtualizar, db: Session = Depends(get_db)):
    tarefa = encontrar_tarefa(tarefa_id, db)
    return aplicar_alteracoes(tarefa, dados.model_dump(exclude_unset=True), db)


@app.delete("/tarefas/{tarefa_id}")
def remover_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = encontrar_tarefa(tarefa_id, db)
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa removida com sucesso"}