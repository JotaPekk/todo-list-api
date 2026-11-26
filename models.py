from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, default="")
    concluida = Column(Boolean, default=False)