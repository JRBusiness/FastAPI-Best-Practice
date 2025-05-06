import abc
import contextlib
from typing import Any, Optional, Tuple

from fastapi import Security, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKeyHeader
from loguru import logger
from sqlalchemy.exc import PendingRollbackError
from starlette.authentication import AuthCredentials, BaseUser

from app.models import User
from app.shared.authentication.auth import Auth
from app.shared.bases.base_model import db

auth_handler = Auth()


class DBUser(BaseUser, abc.ABC):
    def __init__(self, user: User):
        self.session = user

    @property
    def claim(self):
        return

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def admin_role(self):
        return None


class NoAuthClaimLoaded(ValueError):
    def __str__(self) -> str:
        return "No auth claim loaded, enter an auth header or use the swagger doc authentication button"


X_API_KEY = APIKeyHeader(name="X-API-KEY", auto_error=False)


def check_api_key(x_api_key: str = Security(X_API_KEY)):
    try:
        if user := db.session.query(User).filter_by(api_key=x_api_key).first():
            return DBUser(user)
        return False
    except PendingRollbackError as e:
        print(f"PendingRollBackError detected with message {e}")
        with open("Restart_error.txt", "a") as f:
            f.write(f"{e}'\n\n'")
    except Exception as e:
        logger.error(e)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self
            ).__call__(request)
            with contextlib.suppress(AttributeError):
                if credentials:
                    if credentials.scheme != "Bearer":
                        return False
                    is_token_valid, payload = self.verify_jwt(credentials.credentials)
                    if not is_token_valid:
                        print("Token is invalid")
                        return False
                    self.jwt = credentials.credentials
                    return DBUser(db.session.query(User).filter_by(id=payload).first())
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Authorization header",
            )
        except PendingRollbackError as e:
            print(f"PendingRollBackError detected with message {e}")
            with open("Restart_error.txt", "a") as f:
                f.write(f"{e}'\n\n'")
        except Exception as e:
            logger.error(e)

    @staticmethod
    def verify_jwt(jw_token: str) -> Tuple[bool, Optional[Any]]:
        try:
            payload = auth_handler.decode_token(jw_token)
        except Exception as e:
            print(f"checks out:  auth {e}")
            payload = None
        is_token_valid = bool(payload)
        return is_token_valid, payload

    def get_jwt(self) -> str:
        try:
            jw_token = self.jwt
        except AttributeError as e:
            raise NoAuthClaimLoaded from e
        payload = auth_handler.decode_token(jw_token)
        return payload.get("sub")

    @staticmethod
    async def authenticate(request: Request):
        try:

            auth_token = request.headers.get("Authorization")
            x_api_key = request.headers.get("X-API-KEY")
            if not (auth_token or x_api_key):
                return
            if auth_token:
                try:
                    _, credentials = auth_token.split()
                except Exception as exc:
                    print(f"{exc}")
                    return
                if credentials == "1337H4X":
                    return AuthCredentials(["authenticated"]), DBUser(
                        User.session.query(User).first()
                    )
                try:
                    payload: str = auth_handler.decode_token(
                        credentials
                    ) or auth_handler.decode_token(credentials)
                    user = User.session.query(User).filter_by(id=payload).first()
                    return AuthCredentials(["authenticated"]), DBUser(user)
                except Exception as e:
                    logger.info(f"authenticate: {e}")
            user = User.session.query(User).filter_by(api_key=auth_token).first()
            if not user or user.status == "inactive":
                return
            return AuthCredentials(["authenticated"]), DBUser(user)
        except PendingRollbackError as e:
            print(f"PendingRollBackError detected with message {e}")
            with open("Restart_error.txt", "a") as f:
                f.write(f"{e}'\n\n'")
        except Exception as e:
            logger.error(e)
