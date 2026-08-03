from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from lunch_menu.models.session import SessionRequest, SessionResponse, UserResponse
from lunch_menu.services.session import SessionService

security = HTTPBearer()

router = APIRouter(
    tags = ["Session"]
)

@router.post(
    "/user",
    name = "Start session",
    description = "Start a new session"
)
async def login(body: SessionRequest, session_service: Annotated[SessionService, Depends()]):
    token = await session_service.create_session(body.id_token)
    return SessionResponse(token = token)

@router.get(
    "/user",
    name = "Get User",
    description = "Get user information"
)
async def user(authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], session_service: Annotated[SessionService, Depends()]):
    token = authorization.credentials

    user = await session_service.get_user(token)
    return UserResponse(**user)

@router.delete(
    "/user",
    name = "Delete session",
    description = "Delete a session"
)
async def logout(authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], session_service: Annotated[SessionService, Depends()]):
    token = authorization.credentials

    await session_service.delete_session(token)