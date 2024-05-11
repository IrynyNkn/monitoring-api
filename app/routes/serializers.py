from enum import Enum

from pydantic import BaseModel, Field, EmailStr


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


class AlertGroup(str, Enum):
    ICMP_PING = "ICMP_PING"
    HTTP_PING = "HTTP_PING"
    KUBERNETES = "KUBERNETES"


class AlertType(str, Enum):
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    HEALTH_CHECK_FAILED = "HEALTH_CHECK_FAILED"
    HIGH_CPU_USAGE = "HIGH_CPU_USAGE"
    HIGH_MEMORY_USAGE = "HIGH_MEMORY_USAGE"


class CreateAlert(BaseModel):
    email: EmailStr
    for_: int
    repeat_alert: int
    alert_group: AlertGroup
    alert_type: AlertType
