# app/schemas/user.py

from pydantic import BaseModel


class UserBase(BaseModel):
    clerk_id: str
    name: str | None = None
    email: str | None = None
    avatarUrl: str | None = None


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }