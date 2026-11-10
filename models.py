from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TarefaModel(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(300))
    concluida = Column(Boolean, default=False)


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(200), nullable=False)