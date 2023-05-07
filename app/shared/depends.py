from typing import Annotated

from fastapi import Depends

from app.shared.utils import get_query_params
from app.shared.schemas import QueryParamsSchema
from app.auth.service import get_logged_in_user
from app.users.model import User


QueryParamsDep = Annotated[QueryParamsSchema, Depends(get_query_params)]
UserLoggedInDep = Annotated[User, Depends(get_logged_in_user)]
