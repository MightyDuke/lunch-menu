from pydantic import BaseModel

class SessionRequest(BaseModel):
    id_token: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id_token": "bjiwQW7TSfl4YJmVIIiqkt...",
            }]
        }
    }

class SessionResponse(BaseModel):
    token: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "token": "EccVlFVk5Uihhz5DxofjggGGmyOkxH9UvkUA9mleURQVlAw9V4sozWrbs5lZ5aoR",
            }]
        }
    }

class UserResponse(BaseModel):
    name: str
    picture: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Prokop Buben",
                "picture": "https://example.com/avatar.png"
            }]
        }
    }