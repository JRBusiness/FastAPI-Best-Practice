from fastapi import APIRouter, Depends, Request

import app.api.auth.schemas as auth_schemas
import app.api.users.schemas as user_schemas
from app.models import User
from app.shared.authentication.auth import Auth
from app.shared.authentication.password_handler import get_hashed_password
from app.shared.bases.base_model import db
from app.shared.middleware import AuthenticationFailed, PermissionDenied
from app.shared.middleware.auth import JWTBearer

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.get(
    "/refresh_token",
    dependencies=[Depends(JWTBearer())],
    response_model=auth_schemas.LoginResponseData,
)
async def refresh_token(request: Request) -> auth_schemas.LoginResponseData:
    bearer = await JWTBearer().__call__(request)
    jwt_refresh = Auth().refresh_tokens(bearer)
    return auth_schemas.LoginResponseData(
        access_token=jwt_refresh, user=request.user.session.to_dict()
    )


@router.post("/login", response_model=auth_schemas.LoginResponseData)
async def login(context: auth_schemas.LoginRequest) -> auth_schemas.LoginResponseData:
    user = db.session.query(User).filter_by(username=context.username).first()
    if not user:
        raise AuthenticationFailed(detail="Invalid username.")
    if user.status == user_schemas.UserStatus.inactive:
        raise PermissionDenied(detail="This user is disabled.")
    auth_handler = Auth()
    if not auth_handler.verify_password(context.password, user.password):
        raise AuthenticationFailed(detail="Invalid password.")
    access_tokens = auth_handler.encode_token(str(user.id))
    return auth_schemas.LoginResponseData(access_token=access_tokens, user=user)


@router.post(
    "/reset-password",
    response_model=user_schemas.UserInfoResponse,
    dependencies=[Depends(JWTBearer())],
)
async def reset_password(
    context: auth_schemas.ResetPasswordRequest, request: Request
) -> user_schemas.UserInfoResponse:
    user = (
        db.session.query(User).filter_by(username=request.user.session.username).first()
    )
    if not user:
        raise AuthenticationFailed()
    if user.status == user_schemas.UserStatus.inactive:
        raise PermissionDenied(detail="This user is disabled.")
    auth_handler = Auth()
    if not auth_handler.verify_password(context.password, user.password):
        raise AuthenticationFailed(detail="Invalid password.")
    user.password = get_hashed_password(context.new_password)
    db.session.add(user)
    db.session.commit()
    return user_schemas.UserInfoResponse.from_orm(user)
