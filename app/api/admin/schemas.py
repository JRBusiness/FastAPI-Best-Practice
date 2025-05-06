import datetime
import uuid
from typing import Optional, Union

from fastapi_camelcase import CamelModel
from pydantic import BaseModel

from app.api.users.schemas import UserStatus


class ResetPasswordRequest(CamelModel):
    username: str
    password: Optional[str]


class UserItem(CamelModel):
    username: str


class UserCreateRequest(UserItem):
    password: str



class UserInfoResponse(UserItem):
    id: uuid.UUID
    created: datetime.datetime
    status: UserStatus
    api_key: str
    callback_url: Optional[str]
    is_admin: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UpdateUserResponse(CamelModel):
    status: str
    detail: Union[UserInfoResponse, str]

