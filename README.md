# Autenticação com JWT

Atividade da disciplina de APIs e Microsserviços. API de tarefas feita com FastAPI, SQLAlchemy e SQLite, com login usando OAuth2 e token JWT. As rotas de leitura (GET) são públicas e as de escrita (POST, PUT e DELETE) exigem token.

## Como rodar

1. Baixe o projeto:
   ```
   git clone https://github.com/iguw/Autenticacao-e-Autorizacao.git
   cd Autenticacao-e-Autorizacao

   ```

2. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Crie o banco com as migrações:
   ```
   alembic upgrade head
   ```

5. Rode a API:
   ```
   uvicorn main:app --reload
   ```

6. Abra http://127.0.0.1:8000/docs

## Como usar o login

1. Crie um usuário em `POST /usuarios` (e-mail e senha).
2. Clique em **Authorize** no Swagger e entre com o e-mail (no campo username) e a senha.
3. Pronto, as rotas POST, PUT e DELETE de `/tarefas` passam a funcionar.

Sem o token, essas rotas retornam 401. As rotas GET funcionam sem login.

## Autor

Guilherme Alves - [@iguw](https://github.com/iguw)