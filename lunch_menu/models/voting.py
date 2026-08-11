from pydantic import BaseModel, RootModel
from datetime import date
from lunch_menu.models.user import UserResponse

class VoteRequest(BaseModel):
    date: date
    establishment: str
    item: str

class VoteResponse(RootModel):
    root: dict[date, dict[str, list[UserResponse]]]