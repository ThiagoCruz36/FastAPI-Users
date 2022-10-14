from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    email: str
    name: str
    image_filename: Optional[str]
    thumb: Optional[str]


class UserRequest(BaseModel):
    email: str
    name: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
