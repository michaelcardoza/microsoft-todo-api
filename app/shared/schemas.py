from pydantic import BaseModel, Field


class QueryParamsSchema(BaseModel):
    limit: int = Field(20, ge=1, le=100)
    page: int = Field(1, ge=0)
    order_by: str = Field(None)
