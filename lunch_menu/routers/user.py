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
    return UserResponse(id = user["id"], name = user["name"], picture = user["picture"])

@router.delete("/user/session", name = "Logout", description = "Delete a user session", status_code = status.HTTP_204_NO_CONTENT)
async def logout(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
):
    await user_service.delete_session(authorization.credentials)

@router.put("/user/settings", name = "Save settings", description = "Save user settings", status_code = status.HTTP_204_NO_CONTENT)
async def settings_save(
    body: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
):
    await user_service.set_user_settings(authorization.credentials, await body.json())

@router.get("/user/settings", name = "Get settings", description = "Get user settings")
async def settings_get(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
) -> Any | None:
    settings = await user_service.get_user_settings(authorization.credentials)
    return settings

@router.delete("/user/settings", name = "Delete settings", description = "Delete user settings")
async def settings_delete(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    user_service: Annotated[UserService, Depends()]
) -> Any | None:
    await user_service.delete_user_settings(authorization.credentials)

