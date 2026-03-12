from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import bcrypt
import jwt

from src.core.setting import Settings


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> Optional[str]:
    if not Settings.JWT_SECRET_KEY:
        return None

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update(
        {
            "exp": int(expire.timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }
    )

    encoded_jwt = jwt.encode(
        to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str | None:
    if not Settings.JWT_SECRET_KEY:
        return None

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=Settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update(
        {
            "exp": int(expire.timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }
    )

    encoded_jwt = jwt.encode(
        to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def create_token_pair(data: dict) -> Dict[str, str | None]:
    """
    Returns both tokens at once — after successful login/register.
    """
    return {
        "access_token": create_access_token(data),
        "refresh_token": create_refresh_token(data),
        "token_type": "bearer",
    }
