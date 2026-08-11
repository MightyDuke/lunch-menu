from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from lunch_menu.models.user import SessionRequest, SessionResponse, UserResponse
from lunch_menu.services.user import UserService

security = HTTPBearer()
router = APIRouter(tags = ["User"])

@router.post("/user/login", name = "Login", description = "Start a new user session")
async def login(
    body: SessionRequest, 
    session_service: Annotated[UserService, Depends()]
) -> SessionResponse:
    token = await session_service.create_session(body.id_token)
    return SessionResponse(token = token)

@router.get("/user/profile", name = "User Profile", description = "Get user profile")
async def user(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    session_service: Annotated[UserService, Depends()]
) -> UserResponse:
    token = authorization.credentials
    user = await session_service.get_user(token)

    return UserResponse(**user)

@router.post("/user/logout", name = "Logout", description = "Delete a user session")
async def logout(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    session_service: Annotated[UserService, Depends()]
):
    token = authorization.credentials
    await session_service.delete_session(token)

    return Response(status_code = status.HTTP_204_NO_CONTENT)