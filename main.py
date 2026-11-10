from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import TarefaModel, UsuarioModel
from schemas import Tarefa, TarefaCreate, UsuarioCreate, UsuarioOut, Token
from auth import gerar_hash, verificar_senha, criar_token, usuario_atual

app = FastAPI(title="API de Tarefas")


@app.get("/")
def raiz():
    return {"mensagem": "API de Tarefas no ar!"}


#usuarios e login

@app.post("/usuarios", response_model=UsuarioOut, status_code=201, tags=["Auth"])
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(UsuarioModel).filter(UsuarioModel.email == dados.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo = UsuarioModel(email=dados.email, senha_hash=gerar_hash(dados.senha))
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


#o formulario do OAuth2 usa o campo "username", aqui ele recebe o e-mail
@app.post("/login", response_model=Token, tags=["Auth"])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == form.username).first()
    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token(usuario.email)
    return {"access_token": token, "token_type": "bearer"}


#tarefas do get publico

@app.get("/tarefas", response_model=list[Tarefa], tags=["Tarefas"])
def listar_tarefas(concluida: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(TarefaModel)
    if concluida is not None:
        query = query.filter(TarefaModel.concluida == concluida)
    return query.all()


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["Tarefas"])
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaModel).filter(TarefaModel.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


#tarefas post, put e delete protegidos

@app.post("/tarefas", response_model=Tarefa, status_code=201, tags=["Tarefas"])
def criar_tarefa(
    dados: TarefaCreate,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(usuario_atual),
):
    nova = TarefaModel(
        titulo=dados.titulo,
        descricao=dados.descricao,
        concluida=dados.concluida,
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@app.put("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["Tarefas"])
def atualizar_tarefa(
    tarefa_id: int,
    dados: TarefaCreate,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(usuario_atual),
):
    tarefa = db.query(TarefaModel).filter(TarefaModel.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao
    tarefa.concluida = dados.concluida

    db.commit()
    db.refresh(tarefa)
    return tarefa


@app.delete("/tarefas/{tarefa_id}", status_code=204, tags=["Tarefas"])
def remover_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(usuario_atual),
):
    tarefa = db.query(TarefaModel).filter(TarefaModel.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()