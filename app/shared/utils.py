from typing import Any

from fastapi import Query

from app.shared.schemas import QueryParamsSchema


def get_query_params(
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    order_by: str = Query(None),
) -> QueryParamsSchema:
    return QueryParamsSchema(limit=limit, page=page, order_by=order_by)


def parse_order_by(order_by: str, entity: Any, extra_fields: list[str] | None = None) -> list:
    if extra_fields is None:
        extra_fields = []
    fields = ["created_at", "updated_at", *extra_fields]
    expressions = []

    if order_by is not None:
        for field in order_by.split(","):
            field = field.strip()
            if field.startswith("-"):
                field = field[1:]
                if field in fields:
                    expressions.append(getattr(entity, field).desc())
            else:
                if field in fields:
                    expressions.append(getattr(entity, field).asc())
    else:
        created_at_attr = getattr(entity, "created_at", None)
        if created_at_attr is not None:
            expressions.append(created_at_attr.desc())

    return expressions
