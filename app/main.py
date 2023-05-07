from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.task_groups.router import router as task_groups_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(task_groups_router, prefix="/task-groups", tags=["Task Groups"])


@app.get("/")
def index():
    return {
        "message": "TODO Api"
    }
