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
    name = "Login",
    description = "Start a new user session"
)
async def login(
    body: SessionRequest, 
    session_service: Annotated[SessionService, Depends()]
) -> SessionResponse:
    token = await session_service.create_session(body.id_token)
    return SessionResponse(token = token)

@router.get(
    "/user",
    name = "User Information",
    description = "Get user information"
)
async def user(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    session_service: Annotated[SessionService, Depends()]
) -> UserResponse:
    token = authorization.credentials
    user = await session_service.get_user(token)

    return UserResponse(**user)

@router.delete(
    "/user",
    name = "Logout",
    description = "Delete a user session"
)
async def logout(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    session_service: Annotated[SessionService, Depends()]
) -> None:
    token = authorization.credentials
    await session_service.delete_session(token)