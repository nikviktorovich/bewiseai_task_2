import pydantic


class UserBase(pydantic.BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    access_token: str


    @pydantic.validator('access_token', pre=True)
    def convert_uuid_to_hex(cls, v) -> str:
        return v.hex


    class Config:
        orm_mode = True
