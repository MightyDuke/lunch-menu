from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from lunch_menu.models.session import SessionRequest, SessionResponse, UserResponse
from lunch_menu.services.session import SessionService

auth_header = APIKeyHeader(name = "Auth")

router = APIRouter(
    tags = ["Session"]
)

@router.post("/user")
async def login(body: SessionRequest, session_service: Annotated[SessionService, Depends()]):
    token = await session_service.create_session(body.id_token)
    return SessionResponse(token = token)

@router.get("/user")
async def user(token: Annotated[str, Depends(auth_header)], session_service: Annotated[SessionService, Depends()]):
    user = await session_service.get_user(token)
    return UserResponse(**user)

@router.delete("/user")
async def logout(token: Annotated[str, Depends(auth_header)], session_service: Annotated[SessionService, Depends()]):
    await session_service.delete_session(token)