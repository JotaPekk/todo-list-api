from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tarefa(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False

tarefas = []
proximo_id = 1


def encontrar_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.get("/tarefas")
def listar_tarefas():
    return tarefas

@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int):
    return encontrar_tarefa(tarefa_id)

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    global proximo_id
    tarefa_dict = tarefa.model_dump()
    tarefa_dict["id"] = proximo_id
    proximo_id += 1
    tarefas.append(tarefa_dict)
    return tarefa_dict

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: Tarefa):
    tarefa = encontrar_tarefa(tarefa_id)
    tarefa.update(dados.model_dump())
    return tarefa

@app.delete("/tarefas/{tarefa_id}")
def remover_tarefa(tarefa_id: int):
    tarefa = encontrar_tarefa(tarefa_id)
    tarefas.remove(tarefa)
    return {"mensagem": "Tarefa removida com sucesso"}