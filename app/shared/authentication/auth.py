from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.shared.middleware import AuthenticationFailed
from config.settings import Settings


class Auth:
    hasher = CryptContext(schemes=["bcrypt"])
    secret = Settings.auth_key

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, user_id: str):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=365),
            "iat": datetime.now(timezone.utc),
            "scope": "access_token",
            "sub": user_id,
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
        except jwt.ExpiredSignatureError as e:
            print(e)
        except jwt.InvalidTokenError as e:
            print(e)

    def refresh_tokens(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                user_id = payload["sub"]
                return self.encode_token(user_id)
            raise AuthenticationFailed(detail="Invalid scope for token")
        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed(detail="Refresh token expired") from e
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(detail="Invalid refresh token") from e
