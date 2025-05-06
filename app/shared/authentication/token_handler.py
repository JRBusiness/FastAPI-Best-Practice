from typing import Optional

from itsdangerous import URLSafeTimedSerializer
from app import logger

from config.settings import Settings


def generate_confirmation_token(data: str) -> str:
    """
    Serialize the given token into a base64 object with custom
    salt to provide a basic encryption scheme to the returned data
    """
    serializer = URLSafeTimedSerializer(Settings.auth_key)
    return serializer.dumps(data, salt=Settings.salt)


def confirm_token(token, expiration=10000000) -> Optional[str]:
    """
    Deserialize token into base object or return false if the
    token can not be verified with the provided salt
    """
    serializer = URLSafeTimedSerializer(Settings.auth_key)
    try:
        data = serializer.loads(token, salt=Settings.salt, max_age=expiration)
    except Exception as e:
        print(f"checks out config token: {e}")
        return None
    return data
