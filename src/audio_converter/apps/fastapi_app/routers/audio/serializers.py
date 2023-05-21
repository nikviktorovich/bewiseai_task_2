import pydantic


class AudioRead(pydantic.BaseModel):
    uuid: str
    user_id: int
    audio_url: str

    
    @pydantic.validator('uuid', pre=True)
    def convert_uuid_to_hex(cls, v) -> str:
        return v.hex


    class Config:
        orm_mode = True
