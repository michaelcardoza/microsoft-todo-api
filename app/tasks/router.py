from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.shared.resources import strings
from app.shared.utils import parse_order_by
from app.shared.depends import UserLoggedInDep, QueryParamsDep
from app.tasks.model import Task
from app.tasks.repository import TaskRepositoryDep
from app.tasks.schemas import TaskSchema, TaskListSchema, TaskCreateSchema, TaskUpdateSchema

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=TaskListSchema)
def read_tasks(
    current_user: UserLoggedInDep,
    task_repository: TaskRepositoryDep,
    query_params: QueryParamsDep,
    group: Optional[int] = None,
):
    order_by = parse_order_by(query_params.order_by, entity=Task, extra_fields=["content"])
    total, tasks = task_repository.find(
        user_id=current_user.id,
        group=group,
        limit=query_params.limit,
        page=query_params.page,
        order_by=order_by,
    )
    has_more = total > query_params.limit * query_params.page
    return {"data": tasks, "total": total, "has_more": has_more}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(payload: TaskCreateSchema, current_user: UserLoggedInDep, task_repository: TaskRepositoryDep):
    new_task = task_repository.create(current_user.id, payload)
    return new_task


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskSchema)
def read_task(task_id: int, current_user: UserLoggedInDep, task_repository: TaskRepositoryDep):
    task = task_repository.find_one(current_user.id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_NOT_FOUND_ERROR
        )
    return task


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskSchema)
def update_task(
    task_id: int,
    payload: TaskUpdateSchema,
    current_user: UserLoggedInDep,
    task_repository: TaskRepositoryDep
):
    task = task_repository.find_one(current_user.id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_NOT_FOUND_ERROR
        )
    task_updated = task_repository.update(task, payload)
    return task_updated


@router.delete("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskSchema)
def remove_task(task_id: int, current_user: UserLoggedInDep, task_repository: TaskRepositoryDep):
    task = task_repository.find_one(current_user.id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_NOT_FOUND_ERROR
        )
    task_removed = task_repository.remove(task)
    return task_removed
