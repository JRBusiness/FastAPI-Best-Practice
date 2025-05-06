import datetime
import uuid
from typing import Optional

from fastapi_camelcase import CamelModel

from app.api.users.schemas import UserStatus


class UserInfoResponse(CamelModel):
    username: str
    reveal_credits: float
    reverse_credits: float
    id: uuid.UUID
    created: datetime.datetime
    status: UserStatus
    api_key: str
    callback_url: Optional[str]
    is_admin: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LoginRequest(CamelModel):
    username: str
    password: str


class ResetPasswordRequest(CamelModel):
    password: str
    new_password: str


class LoginResponseData(CamelModel):
    access_token: Optional[str]
    user: UserInfoResponse
