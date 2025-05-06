import datetime
import uuid
from enum import Enum
from typing import Optional

from fastapi_camelcase import CamelModel


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"



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


class UserUpdateRequest(CamelModel):
    status: Optional[UserStatus]
    api_key: str
    callback_url: Optional[str]
