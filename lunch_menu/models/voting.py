from pydantic import BaseModel, RootModel
from datetime import date
from lunch_menu.models.user import UserResponse

class VoteRequest(BaseModel):
    date: date
    establishment: str
    item: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "date": "2026-08-11",
                "establishment": "bo-asi",
                "item": "2"
            }]
        }
    }

class VoteResponse(RootModel):
    root: dict[date, dict[str, list[UserResponse]]]