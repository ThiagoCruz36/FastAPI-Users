from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    email: str
    name: str
    image_filename: Optional[str]
    thumb: Optional[str]


class UserRequest(UserBase):
    ...

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
