from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=300)
    concluida: bool = False


class Tarefa(TarefaCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)


class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str