from fastapi import APIRouter, HTTPException, status

from app.shared.depends import UserLoggedInDep, QueryParamsDep
from app.shared.utils import parse_order_by
from app.shared.resources import strings
from app.task_groups.model import TaskGroup
from app.task_groups.repository import TaskGroupRepositoryDep
from app.task_groups.schemas import TaskGroupSchema, TaskGroupListSchema, TaskGroupCreateSchema, TaskGroupUpdateSchema

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=TaskGroupListSchema)
def read_groups(
    current_user: UserLoggedInDep,
    task_group_repository: TaskGroupRepositoryDep,
    query_params: QueryParamsDep,
):
    order_by = parse_order_by(query_params.order_by, entity=TaskGroup, extra_fields=["name"])
    total, task_groups = task_group_repository.find(
        user_id=current_user.id,
        limit=query_params.limit,
        page=query_params.page,
        order_by=order_by,
    )
    has_more = total > query_params.limit * query_params.page
    return {"data": task_groups, "total": total, "has_more": has_more}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskGroupSchema)
def create_group(
    payload: TaskGroupCreateSchema,
    current_user: UserLoggedInDep,
    task_group_repository: TaskGroupRepositoryDep,
):
    task_group = task_group_repository.create(current_user.id, payload)
    return task_group


@router.get("/{group_id}", status_code=status.HTTP_200_OK)
def read_group(
    group_id: int,
    current_user: UserLoggedInDep,
    task_group_repository: TaskGroupRepositoryDep,
):
    task_group = task_group_repository.find_one(user_id=current_user.id, task_group_id=group_id)
    if task_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_GROUP_NOT_FOUND_ERROR,
        )
    return task_group


@router.put("/{group_id}", status_code=status.HTTP_200_OK)
def update_group(
    group_id: int,
    payload: TaskGroupUpdateSchema,
    current_user: UserLoggedInDep,
    task_group_repository: TaskGroupRepositoryDep,
):
    task_group = task_group_repository.find_one(user_id=current_user.id, task_group_id=group_id)
    if task_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_GROUP_NOT_FOUND_ERROR,
        )
    task_group = task_group_repository.update(task_group, payload)
    return task_group


@router.delete("/{group_id}", status_code=status.HTTP_200_OK, response_model=TaskGroupSchema)
def update_group(
    group_id: int,
    current_user: UserLoggedInDep,
    task_group_repository: TaskGroupRepositoryDep,
):
    task_group = task_group_repository.find_one(user_id=current_user.id, task_group_id=group_id)
    if task_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_GROUP_NOT_FOUND_ERROR,
        )
    task_group_removed = task_group_repository.remove(task_group)
    return task_group_removed
