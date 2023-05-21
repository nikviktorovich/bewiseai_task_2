import pydantic


class AudioRead(pydantic.BaseModel):
    uuid: str
    user_id: int
    audio_url: str

    class Config:
        orm_mode = True
