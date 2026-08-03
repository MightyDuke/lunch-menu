from pydantic import BaseModel, RootModel
from lunch_menu.models.session import UserResponse

class VoteRequest(BaseModel):
    path: str

class VoteResponse(RootModel):
    root: dict[str, list[UserResponse]]