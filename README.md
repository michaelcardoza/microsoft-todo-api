### Details
Python version: >= 3.10

### Install packages
```bash
$ poetry shell

$ poetry install
```

### Run
```bash
$ uvicorn app.main:app --reload
```

Host: http://localhost:8000/

Swagger: http://localhost:8000/docs

Redocly: http://localhost:8000/redoc

### Migrations
```bash
$ alembic revision --autogenerate -m "init"

$ alembic upgrade head

$ alembic downgrade -1
```
