import json
from typing import List, Optional

from fastapi import Header, Request
from fastapi.security import SecurityScopes
from pydantic import BaseModel

from ..common.exception import UnauthorizedException, NotPermissionException


class CurrentUser(BaseModel):
    id: int
    token_id: int
    authorities: List[str]


async def get_current_user(
        request: Request,
        security_scopes: SecurityScopes,
        user_id: Optional[int] = Header(None),
        user_token_id: Optional[int] = Header(None),
        authorities: Optional[str] = Header(None),
) -> CurrentUser:
    """ 通过依赖注入获取当前登录用户 """
    if not user_id:
        raise UnauthorizedException
    try:
        authorities = json.loads(authorities)
    except json.JSONDecodeError:
        authorities = []
    user = CurrentUser(
        id=user_id,
        token_id=user_token_id,
        authorities=authorities
    )
    for scope in security_scopes.scopes:
        if scope not in user.authorities:
            raise NotPermissionException
    return user


async def as_permission(
        request: Request,
        security_scopes: SecurityScopes,
):
    """ 权限校验 """
    for scope in security_scopes.scopes:
        if scope not in request.user.authorities:
            raise NotPermissionException
    return True
