from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from lunch_menu.models.user import SessionRequest, SessionResponse, UserResponse
from lunch_menu.services.user import UserService

security = HTTPBearer()
router = APIRouter(tags = ["User"])

@router.post("/user/session", name = "Login", description = "Start a new user session")
async def login(
    body: SessionRequest, 
    session_service: Annotated[UserService, Depends()]
) -> SessionResponse:
    token = await session_service.create_session(body.id_token)
    return SessionResponse(token = token)

@router.get("/user/profile", name = "User Profile", description = "Get user profile")
async def user(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    user = await user_service.get_user(authorization.credentials)
    return UserResponse(name = user["name"], picture = user["picture"])

@router.delete("/user/session", name = "Logout", description = "Delete a user session", status_code = status.HTTP_204_NO_CONTENT)
async def logout(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
):
    await user_service.delete_session(authorization.credentials)

@router.put("/user/layout", name = "Save layout", description = "Save user layout", status_code = status.HTTP_204_NO_CONTENT)
async def layout_save(
    body: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
):
    await user_service.set_layout(authorization.credentials, await body.json())

@router.get("/user/layout", name = "Get layout", description = "Get user layout")
async def layout_get(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
) -> Any | None:
    layout = await user_service.get_layout(authorization.credentials)
    return layout

@router.delete("/user/layout", name = "Delete layout", description = "Delete user layout")
async def layout_get(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
) -> Any | None:
    await user_service.delete_layout(authorization.credentials)

