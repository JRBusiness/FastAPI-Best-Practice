import secrets

from fastapi import APIRouter, Depends, Request

import app.api.users.schemas as user_schemas
from app.models import User
from app.shared.bases.base_model import db
from app.shared.middleware.auth import JWTBearer, auth_handler

router = APIRouter(
    prefix="/api/users",
    dependencies=[Depends(JWTBearer())],
    tags=["users"],
)


@router.get(
    "/me",
    response_model=user_schemas.UserInfoResponse,
)
async def get_user_info(request: Request):
    if user := db.session.query(User).filter_by(id=request.user.session.id).first():
        return user_schemas.UserInfoResponse.from_orm(user)


@router.post(
    "/me/reset-api-key",
    response_model=user_schemas.UserInfoResponse,
)
async def update_user(request: Request):
    user = db.session.query(User).filter_by(id=request.user.session.id).first()
    new_api_key = secrets.token_urlsafe(36)
    user.api_key = new_api_key
    db.session.add(user)
    db.session.commit()
    return user_schemas.UserInfoResponse.from_orm(user)
