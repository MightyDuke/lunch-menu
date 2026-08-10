from pydantic import BaseModel

class SessionRequest(BaseModel):
    id_token: str

class SessionResponse(BaseModel):
    token: str

class UserResponse(BaseModel):
    name: str
    picture: str | None