from passlib.context import CryptContext
from typing import Union
from app.models import User
from fastapi_sqlalchemy import db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Union[bool, dict]:
    """
    Verify users password by reversing the bcrypt hash and
    returns a bool or the users object from database
    """
    user = db.session.query(User).filter_by(username=username).first()
    print(user, verify_password(password, user.password))
    if not user:
        return False
    return user if verify_password(password, user.password) else False
