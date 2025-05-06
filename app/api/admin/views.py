import logging

from fastapi import APIRouter, Depends, Request
from fastapi_sqlalchemy import db

from app.api.admin.schemas import (
    ResetPasswordRequest,
    UserInfoResponse
)
from app.models import User
from app.shared.authentication.password_handler import get_hashed_password
from app.shared.middleware import (
    PermissionDenied,
)
from app.shared.middleware.auth import JWTBearer

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/admin.log",
)

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(JWTBearer())],
    tags=["admin"],
    include_in_schema=False,
)


@router.get(
    "/users/",
    response_model=list,
)
async def user_list(request: Request):
    current_user = (
        db.session.query(User)
        .filter_by(username=request.user.session.username)
        .first()
    )
    has_admin_perms(current_user)
    users = db.session.query(User).all()
    return [UserInfoResponse.from_orm(user) for user in users]



@router.post(
    "/users/reset-password/",
    response_model=UserInfoResponse,
)
async def reset_password(
    context: ResetPasswordRequest, request: Request
) -> UserInfoResponse:
    current_user = (
        db.session.query(User)
        .filter_by(username=request.user.session.username)
        .first()
    )
    has_admin_perms(current_user)
    user = db.session.query(User).filter_by(username=context.username).first()
    user.password = get_hashed_password(context.password)
    user.session.commit()
    return UserInfoResponse.from_orm(user)



def has_admin_perms(user):
    """
    Check if user has permission
    Args:
        user:  User

    Returns: bool

    """
    if not user.is_admin:
        raise PermissionDenied(detail="You do not have permission to create news.")
    return True
