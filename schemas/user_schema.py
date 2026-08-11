from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        from_attributes = True
