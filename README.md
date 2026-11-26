# To-Do List API

API REST para criação e acompanhamento de tarefas, desenvolvida em Python com FastAPI. Permite criar, listar, consultar, atualizar e remover tarefas, com validação dos dados e tratamento de erros. Os dados são persistidos em um banco SQLite.

**Demonstração online:** https://todo-list-api-mnx5.onrender.com (abre direto na documentação interativa)

> A versão publicada roda no plano gratuito do Render: a primeira requisição pode demorar alguns segundos para o serviço "acordar", e os dados não são permanentes (o banco é recriado a cada reinício ou novo deploy).

## Tecnologias
- Python
- FastAPI
- Pydantic (validação de dados)
- SQLAlchemy e SQLite (persistência)
- Uvicorn (servidor)
- Pytest (testes automatizados)
- Render (deploy)

## Como rodar

```bash
git clone https://github.com/JotaPekk/todo-list-api.git
cd todo-list-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. O banco `tarefas.db` é criado automaticamente na primeira execução.

> No Linux/macOS, ative o ambiente com `source venv/bin/activate`.

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | /tarefas | Lista todas as tarefas |
| GET | /tarefas/{id} | Busca uma tarefa pelo id |
| POST | /tarefas | Cria uma nova tarefa |
| PUT | /tarefas/{id} | Substitui uma tarefa (todos os campos) |
| PATCH | /tarefas/{id} | Atualiza só os campos enviados |
| DELETE | /tarefas/{id} | Remove uma tarefa |

Ids inexistentes retornam erro 404 e dados inválidos retornam erro 422.

## Documentação

O FastAPI gera automaticamente uma documentação interativa (Swagger). Com o servidor rodando, acesse `http://127.0.0.1:8000/docs` para testar as rotas pelo navegador. Na versão online, a página inicial já redireciona para ela.

![Swagger](docs.png)

## Testes

```bash
python -m pytest -v
```

A suíte cobre todas as rotas, incluindo os casos de erro (404 e 422). Os testes usam um banco SQLite em memória, separado do `tarefas.db`.

## Próximos passos
- Novos campos nas tarefas (prazo, prioridade, grupos)
- Banco de dados persistente na versão publicada (PostgreSQL)