import pydantic


class UserBase(pydantic.BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    access_token: str

    class Config:
        orm_mode = True
