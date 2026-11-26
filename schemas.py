from pydantic import BaseModel
from pydantic import BaseModel, field_validator


class Tarefa(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False


class TarefaAtualizar(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    concluida: bool | None = None

    @field_validator("titulo", "concluida")
    @classmethod
    def campo_nao_pode_ser_nulo(cls, valor, info):
        if valor is None:
            raise ValueError(f"O campo {info.field_name} não pode ser nulo")
        return valor