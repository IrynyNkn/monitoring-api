from pydantic import BaseModel


class UpdatePing(BaseModel):
    interval: int


class CreatePing(BaseModel):
    interval: int
    host: str
