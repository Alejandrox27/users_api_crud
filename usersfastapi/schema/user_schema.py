from pydantic import BaseModel

class UserSchema(BaseModel):
    id: str | None = None
    name: str
    username: str
    user_passw: str

class DataUser(BaseModel):
    username: str
    user_passw: str