from pydantic import BaseModel, Field


class UpdatePing(BaseModel):
    interval: int


class PausePing(BaseModel):
    pause_value: bool


class CreatePing(BaseModel):
    interval: int
    host: str


class User(BaseModel):
    email: str


class LoginUserData(User):
    password: str


class RegisterUserData(User):
    password: str
    repeat_password: str = Field(..., alias="repeatPassword")
