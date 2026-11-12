from pydantic import BaseModel, RootModel
from datetime import date
from lunch_menu.models.user import UserResponse

class VoteRequest(BaseModel):
    date: date
    establishment: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "date": "2026-08-11",
                "establishment": "bo-asi"
            }]
        }
    }

class VoteResponse(RootModel):
    root: dict[date, dict[str, list[UserResponse]]]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "2026-11-06": [{
                        "name": "Prokop Buben",
                        "id": "b2JzZXJ2ZWZpZWxkbGluZWRyeXNwaXRlbmV3c2RpcnQ=",
                        "picture": "https://example.com/avatar.png"
                    },
                    {
                        "name": "Tomáš Jedno",
                        "id": "cGlua2VhcmxpZXJjb3VwbGVhbm90aGVyc3dlZXR0b20=",
                        "picture": "https://example.com/avatar2.jpg"
                    }
                ]
            }]
        }
    }